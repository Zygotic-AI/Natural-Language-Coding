# Audit A-CS10 — Quality snapshot recorded at boundary exit

Requirement: CS10 (Confirmation checklist — systems)

## Criterion

Quality snapshot recorded at boundary exit (`{ opportunities, ops, defects, quality }`).

## Met when

Completion artifact includes `quality_snapshot` with all four fields:

- `opportunities` (integer ≥ 0)
- `ops` (integer ≥ 0)
- `defects` (integer ≥ 0)
- `quality` (number 0.0 – 1.0)

AND consistency holds:
- `ops + defects = opportunities`
- `quality ≈ ops / opportunities` (within floating-point tolerance)

## Not met when

- `quality_snapshot` missing from completion artifact
- Any of the four required fields missing
- Field values inconsistent (`ops + defects ≠ opportunities`)
- `quality` not within tolerance of `ops / opportunities`
- `opportunities` is 0 but `quality` is not 0 or undefined

## Evidence

- Path to completion artifact
- Contents of `quality_snapshot` object
- Consistency check results

## Cross-references

- [`../QUALITY_METRIC.md`](../QUALITY_METRIC.md) Q3 — Quality snapshot recorded at boundary exit
- Charter §16.9 CS10
