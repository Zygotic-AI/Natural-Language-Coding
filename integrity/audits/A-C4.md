# A-C4

- Requirement: `C4`
- Outcome: **met** | **not met** only
- Binder: `tools/fitness-no-noun-field-writes.py`

## Statement

No assignment to noun fields occurs outside the noun module.

## Binary criteria

Met iff `tools/fitness-no-noun-field-writes.py` exits 0 on the scanned tree(s) (`RESULT:MET`).

Not met iff the tool prints one or more `VIOLATION` lines and exits 1 (`RESULT:NOT_MET`).

This checklist item is exactly the assignment surface check 1 enforces.

## Evidence

Cite each `VIOLATION <path>:<line> <field>` line, or `RESULT:MET` with the scan roots used.

## Fixtures

- `examples/invoice-violation/` is expected **not met** when scanned alone.
- Adopter / correct trees must be **met**.
