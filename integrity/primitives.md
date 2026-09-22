# [Primitive](../docs/TERMS.md#primitive) set (SSOT)

Closed list of **interior function names**. Not public verbs. Not an AI vocabulary.

**New [primitive](../docs/TERMS.md#primitive) = [ADR](../docs/TERMS.md#adr)**, then a row here. Prefer a new [tag](../docs/TERMS.md#tag) or fact before a new [primitive](../docs/TERMS.md#primitive) ([ADR 0007](../adrs/0007-tags-primitives-reduced-adrs.md)).

Normative use: [ADR 0009](../adrs/0009-primitive-interior-functions.md).

## v1 names

| Name | Meaning |
|------|---------|
| `read` | Load from a store or neighbor via [contract](../docs/TERMS.md#contract) |
| `write` | Persist or mutate durable state (`store` in 0007 examples means this) |
| `return` | Hand a value out of this verb |
| `log` | Emit a record |
| `display` | Present to a human |
| `transmit` | Send across a process/network [boundary](../docs/TERMS.md#boundary) |
| `copy` | Duplicate a value |
| `retain` | Keep after the verb returns (memory, cache, field) |
| `retry` | Repeat a call |
| `wait` | Yield for time, signal, or human |
| `ship` | Authorize release |

Do not add names here in a generate pass. Do not invent `process`, `handle`, or `save` as a [primitive](../docs/TERMS.md#primitive).

## Reserved

These names are **not** legal public verb names on a [noun](../docs/TERMS.md#noun). They live under an interior module (e.g. `primitives/write.py` or `_write`). A public `Invoice.write` is a [defect](../docs/TERMS.md#defect).
