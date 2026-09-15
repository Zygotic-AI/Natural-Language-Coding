# A-R6

- Requirement: `R6`
- Outcome: **met** | **not met** only
- Gate: `tools/fitness-verb-path.py`

## Statement

The only legal mutation of a noun is a public verb on that noun.

## V1 bind

Fails persistence escapes in `goals/` / `adapters/` / `workflows/`:
`.save(`, `.update(`, `.execute(`, `UPDATE`, `INSERT INTO`, `DELETE FROM`, `setattr(`.

Does **not** replace R5 (field assignment). Direct `invoice.status =` is R5.

Designed fail: `examples/invoice-verb-path-violation/`.
Designed pass: `examples/invoice-correct/`.

Surface stays `reference`. V1 is SQL/ORM/setattr, not "every possible mutation".
