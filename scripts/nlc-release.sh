#!/usr/bin/env bash
# Hub release — one command, resumable (ADR 0039). Tag only after tag gate (ADR 0038–0040).
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
  ./release                 Prepare (if needed) → PR → wait for merge → tag (resumes automatically)
  ./release prepare         Legacy alias — same prepare leg; prefer ./release
  ./release finish          Legacy alias — tag leg only if merge already done; prefer ./release

Options:
  --two-step                Same as ./release prepare
  --bump patch|minor|major|keep
  --message "text"
  --yes                     Auto-yes for routine confirms (not tag move; not release notes)
  --no-push
  --dry-run
  -h, --help

See docs/adoption/RELEASE.md (ADR 0039)
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

confirm_tag_move() {
  local prompt="$1"
  if [[ -n "${NLC_RELEASE_ALLOW_RETAG:-}" ]]; then
    return 0
  fi
  read -r -p "${prompt} [y/N] (requires explicit yes; --yes does not apply) " ans
  [[ "${ans}" =~ ^[Yy] ]]
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

  if git show-ref --verify --quiet "refs/heads/${rel_branch}"; then
    echo "  Using existing ${rel_branch}."
    run git checkout "${rel_branch}"
    return 0
  fi

  if [[ "${branch_now}" == "${BASE_BRANCH}" ]]; then
    echo "  Creating ${rel_branch} from ${BASE_BRANCH} (release commits stay off ${BASE_BRANCH})."
    run git checkout -b "${rel_branch}"
    return 0
  fi

  echo ""
  echo "  You are on ${branch_now}, not ${BASE_BRANCH}."
  if [[ "${YES}" -eq 1 ]]; then
    echo "  --yes: creating ${rel_branch} from ${branch_now}."
    run git checkout -b "${rel_branch}"
    return 0
  fi
  if ! confirm "Create ${rel_branch} from ${branch_now}? (Recommended: git checkout ${BASE_BRANCH} first)" 0; then
    echo "  Stopped. From ${BASE_BRANCH}, ./release creates ${rel_branch} automatically." >&2
    exit 1
  fi
  run git checkout -b "${rel_branch}"
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

read_version_at_commit() {
  python3 -c "import sys; sys.path.insert(0,'tools'); from nlc_release_record import read_version_at; v=read_version_at('$1'); print(v or '')"
}

release_context_wizard() {
  local branch_now
  branch_now="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo HEAD)"
  echo ""
  echo "Step context — release branches (ADR 0040)"
  python3 tools/nlc_release_context.py --remote "${REMOTE}" --base "${BASE_BRANCH}" --list-branches || true
  if [[ "${branch_now}" == "${BASE_BRANCH}" ]]; then
    echo "  You are on ${BASE_BRANCH}. ./release will create or resume release/v*."
  fi
}

cmd_finish() {
  local tag_at="${MERGE_COMMIT_SHA}"
  local release_branch="${RESUME_BRANCH:-}"
  local prev_branch
  prev_branch="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo HEAD)"

  echo ""
  echo "Natural Language Coding — release tag leg"

  if [[ -z "${release_branch}" ]]; then
    local guess
    guess="$(python3 tools/nlc_release_bump.py --current)"
    release_branch="$(release_branch_name "${guess}")"
  fi

  if [[ -z "${tag_at}" ]]; then
    run git fetch "${REMOTE}" "${BASE_BRANCH}" "${release_branch}" 2>/dev/null || true
    local release_sha
    release_sha="$(git rev-parse "${REMOTE}/${release_branch}" 2>/dev/null || true)"
    if [[ -z "${release_sha}" ]]; then
      release_sha="$(git rev-parse "${release_branch}" 2>/dev/null || true)"
    fi
    if [[ -z "${release_sha}" ]]; then
      echo "Cannot find ${release_branch} to resolve merge commit." >&2
      echo "  Fix: run ./release (resumes from release/v* state)." >&2
      exit 1
    fi
    tag_at="$(resolve_merged_commit_sha "${release_branch}" "${release_sha}")" || tag_at=""
    if [[ -z "${tag_at}" ]]; then
      echo "No merged PR found for ${release_branch} → ${BASE_BRANCH}." >&2
      echo "  Fix: merge the release PR, or run ./release to resume." >&2
      exit 1
    fi
  fi

  TARGET="$(read_version_at_commit "${tag_at}")"
  if [[ -z "${TARGET}" ]]; then
    echo "RELEASE:NOT_MET cannot read integrity/nlc-version.json at merge commit ${tag_at:0:12}" >&2
    exit 1
  fi
  TAG="v${TARGET}"
  release_branch="$(release_branch_name "${TARGET}")"

  warn_if_main_moved_past_merge "${tag_at}"
  echo "  Tag target (merge commit): ${tag_at:0:12}"
  echo "  Version from commit: ${TARGET}  Tag: ${TAG}"

  echo ""
  echo "Step 1/3 — release tag gate (record, notes, migrations, verify-deep)"
  if ! python3 tools/nlc_release_tag_gate.py --check --commit "${tag_at}" --tag "${TAG}"; then
    run git checkout "${prev_branch}" 2>/dev/null || true
    exit 1
  fi

  echo ""
  echo "Step 2/3 — annotated tag ${TAG} on ${tag_at:0:12}"
  if git rev-parse -q --verify "refs/tags/${TAG}" >/dev/null; then
    local existing
    existing="$(git rev-parse "${TAG}^{commit}")"
    if [[ "${existing}" == "${tag_at}" ]]; then
      echo "  Tag ${TAG} already points at merge commit."
    else
      echo "  Tag ${TAG} exists at ${existing:0:12} (not merge commit)."
      if ! confirm_tag_move "Move tag ${TAG} to merge commit ${tag_at:0:12}?"; then
        run git checkout "${prev_branch}" 2>/dev/null || true
        exit 1
      fi
      run git tag -f -a "${TAG}" -m "Natural Language Coding hub ${TARGET}"
    fi
  else
    run git tag -a "${TAG}" -m "Natural Language Coding hub ${TARGET}"
  fi

  echo ""
  echo "Step 3/3 — push tag ${TAG} to ${REMOTE}"
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
  echo "Step 0b/9 — shipped tag audit (ADR 0040)"
  run python3 tools/nlc_release_shipped_tag_audit.py --check
  echo "Step 0c/9 — full NLC audit (ADR 0038 / continuity, profile release-prep)"
  run python3 tools/full-nlc-audit.py --check --profile release-prep

  release_context_wizard

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

  python3 tools/nlc_release_context.py --remote "${REMOTE}" --base "${BASE_BRANCH}" --branch "${RELEASE_BRANCH}" || {
    if ! confirm "Continue anyway (release branch may be missing commits from ${BASE_BRANCH})?" 0; then
      exit 1
    fi
  }

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
  echo "Step 9/9 — release record + commit"

  run python3 tools/nlc_release_record.py --version "${TARGET}" --branch "${RELEASE_BRANCH}"

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

load_resume_state() {
  eval "$(python3 tools/nlc_release_resume.py --remote "${REMOTE}" --base "${BASE_BRANCH}")"
}

cmd_release() {
  if [[ "${MODE}" == "finish" ]]; then
    echo "Note: ./release resumes automatically (ADR 0039). Running tag leg." >&2
    load_resume_state
    if [[ -n "${RESUME_MERGE_COMMIT}" ]]; then
      MERGE_COMMIT_SHA="${RESUME_MERGE_COMMIT}"
    fi
    cmd_finish
    return
  fi
  if [[ "${MODE}" == "prepare" ]]; then
    echo "Note: prefer ./release alone (ADR 0039). Running prepare leg." >&2
    cmd_prepare
    return
  fi
  load_resume_state
  case "${RESUME_PHASE}" in
    tag_ready)
      echo "Resume: merged ${RESUME_BRANCH}; tagging ${RESUME_TAG}."
      MERGE_COMMIT_SHA="${RESUME_MERGE_COMMIT}"
      if confirm "Continue tagging ${RESUME_TAG} at ${RESUME_MERGE_COMMIT:0:12}?" 1; then
        cmd_finish
      fi
      ;;
    await_merge)
      echo "Resume: ${RESUME_BRANCH} pushed; waiting for merge to ${BASE_BRANCH}."
      RELEASE_SHA="$(git rev-parse "${REMOTE}/${RESUME_BRANCH}" 2>/dev/null || git rev-parse "${RESUME_BRANCH}")"
      wait_for_merge_on_main "${RELEASE_SHA}" "${RESUME_BRANCH}"
      cmd_finish
      ;;
    complete)
      echo "Release ${RESUME_TAG} already tags merge ${RESUME_MERGE_COMMIT:0:12}."
      echo "  Start a new version with ./release --bump … on ${BASE_BRANCH}."
      ;;
    *)
      cmd_single
      ;;
  esac
}

case "${MODE}" in
  finish|prepare|single) cmd_release ;;
  *)
    echo "Unknown mode: ${MODE}" >&2
    exit 2
    ;;
esac
