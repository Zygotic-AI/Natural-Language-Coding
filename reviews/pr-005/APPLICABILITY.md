# Applicability — SSOT exit evidence abstract delta

## Scope

1. `CHARTER.md` — §6 Step 2, S8, CS8
2. `adrs/0005-ssot-exit-evidence.md` (replace Notion-named ADR 0005 file)
3. `AGENTS.md` — P-020 standing instruction
4. `agents/standards-steward/{AGENT.md,verbs.md}`
5. `agents/quality-architect/verbs.md`
6. `agents/adversarial-auditor/{AGENT.md,verbs.md}`
7. `integrity/audits/A-S8.md`, `A-CS8.md`
8. `integrity/binding-matrix.json` — S8/CS8 statement text only
9. Produce package for this delta (dogfood abstract fields)

## Exclusions

- Implementation/bindings repo (product how-to)
- Product application code
- Session gate implementation
- Existing CI binders (none for S8/CS8; remain unbound)
- Requiring any board product brand in BBA artifacts

## Applicability rationale

**Principle lock:** BBA architecture definition must stay tool-agnostic. PR #5's Notion-named fields are an architecture-scope FAIL even if package completeness MET under that vocabulary.

**S7 / P-016:** Same refuse class — missing evidence → `handoff_refused` with missing-enum token; not soft-fail discovery.

**P7:** S8/CS8 stay reference/unbound until bindable.

## Backward compatibility

- Notion-named required fields are **removed** from BBA contracts (not aliased as dual-required)
- Opaque leaf id strings may still be UUID-shaped data without labeling the field as a product id
- No false binders introduced

## Forward compatibility

- Bindings repo may map `ssot_leaf_ids` ↔ product leaf ids without changing BBA
- Future binders enforce abstract field presence only
