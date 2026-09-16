# A-C2

- Requirement: `C2`
- Outcome: **met** | **not met** only
- Gate: `tools/fitness-c2.py`

## Statement

Adjectives live on the noun named in C1, not in a goal folder.

## V1 bind

`adjectives.txt` and `fields.txt` must not appear under `goals/`.

Does not parse the noun named in C1.

Designed fail: `examples/adjectives-in-goal/`.
Designed pass: `examples/invoice-correct/`.
