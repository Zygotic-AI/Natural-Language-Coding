# Primitive set (SSOT)

Closed list of **interior function names**. Not public verbs. Not an AI vocabulary.

**New primitive = ADR**, then a row here. Prefer a new tag or fact before a new primitive ([ADR 0007](../adrs/0007-tags-primitives-reduced-adrs.md)).

Normative use: [ADR 0009](../adrs/0009-primitive-interior-functions.md).

## v1 names

| Name | Meaning |
|------|---------|
| `read` | Load from a store or neighbor via contract |
| `write` | Persist or mutate durable state (`store` in 0007 examples means this) |
| `return` | Hand a value out of this verb |
| `log` | Emit a record |
| `display` | Present to a human |
| `transmit` | Send across a process/network boundary |
| `copy` | Duplicate a value |
| `retain` | Keep after the verb returns (memory, cache, field) |
| `retry` | Repeat a call |
| `wait` | Yield for time, signal, or human |
| `ship` | Authorize release |

Do not add names here in a generate pass. Do not invent `process`, `handle`, or `save` as a primitive.

## Reserved

These names are **not** legal public verb names on a noun. They live under an interior module (e.g. `primitives/write.py` or `_write`). A public `Invoice.write` is a defect.
