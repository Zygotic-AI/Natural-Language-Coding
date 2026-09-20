#!/usr/bin/env bash
# Hub release — one guided path (verify-deep, version, prep, commit, tag, push).
# Humans: from repo root run   ./release
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${ROOT}"

DRY_RUN=0
YES=0
NO_PUSH=0
BUMP=""
MSG=""
REMOTE="${NLC_RELEASE_REMOTE:-origin}"
BRANCH="${NLC_RELEASE_BRANCH:-main}"

usage() {
  cat <<'EOF'
Usage: ./release [options]

  Guided hub release. You do not need to remember verify-deep / prep / tag order.

Options:
  --bump patch|minor|major|keep   Skip the interactive bump question
  --message "text"                Commit message (default: "Release vX.Y.Z")
  --yes                           Accept defaults without prompts (still confirms push unless --no-push)
  --no-push                       Stop after local commit + tag
  --dry-run                       Print steps only
  -h, --help

See docs/adoption/RELEASE.md
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=1 ;;
    --yes) YES=1 ;;
    --no-push) NO_PUSH=1 ;;
    --bump) BUMP="${2:-}"; shift ;;
    --message) MSG="${2:-}"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage; exit 2 ;;
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
  if [[ "${YES}" -eq 1 ]]; then
    return 0
  fi
  read -r -p "${prompt} [y/N] " ans
  [[ "${ans}" =~ ^[Yy] ]]
}

echo ""
echo "Natural Language Coding — hub release"
echo "  Repo: ${ROOT}"
echo "  Commands live here: ./release   (and scripts/nlc-release.sh)"
echo ""

CURRENT="$(python3 tools/nlc_release_bump.py --current)"
SUGGEST="$(python3 tools/nlc_release_bump.py --suggest 2>/dev/null | head -1)"

if [[ -z "${BUMP}" ]]; then
  echo "Current version (integrity/nlc-version.json): ${CURRENT}"
  echo "Suggested bump from your changes: ${SUGGEST}"
  python3 tools/nlc_release_bump.py --suggest >/dev/null
  echo ""
  echo "Release type:"
  PATCH_NEXT="$(python3 -c "
m, mi, p = '${CURRENT}'.split('.')
print(f'{m}.{mi}.{int(p)+1}')
")"
  MINOR_NEXT="$(python3 -c "
m, mi, p = '${CURRENT}'.split('.')
print(f'{m}.{int(mi)+1}.0')
")"
  MAJOR_NEXT="$(python3 -c "
m, mi, p = '${CURRENT}'.split('.')
print(f'{int(m)+1}.0.0')
")"
  echo "  p = patch  → ${PATCH_NEXT}"
  echo "  m = minor  → ${MINOR_NEXT}  (new requirements, policy packs, e.g. PCI)"
  echo "  M = major  → ${MAJOR_NEXT}  (breaking contract / charter-level)"
  echo "  k = keep   → ship ${CURRENT} as-is (no version file change)"
  echo ""
  read -r -p "Choice [p/m/M/k] (default ${SUGGEST:0:1}): " choice
  choice="${choice:-${SUGGEST:0:1}}"
  case "${choice}" in
    p|patch) BUMP="patch" ;;
    m|minor) BUMP="minor" ;;
    M|major) BUMP="major" ;;
    k|keep) BUMP="keep" ;;
    *)
      echo "Invalid choice." >&2
      exit 2
      ;;
  esac
fi

echo ""
echo "Step 1/6 — verify-deep (full gates + refresh fingerprints)"
run python3 tools/nlc.py --project . verify-deep

echo ""
echo "Step 2/6 — version"
if [[ "${BUMP}" == "keep" ]]; then
  TARGET="${CURRENT}"
  echo "  Keeping ${TARGET}"
else
  run python3 tools/nlc_release_bump.py --apply "${BUMP}"
  TARGET="$(python3 tools/nlc_release_bump.py --current)"
  echo "  Bumped to ${TARGET}"
fi

echo ""
echo "Step 3/6 — release prep (fitness, install hashes, smoke, FINDINGS sha)"
export NLC_RELEASE_ORCHESTRATOR=1
run bash scripts/nlc-release-prep.sh
unset NLC_RELEASE_ORCHESTRATOR

if [[ -z "${MSG}" ]]; then
  MSG="Release v${TARGET}"
fi

echo ""
echo "Step 4/6 — commit"
if git diff --quiet && git diff --cached --quiet; then
  echo "  Working tree clean — nothing to commit."
else
  git status -sb
  if confirm "Commit all changes with message: \"${MSG}\"?"; then
    run git add -A
    run git commit -m "${MSG}"
  else
    echo "  Stopped: commit declined." >&2
    exit 1
  fi
fi

SHA="$(git rev-parse HEAD)"
TAG="v${TARGET}"

echo ""
echo "Step 5/6 — tag ${TAG} on ${SHA}"
if git rev-parse -q --verify "refs/tags/${TAG}" >/dev/null; then
  echo "  Tag ${TAG} already exists locally."
  if confirm "Move tag ${TAG} to current HEAD?"; then
    run git tag -f -a "${TAG}" -m "Natural Language Coding hub ${TARGET}"
  else
    echo "  Stopped: tag not updated." >&2
    exit 1
  fi
else
  run git tag -a "${TAG}" -m "Natural Language Coding hub ${TARGET}"
fi

echo ""
echo "Step 6/6 — push ${BRANCH} and ${TAG} to ${REMOTE}"
if [[ "${NO_PUSH}" -eq 1 ]]; then
  echo "  --no-push: done locally."
  echo ""
  echo "RELEASE:READY_LOCAL tag=${TAG} commit=${SHA}"
  exit 0
fi

if confirm "Push to ${REMOTE}?"; then
  run git push "${REMOTE}" "${BRANCH}"
  run git push "${REMOTE}" "${TAG}"
else
  echo "  Skipped push. Run when ready:"
  echo "    git push ${REMOTE} ${BRANCH}"
  echo "    git push ${REMOTE} ${TAG}"
  exit 0
fi

echo ""
echo "RELEASE:PUSHED ${TAG}"
echo "  GitHub Actions will build the tarball and publish the Release."
