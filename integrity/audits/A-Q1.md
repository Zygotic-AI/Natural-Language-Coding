# [Audit](../../docs/TERMS.md#audit) A-Q1 — [Quality evidence](../../docs/TERMS.md#quality-evidence) required at fitness

[Requirement](../../docs/TERMS.md#requirement): Q1

## Criterion

Every [produce package](../../docs/TERMS.md#produce-package) submitted to fitness preflight must include [quality evidence](../../docs/TERMS.md#quality-evidence) from prior [gate](../../docs/TERMS.md#gate) executions in the produce cycle.

## [Met](../../docs/TERMS.md#met) when

- [Produce package](../../docs/TERMS.md#produce-package) contains at least one [gate](../../docs/TERMS.md#gate) receipt
- [Gate](../../docs/TERMS.md#gate) receipt has valid `outcome` field (PASS, FAIL, MET, or REFUSE)
- [Gate](../../docs/TERMS.md#gate) receipt has valid `timestamp` field (ISO 8601)

## Not [met](../../docs/TERMS.md#met) when

- [Produce package](../../docs/TERMS.md#produce-package) missing [quality evidence](../../docs/TERMS.md#quality-evidence) entirely
- [Gate](../../docs/TERMS.md#gate) receipt present but `outcome` field missing or invalid
- [Gate](../../docs/TERMS.md#gate) receipt present but `timestamp` field missing or invalid

## Evidence

- Path to [gate](../../docs/TERMS.md#gate) receipt in [produce package](../../docs/TERMS.md#produce-package)
- Contents of `outcome` and `timestamp` fields

## Failure mode

Fitness preflight returns `handoff_refused` with `QUALITY_EVIDENCE` in the `missing` enum. Fitness scoring returns error `QUALITY_EVIDENCE_MISSING`.

## Cross-references

- [`../QUALITY_METRIC.md`](../QUALITY_METRIC.md) — [Quality](../../docs/TERMS.md#quality) Metric SSOT
- [`../agents/quality-architect/verbs.md`](../../agents/quality-architect/verbs.md) — Fitness verbs
