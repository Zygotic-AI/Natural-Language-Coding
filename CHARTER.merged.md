## 7. Agent roles

> **TODO (vocabulary):** this section still says *invariant* / *law*. Settled term is **adjective**. Apply in the dedicated vocabulary pass.
>
> **TODO (binder → gate):** "binder" language below reads as **gate** per the settled split (binding = planning act; gate = post-generation verification). Rename in the vocabulary pass.
>
> **TODO (workflow):** class D still lists workflow as a peer class. ACS: workflow is a goal of goals. Same open question as §2 / §4.4 / §5.5.
>
> **ACS integration:** PLANIT (interview → bind → generate → prove) runs *above* this loop. PLANIT's bind step feeds the proposal; PLANIT's prove step is this loop's review + confirm, executed as independent gates. The loop below is the execution spine; PLANIT is the planning spine that feeds it. The roles here are the *execution* roles; PLANIT's interview and RCA are *planning* roles that sit above them.

Separate roles. One model may play them in sequence, but not in the same pass as both author and skeptic of its own work.

| Role | Allowed to do | Not allowed to do |
|---|---|---|
| Proposer | Draft spec, then implement after ratification | Grade its own proposal as final |
| Reviewer | Attack the spec and the diff against this charter | Write the implementation in the same turn |
| Confirmer | Run checklist, report pass/fail with evidence | "Approve" without evidence |
| Recorder | Write ADRs and status | Change rules without an ADR |

The reviewer prompt is: you are the skeptic. Find the hole. Cite the rule number.

Under PLANIT, the proposer also declares bindings for each atomic statement (or explicitly declares "no bindings necessary") before generation. The confirmer's gate verifies those bindings were held — it does not trust the proposer's label.

---

## 8. Repository shape

> **TODO (vocabulary):** "invariants" below → **adjectives**. Apply in the vocabulary pass.
>
> **ACS addition:** the AI compiler's output lives under `generated/` (or equivalent). Humans never edit it to "help." If a gate fails, RCA fixes the spec and the compiler regenerates. The tree below is the *shape* the compiler must emit; it is not a place for hand-maintained code.

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
├─ generated/                          # AI-compiled output; disposable; never hand-edited
└─ integrity/
    ├─ fitness/                        # lint/arch rules (the gates)
    └─ checklist.md                    # or generate from this document
```

`capabilities/` as a second tree is optional. Do not add `governance/`, `compliance/`, `risk/` folders unless a real artifact has nowhere else to live. Empty architecture folders are how charters rot.

---

## 9. What we took from the original "AI-First" sketch — and what we did not

> **TODO (vocabulary):** "invariants" / "laws" below → **adjectives**. Apply in the vocabulary pass.
>
> **ACS addition:** the original sketch assumed a human developer wrote the code. ACS assumes the AI *compiles* it from intent. What we took and rejected below still holds — the compiler is just the new author that must be kept honest by the same shape.

The original sketch was right about:

- Organize work so agents have a small, named unit of change
- Machine-readable contracts on boundaries
- Explicit dependencies aimed at "if I change X, what breaks?"
- Co-located tests
- ADRs as recorded decisions
- Validation as proof, not prose

The original sketch was weak where it:

- Named thirty "architectures" as peer systems
- Treated security, data, observability, audit, and evidence as sibling trees instead of annotations on nouns, verbs, and goals
- Put Agent concerns in a later tier even though agents are the primary consumer
- Assumed hand-maintained `dependency-graph.json` and `impact-analysis.json`
- Isolated goals without a noun, which scatters invariants and invites duplication
- Used "governance" as a bucket instead of a charter plus review

Those higher-level views (product, portfolio, strategy) can be derived later. They are not the foundation agents implement against. Under ACS, they are *requirements and ADRs* the interview consults — never a second implementation of a noun.

---

## 10. Pitfalls and remediations

> **TODO (vocabulary):** "invariant" / "law" below → **adjective**. Apply in the vocabulary pass.
>
> **ACS addition:** every pitfall below is now also a *compile failure*. The compiler that emits the pitfall fails its gate; RCA traces back to the spec, not the output.

### 10.1 Scattered invariants

**Pitfall.** "Cannot void after payment" lives in `VoidInvoice` and a slightly different version lives in `ApplyPayment`. An agent edits one.

**Remediation.** The adjective lives on `Invoice`. Both verbs consult it. Goal tests are not the home of the adjective. The gate fails if the status machine is reimplemented in a goal.

### 10.2 Duplication that looks locally correct

**Pitfall.** The agent's context is the current goal. It reimplements tax rounding. CI on that goal is green.

**Remediation.** R15 and R24. Money math has one module. Reviewer asks "where else does this formula exist?" Confirmer greps.

### 10.3 Conceptual changes treated as goal changes

**Pitfall.** "Allow partial payments" is implemented only in `ApplyPayment` the goal. `VoidInvoice` still assumes full-payment status values.

**Remediation.** Classification step. Conceptual change is class A. Proposer must open the noun and list every verb that assumes the old adjective.

### 10.4 Hidden coupling through shared data

**Pitfall.** Goals look independent. They write the same row. The call graph does not show that `status` means two things.

**Remediation.** Only verbs write. Generated impact includes "who calls this verb," not only "which goal folder changed." Shared tables are behind the noun's persistence adapter, not open to every goal.

### 10.5 Goal explosion or god-goal

**Pitfall.** One function per goal, or one goal that does the entire billing domain.

**Remediation.** R16 and the pass-through rule. Reviewer flags both. Sizing heuristic: a goal names a use-case a stakeholder would recognize; a verb names a state change the noun must survive.

### 10.6 God-noun

**Pitfall.** `Invoice.renderPdf`, `Invoice.sendReminder`, `Invoice.exportQuickBooks`.

**Remediation.** R4. If the verb does not need the adjective set, it is a goal or another noun. Reviewer checklist includes god-noun. Under ACS the compiler is rewarded for fat nouns — the own-state test (does this behavior read or write *this* noun's adjectives?) is what keeps it honest.

### 10.7 Two contract layers that drift

**Pitfall.** Goal input defines `balance` one way. Verb input defines it another.

**Remediation.** R11. Canonical type. Goal contract references it. Confirmer diffs schemas for same-named fields with different types.

### 10.8 Hand-maintained graphs that lie

**Pitfall.** `dependency-graph.json` is stale. Agents trust it.

**Remediation.** R21. Generate from imports, workflow definitions, and registered verb calls. If it cannot be generated, do not pretend the file is a source of truth.

### 10.9 Convention without enforcement

**Pitfall.** "Internals are private" is a README sentence. The third agent session writes `invoice.status = 'paid'` from a goal.

**Remediation.** R5, R6, R23. Language visibility, module boundaries, and a CI gate. Convention is not a boundary. Under ACS the compiler is the third agent session — the gate is what stops it.

### 10.10 Author grades its own homework

**Pitfall.** The same pass proposes and approves.

**Remediation.** Step 3 as a separate role. Review with rule numbers. "Looks good" is not evidence. Under ACS the compiler is also not the auditor — produce ≠ audit.

### 10.11 Workflow as a second domain model

**Pitfall.** Temporal workflow re-implements "when an invoice is paid" instead of calling `applyPayment`.

**Remediation.** R17–R18. Workflows compose goals; verbs keep the adjective. Reviewer asks where the status machine lives. Under ACS, workflow is a goal of goals — the same rule, no new citizen.

### 10.12 The compiler emits the pitfall with better traceability

**Pitfall.** AI-compiled code passes every test and still forks an adjective, because the interview never captured it. Traceability is excellent; the fork is silent.

**Remediation.** The gate, not the interview. R25a (taint lifetime) and R25b (non-OO escape hatches) catch the fork mechanically. RCA then tightens the interview so the next compile does not repeat it. Traceability without a gate is stationery.

---
