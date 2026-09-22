# A-R5

- [Requirement](../../docs/TERMS.md#requirement): `R5`
- Outcome: **[met](../../docs/TERMS.md#met)** | **not [met](../../docs/TERMS.md#met)** only
- [Gate](../../docs/TERMS.md#gate): `tools/fitness-no-noun-field-writes.py`

## Statement

[Noun](../../docs/TERMS.md#noun) fields are private. No [goal](../../docs/TERMS.md#goal), adapter, or other [noun](../../docs/TERMS.md#noun) writes them.

## Binary criteria

[Met](../../docs/TERMS.md#met) iff `tools/fitness-no-noun-field-writes.py` exits 0 on the scanned tree(s) (`RESULT:MET`).

Not [met](../../docs/TERMS.md#met) iff the tool prints one or more `VIOLATION` lines and exits 1 (`RESULT:NOT_MET`).

Scope of this [gate](../../docs/TERMS.md#gate): **field assignments** from outside the [noun](../../docs/TERMS.md#noun) module (`goals/`, `adapters/`, and optional `workflows/` packaging for durable goals). It does not [prove](../../docs/TERMS.md#prove) every mutation goes through a public verb (see R6 / C5).

## Evidence

Cite each `VIOLATION <path>:<line> <field>` line, or `RESULT:MET` with the scan roots used.

## Fixtures

- `examples/invoice-violation/` is expected **not [met](../../docs/TERMS.md#met)** when scanned alone (deliberate outside writes).
- [Adopter](../../docs/TERMS.md#adopter) / correct trees must be **[met](../../docs/TERMS.md#met)**.
