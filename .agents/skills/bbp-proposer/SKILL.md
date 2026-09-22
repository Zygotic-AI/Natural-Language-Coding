---
name: [bbp-proposer](../../../docs/TERMS.md#bbp-proposer)
description: [BBP](../../../docs/TERMS.md#bbp) proposer — spec first, then implement to the ratified spec. Use when starting a [BBP](../../../docs/TERMS.md#bbp) change.
---

# [BBP](../../../docs/TERMS.md#bbp) Proposer

[Gate](../../../docs/TERMS.md#gate): `G-PROPOSE`. [PLANIT](../../../docs/TERMS.md#planit) steps 2–6 (plan through generate). [Charter](../../../docs/TERMS.md#charter) §§6–7.

SSOT role: [`agents/proposer.md`](../../../agents/proposer.md). Do not fork rules here.

Always on (charter §15): nouns own adjectives; only public verbs mutate; goals call verbs and other goals’ public entrypoints; never assign [noun](../../../docs/TERMS.md#noun) fields; do not approve your own proposal in the same pass.

**Complete:** proposal lists [change class](../../../docs/TERMS.md#change-class) A–F, nouns/verbs/goals touched, adjectives that must hold, non-goals, test names, impact list (generated callers, not a hand JSON).

**Generate:** at each adopted [rule](../../../docs/TERMS.md#rule) enforcement site emit `# nlc:rule=<rule_id>` ([ADR 0023](../../../adrs/0023-rule-instance-trace-and-instant-audit-scope.md)) via `./nlc maintainer rule-marker --id <rule_id>`; for `goals/<id>/implementation.py` finish with `./nlc maintainer rule-emit --goal <id>` so markers stay compiler-owned.

**Incomplete:** code in the same pass as the first proposal, or missing [change class](../../../docs/TERMS.md#change-class).
