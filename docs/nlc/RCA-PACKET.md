# RCA packet (ADR 0025)

Machine-checkable record for a certified [RCA](../TERMS.md#rca) that names an **unsuitable process**, not an agent or human as the cause ([ADR 0025](../../adrs/0025-belief-no-blame-climb.md)).

## Shape

- Schema: [`integrity/schemas/rca-packet.schema.json`](../../integrity/schemas/rca-packet.schema.json)
- Validator: `python3 tools/validate-rca-packet.py <path-to-rca-packet.json>`
- Ok specimen: [`examples/rca-packet-ok/rca-packet.json`](../../examples/rca-packet-ok/rca-packet.json)

## Gate

Default-closed. `RCA_PACKET:MET` only when schema, climb steps, and `repo_touch` (belief / ADR / rule / gate citation) pass.
