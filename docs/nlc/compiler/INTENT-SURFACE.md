# What humans hold vs what the [compiler](../../TERMS.md#compiler) emits

SSOT for division of labor in [Natural Language Coding](../../TERMS.md#nlc). Design shape (nouns, verbs, gates) is [`CHARTER.md`](../../../CHARTER.md). This page is the **[intent surface](../../TERMS.md#intent-surface)**—what managers and approvers touch—versus **derived** artifacts the [AI system compiler](../../TERMS.md#compiler) regenerates.

## Three things humans focus on (value stream start)

These are the durable product for non-coding managers. Everything downstream is derived or proof.

| Focus | Say | What it is |
| ----- | --- | ---------- |
| **Goals** | [goal](../../TERMS.md#goal) | Outcomes the system must deliver. Orchestration boundaries; they call published verbs only. |
| **Requirements** | [requirement](../../TERMS.md#requirement) | [Binding](../../TERMS.md#binding) constraints on behavior—policies, standards, regulatory obligations, “must / must not,” SLAs, and similar prose **before** or **without** a dated decision record. When the choice is recorded with alternatives and consequences, it becomes (or updates) an **[ADR](../../TERMS.md#adr)**. |
| **[Knowledge domains](../../TERMS.md#knowledge-domain)** | [knowledge domain](../../TERMS.md#knowledge-domain), standing knowledge | Facts and references the [interview](../../TERMS.md#interview) and bind steps must consult: what is in scope, what entities exist, which external standards apply. Not a fourth code citizen—[standing requirements](../../TERMS.md#standing-requirements), ADRs, and **facts** the rules can bind ([`MERGE.md`](MERGE.md), [UC18](../../TERMS.md#uc18)). |

**Requirements** is the single umbrella word for standards, policies, business rules in prose, PCI/PII obligations, and operational constraints **until** they are folded into an [ADR](../../TERMS.md#adr) or reduced to executable **rules**. Do not invent a parallel “policy” type; say **[requirement](../../TERMS.md#requirement)** or name the standard (“PCI DSS”) and bind it.

Optional split for clarity in conversation only:

- **[Standing requirements](../../TERMS.md#standing-requirements)** — constraints that apply across goals (retention, encryption policy, runtime engine).
- **Knowledge facts** — domain truths (“invoice receives payments,” “PAN is in scope”) proposed into the [knowledge domain](../../TERMS.md#knowledge-domain); unbound fact → [interview](../../TERMS.md#interview) continues (UC1 / UC18).

## Human touch vs human approve

**Touch** = author, refine, or negotiate in natural language (interview, bind, gap closure).

**Approve** = dated sign-off, adoption, or release authority. The [compiler](../../TERMS.md#compiler) may **draft**; it does not **adopt**.

| Artifact | Human touch | Human approve | [Compiler](../../TERMS.md#compiler) role |
| -------- | ----------- | ------------- | --------------- |
| **[Goal](../../TERMS.md#goal)** | yes — outcomes, priorities | when class requires `Ratified-by:` | emits [goal](../../TERMS.md#goal) implementation; never assigns [noun](../../TERMS.md#noun) fields |
| **[Requirement](../../TERMS.md#requirement)** | yes — constraints, standards, policies | when promoted to ratified charter/rule class | binds statements to [requirement](../../TERMS.md#requirement) ids; does not invent business law silently |
| **[Knowledge domain](../../TERMS.md#knowledge-domain)** | yes — facts, scope, references | fact adoption / gap closure (`propose-fact`, steward verbs) | `load-knowledge-domain`; flags gaps; does not emit from prompt memory |
| **[ADR](../../TERMS.md#adr)** | yes — context, options, consequences | **yes** — dated decision adopted | keeps [ADR](../../TERMS.md#adr) as *why*; reduces to rules when adopted ([ADR 0007](../../../adrs/0007-tags-primitives-reduced-adrs.md)) |
| **[Rule](../../TERMS.md#rule)** (if/then over tags, primitives, facts) | review drafts | **yes** — [rule](../../TERMS.md#rule) set **adopted** with the [ADR](../../TERMS.md#adr) | applies adopted rules at emit; unbound [rule](../../TERMS.md#rule) → [gate](../../TERMS.md#gate) fails |
| **Tags** on nouns / adjectives | name classifications in adoption | **yes** — part of adopt (mark IR) | proposes / applies markings per adopted rules; tags feed if/thens |
| **Primitives** (closed verb interior set) | only when closed set must expand | **yes** — charter-grade [ADR](../../TERMS.md#adr) to extend set | maps verb bodies to declared primitives ([ADR 0009](../../../adrs/0009-primitive-interior-functions.md)) |
| **[Noun](../../TERMS.md#noun)** (module, state, adjectives) | no authoring | indirect — via requirements/ADRs/rules | **creates** and regenerates [noun](../../TERMS.md#noun) + [adjective](../../TERMS.md#adjective) implementations |
| **Verb** (contract + body) | no authoring | breaking [contract](../../TERMS.md#contract) change → accept requirement/ADR, then regenerate ([ADR 0006](../../../adrs/0006-contract-change-notice.md)) | **creates** [contract](../../TERMS.md#contract) and implementation |
| **[Adjective](../../TERMS.md#adjective)** (descriptor on noun) | no authoring | same as [noun](../../TERMS.md#noun) — one home per [adjective](../../TERMS.md#adjective) is a design law | **creates**; two implementations → [gate](../../TERMS.md#gate) red |
| **[Goal](../../TERMS.md#goal) code** | no | [audit](../../TERMS.md#audit) acceptance | **creates** |
| **Tests, fitness, generated views** | no | — | **creates** |
| **[RCA](../../TERMS.md#rca) record** | touch narrative | **certified** [RCA](../../TERMS.md#rca) | consumes [gate](../../TERMS.md#gate) signal; does not patch emit to green |
| **Adversarial [audit](../../TERMS.md#audit)** | — | **accepted** findings (or rebuttal) | separate role from generator |
| **[Ship](../../TERMS.md#ship) / release** | — | **`Released-by:`** (and **`Ratified-by:`** when required) | [prove](../../TERMS.md#prove) PASS is compile, not release ([`PROCESS.md`](PROCESS.md)) |

## [Compiler](../../TERMS.md#compiler) creates (derived, regenerable)

The [AI system compiler](../../TERMS.md#compiler) emits BBP-shaped artifacts. Humans do not maintain these files by hand.

- **[Noun](../../TERMS.md#noun)** boundaries (identity, adjectives, verb surface)
- **Verb** implementations behind published contracts
- **[Goal](../../TERMS.md#goal)** bodies that only call those verbs
- **Tags** on the IR as required by adopted rules (not free-form labels invented at emit time)
- **Tests** and machine-checkable evidence
- **Generated** diagrams and impact views (not hand-edited JSON)

**Not derived:** the BBP/BBA **method** (`CHARTER.md`)—the instruction set the [compiler](../../TERMS.md#compiler) must not skip.

## Corrections to informal lists

| Informal claim | Validated |
| -------------- | --------- |
| “Humans touch goals and standards” | **Goals** + **requirements** (standards/policies are requirements until ADR/rule adoption). |
| “Knowledge is separate” | **[Knowledge domains](../../TERMS.md#knowledge-domain)** are the third human focus—not a code type, but a first-class interview/bind input. |
| “Humans approve [ADR](../../TERMS.md#adr) and if/then” | **[ADR](../../TERMS.md#adr) adoption** and **[rule](../../TERMS.md#rule) adoption** (if/then is the executable face of an adopted ADR). |
| “[Compiler](../../TERMS.md#compiler) creates tags; human approves” | **yes** — tags are meaningless without adopted rules; adoption marks nouns/adjectives and binds [rule](../../TERMS.md#rule) ids ([ADR 0007](../../../adrs/0007-tags-primitives-reduced-adrs.md)). |
| “[Compiler](../../TERMS.md#compiler) creates adjectives” | **yes** as **implementations** of descriptors required by goals and requirements; humans do not edit [adjective](../../TERMS.md#adjective) fields in generated code to “fix” drift. |
| “Humans approve every [noun](../../TERMS.md#noun)” | **no** — humans approve **intent** (goals, requirements, ADRs, rules). Nouns are regenerated when that intent changes. |
| “Humans write code in emergencies” | **[Charter](../../TERMS.md#charter) violation for product truth** — emergency patch of generated code hides a process [defect](../../TERMS.md#defect); [RCA](../../TERMS.md#rca) → intent → regenerate (UC10). |

## Where this shows up in the loop

```text
Interview / touch:     goals, requirements, knowledge domains
Plan / bind:           point statements at requirement, ADR, rule ids + BBP standard
Adopt / approve:       ADR, rules, tags/primitives extension, ratification, release
Generate + gate:       compiler emits one artifact → immediate adversarial gate (PLANIT 6 / 6.5)
Prove:                 machine fitness + adversarial audit
```

See [PROCESS.md](PROCESS.md), [HOW-IT-CODES.md](HOW-IT-CODES.md), [MANIFESTO.md](MANIFESTO.md).
