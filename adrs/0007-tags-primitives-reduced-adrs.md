# ADR 0007 — Tags, primitives, and reduced ADRs

- Status: Accepted
- Date: 2026-09-16
- Deciders: Human manager
- Class: F (charter extension)

## Context

ADRs, requirements, and standards are prose. The compiler cannot apply prose.
PCI, PII, and “durable goals run on Temporal” were being treated as different
kinds of law. They are not: they are facts plus if-thens, if we name the facts.

## Decision

**Every adopted ADR that constrains emit reduces to rules over tags, primitives,
and facts. The ADR remains the why. The if-then is what the compiler runs.**

### Citizens (not new design primitives)

| Piece | What it is |
|---|---|
| **Adjective** | Data slot on a noun (`card_number`, `status`). |
| **Tag** | Classification on an adjective or on a noun (`pan`, `pii`, `pci-scope`, `runtime=temporal`). |
| **Primitive** | Closed action (`store`, `return`, `log`, `display`, `transmit`, `copy`, `retain`, `retry`, `wait`, `ship`). |
| **Fact** | Other IR the compiler already has (`goal.durable`, `change.class`). |
| **Rule** | `if tags ∧ primitives ∧ facts → must \| forbid`. |

Nouns and adjectives may carry tags. Customer is still a noun, not a tag of Invoice.

### Verbs

When a verb is created it declares: these primitives, on these tagged adjectives.
Undeclared primitive that the body still performs → fail (default closed).
Over-declare is cheap. Language adapters map known calls to primitives.

### Adoption

When a human adopts a requirement (PCI, Temporal, …):

1. Write the ADR (why).
2. If the current primitive/tag/fact set cannot express it, **add** to the set (charter-grade; this is an ADR).
3. Prefer a new **tag or fact** before a new primitive (Temporal does not need `store`).
4. Write the rules. Point each rule id at the ADR.
5. Mark adjectives and nouns in the IR.
6. The compiler **applies** the rule (emits the obligation or the gate fails). Prompt memory is not the bind.

### Examples (normative shape, not a PCI implementation)

- `pan ∧ write → encrypt; key not in this noun` (`store` in earlier drafts = `write`)

- `pan ∧ use → consuming verb only; clear after`
- `pan ∧ log → forbid`
- `pan ∧ return → forbid` (R32 is this rule for v1 `taint.txt`)
- `goal.durable ∧ engine.runtime ≠ temporal → forbid`

Derived values keep the parent tag unless a rule says they do not (`last4` stays `pan`; `amount` does not).

### Durability

The engine is a noun tagged `runtime=temporal` (or `airflow`, or none).
A durable goal may only call an engine with the runtime the ADR named.
Same if-then shape as PAN. No fourth design primitive.

## Consequences

- Charter §4.7 points here. Primitive **names** are [`integrity/primitives.md`](../integrity/primitives.md) (ADR 0009). No new **R** id until a rule-IR gate exists (R27).

- v1 `taint.txt` is the Python-era stand-in for tags on sensitive adjectives.
- Executable rule runner is **parked**, same class of work as [`docs/LANGUAGE-SCANNER.md`](../docs/LANGUAGE-SCANNER.md): spec the IR, then the gate. Do not fork prose ADRs into prompt checklists.
- Process ADRs (ratify class A, no noun inheritance) use facts (`change.class`, `noun.inherits`) on the same rule machine. They do not get a fake `store`.

## Rejected

- **Prose-only ADRs at emit time** — the compiler cannot apply them.
- **Open-ended primitives** — the verb invents `process` and skips `store`.
- **AI remembers the if-then** — hope. Compiler applies or the gate fails.
- **Tags replace adjectives** — adjectives are state; tags classify it.
- **Temporal as a special parser** — it is a noun tag plus a durable fact.
