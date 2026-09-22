#!/usr/bin/env bash
# Hub release — default: single session (branch → PR → wait → tag). Two-step: prepare + finish.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${ROOT}"

DRY_RUN=0
YES=0
NO_PUSH=0
BUMP=""
MSG=""
REMOTE="${NLC_RELEASE_REMOTE:-origin}"
BASE_BRANCH="${NLC_RELEASE_BASE_BRANCH:-main}"
MODE="single"
# Commit to tag (PR merge / squash commit on main — not a later main HEAD).
MERGE_COMMIT_SHA=""

usage() {
  cat <<'EOF'
Usage:
  ./release                 Single session: branch, push, PR link, wait for merge, tag
  ./release prepare         Two-step: branch + push only (resume with ./release finish)
  ./release finish          Two-step: on main after merge — verify, tag, push tag

Options:
  --two-step                Same as ./release prepare
  --bump patch|minor|major|keep
  --message "text"
  --yes                     Auto-yes confirms (single-step still waits for Enter after PR)
  --no-push
  --dry-run
  -h, --help

See docs/adoption/RELEASE.md
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    single|prepare|finish|tag)
      MODE="$1"
      [[ "$MODE" == "tag" ]] && MODE="finish"
      ;;
    --two-step) MODE="prepare" ;;
    --dry-run) DRY_RUN=1 ;;
    --yes) YES=1 ;;
    --no-push) NO_PUSH=1 ;;
    --bump) BUMP="${2:-}"; shift ;;
    --message) MSG="${2:-}"; shift ;;
    -h|--help) usage; exit 0 ;;
    --*) echo "Unknown option: $1" >&2; usage; exit 2 ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 2
      ;;
  esac
  shift
done

run() {
  if [[ "${DRY_RUN}" -eq 1 ]]; then
    echo "DRY_RUN: $*"
    return 0
  fi
  "$@"
}

confirm() {
  local prompt="$1"
  local default_y="${2:-0}"
  if [[ "${YES}" -eq 1 ]]; then
    return 0
  fi
  if [[ "${default_y}" -eq 1 ]]; then
    read -r -p "${prompt} [Y/n] " ans
    [[ -z "${ans}" || "${ans}" =~ ^[Yy] ]]
    return
  fi
  read -r -p "${prompt} [y/N] " ans
  [[ "${ans}" =~ ^[Yy] ]]
}

release_branch_name() {
  echo "release/v${1}"
}

github_compare_url() {
  local rel_branch="$1"
  local url slug
  url="$(git remote get-url "${REMOTE}" 2>/dev/null || true)"
  if [[ "${url}" =~ github\.com[:/]([^/]+/[^/.]+)(\.git)?$ ]]; then
    slug="${BASH_REMATCH[1]}"
    echo "https://github.com/${slug}/compare/${BASE_BRANCH}...${rel_branch}?expand=1"
    return 0
  fi
  return 1
}

# Resolve the commit GitHub landed on main for this release PR (not origin/main HEAD).
resolve_merged_commit_sha() {
  local rel_branch="$1"
  local release_sha="$2"
  local sha="" main_ref="${REMOTE}/${BASE_BRANCH}"

  if command -v gh >/dev/null 2>&1; then
    sha="$(gh pr list --head "${rel_branch}" --base "${BASE_BRANCH}" --state merged \
      --json mergeCommit -q '.[0].mergeCommit.oid' 2>/dev/null || true)"
    if [[ "${sha}" == "null" || -z "${sha}" ]]; then
      sha=""
    fi
  fi

  if [[ -z "${sha}" ]]; then
    run git fetch "${REMOTE}" "${BASE_BRANCH}" "${rel_branch}" 2>/dev/null || true
    if git merge-base --is-ancestor "${release_sha}" "${main_ref}" 2>/dev/null; then
      sha="$(git rev-list --ancestry-path "${release_sha}..${main_ref}" 2>/dev/null | tail -n 1 || true)"
    fi
  fi

  if [[ -z "${sha}" ]]; then
    return 1
  fi
  echo "${sha}"
}

release_notes_file() {
  echo "docs/adoption/RELEASE-v${1}.md"
}

assert_release_notes_on_commit() {
  local ver="$1"
  local path
  path="$(release_notes_file "${ver}")"
  if ! python3 tools/nlc_release_notes.py --check --version "${ver}"; then
    echo "  Release notes invalid or Highlights missing: ${path}" >&2
    exit 1
  fi
  if ! git cat-file -e "HEAD:${path}" 2>/dev/null; then
    echo "  ${path} must be committed on this branch before continuing." >&2
    exit 1
  fi
}

ensure_release_notes() {
  local ver="$1"
  local ref="$2"
  local path
  path="$(release_notes_file "${ver}")"
  local prev_tag=""
  local ans=""

  echo ""
  echo "Step 4/9 — release notes (after target + verify gates; before version bump; ADR 0022)"
  echo "  File: ${path}"
  prev_tag="$(python3 tools/nlc_release_notes.py --version "${ver}" --previous-tag --to "${ref}" 2>/dev/null || true)"
  if [[ -n "${prev_tag}" ]]; then
    echo "  Last git tag on this history: ${prev_tag} (not integrity/nlc-version.json)"
    echo "  Draft range: ${prev_tag} .. ${ref}"
  else
    echo "  No prior v*.*.* tag reachable from ${ref} — draft uses recent commits."
  fi
  echo "  Regenerate: python3 tools/nlc_release_notes.py --write-draft --version ${ver} --to ${ref}"

  if [[ ! -f "${path}" ]]; then
    if [[ "${DRY_RUN}" -eq 1 ]]; then
      echo "DRY_RUN: missing ${path} — release blocked." >&2
      exit 1
    fi
    run python3 tools/nlc_release_notes.py --write-draft --version "${ver}" --to "${ref}"
    echo "  Created draft — you must fill Highlights before continuing."
  elif confirm "Refresh the auto-generated Changes section in ${path}?" 0; then
    run python3 tools/nlc_release_notes.py --refresh-changes --version "${ver}" --to "${ref}"
  fi

  if [[ "${YES}" -eq 1 ]]; then
    if ! python3 tools/nlc_release_notes.py --check --version "${ver}"; then
      echo "  --yes does not skip release notes. Fill Highlights in ${path} and re-run." >&2
      exit 1
    fi
    echo "  RELEASE_NOTES:MET"
    return 0
  fi

  while ! python3 tools/nlc_release_notes.py --check --version "${ver}"; do
    echo "" >&2
    echo "  RELEASE_NOTES:NOT_MET — Highlights required in ${path}" >&2
    if [[ "${DRY_RUN}" -eq 1 ]]; then
      exit 1
    fi
    read -r -p "Edit ${path} now in \${EDITOR:-nano}? [Y/n] " ans
    if [[ -n "${ans}" && ! "${ans}" =~ ^[Yy] ]]; then
      echo "  Stopped: release notes required." >&2
      exit 1
    fi
    "${EDITOR:-nano}" "${path}"
  done
  echo "  RELEASE_NOTES:MET"
}

release_target_gate() {
  local target="$1"
  echo ""
  echo "Step 2/9 — release target preflight (migrations for v${target}; ADR 0014)"
  if python3 tools/nlc_release_target_preflight.py --check --target "${target}"; then
    return 0
  fi
  echo ""
  if confirm "Scaffold missing noop migration units for v${target}?" 1; then
    if python3 tools/nlc_release_target_preflight.py --ensure-noop --target "${target}" \
      && python3 tools/nlc_release_target_preflight.py --check --target "${target}"; then
      return 0
    fi
  fi
  python3 tools/nlc_release_target_preflight.py --check --print-agent-prompt --target "${target}" \
    >/dev/null 2>&1 || true
  echo "  Stopped before notes, branch, or version bump." >&2
  exit 1
}

block_until_release_notes_met() {
  local ver="$1"
  local path
  path="$(release_notes_file "${ver}")"
  if [[ ! -f "${path}" ]]; then
    echo "  Blocked: missing ${path}" >&2
    exit 1
  fi
  if ! python3 tools/nlc_release_notes.py --check --version "${ver}"; then
    echo "  Blocked: release notes not valid for v${ver}." >&2
    exit 1
  fi
}

warn_if_main_moved_past_merge() {
  local merge_sha="$1"
  local main_ref="${REMOTE}/${BASE_BRANCH}"
  run git fetch "${REMOTE}" "${BASE_BRANCH}" 2>/dev/null || true
  local head
  head="$(git rev-parse "${main_ref}" 2>/dev/null || true)"
  if [[ -n "${head}" && "${head}" != "${merge_sha}" ]]; then
    if ! git merge-base --is-ancestor "${merge_sha}" "${head}" 2>/dev/null; then
      echo "  Warning: ${BASE_BRANCH} HEAD is not a descendant of merge commit." >&2
      return
    fi
    echo "  Note: ${BASE_BRANCH} has commits after this merge; tagging merge commit ${merge_sha:0:12} only (not HEAD ${head:0:12})."
  fi
}

print_pr_help() {
  local rel_branch="$1"
  local title="$2"
  echo ""
  echo "Open a PR: ${rel_branch} → ${BASE_BRANCH}"
  if compare="$(github_compare_url "${rel_branch}")"; then
    echo "  ${compare}"
  fi
  if command -v gh >/dev/null 2>&1; then
    echo "  gh pr create --base ${BASE_BRANCH} --head ${rel_branch} --title \"${title}\" --web"
  fi
}

ensure_release_branch() {
  local rel_branch="$1"
  local branch_now
  branch_now="$(git rev-parse --abbrev-ref HEAD)"

  if [[ "${branch_now}" == "${rel_branch}" ]]; then
    return 0
  fi

  if [[ "${branch_now}" == "${BASE_BRANCH}" ]]; then
    echo ""
    echo "You are on ${BASE_BRANCH}. Most teams protect it — release commits belong on a branch."
    if ! confirm "Create and use ${rel_branch}?" 1; then
      echo "  Stopped. Checkout a branch or run from a feature branch." >&2
      exit 1
    fi
  fi

  if git show-ref --verify --quiet "refs/heads/${rel_branch}"; then
    if ! confirm "Check out existing ${rel_branch}?"; then
      exit 1
    fi
    run git checkout "${rel_branch}"
  else
    if ! confirm "Create branch ${rel_branch} from ${branch_now}?"; then
      exit 1
    fi
    run git checkout -b "${rel_branch}"
  fi
}

wait_for_merge_on_main() {
  local sha="$1"
  local rel_branch="$2"

  echo ""
  print_pr_help "${rel_branch}" "${MSG}"
  echo ""
  echo "Merge the PR when CI is green, then return here."
  if [[ "${DRY_RUN}" -eq 1 ]]; then
    echo "DRY_RUN: would wait for Enter, then verify merge and tag."
    return 0
  fi

  while true; do
    read -r -p "Press Enter when merged to ${BASE_BRANCH} (Ctrl-C to stop — use ./release finish later)... " _
    local merged
    merged="$(resolve_merged_commit_sha "${rel_branch}" "${sha}" || true)"
    if [[ -n "${merged}" ]]; then
      MERGE_COMMIT_SHA="${merged}"
      echo "  Merge commit to tag: ${MERGE_COMMIT_SHA:0:12}"
      warn_if_main_moved_past_merge "${MERGE_COMMIT_SHA}"
      return 0
    fi
    echo "  PR not merged yet (or could not resolve merge commit). Check the PR and try again." >&2
  done
}

cmd_finish() {
  TARGET="$(python3 tools/nlc_release_bump.py --current)"
  TAG="v${TARGET}"
  RELEASE_BRANCH="$(release_branch_name "${TARGET}")"
  local tag_at="${MERGE_COMMIT_SHA}"
  local prev_branch
  prev_branch="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo HEAD)"

  echo ""
  echo "Natural Language Coding — release finish (tag after merge)"
  echo "  Version: ${TARGET}  Tag: ${TAG}"
  echo ""

  if [[ -z "${tag_at}" ]]; then
    run git fetch "${REMOTE}" "${BASE_BRANCH}" "${RELEASE_BRANCH}" 2>/dev/null || true
    local release_sha
    release_sha="$(git rev-parse "${REMOTE}/${RELEASE_BRANCH}" 2>/dev/null || true)"
    if [[ -z "${release_sha}" ]]; then
      release_sha="$(git rev-parse "${RELEASE_BRANCH}" 2>/dev/null || true)"
    fi
    if [[ -z "${release_sha}" ]]; then
      echo "Cannot find ${RELEASE_BRANCH} to resolve merge commit." >&2
      echo "  Run ./release finish from a repo with the merged PR, or use single-session ./release." >&2
      exit 1
    fi
    tag_at="$(resolve_merged_commit_sha "${RELEASE_BRANCH}" "${release_sha}")" || tag_at=""
    if [[ -z "${tag_at}" ]]; then
      echo "No merged PR found for ${RELEASE_BRANCH} → ${BASE_BRANCH}." >&2
      exit 1
    fi
  fi

  warn_if_main_moved_past_merge "${tag_at}"
  echo "  Tag target (merge commit): ${tag_at:0:12}"

  echo ""
  echo "Step 1/4 — verify at merge commit"
  run git checkout "${tag_at}"
  run python3 tools/nlc.py --project . verify

  echo ""
  echo "Step 2/4 — release notes at merge commit"
  if ! python3 tools/nlc_release_notes.py --check --version "${TARGET}"; then
    echo "  Notes must be on the merged release branch (Highlights filled)." >&2
    echo "  Fix on a follow-up PR or re-run ./release prepare with notes, then merge again." >&2
    run git checkout "${prev_branch}" 2>/dev/null || true
    exit 1
  fi

  echo ""
  echo "Step 3/4 — annotated tag ${TAG} on ${tag_at:0:12}"
  if git rev-parse -q --verify "refs/tags/${TAG}" >/dev/null; then
    local existing
    existing="$(git rev-parse "${TAG}^{commit}")"
    if [[ "${existing}" == "${tag_at}" ]]; then
      echo "  Tag ${TAG} already points at merge commit."
    else
      echo "  Tag ${TAG} exists at ${existing:0:12} (not merge commit)."
      if ! confirm "Move tag ${TAG} to merge commit ${tag_at:0:12}?"; then
        run git checkout "${prev_branch}" 2>/dev/null || true
        exit 1
      fi
      run git tag -f -a "${TAG}" -m "Natural Language Coding hub ${TARGET}"
    fi
  else
    run git tag -a "${TAG}" -m "Natural Language Coding hub ${TARGET}"
  fi

  echo ""
  echo "Step 4/4 — push tag ${TAG} to ${REMOTE}"
  if [[ "${NO_PUSH}" -eq 1 ]]; then
    run git checkout "${prev_branch}" 2>/dev/null || run git checkout "${BASE_BRANCH}" 2>/dev/null || true
    echo "  --no-push: tag on ${tag_at:0:12}"
    echo "RELEASE:READY_LOCAL tag=${TAG} commit=${tag_at}"
    exit 0
  fi

  if confirm "Push tag ${TAG}?" 1; then
    run git push "${REMOTE}" "${TAG}"
  else
    echo "  Skipped. When ready: git push ${REMOTE} ${TAG}"
    run git checkout "${prev_branch}" 2>/dev/null || true
    exit 0
  fi

  run git checkout "${prev_branch}" 2>/dev/null || run git checkout "${BASE_BRANCH}" 2>/dev/null || true

  echo ""
  echo "RELEASE:TAG_PUSHED ${TAG} @ ${tag_at:0:12}"
  echo "  GitHub Actions will build the tarball and publish the Release."
}

run_prepare_core() {
  echo ""
  if [[ "${MODE}" == "single" ]]; then
    echo "Natural Language Coding — release (single session)"
  else
    echo "Natural Language Coding — release prepare (two-step)"
  fi
  echo "  Repo: ${ROOT}"
  echo ""

  echo "Step 0/9 — preflight (version/tag + shipped baseline)"
  run python3 tools/nlc_release_preflight.py --check

  CURRENT="$(python3 tools/nlc_release_bump.py --current)"
  SUGGEST="$(python3 tools/nlc_release_bump.py --suggest 2>/dev/null | head -1)"

  if [[ -z "${BUMP}" ]]; then
    echo ""
    echo "Step 1/9 — release type (ADR 0022):"
    echo "  Current integrity/nlc-version.json: ${CURRENT}"
    echo "  Suggested bump from your changes: ${SUGGEST} (hint only — not a default choice)"
    python3 tools/nlc_release_bump.py --suggest >/dev/null
    echo ""
    PATCH_NEXT="$(python3 -c "m,mi,p='${CURRENT}'.split('.'); print(f'{m}.{mi}.{int(p)+1}')")"
    MINOR_NEXT="$(python3 -c "m,mi,p='${CURRENT}'.split('.'); print(f'{m}.{int(mi)+1}.0')")"
    MAJOR_NEXT="$(python3 -c "m,mi,p='${CURRENT}'.split('.'); print(f'{int(m)+1}.0.0')")"
    echo "  p = patch  → ${PATCH_NEXT}"
    echo "  m = minor  → ${MINOR_NEXT}"
    echo "  M = major  → ${MAJOR_NEXT}"
    echo "  k = keep   → ship ${CURRENT} as-is (no version file change)"
    echo ""
    while [[ -z "${BUMP}" ]]; do
      read -r -p "Choice [p/m/M/k] (no default — suggested: ${SUGGEST}): " choice
      case "${choice}" in
        p|patch) BUMP="patch" ;;
        m|minor) BUMP="minor" ;;
        M|major) BUMP="major" ;;
        k|keep) BUMP="keep" ;;
        "")
          echo "  Pick p, m, M, or k." >&2
          ;;
        *)
          echo "  Invalid choice." >&2
          ;;
      esac
    done
  fi

  TARGET="$(python3 tools/nlc_release_bump.py --peek "${BUMP}")"
  RELEASE_BRANCH="$(release_branch_name "${TARGET}")"
  echo ""
  echo "  Target version for this run: ${TARGET}"

  release_target_gate "${TARGET}"

  echo ""
  echo "Step 3/9 — verify-deep (on main at shipped version; fail before notes or bump)"
  run python3 tools/nlc.py --project . verify-deep

  ensure_release_notes "${TARGET}" "HEAD"
  block_until_release_notes_met "${TARGET}"

  echo ""
  echo "Step 5/9 — branch ${RELEASE_BRANCH} (version bump stays off main until here)"
  ensure_release_branch "${RELEASE_BRANCH}"

  echo ""
  echo "Step 6/9 — write version (on release branch only)"
  if [[ "${BUMP}" == "keep" ]]; then
    echo "  Keeping ${TARGET}"
  else
    run python3 tools/nlc_release_bump.py --apply "${BUMP}"
    TARGET="$(python3 tools/nlc_release_bump.py --current)"
    echo "  Bumped integrity/nlc-version.json to ${TARGET}"
  fi

  echo ""
  echo "Step 7/9 — verify-deep (target version + full CI)"
  run python3 tools/nlc.py --project . verify-deep

  echo ""
  echo "Step 8/9 — release prep"
  export NLC_RELEASE_ORCHESTRATOR=1
  run bash scripts/nlc-release-prep.sh
  unset NLC_RELEASE_ORCHESTRATOR

  if [[ -z "${MSG}" ]]; then
    MSG="Release v${TARGET}"
  fi

  echo ""
  echo "Step 9/9 — commit release artifacts"

  local notes_path need_commit
  notes_path="$(release_notes_file "${TARGET}")"
  need_commit=0
  if ! git diff --quiet || ! git diff --cached --quiet; then
    need_commit=1
  fi
  if ! git cat-file -e "HEAD:${notes_path}" 2>/dev/null; then
    need_commit=1
  fi

  if [[ "${need_commit}" -eq 0 ]]; then
    echo "  Working tree clean."
    assert_release_notes_on_commit "${TARGET}"
  else
    if [[ ! -f "${notes_path}" ]] || ! python3 tools/nlc_release_notes.py --check --version "${TARGET}"; then
      echo "  Stopped: fix release notes before commit (${notes_path})." >&2
      exit 1
    fi
    git status -sb
    if confirm "Commit all changes with message: \"${MSG}\"?" 1; then
      run git add -A
      run git commit -m "${MSG}"
      assert_release_notes_on_commit "${TARGET}"
    else
      echo "  Stopped: commit declined." >&2
      exit 1
    fi
  fi

  RELEASE_SHA="$(git rev-parse HEAD)"
  echo ""
  echo "Push branch (no tag yet)"
  assert_release_notes_on_commit "${TARGET}"
  if [[ "${NO_PUSH}" -eq 1 ]]; then
    echo "  --no-push: commit on ${RELEASE_BRANCH} at ${RELEASE_SHA}"
    return 0
  fi

  if confirm "Push ${RELEASE_BRANCH} to ${REMOTE}?" 1; then
    run git push -u "${REMOTE}" "${RELEASE_BRANCH}"
  else
    echo "  Skipped push. When ready:"
    echo "    git push -u ${REMOTE} ${RELEASE_BRANCH}"
    exit 0
  fi

  echo ""
  echo "RELEASE:BRANCH_PUSHED ${RELEASE_BRANCH} @ ${RELEASE_SHA}"
}

cmd_prepare() {
  run_prepare_core
  if [[ "${NO_PUSH}" -eq 1 ]]; then
    echo ""
    echo "RELEASE:READY_LOCAL branch=$(release_branch_name "$(python3 tools/nlc_release_bump.py --current)")"
    echo "  Next: PR → merge → ./release finish"
    exit 0
  fi
  TARGET="$(python3 tools/nlc_release_bump.py --current)"
  RELEASE_BRANCH="$(release_branch_name "${TARGET}")"
  print_pr_help "${RELEASE_BRANCH}" "${MSG:-Release v${TARGET}}"
  echo ""
  echo "  After merge: git checkout ${BASE_BRANCH} && git pull && ./release finish"
}

cmd_single() {
  run_prepare_core
  if [[ "${NO_PUSH}" -eq 1 ]]; then
    echo "  --no-push: cannot complete single-session tag without push."
    echo "  Use ./release finish after you push and merge."
    exit 0
  fi
  TARGET="$(python3 tools/nlc_release_bump.py --current)"
  RELEASE_BRANCH="$(release_branch_name "${TARGET}")"
  RELEASE_SHA="$(git rev-parse HEAD)"
  wait_for_merge_on_main "${RELEASE_SHA}" "${RELEASE_BRANCH}"
  cmd_finish
}

case "${MODE}" in
  finish) cmd_finish ;;
  prepare) cmd_prepare ;;
  single) cmd_single ;;
  *)
    echo "Unknown mode: ${MODE}" >&2
    exit 2
    ;;
esac
