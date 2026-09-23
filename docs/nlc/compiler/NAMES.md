# Names

Use these on purpose ([ADR 0011](../../../adrs/0011-natural-language-coding-naming.md)). Do not stack them as synonyms.

| Say | When |
| ----- | ---- |
| **[NLC](../../TERMS.md#nlc)** | The product: [Natural Language Coding](../../TERMS.md#nlc). |
| **[Compiler](../../TERMS.md#compiler)** | [Interview](../../TERMS.md#interview) → plan → bind → generate → [prove](../../TERMS.md#prove). Optional **[ASC](../../TERMS.md#asc)** in integrator docs only. |
| **[Compiled system](../../TERMS.md#compiled-system)** | Runnable output in an [adopter repo](../../TERMS.md#adopter). Optional **[ACS](../../TERMS.md#acs)** = artifact only. |
| **[BBP](../../TERMS.md#bbp)** | Emit shape: [noun](../../TERMS.md#noun) / verb / [adjective](../../TERMS.md#adjective) / [goal](../../TERMS.md#goal). |
| **[PLANIT](../../TERMS.md#planit)** | The orchestrated loop; `/planit` in Cursor. |

Consumer glossary: [GLOSSARY.md](GLOSSARY.md).

Retired in running prose: **[ACS](../../TERMS.md#acs) = whole product**; [BBA](../../TERMS.md#bba) as consumer hero (use BBP/BBA under the covers); [AIMS](../../TERMS.md#aims) (folded into NLC + PLANIT); workflow-as-peer (goals may call goals).

## Id prefixes (P, R, C)

| Letter | Word | Job |
|--------|------|-----|
| **P** | Principle | [Hub](../../TERMS.md#hub) [integrity](../../TERMS.md#integrity) (P1–P7). Not the hyphenated `P-0xx` operating policies. |
| **R** | [Requirement](../../TERMS.md#requirement) | [Charter](../../TERMS.md#charter) [rule](../../TERMS.md#rule) the code/shape must keep. |
| **C** | Confirmation | Checklist line on one change. |

Also: **S**/**CS** (agent-noun structure), **Q** (quality metric).

Specimens in `examples/` are not compiled systems. They exist so a [gate](../../TERMS.md#gate) can go red or green.
