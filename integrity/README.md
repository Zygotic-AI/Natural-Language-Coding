# [Integrity](../docs/TERMS.md#integrity)

[Zero-variance](../docs/TERMS.md#zero-variance) practice [integrity](../docs/TERMS.md#integrity) for the [BBP](../docs/TERMS.md#bbp) [hub](../docs/TERMS.md#hub).

| Path | Role |
|------|------|
| [`PRINCIPLES.md`](PRINCIPLES.md) | P1–P7 with binary audits |
| [`BOUNDARY.md`](BOUNDARY.md) | [Boundary](../docs/TERMS.md#boundary) + [Handoff](../docs/TERMS.md#handoff) [noun](../docs/TERMS.md#noun) SSOT; role-bound SOP |
| [`BOUNDED_CONTEXT.md`](BOUNDED_CONTEXT.md) | Bounded Context [noun](../docs/TERMS.md#noun) SSOT; living system-as-is knowledge |
| [`GATE.md`](GATE.md) | [Gate](../docs/TERMS.md#gate) [noun](../docs/TERMS.md#noun) SSOT (G1–G4, incomplete-packet hunt) |
| [`CONTRIBUTION.md`](CONTRIBUTION.md) | [Shared docs standard](../docs/TERMS.md#shared-docs-standard) + [Contribution Gate](../docs/TERMS.md#contribution-gate) (G1–G4 refuse) |
| [`LEXICON.md`](LEXICON.md) | Locked term definitions (Action, Content type, Type recipe, etc.) |
| [`ACTIONS.md`](ACTIONS.md) | [Action](../docs/TERMS.md#action) [noun](../docs/TERMS.md#noun) SSOT; gated [action](../docs/TERMS.md#action) catalog; nesting [rule](../docs/TERMS.md#rule) |
| [`QUALITY_METRIC.md`](QUALITY_METRIC.md) | [Quality](../docs/TERMS.md#quality) metric SSOT (ops vs defects; Q1–Q5) |
| [`binding-matrix.md`](binding-matrix.md) | Matrix rules + unbound/promote audits |
| [`binding-matrix.json`](binding-matrix.json) | Machine index (requirement → audit → binder) |
| [`audits/`](audits/) | Per-requirement [audit](../docs/TERMS.md#audit) definitions |
| [`../content-types/HOW-TO-ADD.md`](../content-types/HOW-TO-ADD.md) | Type recipes for adding content (ADR, integrity doc, etc.) |
| [`../adrs/0001-zero-variance-integrity.md`](../adrs/0001-zero-variance-integrity.md) | Ratifying [ADR](../docs/TERMS.md#adr) |
| [`../tools/audit-binding-matrix.py`](../tools/audit-binding-matrix.py) | Binder for matrix audits (lists offenders; exit 1 on not met) |

Authoritative change checklist for adopters: [`../CHARTER.md`](../CHARTER.md) §11. Practice [integrity](../docs/TERMS.md#integrity) rules: [charter](../docs/TERMS.md#charter) §5.8.

**Current truth:** the matrix is mostly `unbound` by design until per-requirement binders exist. Running the matrix auditor must fail and list them.
