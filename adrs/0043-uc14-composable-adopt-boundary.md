# ADR 0043 — UC14 composable rules product boundary (ADR 0012)

- Status: Accepted
- Date: 2026-09-23
- Deciders: Human manager
- Class: F (product)
- Corpus: nlc

## Context

[ADR 0012](0012-rule-adoption-conflicts.md) requires adopt-time detection of conflicting rules. Product completion wave **P2.2** tracked `composable_ir_cross_primitive` as expansion. Hub already ships `check-rule-adoption.py` with precedence tiers and overrides.

## Decision

1. **UC14 v1 product-closed:** adopt-time **conflict + precedence** resolution for adopted rules (`ADOPTION:MET`). Proof:
   - `python3 tools/check-rule-adoption.py <rules/adopted.json>`
   - `python3 tools/assert-rule-adoption-conflicts-fails.py`
   - `python3 tools/assert-rule-adoption-passes.py`

2. **Remain expansion:** cross-primitive **composable IR** (obligations spanning multiple primitives with shared policy graph) — not claimed until ADR amendment + `UC14.expansion_only` re-opened intentionally.

3. **SSOT:** [`integrity/uc14-product-boundary.json`](../integrity/uc14-product-boundary.json); binder `tools/fitness-uc14-product-boundary.py`.

## Consequences

- `integrity/uc-product-status.json` clears `UC14.expansion_only` for v1.
- FINDINGS Parked UC14 narrative updated.

## Rejected

- Marking full composable IR done when only adopt-time conflict check exists.
