# A-C3

- [Requirement](../../docs/TERMS.md#requirement): `C3`
- Outcome: **[met](../../docs/TERMS.md#met)** | **not [met](../../docs/TERMS.md#met)** only
- [Gate](../../docs/TERMS.md#gate): `tools/fitness-c3.py`

## Statement

New orchestration lives in a [goal](../../docs/TERMS.md#goal), not as a method on an unrelated [noun](../../docs/TERMS.md#noun).

## V1 bind

If `domain/<other>/*.py` calls `.verb(` owned by a different [noun](../../docs/TERMS.md#noun), fail.

One [noun](../../docs/TERMS.md#noun) in the tree → skip (MET). Does not judge "related."

Designed fail: `examples/orchestration-on-noun/`.
Designed pass: `examples/invoice-correct/`.
