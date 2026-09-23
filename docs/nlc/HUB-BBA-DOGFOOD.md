# Hub BBA dogfood (X4)

Hub *process* is NLC. Hub *emit* — when this repo writes a compiled-system tree — is BBA.

v1 bound on `nlc-init` + adopter template:

- `tools/nlc-init.py` creates `nouns/` and `goals/` with READMEs
- `templates/adopter/nouns/` and `templates/adopter/goals/` exist
- `tools/fitness-hub-bba-dogfood.py` refuses if those homes disappear

Not this pass: rewriting hub `tools/*.py` interiors into noun/verb packages.
