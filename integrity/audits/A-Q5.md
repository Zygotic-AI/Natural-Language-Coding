# [Audit](../../docs/TERMS.md#audit) A-Q5 — [Quality](../../docs/TERMS.md#quality) metric is ops/opportunities

[Requirement](../../docs/TERMS.md#requirement): Q5

## Criterion

The [quality](../../docs/TERMS.md#quality) metric formula is Ops divided by Opportunities. No alternative formulas (e.g., weighted scores, continuous grades) are used for the canonical [quality](../../docs/TERMS.md#quality) metric.

## [Met](../../docs/TERMS.md#met) when

- [Quality](../../docs/TERMS.md#quality) value equals `ops / opportunities` (within floating-point tolerance of 1e-9)
- No weighting factors applied to opportunities or defects
- No continuous scoring substituted for binary classification
- Formula used: `Quality = Ops / Opportunities`

## Not [met](../../docs/TERMS.md#met) when

- [Quality](../../docs/TERMS.md#quality) computed with different formula
- Weighting factors applied
- Continuous scores used instead of binary op/defect counts
- [Quality](../../docs/TERMS.md#quality) value does not match `ops / opportunities`

## Evidence

- Recorded `quality` value
- Recorded `ops` and `opportunities` values
- Verification: `|quality - (ops / opportunities)| < 1e-9`

## Failure mode

[Quality](../../docs/TERMS.md#quality) metric rejected as non-conformant; SSOT sync refused.

## Cross-references

- [`../QUALITY_METRIC.md`](../QUALITY_METRIC.md) — [Quality](../../docs/TERMS.md#quality) Metric SSOT (formula definition)
- [Charter](../../docs/TERMS.md#charter) §16.6 S4 — Success criteria are binary (ops vs defects)
