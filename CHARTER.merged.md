## 11. Confirmation checklist

> **TODO (vocabulary):** "Laws" / "invariant" / "law" below → **adjective**. Apply in the vocabulary pass.
>
> **ACS addition:** under PLANIT, the confirmer's gate also verifies the binding declarations from the proposal (each atomic statement bound to rules, or explicitly "no bindings necessary") and runs the taint-lifetime and escape-hatch checks (R25a, R25b). Those are not separate checklist items — they are how C4, C5, C16, C19, and C20 are *proven*, not just claimed.

An implementing agent must print this list with `PASS`, `FAIL`, or `N/A` and a pointer (file and symbol) for every non-N/A item. `N/A` requires a one-line reason.

### Classification and home

- [ ] C1. Change class (A–F) is stated.
- [ ] C2. Adjectives live on the noun named in C1, not in a goal folder.
- [ ] C3. New orchestration lives in a goal or workflow, not as a method on an unrelated noun.

### Mutation path

- [ ] C4. No assignment to noun fields occurs outside the noun module.
- [ ] C5. Every state change of a noun goes through a public verb.
- [ ] C6. No noun module imports a goal or workflow module.

### Contracts

- [ ] C7. Each changed public goal has input and output schemas.
- [ ] C8. Each changed public verb has input and output schemas.
- [ ] C9. Shared meanings use a shared type; no forked `balance` / `status` / `currency`.
- [ ] C10. Breaking schema changes have a new version and an ADR. New verb versions honor every adjective on the noun.

### Goal and workflow shape

- [ ] C11. Each changed goal has exactly one public entrypoint.
- [ ] C12. No goal imports another goal's internals.
- [ ] C13. No new goal exists whose only job is a single noun-verb with no I/O or policy — or an ADR explains why the wrapper exists.
- [ ] C14. Workflows call goals (or the ADR-chosen single exception is documented).
- [ ] C15. Verbs invoked from a retrying workflow are idempotent, or the workflow uses an idempotency key the verb honors.

### Adjectives and tests

- [ ] C16. Every adjective named in the proposal has a test on the noun.
- [ ] C17. Every new verb has tests for success, precondition failure, and adjective preservation.
- [ ] C18. Goal tests cover the use-case, not a copy of the noun's adjective suite.
- [ ] C19. No second implementation of the same adjective exists in the diff (search for duplicated predicates).
- [ ] C19a. No sensitive adjective's value is stored, passed to another boundary, or returned from the consuming verb (taint-lifetime gate).
- [ ] C19b. No non-OO escape hatch (raw SQL, ORM, deserialization, reflection) touches a noun's adjectives outside a published verb.

### Integrity of the change

- [ ] C20. Fitness / lint rules for R23 and R24 passed.
- [ ] C21. Impact list in the proposal matches generated callers of the changed verbs/goals.
- [ ] C22. Charter/ADR/code/contracts were updated in the same change if they were affected.
- [ ] C23. Adversarial review findings are all fixed or explicitly rebutted.
- [ ] C24. Ratification is recorded for classes that require it.
- [ ] C25. Binding declarations present for every atomic statement (or explicit "no bindings necessary").

If C4, C5, C9, C16, C19, C19a, C19b, or C20 fail, the change is not complete.

---
