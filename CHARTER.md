# [Boundary-Based Programming](docs/TERMS.md#bbp)

A working spec for software that humans and agents can change without scattering adjectives or widening [blast radius](docs/TERMS.md#blast-radius).

This document is the [charter](docs/TERMS.md#charter). Implementation must be confirmable against the rules in [Confirmation checklist](#confirmation-checklist). If a [rule](docs/TERMS.md#rule) cannot be checked, it is not a [rule](docs/TERMS.md#rule) yet — it is a wish.

---

## 1. Purpose

The [goal](docs/TERMS.md#goal) is surgical change.

An agent (or a person) should be able to answer three questions before touching code:

1. What is the unit of change?
2. What is allowed to mutate state?
3. If I change this, what else must still be true?

[Boundary-Based Programming](docs/TERMS.md#bbp) organizes a system around **nouns** that own adjectives, **verbs** that are the only legal way to change those nouns, and **goals** that orchestrate work across nouns and the outside world. Boundaries are not documentation. They are contracts plus enforcement.

This exists because AI-assisted engineering fails in two opposite ways:

- The agent sees the whole repository and thrashes.
- The agent sees one folder, makes that folder green, and silently breaks an [adjective](docs/TERMS.md#adjective) that lived somewhere else.

We shrink the search space for *use-case* changes without exploding the search space for *concept* changes.

---

## 2. Why this shape

Layered architecture groups code by technical concern. Agents then hunt across controllers, services, and repositories to change one business outcome.

Goal-only architecture groups code by verb. That helps a single use-case edit. It hurts when the [adjective](docs/TERMS.md#adjective) is a [noun](docs/TERMS.md#noun): invoice status, money rounding, eligibility. Those adjectives get copied into every verb folder. Each copy looks correct. The system becomes several slightly different truths.

Object-only architecture concentrates the adjectives and hides the use-case. Agents cannot find “the work to do.” [Blast radius](docs/TERMS.md#blast-radius) becomes “the Invoice class.”

The combined shape:

- **[Noun](docs/TERMS.md#noun)** = identity, state, adjectives. The retrieval key for “how does an invoice work?”
- **Verb on the [noun](docs/TERMS.md#noun)** = a contracted mutation. The only way state changes.
- **[Goal](docs/TERMS.md#goal)** = a use-case that reaches the edge: I/O, other nouns, other goals, events, policy. It calls verbs and other goals' public entrypoints. It does not write fields.
- **[Durability](docs/TERMS.md#durability)** = a runtime property of a [goal](docs/TERMS.md#goal), not a fourth design [primitive](docs/TERMS.md#primitive). If the [goal](docs/TERMS.md#goal) must wait, retry, compensate, or take a human decision, it runs on a durable engine (Temporal or equivalent). That engine is not a peer of [noun](docs/TERMS.md#noun) / verb / [goal](docs/TERMS.md#goal).

That is the whole model. Everything else is how we keep it honest.

---

## 3. Naming

**Practice name:** [Boundary-Based Programming](docs/TERMS.md#bbp).

**Mechanism:** boundaries are enforced (contracts, privacy of fields, gates, review).

Do not name the practice “governance” or “governed.” Those words imply a committee ruling subjects. The artifacts that hold decisions are a **[charter](docs/TERMS.md#charter)** (this document, plus ADRs). The property we protect is **[integrity](docs/TERMS.md#integrity)**. The act that keeps agents honest is **adversarial review against the [charter](docs/TERMS.md#charter)**.

Useful substitutes if a slot in an older diagram said “Governance Architecture”:

| Avoid | Use |
|---|---|
| Governance | [Charter](docs/TERMS.md#charter), [integrity](docs/TERMS.md#integrity), covenant, protocol |
| Governed system | Bounded system, charter-bound system |
| Governance review | Adversarial review, [integrity](docs/TERMS.md#integrity) check |

**Boundary-Enforced Programming** is a true claim about the pipeline. It is a poor name for the practice. Put enforcement in the rules and the CI [gate](docs/TERMS.md#gate), not in the title.

Corpus tags for every published **R** / **C** / **P** id live in `integrity/rule-corpus.json` (ADR 0024): `bba` = emit shape, `nlc` = factory process.

### Id prefixes

These letters on [requirement](docs/TERMS.md#requirement) ids are not interchangeable.

| Prefix | Stands for | What it is |
|--------|------------|------------|
| **P** | Principle | How *this practice [hub](docs/TERMS.md#hub)* stays honest (P1–P7 in `integrity/PRINCIPLES.md`). |
| **R** | [Requirement](docs/TERMS.md#requirement) | A [charter](docs/TERMS.md#charter) design [rule](docs/TERMS.md#rule) the emit must obey (R1–R31). |
| **C** | Confirmation | A per-change checklist item the [confirmer](docs/TERMS.md#confirmer) scores PASS/FAIL/N/A (C1–C24). |
| **S** / **CS** | Systems / confirmation-systems | Agent-noun package structure (identity, verbs, handoff). |
| **Q** | [Quality](docs/TERMS.md#quality) | Ops/opportunities metric at a [boundary](docs/TERMS.md#boundary). |

`P-016`, `P-020` and other hyphenated **[P-0xx](docs/TERMS.md#p-0xx)** ids are *operating policies* in the companion bindings repo. They are not P1–P7.

An **R** can stand without a matching **C**. A **C** usually restates an **R** as something you can tick on *this* change.

---

## 4. Core model

### 4.1 [Noun](docs/TERMS.md#noun)

A [noun](docs/TERMS.md#noun) is a domain concept with identity and adjectives. **A [noun](docs/TERMS.md#noun) does not inherit another [noun](docs/TERMS.md#noun)** ([`adrs/0008-no-noun-inheritance.md`](adrs/0008-no-noun-inheritance.md)). Reuse is a protocol or composition via verbs. Value objects are interior data, not parent classes.


Examples: `Invoice`, `Customer`, `Order`, `PaymentAllocation`.

A [noun](docs/TERMS.md#noun) contains:

- Identity
- Private state
- Adjectives, which may carry **tags** (classification: `pan`, `pii`). A [noun](docs/TERMS.md#noun) may also carry tags (`runtime=temporal`, `pci-scope`). See [§4.7](#47-tags-primitives-and-reduced-adrs).
- A short public verb list
- Tests that [prove](docs/TERMS.md#prove) the adjectives hold after every verb

A [noun](docs/TERMS.md#noun) does **not** contain:

- HTTP, file, queue, or database adapter code
- Multi-noun orchestration
- “Send the reminder email”
- “Render the PDF”
- “Export to QuickBooks”

Those are goals, or they belong to a different [noun](docs/TERMS.md#noun).

### 4.2 Verb (on a noun)

A verb is a state change that must leave the [noun](docs/TERMS.md#noun) truthful.

Examples on `Invoice`: `issue`, `applyPayment`, `void`.

Every verb has:

- A name
- An input [contract](docs/TERMS.md#contract)
- An output [contract](docs/TERMS.md#contract) (result or error)
- Preconditions
- Postconditions / adjectives
- Tests
- **Primitives** it performs, by **calling interior functions** named in [`integrity/primitives.md`](integrity/primitives.md) ([§4.7](#47-tags-primitives-and-reduced-adrs), [ADR 0009](adrs/0009-primitive-interior-functions.md)). Those names are not public verbs. The call tree under the verb *is* the [primitive](docs/TERMS.md#primitive) inventory.


Verbs are the contracted [boundary](docs/TERMS.md#boundary) of the [noun](docs/TERMS.md#noun). There is no other public mutation path.

### 4.3 [Goal](docs/TERMS.md#goal)

A [goal](docs/TERMS.md#goal) is an executable business use-case.

Examples: `CreateInvoice`, `RecordBankPayment`, `ApproveOrder`, `GenerateYearEndReport`.

A [goal](docs/TERMS.md#goal) contains:

- Purpose
- Input / output [contract](docs/TERMS.md#contract)
- One public entrypoint
- Orchestration: load nouns, call verbs, call other goals through their public contracts, persist, publish, talk to the outside world
- Explicit dependencies
- Tests for the use-case, not for the [noun](docs/TERMS.md#noun)’s adjectives (those live on the noun)

A [goal](docs/TERMS.md#goal) does **not**:

- Assign [noun](docs/TERMS.md#noun) fields
- Reimplement [noun](docs/TERMS.md#noun) adjectives
- Become a second home for “how invoices work”

A [goal](docs/TERMS.md#goal) that only calls one noun-verb and does no I/O or policy is optional. Do not invent YAML theater for a pass-through. Expose the noun-verb. Add the [goal](docs/TERMS.md#goal) when there is orchestration to justify it.

A [goal](docs/TERMS.md#goal) may call another [goal](docs/TERMS.md#goal) only through that [goal](docs/TERMS.md#goal)'s public [contract](docs/TERMS.md#contract). The starting [goal](docs/TERMS.md#goal) owns the outcome. Callees do not grow a competing story of how the same use-case works.

### 4.4 [Durability](docs/TERMS.md#durability) (not a peer)

There is no fourth design [primitive](docs/TERMS.md#primitive) named [workflow](docs/TERMS.md#workflow).

When a [goal](docs/TERMS.md#goal) cannot finish in one process — waits, human approval, retries, compensation, or work that cannot share a single transaction — that [goal](docs/TERMS.md#goal) is durable. The durable engine (Temporal or equivalent) is how the [goal](docs/TERMS.md#goal) runs. The engine is a [noun](docs/TERMS.md#noun) tagged `runtime=temporal` (or the runtime the ADR named). A durable [goal](docs/TERMS.md#goal) may only call an engine with that [tag](docs/TERMS.md#tag) ([§4.7](#47-tags-primitives-and-reduced-adrs), [`adrs/0007-tags-primitives-reduced-adrs.md`](adrs/0007-tags-primitives-reduced-adrs.md)). The [goal](docs/TERMS.md#goal) still calls verbs and other goals' public entrypoints. Verbs still protect the [noun](docs/TERMS.md#noun).


Do not use the durable engine as a second home for a [noun](docs/TERMS.md#noun) [adjective](docs/TERMS.md#adjective). Do not maintain a hand-written execution graph that duplicates the engine's definition.

A `workflows/` folder is optional packaging for durable goals. It does not create a new kind of thing.

### 4.5 [Contract](docs/TERMS.md#contract)

A [contract](docs/TERMS.md#contract) is a machine-readable schema for a [boundary](docs/TERMS.md#boundary).

Two layers, one meaning:

1. **Noun-verb [contract](docs/TERMS.md#contract)** — canonical payload and result for `Invoice.applyPayment`.
2. **[Goal](docs/TERMS.md#goal) [contract](docs/TERMS.md#contract)** — the use-case envelope (actor, source system, idempotency key, the verb payload).

The [goal](docs/TERMS.md#goal) wraps the verb [contract](docs/TERMS.md#contract). It does not fork the meaning of `balance`, `status`, or `currency`. Shared fields come from one canonical type.

### 4.6 [Charter](docs/TERMS.md#charter) and [ADR](docs/TERMS.md#adr)

The **[charter](docs/TERMS.md#charter)** is this document plus accepted ADRs.

An **[ADR](docs/TERMS.md#adr)** records a decision that later work must not quietly undo:

- Why this [noun](docs/TERMS.md#noun) exists
- Which verbs it exposes
- Which goals may call them
- What was rejected and why

ADRs are not essays. They are decisions with consequences.

When an [ADR](docs/TERMS.md#adr) constrains emit (data policy, runtime, shape), it **reduces** to if-thens over tags, primitives, and facts. The [ADR](docs/TERMS.md#adr) remains the why. The [compiler](docs/TERMS.md#compiler) applies the rules. Ratified: [`adrs/0007-tags-primitives-reduced-adrs.md`](adrs/0007-tags-primitives-reduced-adrs.md).

### 4.7 Tags, primitives, and reduced ADRs

- **[Tag](docs/TERMS.md#tag)** — classification on an [adjective](docs/TERMS.md#adjective) or [noun](docs/TERMS.md#noun) (`pan`, `runtime=temporal`).
- **[Primitive](docs/TERMS.md#primitive)** — closed interior function names in [`integrity/primitives.md`](integrity/primitives.md) (`read`, `write`, `return`, `log`, …). Not public verbs. New [primitive](docs/TERMS.md#primitive) = [ADR](docs/TERMS.md#adr). Call-tree inventory is the [audit](docs/TERMS.md#audit) point ([ADR 0009](adrs/0009-primitive-interior-functions.md)).
- **[Rule](docs/TERMS.md#rule)** — `if tags ∧ primitives ∧ facts → must | forbid`.
- Verbs call [primitive](docs/TERMS.md#primitive) functions; a body that does `write`-work without calling `write` fails (default closed).
- Prefer a new [tag](docs/TERMS.md#tag) or fact before a new [primitive](docs/TERMS.md#primitive). Temporal is `goal.durable ∧ engine.runtime ≠ temporal → forbid`, not a special parser.
- v1 `taint.txt` is the stand-in for tags on sensitive adjectives (R32). A rule-IR [gate](docs/TERMS.md#gate) is not in force yet; do not mint an **R** id until it is bindable (R27).



---

## 5. Rules

Rules are written so an implementing agent can confirm or fail them. “Should” is not a [rule](docs/TERMS.md#rule).

### 5.1 Ownership

**R1.** If breaking the [rule](docs/TERMS.md#rule) would make *this [noun](docs/TERMS.md#noun)* a lie, the [rule](docs/TERMS.md#rule) lives on the [noun](docs/TERMS.md#noun), as an [adjective](docs/TERMS.md#adjective) or as a verb precondition/postcondition.

**R2.** If the work spans nouns, I/O, other goals, or a business outcome, it is a [goal](docs/TERMS.md#goal).

**R3.** Cross-noun work does not get glued onto the most convenient [noun](docs/TERMS.md#noun). `allocatePaymentToInvoices` is a [goal](docs/TERMS.md#goal), or a `PaymentAllocation` [noun](docs/TERMS.md#noun) if it has its own adjectives. It is not `Invoice.allocateAcrossFriends`.

**R4.** If a verb does not need the [noun](docs/TERMS.md#noun)’s [adjective](docs/TERMS.md#adjective) set, it does not belong on the [noun](docs/TERMS.md#noun).

### 5.2 Mutation

**R5.** [Noun](docs/TERMS.md#noun) fields are private. No [goal](docs/TERMS.md#goal), adapter, or other [noun](docs/TERMS.md#noun) writes them.

**R6.** The only legal mutation of a [noun](docs/TERMS.md#noun) is a public verb on that [noun](docs/TERMS.md#noun).

**R7.** Nouns never call goals. Direction is [goal](docs/TERMS.md#goal) → (goal public entrypoint | noun-verb) plus explicit reads. A durable engine may host a [goal](docs/TERMS.md#goal); it is not a caller above the [goal](docs/TERMS.md#goal) layer.

**R8.** Goals may read what the [noun](docs/TERMS.md#noun) chooses to expose (queries / snapshots). Goals may not reach through that snapshot and write.

### 5.3 Contracts

**R9.** Every public [goal](docs/TERMS.md#goal) entrypoint has an input [contract](docs/TERMS.md#contract) and an output [contract](docs/TERMS.md#contract).

**R10.** Every public noun-verb has an input [contract](docs/TERMS.md#contract) and an output [contract](docs/TERMS.md#contract).

**R11.** A field that means the same thing in two contracts is defined once and referenced. Duplicate independent definitions of the same meaning are a [defect](docs/TERMS.md#defect).

**R12.** Contracts are versioned. Breaking changes require a new version and an [ADR](docs/TERMS.md#adr).

### 5.4 [Goal](docs/TERMS.md#goal) shape

**R13.** One public entrypoint per [goal](docs/TERMS.md#goal).

**R14.** A [goal](docs/TERMS.md#goal) may call another [goal](docs/TERMS.md#goal) only through that [goal](docs/TERMS.md#goal)'s public entrypoint and [contract](docs/TERMS.md#contract). [Goal](docs/TERMS.md#goal) internals are not importable. If two goals need the same fragment, extract a noun-verb, a shared library with its own [contract](docs/TERMS.md#contract), or a smaller [goal](docs/TERMS.md#goal) with its own public [contract](docs/TERMS.md#contract).

**R15.** Shared domain logic that protects a [noun](docs/TERMS.md#noun) lives on the [noun](docs/TERMS.md#noun), not in a helper copied into two goals.

**R16.** A new [goal](docs/TERMS.md#goal) is created only when there is a distinct use-case. Do not create a [goal](docs/TERMS.md#goal) per function (`ValidateEmail` as a sibling of `CreateCustomer` unless it is a real standalone capability).

### 5.5 [Goal](docs/TERMS.md#goal) composition and [durability](docs/TERMS.md#durability)

**R17.** Goals may call goals through public contracts. There is no separate [workflow](docs/TERMS.md#workflow) citizen. A durable runtime hosts a [goal](docs/TERMS.md#goal); it does not replace the [goal](docs/TERMS.md#goal).

**R18.** Compensation and retries live in the calling [goal](docs/TERMS.md#goal) (and its runtime if durable), not inside the [noun](docs/TERMS.md#noun), unless the [noun](docs/TERMS.md#noun)'s [adjective](docs/TERMS.md#adjective) itself requires idempotency of a verb. Verbs must be safe to retry if a durable [goal](docs/TERMS.md#goal) retries them. Declare that on the verb.

**R19.** Do not maintain a separate hand-authored execution-graph file that duplicates a durable [goal](docs/TERMS.md#goal)'s runtime definition.

### 5.6 Knowledge and drift

**R20.** The [charter](docs/TERMS.md#charter), contracts, and code must agree. If they disagree, the build fails. Code does not win by existing. Spec does not win by being newer. They must be reconciled in the same change.

**R21.** Dependency and impact information is generated from code and contracts, not authored as a parallel JSON document. The [binding matrix](docs/TERMS.md#binding-matrix) is the [requirement](docs/TERMS.md#requirement) index for this practice [hub](docs/TERMS.md#hub) (requirement → audit → gate); it is not a dependency or impact graph, and R21 applies to generated “what breaks” views in adopting codebases, not to that matrix.

**R22.** ADRs that are superseded are marked superseded, not deleted. The trail is part of [integrity](docs/TERMS.md#integrity).

### 5.7 Enforcement

**R23.** A [gate](docs/TERMS.md#gate) fails the change if a [goal](docs/TERMS.md#goal) or adapter assigns a [noun](docs/TERMS.md#noun) field or imports a [noun](docs/TERMS.md#noun) internals module.

**R24.** A [gate](docs/TERMS.md#gate) fails the change if invoice-equivalent money math, status transitions, or named adjectives appear outside the owning [noun](docs/TERMS.md#noun) (copy-paste of the adjective).

**R25.** Tests for a [noun](docs/TERMS.md#noun)’s adjectives live next to the [noun](docs/TERMS.md#noun) and run on every verb. [Goal](docs/TERMS.md#goal) tests do not replace them.

**R32.** A sensitive [adjective](docs/TERMS.md#adjective) listed in `taint.txt` may cross one [boundary](docs/TERMS.md#boundary): the consuming verb. It is not returned, stored on another object, or passed to another [boundary](docs/TERMS.md#boundary).

**R33.** [Noun](docs/TERMS.md#noun) state is not mutated through non-OO escape hatches (`__dict__`, `vars()`, `exec()`, `eval()`, or equivalent reflection) from outside a published verb.

### 5.8 Practice [integrity](docs/TERMS.md#integrity) (zero variance)


Ratified by [`adrs/0001-zero-variance-integrity.md`](adrs/0001-zero-variance-integrity.md). P2 scope: [`adrs/0002-p2-scope.md`](adrs/0002-p2-scope.md). Detail: [`integrity/PRINCIPLES.md`](integrity/PRINCIPLES.md). Matrix: [`integrity/binding-matrix.json`](integrity/binding-matrix.json).

**R26.** Practice [integrity](docs/TERMS.md#integrity) principles P1–P7 are in force: stand-alone branding, [zero variance](docs/TERMS.md#zero-variance), and [binding](docs/TERMS.md#binding) of every published rule to a [gate](docs/TERMS.md#gate).

**R27.** No published **R** id exists without a binder in this repo. A rule without a gate is a wish, not a rule.

**R28.** The [hub](docs/TERMS.md#hub) does not ship product requirements; it ships the compiler and its gates ([ADR 0016](adrs/0016-hub-no-product-requirements.md)).

**R29.** Every [gate](docs/TERMS.md#gate) is default-closed: it starts NOT_MET and only becomes MET when its evidence is present.

**R30.** [Fitness](docs/TERMS.md#fitness) output is machine-readable and stable enough for agents to act on without parsing prose.

**R31.** The [hub](docs/TERMS.md#hub) is the only place that may change the [charter](docs/TERMS.md#charter), ADRs, or rules. Adopter repos consume; they do not author.

---

## 6. Confirmation checklist

Score each item PASS / FAIL / N/A for *this* change. N/A requires a one-line reason.

### 6.1 Ownership and mutation

**C1.** The change touches only the [noun](docs/TERMS.md#noun) or [goal](docs/TERMS.md#goal) it claims to.
**C2.** No [noun](docs/TERMS.md#noun) field is assigned outside a published verb.
**C3.** No [goal](docs/TERMS.md#goal) writes a [noun](docs/TERMS.md#noun) field.
**C4.** No copied [adjective](docs/TERMS.md#adjective) — the same meaning defined in two places.
**C5.** Verbs call [primitive](docs/TERMS.md#primitive) interior functions; no raw `write` outside them.

### 6.2 Contracts

**C6.** Every public entrypoint has an input and output [contract](docs/TERMS.md#contract).
**C7.** Shared fields come from one canonical type.
**C8.** Breaking [contract](docs/TERMS.md#contract) change has a new version and an [ADR](docs/TERMS.md#adr).

### 6.3 [Goal](docs/TERMS.md#goal) shape

**C9.** One public entrypoint per [goal](docs/TERMS.md#goal).
**C10.** [Goal](docs/TERMS.md#goal) calls [goal](docs/TERMS.md#goal) only through public contracts.
**C11.** No pass-through [goal](docs/TERMS.md#goal) theater.
**C12.** [Goal](docs/TERMS.md#goal) tests cover the use-case, not the [noun](docs/TERMS.md#noun) adjectives.

### 6.4 Drift and enforcement

**C13.** [Charter](docs/TERMS.md#charter), contracts, and code agree in this change.
**C14.** No superseded [ADR](docs/TERMS.md#adr) is treated as live.
**C15.** No [gate](docs/TERMS.md#gate) is skipped or soft-green.
**C16.** [Fitness](docs/TERMS.md#fitness) output is present and parseable.
**C17.** The change is [ratified](docs/TERMS.md#ratified-by) when its class requires it.
**C18.** The change is [released](docs/TERMS.md#released-by) by a human when required.
**C19.** No agent acts as releaser.
**C20.** Adversarial review ran and findings are addressed or rebutted.
**C21.** [Binding matrix](docs/TERMS.md#binding-matrix) row for touched rules is updated.
**C22.** No new [primitive](docs/TERMS.md#primitive) without an [ADR](docs/TERMS.md#adr).
**C23.** Sensitive [adjective](docs/TERMS.md#adjective) crossing is limited to the consuming verb.
**C24.** Release audit refuses agent-as-releaser.

---

## 7. Ratification

Ratified decisions: [0001](adrs/0001-zero-variance-integrity.md), [0002](adrs/0002-p2-scope.md), [0003](adrs/0003-agent-nouns.md), [0007](adrs/0007-tags-primitives-reduced-adrs.md), [0008](adrs/0008-no-noun-inheritance.md), [0009](adrs/0009-primitive-interior-functions.md), [0010](adrs/0010-gate-after-generate.md).

---

*End of charter. The [binding matrix](integrity/binding-matrix.json) is the machine index of these rules.*
