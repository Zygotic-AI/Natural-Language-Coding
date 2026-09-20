# A-R9

- [Requirement](../../docs/TERMS.md#requirement): `R9`
- Outcome: **[met](../../docs/TERMS.md#met)** | **not [met](../../docs/TERMS.md#met)** only
- [Gate](../../docs/TERMS.md#gate): `tools/fitness-contract-presence.py`

## Statement

Every public [goal](../../docs/TERMS.md#goal) entrypoint has an input [contract](../../docs/TERMS.md#contract) and an output [contract](../../docs/TERMS.md#contract).

## V1 bind

A `goals/<id>/` directory that contains code must also contain `input.schema.json` and `output.schema.json` that parse as JSON objects.

Presence is not semantic completeness. Empty `{"type":"object"}` still [MET](../../docs/TERMS.md#met).

Designed fail: `examples/missing-contract/`.
Designed pass: `examples/invoice-correct/`.

C7 stays unbound: it is "each *changed* [goal](../../docs/TERMS.md#goal)" (diff-scoped).
