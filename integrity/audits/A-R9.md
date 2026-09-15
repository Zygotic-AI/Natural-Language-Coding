# A-R9

- Requirement: `R9`
- Outcome: **met** | **not met** only
- Gate: `tools/fitness-contract-presence.py`

## Statement

Every public goal entrypoint has an input contract and an output contract.

## V1 bind

A `goals/<id>/` directory that contains code must also contain `input.schema.json` and `output.schema.json` that parse as JSON objects.

Presence is not semantic completeness. Empty `{"type":"object"}` still MET.

Designed fail: `examples/missing-contract/`.
Designed pass: `examples/invoice-correct/`.

C7 stays unbound: it is "each *changed* goal" (diff-scoped).
