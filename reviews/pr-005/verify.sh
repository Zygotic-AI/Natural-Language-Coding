#!/usr/bin/env bash
# PR-005 verification script
# Structural checks for Notion exit evidence requirement (P-020)

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

echo "=== PR-005 Verification (P-020 Notion Exit Evidence) ==="
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

# 1. ADR 0005 exists
if [ -f "$REPO_ROOT/adrs/0005-notion-exit-evidence.md" ]; then
    check "ADR 0005 exists" "PASS"
else
    check "ADR 0005 exists" "FAIL"
fi

# 2. Charter has S8
if grep -q '^\*\*S8\.\*\*' "$REPO_ROOT/CHARTER.md" 2>/dev/null; then
    check "Charter has S8" "PASS"
else
    check "Charter has S8" "FAIL"
fi

# 3. Charter has CS8
if grep -q '\- \[ \] CS8\.' "$REPO_ROOT/CHARTER.md" 2>/dev/null; then
    check "Charter has CS8" "PASS"
else
    check "Charter has CS8" "FAIL"
fi

# 4. Charter Step 2 mentions Notion exit evidence
if grep -q 'Notion exit evidence' "$REPO_ROOT/CHARTER.md" 2>/dev/null; then
    check "Charter Step 2 mentions Notion exit evidence" "PASS"
else
    check "Charter Step 2 mentions Notion exit evidence" "FAIL"
fi

# 5. Binding matrix has S8
if grep -q '"id": "S8"' "$REPO_ROOT/integrity/binding-matrix.json" 2>/dev/null; then
    check "Binding matrix has S8" "PASS"
else
    check "Binding matrix has S8" "FAIL"
fi

# 6. Binding matrix has CS8
if grep -q '"id": "CS8"' "$REPO_ROOT/integrity/binding-matrix.json" 2>/dev/null; then
    check "Binding matrix has CS8" "PASS"
else
    check "Binding matrix has CS8" "FAIL"
fi

# 7. S8/CS8 are unbound (no false binders)
S8_UNBOUND=$(grep -A10 '"id": "S8"' "$REPO_ROOT/integrity/binding-matrix.json" 2>/dev/null | grep -c '"status": "unbound"' || echo 0)
if [ "$S8_UNBOUND" -ge 1 ]; then
    check "S8 is unbound (no false binder)" "PASS"
else
    check "S8 is unbound (no false binder)" "FAIL"
fi

CS8_UNBOUND=$(grep -A10 '"id": "CS8"' "$REPO_ROOT/integrity/binding-matrix.json" 2>/dev/null | grep -c '"status": "unbound"' || echo 0)
if [ "$CS8_UNBOUND" -ge 1 ]; then
    check "CS8 is unbound (no false binder)" "PASS"
else
    check "CS8 is unbound (no false binder)" "FAIL"
fi

# 8. Audit definitions exist
if [ -f "$REPO_ROOT/integrity/audits/A-S8.md" ]; then
    check "Audit definition A-S8.md exists" "PASS"
else
    check "Audit definition A-S8.md exists" "FAIL"
fi

if [ -f "$REPO_ROOT/integrity/audits/A-CS8.md" ]; then
    check "Audit definition A-CS8.md exists" "PASS"
else
    check "Audit definition A-CS8.md exists" "FAIL"
fi

# 9. Standards-steward verbs have NOTION_EXIT_EVIDENCE
if grep -q 'NOTION_EXIT_EVIDENCE' "$REPO_ROOT/agents/standards-steward/verbs.md" 2>/dev/null; then
    check "Standards-steward verbs have NOTION_EXIT_EVIDENCE" "PASS"
else
    check "Standards-steward verbs have NOTION_EXIT_EVIDENCE" "FAIL"
fi

# 10. Quality-architect verbs have NOTION_EXIT_EVIDENCE
if grep -q 'NOTION_EXIT_EVIDENCE' "$REPO_ROOT/agents/quality-architect/verbs.md" 2>/dev/null; then
    check "Quality-architect verbs have NOTION_EXIT_EVIDENCE" "PASS"
else
    check "Quality-architect verbs have NOTION_EXIT_EVIDENCE" "FAIL"
fi

# 11. Adversarial-auditor verbs have NOTION_EVIDENCE_MISSING
if grep -q 'NOTION_EVIDENCE_MISSING' "$REPO_ROOT/agents/adversarial-auditor/verbs.md" 2>/dev/null; then
    check "Adversarial-auditor verbs have NOTION_EVIDENCE_MISSING" "PASS"
else
    check "Adversarial-auditor verbs have NOTION_EVIDENCE_MISSING" "FAIL"
fi

# 12. AGENTS.md has Notion exit evidence instruction
if grep -q 'Notion exit evidence required' "$REPO_ROOT/AGENTS.md" 2>/dev/null; then
    check "AGENTS.md has Notion exit evidence instruction" "PASS"
else
    check "AGENTS.md has Notion exit evidence instruction" "FAIL"
fi

# 13. Produce package complete
PACKAGE_DIR="$REPO_ROOT/reviews/pr-005"
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

# 14. ADVERSARIAL.md has Notion page id (dogfood)
if grep -q '3d29d973-ccd7-81fa-9cb1-c7b01cf5a2da' "$PACKAGE_DIR/ADVERSARIAL.md" 2>/dev/null; then
    check "ADVERSARIAL.md has Notion page id (dogfood)" "PASS"
else
    check "ADVERSARIAL.md has Notion page id (dogfood)" "FAIL"
fi

# 15. ADVERSARIAL.md has notion_exit_status (dogfood)
if grep -q 'notion_exit_status:' "$PACKAGE_DIR/ADVERSARIAL.md" 2>/dev/null; then
    check "ADVERSARIAL.md has notion_exit_status (dogfood)" "PASS"
else
    check "ADVERSARIAL.md has notion_exit_status (dogfood)" "FAIL"
fi

# 16. Adversarial-auditor handoff-in mentions P-020
if grep -q 'P-020' "$REPO_ROOT/agents/adversarial-auditor/AGENT.md" 2>/dev/null; then
    check "Adversarial-auditor handoff-in mentions P-020" "PASS"
else
    check "Adversarial-auditor handoff-in mentions P-020" "FAIL"
fi

echo ""
echo "=== Summary ==="
echo "PASS: $PASS"
echo "FAIL: $FAIL"

if [ "$FAIL" -gt 0 ]; then
    echo ""
    echo "Verification FAILED"
    exit 1
else
    echo ""
    echo "Verification PASSED"
    exit 0
fi
