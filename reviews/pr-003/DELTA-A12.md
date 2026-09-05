# Delta A1/A2 — Adversarial Findings Fix

**PR:** #3  
**Findings:** A1 (Gate≠Audit bleed), A2 (R20 section drift)

---

## A1 — Gate≠Audit bleed

**Rule citations:** R20 (charter/code agreement), §16.1 (vocabulary: Gate = automated, Audit = role-based), S5 (Produce ≠ Audit ≠ Ship)

**Problem:** Ship noun Purpose used "Gate the transition" language. Per §16.1 vocabulary, Gate means automated enforcement. Ship is a role-based decision (S5), not automated.

**Fix:**

| File | Before | After |
|------|--------|-------|
| `CHARTER.md` §16.5 | "Gate the transition from 'done' to 'shipped'" | "Decide whether work moves from 'done' to 'shipped'" |
| `agents/ship-role/AGENT.md` | "Gate the transition from 'done' to 'shipped'" | "Authorize release — decide whether produced artifacts with audit findings may move from 'done' to 'shipped'" |

**Verification:** `grep -i "gate the transition" CHARTER.md agents/ship-role/AGENT.md` returns empty.

---

## A2 — R20 section drift

**Rule citations:** R20 (charter/code/contracts must agree)

**Problem:** Review artifacts cited §16.8 for Confirmation checklist, but charter has §16.7 after renumbering.

**Fix:**

| File | Before | After |
|------|--------|-------|
| `reviews/pr-003/APPLICABILITY.md` | "§16.8" heading | "§16.7" |
| `reviews/pr-003/BOUNDARY-IO.md` | Stale renumber notes | "Former §16.5 Rules → §16.6; Former §16.6 Confirmation → §16.7" |

**Verification:** `grep "§16\.8" reviews/pr-003/APPLICABILITY.md reviews/pr-003/BOUNDARY-IO.md` returns empty.

---

## Verification

```bash
bash reviews/pr-003/verify.sh  # exit 0
grep -i "gate the transition" CHARTER.md agents/ship-role/AGENT.md  # empty
grep "§16\.8" reviews/pr-003/APPLICABILITY.md reviews/pr-003/BOUNDARY-IO.md  # empty
```
