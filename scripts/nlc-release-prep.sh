#!/usr/bin/env bash
# Dummy-proof hub release preparation. Tag push is still manual (last step).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${ROOT}"

echo "RELEASE_PREP:START"

python3 tools/ci_fitness.py
echo "RELEASE_PREP:MET ci_fitness"

python3 tools/nlc-install-hash-update.py
if ! git diff --quiet -- integrity/nlc-install-hashes.json; then
  if [[ -n "${NLC_RELEASE_ORCHESTRATOR:-}" ]]; then
    echo "RELEASE_PREP:NOTE install hashes updated (will commit in ./release step)"
  else
    echo "RELEASE_PREP:NOT_MET"
    echo "  stale: integrity/nlc-install-hashes.json (commit hash update, re-run this script)"
    exit 1
  fi
else
  echo "RELEASE_PREP:MET install_hashes"
fi

bash scripts/nlc-release-smoke.sh
echo "RELEASE_PREP:MET smoke"

VER="$(python3 -c "import json; print(json.load(open('integrity/nlc-version.json'))['version'])")"
echo "RELEASE_PREP:VERSION ${VER}"

SHA="$(git rev-parse --short HEAD)"
FINDINGS="${ROOT}/FINDINGS.md"
if [[ -f "${FINDINGS}" ]]; then
  sed -i "s/^Last pass: \`[^\`]*\`.*/Last pass: \`${SHA}\` (release prep; tag v${VER} when ready)./" "${FINDINGS}"
  echo "RELEASE_PREP:MET findings_sha=${SHA}"
fi

if ! git diff --quiet; then
  echo "RELEASE_PREP:NOTE commit FINDINGS (and any other) changes before tagging"
  git status -sb
fi

cat <<EOF

RELEASE_PREP:READY
  version: ${VER}
  commit:  ${SHA}

Tag (last — human):
  git tag -a v${VER} -m "Natural Language Coding hub v${VER}"
  git push origin main
  git push origin v${VER}

See docs/adoption/RELEASE-v0.1.0.md and docs/nlc/README.md

EOF
