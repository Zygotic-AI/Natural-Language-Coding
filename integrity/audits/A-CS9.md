# Audit A-CS9 — Quality evidence present in produce package

Requirement: CS9 (Confirmation checklist — systems)

## Criterion

Quality evidence present in produce package (gate receipts with outcome + timestamp).

## Met when

- Produce package contains `quality_evidence` field or equivalent
- At least one gate receipt present with:
  - `gate_id` (string, non-empty)
  - `outcome` (PASS, FAIL, MET, or REFUSE)
  - `timestamp` (ISO 8601 format)

## Not met when

- `quality_evidence` missing from produce package
- Gate receipts array empty
- Any gate receipt missing required fields (`gate_id`, `outcome`, `timestamp`)
- `outcome` value not in allowed enum
- `timestamp` not valid ISO 8601

## Evidence

- Path to produce package
- Contents of `quality_evidence` field
- List of gate receipts with their fields

## Cross-references

- [`../QUALITY_METRIC.md`](../QUALITY_METRIC.md) Q1 — Quality evidence required at fitness
- Charter §16.9 CS9
