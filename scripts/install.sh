#!/usr/bin/env bash
# Natural Language Coding — install portable skills into the user's agent harness.
# macOS, Linux, WSL. Requires: bash, curl or git, mkdir, cp or rsync.
set -euo pipefail

# ADR 0013 — requirements preflight (all gaps, then exit)
requirements_preflight() {
  local -a missing=()
  command -v python3 >/dev/null 2>&1 || missing+=("python3")
  local script_dir local_marker
  script_dir="$(cd "$(dirname "$0")" && pwd)"
  local_marker="${script_dir}/../.agents/skills/planit/SKILL.md"
  if [[ ! -f "${local_marker}" ]]; then
    command -v curl >/dev/null 2>&1 || missing+=("curl")
  fi
  if ((${#missing[@]} > 0)); then
    echo "REQUIREMENTS:NOT_MET"
    local m
    for m in "${missing[@]}"; do
      echo "  missing: ${m}"
    done
    echo "  hint: install missing tools or clone this repo and re-run install.sh"
    exit 1
  fi
}
requirements_preflight

NLC_REPO_SLUG="${NLC_REPO_SLUG:-Zygotic-AI/Natural-Language-Coding}"
NLC_RAW_BASE="${NLC_RAW_BASE:-https://raw.githubusercontent.com/${NLC_REPO_SLUG}/main}"
NLC_REF="${NLC_REF:-}"
INSTALL_ROOT="${NLC_INSTALL_ROOT:-${HOME}/.local/share/nlc}"
AGENTS_SKILLS="${HOME}/.agents/skills"
CURSOR_SKILLS="${HOME}/.cursor/skills"

tmpdir=""
cleanup() {
  if [[ -n "${tmpdir}" && -d "${tmpdir}" ]]; then
    rm -rf "${tmpdir}"
  fi
}
trap cleanup EXIT

echo "Natural Language Coding — install"
echo "  target: ${INSTALL_ROOT}"
echo "  skills: ${AGENTS_SKILLS}"

mkdir -p "${INSTALL_ROOT}" "${AGENTS_SKILLS}"

script_dir="$(cd "$(dirname "$0")" && pwd)"
if [[ -f "${script_dir}/../.agents/skills/planit/SKILL.md" ]]; then
  src_root="$(cd "${script_dir}/.." && pwd)"
  echo "  source: local repo ${src_root}"
  python3 "${src_root}/tools/nlc-fetch-hub.py" --install-root "${INSTALL_ROOT}" --from-path "${src_root}"
  src_root="${INSTALL_ROOT}/hub"
else
  tmpdir="$(mktemp -d)"
  tool_dir="${tmpdir}/nlc-tools"
  mkdir -p "${tool_dir}"
  curl -fsSL "${NLC_RAW_BASE}/tools/nlc-fetch-hub.py" -o "${tool_dir}/nlc-fetch-hub.py"
  curl -fsSL "${NLC_RAW_BASE}/tools/nlc_distribution.py" -o "${tool_dir}/nlc_distribution.py"
  curl -fsSL "${NLC_RAW_BASE}/tools/nlc_requirements.py" -o "${tool_dir}/nlc_requirements.py"
  fetch_args=(--install-root "${INSTALL_ROOT}" --repo "${NLC_REPO_SLUG}")
  if [[ -n "${NLC_VERSION:-}" ]]; then
    fetch_args+=(--version "${NLC_VERSION}")
  elif [[ -n "${NLC_REF}" ]]; then
    fetch_args+=(--version "${NLC_REF#v}")
  fi
  echo "  source: release tarball (latest semver unless NLC_VERSION/NLC_REF set)"
  python3 "${tool_dir}/nlc-fetch-hub.py" "${fetch_args[@]}"
  src_root="${INSTALL_ROOT}/hub"
fi

if command -v rsync >/dev/null 2>&1; then
  rsync -a "${src_root}/.agents/skills/" "${AGENTS_SKILLS}/"
else
  cp -R "${src_root}/.agents/skills/." "${AGENTS_SKILLS}/"
fi

if [[ -d "${HOME}/.cursor" ]]; then
  mkdir -p "${CURSOR_SKILLS}"
  for skill in bbp-confirmer bbp-proposer bbp-recorder bbp-reviewer interview planit; do
    if [[ -d "${src_root}/.cursor/skills/${skill}" ]]; then
      rm -rf "${CURSOR_SKILLS}/${skill}"
      cp -R "${src_root}/.cursor/skills/${skill}" "${CURSOR_SKILLS}/${skill}"
    fi
  done
  echo "  cursor: copied repo-local BBP + planit skills"
fi

if [[ -z "${NLC_SKIP_VERIFY:-}" ]] && [[ -f "${INSTALL_ROOT}/hub/tools/nlc-install-verify.py" ]]; then
  echo "  verify: hub file hashes"
  python3 "${INSTALL_ROOT}/hub/tools/nlc-install-verify.py" "${INSTALL_ROOT}/hub" || {
    echo "INSTALL:NOT_MET hub verify failed (set NLC_SKIP_VERIFY=1 to skip)"
    exit 1
  }
fi

if [[ -f "${INSTALL_ROOT}/current" ]]; then
  echo "  hub version: $(tr -d '\n' < "${INSTALL_ROOT}/current")"
fi

cat <<EOF

Done.

Hub copy (tools, charter): ${INSTALL_ROOT}/hub
Portable skills: ${AGENTS_SKILLS}

Next:
  1. Open your application repo in Cursor.
  2. /interview — bind goals, requirements, knowledge domains.
  3. /planit — build and prove (see ${INSTALL_ROOT}/hub/docs/ai-compiled-systems/PROCESS.md)

Prove (from hub): python3 ${INSTALL_ROOT}/hub/tools/ci_fitness.py

EOF
