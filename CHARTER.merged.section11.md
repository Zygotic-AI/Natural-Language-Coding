## 11. Confirmation checklist

> **TODO (carried forward):** vocabulary rename — "laws"/"invariants" → **adjective** is a whole-document pass, not applied locally here.
> **TODO (carried forward):** "binder" → **gate** (binding = planning act; gate = verification act). Not applied locally.
> **TODO (open):** workflow listed as a peer of noun/verb/goal. ACS says workflow is a goal-of-goals. Confirm before this lands.

Run after implementation. Every item is a hard gate: pass or fail, with evidence. No soft "mostly."

### Noun

- [ ] Every noun has identity, private state, and a short public verb list.
- [ ] Every invariant is expressed as a verb precondition, postcondition, or private check — not as a comment.
- [ ] No goal, workflow, or adapter assigns a noun field.
- [ ] No noun calls a goal or another noun's internals.
- [ ] Tests for the noun's invariants exist and pass on every verb.

### Verb

- [ ] Every public verb has an input contract, output contract, preconditions, postconditions.
- [ ] Every verb leaves the noun truthful (invariants hold after it runs).
- [ ] No verb is a pass-through that only calls another goal.
- [ ] Verbs are safe to retry if a workflow retries them (declared).

### Goal

- [ ] Every goal has one public entrypoint, an input contract, an output contract.
- [ ] No goal assigns noun fields or reimplements noun invariants.
- [ ] No goal imports another goal's internals.
- [ ] Goal tests cover the use-case; noun tests cover the noun.
- [ ] Pass-through goals are not invented; the noun-verb is exposed instead.

### Workflow

- [ ] Workflows compose goals; they do not call noun-verbs directly (unless ADR-stated exception).
- [ ] No hand-authored execution graph duplicates the workflow definition.
- [ ] Compensation and retries are declared where the workflow needs them.

### Contracts and drift

- [ ] Shared field meanings are defined once and referenced.
- [ ] No parallel `dependency-graph.json` or `impact-analysis.json` authored by hand.
- [ ] Generated impact/dependency views are present and current.
- [ ] ADRs that were superseded are marked, not deleted.

### Practice integrity

- [ ] `A-BINDING-COVERAGE` passes (no published requirement missing from the matrix).
- [ ] `A-BINDING-UNBOUND` passes (no in-force row lacks a binder).
- [ ] `A-BINDING-PROMOTE` passes (no in-force row is unbound).
- [ ] Every public boundary declares hard input, output, and failure mode.
- [ ] The charter, contracts, and code agree; disagreements fail the build.

### Agent loop

- [ ] The change was classified (A–F) before implementation.
- [ ] A proposal existed and was reviewed by a different role.
- [ ] Ratification is recorded (who, when, version).
- [ ] Implementation matches the ratified spec — no silent scope creep.
- [ ] This checklist was run and every item passed with evidence.

If any item fails, the change is failed. Do not ship, do not "fix later," do not normalize the failure into a note.

---

**ACS addition — gates, not wishes.** Every item above is a gate: default-closed, binary outcome, evidence required. An item with no registered gate is marked **unbound**, never passed. The PLANIT bind step attaches the relevant rule to each atomic plan step before generation; the gate verifies after. A step that finds no applicable rule must explicitly declare "no bindings applicable" — that declaration is itself a binding.

**ACS addition — independent audit.** The confirmer runs this checklist (one gate). The adversarial audit (A1–A7) is a second, independent pass: different agent, different question, does not trust the proposer's labels. It tracks adjective lifetimes and boundary crossings directly.

**How §11 works in the merge:** the checklist is unchanged BBA — it was already the right set of hard questions. ACS adds the gate semantics: default-closed, unbound-never-passed, and the binding declaration at plan time. The independent audit is the second prove gate from PLANIT, run after the confirmer.
