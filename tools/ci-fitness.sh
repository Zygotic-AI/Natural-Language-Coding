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
for a in \
  tools/assert-invoice-violation-fails.py \
  tools/assert-verb-path-violation-fails.py \
  tools/assert-adjective-locality-violation-fails.py \
  tools/assert-contract-presence-fails.py \
  tools/assert-schema-identity-fails.py \
  tools/assert-boundary-io-fails.py \
  tools/assert-taint-violation-fails.py \
  tools/assert-escape-hatch-violation-fails.py \
  tools/assert-duplicated-adjective-fails.py \
  tools/assert-r13-fails.py \
  tools/assert-c21-fails.py \
  tools/assert-r25-fails.py \
  tools/assert-c16-fails.py \
  tools/assert-c17-fails.py \
  tools/assert-c18-fails.py \
  tools/assert-r12-fails.py \
  tools/assert-c1-fails.py \
  tools/assert-r15-fails.py \
  tools/assert-r17-fails.py \
  tools/assert-r18-fails.py \
  tools/assert-c15-fails.py \
  tools/assert-c2-fails.py \
  tools/assert-c24-fails.py \
  tools/assert-c3-fails.py \
  tools/assert-r4-fails.py \
  tools/assert-c13-fails.py \
  tools/assert-c10-fails.py \
  tools/assert-c22-fails.py \
  tools/assert-c23-fails.py
















do
  echo "--- $a ---"
  python3 "$a" || fail "$a"
done

echo "=== designed-pass impact graph ==="
python3 tools/assert-impact-graph-generated.py || fail "impact graph"

echo "=== invoice-correct must MET on bound v1 tools ==="
CORRECT=examples/invoice-correct
for t in \
  tools/fitness-no-noun-field-writes.py \
  tools/fitness-verb-path.py \
  tools/fitness-adjective-locality.py \
  tools/fitness-contract-presence.py \
  tools/fitness-schema-identity.py \
  tools/fitness-boundary-io.py \
  tools/fitness-taint-lifetime.py \
  tools/fitness-escape-hatch.py \
  tools/fitness-duplicated-adjective.py \
  tools/fitness-r13-entrypoints.py \
  tools/fitness-c21.py \
  tools/fitness-goal-imports.py \
  tools/fitness-c20.py \
  tools/fitness-p4-r31.py \
  tools/fitness-r25-noun-tests.py \
  tools/fitness-c16.py \
  tools/fitness-c17.py \
  tools/fitness-c18.py \
  tools/fitness-r12-version.py \
  tools/fitness-c1.py \
  tools/fitness-r15-copied-helpers.py \
  tools/fitness-r17-workflow-citizen.py \
  tools/fitness-r18-noun-retries.py \
  tools/fitness-c15-idempotent.py \
  tools/fitness-c2.py \
  tools/fitness-c24.py \
  tools/fitness-c3.py \
  tools/fitness-r4.py \
  tools/fitness-c13.py \
  tools/fitness-c10.py \
  tools/fitness-c22.py \
  tools/fitness-c23.py















do
  echo "--- $t $CORRECT ---"
  python3 "$t" "$CORRECT" || fail "$t on invoice-correct"
done

echo "=== binding matrix ==="
python3 tools/audit-binding-matrix.py || fail "binding matrix"

echo "CI:MET"
exit 0
