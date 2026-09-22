# A-P4

- [Requirement](../../docs/TERMS.md#requirement): `P4`
- Outcome: **[met](../../docs/TERMS.md#met)** | **not [met](../../docs/TERMS.md#met)** only
- [Gate](../../docs/TERMS.md#gate): `tools/fitness-p4-r31.py`

## Statement

Every [boundary](../../docs/TERMS.md#boundary) declares hard input, output, and failure mode (error return, throw, or process exit).

## Bind

Wrapper runs both:

- `tools/fitness-agent-noun-structure.py` (agent nouns; always hub `agents/`)
- `tools/fitness-boundary-io.py` (code goals/nouns; argv roots)

Either child `NOT_MET` → P4 `NOT_MET`.

Designed pass (code half): `examples/invoice-correct/`.
Designed fail (code half): `examples/missing-failure-mode/`.
