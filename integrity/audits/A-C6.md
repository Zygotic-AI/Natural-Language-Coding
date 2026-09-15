# A-C6

- Requirement: `C6`
- Outcome: **met** | **not met** only
- Gate: `tools/fitness-noun-imports.py`

## Statement

No noun module imports a goal module.

## Binary criteria

Met iff `tools/fitness-noun-imports.py` exits 0 with `RESULT:MET`. Not met if the gate fails, did not run, or evidence is missing.

## Evidence

On met or not met, cite file and symbol (or N/A reason). List failing ids when the audit is a matrix audit.
