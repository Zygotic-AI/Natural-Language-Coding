# [ADR](../docs/TERMS.md#adr) 0011 — [Natural Language Coding](../docs/TERMS.md#nlc) product naming

- Status: Accepted
- Date: 2026-09-20
- Deciders: Human manager
- Class: F (product / documentation)

## Context

Running prose used **[ACS](../docs/TERMS.md#acs)** (AI-Compiled Systems) for both the product and the compile story. That collided with a separate need to name the **[compiler](../docs/TERMS.md#compiler)** vs the **artifact** it produces. Consumers also need one umbrella brand that is not an acronym soup.

## Decision

| Say | Meaning |
| ----- | -------- |
| **[Natural Language Coding](../docs/TERMS.md#nlc) (NLC)** | The product and this practice [hub](../docs/TERMS.md#hub): describe goals and requirements in natural language; compile or [refuse](../docs/TERMS.md#refuse). |
| **[AI system compiler](../docs/TERMS.md#compiler)** (optional **ASC**) | The worker: [interview](../docs/TERMS.md#interview), plan, bind, generate, [prove](../docs/TERMS.md#prove) (PLANIT + harness + gates). Prefer “the [compiler](../docs/TERMS.md#compiler)” in consumer copy. |
| **[Compiled system](../docs/TERMS.md#compiled-system)** (optional **ACS**) | The BBP-shaped runnable tree in an [adopter repo](../docs/TERMS.md#adopter)—not [hub](../docs/TERMS.md#hub) `examples/` specimens. |
| **[BBP](../docs/TERMS.md#bbp)** | Code shape the [compiler](../docs/TERMS.md#compiler) must emit (noun, verb, adjective, goal). |
| **[BBA](../docs/TERMS.md#bba)** | Roof architecture and [integrity](../docs/TERMS.md#integrity) rules in this [hub](../docs/TERMS.md#hub) (`CHARTER.md`, `integrity/`). Consumer docs mention [BBA](../docs/TERMS.md#bba) only as “under the covers.” |
| **[PLANIT](../docs/TERMS.md#planit)** | Orchestrated compile loop; invoke as `/planit` in Cursor. |

Retired in **consumer** prose: **[ACS](../docs/TERMS.md#acs) = whole product**. [Hub](../docs/TERMS.md#hub) technical docs may still say “[ACS](../docs/TERMS.md#acs) folder” as shorthand for `docs/nlc/compiler/` until paths are renamed.

**[NLC](../docs/TERMS.md#nlc)** is the default acronym for the whole project. **[ASC](../docs/TERMS.md#asc)** vs **[ACS](../docs/TERMS.md#acs)** appear only in glossary or integrator docs, never both unexplained in the same hero paragraph.

## Consequences

- Root `README.md` and [`docs/nlc/compiler/NAMES.md`](../docs/nlc/compiler/NAMES.md) follow this table.
- GitHub repo name **Natural-Language-Coding** matches the product name; legacy “Boundary-Based-Architecture” references are historical only.

## Supersedes

Informal “three names” row that equated [ACS](../docs/TERMS.md#acs) with the entire product story.
