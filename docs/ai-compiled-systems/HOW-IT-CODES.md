# How it codes (under the covers)

Consumer-facing story: [manifesto](MANIFESTO.md) and [intent surface](INTENT-SURFACE.md). This page is **how the [AI system compiler](../TERMS.md#compiler) builds software** without asking humans to author [noun](../TERMS.md#noun) files.

BBA/BBP shape is internal vocabulary: small boundaries, [noun](../TERMS.md#noun) inside, verbs on the edge, goals only call verbs ([`CHARTER.md`](../../CHARTER.md)). You do not need that vocabulary to **use** [NLC](../TERMS.md#nlc); you need it to **[audit](../TERMS.md#audit)** emit.

## Pipeline (one compile)

```text
┌─────────────────────────────────────────────────────────────┐
│ Human intent (touch + approve)                               │
│   goals · requirements · knowledge domains · ADRs · adopted rules │
└────────────────────────────┬────────────────────────────────┘
                             │ PLANIT: load → interview → plan
                             ▼
┌─────────────────────────────────────────────────────────────┐
│ Bind every statement to requirement / ADR / rule ids + BBP   │
│ Close gaps (no unbound business statements)                  │
└────────────────────────────┬────────────────────────────────┘
                             │ generate ONE artifact per step
                             ▼
┌─────────────────────────────────────────────────────────────┐
│ Compiler emit: noun · verbs · adjectives · goal body · tests │
│ Tags/primitives applied per adopted if/thens (ADR 0007)      │
└────────────────────────────┬────────────────────────────────┘
                             │ immediate gate (6.5)
                             ▼
┌─────────────────────────────────────────────────────────────┐
│ Machine metrics + adversarial audit on that artifact         │
│ FAIL → RCA → intent/bind → regenerate (not patch emit)       │
└────────────────────────────┬────────────────────────────────┘
                             │ prove (full tree)
                             ▼
┌─────────────────────────────────────────────────────────────┐
│ Compile green · optional human release (`Released-by:`)      │
└─────────────────────────────────────────────────────────────┘
```

## What gets built when

| Step | [Compiler](../TERMS.md#compiler) output | [Rule](../TERMS.md#rule) |
| ---- | --------------- | ---- |
| New domain concept | **[Noun](../TERMS.md#noun)** + **adjectives** + **verbs** on the [boundary](../TERMS.md#boundary) | One home per [adjective](../TERMS.md#adjective) (R24 / C19) |
| Use case | **[Goal](../TERMS.md#goal)** implementation | Calls verbs only; no [noun](../TERMS.md#noun) field writes (R5) |
| Policy / standard adopted | **Rules** + **tags** on IR | Prose [ADR](../TERMS.md#adr) → if/then; [compiler](../TERMS.md#compiler) applies or fails |
| Verb interior | Calls to closed **primitives** | Undeclared [primitive](../TERMS.md#primitive) in body → fail (ADR 0009) |
| Neighbor access | **Contracts** only | No reaching into another [noun](../TERMS.md#noun)’s fields |

TypeScript or Python is an **object file**—proof that intent compiled—not the SSOT ([`COMPILER.md`](COMPILER.md)).

## When generation is incomplete

Generation stops (gate red) if any of these hold—non-exhaustive; see [`COMPILER.md`](COMPILER.md):

- [Goal](../TERMS.md#goal) assigns a [noun](../TERMS.md#noun) field.
- Same [adjective](../TERMS.md#adjective) implemented twice.
- Plan statement has no [binding](../TERMS.md#binding).
- [Published verb contract](../TERMS.md#published-verb-contract) broke and callers were not in the plan.
- Public [boundary](../TERMS.md#boundary) missing failure mode.

Same inputs + same standard → same **shape and contracts**. Interiors may change behind a [contract](../TERMS.md#contract).

## Audits in the build, not after QA

Traditional flow often finds forked business rules in UAT or production. [NLC](../TERMS.md#nlc) inserts **[audit](../TERMS.md#audit) immediately after each emit** so the expensive stages (PR review, QA, UAT, user) see fewer novel defects. Cost model: [`QUALITY-PROCESSES.md`](QUALITY-PROCESSES.md).

## Roles (compressed)

| Role | Holds |
| ---- | ----- |
| Human manager | Goals, requirements, [knowledge domains](../TERMS.md#knowledge-domain); adopts ADRs and rules; release |
| AI [compiler](../TERMS.md#compiler) | Nouns, verbs, adjectives, [goal](../TERMS.md#goal) bodies, tests, derived views |
| Red [gate](../TERMS.md#gate) | Machine signal for [RCA](../TERMS.md#rca)—not a human editing the object file |

Full matrix: [`INTENT-SURFACE.md`](INTENT-SURFACE.md). Step list: [`PROCESS.md`](PROCESS.md). Orchestration in Cursor: [`PLANIT-ORCHESTRATION.md`](PLANIT-ORCHESTRATION.md).
