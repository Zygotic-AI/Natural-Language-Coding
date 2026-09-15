# Boundary-Based Programming

A working spec for software that humans and agents can change without scattering invariants or widening blast radius.

> **Working merge copy.** Source of truth remains [`CHARTER.md`](CHARTER.md). This file is the section-by-section ACS ↔ BBA merge. Not ratified until the merge is complete.

This document is the charter. Implementation must be confirmable against the rules in [Confirmation checklist](#confirmation-checklist). If a rule cannot be checked, it is not a rule yet — it is a wish.

---

## 1. Purpose

> **TODO (vocabulary):** this charter still says *laws* / *invariants*. Settled term is **adjective** — a descriptor on the noun that no verb may violate. Do not rename mid-document; apply in a dedicated pass after §1–§16 are merged.

The goal is surgical change, from intent.

Humans hold intent: goals, requirements, and ADRs. AI compiles that intent into a system. The code is the object file. Generation is incomplete unless the object file is BBA-shaped — nouns own their descriptors, verbs are the only mutation path, goals only call verbs. Locally green, globally wrong — stopped.

An agent (or a person confirming a change) should be able to answer three questions before touching a boundary:

1. What is the unit of change?
2. What is allowed to mutate state?
3. If I change this, what else must still be true?

Boundary-Based Programming organizes a system around **nouns** that own laws, **verbs** that are the only legal way to change those nouns, and **goals** that orchestrate work across nouns and the outside world. Boundaries are not documentation. They are contracts plus enforcement.

This exists because AI-assisted engineering fails in two opposite ways:

- The agent sees the whole repository and thrashes.
- The agent sees one folder, makes that folder green, and silently breaks a law that lived somewhere else.

We shrink the search space for *use-case* changes without exploding the search space for *concept* changes.

---

## 2. Why this shape

> **TODO (workflow):** `CHARTER.md` §2 lists workflow as a fourth piece of “the whole model.” ACS treats workflow as a goal of goals — durable is a property, not a new design citizen. Merged here as composition, not as a fourth kind. Confirm before §4 / §5.5 land.

Layered architecture groups code by technical concern. Agents then hunt across controllers, services, and repositories to change one business outcome.

Goal-only architecture groups code by verb. That helps a single use-case edit. It hurts when the law is a noun: invoice status, money rounding, eligibility. Those laws get copied into every verb folder. Each copy looks correct. The system becomes several slightly different truths. Two fine goals. Two invoices.

Object-only architecture concentrates the laws and hides the use-case. Agents cannot find “the work to do.” Blast radius becomes “the Invoice class.”

The compiler makes that worse if it has no required shape: it will emit whichever of those three is easiest for the current goal. That is why BBA is the instruction set the process may not skip.

Two layers, one architecture:

- **Process** (ACS) — humans hold goals, requirements, ADRs. Interview, bind, generate, audit, RCA.
- **Design** (BBA) — the emitted system is nouns, verbs, and goals. A goal is an outcome *and* a boundary that may only call published verbs.

The combined shape the compiler must emit:

- **Noun** = identity, state, invariants. The retrieval key for “how does an invoice work?”
- **Verb on the noun** = a contracted mutation. The only way state changes.
- **Goal** = a use-case that reaches the edge: I/O, other nouns, events, policy. It calls verbs. It does not write fields.
- **Workflow** = a durable sequence of goals when one in-process call is not enough. Not a fourth design citizen. A goal of goals.

Generation is incomplete unless that shape is present and a binder fails a goal that writes noun fields or re-decides a noun’s descriptor. Two goal boxes are fine if both only call Invoice verbs.

The repo may be huge. The window for write, audit, and graph is one boundary plus the published contracts of its neighbors. If a step needs two objects’ internals at once, the cut is wrong.

That is the whole model. Everything else is how we keep it honest.

---

## 3. Naming

**Practice name:** Boundary-Based Programming.

**Mechanism:** boundaries are enforced (contracts, privacy of fields, fitness checks, review).

Do not name the practice “governance” or “governed.” Those words imply a committee ruling subjects. The artifacts that hold decisions are a **charter** (this document, plus ADRs). The property we protect is **integrity**. The act that keeps agents honest is **adversarial review against the charter**.

Useful substitutes if a slot in an older diagram said “Governance Architecture”:

| Avoid | Use |
|---|---|
| Governance | Charter, integrity, covenant, protocol |
| Governed system | Bounded system, charter-bound system |
| Governance review | Adversarial review, integrity check |

**Boundary-Enforced Programming** is a true claim about the pipeline. It is a poor name for the practice. Put enforcement in the rules and the CI gate, not in the title.

---

## 4. Core model

### 4.1 Noun

A noun is a domain concept with identity and laws.

Examples: `Invoice`, `Customer`, `Order`, `PaymentAllocation`.

A noun contains:

- Identity
- Private state
- Invariants
- A short public verb list
- Tests that prove the invariants hold after every verb

A noun does **not** contain:

- HTTP, file, queue, or database adapter code
- Multi-noun orchestration
- “Send the reminder email”
- “Render the PDF”
- “Export to QuickBooks”

Those are goals, or they belong to a different noun.

### 4.2 Verb (on a noun)

A verb is a state change that must leave the noun truthful.

Examples on `Invoice`: `issue`, `applyPayment`, `void`.

Every verb has:

- A name
- An input contract
- An output contract (result or error)
- Preconditions
- Postconditions / invariants
- Tests

Verbs are the contracted boundary of the noun. There is no other public mutation path.

### 4.3 Goal

A goal is an executable business use-case.

Examples: `CreateInvoice`, `RecordBankPayment`, `ApproveOrder`, `GenerateYearEndReport`.

A goal contains:

- Purpose
- Input / output contract
- One public entrypoint
- Orchestration: load nouns, call verbs, persist, publish, talk to the outside world
- Explicit dependencies
- Tests for the use-case, not for the noun’s invariants (those live on the noun)

A goal does **not**:

- Assign noun fields
- Reimplement noun invariants
- Become a second home for “how invoices work”

A goal that only calls one noun-verb and does no I/O or policy is optional. Do not invent YAML theater for a pass-through. Expose the noun-verb. Add the goal when there is orchestration to justify it.

### 4.4 Workflow

A workflow is an ordered, durable composition of goals.

Use a workflow when:

- Work spans time (waits, human approval, retries)
- Work spans nouns that cannot share a single transaction
- Failure requires compensation

Do not use a workflow as a second implementation of a noun invariant. The workflow calls goals. Goals call verbs. Verbs protect the noun.

If the runtime is Temporal (or equivalent), the workflow definition *is* the execution graph for that multi-step outcome. Do not maintain a hand-written execution graph that duplicates it.

### 4.5 Contract

A contract is a machine-readable schema for a boundary.

Two layers, one meaning:

1. **Noun-verb contract** — canonical payload and result for `Invoice.applyPayment`.
2. **Goal contract** — the use-case envelope (actor, source system, idempotency key, the verb payload).

The goal wraps the verb contract. It does not fork the meaning of `balance`, `status`, or `currency`. Shared fields come from one canonical type.

### 4.6 Charter and ADR

The **charter** is this document plus accepted ADRs.

An **ADR** records a decision that later work must not quietly undo:

- Why this noun exists
- Which verbs it exposes
- Which goals may call them
- What was rejected and why

ADRs are not essays. They are decisions with consequences.

---

## 5. Rules

> **TODO (vocabulary):** throughout this section the charter says *invariant* / *law*. Settled term is **adjective** — a descriptor on the noun that no verb may violate. Apply the rename in the dedicated vocabulary pass, not here.
>
> **TODO (binder → gate):** R21, R23–R31 and the binding-matrix language still say "binder." Settled split: **binding** is the planning act (each atomic step linked to the ADRs/requirements it must honor); **gate** is the machine that fails the change after generation. R30 already uses "hard gate" — keep that. Rename the rest in the vocabulary pass. Until then, read "binder" here as "gate."
>
> **TODO (workflow):** R2, R7, R17–R19 treat workflow as a peer of goal. ACS: workflow is a goal of goals (durable is a property). Same open question as §2 / §4.4 — confirm before this section is considered final.
>
> **ACS addition:** these rules are not only checked at review time. Under PLANIT, each atomic step is *bound* to the applicable rules before generation, and a **gate** verifies the binding after. A step with no applicable rule must explicitly declare "no bindings necessary" — that declaration is itself a binding.

Rules are written so an implementing agent can confirm or fail them. "Should" is not a rule.

### 5.1 Ownership

**R1.** If breaking the rule would make *this noun* a lie, the rule lives on the noun, as an adjective or as a verb precondition/postcondition.

**R2.** If the work spans nouns, I/O, or a business outcome, it is a goal (or a workflow of goals).

**R3.** Cross-noun work does not get glued onto the most convenient noun. `allocatePaymentToInvoices` is a goal, or a `PaymentAllocation` noun if it has its own adjectives. It is not `Invoice.allocateAcrossFriends`.

**R4.** If a verb does not need the noun's adjective set, it does not belong on the noun.

### 5.2 Mutation

**R5.** Noun fields are private. No goal, workflow, adapter, or other noun writes them.

**R6.** The only legal mutation of a noun is a public verb on that noun.

**R7.** Nouns never call goals. Nouns never call workflows. Direction is workflow → goal → noun-verb only (plus explicit reads).

**R8.** Goals may read what the noun chooses to expose (queries / snapshots). Goals may not reach through that snapshot and write. A sensitive adjective fetched through a verb may cross only one boundary — the consuming verb — and must be consumed in place or dropped. It must not be stored, passed to another boundary, or returned. The gate tracks the value's lifetime, not a declared label.

### 5.3 Contracts

**R9.** Every public goal entrypoint has an input contract and an output contract.

**R10.** Every public noun-verb has an input contract and an output contract.

**R11.** A field that means the same thing in two contracts is defined once and referenced. Duplicate independent definitions of the same meaning are a defect.

**R12.** Contracts are versioned. Breaking changes require a new version and an ADR. A new verb version must honor every adjective on its noun — it may add behavior but never drop or silently change an adjective. Versioning changes API shape, not ownership of adjectives.

### 5.4 Goal shape

**R13.** One public entrypoint per goal.

**R14.** Goal internals are not callable from other goals. If two goals need the same orchestration fragment, extract a noun-verb, a shared library with its own contract, or a smaller goal. Do not import another goal's internals.

**R15.** Shared domain logic that protects a noun lives on the noun, not in a helper copied into two goals.

**R16.** A new goal is created only when there is a distinct use-case. Do not create a goal per function (`ValidateEmail` as a sibling of `CreateCustomer` unless it is a real standalone capability).

### 5.5 Workflows

**R17.** Workflows compose goals. They do not call noun-verbs directly unless the runtime has no goal layer and the workflow *is* the goal. Prefer one rule in a given codebase and state it in an ADR.

**R18.** Compensation and retries live in the workflow or the goal, not inside the noun, unless the noun's adjective itself requires idempotency of a verb. Verbs must be safe to retry if the workflow retries them. Declare that on the verb.

**R19.** Do not maintain a separate hand-authored execution-graph file that duplicates the workflow definition.

### 5.6 Knowledge and drift

**R20.** The charter, contracts, and code must agree. If they disagree, the build fails. Code does not win by existing. Spec does not win by being newer. They must be reconciled in the same change.

**R21.** Dependency and impact information is generated from code and contracts, not authored as a parallel JSON document. The binding matrix is the requirement index for this practice hub (requirement → audit → gate); it is not a dependency or impact graph, and R21 applies to generated "what breaks" views in adopting codebases, not to that matrix. Knowledge domains are shelves of standing ADRs and requirements the interview consults before asking.

**R22.** ADRs that are superseded are marked superseded, not deleted. The trail is part of integrity.

### 5.7 Enforcement

**R23.** A gate fails the change if a goal (or workflow, or adapter) assigns a noun field or imports a noun internals module.

**R24.** A gate fails the change if invoice-equivalent money math, status transitions, or named adjectives appear outside the owning noun (copy-paste of the adjective).

**R25.** Tests for a noun's adjectives live next to the noun and run on every verb. Goal tests do not replace them.

**R25a.** A gate fails the change if a sensitive adjective's value is stored in another datum, passed to another boundary, or returned from the consuming verb. The value must be consumed in place or dropped. This is taint-lifetime tracking, not label-checking.

**R25b.** A gate scans for non-OO escape hatches — raw SQL, ORM bypasses, deserialization, reflection — that touch a noun's adjectives without going through a published verb.

### 5.8 Practice integrity (zero variance)

Ratified by [`adrs/0001-zero-variance-integrity.md`](adrs/0001-zero-variance-integrity.md). P2 scope: [`adrs/0002-p2-scope.md`](adrs/0002-p2-scope.md). Detail: [`integrity/PRINCIPLES.md`](integrity/PRINCIPLES.md). Matrix: [`integrity/binding-matrix.json`](integrity/binding-matrix.json).

**R26.** Practice integrity principles P1–P7 are in force: stand-alone branding, zero variance, hard gates, hard boundary I/O, binary requirement audits, unbound-matrix failure with listing, promote-only-when-bindable with listing.

**R27.** Every published requirement in this repo appears in the binding matrix with an audit id. Audit `A-BINDING-COVERAGE` fails and lists any missing id.

**R28.** Unbound binding-matrix entries fail audit `A-BINDING-UNBOUND`. The audit report lists every unbound requirement id.

**R29.** In-force requirements that are not bindable fail audit `A-BINDING-PROMOTE`. The audit report lists every offending requirement id.

**R30.** Every prescribed step or action has a hard gate whose only outcomes are complete or incomplete, with evidence. Gates are default-closed: a gate with no binder registered is marked **unbound**, never passed.

**R31.** Every public boundary declares hard input, hard output, and failure mode (returned error, thrown exception, or process exit when the boundary is code).

---

## 6. Order of agent execution

> **TODO (vocabulary):** this section still says *invariant* / *law*. Settled term is **adjective**. Apply in the dedicated vocabulary pass.
>
> **TODO (binder → gate):** "binder" language below reads as **gate** per the settled split (binding = planning act; gate = post-generation verification). Rename in the vocabulary pass.
>
> **TODO (workflow):** class D still lists workflow as a peer class. ACS: workflow is a goal of goals. Same open question as §2 / §4.4 / §5.5.
>
> **ACS integration:** PLANIT (interview → bind → generate → prove) runs *above* this loop. PLANIT's bind step feeds the proposal; PLANIT's prove step is this loop's review + confirm, executed as independent gates. The loop below is the execution spine; PLANIT is the planning spine that feeds it.

This is the default loop for design and code. Skip a step only when an ADR says that class of change is exempt (for example, a one-line copy fix inside an already-ratified verb).

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

### Step 0 — Load charter

Read this document and the ADRs that touch the nouns and goals in scope. If the change would violate a rule, stop and propose an ADR first. Under PLANIT this is step 0 (load what already exists) — do not interview for facts already bound.

### Step 1 — Classify the change

Choose exactly one primary class:

| Class | You are changing | Home of the work |
|---|---|---|
| A. Adjective | Adjective, status machine, money, eligibility | Noun + its verbs |
| B. Mutation API | Add/change a verb | Noun-verb contract + noun tests |
| C. Use-case | Orchestration, I/O, policy around existing verbs | Goal |
| D. Multi-step | Time, approval, compensation across goals | Workflow (goal of goals) |
| E. Boundary meaning | Shared field meaning, version, compatibility | Canonical contract + ADR |
| F. Charter | A rule in this document | ADR first, then this file |

If the request is "change how invoices work," it is class A, not class C. Open the noun. Do not open one goal and improvise.

### Step 2 — Propose (spec, not code)

The proposing agent produces, in one change-set of documents:

- Classification (A–F)
- Nouns touched, verbs touched, goals touched, workflows touched
- Draft contracts if any boundary changes
- Adjectives that must still hold
- Explicit non-goals ("this does not change tax rounding")
- Test names that will prove it
- Impact list: other goals/verbs that call the changed boundary
- **Bindings:** each atomic statement points to the requirement IDs, ADR IDs, or BBA standard it must honor. A statement with nothing applicable must explicitly declare "no bindings necessary" — that declaration is itself a binding.

No implementation in this step unless the change is already classified as exempt.

**Produce package required for handoff.** Proposal completion includes the produce package: classification (plan A–F as above), applicability statement, boundary I/O declarations, self-adversarial notes, binding declarations, and task/board SSOT exit evidence (`ssot_leaf_ids` + `ssot_exit_status`). A proposal without this package is incomplete. Incomplete proposals do not hand off to fitness or adversarial review.

### Step 2.5 — Fitness preflight

Before adversarial review opens, fitness performs a preflight check:

- **Package present and complete** → proceed to Step 3.
- **Package missing or incomplete** → return `handoff_refused` with defect log. Do not open content scoring. The proposal is not fitness-FAIL; it is produce-incomplete.

Preflight is not discovery. Fitness does not invent the package, coach the producer, or soft-fail to prompt remediation. The producer fixes the package and resubmits. Do not normalize "re-gate" for missing-package rework.

### Step 3 — Adversarial review

A second agent, with a different role, attacks the proposal. It does not implement. It does not protect the author's feelings. It answers only:

- Where can a goal now write private state?
- Which adjective is now split across two homes?
- Which contract field is defined twice with room to drift?
- Is this a god-noun collecting verbs it should not own?
- Is this a new goal that should have been a noun-verb?
- Is this a noun-verb that should have been a goal?
- What breaks if this verb is retried?
- What did the impact list miss?
- Does any sensitive adjective's value escape its consuming verb (stored, passed, or returned)?
- Does any noun reach past another boundary except through a published verb?

Findings are comments against the proposal. "Looks good" with no checklist is not a review. This is PLANIT's prove gate, run independently of the generator.

### Step 4 — Revise

The proposing agent answers every finding: fix, or record why the finding is wrong. Unresolved findings block ratification.

### Step 5 — Ratify

A human, or an automated gate whose policy an ADR named, accepts the proposal. Ratification is a recorded event: who, when, which proposal version.

Until ratification, implementation is not authorized for class A, B, D, E, or F. Class C may be tightened by ADR for a given repo (some teams ratify every new goal; some do not).

### Step 6 — Implement

Code follows the ratified spec. This is PLANIT's generate step: AI emits BBA-shaped code for bound statements only. Humans do not edit the output.

- Noun internals stay inside the noun module.
- Goals call verbs only.
- Contracts generate or validate I/O.
- Tests named in the proposal are written and pass.
- Generated code respects all declared bindings; a gate fails any escape.

### Step 7 — Confirm

Run the [Confirmation checklist](#confirmation-checklist). Any fail is a failed change, not a note for later. This is the second half of PLANIT's prove: an independent gate verifies the code holds every binding and delivers the stated outcome. Fail → RCA into interview or bind, then regenerate. Never patch the generated tree to quiet the gate.

### Step 8 — Record

- Update or add the ADR if a decision was made.
- Leave the generated impact/dependency view in the state the tooling produces.
- Do not write a parallel "architecture JSON" by hand.
- Record the interview miss if a fork was caught here — the log is how interview quality compounds.

---
