# Hub BBA dogfood (X4)

Hub *process* is NLC. Hub *emit* — when this repo writes a compiled-system tree — is BBA.

v1 bound on `nlc-init` + adopter template:

- `tools/nlc-init.py` creates `nouns/` and `goals/` with READMEs
- `templates/adopter/nouns/` and `templates/adopter/goals/` exist
- `tools/fitness-hub-bba-dogfood.py` refuses if those homes disappear

Not this pass: rewriting hub `tools/*.py` interiors into noun/verb packages.

## v2 — emit-path boundary markers

The hub's own emit-path modules declare their BBA role at module scope (after `from __future__`):

```python
BOUNDARY = "bba-emit"
```

Covered modules (tranche-1 emit-path):

- `tools/nlc-init.py`
- `tools/nlc_distribution.py`
- `tools/nlc_requirements.py`
- `tools/nlc-pack-install.py`
- `tools/nlc-pack-export.py`
- `tools/nlc-pack-ingest.py`
- `tools/nlc-pipeline-wire.py`
- `tools/nlc-before-generate.py`
- `tools/nlc-emit-from-prose.py`
- `tools/nlc_goal_scaffold.py`
- `tools/nlc_rule_emit.py`

Enforced by `tools/fitness-hub-bba-interior-slice.py`. A missing or renamed marker fails the gate (default-closed).

Remainder inventory: [`integrity/hub-x4-remainder.json`](../integrity/hub-x4-remainder.json) (emit-path-open + assert-only counts). Full noun/verb package rewrite of `tools/*.py` interiors remains parked.

## Hub self-verify (A12 soft-green)

This hub **is** the first subject of `./nlc verify` / CI `fitness-*` (not an afterthought adopter-only suite). Concrete door permanence:

- `tools/fitness-charter-nlc-door.py` — CHARTER first H1 must name the NLC roof
- `tools/fitness-hub-bba-dogfood.py` / `fitness-hub-bba-interior-slice.py` — emit-path dogfood
- Binding matrix + install hashes run on this checkout

Still expansion (not claimed closed): full hub `tools/*.py` noun/verb rewrite; RCA packet schema binder for ADR 0025.

## v3 — noun/verb pilot (`RuleReceipt`)

First true interior rewrite (not BOUNDARY-only): ADR 0023 rule family lives as a BBA noun under `tools/nouns/rule_receipt/`.

- Noun: `RuleReceipt` (`format_marker`, `apply_markers_to_source`, `load_adopted`, `scan_markers`, `materialize_ir`, `write_snapshot`, `check_ir`)
- Thin CLI adapters: `nlc_rule_marker.py`, `nlc_rule_coverage.py`, `nlc_rule_runner.py`, `nlc_rule_emit.py`
- Gate: `tools/fitness-hub-x4-noun-pilot.py`

Full rewrite of remaining `tools/*.py` stays open — see [`integrity/hub-x4-remainder.json`](../integrity/hub-x4-remainder.json).

### GateLedger (second pilot)

- Noun: `tools/nouns/gate_ledger/` (`GateLedger`: scope paths + gate receipts)
- Thin CLI adapters: `nlc_gate_scope.py`, `nlc_gate_record.py`
- Same gate: `tools/fitness-hub-x4-noun-pilot.py` (multi-pilot)

## v4 — emit-path noun completion

All former `emit_path_open` hub `nlc*` writers are noun packages under `tools/nouns/` with thin CLI adapters. Enforced by `tools/fitness-hub-x4-noun-pilot.py` + `integrity/hub-x4-remainder.json` (`emit_path_complete`).

Still residual (not claimed closed): mass rewrite of assert/fitness-only `tools/*.py` into nouns.

## v5 — tranche `x4-t1-other-or-lib` (lib slice)

First `other-or-lib` conversions (shared libs, not CLI): `markdown_plain`, `changeset` under `tools/nouns/` with thin `tools/*.py` adapters.

- Progress SSOT: [`integrity/hub-x4-tranche-plan.json`](../integrity/hub-x4-tranche-plan.json) (`tranche_1_progress`)
- Gates: `fitness-hub-x4-tranche-t1.py`, `fitness-hub-x4-noun-pilot.py` (inventory + pilot shape)

## v6 — tranche `x4-t2-assert-batch-a` (assert slice)

First **70** `assert_only` landmines are noun packages under `tools/nouns/assert_*` with thin `tools/assert-*.py` adapters.

- Progress SSOT: [`integrity/hub-x4-tranche-plan.json`](../integrity/hub-x4-tranche-plan.json) (`tranche_2_progress`)
- Gates: `fitness-hub-x4-tranche-t2.py`, `fitness-hub-x4-noun-pilot.py`

## v7 — tranche `x4-t3-assert-batch-b` (assert completion)

All **209** `assert_only` landmines are noun-backed (`assert_tranche_complete` in remainder inventory).

- Progress SSOT: [`integrity/hub-x4-tranche-plan.json`](../integrity/hub-x4-tranche-plan.json) (`tranche_3_progress`)
- Gates: `fitness-hub-x4-tranche-t3.py`, `fitness-hub-x4-noun-pilot.py`
- Honest residual: `fitness-*.py` tool interiors not in the assert inventory bucket (see FINDINGS X4 row).

## v8 — tranche `x4-t4-fitness-complete` (fitness slice)

All hub `fitness-*.py` tools are noun packages under `tools/nouns/fitness_*` with thin adapters (`hub-x4-migrate-fitness-noun.py` + `hub-x4-refresh-inventory.py`).

- Progress SSOT: [`integrity/hub-x4-tranche-plan.json`](../integrity/hub-x4-tranche-plan.json) (`tranche_4_progress`)
- Gates: `fitness-hub-x4-tranche-t4.py`, `fitness-hub-x4-noun-pilot.py`
- Inventory: `fitness_only` **0**, `fitness_tranche_complete` in [`integrity/hub-x4-remainder.json`](../integrity/hub-x4-remainder.json)

