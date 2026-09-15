# ACS merge (settled)

Date: 2026-09-15

Two layers of one architecture. Not two competing sources of truth.

- **PLANIT** — process. How work is interviewed, planned, bound, generated, audited, and sent back through RCA.
- **BBP** — design. The shape generated code must have.
- **ACS** — the name for both layers together.

PLANIT does not replace BBP. BBP is the instruction set the process is not allowed to skip.

AIMS was the process draft. BBA was an earlier name for BBP. Use the table in [NAMES.md](NAMES.md).

---

## Vocabulary

| Say | Do not say | Meaning |
|-----|------------|---------|
| BBP standard | standing rules, “fixture” for Invoice.py | Permanent *method*: small boundaries, noun inside, verbs on the edge, goals only call verbs |
| Adjective | law, invariant | A descriptor on a noun that every use must leave true |
| Requirement | | Constraint on behavior |
| ADR | | Dated choice |
| Goal | | Outcome to produce |
| Knowledge domain | first-class kind | A *shelf* of standing ADRs + requirements the interview must consult |
| Gate | binder (as a noun) | Machine that fails the change when an audit would be not-met |
| Binding | | Planning act of pointing a statement at the rules it must honor |
| Turns red | | Gate exits non-zero and prints the violation |

---

## Two lists, both in force

**Human-held.** People write or sign these.

- Goals
- Requirements
- ADRs
- Certified RCA
- Accepted audit findings

Humans do not author noun classes or verb bodies. They hire the compiler.

**Derived.** Regenerable.

- A particular noun module (`Invoice`)
- Verb implementations behind published contracts
- Goal code
- Most runbooks and diagrams

**BBP standard** is neither. It is the method. It does not change when Invoice internals are regenerated.

**Contracts** are derived but *breaking* a published verb contract is a product event: impact on callers, then fix the *requirement* if the behavior was wrong, then regenerate. Humans do not patch the generated contract to hide a defect.

---

## Citizens, by layer

Process citizens (PLANIT): goal, requirement, ADR, interview, RCA.

Design citizens (BBP): noun, verb, goal-as-boundary, contract, gate.

Goal sits on both lists on purpose.

Not citizens: workflow-as-a-new-type (it is a goal of goals; durable is a property), business-need-as-a-document (optional tag on a goal), process-as-an-object (it is the generated body of a goal), knowledge-domain-as-a-new-kind (it is a shelf).

---

## The compile gate

Generation is incomplete unless:

1. Output is BBP-shaped.
2. Every invoice-shaped fact lives behind an Invoice boundary (noun inside, verbs on the edge).
3. A gate fails a goal that implements that adjective itself or writes noun fields.

Two small goal boxes are fine if both only call Invoice verbs. The failure is a goal box that *is* a second Invoice.

---

## Human vs AI

Human = non-coding manager. Passes goals, requirements, ADRs; certifies RCA; validates audit findings.

AI = developer bound to the BBP standard. Writes nouns, verbs, code.

If a human must edit generated files to keep adjectives consistent, the architecture failed. Fail → RCA → tighter interview / requirement / ADR / knowledge → regenerate.

The red gate is not a human in the file. It is the signal RCA gets before users pay.

---

## Process

See [PROCESS.md](PROCESS.md) (PLANIT steps 0–7).

---

## What this is not

- Not “goals and requirements only; shape is optional.”
- Not “humans confirm by reading Invoice.py into shape.”
- Not the old AIMS zip-as-written (those papers omitted noun/verb/gate).
- Not a second governance tree. Charter + bind + red check.

---

## Open items (not disagreements)

None. Contract-change loudness is [ADR 0006](../../adrs/0006-contract-change-notice.md).

