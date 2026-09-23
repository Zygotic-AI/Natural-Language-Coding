# ADR 0033 — Charter contracts (R9–R12)

- Status: Accepted
- Date: 2026-09-23
- Deciders: Human manager
- Class: A (charter shape)
- Corpus: bba
- Ratifies: R9, R10, R11, R12

## Context

Contract presence, identity, and versioning were charter-only with binders; R12 breaking-change noise overlaps [ADR 0006](0006-contract-change-notice.md) but R9–R11 lacked a ratifying ADR.

## Decision

Adopt charter §5.3:

- **R9–R10:** Public goal entrypoints and noun-verbs have input and output contracts.
- **R11:** Same meaning → one definition, referenced.
- **R12:** Contracts are versioned; breaking changes need a new version and an ADR (loudness: ADR 0006).

## Consequences

- Backlog marks R9–R12 ratified by this ADR (R12 also cites 0006 for change notice).
- Binders unchanged.

## Rejected

- Duplicate independent field definitions across contracts.
