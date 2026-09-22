# [ADR](../docs/TERMS.md#adr) 0006 — How loud a published-contract change is

- Status: Accepted
- Date: 2026-09-15
- Deciders: Human manager, Standards Steward
- Class: F (process + charter completeness)

## Context

[ACS](../docs/TERMS.md#acs) regenerates [noun](../docs/TERMS.md#noun) internals freely. A *[published verb contract](../docs/TERMS.md#published-verb-contract)* is the edge other boundaries depend on. If that edge moves quietly, callers compile against a lie.

MERGE left one open item: how loud the notice to the manager should be. Too loud and the manager becomes the [compiler](../docs/TERMS.md#compiler). Too quiet and we spend the $100k again.

C10 already says breaking schema changes need a new version and an [ADR](../docs/TERMS.md#adr). C21 already says the proposal’s impact list must match generated callers. This [ADR](../docs/TERMS.md#adr) is the volume knob, not a new citizen.

## Decision

**Loudness is the [prove](../docs/TERMS.md#prove) step staying red. It is not a chat ping and not a human edit of the generated [contract](../docs/TERMS.md#contract).**

| Change | Loudness |
|--------|----------|
| Internals behind an unchanged [contract](../docs/TERMS.md#contract) | Silent. Regenerate. Manager is not in the file. |
| Additive / non-breaking (new optional input, new unused output field, new verb) | Quiet. [Prove](../docs/TERMS.md#prove) packet includes the generated impact graph. No extra sign-off. |
| Breaking (remove/rename field, change type, new required input, tighter postcondition, changed error meaning) | Loud: compile **incomplete** until (1) a [requirement](../docs/TERMS.md#requirement) or [ADR](../docs/TERMS.md#adr) justifies the break, (2) generated callers are named in the plan, (3) the manager accepts the *requirement/ADR*, not the `.schema.json`. |

The manager is notified by a red [prove](../docs/TERMS.md#prove), with callers listed from `tools/generate-impact-graph.py`. They do not patch `verbs.schema.json` to make it green.

If the behavior was wrong, the [defect](../docs/TERMS.md#defect) is the [requirement](../docs/TERMS.md#requirement), not the [contract](../docs/TERMS.md#contract). Update the [requirement](../docs/TERMS.md#requirement), regenerate, [prove](../docs/TERMS.md#prove) again.

## Consequences

- [COMPILER](../docs/TERMS.md#compiler).md incomplete-generation bullet on [contract](../docs/TERMS.md#contract) change is this [ADR](../docs/TERMS.md#adr).
- C10 and C21 stay the [confirmer](../docs/TERMS.md#confirmer) ticks. They stay unbound until a diff-scoped binder exists. Tree-wide schema presence is R9/R10, already bound.
- Additive changes must not page the manager.

## Rejected

- **Always-loud** — every regen interrupts the manager. The manager becomes the [compiler](../docs/TERMS.md#compiler).
- **Always-silent** — changelog only. Callers drift. Users find it.
- **Human edits the generated [contract](../docs/TERMS.md#contract)** — that is the architecture failing. [RCA](../docs/TERMS.md#rca) instead.
