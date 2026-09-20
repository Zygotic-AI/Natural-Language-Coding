#!/usr/bin/env bash
# Session gate v1 — start of an agent session on this hub.
# Not a P2 binder. Fail = do not generate yet.
#
# Input: no argv. Repo root = parent of tools/.
# Output: SESSION:* lines; child matrix stdout; SESSION:MET|NOT_MET.
# Failure mode: exit 0 = MET; exit 1 = NOT_MET.
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

fail() {
  echo "SESSION:NOT_MET $*"
  exit 1
}

echo "SESSION:LOAD short-form .agents/bbp-short-form.md"
test -f .agents/bbp-short-form.md || fail "missing short-form"

echo "SESSION:LOAD charter CHARTER.md"
test -f CHARTER.md || fail "missing charter"

echo "SESSION:REMIND knowledge-steward load-knowledge-domain before generate"
echo "SESSION:REMIND confirmer python3 tools/ci_fitness.py"
echo "SESSION:REMIND ADR 0006 breaking contracts stay red until callers are in the plan"

echo "SESSION:MATRIX"
python3 tools/audit-binding-matrix.py || fail "binding matrix"

echo "SESSION:MET"
exit 0
