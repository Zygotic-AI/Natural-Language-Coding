# A-R5

- Requirement: `R5`
- Outcome: **met** | **not met** only
- Binder: `tools/fitness-no-noun-field-writes.py`

## Statement

Noun fields are private. No goal, workflow, adapter, or other noun writes them.

## Binary criteria

Met iff `tools/fitness-no-noun-field-writes.py` exits 0 on the scanned tree(s) (`RESULT:MET`).

Not met iff the tool prints one or more `VIOLATION` lines and exits 1 (`RESULT:NOT_MET`).

Scope of this binder: **field assignments** from outside the noun module (`goals/`, `workflows/`, `adapters/`). It does not prove every mutation goes through a public verb (see R6 / C5).

## Evidence

Cite each `VIOLATION <path>:<line> <field>` line, or `RESULT:MET` with the scan roots used.

## Fixtures

- `examples/invoice-violation/` is expected **not met** when scanned alone (deliberate outside writes).
- Adopter / correct trees must be **met**.
