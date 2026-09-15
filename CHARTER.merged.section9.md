> **TODO (vocabulary):** "invariant" / "laws" → **adjective** throughout. Not applied in this pass; dedicated rename pass pending.
> **TODO (binder → gate):** "binder" as a noun is retired. **Binding** = planning act; **gate** = post-generation verification. Not applied here.
> **TODO (workflow-as-peer):** workflow listed as a peer. ACS: workflow is a goal-of-goals. Confirm before §4.4 / §5.5.

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

**ACS addition.** The original sketch's real gap wasn't the list of architectures — it was that nothing forced the output to be BBA-shaped, so agents generated whichever shape was easiest for the current goal. ACS closes that: the compile gate fails any output that isn't noun/verb/goal-shaped. "Isolated goals without a noun" (listed as a weakness above) is exactly what the gate prevents. "Governance as a bucket" is already renamed to charter plus review in §3.
