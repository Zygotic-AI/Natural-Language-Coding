# A-R4

- Requirement: `R4`
- Outcome: **met** | **not met** only
- Gate: `tools/fitness-r4.py`

## Statement

If a verb does not need the noun's adjective set, it does not belong on the noun.

## V1 bind

Public methods (not `__init__` / `_private`) must mention a token from
`fields.txt` or `adjectives.txt`.

No field/adjective lists → skip (MET). Token presence, not that the verb *needs* the adjective.

Designed fail: `examples/stray-verb/`.
Designed pass: `examples/invoice-correct/`.
