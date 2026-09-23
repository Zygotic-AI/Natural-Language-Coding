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

