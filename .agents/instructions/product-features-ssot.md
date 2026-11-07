# Product features SSOT (always)

When talking about what NLC already does, what it will do, the order of that work, or **why** a feature sits where it does, the living document is [`docs/nlc/FEATURES.md`](../../docs/nlc/FEATURES.md).

That file is not an architecture decision record. Records that must be enforced as law still go in `adrs/`. FEATURES.md keeps the story, use cases, and ordering reasons so a later teammate can argue with an agent from the same text instead of re-deriving it.

## Gate (default-closed)

| Criterion | Blocking? | Pass when |
| --------- | --------- | --------- |
| One story file | yes | Feature order and “why this order” are in FEATURES.md, not only in chat |
| Reasons travel with the feature | yes | A use case or ordering reason spoken in planning is written next to that feature in the same change |
| Upcoming vs milestone | yes | Thinking-about items stay under Upcoming; only the next few scheduled slices are Milestones |
| Law vs story | yes | A hard rule (“no harness hooks”) has or gets an ADR; FEATURES.md points at it |
| Operator words | yes | In conversation, use the operator’s names for features; do not rename them and then cite the new name |

## When you change the plan

Edit FEATURES.md in the same change. If the next milestone moved, say so there. Do not leave the reasons only in the transcript.

## Harness

Portable harnesses: this file via [`AGENTS.md`](../../AGENTS.md). Cursor may mirror a thin pointer under `.cursor/rules/`; **SSOT is this path**. `docs/nlc/FEATURES.md` is the story file.
