---
name: bbp-proposer
description: BBP proposer — spec first, then implement to the ratified spec. Use when starting a BBP change.
---

# BBP Proposer

Gate: `G-PROPOSE`. PLANIT steps 2–6 (plan through generate). Charter §§6–7.

SSOT role: [`agents/proposer.md`](../../../agents/proposer.md). Do not fork rules here.

Always on (charter §15): nouns own adjectives; only public verbs mutate; goals call verbs and other goals’ public entrypoints; never assign noun fields; do not approve your own proposal in the same pass.

**Complete:** proposal lists change class A–F, nouns/verbs/goals touched, adjectives that must hold, non-goals, test names, impact list (generated callers, not a hand JSON).

**Incomplete:** code in the same pass as the first proposal, or missing change class.
