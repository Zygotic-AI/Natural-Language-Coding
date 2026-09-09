# Audit A-Q2 — Quality evidence required at adversarial audit

Requirement: Q2

## Criterion

Every artifact submitted to adversarial audit must have quality evidence traceable to SSOT.

## Met when

- `ssot_leaf_ids` present with at least one opaque leaf id
- `quality_snapshot` present and non-null
- `quality_snapshot.opportunities` > 0

## Not met when

- `ssot_leaf_ids` missing or empty
- `quality_snapshot` missing or null
- `quality_snapshot.opportunities` is 0 or missing

## Evidence

- Presence of `ssot_leaf_ids` array with ≥1 element
- Contents of `quality_snapshot` object
- Value of `quality_snapshot.opportunities`

## Failure mode

Adversarial audit returns FAIL citing Q2. Audit cannot verify quality without evidence.

## Cross-references

- [`../QUALITY_METRIC.md`](../QUALITY_METRIC.md) — Quality Metric SSOT
- [`../../agents/adversarial-auditor/AGENT.md`](../../agents/adversarial-auditor/AGENT.md) — Adversarial Auditor
