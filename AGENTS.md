# AGENTS.md

Standing instructions for any coding harness working in this repository.

## Practice

This repo is the central home for **Boundary-Based Programming**. Read [`CHARTER.md`](CHARTER.md) before changing theory, agent materials, or tools. Confirmable rules live in the charter; wishes are not rules.

Practice integrity (charter §5.8, [`integrity/PRINCIPLES.md`](integrity/PRINCIPLES.md)):

- Zero variance: prescribed actions only; hard gates; complete/incomplete.
- Every requirement has a binary audit; unbound and in-force-unbindable entries fail and are listed (`tools/audit-binding-matrix.py`).
- Every public boundary declares input, output, and failure mode.
- Stand-alone BBP branding; copy and re/unbrand useful shapes; do not import foreign brand integrity packages.

**Notion exit evidence required (P-020, S8).** Every produce package must include Notion page id(s) and exit status. Fitness refuses MET without this evidence; adversarial audit refuses PASS. Missing Notion evidence triggers `handoff_refused` with `NOTION_EXIT_EVIDENCE` in the defect log. Do not normalize leaving Notion for later.


## Layout

- `theory/` — rationale and history (OG draft is frozen under `theory/history/`)
- `agents/` — how agents apply the charter
- `tools/` — enforcement and scaffolding
- `examples/` — adopter samples
- `adrs/` — recorded decisions
- `integrity/` — principles, binding matrix, binary audits

Do not invent empty “governance / compliance / risk” trees. Put real artifacts where they belong.

## Portable agent content

Skills and portable instructions live under [`.agents/`](.agents/). Cursor-only rules stay under `.cursor/`. See project rule `agents-portable-ssot`.

## Memory files

- [`DESCRIBE.md`](DESCRIBE.md) — durable project facts for agents
- [`TODO`](TODO) — task queue (`☐` open, `✔ … @done(YY-MM-DD HH:MM)` when done)
