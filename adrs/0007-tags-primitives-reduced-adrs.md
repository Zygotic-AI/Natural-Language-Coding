# [ADR](../docs/TERMS.md#adr) 0007 — Tags, primitives, and reduced ADRs

- Status: Accepted
- Date: 2026-09-16
- Deciders: Human manager
- Class: F (charter extension)

## Context

ADRs, requirements, and standards are prose. The [compiler](../docs/TERMS.md#compiler) cannot apply prose.
PCI, PII, and “durable goals run on Temporal” were being treated as different
kinds of law. They are not: they are facts plus if-thens, if we name the facts.

## Decision

**Every adopted [ADR](../docs/TERMS.md#adr) that constrains emit reduces to rules over tags, primitives,
and facts. The [ADR](../docs/TERMS.md#adr) remains the why. The if-then is what the [compiler](../docs/TERMS.md#compiler) runs.**

### Citizens (not new design primitives)

| Piece | What it is |
|---|---|
| **[Adjective](../docs/TERMS.md#adjective)** | Data slot on a [noun](../docs/TERMS.md#noun) (`card_number`, `status`). |
| **[Tag](../docs/TERMS.md#tag)** | Classification on an [adjective](../docs/TERMS.md#adjective) or on a [noun](../docs/TERMS.md#noun) (`pan`, `pii`, `pci-scope`, `runtime=temporal`). |
| **[Primitive](../docs/TERMS.md#primitive)** | Closed [action](../docs/TERMS.md#action) (`store`, `return`, `log`, `display`, `transmit`, `copy`, `retain`, `retry`, `wait`, `ship`). |
| **Fact** | Other IR the [compiler](../docs/TERMS.md#compiler) already has (`goal.durable`, `change.class`). |
| **[Rule](../docs/TERMS.md#rule)** | `if tags ∧ primitives ∧ facts → must \| forbid`. |

Nouns and adjectives may carry tags. Customer is still a [noun](../docs/TERMS.md#noun), not a [tag](../docs/TERMS.md#tag) of Invoice.

### Verbs

When a verb is created it declares: these primitives, on these tagged adjectives.
Undeclared [primitive](../docs/TERMS.md#primitive) that the body still performs → fail (default closed).
Over-declare is cheap. Language adapters map known calls to primitives.

### Adoption

When a human adopts a [requirement](../docs/TERMS.md#requirement) (PCI, Temporal, …):

1. Write the [ADR](../docs/TERMS.md#adr) (why).
2. If the current primitive/tag/fact set cannot express it, **add** to the set (charter-grade; this is an ADR).
3. Prefer a new **[tag](../docs/TERMS.md#tag) or fact** before a new [primitive](../docs/TERMS.md#primitive) (Temporal does not need `store`).
4. Write the rules. Point each [rule](../docs/TERMS.md#rule) id at the [ADR](../docs/TERMS.md#adr).
5. Mark adjectives and nouns in the IR.
6. The [compiler](../docs/TERMS.md#compiler) **applies** the [rule](../docs/TERMS.md#rule) (emits the obligation or the gate fails). Prompt memory is not the bind.

### Examples (normative shape, not a PCI implementation)

- `pan ∧ write → encrypt; key not in this noun` (`store` in earlier drafts = `write`)

- `pan ∧ use → consuming verb only; clear after`
- `pan ∧ log → forbid`
- `pan ∧ return → forbid` (R32 is this rule for v1 `taint.txt`)
- `goal.durable ∧ engine.runtime ≠ temporal → forbid`

Derived values keep the parent [tag](../docs/TERMS.md#tag) unless a [rule](../docs/TERMS.md#rule) says they do not (`last4` stays `pan`; `amount` does not).

### [Durability](../docs/TERMS.md#durability)

The engine is a [noun](../docs/TERMS.md#noun) tagged `runtime=temporal` (or `airflow`, or none).
A durable [goal](../docs/TERMS.md#goal) may only call an engine with the runtime the [ADR](../docs/TERMS.md#adr) named.
Same if-then shape as PAN. No fourth design [primitive](../docs/TERMS.md#primitive).

## Consequences

- [Charter](../docs/TERMS.md#charter) §4.7 points here. [Primitive](../docs/TERMS.md#primitive) **names** are [`integrity/primitives.md`](../integrity/primitives.md) (ADR 0009). No new **R** id until a rule-IR [gate](../docs/TERMS.md#gate) exists (R27).

- v1 `taint.txt` is the Python-era stand-in for tags on sensitive adjectives.
- Executable [rule](../docs/TERMS.md#rule) runner is **parked**, same class of work as [`docs/LANGUAGE-SCANNER.md`](../docs/LANGUAGE-SCANNER.md): spec the IR, then the [gate](../docs/TERMS.md#gate). Do not fork prose ADRs into prompt checklists.
- Process ADRs (ratify class A, no noun inheritance) use facts (`change.class`, `noun.inherits`) on the same [rule](../docs/TERMS.md#rule) machine. They do not get a fake `store`.

## Rejected

- **Prose-only ADRs at emit time** — the [compiler](../docs/TERMS.md#compiler) cannot apply them.
- **Open-ended primitives** — the verb invents `process` and skips `store`.
- **AI remembers the if-then** — hope. [Compiler](../docs/TERMS.md#compiler) applies or the [gate](../docs/TERMS.md#gate) fails.
- **Tags replace adjectives** — adjectives are state; tags classify it.
- **Temporal as a special parser** — it is a [noun](../docs/TERMS.md#noun) [tag](../docs/TERMS.md#tag) plus a durable fact.
