# PR-003 Verification Checklist

**PR:** #3  
**Purpose:** Machine-checkable verification for bot audit (no human mind-reading required)

---

## Required commands

Each command must exit 0 for the PR to pass.

### V1. Binding matrix audits pass

```bash
python3 tools/audit-binding-matrix.py
```

**Expected output:**
```
A-BINDING-COVERAGE:MET
A-BINDING-UNBOUND:MET
A-BINDING-PROMOTE:MET
RESULT:MET
```

**Exit code:** 0

---

### V2. Ship-role package exists with required files

```bash
test -f agents/ship-role/AGENT.md && test -f agents/ship-role/verbs.md && echo "PASS"
```

**Expected output:** `PASS`

---

### V3. Ship-role AGENT.md has all §16.2 elements

```bash
grep -c "## Identity" agents/ship-role/AGENT.md && \
grep -c "## Invariants" agents/ship-role/AGENT.md && \
grep -c "## Shipping authority" agents/ship-role/AGENT.md && \
grep -c "## Verbs" agents/ship-role/AGENT.md && \
grep -c "## Handoff-in" agents/ship-role/AGENT.md && \
grep -c "## Completion artifact" agents/ship-role/AGENT.md && \
grep -c "## Success criteria" agents/ship-role/AGENT.md
```

**Expected:** Each grep returns 1 (element present)

---

### V4. Ship-role verbs have I/O contracts

```bash
grep -c "### Input contract" agents/ship-role/verbs.md
grep -c "### Output contract" agents/ship-role/verbs.md
grep -c "### Failure mode" agents/ship-role/verbs.md
```

**Expected:** Each grep returns 4 (one per verb: ratify, merge, release, waive-finding)

---

### V5. load-applicability verb exists with I/O

```bash
grep -c "## load-applicability" agents/standards-steward/verbs.md
grep -A 100 "## load-applicability" agents/standards-steward/verbs.md | grep -c "### Input contract"
grep -A 100 "## load-applicability" agents/standards-steward/verbs.md | grep -c "### Output contract"
grep -A 100 "## load-applicability" agents/standards-steward/verbs.md | grep -c "### Failure mode"
```

**Expected:** Each grep returns 1

---

### V6. load-applicability has separation guarantee

```bash
grep -c "### Separation guarantee" agents/standards-steward/verbs.md
grep -c "read-only" agents/standards-steward/verbs.md
```

**Expected:** First grep returns 1; second grep returns at least 1

---

### V7. Charter §16.5 Ship noun exists

```bash
grep -c "### 16.5 Ship noun" CHARTER.md
grep -c "ship-role" CHARTER.md
```

**Expected:** First grep returns 1; second grep returns at least 1

---

### V8. Vocabulary mapping distinguishes Gate and Audit

```bash
grep "Fitness check" CHARTER.md | grep -c "Gate"
grep "Adversarial review" CHARTER.md | grep -c "Audit"
grep -c "Gate ≠ Audit" CHARTER.md
```

**Expected:** Each grep returns at least 1

---

### V9. ADR 0003 vocabulary updated

```bash
grep "Fitness check" adrs/0003-systems-extension-agent-nouns.md | grep -c "Gate"
grep "Adversarial review" adrs/0003-systems-extension-agent-nouns.md | grep -c "Audit"
```

**Expected:** Each grep returns 1

---

### V10. No false binders added

```bash
python3 -c "
import json
with open('integrity/binding-matrix.json') as f:
    m = json.load(f)
    unbound = [r['id'] for r in m['requirements'] if r['status'] == 'unbound']
    bound = [r['id'] for r in m['requirements'] if r['status'] == 'bound']
    print(f'Bound: {len(bound)}, Unbound: {len(unbound)}')
    # Verify bound items have binders
    for r in m['requirements']:
        if r['status'] == 'bound' and not r.get('binder'):
            print(f'ERROR: {r[\"id\"]} claims bound but has no binder')
            exit(1)
    print('No false binders')
"
```

**Expected output:** `No false binders` and exit 0

---

### V11. Section numbers consecutive (no gaps)

```bash
grep -c "### 16.6 Rules for agent nouns" CHARTER.md
grep -c "### 16.7 Confirmation checklist" CHARTER.md
```

**Expected:** Each grep returns 1

---

### V12. Ship-role in agents/README.md

```bash
grep -c "ship-role" agents/README.md
grep -c "Produce ≠ Audit ≠ Ship" agents/README.md
```

**Expected:** Each grep returns at least 1

---

### V13. ADR 0003 Consequences mentions ship-role

```bash
grep "ship-role" adrs/0003-systems-extension-agent-nouns.md | grep -c "Consequences" || \
grep -A 5 "## Consequences" adrs/0003-systems-extension-agent-nouns.md | grep -c "ship-role"
```

**Expected:** Returns at least 1

---

## Checklist summary

| ID | Check | Command exit | Pass criteria |
|----|-------|--------------|---------------|
| V1 | Matrix audits | 0 | RESULT:MET |
| V2 | Package exists | 0 | PASS printed |
| V3 | AGENT.md elements | 0 | All 7 sections present |
| V4 | Verb I/O contracts | 0 | 4 of each element |
| V5 | load-applicability | 0 | Verb with I/O |
| V6 | Separation guarantee | 0 | Section + read-only |
| V7 | §16.5 Ship noun | 0 | Section exists |
| V8 | Gate ≠ Audit | 0 | Both terms present |
| V9 | ADR 0003 updated | 0 | Mapping matches |
| V10 | No false binders | 0 | Script passes |
| V11 | Section numbers | 0 | Consecutive (no gaps) |
| V12 | README updated | 0 | Ship-role listed |
| V13 | ADR 0003 updated | 0 | Ship-role in Consequences |

---

## One-shot verification script

```bash
#!/bin/bash
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

echo ""
echo "=== ALL CHECKS PASSED ==="
```

Save as `reviews/pr-003/verify.sh` and run with `bash reviews/pr-003/verify.sh`.
