# Hub BBA dogfood (X4)

Hub *process* is NLC. Hub *emit* — when this repo writes a compiled-system tree — is BBA.

## v1 — emit homes (bound)

- `tools/nlc-init.py` creates `nouns/` and `goals/` with READMEs
- `templates/adopter/nouns/` and `templates/adopter/goals/` exist
- `tools/fitness-hub-bba-dogfood.py` refuses if those homes disappear

## v2 — emit-path boundary markers (this slice)

The hub's own emit-path modules declare their BBA role at module scope:

```python
BOUNDARY = "bba-emit"
```

Covered modules:

- `tools/nlc-init.py`
- `tools/nlc_distribution.py`
- `tools/nlc_requirements.py`

Enforced by `tools/fitness-hub-bba-interior-slice.py`. A missing or renamed
marker fails the gate (default closed).

## Not this pass

Rewriting hub `tools/*.py` interiors into noun/verb packages with contracts.
That is a separate, larger effort — each tool becomes a noun with verbs, not
just a marked script.
