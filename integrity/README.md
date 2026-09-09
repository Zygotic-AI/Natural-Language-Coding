# Integrity

Zero-variance practice integrity for the BBP hub.

| Path | Role |
|------|------|
| [`PRINCIPLES.md`](PRINCIPLES.md) | P1–P7 with binary audits |
| [`QUALITY_METRIC.md`](QUALITY_METRIC.md) | Quality metric SSOT (ops vs defects; Q1–Q5) |
| [`binding-matrix.md`](binding-matrix.md) | Matrix rules + unbound/promote audits |
| [`binding-matrix.json`](binding-matrix.json) | Machine index (requirement → audit → binder) |
| [`audits/`](audits/) | Per-requirement audit definitions |
| [`../adrs/0001-zero-variance-integrity.md`](../adrs/0001-zero-variance-integrity.md) | Ratifying ADR |
| [`../tools/audit-binding-matrix.py`](../tools/audit-binding-matrix.py) | Binder for matrix audits (lists offenders; exit 1 on not met) |

Authoritative change checklist for adopters: [`../CHARTER.md`](../CHARTER.md) §11. Practice integrity rules: charter §5.8.

**Current truth:** the matrix is mostly `unbound` by design until per-requirement binders exist. Running the matrix auditor must fail and list them.
