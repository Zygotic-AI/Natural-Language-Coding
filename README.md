# Boundary-Based Architecture

**Locally green, globally wrong — stopped.**

Agents write code that is correct in one file and false across the system. This repo is the compile gate for that failure: small boundaries, adjectives on the noun, verbs as the only mutation path, requirements bound before generate.

## Three names

| Name | What it is | What it is not |
|------|------------|----------------|
| **ACS** — AI-Compiled Systems | The whole thing. Goals and requirements in; BBP-shaped system out, or the build fails. | Not “AI manages my cluster.” |
| **BBP** — Boundary-Based Programming | The *shape* the compiler must emit. Nouns, verbs, adjectives, goals. | Not an invoice app. `examples/` are specimens for the gates. |
| **PLANIT** | The *process*: load, interview, plan, bind, close gaps, generate, prove. | Not a second charter. |

Charter SSOT: [`CHARTER.md`](CHARTER.md). Process pages: [`docs/ai-compiled-systems/`](docs/ai-compiled-systems/). Name card: [`docs/ai-compiled-systems/NAMES.md`](docs/ai-compiled-systems/NAMES.md).

**P / R / C** on rule ids: **P**rinciple (hub honesty), **R**equirement (charter shape), **C**onfirmation (this change). Hyphenated `P-020` is a different series.

## Start here

| Artifact | Role |
|----------|------|
| [`CHARTER.md`](CHARTER.md) | Rules |
| [`docs/ai-compiled-systems/`](docs/ai-compiled-systems/) | ACS + PLANIT |
| [`examples/`](examples/) | Specimens the gates scan |
| [`tools/`](tools/) | Gates and the impact-graph generator |
| [`TODO`](TODO) | Open work |
| [`DESCRIBE.md`](DESCRIBE.md) | Repo memory for agents |

This repo is a practice hub. Adopting application repos follow charter §8 (`domain/`, `goals/`, …). They do not copy `examples/invoice-*` as a product.

## Status

Working charter. Not a ratified organizational standard. Adoption “done” is charter §14.
