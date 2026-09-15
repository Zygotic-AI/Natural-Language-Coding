# A-R9

- Requirement: `R9`
- Outcome: **met** | **not met** only

## Statement

Every public goal entrypoint has an input contract and an output contract.

## V1 tool (not a matrix bind)

`tools/fitness-contract-presence.py` — `goals/<id>/` with code must have
`input.schema.json` and `output.schema.json` that parse as JSON objects.

Known-fail: `examples/missing-contract/`.
Known-pass: `examples/invoice-correct/`.

Presence of a file is not a complete contract. R9 stays unbound.
