#!/usr/bin/env bash
# Published-skill author checklist (same list before release and after install).
#
# Input: optional --root <skills-tree>. Default: <repo>/.agents/skills.
# Output: child SKILL_AUTHOR:MET|NOT_MET lines; this script exits with the child.
# Failure mode: exit 0 = MET; non-zero = NOT_MET (missing CLI or checklist fail).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "${ROOT}"

SKILLS_ROOT="${ROOT}/.agents/skills"
if [[ "${1:-}" == "--root" ]]; then
  if [[ $# -lt 2 ]]; then
    echo "SKILL_AUTHOR:NOT_MET --root needs a path" >&2
    exit 2
  fi
  SKILLS_ROOT="$2"
fi

CLI="${ROOT}/tools/nlc-skill-author-check.py"
if [[ ! -f "${CLI}" ]]; then
  echo "SKILL_AUTHOR:NOT_MET missing tools/nlc-skill-author-check.py" >&2
  exit 1
fi

exec python3 "${CLI}" --root "${SKILLS_ROOT}"
