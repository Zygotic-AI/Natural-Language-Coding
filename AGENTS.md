# AGENTS.md

Standing instructions for any coding harness working in this repository.

## Practice

This repo is the central home for **[Boundary-Based Programming](docs/TERMS.md#bbp)**. Read [`CHARTER.md`](CHARTER.md) before changing theory, agent materials, or tools. Confirmable rules live in the [charter](docs/TERMS.md#charter); wishes are not rules.

Id prefixes: **P** = principle (hub honesty), **R** = [requirement](docs/TERMS.md#requirement) (charter shape), **C** = confirmation (this change). `P-0xx` (hyphen) is an operating policy in the companion bindings repo, not P1–P7.

Practice [integrity](docs/TERMS.md#integrity) (charter §5.8, [`integrity/PRINCIPLES.md`](integrity/PRINCIPLES.md)):

- [Zero variance](docs/TERMS.md#zero-variance): prescribed actions only; hard gates; complete/incomplete.
- Every [requirement](docs/TERMS.md#requirement) has a binary [audit](docs/TERMS.md#audit); unbound and in-force-unbindable entries fail and are listed (`tools/audit-binding-matrix.py`).
- Every public [boundary](docs/TERMS.md#boundary) declares input, output, and failure mode.
- Stand-alone [BBP](docs/TERMS.md#bbp) branding; copy and re/unbrand useful shapes; do not import foreign brand [integrity](docs/TERMS.md#integrity) packages.

**[SSOT exit evidence](docs/TERMS.md#ssot-exit-evidence) required (P-020, S8).** Every [produce package](docs/TERMS.md#produce-package) must include task/board [SSOT exit evidence](docs/TERMS.md#ssot-exit-evidence): `ssot_leaf_ids` (one or more opaque leaf ids) and `ssot_exit_status` (non-empty exit state string). Fitness refuses [MET](docs/TERMS.md#met) without this evidence; adversarial [audit](docs/TERMS.md#audit) refuses PASS. Missing [SSOT exit evidence](docs/TERMS.md#ssot-exit-evidence) triggers `handoff_refused` with `SSOT_EXIT_EVIDENCE` in the [defect](docs/TERMS.md#defect) log. Do not normalize leaving [SSOT exit evidence](docs/TERMS.md#ssot-exit-evidence) for later.

**Operating bindings.** P-series operating policies (P-016 handoff default-closed, P-020 SSOT exit evidence, P-030 raise-readiness refuse, etc.) live in the companion [`BBA-Bindings`](https://github.com/richardpickett/BBA-Bindings) repo. See [`docs/OPERATING_BINDINGS.md`](docs/OPERATING_BINDINGS.md) for the index and how to locate BINDING-MAP.


## Layout

- `theory/` — rationale and history (OG draft is frozen under `theory/history/`)
- `agents/` — how agents apply the [charter](docs/TERMS.md#charter); validate with [`tools/validate-agent-noun-packages.py`](tools/validate-agent-noun-packages.py)
- `tools/` — enforcement and scaffolding
- `examples/` — [adopter](docs/TERMS.md#adopter) samples
- `adrs/` — recorded decisions
- `integrity/` — principles, [binding matrix](docs/TERMS.md#binding-matrix), binary audits
- `content-types/` — type recipes for adding content (see [`content-types/HOW-TO-ADD.md`](content-types/HOW-TO-ADD.md))

## Contribution standards

Before adding or amending content, follow the [shared docs standard](docs/TERMS.md#shared-docs-standard) and [type recipe](docs/TERMS.md#type-recipe):

- [`integrity/CONTRIBUTION.md`](integrity/CONTRIBUTION.md) — [shared docs standard](docs/TERMS.md#shared-docs-standard) + [Contribution Gate](docs/TERMS.md#contribution-gate)
- [`integrity/LEXICON.md`](integrity/LEXICON.md) — locked term definitions
- [`content-types/HOW-TO-ADD.md`](content-types/HOW-TO-ADD.md) — type recipes (ADR, integrity doc, agent noun, audit, example)

[Contribution Gate](docs/TERMS.md#contribution-gate) [refuse](docs/TERMS.md#refuse) criteria (CG-R1 through CG-R7) apply to all [add-X](docs/TERMS.md#contribution-gate) contributions. No person names in SSOT surfaces (CG-R4); role language only.

Do not invent empty “governance / compliance / risk” trees. Put real artifacts where they belong.

## Portable agent content

Skills and portable instructions live under [`.agents/`](.agents/). End-to-end compile work: [`planit`](.agents/skills/planit/SKILL.md) ([`docs/nlc/compiler/PLANIT-ORCHESTRATION.md`](docs/nlc/compiler/PLANIT-ORCHESTRATION.md)). Cursor-only rules stay under `.cursor/`. See project [rule](docs/TERMS.md#rule) `agents-portable-ssot`.

**Version class:** Before material [hub](docs/TERMS.md#hub) or [adopter](docs/TERMS.md#adopter) changes, ask patch / minor / major when unclear — see [`.agents/instructions/change-version-class.md`](.agents/instructions/change-version-class.md). [Hub](docs/TERMS.md#hub) [ship](docs/TERMS.md#ship): human runs **`./release`** ([`docs/adoption/RELEASE.md`](docs/adoption/RELEASE.md)), not ad-hoc [tag](docs/TERMS.md#tag) commands.

**Product UC TODO:** Do not mark [`TODO`](TODO) “Build a compiled system” rows `@done` for full USE-CASE closure while [`docs/USE-CASES.md`](docs/USE-CASES.md) still lists Parked/Needed — see [`.agents/instructions/todo-product-uc-completion.md`](.agents/instructions/todo-product-uc-completion.md). CI: `tools/fitness-todo-use-cases-ssot.py`.

## Memory files

- [`DESCRIBE.md`](DESCRIBE.md) — durable project facts for agents
- [`TODO`](TODO) — task queue (`☐` open, `✔ … @done(YY-MM-DD HH:MM)` when done)
