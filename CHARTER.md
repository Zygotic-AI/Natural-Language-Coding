# [Natural Language Coding](docs/TERMS.md#nlc) — charter (BBP emit + integrity under the roof)

**Product / consumer roof = [Natural Language Coding (NLC)](docs/TERMS.md#nlc)** ([ADR 0011](adrs/0011-natural-language-coding-naming.md)).
This document is the **[Boundary-Based Programming](docs/TERMS.md#bbp) (BBP)** emit + integrity doctrine **under that roof**.
**[BBA](docs/TERMS.md#bba)** is under-covers integrity architecture, not the public product name.

---

# [Boundary-Based Programming](docs/TERMS.md#bbp) — emit + integrity practice

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

**Practice name (under NLC roof):** [Boundary-Based Programming](docs/TERMS.md#bbp) — emit + integrity. **Product roof:** [Natural Language Coding](docs/TERMS.md#nlc) ([ADR 0011](adrs/0011-natural-language-coding-naming.md)).

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

**R26.** Practice [integrity](docs/TERMS.md#integrity) principles P1–P7 are in force: stand-alone branding, [zero variance](docs/TERMS.md#zero-variance), hard gates, hard [boundary](docs/TERMS.md#boundary) I/O, binary [requirement](docs/TERMS.md#requirement) audits, unbound-matrix failure with listing, promote-only-when-bindable with listing.

**R27.** Every published [requirement](docs/TERMS.md#requirement) in this repo appears in the [binding matrix](docs/TERMS.md#binding-matrix) with an [audit](docs/TERMS.md#audit) id. [Audit](docs/TERMS.md#audit) `A-BINDING-COVERAGE` fails and lists any missing id.

**R28.** Unbound binding-matrix entries fail [audit](docs/TERMS.md#audit) `A-BINDING-UNBOUND`. The [audit](docs/TERMS.md#audit) report lists every unbound [requirement](docs/TERMS.md#requirement) id.

**R29.** In-force requirements that are not bindable fail [audit](docs/TERMS.md#audit) `A-BINDING-PROMOTE`. The [audit](docs/TERMS.md#audit) report lists every offending [requirement](docs/TERMS.md#requirement) id.

**R30.** Every prescribed step or [action](docs/TERMS.md#action) has a hard [gate](docs/TERMS.md#gate) whose only outcomes are complete or incomplete, with evidence.

**R31.** Every public [boundary](docs/TERMS.md#boundary) declares hard input, hard output, and failure mode (returned error, thrown exception, or process exit when the boundary is code).

---

## 6. Order of agent execution

This is the default loop for design and code. Skip a step only when an [ADR](docs/TERMS.md#adr) says that class of change is exempt (for example, a one-line copy fix inside an already-ratified verb).

```text
0. Load charter
1. Classify the change
2. Propose
3. Adversarial review
4. Revise
5. Ratify
6. Implement
7. Confirm
8. Record
```

### Step 0 — Load [charter](docs/TERMS.md#charter)

Read this document and the ADRs that touch the nouns and goals in scope. If the change would violate a [rule](docs/TERMS.md#rule), stop and propose an [ADR](docs/TERMS.md#adr) first.

### Step 1 — Classify the change

Choose exactly one primary class:

| Class | You are changing | Home of the work |
|---|---|---|
| A. [Adjective](docs/TERMS.md#adjective) | Status machine, money, eligibility | [Noun](docs/TERMS.md#noun) + its verbs |
| B. Mutation API | Add/change a verb | Noun-verb [contract](docs/TERMS.md#contract) + [noun](docs/TERMS.md#noun) tests |
| C. Use-case | Orchestration, I/O, policy around existing verbs | [Goal](docs/TERMS.md#goal) |
| D. Durable use-case | Time, approval, compensation across goals | [Goal](docs/TERMS.md#goal) + durable runtime |
| E. [Boundary](docs/TERMS.md#boundary) meaning | Shared field meaning, version, compatibility | Canonical [contract](docs/TERMS.md#contract) + [ADR](docs/TERMS.md#adr) |
| F. [Charter](docs/TERMS.md#charter) | A [rule](docs/TERMS.md#rule) in this document | [ADR](docs/TERMS.md#adr) first, then this file |

If the request is “change how invoices work,” it is class A, not class C. Open the [noun](docs/TERMS.md#noun). Do not open one [goal](docs/TERMS.md#goal) and improvise.

### Step 2 — Propose (spec, not code)

The proposing agent produces, in one change-set of documents:

- Classification (A–F)
- Nouns touched, verbs touched, goals touched, durable goals named
- Draft contracts if any [boundary](docs/TERMS.md#boundary) changes
- Adjectives that must still hold
- Explicit non-goals (“this does not change tax rounding”)
- Test names that will [prove](docs/TERMS.md#prove) it
- Impact list: other goals/verbs that call the changed [boundary](docs/TERMS.md#boundary)

No implementation in this step unless the change is already classified as exempt.

**[Produce package](docs/TERMS.md#produce-package) required for [handoff](docs/TERMS.md#handoff).** Proposal completion includes the [produce package](docs/TERMS.md#produce-package): classification (plan A–F as above), applicability statement, [boundary](docs/TERMS.md#boundary) I/O declarations, self-adversarial notes, and task/board [SSOT exit evidence](docs/TERMS.md#ssot-exit-evidence) (`ssot_leaf_ids` + `ssot_exit_status`). A proposal without this package is incomplete. Incomplete proposals do not hand off to fitness or adversarial review.

### Step 2.5 — Fitness preflight

Before adversarial review opens, fitness performs a preflight check:

- **Package present and complete** → proceed to Step 3.
- **Package missing or incomplete** → return `handoff_refused` with [defect](docs/TERMS.md#defect) log. Do not open content scoring. The proposal is not fitness-FAIL; it is produce-incomplete.

Preflight is not discovery. Fitness does not invent the package, coach the producer, or soft-fail to prompt remediation. The producer fixes the package and resubmits. Do not normalize "re-gate" for missing-package rework.

### Step 3 — Adversarial review

A second agent, with a different role, attacks the proposal. It does not implement. It does not protect the author’s feelings. It answers only:

- Where can a [goal](docs/TERMS.md#goal) now write private state?
- Which [adjective](docs/TERMS.md#adjective) is now split across two homes?
- Which [contract](docs/TERMS.md#contract) field is defined twice with room to drift?
- Is this a [god-noun](docs/TERMS.md#god-noun) collecting verbs it should not own?
- Is this a new [goal](docs/TERMS.md#goal) that should have been a noun-verb?
- Is this a noun-verb that should have been a [goal](docs/TERMS.md#goal)?
- What breaks if this verb is retried?
- What did the impact list miss?

Findings are comments against the proposal. “Looks good” with no checklist is not a review.

### Step 4 — Revise

The proposing agent answers every finding: fix, or record why the finding is wrong. Unresolved findings block ratification.

### Step 5 — Ratify

A human, or an automated [gate](docs/TERMS.md#gate) whose policy an [ADR](docs/TERMS.md#adr) named, accepts the proposal. Ratification is a recorded event: who, when, which proposal version.

Until ratification, implementation is not authorized for class A, B, D, E, or F. Class C may be tightened by [ADR](docs/TERMS.md#adr) for a given repo (some teams ratify every new goal; some do not).

### Step 6 — Implement

Code follows the ratified spec.

- [Noun](docs/TERMS.md#noun) internals stay inside the [noun](docs/TERMS.md#noun) module.
- Goals call verbs and other goals' public entrypoints. Goals never write [noun](docs/TERMS.md#noun) fields.
- Contracts generate or validate I/O.
- Tests named in the proposal are written and pass.

### Step 7 — Confirm

Run the [Confirmation checklist](#confirmation-checklist). Any fail is a failed change, not a note for later.

### Step 8 — Record

- Update or add the [ADR](docs/TERMS.md#adr) if a decision was made.
- Leave the generated impact/dependency view in the state the tooling produces.
- Do not write a parallel “architecture JSON” by hand.

---

## 7. Agent roles

Separate roles. One model may play them in sequence, but not in the same pass as both author and skeptic of its own work.

| Role | Allowed to do | Not allowed to do |
|---|---|---|
| Proposer | Draft spec, then implement after ratification | Grade its own proposal as final |
| Reviewer | Attack the spec and the diff against this [charter](docs/TERMS.md#charter) | Write the implementation in the same turn |
| [Confirmer](docs/TERMS.md#confirmer) | Run checklist, report pass/fail with evidence | “Approve” without evidence |
| Recorder | Write ADRs and status | Change rules without an [ADR](docs/TERMS.md#adr) |

The reviewer prompt is: you are the skeptic. Find the hole. Cite the [rule](docs/TERMS.md#rule) number.

---

## 8. Repository shape

Suggested layout. Adapt names; keep the separations.

```text
repo/
├─ CHARTER.md                          # this document, or a pointer to it
├─ adrs/
│   ├─ 0001-boundary-based-programming.md
│   └─ 0002-invoice-verbs.md
├─ domain/
│   └─ invoice/
│       ├─ invoice.ts                  # noun, private state
│       ├─ verbs/
│       │   ├─ issue.ts
│       │   ├─ apply-payment.ts
│       │   └─ void.ts
│       ├─ contracts/                  # canonical verb schemas
│       └─ tests/
├─ goals/
│   └─ record-bank-payment/
│       ├─ goal.yaml                   # purpose, owner, entrypoint, deps
│       ├─ contract-input.json
│       ├─ contract-output.json
│       ├─ implementation/
│       └─ tests/
├─ workflows/                          # optional packaging for durable goals; not a fourth primitive
│   └─ collect-invoice-payment/
├─ contracts-shared/                   # canonical types referenced by both layers
└─ integrity/
    ├─ fitness/                        # lint/arch rules
    └─ checklist.md                    # or generate from this document
```

`capabilities/` as a second tree is optional. Do not add `governance/`, `compliance/`, `risk/` folders unless a real artifact has nowhere else to live. Empty architecture folders are how charters rot.

---

## 9. What we took from the original “AI-First” sketch — and what we did not

The original sketch was right about:

- Organize work so agents have a small, named unit of change
- Machine-readable contracts on boundaries
- Explicit dependencies aimed at “if I change X, what breaks?”
- Co-located tests
- ADRs as recorded decisions
- Validation as proof, not prose

The original sketch was weak where it:

- Named thirty “architectures” as peer systems
- Treated security, data, observability, [audit](docs/TERMS.md#audit), and evidence as sibling trees instead of annotations on nouns, verbs, and goals
- Put Agent concerns in a later tier even though agents are the primary consumer
- Assumed hand-maintained `dependency-graph.json` and `impact-analysis.json`
- Isolated goals without a [noun](docs/TERMS.md#noun), which scatters adjectives and invites duplication
- Used “governance” as a bucket instead of a [charter](docs/TERMS.md#charter) plus review

Those higher-level views (product, portfolio, strategy) can be derived later. They are not the foundation agents implement against.

---

## 10. Pitfalls and remediations

### 10.1 Scattered adjectives

**Pitfall.** “Cannot void after payment” lives in `VoidInvoice` and a slightly different version lives in `ApplyPayment`. An agent edits one.

**Remediation.** The [adjective](docs/TERMS.md#adjective) lives on `Invoice`. Both verbs consult it. [Goal](docs/TERMS.md#goal) tests are not the home of the [adjective](docs/TERMS.md#adjective). [Gate](docs/TERMS.md#gate) fails if the status machine is reimplemented in a [goal](docs/TERMS.md#goal).

### 10.2 Duplication that looks locally correct

**Pitfall.** The agent’s context is the current [goal](docs/TERMS.md#goal). It reimplements tax rounding. CI on that [goal](docs/TERMS.md#goal) is green.

**Remediation.** R15 and R24. Money math has one module. Reviewer asks “where else does this formula exist?” [Confirmer](docs/TERMS.md#confirmer) greps.

### 10.3 Conceptual changes treated as [goal](docs/TERMS.md#goal) changes

**Pitfall.** “Allow partial payments” is implemented only in `ApplyPayment` the [goal](docs/TERMS.md#goal). `VoidInvoice` still assumes full-payment status values.

**Remediation.** Classification step. Conceptual change is class A. Proposer must open the [noun](docs/TERMS.md#noun) and list every verb that assumes the old [adjective](docs/TERMS.md#adjective).

### 10.4 Hidden coupling through shared data

**Pitfall.** Goals look independent. They write the same row. The call graph does not show that `status` means two things.

**Remediation.** Only verbs write. Generated impact includes “who calls this verb,” not only “which [goal](docs/TERMS.md#goal) folder changed.” Shared tables are behind the [noun](docs/TERMS.md#noun)’s persistence adapter, not open to every [goal](docs/TERMS.md#goal).

### 10.5 [Goal](docs/TERMS.md#goal) explosion or god-goal

**Pitfall.** One function per [goal](docs/TERMS.md#goal), or one [goal](docs/TERMS.md#goal) that does the entire billing domain.

**Remediation.** R16 and the pass-through [rule](docs/TERMS.md#rule). Reviewer flags both. Sizing heuristic: a [goal](docs/TERMS.md#goal) names a use-case a stakeholder would recognize; a verb names a state change the [noun](docs/TERMS.md#noun) must survive.

### 10.6 [God-noun](docs/TERMS.md#god-noun)

**Pitfall.** `Invoice.renderPdf`, `Invoice.sendReminder`, `Invoice.exportQuickBooks`.

**Remediation.** R4. If the verb does not need the [adjective](docs/TERMS.md#adjective) set, it is a [goal](docs/TERMS.md#goal) or another [noun](docs/TERMS.md#noun). Reviewer checklist includes [god-noun](docs/TERMS.md#god-noun).

### 10.7 Two [contract](docs/TERMS.md#contract) layers that drift

**Pitfall.** [Goal](docs/TERMS.md#goal) input defines `balance` one way. Verb input defines it another.

**Remediation.** R11. Canonical type. [Goal](docs/TERMS.md#goal) [contract](docs/TERMS.md#contract) references it. [Confirmer](docs/TERMS.md#confirmer) diffs schemas for same-named fields with different types.

### 10.8 Hand-maintained graphs that lie

**Pitfall.** `dependency-graph.json` is stale. Agents trust it.

**Remediation.** R21. Generate from imports, durable-goal definitions, and registered verb calls. If it cannot be generated, do not pretend the file is a source of truth.

### 10.9 Convention without enforcement

**Pitfall.** “Internals are private” is a README sentence. The third agent session writes `invoice.status = 'paid'` from a [goal](docs/TERMS.md#goal).

**Remediation.** R5, R6, R23. Language visibility, module boundaries, and a CI [rule](docs/TERMS.md#rule). Convention is not a [boundary](docs/TERMS.md#boundary).

### 10.10 Author grades its own homework

**Pitfall.** The same pass proposes and approves.

**Remediation.** Step 3 as a separate role. Review with [rule](docs/TERMS.md#rule) numbers. “Looks good” is not evidence.

### 10.11 [Durability](docs/TERMS.md#durability) as a second domain model

**Pitfall.** A Temporal definition re-implements “when an invoice is paid” instead of calling `applyPayment`, or a new [goal](docs/TERMS.md#goal) is invented only to wrap one other [goal](docs/TERMS.md#goal).

**Remediation.** R14, R16–R18. Goals call public contracts. Verbs keep the [adjective](docs/TERMS.md#adjective). The starting [goal](docs/TERMS.md#goal) owns the outcome. Reviewer asks where the status machine lives and whether the extra [goal](docs/TERMS.md#goal) earns its keep.

---

## 11. Confirmation checklist

An implementing agent must print this list with `PASS`, `FAIL`, or `N/A` and a pointer (file and symbol) for every non-N/A item. `N/A` requires a one-line reason.

### Classification and home

- [ ] C1. [Change class](docs/TERMS.md#change-class) (A–F) is stated.
- [ ] C2. Adjectives live on the [noun](docs/TERMS.md#noun) named in C1, not in a [goal](docs/TERMS.md#goal) folder.
- [ ] C3. New orchestration lives in a [goal](docs/TERMS.md#goal), not as a method on an unrelated [noun](docs/TERMS.md#noun).

### Mutation path

- [ ] C4. No assignment to [noun](docs/TERMS.md#noun) fields occurs outside the [noun](docs/TERMS.md#noun) module.
- [ ] C5. Every state change of a [noun](docs/TERMS.md#noun) goes through a public verb.
- [ ] C6. No [noun](docs/TERMS.md#noun) module imports a [goal](docs/TERMS.md#goal) module.

### Contracts

- [ ] C7. Each changed public [goal](docs/TERMS.md#goal) has input and output schemas.
- [ ] C8. Each changed public verb has input and output schemas.
- [ ] C9. Shared meanings use a shared type; no forked `balance` / `status` / `currency`.
- [ ] C10. Breaking schema changes have a new version and an [ADR](docs/TERMS.md#adr).

### [Goal](docs/TERMS.md#goal) shape

- [ ] C11. Each changed [goal](docs/TERMS.md#goal) has exactly one public entrypoint.
- [ ] C12. No [goal](docs/TERMS.md#goal) imports another [goal](docs/TERMS.md#goal)’s internals.
- [ ] C13. No new [goal](docs/TERMS.md#goal) exists whose only job is a single noun-verb with no I/O or policy — or an [ADR](docs/TERMS.md#adr) explains why the wrapper exists.
- [ ] C14. Goal-to-goal calls use public entrypoints only; no imports of another [goal](docs/TERMS.md#goal)'s internals.
- [ ] C15. Verbs invoked from a retrying (durable) [goal](docs/TERMS.md#goal) are idempotent, or the caller uses an idempotency key the verb honors.

### Adjectives and tests

- [ ] C16. Every [adjective](docs/TERMS.md#adjective) named in the proposal has a test on the [noun](docs/TERMS.md#noun).
- [ ] C17. Every new verb has tests for success, precondition failure, and [adjective](docs/TERMS.md#adjective) preservation.
- [ ] C18. [Goal](docs/TERMS.md#goal) tests cover the use-case, not a copy of the [noun](docs/TERMS.md#noun)’s [adjective](docs/TERMS.md#adjective) suite.
- [ ] C19. No second implementation of the same [adjective](docs/TERMS.md#adjective) exists in the diff (search for duplicated predicates).
- [ ] C25. Sensitive adjectives fetched in a unit are not returned, stored, or passed across another [boundary](docs/TERMS.md#boundary).
- [ ] C26. No `__dict__` / `vars()` / `exec()` / `eval()` (or equivalent) mutates [noun](docs/TERMS.md#noun) state from outside a published verb.

### [Integrity](docs/TERMS.md#integrity) of the change


- [ ] C20. Fitness / lint rules for R23 and R24 passed.
- [ ] C21. Impact list in the proposal matches generated callers of the changed verbs/goals.
- [ ] C22. Charter/ADR/code/contracts were updated in the same change if they were affected.
- [ ] C23. Adversarial review findings are all fixed or explicitly rebutted.
- [ ] C24. Ratification is recorded for classes that require it.

If C4, C5, C9, C16, C19, C20, C25, or C26 fail, the change is not complete.


---

## 12. Minimal gates to install

These are the smallest enforcement set. Language-specific tools vary (module visibility, ESLint boundaries, ArchUnit, import-linter, custom grep in CI). The check must fail the build, not warn.

1. **No field writes across the [noun](docs/TERMS.md#noun) [boundary](docs/TERMS.md#boundary).** [Goal](docs/TERMS.md#goal) and adapter packages cannot assign [noun](docs/TERMS.md#noun) fields.
2. **No imports of [noun](docs/TERMS.md#noun) internals.** Only the [noun](docs/TERMS.md#noun)’s public verb module is importable.
3. **No imports of [goal](docs/TERMS.md#goal) internals from another [goal](docs/TERMS.md#goal).**
4. **[Adjective](docs/TERMS.md#adjective) locality.** A denylist of [adjective](docs/TERMS.md#adjective) identifiers or modules (status transition tables, rounding functions) that may only appear under `domain/<noun>/`.
5. **[Contract](docs/TERMS.md#contract) presence.** A public entrypoint without a schema file (or generated schema) fails CI.
6. **Schema identity.** Same property name + different type across contracts in one change fails CI or a review bot.

Until [gate](docs/TERMS.md#gate) 1 exists, the [charter](docs/TERMS.md#charter) is not in force. Start there.

---

## 13. Mapping to things that already exist

Use these; do not reimplement them under new folder names.

| Need | Existing tool or pattern |
|---|---|
| [Noun](docs/TERMS.md#noun) + adjective-preserving verbs | DDD aggregate; methods or typed commands on the aggregate |
| Typed mutation contracts on the [noun](docs/TERMS.md#noun) | Axon commands; Orleans / actor grain interface; Design by [Contract](docs/TERMS.md#contract) |
| [Goal](docs/TERMS.md#goal) as use-case folder | Vertical slice; Clean Architecture handler / MediatR command |
| Module privacy enforced in CI | Spring Modulith + ArchUnit; ESLint boundaries; import-linter |
| Durable multi-goal execution | Temporal (or equivalent) workflows |
| Design-first I/O contracts | JSON Schema / Zod / TypeBox; OpenAPI; Smithy; Goa |
| Generated “what breaks” at package grain | Nx project graph / `affected`; language import graph |
| Recorded decisions | ADRs |
| Drift as a merge failure | [Contract](docs/TERMS.md#contract) tests (Pact, schemathesis); spec-code [gate](docs/TERMS.md#gate) |

No single downloaded framework is “[Boundary-Based Programming](docs/TERMS.md#bbp).” The assembly is: [noun](docs/TERMS.md#noun) module with private state, verb contracts, [goal](docs/TERMS.md#goal) folders, durable runtime if needed, generated graphs, gates, [ADR](docs/TERMS.md#adr) [charter](docs/TERMS.md#charter), two-role review.

In Node, that assembly is typically: domain class + private fields, Zod or TypeBox as verb and [goal](docs/TERMS.md#goal) contracts, one handler file per [goal](docs/TERMS.md#goal), Temporal for multi-noun time, lint/import rules that fail when a [goal](docs/TERMS.md#goal) touches [noun](docs/TERMS.md#noun) internals.

---

## 14. What “done” means for adopting this

A codebase has adopted [Boundary-Based Programming](docs/TERMS.md#bbp) when all of the following are true:

1. This [charter](docs/TERMS.md#charter) (or a dated descendant) is in the repo.
2. At least one real [noun](docs/TERMS.md#noun) has private state and contracted verbs.
3. At least one real [goal](docs/TERMS.md#goal) calls those verbs and does not write fields.
4. [Gate](docs/TERMS.md#gate) 1 from section 12 fails a deliberate violation in CI.
5. The agent loop in section 6 is the written procedure for class A and B changes.
6. An implementing agent can run section 11 and produce evidence, not vibes.

Until item 4 is true, treat the rest as a style guide.

---

## 15. Short form for an agent system prompt

You may paste this block into an agent. The rest of this file remains authoritative.

```text
You practice Boundary-Based Programming.

Nouns own identity, private state, and adjectives.
The only legal mutation of a noun is a public verb with an input/output contract.
Goals orchestrate: I/O, other nouns, other goals, events, policy. Goals call verbs and other goals' public entrypoints. Goals never assign noun fields.
Durability is how a goal runs when one process is not enough. It is not a fourth primitive. Durable goals still do not reimplement noun adjectives.
Shared meaning lives in one canonical type. Do not fork balance, status, or currency.
If a change is about how a concept works, open the noun, not a single goal.
Propose spec first. A separate reviewer pass attacks the spec against the charter rules.
Do not approve your own proposal in the same pass.
Confirm with the checklist: private fields, verb-only writes, contract presence, adjective tests on the noun, no duplicated adjectives, gates green.
If charter, contracts, and code disagree, stop and reconcile them in one change.
```

---

## 16. Systems model — [agent nouns](docs/TERMS.md#agent-noun)

Ratified by [`adrs/0003-systems-extension-agent-nouns.md`](adrs/0003-systems-extension-agent-nouns.md).

The software model (§4) organizes code so agents can change it without scattering adjectives. The same structural discipline organizes **agent fleets** — durable roles that operate a system over time.

### 16.1 Vocabulary mapping

| Software [BBP](docs/TERMS.md#bbp) | Systems [BBP](docs/TERMS.md#bbp) |
|--------------|-------------|
| [Noun](docs/TERMS.md#noun) | [Agent noun](docs/TERMS.md#agent-noun) — durable role with identity and adjectives |
| [Verb (on noun)](docs/TERMS.md#verb-on-noun) | Verb — legal function an agent may perform; contracted I/O |
| [Goal](docs/TERMS.md#goal) | Use-case — orchestration across [agent nouns](docs/TERMS.md#agent-noun), other goals, or the outside world |
| [Durability](docs/TERMS.md#durability) | Runtime property of a [goal](docs/TERMS.md#goal) — not a separate citizen |
| [Contract](docs/TERMS.md#contract) | [Boundary artifact](docs/TERMS.md#boundary-artifact) — input, output, failure mode, [handoff](docs/TERMS.md#handoff), completion |
| [Adjective](docs/TERMS.md#adjective) | Role [adjective](docs/TERMS.md#adjective) — what the agent must never violate |
| [Gate](docs/TERMS.md#gate) | [Gate](docs/TERMS.md#gate) — automated enforcement; binary pass/fail; CI-bound |
| Adversarial review | [Audit](docs/TERMS.md#audit) — role-based review against [charter](docs/TERMS.md#charter); produces findings |

**[Gate](docs/TERMS.md#gate) ≠ [Audit](docs/TERMS.md#audit).** Gates are automated enforcement mechanisms (gates, CI rules) that fail the build. Audits are role-based adversarial reviews (adversarial-auditor agent noun) that produce findings for a [ship](docs/TERMS.md#ship) decision. Both yield binary outcomes (ops vs defects), but differ in mechanism and authority:
- Gates block automatically; no human or role decides.
- Audits produce findings; a ship-role or human decides whether findings block.

For the formal [Gate](docs/TERMS.md#gate) definition, all-required PASS fitness bar (G1--G4), and design rules, see [`integrity/GATE.md`](integrity/GATE.md).

**[Handoff refused](docs/TERMS.md#handoff_refused) ≠ fitness FAIL.** When fitness preflight returns `handoff_refused` (produce package missing/incomplete), that is not a fitness FAIL. It is a produce-incomplete signal. The [Gate](docs/TERMS.md#gate) remains the CI enforcement point for fitness scoring; preflight refusal is upstream of [Gate](docs/TERMS.md#gate). Do not normalize "re-gate" language for missing-package rework — that masks the produce-handoff [defect](docs/TERMS.md#defect).

### 16.2 [Agent noun](docs/TERMS.md#agent-noun) structure

Every [agent noun](docs/TERMS.md#agent-noun) package (under `agents/<name>/`) declares:

| Element | Purpose |
|---------|---------|
| **Identity** | Role name, purpose (one line) |
| **Adjectives** | What the agent must never violate |
| **Verb list** | Each verb has input [contract](docs/TERMS.md#contract), output [contract](docs/TERMS.md#contract), failure mode |
| **Handoff-in** | What must be true before this agent receives work |
| **Completion artifact** | What the agent produces to mark work complete |
| **Success criteria** | Ops vs defects; binary auditable outcomes |

Packages may use structured markdown or machine-readable schemas; the [boundary](docs/TERMS.md#boundary) declarations must be confirmer-checkable.

### 16.3 Produce ≠ [Audit](docs/TERMS.md#audit)

An agent that **produces** an artifact may not be the final **auditor** of that artifact. The agent that **ships** (ratifies, merges, releases) may not be the same agent that grades itself.

Separate:

1. **Produce** — create the artifact
2. **[Audit](docs/TERMS.md#audit)** — adversarial review against charter/adjectives
3. **[Ship](docs/TERMS.md#ship)** — authorize release

This is §7 applied to systems: proposer ≠ reviewer ≠ [confirmer](docs/TERMS.md#confirmer).

### 16.4 [Audit](docs/TERMS.md#audit) roles have no shipping authority

[Agent nouns](docs/TERMS.md#agent-noun) whose purpose is **adversarial review**, **[audit](docs/TERMS.md#audit)**, or **standards enforcement** do not have shipping authority.

- They may **not** ratify, merge, or release.
- They **produce findings**. Another role (or human) decides whether findings block the [ship](docs/TERMS.md#ship).
- Their verb lists explicitly exclude [ship](docs/TERMS.md#ship) verbs.

### 16.5 [Ship](docs/TERMS.md#ship) [noun](docs/TERMS.md#noun)

[Ship](docs/TERMS.md#ship) is a first-class [agent noun](docs/TERMS.md#agent-noun), separate from produce and [audit](docs/TERMS.md#audit). The [ship](docs/TERMS.md#ship) [noun](docs/TERMS.md#noun) authorizes release — it decides whether produced artifacts with [audit](docs/TERMS.md#audit) findings may be released.

#### Identity

**Name:** ship-role (or specific variants: ratify-role, merge-role, release-role)

**Purpose:** Authorize the release of artifacts that have completed produce and [audit](docs/TERMS.md#audit) phases. Decide whether work moves from "done" to "shipped."

#### Adjectives

1. **[Ship](docs/TERMS.md#ship) follows produce and [audit](docs/TERMS.md#audit).** A [ship](docs/TERMS.md#ship) verb may only execute after the artifact has been produced and audited. [Ship](docs/TERMS.md#ship) does not skip the pipeline.

2. **[Ship](docs/TERMS.md#ship) is a decision, not a review.** [Ship](docs/TERMS.md#ship) decides whether [audit](docs/TERMS.md#audit) findings block release. [Ship](docs/TERMS.md#ship) does not re-audit.

3. **[Ship](docs/TERMS.md#ship) is recorded.** Every [ship](docs/TERMS.md#ship) [action](docs/TERMS.md#action) records who, when, what artifact version, and what [audit](docs/TERMS.md#audit) findings were accepted or required to be fixed.

4. **[Ship](docs/TERMS.md#ship) authority is granted.** [Ship](docs/TERMS.md#ship) verbs require explicit [charter](docs/TERMS.md#charter) mandate or human delegation. An [agent noun](docs/TERMS.md#agent-noun) does not assume [ship](docs/TERMS.md#ship) authority.

#### Verbs

| Verb | Purpose | Precondition |
|------|---------|--------------|
| `ratify` | Accept a proposal as final | [Audit](docs/TERMS.md#audit) complete; findings addressed or [waived](docs/TERMS.md#waived) |
| `merge` | Merge a change to target branch | [Audit](docs/TERMS.md#audit) complete; CI green (or waiver recorded) |
| `release` | Publish or deploy an artifact | Merge complete; release criteria [met](docs/TERMS.md#met) |
| `waive-finding` | Accept a finding without fix | Finding documented; risk acknowledged |

Each verb has input [contract](docs/TERMS.md#contract), output [contract](docs/TERMS.md#contract), and failure mode. See [agent noun](docs/TERMS.md#agent-noun) package for schemas.

#### Handoff-in

| Condition | Evidence |
|-----------|----------|
| Artifact produced | Path to artifact or proposal |
| [Audit](docs/TERMS.md#audit) complete | [Audit](docs/TERMS.md#audit) report with findings or clean status |
| [Ship](docs/TERMS.md#ship) authority granted | [Charter](docs/TERMS.md#charter) mandate or delegation record |

#### Completion artifact

| Artifact | Contents |
|----------|----------|
| [Ship](docs/TERMS.md#ship) record | Who, when, artifact version, findings disposition |

#### Success criteria

| Measure | Ops (success) | [Defect](docs/TERMS.md#defect) |
|---------|---------------|--------|
| Pipeline honored | [Ship](docs/TERMS.md#ship) followed produce and [audit](docs/TERMS.md#audit) | [Ship](docs/TERMS.md#ship) skipped a phase |
| Decision recorded | [Ship](docs/TERMS.md#ship) record exists with all fields | [Ship](docs/TERMS.md#ship) [action](docs/TERMS.md#action) without record |
| Authority verified | [Ship](docs/TERMS.md#ship) authority checked before verb | [Ship](docs/TERMS.md#ship) without authority |

### 16.6 Rules for [agent nouns](docs/TERMS.md#agent-noun)

**S1.** Every [agent noun](docs/TERMS.md#agent-noun) has an identity file that states purpose and adjectives.

**S2.** Every verb on an [agent noun](docs/TERMS.md#agent-noun) has an input [contract](docs/TERMS.md#contract), output [contract](docs/TERMS.md#contract), and failure mode — just like noun-verbs in code (R10).

**S3.** Every [agent noun](docs/TERMS.md#agent-noun) declares handoff-in (preconditions) and completion artifact (postconditions).

**S4.** Success criteria are binary: ops (work completed as specified) vs defects (deviation from spec or adjectives).

**S5.** [Produce ≠ Audit ≠ Ship](docs/TERMS.md#produce-audit-ship). An agent may not [audit](docs/TERMS.md#audit) its own output as the final [gate](docs/TERMS.md#gate).

**S6.** [Audit](docs/TERMS.md#audit) roles have no [ship](docs/TERMS.md#ship) verbs. Adversarial auditors produce findings; another role decides.

**S7.** Produce→fitness [handoff](docs/TERMS.md#handoff) is [default-closed](docs/TERMS.md#default-closed). Produce completion requires change artifacts AND [produce package](docs/TERMS.md#produce-package). Without a complete package, fitness preflight returns `handoff_refused`; content scoring does not open.

**S8.** Produce packages require task/board [SSOT exit evidence](docs/TERMS.md#ssot-exit-evidence). Packages must include `ssot_leaf_ids` (one or more opaque leaf ids from the task/board SSOT) and `ssot_exit_status` (non-empty exit state string). Missing [SSOT exit evidence](docs/TERMS.md#ssot-exit-evidence) triggers `handoff_refused` (same refuse class as S7); fitness scoring refuses [MET](docs/TERMS.md#met); adversarial [audit](docs/TERMS.md#audit) refuses PASS (P-020).

### 16.8 [Quality](docs/TERMS.md#quality) metric (ops vs defects)

SSOT: [`integrity/QUALITY_METRIC.md`](integrity/QUALITY_METRIC.md).

[Quality](docs/TERMS.md#quality) measures the rate of defect-free operations across agent processes:

```text
Quality = Ops / Opportunities
```

Where **Opportunities** are gate/verb executions with binary outcomes, **Ops** are opportunities that completed as specified (PASS, MET, ready), and **Defects** are deviations from spec (FAIL, handoff_refused, error). This is DPMO-class without the academic theater.

**Q1.** [Quality evidence](docs/TERMS.md#quality-evidence) required at fitness. Produce packages must include [gate](docs/TERMS.md#gate) receipts with `outcome` + `timestamp`. Missing evidence triggers `handoff_refused` with `QUALITY_EVIDENCE`.

**Q2.** [Quality evidence](docs/TERMS.md#quality-evidence) required at adversarial [audit](docs/TERMS.md#audit). Artifacts must have `ssot_leaf_ids` present AND `quality_snapshot` with non-zero `opportunities`. Missing evidence causes [audit](docs/TERMS.md#audit) FAIL citing Q2.

**Q3.** [Quality snapshot](docs/TERMS.md#quality-snapshot) recorded at [boundary](docs/TERMS.md#boundary) exit. Completion artifacts include `{ opportunities, ops, defects, quality }`.

**Q4.** [Defect](docs/TERMS.md#defect) classification is binary. Every outcome is exactly [op](docs/TERMS.md#op) or [defect](docs/TERMS.md#defect). No partial, weighted, or continuous scores.

**Q5.** [Quality](docs/TERMS.md#quality) formula is ops/opportunities. No alternative formulas for the canonical [quality](docs/TERMS.md#quality) metric.

### 16.9 Confirmation checklist (systems)

For changes that touch [agent nouns](docs/TERMS.md#agent-noun):

- [ ] CS1. [Agent noun](docs/TERMS.md#agent-noun) has identity and adjectives.
- [ ] CS2. Each verb has input, output, and failure mode.
- [ ] CS3. Handoff-in and completion artifact are declared.
- [ ] CS4. Success criteria are binary (ops vs defects).
- [ ] CS5. [Produce ≠ Audit ≠ Ship](docs/TERMS.md#produce-audit-ship) separation is honored.
- [ ] CS6. [Audit](docs/TERMS.md#audit) roles have no [ship](docs/TERMS.md#ship) verbs.
- [ ] CS7. [Produce package](docs/TERMS.md#produce-package) present before fitness; incomplete handoffs refused, not soft-failed.
- [ ] CS8. Task/board [SSOT exit evidence](docs/TERMS.md#ssot-exit-evidence) present in [produce package](docs/TERMS.md#produce-package) (`ssot_leaf_ids` + `ssot_exit_status`); missing evidence refused (P-020).
- [ ] CS9. [Quality evidence](docs/TERMS.md#quality-evidence) present in [produce package](docs/TERMS.md#produce-package) (gate receipts with outcome + timestamp).
- [ ] CS10. [Quality snapshot](docs/TERMS.md#quality-snapshot) recorded at [boundary](docs/TERMS.md#boundary) exit (`{ opportunities, ops, defects, quality }`).

---

## Document control

- Status: working [charter](docs/TERMS.md#charter) (living). Descended from the [interview](docs/TERMS.md#interview) draft in [`theory/history/og-interview-draft.md`](theory/history/og-interview-draft.md). Not yet a ratified organizational standard.
- Home: this file (`CHARTER.md`) is authoritative for the practice. Do not edit the OG history copy.
- Subject: Product roof = [NLC](docs/TERMS.md#nlc) ([ADR 0011](adrs/0011-natural-language-coding-naming.md)). This file is [BBP](docs/TERMS.md#bbp) emit + integrity under that roof; [BBA](docs/TERMS.md#bba) is under-covers integrity. Systems model (§16) extends to agent fleets.
- Systems extension: [agent nouns](docs/TERMS.md#agent-noun) (§16), ratified by [ADR](docs/TERMS.md#adr) 0003
- Reduced ADRs: tags + primitives + if-thens, ratified by [ADR](docs/TERMS.md#adr) 0007
- No [noun inheritance](docs/TERMS.md#noun-inheritance), ratified by [ADR](docs/TERMS.md#adr) 0008
- [Primitive](docs/TERMS.md#primitive) interior functions, ratified by [ADR](docs/TERMS.md#adr) 0009
- [Gate](docs/TERMS.md#gate) after every generate, ratified by [ADR](docs/TERMS.md#adr) 0010
- Belief / [RCA](docs/TERMS.md#rca) climb / buck-stops-here: [ADR](docs/TERMS.md#adr) 0025 (`rules/nlc-0025.json`); RCA packet schema binder is expansion
- Factory spine + corpora: [ADR](docs/TERMS.md#adr) 0024
- Door fitness: `tools/fitness-charter-nlc-door.py` refuses a BBP-only first H1 (NLC roof required)
- Companion rejected frame: “governance / governed” as the name of the [integrity](docs/TERMS.md#integrity) loop
