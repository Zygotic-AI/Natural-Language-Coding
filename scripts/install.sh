#!/usr/bin/env bash
# Natural Language Coding — install portable skills into the user's agent harness.
# macOS, Linux, WSL. Requires: bash, curl or git, mkdir, cp or rsync.
set -euo pipefail

NLC_REPO="${NLC_REPO:-https://github.com/Zygotic-AI/Natural-Language-Coding.git}"
NLC_REF="${NLC_REF:-main}"
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

if [[ -f "$(dirname "$0")/../.agents/skills/planit/SKILL.md" ]]; then
  src_root="$(cd "$(dirname "$0")/.." && pwd)"
  echo "  source: local repo ${src_root}"
else
  tmpdir="$(mktemp -d)"
  if command -v git >/dev/null 2>&1; then
    git clone --depth 1 --branch "${NLC_REF}" "${NLC_REPO}" "${tmpdir}/repo"
    src_root="${tmpdir}/repo"
  else
    echo "install: need git or run from a cloned Natural-Language-Coding repo" >&2
    exit 1
  fi
fi

if command -v rsync >/dev/null 2>&1; then
  rsync -a "${src_root}/.agents/skills/" "${AGENTS_SKILLS}/"
else
  cp -R "${src_root}/.agents/skills/." "${AGENTS_SKILLS}/"
fi

mkdir -p "${INSTALL_ROOT}/hub"
if command -v rsync >/dev/null 2>&1; then
  rsync -a --exclude .git "${src_root}/" "${INSTALL_ROOT}/hub/"
else
  echo "  warning: rsync not found; hub tools not mirrored (skills only)" >&2
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

cat <<EOF

Done.

Hub copy (tools, charter): ${INSTALL_ROOT}/hub
Portable skills: ${AGENTS_SKILLS}

Next:
  1. Open your application repo in Cursor.
  2. /interview — bind goals, requirements, knowledge domains.
  3. /planit — build and prove (see ${INSTALL_ROOT}/hub/docs/ai-compiled-systems/PROCESS.md)

Fitness (from hub): bash ${INSTALL_ROOT}/hub/tools/ci-fitness.sh

EOF
