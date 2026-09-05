# PR-005 Plan: Notion exit evidence required in gate packages (P-020)

## Classification

**Class F** — Charter rule change

## Summary

Implement P-020: Make Notion page id(s) and exit status first-class required fields on produce packages and fitness/adversarial receipts. Fitness refuses MET and adversarial audit refuses PASS without Notion evidence (same refuse class as P-016 produce package).

## Nouns touched

- **standards-steward** — update `complete-produce` verb to include `NOTION_EXIT_EVIDENCE` in missing enum
- **quality-architect** — update `preflight-fitness-handoff` and `score-fitness` verbs for Notion evidence
- **adversarial-auditor** — update handoff-in conditions; update `audit-proposal` and `audit-diff` verbs

## Goals touched

None (this is a charter/agent change, not a goal change)

## Workflows touched

None

## Boundary changes

1. **§6 Step 2** — Produce package description updated to include Notion exit evidence
2. **S8** — New rule: Produce packages require Notion exit evidence (page id + status)
3. **CS8** — New checklist item: Notion exit evidence present before fitness
4. **Binding matrix** — S8, CS8 added as reference (unbound)

## Invariants that must still hold

- S5 Produce ≠ Audit ≠ Ship — not violated; this strengthens produce boundary
- S7 Produce→fitness handoff default-closed — extended with Notion evidence requirement
- P6/P7 binding matrix audits — new entries are reference surface, unbound (no false binders)
- Existing agent nouns retain their invariants

## Non-goals

- Does not touch PR #3 / PR #4 scope except inheriting main
- Does not implement session gate wiring
- Does not create false binders
- Does not add product app code
- Does not add external task tracker support (Notion only for now)

## Test names

- `verify.sh` — structural checks for package presence, charter edits, and Notion evidence dogfooding

## Impact list

- Standards-steward consumers must include Notion evidence before fitness handoff
- Quality-architect preflight/score refuse without Notion evidence
- Adversarial-auditor handoff-in tightened; audit verbs refuse PASS without evidence
- All future produce packages require Notion page id(s) + exit status
