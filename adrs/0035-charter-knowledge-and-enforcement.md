# ADR 0035 — Charter knowledge and enforcement (R20–R25, R32–R33)

- Status: Accepted
- Date: 2026-09-23
- Deciders: Human manager
- Class: A (charter shape)
- Corpus: bba
- Ratifies: R20, R21, R22, R23, R24, R25, R32, R33

## Context

Knowledge/drift and enforcement locality rules were bare charter + binders. Integrity zero-variance (R26–R31) already trails to [ADR 0001](0001-zero-variance-integrity.md).

## Decision

Adopt charter §5.6–§5.7 (plus R32–R33):

- **R20–R22:** Charter/contracts/code must agree; impact graphs are generated; superseded ADRs stay marked (trail).
- **R23–R25:** Gates fail illegal noun field writes / copied adjectives; noun adjective tests live with the noun.
- **R32–R33:** Taint single-boundary; no non-OO mutation escape hatches.

## Consequences

- Backlog marks these ids ratified by this ADR.
- R26–R31 remain under ADR 0001.
- Binders unchanged.

## Rejected

- Soft-failing enforcement for “temporary” escapes.
