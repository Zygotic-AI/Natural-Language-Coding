> **TODO (vocabulary):** "invariant" / "laws" → **adjective** throughout. Not applied in this pass; dedicated rename pass pending.
> **TODO (binder → gate):** "binder" as a noun is retired. **Binding** = planning act; **gate** = post-generation verification. Not applied here.
> **TODO (workflow-as-peer):** workflow listed as a peer. ACS: workflow is a goal-of-goals. Confirm before §4.4 / §5.5.

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

**ACS addition — PLANIT binding at each pitfall.** Every pitfall above is a failure the gate must catch, not a convention the agent must remember. The PLANIT bind step attaches the relevant rule (R-number or ADR) to the atomic plan step that could trigger it; the gate verifies after generation. Pitfall 10.9 (convention without enforcement) is the canonical case: a README sentence is not a boundary — the gate is.

**ACS addition — adjective lifetime.** Pitfalls 10.1, 10.2, 10.4, and 10.11 all reduce to one mechanism: an adjective's value must not outlive the verb that fetched it. The taint-lifetime gate (A5) catches the escape mechanically; the planner does not have to foresee it.

**How §10 works in the merge:** the pitfalls are unchanged BBA — they were already the right failure catalogue. ACS adds the binding: each pitfall maps to a gate check, and the planner declares which pitfall a given change could trigger before generation. The gate then proves it didn't.
