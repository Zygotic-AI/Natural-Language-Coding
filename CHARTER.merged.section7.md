## 7. Agent roles

> **TODO (vocabulary):** "invariant" → **adjective** throughout. Not applied in this pass; dedicated rename pass pending.
> **TODO (binder → gate):** "binder" as a noun is retired. **Binding** = planning act; **gate** = post-generation verification. Not applied here.
> **TODO (workflow-as-peer):** workflow listed as a peer role target. ACS: workflow is a goal-of-goals. Confirm before §4.4 / §5.5.

Separate roles. One model may play them in sequence, but not in the same pass as both author and skeptic of its own work.

| Role | Allowed to do | Not allowed to do |
|---|---|---|
| Proposer | Draft spec, then implement after ratification | Grade its own proposal as final |
| Reviewer | Attack the spec and the diff against this charter | Write the implementation in the same turn |
| Confirmer | Run checklist, report pass/fail with evidence | "Approve" without evidence |
| Recorder | Write ADRs and status | Change rules without an ADR |

The reviewer prompt is: you are the skeptic. Find the hole. Cite the rule number.

**ACS addition — binding declarations at propose.** Every atomic statement in the proposal points at the ADRs and requirements it must honor, or explicitly declares "no bindings applicable, reason." An empty declaration is itself a binding; the planner cannot skip the question. The gate later verifies the code held those bindings.

**ACS addition — independent audit.** The confirmer's checklist is one gate. The adversarial audit (A1–A7) is a second, independent pass: a different agent, different question. It does not trust the proposer's binding labels; it tracks adjective lifetimes and boundary crossings directly.
