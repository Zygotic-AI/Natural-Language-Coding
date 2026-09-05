# Agents

How Boundary-Based Programming is applied in agentic programming. Charter §§6–7 and §15 remain authoritative for the loop and short-form prompt.

## Role packs

| Role | File | Gate |
|------|------|------|
| Proposer | [`proposer.md`](proposer.md) | `G-PROPOSE` |
| Reviewer | [`reviewer.md`](reviewer.md) | `G-REVIEW` |
| Confirmer | [`confirmer.md`](confirmer.md) | `G-CONFIRM` |
| Recorder | [`recorder.md`](recorder.md) | `G-RECORD` |

Separate roles. One model may play them in sequence, but not in the same pass as both author and skeptic of its own work.

## Short-form prompt

[`.agents/bbp-short-form.md`](../.agents/bbp-short-form.md) — attribution copy of charter §15.

## Skills (optional pointers)

Thin Cursor/portable skills under [`.agents/skills/`](../.agents/skills/) point at these role files. They do not duplicate the full text. These instruction files are **not** fail-capable CI binders; do not mark P2/P3 bound because they exist.
