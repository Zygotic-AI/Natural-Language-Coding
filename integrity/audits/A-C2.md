# A-C2

- [Requirement](../../docs/TERMS.md#requirement): `C2`
- Outcome: **[met](../../docs/TERMS.md#met)** | **not [met](../../docs/TERMS.md#met)** only
- [Gate](../../docs/TERMS.md#gate): `tools/fitness-c2.py`

## Statement

Adjectives live on the [noun](../../docs/TERMS.md#noun) named in C1, not in a [goal](../../docs/TERMS.md#goal) folder.

## V1 bind

`adjectives.txt` and `fields.txt` must not appear under `goals/`.

Does not parse the [noun](../../docs/TERMS.md#noun) named in C1.

Designed fail: `examples/adjectives-in-goal/`.
Designed pass: `examples/invoice-correct/`.
