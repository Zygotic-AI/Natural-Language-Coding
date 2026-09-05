#!/usr/bin/env bash
# PR-004 verification script
# Structural checks for produce package and charter edits

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

echo "=== PR-004 Verification ==="
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

# 1. ADR exists
if [ -f "$REPO_ROOT/adrs/0004-produce-fitness-handoff.md" ]; then
    check "ADR 0004 exists" "PASS"
else
    check "ADR 0004 exists" "FAIL"
fi

# 2. Charter has Step 2.5
if grep -q "Step 2.5 — Fitness preflight" "$REPO_ROOT/CHARTER.md" 2>/dev/null; then
    check "Charter has Step 2.5" "PASS"
else
    check "Charter has Step 2.5" "FAIL"
fi

# 3. Charter has S7
if grep -q '^\*\*S7\.\*\*' "$REPO_ROOT/CHARTER.md" 2>/dev/null; then
    check "Charter has S7" "PASS"
else
    check "Charter has S7" "FAIL"
fi

# 4. Charter has CS7
if grep -q '\- \[ \] CS7\.' "$REPO_ROOT/CHARTER.md" 2>/dev/null; then
    check "Charter has CS7" "PASS"
else
    check "Charter has CS7" "FAIL"
fi

# 5. Binding matrix has S7
if grep -q '"id": "S7"' "$REPO_ROOT/integrity/binding-matrix.json" 2>/dev/null; then
    check "Binding matrix has S7" "PASS"
else
    check "Binding matrix has S7" "FAIL"
fi

# 6. Binding matrix has CS7
if grep -q '"id": "CS7"' "$REPO_ROOT/integrity/binding-matrix.json" 2>/dev/null; then
    check "Binding matrix has CS7" "PASS"
else
    check "Binding matrix has CS7" "FAIL"
fi

# 7. S7/CS7 are unbound (no false binders)
S7_UNBOUND=$(grep -A10 '"id": "S7"' "$REPO_ROOT/integrity/binding-matrix.json" 2>/dev/null | grep -c '"status": "unbound"' || echo 0)
if [ "$S7_UNBOUND" -ge 1 ]; then
    check "S7 is unbound (no false binder)" "PASS"
else
    check "S7 is unbound (no false binder)" "FAIL"
fi

CS7_UNBOUND=$(grep -A10 '"id": "CS7"' "$REPO_ROOT/integrity/binding-matrix.json" 2>/dev/null | grep -c '"status": "unbound"' || echo 0)
if [ "$CS7_UNBOUND" -ge 1 ]; then
    check "CS7 is unbound (no false binder)" "PASS"
else
    check "CS7 is unbound (no false binder)" "FAIL"
fi

# 8. Quality-architect agent noun exists
if [ -f "$REPO_ROOT/agents/quality-architect/AGENT.md" ] && [ -f "$REPO_ROOT/agents/quality-architect/verbs.md" ]; then
    check "Quality-architect agent noun exists" "PASS"
else
    check "Quality-architect agent noun exists" "FAIL"
fi

# 9. Standards-steward has complete-produce verb
if grep -q "## complete-produce" "$REPO_ROOT/agents/standards-steward/verbs.md" 2>/dev/null; then
    check "Standards-steward has complete-produce verb" "PASS"
else
    check "Standards-steward has complete-produce verb" "FAIL"
fi

# 10. Adversarial-auditor handoff-in updated
if grep -q "Preflight ready" "$REPO_ROOT/agents/adversarial-auditor/AGENT.md" 2>/dev/null; then
    check "Adversarial-auditor handoff-in updated" "PASS"
else
    check "Adversarial-auditor handoff-in updated" "FAIL"
fi

# 11. Vocabulary table in README
VOCAB_CHECK=0
if grep -q "handoff_refused" "$REPO_ROOT/agents/README.md" 2>/dev/null; then
    VOCAB_CHECK=$((VOCAB_CHECK + 1))
fi
if grep -q "re-gate" "$REPO_ROOT/agents/README.md" 2>/dev/null; then
    VOCAB_CHECK=$((VOCAB_CHECK + 1))
fi
if [ "$VOCAB_CHECK" -ge 2 ]; then
    check "Vocabulary table in agents/README.md" "PASS"
else
    check "Vocabulary table in agents/README.md" "FAIL"
fi

# 12. Produce package complete
PACKAGE_DIR="$REPO_ROOT/reviews/pr-004"
PACKAGE_COUNT=0
[ -f "$PACKAGE_DIR/PLAN.md" ] && PACKAGE_COUNT=$((PACKAGE_COUNT + 1))
[ -f "$PACKAGE_DIR/APPLICABILITY.md" ] && PACKAGE_COUNT=$((PACKAGE_COUNT + 1))
[ -f "$PACKAGE_DIR/BOUNDARY-IO.md" ] && PACKAGE_COUNT=$((PACKAGE_COUNT + 1))
[ -f "$PACKAGE_DIR/ADVERSARIAL.md" ] && PACKAGE_COUNT=$((PACKAGE_COUNT + 1))
[ -f "$PACKAGE_DIR/verify.sh" ] && PACKAGE_COUNT=$((PACKAGE_COUNT + 1))

if [ "$PACKAGE_COUNT" -ge 5 ]; then
    check "Produce package complete" "PASS"
else
    check "Produce package complete" "FAIL"
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
