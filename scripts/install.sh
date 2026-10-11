#!/usr/bin/env bash
# Thin entrypoint. Policy lives in goals/hub_install/execute.sh.
set -euo pipefail

if [[ -n "${BASH_SOURCE[0]:-}" && "${BASH_SOURCE[0]}" != "bash" ]]; then
  _script="${BASH_SOURCE[0]}"
  if [[ -f "$(dirname "$_script")/../goals/hub_install/execute.sh" ]]; then
    ROOT="$(cd "$(dirname "$_script")/.." && pwd)"
    exec bash "${ROOT}/goals/hub_install/execute.sh" "$@"
  fi
fi

NLC_REPO_SLUG="${NLC_REPO_SLUG:-Zygotic-AI/Natural-Language-Coding}"
NLC_REF="${NLC_REF:-main}"
NLC_RAW_BASE="${NLC_RAW_BASE:-https://raw.githubusercontent.com/${NLC_REPO_SLUG}/${NLC_REF}}"

tmpdir="$(mktemp -d)"
trap 'rm -rf "${tmpdir}"' EXIT

if [[ "${NLC_RAW_BASE}" == file://* ]]; then
  local_root="${NLC_RAW_BASE#file://}"
  exec bash "${local_root}/goals/hub_install/execute.sh" "$@"
fi

if ! command -v git >/dev/null 2>&1; then
  echo "Install can't continue — piped install requires git to fetch the hub." >&2
  exit 1
fi

clone_url="https://github.com/${NLC_REPO_SLUG}.git"
if [[ -n "${NLC_REF}" ]]; then
  git -c core.autocrlf=false clone --depth 1 --branch "${NLC_REF}" "${clone_url}" "${tmpdir}/repo"
else
  git -c core.autocrlf=false clone --depth 1 "${clone_url}" "${tmpdir}/repo"
fi
exec bash "${tmpdir}/repo/goals/hub_install/execute.sh" "$@"
