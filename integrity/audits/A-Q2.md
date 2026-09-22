# [Audit](../../docs/TERMS.md#audit) A-Q2 — [Quality evidence](../../docs/TERMS.md#quality-evidence) required at adversarial [audit](../../docs/TERMS.md#audit)

[Requirement](../../docs/TERMS.md#requirement): Q2

## Criterion

Every artifact submitted to adversarial [audit](../../docs/TERMS.md#audit) must have [quality evidence](../../docs/TERMS.md#quality-evidence) traceable to SSOT.

## [Met](../../docs/TERMS.md#met) when

- `ssot_leaf_ids` present with at least one opaque leaf id
- `quality_snapshot` present and non-null
- `quality_snapshot.opportunities` > 0

## Not [met](../../docs/TERMS.md#met) when

- `ssot_leaf_ids` missing or empty
- `quality_snapshot` missing or null
- `quality_snapshot.opportunities` is 0 or missing

## Evidence

- Presence of `ssot_leaf_ids` array with ≥1 element
- Contents of `quality_snapshot` object
- Value of `quality_snapshot.opportunities`

## Failure mode

Adversarial [audit](../../docs/TERMS.md#audit) returns FAIL citing Q2. [Audit](../../docs/TERMS.md#audit) cannot [verify](../../docs/TERMS.md#verify) [quality](../../docs/TERMS.md#quality) without evidence.

## Cross-references

- [`../QUALITY_METRIC.md`](../QUALITY_METRIC.md) — [Quality](../../docs/TERMS.md#quality) Metric SSOT
- [`../../agents/adversarial-auditor/AGENT.md`](../../agents/adversarial-auditor/AGENT.md) — Adversarial Auditor
