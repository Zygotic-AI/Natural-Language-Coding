# A-C4

- [Requirement](../../docs/TERMS.md#requirement): `C4`
- Outcome: **[met](../../docs/TERMS.md#met)** | **not [met](../../docs/TERMS.md#met)** only
- Binder: `tools/fitness-no-noun-field-writes.py`

## Statement

No assignment to [noun](../../docs/TERMS.md#noun) fields occurs outside the [noun](../../docs/TERMS.md#noun) module.

## Binary criteria

[Met](../../docs/TERMS.md#met) iff `tools/fitness-no-noun-field-writes.py` exits 0 on the scanned tree(s) (`RESULT:MET`).

Not [met](../../docs/TERMS.md#met) iff the tool prints one or more `VIOLATION` lines and exits 1 (`RESULT:NOT_MET`).

This checklist item is exactly the assignment surface check 1 enforces.

## Evidence

Cite each `VIOLATION <path>:<line> <field>` line, or `RESULT:MET` with the scan roots used.

## Fixtures

- `examples/invoice-violation/` is expected **not [met](../../docs/TERMS.md#met)** when scanned alone.
- [Adopter](../../docs/TERMS.md#adopter) / correct trees must be **[met](../../docs/TERMS.md#met)**.
