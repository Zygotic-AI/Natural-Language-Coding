# ADR 0006 — How loud a published-contract change is

- Status: Accepted
- Date: 2026-09-15
- Deciders: Human manager, Standards Steward
- Class: F (process + charter completeness)

## Context

ACS regenerates noun internals freely. A *published verb contract* is the edge other boundaries depend on. If that edge moves quietly, callers compile against a lie.

MERGE left one open item: how loud the notice to the manager should be. Too loud and the manager becomes the compiler. Too quiet and we spend the $100k again.

C10 already says breaking schema changes need a new version and an ADR. C21 already says the proposal’s impact list must match generated callers. This ADR is the volume knob, not a new citizen.

## Decision

**Loudness is the prove step staying red. It is not a chat ping and not a human edit of the generated contract.**

| Change | Loudness |
|--------|----------|
| Internals behind an unchanged contract | Silent. Regenerate. Manager is not in the file. |
| Additive / non-breaking (new optional input, new unused output field, new verb) | Quiet. Prove packet includes the generated impact graph. No extra sign-off. |
| Breaking (remove/rename field, change type, new required input, tighter postcondition, changed error meaning) | Loud: compile **incomplete** until (1) a requirement or ADR justifies the break, (2) generated callers are named in the plan, (3) the manager accepts the *requirement/ADR*, not the `.schema.json`. |

The manager is notified by a red prove, with callers listed from `tools/generate-impact-graph.py`. They do not patch `verbs.schema.json` to make it green.

If the behavior was wrong, the defect is the requirement, not the contract. Update the requirement, regenerate, prove again.

## Consequences

- COMPILER.md incomplete-generation bullet on contract change is this ADR.
- C10 and C21 stay the confirmer ticks. They stay unbound until a diff-scoped binder exists. Tree-wide schema presence is R9/R10, already bound.
- Additive changes must not page the manager.

## Rejected

- **Always-loud** — every regen interrupts the manager. The manager becomes the compiler.
- **Always-silent** — changelog only. Callers drift. Users find it.
- **Human edits the generated contract** — that is the architecture failing. RCA instead.
