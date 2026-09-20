# [Audit](../../docs/TERMS.md#audit) A-Q3 — [Quality snapshot](../../docs/TERMS.md#quality-snapshot) recorded at [boundary](../../docs/TERMS.md#boundary) exit

[Requirement](../../docs/TERMS.md#requirement): Q3

## Criterion

Every [boundary](../../docs/TERMS.md#boundary) exit that advances work must record a [quality snapshot](../../docs/TERMS.md#quality-snapshot).

## [Met](../../docs/TERMS.md#met) when

[Boundary](../../docs/TERMS.md#boundary) completion artifact includes `quality_snapshot` with all four required fields:

- `opportunities` (integer ≥ 0)
- `ops` (integer ≥ 0)
- `defects` (integer ≥ 0)
- `quality` (number 0.0 – 1.0)

AND `ops + defects = opportunities` (consistency check).

## Not [met](../../docs/TERMS.md#met) when

- `quality_snapshot` missing from completion artifact
- Any of the four required fields missing
- Field values inconsistent (`ops + defects ≠ opportunities`)
- `quality` value inconsistent with `ops / opportunities`

## Evidence

- Path to completion artifact
- Contents of `quality_snapshot` object
- Consistency verification: `ops + defects = opportunities`
- Formula verification: `quality ≈ ops / opportunities`

## Failure mode

[Boundary](../../docs/TERMS.md#boundary) exit blocked; completion artifact rejected as incomplete.

## Cross-references

- [`../QUALITY_METRIC.md`](../QUALITY_METRIC.md) — [Quality](../../docs/TERMS.md#quality) Metric SSOT
- [`../GATE.md`](../GATE.md) — [Gate](../../docs/TERMS.md#gate) definition
