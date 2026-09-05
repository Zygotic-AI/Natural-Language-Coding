# PR-004 Applicability Statement

## Scope

This change applies to:

1. **Charter document** (`CHARTER.md`) — §6 Step 2, Step 2.5, §16.1, S7, CS7
2. **Binding matrix** (`integrity/binding-matrix.json`) — S7, CS7 entries
3. **Agent noun packages** (`agents/`) — standards-steward, quality-architect, adversarial-auditor
4. **Agent documentation** (`agents/README.md`) — ship-role handoff-in, vocabulary table
5. **ADR** (`adrs/0004-produce-fitness-handoff.md`) — decision record

## Exclusions

This change does **not** apply to:

- PR #3 or branch `cursor/close-deferred-audit-findings-9be0`
- Product application code
- Session gate implementation (deferred)
- Existing CI tooling (no binder changes)

## Applicability rationale

**Charter §16.3 (Produce ≠ Audit)** already separates produce from audit. This change strengthens the produce→audit handoff by making it default-closed. The change is consistent with existing practice; it formalizes what should have been enforced.

**P-015/KD-010** alignment: Quality north star requires default-closed boundaries. Fitness discovery loops are variance.

## Backward compatibility

- Existing proposals without produce packages will receive `handoff_refused` (not retroactive FAIL)
- No breaking change to existing bound rules
- New rules S7/CS7 are reference surface (unbound) — no false binders

## Forward compatibility

- Future binders for S7/CS7 will enforce produce package presence
- Future session gate wiring can reference this handoff contract
