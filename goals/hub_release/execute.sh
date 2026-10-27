#!/usr/bin/env bash
# Hub release action interpreter. The pure planner owns every stop (ADR 0045/0049).
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "${ROOT}"

REMOTE="${NLC_RELEASE_REMOTE:-origin}"
BASE_BRANCH="${NLC_RELEASE_BASE_BRANCH:-main}"
DRY_RUN=0
NO_PUSH=0
MSG=""
CLI_BLOCKER=""
RELEASE_PLAN_CACHE=""
LAST_ACTION=""
LAST_PROGRESS_TOKEN=""

usage() {
  cat <<'EOF'
Usage:
  ./release

Automation overrides:
  --dry-run
  --no-push
  --message "text"
  -h, --help
EOF
}

PROBE_REF=""
PROBE_REF_SET=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --probe-ref)
      PROBE_REF_SET=1
      if [[ $# -ge 2 ]]; then
        PROBE_REF="$2"
        shift
      else
        PROBE_REF=""
      fi
      ;;
    --dry-run) DRY_RUN=1 ;;
    --no-push) NO_PUSH=1 ;;
    --message)
      if [[ $# -lt 2 ]]; then
        CLI_BLOCKER="BLOCKED_INVALID_ARGUMENT"
      else
        MSG="$2"
        shift
      fi
      ;;
    -h|--help) usage; exit 0 ;;
    *) CLI_BLOCKER="BLOCKED_INVALID_ARGUMENT" ;;
  esac
  shift
done

invalidate_release_plan_cache() {
  if [[ -n "${RELEASE_PLAN_CACHE}" && -f "${RELEASE_PLAN_CACHE}" ]]; then
    rm -f "${RELEASE_PLAN_CACHE}"
  fi
  RELEASE_PLAN_CACHE=""
}

release_plan_cache() {
  if [[ -z "${RELEASE_PLAN_CACHE}" || ! -f "${RELEASE_PLAN_CACHE}" ]]; then
    RELEASE_PLAN_CACHE="$(mktemp)"
    python3 tools/nlc_release_state.py \
      --remote "${REMOTE}" \
      --base "${BASE_BRANCH}" \
      --emit facts >"${RELEASE_PLAN_CACHE}"
  fi
  printf '%s\n' "${RELEASE_PLAN_CACHE}"
}

release_plan_field() {
  local field="$1"
  local cache
  cache="$(release_plan_cache)"
  python3 tools/nlc_release_state.py --facts "${cache}" --print "${field}"
}

release_fact_field() {
  local field="$1"
  local cache
  cache="$(release_plan_cache)"
  python3 -c \
    "import json; print(json.load(open('${cache}', encoding='utf-8')).get('${field}', ''))"
}

release_fail() {
  local cache
  cache="$(release_plan_cache)"
  python3 tools/nlc_release_state.py --facts "${cache}" --emit remediation || true
}

run_planned() {
  if [[ "${DRY_RUN}" -eq 1 ]]; then
    echo "DRY_RUN: $*"
  else
    "$@"
  fi
}

create_release_line_ref_state() {
  local branch="$1"
  if ! command -v git >/dev/null 2>&1; then
    echo "error:missing_tool"
    return 0
  fi
  if [[ -z "${branch}" ]]; then
    echo "error:empty"
    return 0
  fi
  git show-ref --verify --quiet "refs/heads/${branch}"
  local show_rc=$?
  if [[ "${show_rc}" -eq 0 ]]; then
    echo "exists"
    return 0
  fi
  if [[ "${show_rc}" -eq 1 ]]; then
    echo "absent"
    return 0
  fi
  echo "error:unexpected rc=${show_rc}"
  return 0
}

apply_release_infer() {
  # Compatibility diagnostic only. It presents the planner and does not choose an action.
  python3 tools/nlc_release_infer.py \
    --remote "${REMOTE}" \
    --base "${BASE_BRANCH}" \
    --emit json >/dev/null
}

mark_action_failure() {
  export NLC_RELEASE_FAILED_ACTION="$1"
  unset NLC_RELEASE_STALLED_ACTION
  invalidate_release_plan_cache
}

mark_action_stall() {
  export NLC_RELEASE_STALLED_ACTION="$1"
  unset NLC_RELEASE_FAILED_ACTION
  invalidate_release_plan_cache
}

clear_action_observations() {
  unset NLC_RELEASE_FAILED_ACTION
  unset NLC_RELEASE_STALLED_ACTION
  unset NLC_RELEASE_RUNTIME_BLOCKER
}

dispatch_release_plan() {
  if [[ "${PROBE_REF_SET}" -eq 1 ]]; then
    local ref_state
    ref_state="$(create_release_line_ref_state "${PROBE_REF}")"
    printf '%s\n' "${ref_state}"
    if [[ "${ref_state}" == "exists" || "${ref_state}" == "absent" ]]; then
      exit 0
    fi
    echo "CREATE_RELEASE_LINE:REFUSE ${ref_state}" >&2
    exit 2
  fi
  local phase action kind desired branch tag merge_sha rc worktree shipped_sha
  local tag_output run_id
  local -a tag_argv=()
  phase="$(release_plan_field phase)"
  action="$(release_plan_field action)"
  kind="$(release_plan_field action_kind)"
  desired="$(release_plan_field desired_version)"
  branch="$(release_plan_field desired_branch)"
  tag="$(release_plan_field planned_tag)"
  merge_sha="$(release_plan_field merge_sha)"
  rc=0

  if [[ -z "${phase}" || -z "${action}" || -z "${kind}" ]]; then
    export NLC_RELEASE_RUNTIME_BLOCKER="BLOCKED_PLANNER_READ"
    invalidate_release_plan_cache
    release_plan_cache >/dev/null
    release_fail
    exit 1
  fi

  echo "Planner: phase=${phase} action=${action} kind=${kind}"

  case "${kind}" in
    HUMAN_DECISION)
      release_fail
      exit 1
      ;;
    AWAIT)
      if [[ "${action}" == "EXIT_AWAIT" ]]; then
        python3 tools/nlc_release_resume.py \
          --remote "${REMOTE}" --base "${BASE_BRANCH}" --emit json >/dev/null
        echo "RELEASE:AWAIT pull request merge; resume with ./release"
      else
        echo "RELEASE:AWAIT publication for ${tag}; resume with ./release"
      fi
      exit 0
      ;;
    TERMINAL)
      echo "RELEASE:MET ${tag} shipped"
      exit 0
      ;;
    REPAIR) ;;
    *)
      export NLC_RELEASE_RUNTIME_BLOCKER="BLOCKED_PLANNER_READ"
      invalidate_release_plan_cache
      release_plan_cache >/dev/null
      release_fail
      exit 1
      ;;
  esac

  case "${action}" in
    FETCH_REMOTE)
      : action_result_boundary:FETCH_REMOTE
      run_planned git fetch "${REMOTE}" --prune --tags || rc=$?
      ;;
    FAST_FORWARD_LOCAL)
      : action_result_boundary:FAST_FORWARD_LOCAL
      run_planned git fetch "${REMOTE}" "${branch}" &&
        run_planned git checkout "${branch}" &&
        run_planned git pull --ff-only "${REMOTE}" "${branch}" || rc=$?
      ;;
    ENSURE_MIGRATIONS)
      : action_result_boundary:ENSURE_MIGRATIONS
      python3 tools/nlc_release_preflight.py --check || rc=$?
      ;;
    VERIFY_SHIPPED_BASELINE)
      : action_result_boundary:VERIFY_SHIPPED_BASELINE
      shipped_sha="$(release_fact_field shipped_tag_sha)"
      if [[ -z "${shipped_sha}" ]]; then
        python3 tools/nlc.py --project . verify-deep || rc=$?
      else
        worktree="$(mktemp -d)"
        git worktree add --detach "${worktree}" "${shipped_sha}" || rc=$?
        if [[ "${rc}" -eq 0 ]]; then
          (
            cd "${worktree}" &&
              python3 tools/nlc.py --project . verify-deep
          ) || rc=$?
        fi
        git worktree remove --force "${worktree}" >/dev/null 2>&1
        rm -rf "${worktree}"
      fi
      if [[ "${rc}" -eq 0 ]]; then
        python3 tools/nlc_release_state.py \
          --remote "${REMOTE}" --base "${BASE_BRANCH}" \
          --record-fact shipped_verify_met || rc=$?
      fi
      ;;
    WRITE_NOTES)
      : action_result_boundary:WRITE_NOTES
      python3 tools/nlc_release_notes.py \
        --version "${desired}" --write-draft &&
        python3 tools/nlc_release_notes.py \
          --version "${desired}" --refresh-changes &&
        python3 tools/nlc_release_notes.py \
          --version "${desired}" --check || rc=$?
      ;;
    ALIGN_VERSION)
      : action_result_boundary:ALIGN_VERSION
      python3 tools/nlc_release_bump.py --align-to "${desired}" || rc=$?
      ;;
    VERIFY_TARGET)
      : action_result_boundary:VERIFY_TARGET
      python3 tools/nlc.py --project . verify-deep || rc=$?
      if [[ "${rc}" -eq 0 ]]; then
        python3 tools/nlc_release_state.py \
          --remote "${REMOTE}" --base "${BASE_BRANCH}" \
          --record-fact target_verify_met || rc=$?
      fi
      ;;
    PREP)
      : action_result_boundary:PREP
      python3 tools/nlc_release_shipped_tag_audit.py \
        --check --align-local --remote "${REMOTE}" &&
        python3 tools/full-nlc-audit.py --check --profile release-prep &&
        bash scripts/nlc-release-prep.sh || rc=$?
      if [[ "${rc}" -eq 0 ]]; then
        python3 tools/nlc_release_state.py \
          --remote "${REMOTE}" --base "${BASE_BRANCH}" \
          --record-fact prep_met || rc=$?
      fi
      ;;
    WRITE_RECORD)
      : action_result_boundary:WRITE_RECORD
      python3 tools/nlc_release_record.py \
        --version "${desired}" \
        --branch "${branch}" || rc=$?
      ;;
    COMMIT)
      : action_result_boundary:COMMIT
      run_planned git add -A &&
        run_planned git commit -m "${MSG:-Release v${desired}}" || rc=$?
      ;;
    CREATE_RELEASE_LINE)
      : action_result_boundary:CREATE_RELEASE_LINE
      apply_release_infer || rc=$?
      if [[ "${rc}" -eq 0 ]]; then
        if [[ -z "${branch}" ]]; then
          rc=2
        else
          ref_state="$(create_release_line_ref_state "${branch}")"
          if [[ "${ref_state}" == "exists" ]]; then
            run_planned git checkout "${branch}" || rc=$?
          elif [[ "${ref_state}" == "absent" ]]; then
            run_planned git checkout -b "${branch}" || rc=$?
          else
            echo "CREATE_RELEASE_LINE:REFUSE unknown ref state" >&2
            rc=2
          fi
        fi
      fi
      ;;
    CREATE_REPAIR_COMMIT)
      : action_result_boundary:CREATE_REPAIR_COMMIT
      run_planned git checkout "${branch}" &&
        run_planned git commit --allow-empty \
          -m "Repair ${branch} release identity" || rc=$?
      ;;
    PUSH_NEW|PUSH_FAST_FORWARD)
      : action_result_boundary:PUSH_NEW
      : action_result_boundary:PUSH_FAST_FORWARD
      if [[ "${NO_PUSH}" -eq 1 ]]; then
        echo "RELEASE:READY_LOCAL branch=${branch}"
      else
        run_planned git push -u "${REMOTE}" "${branch}" || rc=$?
      fi
      ;;
    CREATE_PR)
      : action_result_boundary:CREATE_PR
      if [[ "${NO_PUSH}" -eq 1 ]]; then
        echo "RELEASE:READY_LOCAL pull-request=${branch}"
      else
        gh pr create \
          --base "${BASE_BRANCH}" \
          --head "${branch}" \
          --title "Release v${desired}" \
          --body "Release v${desired}" || rc=$?
      fi
      ;;
    CREATE_LOCAL_TAG)
      : action_result_boundary:CREATE_LOCAL_TAG
      python3 tools/nlc_release_tag_gate.py \
        --check --commit "${merge_sha}" --tag "${tag}" || rc=$?
      if [[ "${rc}" -eq 0 ]]; then
        tag_output="$(python3 tools/nlc_release_state.py \
          --tag-argv --tag "${tag}" --commit "${merge_sha}")" || rc=$?
      fi
      if [[ "${rc}" -eq 0 ]]; then
        mapfile -t tag_argv <<<"${tag_output}"
        run_planned "${tag_argv[@]}" || rc=$?
      fi
      ;;
    PUSH_TAG)
      : action_result_boundary:PUSH_TAG
      if [[ "${NO_PUSH}" -eq 1 ]]; then
        echo "RELEASE:READY_LOCAL tag=${tag}"
      else
        run_planned git push "${REMOTE}" "${tag}" || rc=$?
      fi
      ;;
    RETRY_PUBLISH)
      : action_result_boundary:RETRY_PUBLISH
      run_id="$(gh run list \
        --workflow release.yml \
        --branch "${tag}" \
        --limit 1 \
        --json databaseId \
        --jq '.[0].databaseId')" || rc=$?
      if [[ "${rc}" -eq 0 && -n "${run_id}" ]]; then
        gh run rerun "${run_id}" --failed || rc=$?
      elif [[ "${rc}" -eq 0 ]]; then
        rc=2
      fi
      ;;
    *)
      rc=2
      ;;
  esac

  if [[ "${rc}" -ne 0 ]]; then
    mark_action_failure "${action}"
    release_plan_cache >/dev/null
    release_fail
    exit 1
  fi

  clear_action_observations
  invalidate_release_plan_cache
}

cmd_release() {
  local iteration action kind cache progress_token
  if [[ -n "${CLI_BLOCKER}" ]]; then
    export NLC_RELEASE_RUNTIME_BLOCKER="${CLI_BLOCKER}"
  fi

  for iteration in $(seq 1 64); do
    cache="$(release_plan_cache)"
    action="$(python3 tools/nlc_release_state.py --facts "${cache}" --print action)"
    kind="$(python3 tools/nlc_release_state.py --facts "${cache}" --print action_kind)"
    progress_token="$(
      python3 tools/nlc_release_state.py --facts "${cache}" --print progress_token
    )"
    if [[ "${kind}" == "REPAIR" && "${action}" == "${LAST_ACTION}" &&
          "${progress_token}" == "${LAST_PROGRESS_TOKEN}" ]]; then
      mark_action_stall "${action}"
    else
      LAST_ACTION="${action}"
      LAST_PROGRESS_TOKEN="${progress_token}"
    fi
    dispatch_release_plan
  done

  export NLC_RELEASE_RUNTIME_BLOCKER="BLOCKED_ACTION_LOOP_LIMIT"
  invalidate_release_plan_cache
  release_plan_cache >/dev/null
  dispatch_release_plan
}

# Planner observer selects pull requests by headRefOid, not list position.
# Shipped tag integrity remains an action input and is rechecked during PREP.
if [[ "${PROBE_REF_SET}" -eq 1 ]]; then
  dispatch_release_plan
fi
cmd_release
