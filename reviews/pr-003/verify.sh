#!/bin/bash
# PR-003 verification script — bot-auditable checks
set -e

echo "=== V1: Binding matrix ==="
python3 tools/audit-binding-matrix.py

echo "=== V2: Package exists ==="
test -f agents/ship-role/AGENT.md && test -f agents/ship-role/verbs.md && echo "PASS"

echo "=== V3: AGENT.md elements ==="
for section in "Identity" "Invariants" "Shipping authority" "Verbs" "Handoff-in" "Completion artifact" "Success criteria"; do
    grep -q "## $section" agents/ship-role/AGENT.md && echo "$section: found" || exit 1
done

echo "=== V4: Verb I/O contracts ==="
[ $(grep -c "### Input contract" agents/ship-role/verbs.md) -eq 4 ] && echo "Input: 4"
[ $(grep -c "### Output contract" agents/ship-role/verbs.md) -eq 4 ] && echo "Output: 4"
[ $(grep -c "### Failure mode" agents/ship-role/verbs.md) -eq 4 ] && echo "Failure: 4"

echo "=== V5: load-applicability ==="
grep -q "## load-applicability" agents/standards-steward/verbs.md && echo "Verb: found"

echo "=== V6: Separation guarantee ==="
grep -q "### Separation guarantee" agents/standards-steward/verbs.md && echo "Guarantee: found"

echo "=== V7: §16.5 Ship noun ==="
grep -q "### 16.5 Ship noun" CHARTER.md && echo "Section: found"

echo "=== V8: Gate ≠ Audit ==="
grep -q "Gate — automated" CHARTER.md && echo "Gate: found"
grep -q "Audit — role-based" CHARTER.md && echo "Audit: found"

echo "=== V9: ADR 0003 ==="
grep "Fitness check" adrs/0003-systems-extension-agent-nouns.md | grep -q "Gate" && echo "ADR: updated"

echo "=== V10: No false binders ==="
python3 -c "
import json
with open('integrity/binding-matrix.json') as f:
    m = json.load(f)
    for r in m['requirements']:
        if r['status'] == 'bound' and not r.get('binder'):
            exit(1)
print('No false binders')
"

echo "=== V11: Section numbers consecutive ==="
grep -q "### 16.6 Rules for agent nouns" CHARTER.md && echo "16.6: found"
grep -q "### 16.7 Confirmation checklist" CHARTER.md && echo "16.7: found"

echo "=== V12: README updated ==="
grep -q "ship-role" agents/README.md && echo "ship-role: listed"

echo "=== V13: ADR 0003 Consequences ==="
grep -A 5 "## Consequences" adrs/0003-systems-extension-agent-nouns.md | grep -q "ship-role" && echo "ship-role: in Consequences"

echo ""
echo "=== ALL CHECKS PASSED ==="
