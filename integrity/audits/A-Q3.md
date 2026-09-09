# Audit A-Q3 — Quality snapshot recorded at boundary exit

Requirement: Q3

## Criterion

Every boundary exit that advances work must record a quality snapshot.

## Met when

Boundary completion artifact includes `quality_snapshot` with all four required fields:

- `opportunities` (integer ≥ 0)
- `ops` (integer ≥ 0)
- `defects` (integer ≥ 0)
- `quality` (number 0.0 – 1.0)

AND `ops + defects = opportunities` (consistency check).

## Not met when

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

Boundary exit blocked; completion artifact rejected as incomplete.

## Cross-references

- [`../QUALITY_METRIC.md`](../QUALITY_METRIC.md) — Quality Metric SSOT
- [`../GATE.md`](../GATE.md) — Gate definition
