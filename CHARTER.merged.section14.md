> **TODO (vocabulary):** "invariant" / "laws" → **adjective** throughout. Not applied in this pass; dedicated rename pass pending.
> **TODO (binder → gate):** "binder" as a noun is retired. **Binding** = planning act; **gate** = post-generation verification. Not applied here.
> **TODO (workflow-as-peer):** workflow listed as a peer. ACS: workflow is a goal-of-goals. Confirm before §4.4 / §5.5.

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

**ACS addition.** Criterion 4 (fitness check 1 in CI) is the first gate that must exist before the rest counts as more than a style guide. Criterion 6 now requires the confirmer's checklist plus the independent adversarial audit (A1–A7) producing evidence. Until check 1 is real, treat everything above it as aspirational.
