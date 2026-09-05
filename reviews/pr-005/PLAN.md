# Plan: Abstract P-020 to task/board SSOT exit evidence

## Classification

**Class F** — Charter / agent contract change

## Summary

Rewrite PR #5's Notion-coupled P-020 surface into tool-agnostic **task/board SSOT exit evidence**. Keep S8/CS8, A-S8/A-CS8, P-020 / ADR 0005 identity. Rename ADR file to `adrs/0005-ssot-exit-evidence.md`. Field names become `ssot_leaf_ids` / `ssot_exit_status`; missing enum `SSOT_EXIT_EVIDENCE`; error `SSOT_EVIDENCE_MISSING`.

**Architecture FAIL on prior Notion surface:** BBA is tool-agnostic; product-named fields in charter/agent verbs violate the principle lock. Prior MET on the Notion surface is superseded for architecture scope.

## Principle lock (must honor)

- BBA = architecture definition; tool-agnostic
- No Notion brand, no MCP, no Cursor/Grok product bindings in charter / AGENTS.md / agent verb field names
- Tool bindings belong in a separate implementation/bindings repo (mention only as out of scope — do not invent contents)

## Nouns touched

- **standards-steward** — `complete-produce` + AGENT completion/handoff-out
- **quality-architect** — `preflight-fitness-handoff`, `score-fitness`
- **adversarial-auditor** — handoff-in; `audit-proposal`, `audit-diff`

## Goals / workflows touched

None

## Boundary changes

1. §6 Step 2 — package sentence uses SSOT exit evidence
2. S8 / CS8 — abstract prose + field names
3. ADR 0005 — rewrite + rename file
4. AGENTS.md — abstract standing instruction
5. A-S8 / A-CS8 + matrix statements — abstract
6. Verb contracts — abstract fields/enums/errors

## Invariants that must still hold

- S5 Produce ≠ Audit ≠ Ship
- S7 default-closed handoff; same refuse class extended by S8
- P1 stand-alone / tool-agnostic branding
- P6/P7 — S8/CS8 remain reference/unbound; no false binders
- Fail-closed refuse pattern unchanged (same class as S7/P-016)

## Non-goals

- Inventing implementation/bindings repo contents
- Session gate wiring
- CI binders for S8/CS8
- Product application code
- Dual Notion + SSOT required vocabulary
- Dogfooding parked leaf `3d29d973-ccd7-81fa-9cb1-c7b01cf5a2da`

## Test names

- `verify.sh` — structural checks for abstract surface + absence of required Notion vocabulary + dogfood of abstract fields

## Impact list

- All future produce packages use `ssot_leaf_ids` + `ssot_exit_status`
- Fitness/adversarial refuse without SSOT exit evidence
- Consumers of Notion-named BBA fields must migrate to abstract names (bindings repo owns product mapping)
