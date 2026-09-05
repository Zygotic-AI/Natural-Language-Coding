# ADR 0001 — Zero-variance integrity for Boundary-Based Programming

- Status: Accepted
- Date: 2026-09-04
- Deciders: Richard Pickett

## Context

ADRs alone do not keep a practice honest. The BBP hub must stand alone (own branding, own artifacts). Every requirement and every prescribed action must be auditable with a binary outcome. Unbound requirements and wish-level rules are defects, not backlog flavor.

## Decision

1. **Stand-alone branding.** BBP owns its names, packages, and paths. External systems may be studied. If a shape is useful, copy and re/unbrand it into this repo. Do not import foreign brand packages or leave foreign brand names in BBP artifacts.

2. **Zero variance.** Every action by human or agent that changes this practice or an adopting system under BBP is dictated and prescribed. Informal “judgment calls” that skip a prescribed gate are failures.

3. **Hard gates.** Every step and every action has a hard gate that can be audited as **complete** or **incomplete** (no partial credit).

4. **Hard boundaries.** Every boundary declares hard input and output contracts, including whether it throws, returns an error result, or exits the process (when the boundary is code).

5. **Binary requirement audits.** Every requirement in this repo has an audit that can binarily determine **met** or **not met**. A requirement without such an audit is not a requirement yet — it is unbound.

6. **Binding matrix.** All requirements appear in the binding matrix with an audit id and a binder (check, confirmer step, or gate). An audit of the matrix **fails** if any entry is unbound. An audit of the matrix **lists** every unbound entry.

7. **Promote-only-when-bindable.** A requirement may be promoted into the charter (or other in-force surface) only when a binder exists that can fail. The promote audit **fails** and **lists** any in-force requirement that is not bindable.

## Consequences

- Charter gains confirmable rules for practice integrity (see §5.8).
- `integrity/binding-matrix` becomes mandatory SSOT for requirement → audit → binder.
- Tools and confirmer packs must emit PASS/FAIL with evidence pointers; “looks good” is not an outcome.
- Wish-level prose stays in `theory/` until bindable.

## Rejected

- Importing foreign-branded packages as dependencies of BBP integrity.
- Tolerating unbound charter rules as “aspirational.”
- Soft/warn-only gates as satisfaction of a hard gate.
