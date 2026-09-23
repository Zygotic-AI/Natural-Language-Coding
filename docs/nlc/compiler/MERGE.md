# [ACS](../../TERMS.md#acs) merge (settled)

Date: 2026-09-15

Two layers of one architecture. Not two competing sources of truth.

- **[PLANIT](../../TERMS.md#planit)** — process. How work is interviewed, planned, bound, generated, audited, and sent back through [RCA](../../TERMS.md#rca).
- **[BBP](../../TERMS.md#bbp)** — design. The shape generated code must have.
- **[NLC](../../TERMS.md#nlc)** — product umbrella; **[compiler](../../TERMS.md#compiler)** + **[compiled system](../../TERMS.md#compiled-system)** per [ADR](../../TERMS.md#adr) 0011 (legacy “ACS = both” retired).

[PLANIT](../../TERMS.md#planit) does not replace [BBP](../../TERMS.md#bbp). [BBP](../../TERMS.md#bbp) is the instruction set the process is not allowed to skip.

[AIMS](../../TERMS.md#aims) was the process draft. [BBA](../../TERMS.md#bba) was an earlier name for [BBP](../../TERMS.md#bbp). Use the table in [NAMES.md](NAMES.md).

---

## Vocabulary

| Say | Do not say | Meaning |
|-----|------------|---------|
| [BBP](../../TERMS.md#bbp) standard | standing rules, “fixture” for Invoice.py | Permanent *method*: small boundaries, [noun](../../TERMS.md#noun) inside, verbs on the edge, goals only call verbs |
| [Adjective](../../TERMS.md#adjective) | law, invariant | A descriptor on a [noun](../../TERMS.md#noun) that every use must leave true |
| [Requirement](../../TERMS.md#requirement) | | Constraint on behavior |
| [ADR](../../TERMS.md#adr) | | Dated choice |
| [Goal](../../TERMS.md#goal) | | Outcome to produce |
| [Knowledge domain](../../TERMS.md#knowledge-domain) | first-class kind | Standing ADRs + requirements + facts the [interview](../../TERMS.md#interview) must consult |
| [Gate](../../TERMS.md#gate) | binder (as a noun) | Machine that fails the change when an [audit](../../TERMS.md#audit) would be not-met |
| [Binding](../../TERMS.md#binding) | | Planning act of pointing a statement at the rules it must honor |
| Turns red | | [Gate](../../TERMS.md#gate) exits non-zero and prints the violation |

---

## Two lists, both in force

**Human-held.** People write or sign these.

- Goals
- Requirements
- ADRs
- Certified [RCA](../../TERMS.md#rca)
- Accepted [audit](../../TERMS.md#audit) findings

Humans do not author [noun](../../TERMS.md#noun) classes or verb bodies. They hire the [compiler](../../TERMS.md#compiler).

**Derived.** Regenerable.

- A particular [noun](../../TERMS.md#noun) module (`Invoice`)
- Verb implementations behind published contracts
- [Goal](../../TERMS.md#goal) code
- Most runbooks and diagrams

**[BBP](../../TERMS.md#bbp) standard** is neither. It is the method. It does not change when Invoice internals are regenerated.

**Contracts** are derived but *breaking* a [published verb contract](../../TERMS.md#published-verb-contract) is a product event: impact on callers, then fix the *[requirement](../../TERMS.md#requirement)* if the behavior was wrong, then regenerate. Humans do not patch the generated [contract](../../TERMS.md#contract) to hide a [defect](../../TERMS.md#defect).

---

## Citizens, by layer

Process citizens (PLANIT): [goal](../../TERMS.md#goal), [requirement](../../TERMS.md#requirement), [ADR](../../TERMS.md#adr), [rule](../../TERMS.md#rule), [interview](../../TERMS.md#interview), [RCA](../../TERMS.md#rca).


Design citizens (BBP): [noun](../../TERMS.md#noun), verb, goal-as-boundary, [contract](../../TERMS.md#contract), [gate](../../TERMS.md#gate).

[Goal](../../TERMS.md#goal) sits on both lists on purpose.

Not citizens: workflow-as-a-new-type (it is a goal of goals; durable is a property), business-need-as-a-document (optional tag on a goal), process-as-an-object (it is the generated body of a goal), knowledge-domain-as-a-new-kind (it is standing ADRs + requirements + facts, not a code citizen).

---

## The compile [gate](../../TERMS.md#gate)

Generation is incomplete unless:

1. Output is BBP-shaped.
2. Every invoice-shaped fact lives behind an Invoice [boundary](../../TERMS.md#boundary) (noun inside, verbs on the edge).
3. A [gate](../../TERMS.md#gate) fails a [goal](../../TERMS.md#goal) that implements that [adjective](../../TERMS.md#adjective) itself or writes [noun](../../TERMS.md#noun) fields.

Two small [goal](../../TERMS.md#goal) boxes are fine if both only call Invoice verbs. The failure is a [goal](../../TERMS.md#goal) box that *is* a second Invoice.

---

## Human vs AI

Human = non-coding manager. Passes goals, requirements, ADRs; certifies [RCA](../../TERMS.md#rca); validates [audit](../../TERMS.md#audit) findings.

AI = developer bound to the [BBP](../../TERMS.md#bbp) standard. Writes nouns, verbs, code.

If a human must edit generated files to keep adjectives consistent, the architecture failed. Fail → [RCA](../../TERMS.md#rca) → tighter [interview](../../TERMS.md#interview) / [requirement](../../TERMS.md#requirement) / [ADR](../../TERMS.md#adr) / knowledge → regenerate.

The red [gate](../../TERMS.md#gate) is not a human in the file. It is the signal [RCA](../../TERMS.md#rca) gets before users pay.

---

## Process

See [PROCESS.md](PROCESS.md) (PLANIT steps 0–7).

---

## What this is not

- Not “goals and requirements only; shape is optional.”
- Not “humans confirm by reading Invoice.py into shape.”
- Not the old [AIMS](../../TERMS.md#aims) zip-as-written (those papers omitted noun/verb/gate).
- Not a second governance tree. [Charter](../../TERMS.md#charter) + bind + red check.

---

## Open items (not disagreements)

None. Contract-change loudness is [ADR 0006](../../../adrs/0006-contract-change-notice.md).

