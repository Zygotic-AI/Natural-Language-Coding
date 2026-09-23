# ADR 0032 — Charter ownership and mutation (R1–R8)

- Status: Accepted
- Date: 2026-09-23
- Deciders: Human manager
- Class: A (charter shape)
- Corpus: bba
- Ratifies: R1, R2, R3, R4, R5, R6, R7, R8

## Context

Ownership and mutation rules live as bare charter sentences with binders, but without a named ADR trail (A1 gap).

## Decision

Adopt charter §5.1–§5.2 as ratified law:

- **R1–R4:** Rule locality and goal vs noun placement (ownership).
- **R5–R8:** Noun fields private; mutation only via public verbs; nouns never call goals; goals read snapshots only.

Existing fitness binders remain the machine [gates](../docs/TERMS.md#gate). This ADR is the decision trail, not a new binder.

## Consequences

- Cited from CHARTER document control and [`integrity/charter-ratify-backlog.json`](../integrity/charter-ratify-backlog.json).
- No new R ids.

## Rejected

- Gluing cross-noun work onto the nearest noun (anti-R3).
