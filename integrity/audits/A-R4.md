# A-R4

- [Requirement](../../docs/TERMS.md#requirement): `R4`
- Outcome: **[met](../../docs/TERMS.md#met)** | **not [met](../../docs/TERMS.md#met)** only
- [Gate](../../docs/TERMS.md#gate): `tools/fitness-r4.py`

## Statement

If a verb does not need the [noun](../../docs/TERMS.md#noun)'s [adjective](../../docs/TERMS.md#adjective) set, it does not belong on the [noun](../../docs/TERMS.md#noun).

## Bind

Public methods must **read or write** `self.<token>` / `this.<token>` or
`getattr`/`setattr(self, "<token>")` for a name in `fields.txt` or
`adjectives.txt`. A string that contains the word is not use.

No lists → skip.

Out of reach: a verb that *does* touch state but still shouldn't live on
this [noun](../../docs/TERMS.md#noun) (wrong bounded context). That is a design judgment, not this [gate](../../docs/TERMS.md#gate).

Designed fail: `examples/stray-verb/`, `examples/mention-only-verb/`.
Designed pass: `examples/invoice-correct/`.
