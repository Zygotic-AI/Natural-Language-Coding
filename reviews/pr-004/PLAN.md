# PR-004 Plan: Produce→fitness handoff default-closed (P-016)

## Classification

**Class F** — Charter rule change

## Summary

Implement P-016: Make the produce→fitness handoff default-closed. Producers cannot claim ready without a complete produce package. Fitness preflight refuses incomplete handoffs rather than soft-failing them.

## Nouns touched

- **standards-steward** — add `complete-produce` verb
- **quality-architect** — new agent noun with `preflight-fitness-handoff` and `score-fitness` verbs
- **adversarial-auditor** — update handoff-in conditions

## Goals touched

None (this is a charter/agent change, not a goal change)

## Workflows touched

None

## Boundary changes

1. **§6 Step 2** — Produce package required for handoff
2. **§6 Step 2.5** — New fitness preflight step
3. **§16.1** — Handoff refused ≠ fitness FAIL clarification
4. **S7** — New rule: Produce→fitness handoff default-closed
5. **CS7** — New checklist item: Package present before fitness
6. **Binding matrix** — S7, CS7 added as reference (unbound)

## Invariants that must still hold

- S5 Produce ≠ Audit ≠ Ship — not violated; this strengthens produce boundary
- P6/P7 binding matrix audits — new entries are reference surface, unbound (no false binders)
- Existing agent nouns retain their invariants

## Non-goals

- Does not touch PR #3 / branch cursor/close-deferred-audit-findings-9be0
- Does not implement session gate wiring
- Does not create false binders
- Does not add product app code

## Test names

- `verify.sh` — structural checks for package presence and charter edits

## Impact list

- Standards-steward consumers must use `complete-produce` verb before fitness handoff
- Quality-architect is a new agent noun (no existing callers)
- Adversarial-auditor handoff-in conditions tightened (preflight ready required)
- Ship-role handoff-in documented (fitness MET, no open handoff_refused)
