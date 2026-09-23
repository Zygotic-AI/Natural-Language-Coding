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

Covered modules:

- `tools/nlc-init.py`
- `tools/nlc_distribution.py`
- `tools/nlc_requirements.py`

Enforced by `tools/fitness-hub-bba-interior-slice.py`. A missing or renamed marker fails the gate (default-closed).

Full noun/verb package rewrite of `tools/*.py` interiors remains future work.

## Hub self-verify (A12 soft-green)

This hub **is** the first subject of `./nlc verify` / CI `fitness-*` (not an afterthought adopter-only suite). Concrete door permanence:

- `tools/fitness-charter-nlc-door.py` — CHARTER first H1 must name the NLC roof
- `tools/fitness-hub-bba-dogfood.py` / `fitness-hub-bba-interior-slice.py` — emit-path dogfood
- Binding matrix + install hashes run on this checkout

Still expansion (not claimed closed): full hub `tools/*.py` noun/verb rewrite; RCA packet schema binder for ADR 0025.

