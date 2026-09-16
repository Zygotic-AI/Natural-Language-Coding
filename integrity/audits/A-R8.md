# A-R8

- Requirement: `R8`
- Outcome: **met** | **not met** only
- Gate: `tools/fitness-no-noun-field-writes.py`

## Statement

Goals may read what the noun chooses to expose (queries / snapshots). Goals may not reach through that snapshot and write.

## V1 bind

Same scanner as R5/C4. `snap.status =` and `snap['status'] =` are field writes if `status` is declared on the noun.

Hole: `snap.update({...})` and copies that never assign a declared field name. That is still R8 in spirit and not this v1.
