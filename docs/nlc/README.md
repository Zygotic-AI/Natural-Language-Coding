# [Natural Language Coding](../TERMS.md#nlc) — doc map

This repo is the **[hub](../TERMS.md#hub)**: the [compiler](../TERMS.md#compiler), gates, and skills. It does **not** [ship](../TERMS.md#ship) product requirements (no PCI, no HIPAA built-in). Adopters bring requirements via their own ADRs, rules, and **[requirement packs](../TERMS.md#requirement-pack)** (v0.2 — see [`TODO`](../../TODO)).

## Start here

| You want… | Go to |
| --------- | ----- |
| **What [NLC](../TERMS.md#nlc) is for (honest status)** | [`JOBS-TO-BE-DONE.md`](../JOBS-TO-BE-DONE.md) |
| **ADR → code enforcement tracker** | [`ADR-ENFORCEMENT.md`](../ADR-ENFORCEMENT.md) |
| **Terms dictionary** | [`TERMS.md`](../TERMS.md) |
| Install [NLC](../TERMS.md#nlc) | [Root `README.md`](../../README.md) → curl / PowerShell install |
| **Human menu (`nlc`)** | [`MENU.md`](MENU.md) — one entry, jargon-free, agent prompts |
| Five-minute flow | [`docs/ai-compiled-systems/GETTING-STARTED.md`](../ai-compiled-systems/GETTING-STARTED.md) |
| Adopt a new [app repo](../TERMS.md#adopter) | [`docs/adoption/BOOTSTRAP.md`](../adoption/BOOTSTRAP.md) |
| [Verify](../TERMS.md#verify) vs [ship](../TERMS.md#ship) (QA vs release) | [`VERIFY-AND-SHIP.md`](VERIFY-AND-SHIP.md), [`APP-VERIFY.md`](APP-VERIFY.md) |
| Human judgment (C24, adversarial, nouns) | [`HUMAN-JUDGMENT-GATES.md`](HUMAN-JUDGMENT-GATES.md) |
| Cut a [hub](../TERMS.md#hub) release | **`./release`** — [`docs/adoption/RELEASE.md`](../adoption/RELEASE.md) |

## Three layers

| Layer | Docs |
| ----- | ---- |
| **[NLC](../TERMS.md#nlc) (product)** | [`GLOSSARY.md`](../ai-compiled-systems/GLOSSARY.md), [`MANIFESTO.md`](../ai-compiled-systems/MANIFESTO.md), [`NAMES.md`](../ai-compiled-systems/NAMES.md) |
| **[Compiler](../TERMS.md#compiler)** | [`PROCESS.md`](../ai-compiled-systems/PROCESS.md), [`PLANIT-ORCHESTRATION.md`](../ai-compiled-systems/PLANIT-ORCHESTRATION.md), [`.agents/skills/planit/SKILL.md`](../../.agents/skills/planit/SKILL.md) |
| **[Compiled system](../TERMS.md#compiled-system) (your app)** | [`CHARTER.md`](../../CHARTER.md), [`docs/adoption/BROWNFIELD.md`](../adoption/BROWNFIELD.md) |

## Compile spine (tools)

| Topic | Doc / tool |
| ----- | ---------- |
| Impact graph & [UC9](../TERMS.md#uc9) [delta-regen](../TERMS.md#delta-regen-queue) | [`docs/spine/IMPACT-GRAPH.md`](../spine/IMPACT-GRAPH.md), [`tools/nlc-delta-regen.py`](../../tools/nlc-delta-regen.py) |
| [Rule](../TERMS.md#rule) adoption conflicts | [ADR](../TERMS.md#adr) 0012, [`tools/check-rule-adoption.py`](../../tools/check-rule-adoption.py) |
| [Knowledge domains](../TERMS.md#knowledge-domain) | [`tools/load-knowledge-domain.py`](../../tools/load-knowledge-domain.py), [`tools/nlc-before-generate.py`](../../tools/nlc-before-generate.py) |
| Rule-shape example (not hub requirements) | [`docs/worked-examples/pan-handling/`](../worked-examples/pan-handling/README.md) |
| Per-generate [gate](../TERMS.md#gate) receipts (ADR 0010 / R27) | [`GATE-RECORD-BINDER.md`](GATE-RECORD-BINDER.md), [`tools/nlc_gate_record.py`](../../tools/nlc_gate_record.py) |
| UC product SSOT | [`integrity/uc-product-status.json`](../../integrity/uc-product-status.json), [`fitness-todo-use-cases-ssot.py`](../../tools/fitness-todo-use-cases-ssot.py) |

### `./nlc maintainer` (compile-system v1)

| Command | UC | Notes |
| ------- | -- | ----- |
| `rule-runner --materialize` / `--check` | UC4 | `.nlc/rule-ir.snapshot.json` |
| `rule-emit --goal <id>` | UC5 / 0023 | Compiler-owned markers + provenance |
| `goal-scaffold --goal <id>` | UC5 / 0023 | Scaffold + stamp gate |
| `call-tree --sync` / `--check` | UC20 | Python `domain/` inventory |
| `primitive-propose --name <slug>` | UC12 | Proposed ADR before `primitives.md` |
| `brownfield-migrate --write-plan` / `--apply` | UC15 | After inventory |
| `pack-ingest <source.md>` | packs v0.2 | → `.nlc/pack-ingest-candidates.json` |
| `language-scan` | UC16 | Inventory only until LANGUAGE-SCANNER step 2 |

## Distribution

| Topic | Doc |
| ----- | --- |
| [Version store](../TERMS.md#version-store) & lock | [ADR](../TERMS.md#adr) 0015, [`integrity/schemas/nlc-lock.schema.json`](../../integrity/schemas/nlc-lock.schema.json) |
| Upgrades | [ADR](../TERMS.md#adr) 0014, [`tools/nlc-update.py`](../../tools/nlc-update.py), [`migrations/`](../../migrations/README.md) |

## Roadmap (hub)

| Version | Focus |
| ------- | ----- |
| **v0.1.0** | Install, lock, [greenfield](../TERMS.md#greenfield), spine v1, [verify](../TERMS.md#verify) path |
| **v0.2.0** | [Requirement](../TERMS.md#requirement) **packs** — [`REQUIREMENT-PACKS.md`](REQUIREMENT-PACKS.md), `nlc-pack-export.py` / `nlc-pack-install.py` |
| **Packs (types)** | **[Requirement packs](../TERMS.md#requirement-pack)** — ADRs + rules + facts. **[Code packs](../TERMS.md#code-pack)** — [UC16](../TERMS.md#uc16) scanner + [UC20](../TERMS.md#uc20) call-tree per stack (Python, Node, …). **[Rule IR](../TERMS.md#rule-ir)** — engine for [requirement packs](../TERMS.md#requirement-pack) (ADR 0007), not a [code pack](../TERMS.md#code-pack). |

## [Integrity](../TERMS.md#integrity) & decisions

| Topic | Location |
| ----- | -------- |
| [Charter](../TERMS.md#charter) (design SSOT) | [`CHARTER.md`](../../CHARTER.md) |
| ADRs | [`adrs/README.md`](../../adrs/README.md) |
| Open gaps | [`FINDINGS.md`](../../FINDINGS.md) |
| Task queue | [`TODO`](../../TODO) |
