# Names

Use these on purpose ([ADR 0011](../../adrs/0011-natural-language-coding-naming.md)). Do not stack them as synonyms.

| Say | When |
| ----- | ---- |
| **NLC** | The product: Natural Language Coding. |
| **Compiler** | Interview → plan → bind → generate → prove. Optional **ASC** in integrator docs only. |
| **Compiled system** | Runnable output in an adopter repo. Optional **ACS** = artifact only. |
| **BBP** | Emit shape: noun / verb / adjective / goal. |
| **PLANIT** | The orchestrated loop; `/planit` in Cursor. |

Consumer glossary: [GLOSSARY.md](GLOSSARY.md).

Retired in running prose: **ACS = whole product**; BBA as consumer hero (use BBP/BBA under the covers); AIMS (folded into NLC + PLANIT); workflow-as-peer (goals may call goals).

## Id prefixes (P, R, C)

| Letter | Word | Job |
|--------|------|-----|
| **P** | Principle | Hub integrity (P1–P7). Not the hyphenated `P-0xx` operating policies. |
| **R** | Requirement | Charter rule the code/shape must keep. |
| **C** | Confirmation | Checklist line on one change. |

Also: **S**/**CS** (agent-noun structure), **Q** (quality metric).

Specimens in `examples/` are not compiled systems. They exist so a gate can go red or green.
