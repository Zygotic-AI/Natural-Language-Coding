# ADR 0011 — Natural Language Coding product naming

- Status: Accepted
- Date: 2026-09-20
- Deciders: Human manager
- Class: F (product / documentation)

## Context

Running prose used **ACS** (AI-Compiled Systems) for both the product and the compile story. That collided with a separate need to name the **compiler** vs the **artifact** it produces. Consumers also need one umbrella brand that is not an acronym soup.

## Decision

| Say | Meaning |
| ----- | -------- |
| **Natural Language Coding (NLC)** | The product and this practice hub: describe goals and requirements in natural language; compile or refuse. |
| **AI system compiler** (optional **ASC**) | The worker: interview, plan, bind, generate, prove (PLANIT + harness + gates). Prefer “the compiler” in consumer copy. |
| **Compiled system** (optional **ACS**) | The BBP-shaped runnable tree in an adopter repo—not hub `examples/` specimens. |
| **BBP** | Code shape the compiler must emit (noun, verb, adjective, goal). |
| **BBA** | Roof architecture and integrity rules in this hub (`CHARTER.md`, `integrity/`). Consumer docs mention BBA only as “under the covers.” |
| **PLANIT** | Orchestrated compile loop; invoke as `/planit` in Cursor. |

Retired in **consumer** prose: **ACS = whole product**. Hub technical docs may still say “ACS folder” as shorthand for `docs/ai-compiled-systems/` until paths are renamed.

**NLC** is the default acronym for the whole project. **ASC** vs **ACS** appear only in glossary or integrator docs, never both unexplained in the same hero paragraph.

## Consequences

- Root `README.md` and [`docs/ai-compiled-systems/NAMES.md`](../docs/ai-compiled-systems/NAMES.md) follow this table.
- GitHub repo name **Natural-Language-Coding** matches the product name; legacy “Boundary-Based-Architecture” references are historical only.

## Supersedes

Informal “three names” row that equated ACS with the entire product story.
