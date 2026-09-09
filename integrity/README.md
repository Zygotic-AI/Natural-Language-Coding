# Integrity

Zero-variance practice integrity for the BBP hub.

| Path | Role |
|------|------|
| [`PRINCIPLES.md`](PRINCIPLES.md) | P1–P7 with binary audits |
| [`BOUNDARY.md`](BOUNDARY.md) | Boundary + Handoff noun SSOT; role-bound SOP |
| [`BOUNDED_CONTEXT.md`](BOUNDED_CONTEXT.md) | Bounded Context noun SSOT; living system-as-is knowledge |
| [`GATE.md`](GATE.md) | Gate noun SSOT; G1–G4, incomplete-packet hunt |
| [`binding-matrix.md`](binding-matrix.md) | Matrix rules + unbound/promote audits |
| [`binding-matrix.json`](binding-matrix.json) | Machine index (requirement → audit → binder) |
| [`audits/`](audits/) | Per-requirement audit definitions |
| [`../adrs/0001-zero-variance-integrity.md`](../adrs/0001-zero-variance-integrity.md) | Ratifying ADR |
| [`../tools/audit-binding-matrix.py`](../tools/audit-binding-matrix.py) | Binder for matrix audits (lists offenders; exit 1 on not met) |

Authoritative change checklist for adopters: [`../CHARTER.md`](../CHARTER.md) §11. Practice integrity rules: charter §5.8.

**Current truth:** the matrix is mostly `unbound` by design until per-requirement binders exist. Running the matrix auditor must fail and list them.
