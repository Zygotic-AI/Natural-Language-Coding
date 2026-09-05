#!/usr/bin/env bash
# Hub CI for fitness check 1 (R5 / C4 binder).
# Fail if: known-fail fixture PASSES (checker dead), or any non-fixture tree FAILS.
#
# Input: no argv. Working tree = repo root (parent of tools/).
#   Scans: runs assert-invoice-violation-fails.py (fixed fixture), then each
#   examples/*/ except invoice-violation via fitness-no-noun-field-writes.py.
#
# Output: section banners; child tool stdout (VIOLATION / RESULT / ASSERT / …);
#   CI:FAIL … on failure; CI:MET on success.
#
# Failure mode: process exit 0 = CI:MET (PASS); exit 1 = CI:FAIL (NOT_MET).
#   set -u; child failures are not swallowed — non-zero child → exit 1.
#
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "=== check 1: assert-invoice-violation-fails (fixture must still fail) ==="
python3 tools/assert-invoice-violation-fails.py || {
  echo "CI:FAIL fixture gate"
  exit 1
}

echo "=== check 1: non-fixture example trees must MET ==="
shopt -s nullglob
for d in examples/*/; do
  base="$(basename "$d")"
  if [ "$base" = "invoice-violation" ]; then
    continue
  fi
  echo "scanning $d"
  python3 tools/fitness-no-noun-field-writes.py "$d" || {
    echo "CI:FAIL non-fixture tree failed: $d"
    exit 1
  }
done

echo "CI:MET"
exit 0
