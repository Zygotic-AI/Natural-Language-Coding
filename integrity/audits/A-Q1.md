# Audit A-Q1 — Quality evidence required at fitness

Requirement: Q1

## Criterion

Every produce package submitted to fitness preflight must include quality evidence from prior gate executions in the produce cycle.

## Met when

- Produce package contains at least one gate receipt
- Gate receipt has valid `outcome` field (PASS, FAIL, MET, or REFUSE)
- Gate receipt has valid `timestamp` field (ISO 8601)

## Not met when

- Produce package missing quality evidence entirely
- Gate receipt present but `outcome` field missing or invalid
- Gate receipt present but `timestamp` field missing or invalid

## Evidence

- Path to gate receipt in produce package
- Contents of `outcome` and `timestamp` fields

## Failure mode

Fitness preflight returns `handoff_refused` with `QUALITY_EVIDENCE` in the `missing` enum. Fitness scoring returns error `QUALITY_EVIDENCE_MISSING`.

## Cross-references

- [`../QUALITY_METRIC.md`](../QUALITY_METRIC.md) — Quality Metric SSOT
- [`../agents/quality-architect/verbs.md`](../../agents/quality-architect/verbs.md) — Fitness verbs
