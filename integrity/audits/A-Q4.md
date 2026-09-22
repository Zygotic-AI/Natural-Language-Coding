# [Audit](../../docs/TERMS.md#audit) A-Q4 — [Defect](../../docs/TERMS.md#defect) classification is binary

[Requirement](../../docs/TERMS.md#requirement): Q4

## Criterion

Every [opportunity](../../docs/TERMS.md#opportunity) outcome is classified as exactly one of: [op](../../docs/TERMS.md#op) or [defect](../../docs/TERMS.md#defect). No partial, provisional, or weighted outcomes.

## [Met](../../docs/TERMS.md#met) when

- Every recorded outcome in scope maps to exactly `op` or `defect`
- No outcome is classified as partial, weighted, provisional, or pending
- No outcome has multiple classifications

## Not [met](../../docs/TERMS.md#met) when

- Any outcome is classified as partial, provisional, or weighted
- Any outcome has no classification
- Any outcome has multiple classifications (op AND defect)
- Continuous scores used instead of binary classification

## Evidence

- List of outcomes in scope with their classifications
- Confirmation that each outcome is exactly one of {[op](../../docs/TERMS.md#op), [defect](../../docs/TERMS.md#defect)}

## Failure mode

[Quality](../../docs/TERMS.md#quality) metric computation refuses; evidence rejected as non-binary.

## Cross-references

- [`../QUALITY_METRIC.md`](../QUALITY_METRIC.md) — [Quality](../../docs/TERMS.md#quality) Metric SSOT (defect classification table)
- [`../GATE.md`](../GATE.md) — [Gate](../../docs/TERMS.md#gate) outcomes (PASS/FAIL/REFUSE)
