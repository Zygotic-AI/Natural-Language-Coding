# A-R4

- Requirement: `R4`
- Outcome: **met** | **not met** only
- Gate: `tools/fitness-r4.py`

## Statement

If a verb does not need the noun's adjective set, it does not belong on the noun.

## Bind

Public methods must **read or write** `self.<token>` / `this.<token>` or
`getattr`/`setattr(self, "<token>")` for a name in `fields.txt` or
`adjectives.txt`. A string that contains the word is not use.

No lists → skip.

Out of reach: a verb that *does* touch state but still shouldn't live on
this noun (wrong bounded context). That is a design judgment, not this gate.

Designed fail: `examples/stray-verb/`, `examples/mention-only-verb/`.
Designed pass: `examples/invoice-correct/`.
