# [Audit](../../docs/TERMS.md#audit) A-CS9 — [Quality evidence](../../docs/TERMS.md#quality-evidence) present in [produce package](../../docs/TERMS.md#produce-package)

[Requirement](../../docs/TERMS.md#requirement): CS9 (Confirmation checklist — systems)

## Criterion

[Quality evidence](../../docs/TERMS.md#quality-evidence) present in [produce package](../../docs/TERMS.md#produce-package) (gate receipts with outcome + timestamp).

## [Met](../../docs/TERMS.md#met) when

- [Produce package](../../docs/TERMS.md#produce-package) contains `quality_evidence` field or equivalent
- At least one [gate](../../docs/TERMS.md#gate) receipt present with:
  - `gate_id` (string, non-empty)
  - `outcome` (PASS, FAIL, MET, or REFUSE)
  - `timestamp` (ISO 8601 format)

## Not [met](../../docs/TERMS.md#met) when

- `quality_evidence` missing from [produce package](../../docs/TERMS.md#produce-package)
- [Gate](../../docs/TERMS.md#gate) receipts array empty
- Any [gate](../../docs/TERMS.md#gate) receipt missing required fields (`gate_id`, `outcome`, `timestamp`)
- `outcome` value not in allowed enum
- `timestamp` not valid ISO 8601

## Evidence

- Path to [produce package](../../docs/TERMS.md#produce-package)
- Contents of `quality_evidence` field
- List of [gate](../../docs/TERMS.md#gate) receipts with their fields

## Cross-references

- [`../QUALITY_METRIC.md`](../QUALITY_METRIC.md) Q1 — [Quality evidence](../../docs/TERMS.md#quality-evidence) required at fitness
- [Charter](../../docs/TERMS.md#charter) §16.9 CS9
