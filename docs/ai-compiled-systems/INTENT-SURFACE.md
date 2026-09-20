# What humans hold vs what the compiler emits

SSOT for division of labor in Natural Language Coding. Design shape (nouns, verbs, gates) is [`CHARTER.md`](../../CHARTER.md). This page is the **intent surface**—what managers and approvers touch—versus **derived** artifacts the AI system compiler regenerates.

## Three things humans focus on (value stream start)

These are the durable product for non-coding managers. Everything downstream is derived or proof.

| Focus | Say | What it is |
| ----- | --- | ---------- |
| **Goals** | goal | Outcomes the system must deliver. Orchestration boundaries; they call published verbs only. |
| **Requirements** | requirement | Binding constraints on behavior—policies, standards, regulatory obligations, “must / must not,” SLAs, and similar prose **before** or **without** a dated decision record. When the choice is recorded with alternatives and consequences, it becomes (or updates) an **ADR**. |
| **Knowledge domains** | knowledge domain, standing knowledge | Facts and references the interview and bind steps must consult: what is in scope, what entities exist, which external standards apply. Not a fourth code citizen—standing requirements, ADRs, and **facts** the rules can bind ([`MERGE.md`](MERGE.md), UC18). |

**Requirements** is the single umbrella word for standards, policies, business rules in prose, PCI/PII obligations, and operational constraints **until** they are folded into an ADR or reduced to executable **rules**. Do not invent a parallel “policy” type; say **requirement** or name the standard (“PCI DSS”) and bind it.

Optional split for clarity in conversation only:

- **Standing requirements** — constraints that apply across goals (retention, encryption policy, runtime engine).
- **Knowledge facts** — domain truths (“invoice receives payments,” “PAN is in scope”) proposed into the knowledge domain; unbound fact → interview continues (UC1 / UC18).

## Human touch vs human approve

**Touch** = author, refine, or negotiate in natural language (interview, bind, gap closure).

**Approve** = dated sign-off, adoption, or release authority. The compiler may **draft**; it does not **adopt**.

| Artifact | Human touch | Human approve | Compiler role |
| -------- | ----------- | ------------- | --------------- |
| **Goal** | yes — outcomes, priorities | when class requires `Ratified-by:` | emits goal implementation; never assigns noun fields |
| **Requirement** | yes — constraints, standards, policies | when promoted to ratified charter/rule class | binds statements to requirement ids; does not invent business law silently |
| **Knowledge domain** | yes — facts, scope, references | fact adoption / gap closure (`propose-fact`, steward verbs) | `load-shelf` (loads knowledge domain); flags gaps; does not emit from prompt memory |
| **ADR** | yes — context, options, consequences | **yes** — dated decision adopted | keeps ADR as *why*; reduces to rules when adopted ([ADR 0007](../../adrs/0007-tags-primitives-reduced-adrs.md)) |
| **Rule** (if/then over tags, primitives, facts) | review drafts | **yes** — rule set **adopted** with the ADR | applies adopted rules at emit; unbound rule → gate fails |
| **Tags** on nouns / adjectives | name classifications in adoption | **yes** — part of adopt (mark IR) | proposes / applies markings per adopted rules; tags feed if/thens |
| **Primitives** (closed verb interior set) | only when closed set must expand | **yes** — charter-grade ADR to extend set | maps verb bodies to declared primitives ([ADR 0009](../../adrs/0009-primitive-interior-functions.md)) |
| **Noun** (module, state, adjectives) | no authoring | indirect — via requirements/ADRs/rules | **creates** and regenerates noun + adjective implementations |
| **Verb** (contract + body) | no authoring | breaking contract change → accept requirement/ADR, then regenerate ([ADR 0006](../../adrs/0006-contract-change-notice.md)) | **creates** contract and implementation |
| **Adjective** (descriptor on noun) | no authoring | same as noun — one home per adjective is a design law | **creates**; two implementations → gate red |
| **Goal code** | no | audit acceptance | **creates** |
| **Tests, fitness, generated views** | no | — | **creates** |
| **RCA record** | touch narrative | **certified** RCA | consumes gate signal; does not patch emit to green |
| **Adversarial audit** | — | **accepted** findings (or rebuttal) | separate role from generator |
| **Ship / release** | — | **`Released-by:`** (and **`Ratified-by:`** when required) | prove PASS is compile, not release ([`PROCESS.md`](PROCESS.md)) |

## Compiler creates (derived, regenerable)

The AI system compiler emits BBP-shaped artifacts. Humans do not maintain these files by hand.

- **Noun** boundaries (identity, adjectives, verb surface)
- **Verb** implementations behind published contracts
- **Goal** bodies that only call those verbs
- **Tags** on the IR as required by adopted rules (not free-form labels invented at emit time)
- **Tests** and machine-checkable evidence
- **Generated** diagrams and impact views (not hand-edited JSON)

**Not derived:** the BBP/BBA **method** (`CHARTER.md`)—the instruction set the compiler must not skip.

## Corrections to informal lists

| Informal claim | Validated |
| -------------- | --------- |
| “Humans touch goals and standards” | **Goals** + **requirements** (standards/policies are requirements until ADR/rule adoption). |
| “Knowledge is separate” | **Knowledge domains** are the third human focus—not a code type, but a first-class interview/bind input. |
| “Humans approve ADR and if/then” | **ADR adoption** and **rule adoption** (if/then is the executable face of an adopted ADR). |
| “Compiler creates tags; human approves” | **yes** — tags are meaningless without adopted rules; adoption marks nouns/adjectives and binds rule ids ([ADR 0007](../../adrs/0007-tags-primitives-reduced-adrs.md)). |
| “Compiler creates adjectives” | **yes** as **implementations** of descriptors required by goals and requirements; humans do not edit adjective fields in generated code to “fix” drift. |
| “Humans approve every noun” | **no** — humans approve **intent** (goals, requirements, ADRs, rules). Nouns are regenerated when that intent changes. |
| “Humans write code in emergencies” | **Charter violation for product truth** — emergency patch of generated code hides a process defect; RCA → intent → regenerate (UC10). |

## Where this shows up in the loop

```text
Interview / touch:     goals, requirements, knowledge domains
Plan / bind:           point statements at requirement, ADR, rule ids + BBP standard
Adopt / approve:       ADR, rules, tags/primitives extension, ratification, release
Generate + gate:       compiler emits one artifact → immediate adversarial gate (PLANIT 6 / 6.5)
Prove:                 machine fitness + adversarial audit
```

See [PROCESS.md](PROCESS.md), [HOW-IT-CODES.md](HOW-IT-CODES.md), [MANIFESTO.md](MANIFESTO.md).
