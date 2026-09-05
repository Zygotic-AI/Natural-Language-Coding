# Audit A-S8: Task/board SSOT exit evidence required

## Rule

**S8.** Produce packages require task/board SSOT exit evidence. Packages must include `ssot_leaf_ids` (one or more opaque leaf ids) and `ssot_exit_status` (non-empty exit state string). Missing SSOT exit evidence triggers `handoff_refused`; fitness scoring refuses MET; adversarial audit refuses PASS (P-020).

## Audit criteria

**Met** iff:

1. Every produce package in scope contains `ssot_leaf_ids` with at least one opaque leaf id.
2. Every produce package in scope contains `ssot_exit_status` with a non-empty status value.
3. Fitness preflight returns `handoff_refused` with `SSOT_EXIT_EVIDENCE` in missing enum when SSOT exit evidence is absent.
4. Fitness `score-fitness` returns `FAIL` (not `MET`) when SSOT exit evidence is missing.
5. Adversarial `audit-proposal` and `audit-diff` return error with `SSOT_EVIDENCE_MISSING` when evidence is absent.

**Not met** otherwise; report must enumerate missing `ssot_leaf_ids` / `ssot_exit_status`, MET without evidence, PASS without evidence.

## Evidence

- `reviews/pr-*/ADVERSARIAL.md` — `ssot_leaf_ids` and `ssot_exit_status`
- `agents/quality-architect/verbs.md` — `SSOT_EXIT_EVIDENCE` in missing enum
- `agents/adversarial-auditor/verbs.md` — `SSOT_EVIDENCE_MISSING` in error codes

## Related

- S7, CS8, P-020 — ADR 0005: SSOT exit evidence required
