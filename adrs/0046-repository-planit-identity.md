# ADR 0046 — Repository Planit identity

- Status: Proposed
- Note: Pending a redraft.
- Date: 2026-10-08
- Deciders: Human manager
- Ratified-by: Human manager (practice-enforcement task list, 2026-10-08)
- Class: F (process)
- Corpus: nlc

## Context

Two Planit skills can share the name `planit`. A harness that loads a different skill still looks like it ran `/planit`. Planning then follows another repository's procedure while this hub's architecture decision records stay unread.

## Decision

1. The canonical skill is `.agents/skills/planit/SKILL.md`.
2. `integrity/planit-skill-registry.json` stores that path and the SHA-256 of the file bytes.
3. Intake fails when the loaded path or the loaded bytes do not match the registry.
4. Every Planit handoff records `planit_skill_path` and `planit_skill_sha256`.
5. Cursor blocks prompt submit through `.cursor/hooks/nlc-planit-identity.sh` when the on-disk skill does not match. Other harnesses run `python3 tools/fitness-planit-identity.py --skill-only --loaded .agents/skills/planit/SKILL.md`.
6. `.nlc/planit-change-evidence.json` records that identity and a hash of the tree. A code change that does not refresh the evidence fails the hub compile.

## Consequences

- A negative fixture loads a different skill path and different bytes and must fail.
- Version class for this policy is minor.

## Rejected

- Trusting the skill name without a content hash.
- Letting a harness skip the check because it already has some Planit skill in context.
