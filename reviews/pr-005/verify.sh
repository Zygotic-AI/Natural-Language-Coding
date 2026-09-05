#!/usr/bin/env bash
# Verification draft — abstract P-020 (task/board SSOT exit evidence)
# Intended to run from a landed BBA tree (REPO_ROOT). Adjust PACKAGE_DIR if review path differs.

set -euo pipefail

REPO_ROOT="${REPO_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
PACKAGE_DIR="${PACKAGE_DIR:-$REPO_ROOT/reviews/pr-005}"
# When verifying this draft kit in isolation:
if [ ! -f "$REPO_ROOT/CHARTER.md" ] && [ -f "$(dirname "${BASH_SOURCE[0]}")/ADVERSARIAL.md" ]; then
  PACKAGE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fi

echo "=== P-020 Abstract SSOT Exit Evidence Verification ==="
echo "REPO_ROOT=$REPO_ROOT"
echo "PACKAGE_DIR=$PACKAGE_DIR"
echo ""

PASS=0
FAIL=0

check() {
  local desc="$1"
  local result="$2"
  if [ "$result" = "PASS" ]; then
    echo "[PASS] $desc"
    PASS=$((PASS + 1))
  else
    echo "[FAIL] $desc"
    FAIL=$((FAIL + 1))
  fi
}

# --- ADR rename ---
if [ -f "$REPO_ROOT/adrs/0005-ssot-exit-evidence.md" ]; then
  check "ADR 0005 abstract file exists (0005-ssot-exit-evidence.md)" "PASS"
else
  check "ADR 0005 abstract file exists (0005-ssot-exit-evidence.md)" "FAIL"
fi

if [ -f "$REPO_ROOT/adrs/0005-notion-exit-evidence.md" ]; then
  check "Old Notion-named ADR 0005 file removed" "FAIL"
else
  check "Old Notion-named ADR 0005 file removed" "PASS"
fi

# --- Charter abstract prose ---
if grep -q '^\*\*S8\.\*\*' "$REPO_ROOT/CHARTER.md" 2>/dev/null && grep -q 'SSOT exit evidence\|task/board SSOT exit evidence\|ssot_leaf_ids' "$REPO_ROOT/CHARTER.md" 2>/dev/null; then
  check "Charter S8 uses SSOT exit evidence vocabulary" "PASS"
else
  check "Charter S8 uses SSOT exit evidence vocabulary" "FAIL"
fi

if grep -q '\- \[ \] CS8\.' "$REPO_ROOT/CHARTER.md" 2>/dev/null && grep -A1 '\- \[ \] CS8\.' "$REPO_ROOT/CHARTER.md" 2>/dev/null | grep -q 'SSOT\|ssot_leaf_ids'; then
  check "Charter CS8 uses SSOT exit evidence vocabulary" "PASS"
else
  check "Charter CS8 uses SSOT exit evidence vocabulary" "FAIL"
fi

if grep -q 'ssot_leaf_ids' "$REPO_ROOT/CHARTER.md" 2>/dev/null; then
  check "Charter Step 2 / package sentence mentions ssot_leaf_ids" "PASS"
else
  check "Charter Step 2 / package sentence mentions ssot_leaf_ids" "FAIL"
fi

# --- No required Notion vocabulary in architecture surfaces ---
ARCH_Grep_FAIL=0
for f in \
  "$REPO_ROOT/CHARTER.md" \
  "$REPO_ROOT/AGENTS.md" \
  "$REPO_ROOT/agents/standards-steward/AGENT.md" \
  "$REPO_ROOT/agents/standards-steward/verbs.md" \
  "$REPO_ROOT/agents/quality-architect/verbs.md" \
  "$REPO_ROOT/agents/adversarial-auditor/AGENT.md" \
  "$REPO_ROOT/agents/adversarial-auditor/verbs.md" \
  "$REPO_ROOT/integrity/audits/A-S8.md" \
  "$REPO_ROOT/integrity/audits/A-CS8.md"
do
  if [ -f "$f" ] && grep -Eq 'notion_page_ids|notion_exit_status|NOTION_EXIT_EVIDENCE|NOTION_EVIDENCE_MISSING' "$f"; then
    echo "  leftover Notion token in: $f"
    ARCH_Grep_FAIL=1
  fi
done
# Matrix statements for S8/CS8 must not say Notion
if grep -A6 '"id": "S8"' "$REPO_ROOT/integrity/binding-matrix.json" 2>/dev/null | grep -qi Notion; then
  ARCH_Grep_FAIL=1
  echo "  leftover Notion in S8 matrix statement"
fi
if grep -A6 '"id": "CS8"' "$REPO_ROOT/integrity/binding-matrix.json" 2>/dev/null | grep -qi Notion; then
  ARCH_Grep_FAIL=1
  echo "  leftover Notion in CS8 matrix statement"
fi

if [ "$ARCH_Grep_FAIL" -eq 0 ]; then
  check "No required Notion field/enum tokens in BBA architecture surfaces" "PASS"
else
  check "No required Notion field/enum tokens in BBA architecture surfaces" "FAIL"
fi

# ADR Rejected may mention Notion once — allow only in abstract ADR file
if [ -f "$REPO_ROOT/adrs/0005-ssot-exit-evidence.md" ]; then
  if grep -q 'Notion-named fields in BBA charter' "$REPO_ROOT/adrs/0005-ssot-exit-evidence.md"; then
    check "ADR Rejected includes Notion-named fields rejection" "PASS"
  else
    check "ADR Rejected includes Notion-named fields rejection" "FAIL"
  fi
fi

# --- Matrix unbound ---
if grep -q '"id": "S8"' "$REPO_ROOT/integrity/binding-matrix.json" 2>/dev/null; then
  check "Binding matrix has S8" "PASS"
else
  check "Binding matrix has S8" "FAIL"
fi
if grep -q '"id": "CS8"' "$REPO_ROOT/integrity/binding-matrix.json" 2>/dev/null; then
  check "Binding matrix has CS8" "PASS"
else
  check "Binding matrix has CS8" "FAIL"
fi
S8_UNBOUND=$(grep -A10 '"id": "S8"' "$REPO_ROOT/integrity/binding-matrix.json" 2>/dev/null | grep -c '"status": "unbound"' || true)
if [ "${S8_UNBOUND:-0}" -ge 1 ]; then
  check "S8 unbound (no false binder)" "PASS"
else
  check "S8 unbound (no false binder)" "FAIL"
fi
CS8_UNBOUND=$(grep -A10 '"id": "CS8"' "$REPO_ROOT/integrity/binding-matrix.json" 2>/dev/null | grep -c '"status": "unbound"' || true)
if [ "${CS8_UNBOUND:-0}" -ge 1 ]; then
  check "CS8 unbound (no false binder)" "PASS"
else
  check "CS8 unbound (no false binder)" "FAIL"
fi

# --- Abstract tokens in verbs ---
if grep -q 'SSOT_EXIT_EVIDENCE' "$REPO_ROOT/agents/standards-steward/verbs.md" 2>/dev/null \
   && grep -q 'ssot_leaf_ids' "$REPO_ROOT/agents/standards-steward/verbs.md" 2>/dev/null; then
  check "Standards-steward verbs have SSOT_EXIT_EVIDENCE + ssot_leaf_ids" "PASS"
else
  check "Standards-steward verbs have SSOT_EXIT_EVIDENCE + ssot_leaf_ids" "FAIL"
fi

if grep -q 'SSOT_EXIT_EVIDENCE' "$REPO_ROOT/agents/quality-architect/verbs.md" 2>/dev/null \
   && grep -q 'ssot_leaf_ids' "$REPO_ROOT/agents/quality-architect/verbs.md" 2>/dev/null; then
  check "Quality-architect verbs have SSOT_EXIT_EVIDENCE + ssot_leaf_ids" "PASS"
else
  check "Quality-architect verbs have SSOT_EXIT_EVIDENCE + ssot_leaf_ids" "FAIL"
fi

if grep -q 'SSOT_EVIDENCE_MISSING' "$REPO_ROOT/agents/adversarial-auditor/verbs.md" 2>/dev/null \
   && grep -q 'ssot_leaf_ids' "$REPO_ROOT/agents/adversarial-auditor/verbs.md" 2>/dev/null; then
  check "Adversarial-auditor verbs have SSOT_EVIDENCE_MISSING + ssot_leaf_ids" "PASS"
else
  check "Adversarial-auditor verbs have SSOT_EVIDENCE_MISSING + ssot_leaf_ids" "FAIL"
fi

# --- AGENTS.md ---
if grep -q 'SSOT exit evidence required\|ssot_leaf_ids' "$REPO_ROOT/AGENTS.md" 2>/dev/null; then
  check "AGENTS.md has abstract SSOT exit evidence instruction" "PASS"
else
  check "AGENTS.md has abstract SSOT exit evidence instruction" "FAIL"
fi

# --- Audits ---
if [ -f "$REPO_ROOT/integrity/audits/A-S8.md" ] && grep -q 'ssot_leaf_ids' "$REPO_ROOT/integrity/audits/A-S8.md"; then
  check "A-S8.md uses ssot_leaf_ids" "PASS"
else
  check "A-S8.md uses ssot_leaf_ids" "FAIL"
fi
if [ -f "$REPO_ROOT/integrity/audits/A-CS8.md" ] && grep -q 'ssot_leaf_ids' "$REPO_ROOT/integrity/audits/A-CS8.md"; then
  check "A-CS8.md uses ssot_leaf_ids" "PASS"
else
  check "A-CS8.md uses ssot_leaf_ids" "FAIL"
fi

# --- Produce package + dogfood ---
PACKAGE_COUNT=0
[ -f "$PACKAGE_DIR/PLAN.md" ] && PACKAGE_COUNT=$((PACKAGE_COUNT + 1))
[ -f "$PACKAGE_DIR/APPLICABILITY.md" ] && PACKAGE_COUNT=$((PACKAGE_COUNT + 1))
[ -f "$PACKAGE_DIR/BOUNDARY-IO.md" ] && PACKAGE_COUNT=$((PACKAGE_COUNT + 1))
[ -f "$PACKAGE_DIR/ADVERSARIAL.md" ] && PACKAGE_COUNT=$((PACKAGE_COUNT + 1))
[ -f "$PACKAGE_DIR/verify.sh" ] && PACKAGE_COUNT=$((PACKAGE_COUNT + 1))
if [ "$PACKAGE_COUNT" -ge 5 ]; then
  check "Produce package complete (5/5 files)" "PASS"
else
  check "Produce package complete ($PACKAGE_COUNT/5 files)" "FAIL"
fi

DOGFOOD_LEAF="3d29d973-ccd7-8158-a1c2-e8d46be9bbef"
PARKED_LEAF="3d29d973-ccd7-81fa-9cb1-c7b01cf5a2da"

if grep -q 'ssot_leaf_ids' "$PACKAGE_DIR/ADVERSARIAL.md" 2>/dev/null \
   && grep -q "$DOGFOOD_LEAF" "$PACKAGE_DIR/ADVERSARIAL.md" 2>/dev/null; then
  check "ADVERSARIAL.md dogfoods ssot_leaf_ids with abstract leaf …bbef" "PASS"
else
  check "ADVERSARIAL.md dogfoods ssot_leaf_ids with abstract leaf …bbef" "FAIL"
fi

if grep -q 'ssot_exit_status:' "$PACKAGE_DIR/ADVERSARIAL.md" 2>/dev/null \
   && grep -q 'in progress' "$PACKAGE_DIR/ADVERSARIAL.md" 2>/dev/null; then
  check "ADVERSARIAL.md has ssot_exit_status: in progress" "PASS"
else
  check "ADVERSARIAL.md has ssot_exit_status: in progress" "FAIL"
fi

# Must not dogfood parked leaf; must not label dogfood as Notion fields
if grep -q "$PARKED_LEAF" "$PACKAGE_DIR/ADVERSARIAL.md" 2>/dev/null; then
  check "ADVERSARIAL.md does not dogfood parked leaf …a2da" "FAIL"
else
  check "ADVERSARIAL.md does not dogfood parked leaf …a2da" "PASS"
fi

if grep -Eq 'notion_page_ids:|notion_exit_status:' "$PACKAGE_DIR/ADVERSARIAL.md" 2>/dev/null; then
  check "ADVERSARIAL.md does not use Notion-named dogfood fields" "FAIL"
else
  check "ADVERSARIAL.md does not use Notion-named dogfood fields" "PASS"
fi

echo ""
echo "=== Summary ==="
echo "PASS: $PASS"
echo "FAIL: $FAIL"

if [ "$FAIL" -gt 0 ]; then
  echo "Verification FAILED (expected until landed on BBA tree; kit self-check may N/A charter paths)"
  exit 1
fi
echo "Verification PASSED"
exit 0
