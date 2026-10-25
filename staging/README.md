# Staging (gate machinery candidates)

Candidate bytes for self-referential gate machinery live under `staging/<change-id>/`, mirroring live paths. This prefix is excluded from gate-set membership.

Do not load a staged `SKILL.md` as `/planit`. The live signed machinery verifies the candidate and the owner's signature. `python3 tools/activate-gate-machinery.py` is the only swap onto live paths.
