# AGENTS.md

Standing instructions for any coding harness working in this repository.

## Practice

This repo is the central home for **Boundary-Based Programming**. Read [`CHARTER.md`](CHARTER.md) before changing theory, agent materials, or tools. Confirmable rules live in the charter; wishes are not rules.

Practice integrity (charter §5.8, [`integrity/PRINCIPLES.md`](integrity/PRINCIPLES.md)):

- Zero variance: prescribed actions only; hard gates; complete/incomplete.
- Every requirement has a binary audit; unbound and in-force-unbindable entries fail and are listed (`tools/audit-binding-matrix.py`).
- Every public boundary declares input, output, and failure mode.
- Stand-alone BBP branding; copy and re/unbrand useful shapes; do not import foreign brand integrity packages.

**SSOT exit evidence required (P-020, S8).** Every produce package must include task/board SSOT exit evidence: `ssot_leaf_ids` (one or more opaque leaf ids) and `ssot_exit_status` (non-empty exit state string). Fitness refuses MET without this evidence; adversarial audit refuses PASS. Missing SSOT exit evidence triggers `handoff_refused` with `SSOT_EXIT_EVIDENCE` in the defect log. Do not normalize leaving SSOT exit evidence for later.


## Layout

- `theory/` — rationale and history (OG draft is frozen under `theory/history/`)
- `agents/` — how agents apply the charter; validate with [`tools/validate-agent-noun-packages.py`](tools/validate-agent-noun-packages.py)
- `tools/` — enforcement and scaffolding
- `examples/` — adopter samples
- `adrs/` — recorded decisions
- `integrity/` — principles, binding matrix, binary audits
- `content-types/` — type recipes for adding content (see [`content-types/HOW-TO-ADD.md`](content-types/HOW-TO-ADD.md))

## Contribution standards

Before adding or amending content, follow the shared docs standard and type recipe:

- [`integrity/CONTRIBUTION.md`](integrity/CONTRIBUTION.md) — shared docs standard + Contribution Gate
- [`integrity/LEXICON.md`](integrity/LEXICON.md) — locked term definitions
- [`content-types/HOW-TO-ADD.md`](content-types/HOW-TO-ADD.md) — type recipes (ADR, integrity doc, agent noun, audit, example)

Contribution Gate refuse criteria (CG-R1 through CG-R7) apply to all add-X contributions. No person names in SSOT surfaces (CG-R4); role language only.

Do not invent empty “governance / compliance / risk” trees. Put real artifacts where they belong.

## Portable agent content

Skills and portable instructions live under [`.agents/`](.agents/). Cursor-only rules stay under `.cursor/`. See project rule `agents-portable-ssot`.

## Memory files

- [`DESCRIBE.md`](DESCRIBE.md) — durable project facts for agents
- [`TODO`](TODO) — task queue (`☐` open, `✔ … @done(YY-MM-DD HH:MM)` when done)
