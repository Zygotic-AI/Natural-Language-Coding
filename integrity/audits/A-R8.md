# A-R8

- [Requirement](../../docs/TERMS.md#requirement): `R8`
- Outcome: **[met](../../docs/TERMS.md#met)** | **not [met](../../docs/TERMS.md#met)** only
- [Gate](../../docs/TERMS.md#gate): `tools/fitness-no-noun-field-writes.py`

## Statement

Goals may read what the [noun](../../docs/TERMS.md#noun) chooses to expose (queries / snapshots). Goals may not reach through that snapshot and write.

## V1 bind

Same scanner as R5/C4. `snap.status =` and `snap['status'] =` are field writes if `status` is declared on the [noun](../../docs/TERMS.md#noun).

Hole: `snap.update({...})` and copies that never assign a declared field name. That is still R8 in spirit and not this v1.
