# Proposer

**Role:** Proposer

**Allowed:** Draft the change proposal (spec, not code first). After ratification, implement to the ratified spec.

**Not allowed:** Grade its own proposal as final. Ship implementation in the same pass as the first proposal.

**Gate id:** `G-PROPOSE`

## Complete / Incomplete evidence

**Complete:** A proposal note exists that lists:

- Change class A–F
- Nouns / verbs / goals / workflows touched
- Invariants that must still hold
- Non-goals
- Test names that will prove it
- Impact list

**Incomplete:** Implementation landed in the same pass as the first proposal, or the change class is missing.

Charter: §§6–7 (Steps 1–2, 6). Short-form: [`.agents/bbp-short-form.md`](../.agents/bbp-short-form.md).
