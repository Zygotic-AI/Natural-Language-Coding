# Releasable gate-list duplicate (landmine fixture)

RCA-1 landmine **(a)**: `assert-releasable-gate-list-duplicate-fails.py` drops a temporary
second `profiles.verify` + `profiles.release` JSON here and expects
`fitness-releasable-gate-ssot.py` to refuse it. Do not commit `shadow-profiles.json`.
