> **Provenance:** Original interview / design-conversation draft (OG). Preserved verbatim as historical source.
> **Living charter:** [`CHARTER.md`](../../CHARTER.md) at the repo root — edit there going forward.
> **Decision:** Tracked in git (not gitignored). It is the OG draft of the practice, not private interview notes.

---

# Boundary-Based Programming

A working spec for software that humans and agents can change without scattering invariants or widening blast radius.

This document is the charter. Implementation must be confirmable against the rules in [Confirmation checklist](#confirmation-checklist). If a rule cannot be checked, it is not a rule yet — it is a wish.

---

## 1. Purpose

The goal is surgical change.

An agent (or a person) should be able to answer three questions before touching code:

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

Layered architecture groups code by technical concern. Agents then hunt across controllers, services, and repositories to change one business outcome.

Goal-only architecture groups code by verb. That helps a single use-case edit. It hurts when the law is a noun: invoice status, money rounding, eligibility. Those laws get copied into every verb folder. Each copy looks correct. The system becomes several slightly different truths.

Object-only architecture concentrates the laws and hides the use-case. Agents cannot find “the work to do.” Blast radius becomes “the Invoice class.”

The combined shape:

- **Noun** = identity, state, invariants. The retrieval key for “how does an invoice work?”
- **Verb on the noun** = a contracted mutation. The only way state changes.
- **Goal** = a use-case that reaches the edge: I/O, other nouns, events, policy. It calls verbs. It does not write fields.
- **Workflow** = a durable sequence of goals when one in-process call is not enough.

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

Rules are written so an implementing agent can confirm or fail them. “Should” is not a rule.

### 5.1 Ownership

**R1.** If breaking the rule would make *this noun* a lie, the rule lives on the noun, as an invariant or as a verb precondition/postcondition.

**R2.** If the work spans nouns, I/O, or a business outcome, it is a goal (or a workflow of goals).

**R3.** Cross-noun work does not get glued onto the most convenient noun. `allocatePaymentToInvoices` is a goal, or a `PaymentAllocation` noun if it has its own invariants. It is not `Invoice.allocateAcrossFriends`.

**R4.** If a verb does not need the noun’s invariant set, it does not belong on the noun.

### 5.2 Mutation

**R5.** Noun fields are private. No goal, workflow, adapter, or other noun writes them.

**R6.** The only legal mutation of a noun is a public verb on that noun.

**R7.** Nouns never call goals. Nouns never call workflows. Direction is workflow → goal → noun-verb only (plus explicit reads).

**R8.** Goals may read what the noun chooses to expose (queries / snapshots). Goals may not reach through that snapshot and write.

### 5.3 Contracts

**R9.** Every public goal entrypoint has an input contract and an output contract.

**R10.** Every public noun-verb has an input contract and an output contract.

**R11.** A field that means the same thing in two contracts is defined once and referenced. Duplicate independent definitions of the same meaning are a defect.

**R12.** Contracts are versioned. Breaking changes require a new version and an ADR.

### 5.4 Goal shape

**R13.** One public entrypoint per goal.

**R14.** Goal internals are not callable from other goals. If two goals need the same orchestration fragment, extract a noun-verb, a shared library with its own contract, or a smaller goal. Do not import another goal’s internals.

**R15.** Shared domain logic that protects a noun lives on the noun, not in a helper copied into two goals.

**R16.** A new goal is created only when there is a distinct use-case. Do not create a goal per function (`ValidateEmail` as a sibling of `CreateCustomer` unless it is a real standalone capability).

### 5.5 Workflows

**R17.** Workflows compose goals. They do not call noun-verbs directly unless the runtime has no goal layer and the workflow *is* the goal. Prefer one rule in a given codebase and state it in an ADR.

**R18.** Compensation and retries live in the workflow or the goal, not inside the noun, unless the noun’s invariant itself requires idempotency of a verb. Verbs must be safe to retry if the workflow retries them. Declare that on the verb.

**R19.** Do not maintain a separate hand-authored execution-graph file that duplicates the workflow definition.

### 5.6 Knowledge and drift

**R20.** The charter, contracts, and code must agree. If they disagree, the build fails. Code does not win by existing. Spec does not win by being newer. They must be reconciled in the same change.

**R21.** Dependency and impact information is generated from code and contracts, not authored as a parallel JSON document.

**R22.** ADRs that are superseded are marked superseded, not deleted. The trail is part of integrity.

### 5.7 Enforcement

**R23.** A fitness check fails the change if a goal (or workflow, or adapter) assigns a noun field or imports a noun internals module.

**R24.** A fitness check fails the change if invoice-equivalent money math, status transitions, or named invariants appear outside the owning noun (copy-paste of the law).

**R25.** Tests for a noun’s invariants live next to the noun and run on every verb. Goal tests do not replace them.

---

## 6. Order of agent execution

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

Read this document and the ADRs that touch the nouns and goals in scope. If the change would violate a rule, stop and propose an ADR first.

### Step 1 — Classify the change

Choose exactly one primary class:

| Class | You are changing | Home of the work |
|---|---|---|
| A. Law | Invariant, status machine, money, eligibility | Noun + its verbs |
| B. Mutation API | Add/change a verb | Noun-verb contract + noun tests |
| C. Use-case | Orchestration, I/O, policy around existing verbs | Goal |
| D. Multi-step | Time, approval, compensation across goals | Workflow |
| E. Boundary meaning | Shared field meaning, version, compatibility | Canonical contract + ADR |
| F. Charter | A rule in this document | ADR first, then this file |

If the request is “change how invoices work,” it is class A, not class C. Open the noun. Do not open one goal and improvise.

### Step 2 — Propose (spec, not code)

The proposing agent produces, in one change-set of documents:

- Classification (A–F)
- Nouns touched, verbs touched, goals touched, workflows touched
- Draft contracts if any boundary changes
- Invariants that must still hold
- Explicit non-goals (“this does not change tax rounding”)
- Test names that will prove it
- Impact list: other goals/verbs that call the changed boundary

No implementation in this step unless the change is already classified as exempt.

### Step 3 — Adversarial review

A second agent, with a different role, attacks the proposal. It does not implement. It does not protect the author’s feelings. It answers only:

- Where can a goal now write private state?
- Which invariant is now split across two homes?
- Which contract field is defined twice with room to drift?
- Is this a god-noun collecting verbs it should not own?
- Is this a new goal that should have been a noun-verb?
- Is this a noun-verb that should have been a goal?
- What breaks if this verb is retried?
- What did the impact list miss?

Findings are comments against the proposal. “Looks good” with no checklist is not a review.

### Step 4 — Revise

The proposing agent answers every finding: fix, or record why the finding is wrong. Unresolved findings block ratification.

### Step 5 — Ratify

A human, or an automated gate whose policy an ADR named, accepts the proposal. Ratification is a recorded event: who, when, which proposal version.

Until ratification, implementation is not authorized for class A, B, D, E, or F. Class C may be tightened by ADR for a given repo (some teams ratify every new goal; some do not).

### Step 6 — Implement

Code follows the ratified spec.

- Noun internals stay inside the noun module.
- Goals call verbs only.
- Contracts generate or validate I/O.
- Tests named in the proposal are written and pass.

### Step 7 — Confirm

Run the [Confirmation checklist](#confirmation-checklist). Any fail is a failed change, not a note for later.

### Step 8 — Record

- Update or add the ADR if a decision was made.
- Leave the generated impact/dependency view in the state the tooling produces.
- Do not write a parallel “architecture JSON” by hand.

---

## 7. Agent roles

Separate roles. One model may play them in sequence, but not in the same pass as both author and skeptic of its own work.

| Role | Allowed to do | Not allowed to do |
|---|---|---|
| Proposer | Draft spec, then implement after ratification | Grade its own proposal as final |
| Reviewer | Attack the spec and the diff against this charter | Write the implementation in the same turn |
| Confirmer | Run checklist, report pass/fail with evidence | “Approve” without evidence |
| Recorder | Write ADRs and status | Change rules without an ADR |

The reviewer prompt is: you are the skeptic. Find the hole. Cite the rule number.

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
├─ workflows/                          # if Temporal or equivalent
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
- Treated security, data, observability, audit, and evidence as sibling trees instead of annotations on nouns, verbs, and goals
- Put Agent concerns in a later tier even though agents are the primary consumer
- Assumed hand-maintained `dependency-graph.json` and `impact-analysis.json`
- Isolated goals without a noun, which scatters invariants and invites duplication
- Used “governance” as a bucket instead of a charter plus review

Those higher-level views (product, portfolio, strategy) can be derived later. They are not the foundation agents implement against.

---

## 10. Pitfalls and remediations

### 10.1 Scattered invariants

**Pitfall.** “Cannot void after payment” lives in `VoidInvoice` and a slightly different version lives in `ApplyPayment`. An agent edits one.

**Remediation.** The invariant lives on `Invoice`. Both verbs consult it. Goal tests are not the home of the law. Fitness check fails if the status machine is reimplemented in a goal.

### 10.2 Duplication that looks locally correct

**Pitfall.** The agent’s context is the current goal. It reimplements tax rounding. CI on that goal is green.

**Remediation.** R15 and R24. Money math has one module. Reviewer asks “where else does this formula exist?” Confirmer greps.

### 10.3 Conceptual changes treated as goal changes

**Pitfall.** “Allow partial payments” is implemented only in `ApplyPayment` the goal. `VoidInvoice` still assumes full-payment status values.

**Remediation.** Classification step. Conceptual change is class A. Proposer must open the noun and list every verb that assumes the old law.

### 10.4 Hidden coupling through shared data

**Pitfall.** Goals look independent. They write the same row. The call graph does not show that `status` means two things.

**Remediation.** Only verbs write. Generated impact includes “who calls this verb,” not only “which goal folder changed.” Shared tables are behind the noun’s persistence adapter, not open to every goal.

### 10.5 Goal explosion or god-goal

**Pitfall.** One function per goal, or one goal that does the entire billing domain.

**Remediation.** R16 and the pass-through rule. Reviewer flags both. Sizing heuristic: a goal names a use-case a stakeholder would recognize; a verb names a state change the noun must survive.

### 10.6 God-noun

**Pitfall.** `Invoice.renderPdf`, `Invoice.sendReminder`, `Invoice.exportQuickBooks`.

**Remediation.** R4. If the verb does not need the invariant set, it is a goal or another noun. Reviewer checklist includes god-noun.

### 10.7 Two contract layers that drift

**Pitfall.** Goal input defines `balance` one way. Verb input defines it another.

**Remediation.** R11. Canonical type. Goal contract references it. Confirmer diffs schemas for same-named fields with different types.

### 10.8 Hand-maintained graphs that lie

**Pitfall.** `dependency-graph.json` is stale. Agents trust it.

**Remediation.** R21. Generate from imports, workflow definitions, and registered verb calls. If it cannot be generated, do not pretend the file is a source of truth.

### 10.9 Convention without enforcement

**Pitfall.** “Internals are private” is a README sentence. The third agent session writes `invoice.status = 'paid'` from a goal.

**Remediation.** R5, R6, R23. Language visibility, module boundaries, and a CI rule. Convention is not a boundary.

### 10.10 Author grades its own homework

**Pitfall.** The same pass proposes and approves.

**Remediation.** Step 3 as a separate role. Review with rule numbers. “Looks good” is not evidence.

### 10.11 Workflow as a second domain model

**Pitfall.** Temporal workflow re-implements “when an invoice is paid” instead of calling `applyPayment`.

**Remediation.** R17–R18. Workflows compose goals; verbs keep the law. Reviewer asks where the status machine lives.

---

## 11. Confirmation checklist

An implementing agent must print this list with `PASS`, `FAIL`, or `N/A` and a pointer (file and symbol) for every non-N/A item. `N/A` requires a one-line reason.

### Classification and home

- [ ] C1. Change class (A–F) is stated.
- [ ] C2. Laws live on the noun named in C1, not in a goal folder.
- [ ] C3. New orchestration lives in a goal or workflow, not as a method on an unrelated noun.

### Mutation path

- [ ] C4. No assignment to noun fields occurs outside the noun module.
- [ ] C5. Every state change of a noun goes through a public verb.
- [ ] C6. No noun module imports a goal or workflow module.

### Contracts

- [ ] C7. Each changed public goal has input and output schemas.
- [ ] C8. Each changed public verb has input and output schemas.
- [ ] C9. Shared meanings use a shared type; no forked `balance` / `status` / `currency`.
- [ ] C10. Breaking schema changes have a new version and an ADR.

### Goal and workflow shape

- [ ] C11. Each changed goal has exactly one public entrypoint.
- [ ] C12. No goal imports another goal’s internals.
- [ ] C13. No new goal exists whose only job is a single noun-verb with no I/O or policy — or an ADR explains why the wrapper exists.
- [ ] C14. Workflows call goals (or the ADR-chosen single exception is documented).
- [ ] C15. Verbs invoked from a retrying workflow are idempotent, or the workflow uses an idempotency key the verb honors.

### Invariants and tests

- [ ] C16. Every invariant named in the proposal has a test on the noun.
- [ ] C17. Every new verb has tests for success, precondition failure, and invariant preservation.
- [ ] C18. Goal tests cover the use-case, not a copy of the noun’s invariant suite.
- [ ] C19. No second implementation of the same law exists in the diff (search for duplicated predicates).

### Integrity of the change

- [ ] C20. Fitness / lint rules for R23 and R24 passed.
- [ ] C21. Impact list in the proposal matches generated callers of the changed verbs/goals.
- [ ] C22. Charter/ADR/code/contracts were updated in the same change if they were affected.
- [ ] C23. Adversarial review findings are all fixed or explicitly rebutted.
- [ ] C24. Ratification is recorded for classes that require it.

If C4, C5, C9, C16, C19, or C20 fail, the change is not complete.

---

## 12. Minimal fitness checks to install

These are the smallest enforcement set. Language-specific tools vary (module visibility, ESLint boundaries, ArchUnit, import-linter, custom grep in CI). The check must fail the build, not warn.

1. **No field writes across the noun boundary.** Goal, workflow, and adapter packages cannot assign noun fields.
2. **No imports of noun internals.** Only the noun’s public verb module is importable.
3. **No imports of goal internals from another goal.**
4. **Law locality.** A denylist of invariant identifiers or modules (status transition tables, rounding functions) that may only appear under `domain/<noun>/`.
5. **Contract presence.** A public entrypoint without a schema file (or generated schema) fails CI.
6. **Schema identity.** Same property name + different type across contracts in one change fails CI or a review bot.

Until check 1 exists, the charter is not in force. Start there.

---

## 13. Mapping to things that already exist

Use these; do not reimplement them under new folder names.

| Need | Existing tool or pattern |
|---|---|
| Noun + invariant-preserving verbs | DDD aggregate; methods or typed commands on the aggregate |
| Typed mutation contracts on the noun | Axon commands; Orleans / actor grain interface; Design by Contract |
| Goal as use-case folder | Vertical slice; Clean Architecture handler / MediatR command |
| Module privacy enforced in CI | Spring Modulith + ArchUnit; ESLint boundaries; import-linter |
| Durable multi-goal execution | Temporal (or equivalent) workflows |
| Design-first I/O contracts | JSON Schema / Zod / TypeBox; OpenAPI; Smithy; Goa |
| Generated “what breaks” at package grain | Nx project graph / `affected`; language import graph |
| Recorded decisions | ADRs |
| Drift as a merge failure | Contract tests (Pact, schemathesis); spec-code gate |

No single downloaded framework is “Boundary-Based Programming.” The assembly is: noun module with private state, verb contracts, goal folders, workflow runtime if needed, generated graphs, fitness checks, ADR charter, two-role review.

In Node, that assembly is typically: domain class + private fields, Zod or TypeBox as verb and goal contracts, one handler file per goal, Temporal for multi-noun time, lint/import rules that fail when a goal touches noun internals.

---

## 14. What “done” means for adopting this

A codebase has adopted Boundary-Based Programming when all of the following are true:

1. This charter (or a dated descendant) is in the repo.
2. At least one real noun has private state and contracted verbs.
3. At least one real goal calls those verbs and does not write fields.
4. Fitness check 1 from section 12 fails a deliberate violation in CI.
5. The agent loop in section 6 is the written procedure for class A and B changes.
6. An implementing agent can run section 11 and produce evidence, not vibes.

Until item 4 is true, treat the rest as a style guide.

---

## 15. Short form for an agent system prompt

You may paste this block into an agent. The rest of this file remains authoritative.

```text
You practice Boundary-Based Programming.

Nouns own identity, private state, and invariants.
The only legal mutation of a noun is a public verb with an input/output contract.
Goals orchestrate: I/O, other nouns, events, policy. Goals call verbs. Goals never assign noun fields.
Workflows compose goals. They do not reimplement noun laws.
Shared meaning lives in one canonical type. Do not fork balance, status, or currency.
If a change is about how a concept works, open the noun, not a single goal.
Propose spec first. A separate reviewer pass attacks the spec against the charter rules.
Do not approve your own proposal in the same pass.
Confirm with the checklist: private fields, verb-only writes, contract presence, invariant tests on the noun, no duplicated laws, fitness checks green.
If charter, contracts, and code disagree, stop and reconcile them in one change.
```

---

## Document control

- Status: working charter from design conversation, not a ratified organizational standard
- Subject: Boundary-Based Programming (nouns, contracted verbs, goals, workflows)
- Companion rejected name: Boundary-Enforced Programming (keep as a description of CI, not the practice title)
- Companion rejected frame: “governance / governed” as the name of the integrity loop
