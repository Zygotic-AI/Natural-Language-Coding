# Natural Language Coding — doc map

This repo is the **hub**: the compiler, gates, and skills. It does **not** ship product requirements (no PCI, no HIPAA built-in). Adopters bring requirements via their own ADRs, rules, and **requirement packs** (v0.2 — see [`TODO`](../../TODO)).

## Start here

| You want… | Go to |
| --------- | ----- |
| Install NLC | [Root `README.md`](../../README.md) → curl / PowerShell install |
| Five-minute flow | [`docs/ai-compiled-systems/GETTING-STARTED.md`](../ai-compiled-systems/GETTING-STARTED.md) |
| Adopt a new app repo | [`docs/adoption/BOOTSTRAP.md`](../adoption/BOOTSTRAP.md) |
| Prove vs ship (QA vs release) | [`PROVE-AND-SHIP.md`](PROVE-AND-SHIP.md) |
| Cut a hub release | [`docs/adoption/RELEASE-v0.1.0.md`](../adoption/RELEASE-v0.1.0.md) + `bash scripts/nlc-release-prep.sh` |

## Three layers

| Layer | Docs |
| ----- | ---- |
| **NLC (product)** | [`GLOSSARY.md`](../ai-compiled-systems/GLOSSARY.md), [`MANIFESTO.md`](../ai-compiled-systems/MANIFESTO.md), [`NAMES.md`](../ai-compiled-systems/NAMES.md) |
| **Compiler** | [`PROCESS.md`](../ai-compiled-systems/PROCESS.md), [`PLANIT-ORCHESTRATION.md`](../ai-compiled-systems/PLANIT-ORCHESTRATION.md), [`.agents/skills/planit/SKILL.md`](../../.agents/skills/planit/SKILL.md) |
| **Compiled system (your app)** | [`CHARTER.md`](../../CHARTER.md), [`docs/adoption/BROWNFIELD.md`](../adoption/BROWNFIELD.md) |

## Compile spine (tools)

| Topic | Doc / tool |
| ----- | ---------- |
| Impact graph & UC9 delta-regen | [`docs/spine/IMPACT-GRAPH.md`](../spine/IMPACT-GRAPH.md), [`tools/nlc-delta-regen.py`](../../tools/nlc-delta-regen.py) |
| Rule adoption conflicts | ADR 0012, [`tools/check-rule-adoption.py`](../../tools/check-rule-adoption.py) |
| Knowledge domains | [`tools/load-knowledge-domain.py`](../../tools/load-knowledge-domain.py), [`tools/nlc-before-generate.py`](../../tools/nlc-before-generate.py) |
| Rule-shape example (not hub requirements) | [`docs/worked-examples/pan-handling/`](../worked-examples/pan-handling/README.md) |

## Distribution

| Topic | Doc |
| ----- | --- |
| Version store & lock | ADR 0015, [`integrity/schemas/nlc-lock.schema.json`](../../integrity/schemas/nlc-lock.schema.json) |
| Upgrades | ADR 0014, [`tools/nlc-update.py`](../../tools/nlc-update.py), [`migrations/`](../../migrations/README.md) |

## Roadmap (hub)

| Version | Focus |
| ------- | ----- |
| **v0.1.0** | Install, lock, greenfield, spine v1, prove path |
| **v0.2.0** | Requirement **packs** (ingest → ratify → export → consume) — see [`TODO`](../../TODO) |
| **Packs (types)** | **Requirement packs** — ADRs + rules + facts. **Language packs** — UC16 scanner + UC20 call-tree per stack (Python, Node, …). **Rule IR** — engine for requirement packs (ADR 0007), not a language pack. |

## Integrity & decisions

| Topic | Location |
| ----- | -------- |
| Charter (design SSOT) | [`CHARTER.md`](../../CHARTER.md) |
| ADRs | [`adrs/README.md`](../../adrs/README.md) |
| Open gaps | [`FINDINGS.md`](../../FINDINGS.md) |
| Task queue | [`TODO`](../../TODO) |
