#!/usr/bin/env bash
# Hub CI for all designed-fail landmines + invoice-correct on bound v1 tools.
#
# Input: no argv. Working tree = repo root (parent of tools/).
# Output: section banners; child stdout; CI:FAIL … or CI:MET.
# Failure mode: exit 0 = CI:MET; exit 1 = CI:FAIL. Child failures not swallowed.
#
# Does not scan the whole hub ROOT with code-side tools (specimens would go red).
# Charter §14 check 1 is still tools/ci-fitness-check1.sh; this script calls it first.
#
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

fail() {
  echo "CI:FAIL $*"
  exit 1
}

echo "=== session preflight v1 ==="
bash tools/session-preflight.sh || fail "session preflight"

echo "=== charter §14 check 1 ==="

bash tools/ci-fitness-check1.sh || fail "check 1"

echo "=== designed-fail landmines (assert exit 0 = landmine live) ==="
shopt -s nullglob
for a in tools/assert-*-fails.py; do
  echo "--- $a ---"
  python3 "$a" || fail "$a"
done

echo "=== designed-pass impact graph ==="
python3 tools/assert-impact-graph-generated.py || fail "impact graph"
python3 tools/assert-release-signed-passes.py || fail "release signed"


echo "=== invoice-correct must MET on bound tools ==="
CORRECT=examples/invoice-correct
shopt -s nullglob
for t in tools/fitness-*.py; do
  echo "--- $t $CORRECT ---"
  python3 "$t" "$CORRECT" || fail "$t on invoice-correct"
done

echo "=== changed-only-ok must MET on C7/C11 ==="
python3 tools/fitness-contract-presence.py examples/changed-only-ok || fail "C7 on changed-only-ok"
python3 tools/fitness-r13-entrypoints.py examples/changed-only-ok || fail "C11 on changed-only-ok"
echo "=== retrying-nested-ok must MET on C15 ==="
python3 tools/fitness-c15-idempotent.py examples/retrying-nested-ok || fail "C15 on retrying-nested-ok"

echo "=== binding matrix ==="
python3 tools/audit-binding-matrix.py || fail "binding matrix"

echo "CI:MET"
exit 0
