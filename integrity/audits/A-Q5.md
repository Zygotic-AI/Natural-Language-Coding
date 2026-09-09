# Audit A-Q5 — Quality metric is ops/opportunities

Requirement: Q5

## Criterion

The quality metric formula is Ops divided by Opportunities. No alternative formulas (e.g., weighted scores, continuous grades) are used for the canonical quality metric.

## Met when

- Quality value equals `ops / opportunities` (within floating-point tolerance of 1e-9)
- No weighting factors applied to opportunities or defects
- No continuous scoring substituted for binary classification
- Formula used: `Quality = Ops / Opportunities`

## Not met when

- Quality computed with different formula
- Weighting factors applied
- Continuous scores used instead of binary op/defect counts
- Quality value does not match `ops / opportunities`

## Evidence

- Recorded `quality` value
- Recorded `ops` and `opportunities` values
- Verification: `|quality - (ops / opportunities)| < 1e-9`

## Failure mode

Quality metric rejected as non-conformant; SSOT sync refused.

## Cross-references

- [`../QUALITY_METRIC.md`](../QUALITY_METRIC.md) — Quality Metric SSOT (formula definition)
- Charter §16.6 S4 — Success criteria are binary (ops vs defects)
