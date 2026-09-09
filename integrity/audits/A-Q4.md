# Audit A-Q4 — Defect classification is binary

Requirement: Q4

## Criterion

Every opportunity outcome is classified as exactly one of: op or defect. No partial, provisional, or weighted outcomes.

## Met when

- Every recorded outcome in scope maps to exactly `op` or `defect`
- No outcome is classified as partial, weighted, provisional, or pending
- No outcome has multiple classifications

## Not met when

- Any outcome is classified as partial, provisional, or weighted
- Any outcome has no classification
- Any outcome has multiple classifications (op AND defect)
- Continuous scores used instead of binary classification

## Evidence

- List of outcomes in scope with their classifications
- Confirmation that each outcome is exactly one of {op, defect}

## Failure mode

Quality metric computation refuses; evidence rejected as non-binary.

## Cross-references

- [`../QUALITY_METRIC.md`](../QUALITY_METRIC.md) — Quality Metric SSOT (defect classification table)
- [`../GATE.md`](../GATE.md) — Gate outcomes (PASS/FAIL/REFUSE)
