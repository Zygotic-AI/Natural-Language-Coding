# What the human holds vs what the [compiler](../../TERMS.md#compiler) infers

SSOT for division of labor in [Natural Language Coding](../../TERMS.md#nlc). Design shape (nouns, verbs, gates) is [`CHARTER.md`](../../../CHARTER.md). This page is the **[intent surface](../../TERMS.md#intent-surface)** — ratified by [ADR 0036](../../../adrs/0036-inference-only-human-surface.md): the human contributes **goal and policy only**; everything else is inference.

## The two human contributions

| Human contributes | What it is |
| --- | --- |
| **Goal** | The outcome the system must deliver. Stated in natural language; the [compiler](../../TERMS.md#compiler) derives plans, actions, bindings, and emit from it. |
| **Policy** | Constraints, standards, and “must / must not” that govern the build — regulatory, operational, or business. The [compiler](../../TERMS.md#compiler) folds policy into [requirements](../../TERMS.md#requirement), [ADRs](../../TERMS.md#adr), and [rules](../../TERMS.md#rule); the human does not author those records on the happy path. |

No other human **authorship** is permitted on the happy path. Plans, ADR ids, rule ids, thought anchors, manifests, tags, and noun/verb names are **derived**. If the [compiler](../../TERMS.md#compiler) cannot derive one, it **refuses and reports the gap** — it does not ask the human to fill it. A gap is evidence the process is unsuitable; it is climbed upstream ([ADR 0025](../../../adrs/0025-belief-no-blame-climb.md)), never patched by human authorship.

**Machine records** (for example `.nlc/interview-packet.json` with `goals`, `requirements`, `knowledge_domains`) are agent-written extracts of goal and policy for UC1 gates — not a third human input type.

## What the [compiler](../../TERMS.md#compiler) infers (derived, regenerable)

- Plans and atomic actions ([ADR 0024](../../../adrs/0024-nlc-factory-spine.md), [ADR 0030](../../../adrs/0030-pipeline-wiring.md))
- ADR bindings to actions, and reverse audit that every applicable ADR is bound
- Emit manifests (full schema, optional fields as `na`), thought anchors, decision traces
- Tags, [adjectives](../../TERMS.md#adjective), [noun](../../TERMS.md#noun) and verb structure, tests
- [Requirements](../../TERMS.md#requirement) and [knowledge-domain](../../TERMS.md#knowledge-domain) facts *as derived from policy*

The [compiler](../../TERMS.md#compiler) emits BBP-shaped artifacts. Humans do not maintain generated [noun](../../TERMS.md#noun) or [adjective](../../TERMS.md#adjective) implementations by hand.

**Not derived:** the BBP/BBA **method** (`CHARTER.md`) — the instruction set the [compiler](../../TERMS.md#compiler) must not skip.

## Human approve (judgment, not authorship)

Ratification, [ADR](../../TERMS.md#adr) adoption, [rule](../../TERMS.md#rule) adoption, release, and certified [RCA](../../TERMS.md#rca) remain human *approvals* (C24). That is judgment over derived artifacts, not authorship of them — consistent with [ADR 0036](../../../adrs/0036-inference-only-human-surface.md).

| Artifact | Human touch (goal/policy) | Human approve | [Compiler](../../TERMS.md#compiler) role |
| -------- | ------------------------- | ------------- | ---------------------------------------- |
| **[Goal](../../TERMS.md#goal)** | yes — outcomes in natural language | when class requires `Ratified-by:` | emits implementation; never assigns [noun](../../TERMS.md#noun) fields |
| **Policy** | yes — constraints and standards in prose | when promoted to ratified charter/rule class | derives requirements, ADRs, rules; does not invent business law silently |
| **[ADR](../../TERMS.md#adr)** | context via policy conversation | **yes** — dated adoption | keeps ADR as *why*; reduces to rules when adopted |
| **[Rule](../../TERMS.md#rule)** | review drafts | **yes** — rule set adopted | applies adopted rules at emit |
| **[Noun](../../TERMS.md#noun) / verb / [adjective](../../TERMS.md#adjective) code** | no authoring | indirect — via adopted intent | **creates** and regenerates |
| **[Ship](../../TERMS.md#ship) / release** | — | **`Released-by:`** | [prove](../../TERMS.md#prove) PASS is compile, not release |

## Where this shows up in the loop

```text
Human:                 goal + policy
Interview:             extract goal and policy; report gaps, never collect derived fields
Plan / bind / emit:    compiler infers everything; gates run immediately
Approve:               human ratifies / releases / certifies — judgment only
```

See [PROCESS.md](PROCESS.md), [HOW-IT-CODES.md](HOW-IT-CODES.md), [MANIFESTO.md](MANIFESTO.md), [ADR 0036](../../../adrs/0036-inference-only-human-surface.md).
