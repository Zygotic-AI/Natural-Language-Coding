# A-R6

- [Requirement](../../docs/TERMS.md#requirement): `R6`
- Outcome: **[met](../../docs/TERMS.md#met)** | **not [met](../../docs/TERMS.md#met)** only
- [Gate](../../docs/TERMS.md#gate): `tools/fitness-verb-path.py`

## Statement

The only legal mutation of a [noun](../../docs/TERMS.md#noun) is a public verb on that [noun](../../docs/TERMS.md#noun).

## V1 bind

Fails persistence escapes in `goals/` / `adapters/` / `workflows/`:
`.save(`, `.update(`, `.execute(`, `UPDATE`, `INSERT INTO`, `DELETE FROM`, `setattr(`.

Does **not** replace R5 (field assignment). Direct `invoice.status =` is R5.

Designed fail: `examples/invoice-verb-path-violation/`.
Designed pass: `examples/invoice-correct/`.

Surface stays `reference`. V1 is SQL/ORM/setattr, not "every possible mutation".
