# PR-003 Self-Adversarial Review

**PR:** #3  
**Role:** Self-adversarial review (S5 limitation acknowledged; recorded for bot audit)

---

## Adversarial checks with rule citations

### 1. load-applicability could leak produce authority

**Rule:** S5 (Produce ≠ Audit ≠ Ship), S6 (Audit roles have no ship verbs)

**Risk:** A query verb could secretly allow callers to modify standards, violating separation.

**Check performed:**
- Reviewed `load-applicability` output contract: returns data only, no mutation verbs exposed
- Explicit separation guarantee at `agents/standards-steward/verbs.md:127-133`
- Output schema has no write actions, only `rules_applicable`, `checklist_applicable`, `adrs_applicable`, `gates_required`

**Evidence:** `agents/standards-steward/verbs.md` line 127: "This verb is **read-only**. Calling `load-applicability` does NOT: Grant the caller produce authority..."

**Finding:** None. Query verb is read-only. S5/S6 not violated.

---

### 2. ship-role could self-ship

**Rule:** S5 (Produce ≠ Audit ≠ Ship)

**Risk:** Ship-role package could allow the same agent to produce and ship, violating separation.

**Check performed:**
- Reviewed `agents/ship-role/AGENT.md` invariant 5: "No self-ship. An agent that produced the artifact may not be the sole ship authority."
- Reviewed verb failure modes: all verbs return `SELF_SHIP` error code
- Reviewed preconditions in `agents/ship-role/verbs.md:297`: "No self-ship — Agent calling the verb did not solely produce the artifact"

**Evidence:** `agents/ship-role/AGENT.md` invariant 5 + verb error codes

**Finding:** None. Self-ship explicitly blocked. S5 honored.

---

### 3. ship-role could bypass audit

**Rule:** S5 (Produce ≠ Audit ≠ Ship), S3 (handoff-in preconditions)

**Risk:** Ship verbs could execute without audit completion, violating the pipeline.

**Check performed:**
- Reviewed `agents/ship-role/AGENT.md` invariant 1: "Ship follows produce and audit. A ship verb may only execute after the artifact has been produced and audited."
- Reviewed handoff-in: requires "Audit complete — Audit report with findings or clean status"
- Reviewed verb inputs: all require `audit_report_path`
- Reviewed failure modes: `AUDIT_INCOMPLETE` error code exists

**Evidence:** `agents/ship-role/AGENT.md` handoff-in table; verb input contracts

**Finding:** None. Audit required before ship. S3/S5 honored.

---

### 4. Gate ≠ Audit could be cosmetic only

**Rule:** R20 (charter, contracts, and code must agree)

**Risk:** Vocabulary change could just rename without clarifying mechanism difference.

**Check performed:**
- Reviewed `CHARTER.md:647-651` clarifying paragraph
- Confirms: "Gates block automatically; no human or role decides. Audits produce findings; a ship-role or human decides whether findings block."
- Reviewed `DESCRIBE.md:53-59` terminology section matches
- Reviewed ADR 0003 vocabulary mapping matches

**Evidence:** CHARTER.md §16.1 clarifying paragraph; ADR 0003 lines 30-31

**Finding:** None. Mechanism distinction is clear. R20 honored (charter/ADR agree).

---

### 5. Section renumbering could break references

**Rule:** R20 (charter, contracts, and code must agree), R22 (ADRs not deleted)

**Risk:** Renumbering §16.5→§16.6 could break existing references.

**Check performed:**
```bash
grep -r "§16\.5" --include="*.md" .  # before: Rules
grep -r "§16\.6" --include="*.md" .  # before: Confirmation
grep -r "§16\.7" --include="*.md" .  # new
```
- No external references to old §16.5 (Rules) or old §16.6 (Confirmation) found
- ADR 0003 references §16 generically, not subsection numbers
- DESCRIBE.md references §16 generically

**Evidence:** grep output shows no broken references

**Finding:** None. No broken references. R20/R22 honored.

---

### 6. ADR 0003 Consequences could drift from implementation

**Rule:** R20 (charter, contracts, and code must agree)

**Risk:** ADR says "first two agent nouns" but implementation has three.

**Check performed:**
- Original ADR 0003 said: "First two agent nouns: standards-steward and adversarial-auditor"
- After ship-role addition, this creates drift (R20 violation)
- **Fixed:** Updated to "Three agent nouns implement Produce ≠ Audit ≠ Ship: standards-steward (produce standards), adversarial-auditor (audit), ship-role (authorize release)"

**Evidence:** `adrs/0003-systems-extension-agent-nouns.md` line 61 (updated)

**Finding:** Fixed. ADR Consequences now matches implementation. R20 honored.

---

### 7. Binding matrix could have stale entries

**Rule:** R27 (every requirement in matrix), R28 (unbound entries fail)

**Risk:** New agent noun could require matrix updates not made.

**Check performed:**
- Ship-role is an agent noun; S1-S6 apply (already in matrix as unbound reference)
- No new rules S7+ were invented (per PLAN.md out of scope)
- Ran `python3 tools/audit-binding-matrix.py`: all audits MET

**Evidence:** Command output: `A-BINDING-COVERAGE:MET`, `A-BINDING-UNBOUND:MET`, `A-BINDING-PROMOTE:MET`

**Finding:** None. Matrix unchanged; ship-role validated against existing S1-S6. R27/R28 honored.

---

### 8. Verb contracts could be incomplete

**Rule:** S2 (every verb has input, output, failure mode), CS2 (same for checklist)

**Check performed:**
- Reviewed each verb in `agents/ship-role/verbs.md`:
  - `ratify`: input ✓, output ✓, failure mode ✓
  - `merge`: input ✓, output ✓, failure mode ✓
  - `release`: input ✓, output ✓, failure mode ✓
  - `waive-finding`: input ✓, output ✓, failure mode ✓
- Reviewed `load-applicability` in `agents/standards-steward/verbs.md`:
  - input ✓, output ✓, failure mode ✓

**Evidence:** `grep -c "### Input contract" agents/ship-role/verbs.md` returns 4

**Finding:** None. All verbs have complete I/O contracts. S2/CS2 honored.

---

### 9. Charter section numbers could have gaps

**Rule:** R20 (charter must be internally consistent)

**Risk:** Inserting §16.5 Ship noun without renumbering leaves a gap.

**Check performed:**
- Before fix: §16.5 Ship noun → §16.7 Rules (gap at §16.6)
- **Fixed:** Renumbered §16.7→§16.6, §16.8→§16.7
- Now: §16.1 Vocabulary → §16.2 Structure → §16.3 Produce≠Audit → §16.4 Audit no ship → §16.5 Ship noun → §16.6 Rules → §16.7 Checklist

**Evidence:** `grep "### 16\." CHARTER.md` shows consecutive numbering

**Finding:** Fixed. Section numbers consecutive. R20 honored.

---

## Limitations acknowledged

| Limitation | Rule | Mitigation |
|------------|------|------------|
| Self-review | S5 | Recorded transparently; bot can verify artifacts |
| No human reviewer | P-015 | Bot-auditable package provided |
| Ship-role not CI-bound | S1-S6 | Remain unbound reference; no false binder claimed |

---

## Summary

| Check | Rule(s) | Result |
|-------|---------|--------|
| Produce leak | S5, S6 | None found |
| Self-ship bypass | S5 | None found |
| Audit bypass | S3, S5 | None found |
| Cosmetic-only vocab | R20 | None found |
| Broken references | R20, R22 | None found |
| ADR drift | R20 | **Fixed** |
| Matrix staleness | R27, R28 | None found |
| Incomplete contracts | S2, CS2 | None found |
| Section gaps | R20 | **Fixed** |

All adversarial checks passed. Two issues found and fixed (ADR drift, section gap).
