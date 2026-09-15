# BBA + AIMS merge (settled)

Date: 2026-09-15

Two layers of one architecture. Not two competing sources of truth.

- **AIMS** — process. How work is interviewed, planned, bound, generated, audited, and sent back through RCA.
- **BBA** (Boundary-Based Architecture / Boundary-Based Programming) — design. The shape generated code must have.

AIMS does not replace BBA. BBA is the instruction set the process is not allowed to skip.

---

## Vocabulary

| Say | Do not say | Meaning |
|-----|------------|---------|
| BBA standard | standing rules, “fixture” for Invoice.py | Permanent *method*: small boundaries, noun inside, verbs on the edge, goals only call verbs |
| Invariant | law | A property of a thing that every use must leave true (e.g. no void after paid; balance rules) |
| Requirement | | Constraint on behavior (PCI, “balance never negative”) |
| ADR | | Dated choice (Postgres, not Oracle) |
| Goal | | Outcome to produce |
| Knowledge domain | first-class kind | A *shelf* of standing ADRs + requirements the interview must consult |
| Binder | the requirement itself | Machine that fails the change when an audit would be not-met |
| Turns red | | Binder exits non-zero and prints the violation |

---

## Two lists, both in force

**Human-held (manager artifacts).** People write or sign these.

- Goals
- Requirements
- ADRs
- Certified RCA
- Accepted audit findings

Humans do not author noun classes or verb bodies. They hire the compiler.

**Derived (AI emits, disposable).** Regenerable.

- A particular noun module (`Invoice`)
- Verb implementations behind published contracts
- Goal code
- Most runbooks and diagrams

**BBA standard** is neither. It is the method. It does not change when Invoice internals are regenerated.

**Contracts** are derived but *breaking* a published verb contract is a product event: impact on callers, then fix the *requirement* if the behavior was wrong, then regenerate. Humans do not patch the generated contract to hide a defect.

---

## Citizens, by layer

Process citizens (AIMS): goal, requirement, ADR, interview, RCA.

Design citizens (BBA): noun, verb, goal-as-boundary, contract, binder.

Goal sits on both lists on purpose.

Not citizens: workflow-as-a-new-type (it is a goal of goals; durable is a property), business-need-as-a-document (optional tag on a goal), process-as-an-object (it is the generated body of a goal), knowledge-domain-as-a-new-kind (it is a shelf).

---

## The compile gate (non-negotiable)

Generation is incomplete unless:

1. Output is BBA-shaped.
2. Every invoice-shaped fact lives behind an Invoice boundary (noun inside, verbs on the edge).
3. A binder fails a goal that implements that invariant itself or writes noun fields.

Two small goal boxes are fine if both only call Invoice verbs. The failure is a goal box that *is* a second Invoice.

---

## Human vs AI

Human = non-coding manager. Passes goals, requirements, ADRs; certifies RCA; validates audit findings.

AI = developer bound to the BBA standard. Writes nouns, verbs, code.

If a human must edit generated files to keep invariants consistent, the architecture failed. Fail → RCA → tighter interview / requirement / ADR / knowledge → regenerate.

The red binder is not a human in the file. It is the signal RCA gets before users pay.

---

## Process (load → prove)

See [PROCESS.md](PROCESS.md) for the full loop (steps 0–7).

---

## What this is not

- Not “goals and requirements only; shape is optional.”
- Not “humans confirm by reading Invoice.py into shape.”
- Not AIMS zip-as-written (those papers omitted noun/verb/binder).
- Not a second governance tree. Charter + bind + red check.

---

## Open items (not disagreements)

- How loud a contract-change notice is to the manager.
- Next binders after check 1 (import boundary, invariant locality).
- Goal / requirement authoring pages still to land in this folder.
