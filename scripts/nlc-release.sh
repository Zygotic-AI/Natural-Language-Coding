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
FROM_BRANCH=""
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

Automation overrides (optional):
  --two-step                Same as ./release prepare
  --bump patch|minor|major|keep
  --from-branch NAME        Use named release line (must match release/v*)
  --message "text"
  --yes                     Deprecated: default is non-interactive (retag still requires env)
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
    --from-branch) FROM_BRANCH="${2:-}"; shift ;;
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

release_fail() {
  local problem="$1"
  shift
  local -a gaps=()
  local -a fixes=()
  while [[ $# -gt 0 ]]; do
    if [[ "$1" == "--" ]]; then
      shift
      fixes=("$@")
      break
    fi
    gaps+=("$1")
    shift
  done
  if [[ ${#fixes[@]} -eq 0 ]]; then
    fixes=(
      "git fetch ${REMOTE} ${BASE_BRANCH} --tags"
      "cd ${ROOT} && ./release"
    )
  fi
  python3 tools/nlc_release_remediate.py "${problem}" "${gaps[@]}" -- "${fixes[@]}"
}

is_release_line_branch() {
  [[ "${1}" =~ ^release/v[0-9]+\.[0-9]+\.[0-9]+$ ]]
}

ensure_on_main() {
  local branch_now
  branch_now="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo HEAD)"
  if [[ "${branch_now}" == "${BASE_BRANCH}" ]]; then
    run git pull "${REMOTE}" "${BASE_BRANCH}" 2>/dev/null || true
    return 0
  fi
  echo "  Checking out ${BASE_BRANCH} (tag leg / resume)."
  run git checkout "${BASE_BRANCH}" || release_fail \
    "Cannot checkout ${BASE_BRANCH}" \
    "On branch ${branch_now}" \
    "git stash push -m 'release' --include-untracked" \
    "git checkout ${BASE_BRANCH}"
  run git pull "${REMOTE}" "${BASE_BRANCH}" 2>/dev/null || true
}

load_release_infer() {
  local as_branch="${1:-}"
  local infer_args=(--remote "${REMOTE}" --base "${BASE_BRANCH}" --emit shell)
  if [[ -n "${BUMP}" ]]; then
    infer_args+=(--bump-override "${BUMP}")
  fi
  if [[ -n "${as_branch}" ]]; then
    infer_args+=(--as-branch "${as_branch}")
  fi
  eval "$(python3 tools/nlc_release_infer.py "${infer_args[@]}")"
}

run_inferred_prepare_actions() {
  local depth="${1:-0}"
  local branch_now
  branch_now="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo HEAD)"

  case "${INFER_ACTION:-stay}" in
    stay)
      ;;
    checkout_release)
      run git checkout "${INFER_RELEASE_BRANCH}"
      ;;
    create_release_from_head)
      if git show-ref --verify --quiet "refs/heads/${INFER_RELEASE_BRANCH}"; then
        run git checkout "${INFER_RELEASE_BRANCH}"
      else
        echo "  Creating ${INFER_RELEASE_BRANCH} from ${branch_now}."
        run git checkout -b "${INFER_RELEASE_BRANCH}"
      fi
      ;;
    merge_into_release)
      if ! git show-ref --verify --quiet "refs/heads/${INFER_RELEASE_BRANCH}"; then
        release_fail "Release branch missing for merge" \
          "Expected ${INFER_RELEASE_BRANCH}" \
          "Re-run ./release from ${INFER_SOURCE_BRANCH}"
      fi
      run git checkout "${INFER_RELEASE_BRANCH}"
      if [[ "${branch_now}" != "${INFER_RELEASE_BRANCH}" ]]; then
        run git merge "${INFER_SOURCE_BRANCH}" -m "Merge ${INFER_SOURCE_BRANCH} into ${INFER_RELEASE_BRANCH} for release"
      fi
      ;;
    normalize_main_trunk)
      if [[ "${depth}" -ge 2 ]]; then
        release_fail "Trunk normalize did not stabilize" \
          "Infer still wants normalize_main_trunk after one pass" \
          "Re-run ./release"
      fi
      normalize_main_trunk_for_release
      load_release_infer "${INFER_WORK_BRANCH}"
      echo "  ${INFER_PHASE:-prepare}: ${INFER_RELEASE_BRANCH:-?}"
      if [[ -n "${INFER_LINE:-}" ]]; then
        echo "  ${INFER_LINE}"
      fi
      run_inferred_prepare_actions $((depth + 1))
      return
      ;;
    tag_only|await_merge|complete|blocked)
      ;;
    *)
      release_fail "Unknown infer action" "${INFER_ACTION}"
      ;;
  esac
}

normalize_main_trunk_for_release() {
  local work_branch="${INFER_WORK_BRANCH:-}"
  local shipped_tag="${INFER_SHIPPED_TAG:-}"
  local stashed=0

  _normalize_stash_orphan_warn() {
    if [[ "${stashed}" -ne 1 ]]; then
      return 0
    fi
    echo "  WARNING: trunk normalize stashed your tree and did not pop it (run interrupted)." >&2
    echo "  fix: git checkout ${work_branch} && git stash pop   # message: nlc-release trunk normalize" >&2
  }

  if [[ -z "${work_branch}" || -z "${shipped_tag}" ]]; then
    release_fail "Cannot normalize production trunk" \
      "Missing infer work branch or shipped tag" \
      "Re-run ./release"
  fi

  echo ""
  echo "Step trunk/9 — production trunk normalize (ADR 0044; zero-parameter ./release)"
  echo "  Work branch: ${work_branch}  Ship target: ${INFER_RELEASE_BRANCH:-?}  Tag baseline: ${shipped_tag}"

  if [[ -n "$(git status --porcelain 2>/dev/null)" ]]; then
    echo "  Orchestrator stash (not manual): dirty tree before branch moves…"
    trap _normalize_stash_orphan_warn EXIT
    run git stash push -u -m "nlc-release trunk normalize"
    stashed=1
  fi

  if git show-ref --verify --quiet "refs/heads/${work_branch}"; then
    echo "  Using existing ${work_branch}."
    run git checkout "${work_branch}"
  else
    echo "  Creating ${work_branch} from current ${BASE_BRANCH} (preserve unreleased commits)."
    run git checkout -b "${work_branch}"
  fi

  run git fetch "${REMOTE}" "${BASE_BRANCH}" --tags
  run git checkout "${BASE_BRANCH}"
  local shipped_commit="${INFER_SHIPPED_COMMIT:-}"
  if [[ -z "${shipped_commit}" ]]; then
    shipped_commit="$(python3 -c "import sys; sys.path.insert(0,'tools'); from nlc_release_tags import canonical_tag_commit; print(canonical_tag_commit('${shipped_tag}', '${REMOTE}') or '')")"
  fi
  if [[ -z "${shipped_commit}" ]]; then
    shipped_commit="${shipped_tag}^{commit}"
  fi
  run git reset --hard "${shipped_commit}"
  echo "  ${BASE_BRANCH} now at ${shipped_tag} (${shipped_commit:0:12}; local only; no push)."

  run git checkout "${work_branch}"
  if [[ "${stashed}" -eq 1 ]]; then
    run git stash pop || release_fail \
      "Stash pop failed after trunk normalize" \
      "Resolve conflicts on ${work_branch}" \
      "git status"
    stashed=0
    trap - EXIT
  fi
}

apply_release_infer() {
  local branch_now
  run git fetch "${REMOTE}" "${BASE_BRANCH}" --tags 2>/dev/null || true
  branch_now="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo HEAD)"

  if [[ -n "${FROM_BRANCH}" ]]; then
    if ! is_release_line_branch "${FROM_BRANCH}"; then
      release_fail "Invalid --from-branch" \
        "${FROM_BRANCH} must match release/vX.Y.Z" \
        "./release --from-branch release/v0.0.0"
    fi
    run git checkout "${FROM_BRANCH}"
    branch_now="${FROM_BRANCH}"
  fi

  load_release_infer

  if [[ "${INFER_BLOCK:-0}" == "1" ]]; then
    local -a _infer_gaps=()
    local -a _purity_fixes=()
    if [[ -n "${INFER_BLOCK_GAPS:-}" ]]; then
      IFS='|' read -r -a _infer_gaps <<< "${INFER_BLOCK_GAPS}"
    fi
    if [[ "${INFER_BLOCK_PROBLEM:-}" == *"production-trunk"* ]]; then
      mapfile -t _purity_fixes < <(
        python3 tools/nlc_release_remediate.py --print-main-purity-fixes \
          --remote "${REMOTE}" --base "${BASE_BRANCH}" \
          --next-release-branch "${INFER_RELEASE_BRANCH:-}"
      )
      release_fail "${INFER_BLOCK_PROBLEM:-Release infer blocked}" "${_infer_gaps[@]}" -- "${_purity_fixes[@]}"
    else
      release_fail "${INFER_BLOCK_PROBLEM:-Release infer blocked}" "${_infer_gaps[@]}"
    fi
  fi

  echo "  ${INFER_PHASE:-prepare}: ${INFER_RELEASE_BRANCH:-?}"
  if [[ -n "${INFER_LINE:-}" ]]; then
    echo "  ${INFER_LINE}"
  fi

  run_inferred_prepare_actions 0

  export NLC_RELEASE_SOURCE_BRANCH="${INFER_RELEASE_BRANCH}"
  if [[ -z "${BUMP}" ]]; then
    BUMP="${INFER_BUMP}"
  fi
  TARGET="${INFER_TARGET}"
  RELEASE_BRANCH="${INFER_RELEASE_BRANCH}"
}

verify_deep_at_shipped_baseline() {
  local shipped_tag shipped_commit restore_ref detached=0
  read -r shipped_tag shipped_commit < <(
    python3 -c "import sys; sys.path.insert(0,'tools'); from nlc_release_tags import last_shipped_tag, canonical_tag_commit; t=last_shipped_tag('HEAD') or ''; c=canonical_tag_commit(t, '${REMOTE}') if t else ''; print(t, c)"
  )
  restore_ref="$(git symbolic-ref --quiet --short HEAD 2>/dev/null || true)"
  if [[ -z "${restore_ref}" ]]; then
    restore_ref="${RELEASE_BRANCH:-}"
  fi
  if [[ -z "${restore_ref}" ]]; then
    restore_ref="${BASE_BRANCH}"
  fi

  _restore_after_shipped_verify() {
    if [[ "${detached}" -ne 1 ]]; then
      return 0
    fi
    echo "  Restoring ${restore_ref} after shipped-baseline verify-deep…"
    git checkout "${restore_ref}" 2>/dev/null || git checkout "${BASE_BRANCH}" 2>/dev/null || true
    detached=0
  }

  if [[ -z "${shipped_tag}" ]]; then
    echo "  No shipped tag reachable — verify-deep on release line HEAD."
    run python3 tools/nlc.py --project . verify-deep
    return 0
  fi
  if [[ -z "${shipped_commit}" ]]; then
    shipped_commit="${shipped_tag}^{commit}"
  fi
  echo "  verify-deep at shipped baseline ${shipped_tag} (${shipped_commit:0:12}; ADR 0022 / 0044)."
  trap _restore_after_shipped_verify EXIT
  run git checkout --detach "${shipped_commit}"
  detached=1
  set +e
  python3 tools/nlc.py --project . verify-deep
  local verify_rc=$?
  set -e
  _restore_after_shipped_verify
  trap - EXIT
  if [[ "${verify_rc}" -ne 0 ]]; then
    exit "${verify_rc}"
  fi
}

confirm_tag_move() {
  local prompt="$1"
  if [[ -n "${NLC_RELEASE_ALLOW_RETAG:-}" ]]; then
    return 0
  fi
  read -r -p "${prompt} [y/N] (requires explicit yes; --yes does not apply) " ans
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
    echo "  Auto-drafting ${path}…"
    run python3 tools/nlc_release_notes.py --write-draft --version "${ver}" --to "${ref}"
  else
    echo "  Refreshing Changes section in ${path}…"
    run python3 tools/nlc_release_notes.py --refresh-changes --version "${ver}" --to "${ref}"
  fi

  if ! python3 tools/nlc_release_notes.py --check --version "${ver}"; then
    release_fail \
      "Release notes not valid for v${ver}" \
      "Highlights required in ${path}" \
      "python3 tools/nlc_release_notes.py --check --version ${ver}" \
      "\${EDITOR:-nano} ${path}"
  fi
  echo "  RELEASE_NOTES:MET"
}

release_target_gate() {
  local target="$1"
  echo ""
  echo "Step 2/9 — release target preflight (migrations for v${target}; ADR 0014)"
  if python3 tools/nlc_release_target_preflight.py --check --target "${target}"; then
    return 0
  fi
  echo "  Auto-scaffolding noop migration units for v${target}…"
  run python3 tools/nlc_release_target_preflight.py --ensure-noop --target "${target}" || true
  if python3 tools/nlc_release_target_preflight.py --check --target "${target}"; then
    return 0
  fi
  python3 tools/nlc_release_target_preflight.py --check --print-agent-prompt --target "${target}" \
    >/dev/null 2>&1 || true
  release_fail \
    "Release target preflight NOT_MET for v${target}" \
    "Migration chain from shipped baseline to target is incomplete" \
    "python3 tools/nlc_release_target_preflight.py --check --target ${target}" \
    "python3 tools/nlc_release_target_preflight.py --print-agent-prompt --target ${target}"
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

  release_fail \
    "Release branch must be created from ${BASE_BRANCH}" \
    "Currently on ${branch_now}" \
    "git checkout ${BASE_BRANCH}" \
    "git pull ${REMOTE} ${BASE_BRANCH}" \
    "./release"
}

wait_for_merge_on_main() {
  local sha="$1"
  local rel_branch="$2"

  if [[ "${DRY_RUN}" -eq 1 ]]; then
    echo "DRY_RUN: would poll for merge, then verify merge and tag."
    return 0
  fi

  local merged poll_interval poll_max i
  poll_interval="${NLC_RELEASE_MERGE_POLL_SECONDS:-15}"
  poll_max="${NLC_RELEASE_MERGE_POLL_MAX:-120}"

  if command -v gh >/dev/null 2>&1; then
    echo ""
    echo "Waiting for merged PR: ${rel_branch} → ${BASE_BRANCH} (poll every ${poll_interval}s)…"
    for ((i = 0; i < poll_max; i++)); do
      merged="$(resolve_merged_commit_sha "${rel_branch}" "${sha}" || true)"
      if [[ -n "${merged}" ]]; then
        MERGE_COMMIT_SHA="${merged}"
        echo "  Merge commit to tag: ${MERGE_COMMIT_SHA:0:12}"
        warn_if_main_moved_past_merge "${MERGE_COMMIT_SHA}"
        return 0
      fi
      sleep "${poll_interval}"
    done
  fi

  echo ""
  print_pr_help "${rel_branch}" "${MSG:-Release}"
  release_fail \
    "Release PR not merged to ${BASE_BRANCH} yet" \
    "No merge commit found for ${rel_branch}" \
    "Merge the PR in GitHub when CI is green" \
    "Re-run ./release after merge (same repo root)"
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

  run git push "${REMOTE}" "${TAG}"

  run git checkout "${prev_branch}" 2>/dev/null || run git checkout "${BASE_BRANCH}" 2>/dev/null || true

  echo ""
  echo "RELEASE:TAG_PUSHED ${TAG} @ ${tag_at:0:12}"
  echo "  GitHub Actions will build the tarball and publish the Release."
}

run_prepare_core() {
  apply_release_infer

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
  run python3 tools/nlc_release_shipped_tag_audit.py --check --align-local --remote "${REMOTE}"
  echo "Step 0c/9 — full NLC audit (ADR 0038 / continuity, profile release-prep)"
  run python3 tools/full-nlc-audit.py --check --profile release-prep

  release_context_wizard

  CURRENT="$(python3 tools/nlc_release_bump.py --current)"

  echo ""
  echo "Step 1/9 — target version (inferred; automation may pass --bump)"
  echo "  Current integrity/nlc-version.json: ${CURRENT}"
  if [[ -z "${TARGET}" ]]; then
    TARGET="$(python3 tools/nlc_release_bump.py --peek "${BUMP:-keep}")"
  fi
  if [[ -z "${RELEASE_BRANCH}" ]]; then
    RELEASE_BRANCH="$(release_branch_name "${TARGET}")"
  fi
  echo "  Target version for this run: ${TARGET} (${RELEASE_BRANCH}, bump=${BUMP:-keep})"

  if ! python3 tools/nlc_release_context.py --remote "${REMOTE}" --base "${BASE_BRANCH}" --branch "${RELEASE_BRANCH}"; then
    release_fail \
      "Release branch context NOT_MET" \
      "${RELEASE_BRANCH} may be missing commits from ${BASE_BRANCH}" \
      "python3 tools/nlc_release_context.py --remote ${REMOTE} --base ${BASE_BRANCH} --branch ${RELEASE_BRANCH}"
  fi

  release_target_gate "${TARGET}"

  echo ""
  echo "Step 3/9 — verify-deep (shipped baseline; fail before notes or bump)"
  verify_deep_at_shipped_baseline

  ensure_release_notes "${TARGET}" "HEAD"
  block_until_release_notes_met "${TARGET}"

  echo ""
  echo "Step 5/9 — release line ${RELEASE_BRANCH}"
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
    echo "  Committing release record and notes: \"${MSG}\""
    run git add -A
    run git commit -m "${MSG}"
    assert_release_notes_on_commit "${TARGET}"
  fi

  RELEASE_SHA="$(git rev-parse HEAD)"
  echo ""
  echo "Push branch (no tag yet)"
  assert_release_notes_on_commit "${TARGET}"
  if [[ "${NO_PUSH}" -eq 1 ]]; then
    echo "  --no-push: commit on ${RELEASE_BRANCH} at ${RELEASE_SHA}"
    return 0
  fi

  run git push -u "${REMOTE}" "${RELEASE_BRANCH}"

  echo ""
  echo "RELEASE:BRANCH_PUSHED ${RELEASE_BRANCH} @ ${RELEASE_SHA}"
  echo ""
  echo "Next: merge the release PR in GitHub when CI is green, then re-run ./release."
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
  echo "  After merge: ./release"
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
    ensure_on_main
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
      ensure_on_main
      echo "Resume: merged ${RESUME_BRANCH}; tagging ${RESUME_TAG}."
      MERGE_COMMIT_SHA="${RESUME_MERGE_COMMIT}"
      cmd_finish
      ;;
    await_merge)
      if ! git rev-parse --verify "${REMOTE}/${RESUME_BRANCH}^{commit}" >/dev/null 2>&1; then
        release_fail "Release branch not on ${REMOTE}" \
          "${RESUME_BRANCH} is not on the remote (resume await_merge requires a pushed PR branch)" \
          "git fetch ${REMOTE} --prune" \
          "git push -u ${REMOTE} ${RESUME_BRANCH}" \
          "cd ${ROOT} && ./release"
      fi
      echo "Resume: ${RESUME_BRANCH} on ${REMOTE}; waiting for merge to ${BASE_BRANCH}."
      RELEASE_SHA="$(git rev-parse "${REMOTE}/${RESUME_BRANCH}^{commit}")"
      wait_for_merge_on_main "${RELEASE_SHA}" "${RESUME_BRANCH}"
      ensure_on_main
      cmd_finish
      ;;
    complete)
      echo "Release ${RESUME_TAG} already tags merge ${RESUME_MERGE_COMMIT:0:12}."
      echo "  Start a new version: branch from main, commit, run ./release."
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
