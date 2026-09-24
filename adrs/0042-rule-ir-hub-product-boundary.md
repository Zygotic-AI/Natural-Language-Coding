# ADR 0042 — Rule IR hub product boundary (ADR 0007)

- Status: Accepted
- Date: 2026-09-23
- Deciders: Human manager
- Class: F (product)
- Corpus: nlc

## Context

[ADR 0007](0007-tags-primitives-reduced-adrs.md) requires if/then rules over tags and primitives. [`FINDINGS.md`](../FINDINGS.md) parked **Rule IR** as `gate missing` for “full semantic runners.” Hub already ships **snapshot materialize + check** (`nlc_rule_runner.py`, `RuleReceipt.check_ir`). [`integrity/product-completion-scope.json`](../integrity/product-completion-scope.json) wave **P2** must not confuse v1 product with unbounded semantic expansion.

## Decision

1. **Hub v0.2.x product-closed (UC4/UC5 v1):** adopted rules → `.nlc/rule-ir.snapshot.json` matches live materialization; each rule has valid `match` + `must` obligation shape. Proof:
   - `python3 tools/nlc_rule_runner.py --check --root <app>`
   - `python3 tools/assert-rule-runner-fails.py` (missing snapshot)
   - `python3 tools/assert-rule-runner-passes.py` (green fixture)

2. **Remain expansion (not claimed closed):**
   - **Semantic runner** — evaluate rule bodies against live code beyond IR shape (`UC4.semantic_rule_runner_adr_0007`).
   - **Semantic apply** — compiler applies obligations automatically (`UC5.semantic_apply_adr_0007`).
   - **UC14 composable IR** — cross-primitive policy and conflict resolution (`UC14.composable_ir_cross_primitive`).

3. **SSOT:** [`integrity/rule-ir-product-boundary.json`](../integrity/rule-ir-product-boundary.json) lists proof commands and expansion keys. `tools/fitness-adr-0007-product-boundary.py` binds the split.

## Consequences

- FINDINGS Parked **Rule IR** row documents v1 **done** + semantic **expansion** (not `gate missing` for snapshot path).
- Further semantic work requires ADR amendment and clearing `expansion_only` in `uc-product-status.json`.

## Rejected

- Marking “full semantic runners” done without proof commands.
- Removing designed-fail landmines for missing snapshot.
