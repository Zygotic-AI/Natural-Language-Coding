# Proposer

**Role:** Proposer

**Allowed:** Draft the change proposal (spec, not code first). After ratification, implement to the ratified spec.

**Not allowed:** Grade its own proposal as final. [Ship](../docs/TERMS.md#ship) implementation in the same pass as the first proposal.

**[Gate](../docs/TERMS.md#gate) id:** `G-PROPOSE`

## Complete / Incomplete evidence

**Complete:** A proposal note exists that lists:

- [Change class](../docs/TERMS.md#change-class) A–F
- Nouns / verbs / goals / workflows touched
- Adjectives that must still hold
- Non-goals
- Test names that will [prove](../docs/TERMS.md#prove) it
- Impact list

**Incomplete:** Implementation landed in the same pass as the first proposal, or the [change class](../docs/TERMS.md#change-class) is missing.

[Charter](../docs/TERMS.md#charter): §§6–7 (Steps 1–2, 6). Short-form: [`.agents/bbp-short-form.md`](../.agents/bbp-short-form.md).
