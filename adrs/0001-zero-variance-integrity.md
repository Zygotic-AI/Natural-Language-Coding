# [ADR](../docs/TERMS.md#adr) 0001 — [Zero-variance](../docs/TERMS.md#zero-variance) [integrity](../docs/TERMS.md#integrity) for [Boundary-Based Programming](../docs/TERMS.md#bbp)

- Status: Accepted
- Date: 2026-09-04
- Deciders: Richard Pickett

## Context

ADRs alone do not keep a practice honest. The [BBP](../docs/TERMS.md#bbp) [hub](../docs/TERMS.md#hub) must stand alone (own branding, own artifacts). Every [requirement](../docs/TERMS.md#requirement) and every prescribed [action](../docs/TERMS.md#action) must be auditable with a binary outcome. Unbound requirements and wish-level rules are defects, not backlog flavor.

## Decision

1. **Stand-alone branding.** [BBP](../docs/TERMS.md#bbp) owns its names, packages, and paths. External systems may be studied. If a shape is useful, copy and re/unbrand it into this repo. Do not import foreign brand packages or leave foreign brand names in [BBP](../docs/TERMS.md#bbp) artifacts.

2. **[Zero variance](../docs/TERMS.md#zero-variance).** Every [action](../docs/TERMS.md#action) by human or agent that changes this practice or an adopting system under [BBP](../docs/TERMS.md#bbp) is dictated and prescribed. Informal “judgment calls” that skip a prescribed [gate](../docs/TERMS.md#gate) are failures.

3. **Hard gates.** Every step and every [action](../docs/TERMS.md#action) has a hard [gate](../docs/TERMS.md#gate) that can be audited as **complete** or **incomplete** (no partial credit).

4. **Hard boundaries.** Every [boundary](../docs/TERMS.md#boundary) declares hard input and output contracts, including whether it throws, returns an error result, or exits the process (when the boundary is code).

5. **Binary [requirement](../docs/TERMS.md#requirement) audits.** Every [requirement](../docs/TERMS.md#requirement) in this repo has an [audit](../docs/TERMS.md#audit) that can binarily determine **[met](../docs/TERMS.md#met)** or **not [met](../docs/TERMS.md#met)**. A [requirement](../docs/TERMS.md#requirement) without such an [audit](../docs/TERMS.md#audit) is not a [requirement](../docs/TERMS.md#requirement) yet — it is unbound.

6. **[Binding matrix](../docs/TERMS.md#binding-matrix).** All requirements appear in the [binding matrix](../docs/TERMS.md#binding-matrix) with an [audit](../docs/TERMS.md#audit) id and a binder (check, confirmer step, or gate). An [audit](../docs/TERMS.md#audit) of the matrix **fails** if any entry is unbound. An [audit](../docs/TERMS.md#audit) of the matrix **lists** every unbound entry.

7. **Promote-only-when-bindable.** A [requirement](../docs/TERMS.md#requirement) may be promoted into the [charter](../docs/TERMS.md#charter) (or other in-force surface) only when a binder exists that can fail. The promote [audit](../docs/TERMS.md#audit) **fails** and **lists** any in-force [requirement](../docs/TERMS.md#requirement) that is not bindable.

## Consequences

- [Charter](../docs/TERMS.md#charter) gains confirmable rules for practice [integrity](../docs/TERMS.md#integrity) (see §5.8).
- `integrity/binding-matrix` becomes mandatory SSOT for [requirement](../docs/TERMS.md#requirement) → [audit](../docs/TERMS.md#audit) → binder.
- Tools and [confirmer](../docs/TERMS.md#confirmer) packs must emit PASS/FAIL with evidence pointers; “looks good” is not an outcome.
- Wish-level prose stays in `theory/` until bindable.

## Rejected

- Importing foreign-branded packages as dependencies of [BBP](../docs/TERMS.md#bbp) [integrity](../docs/TERMS.md#integrity).
- Tolerating unbound [charter](../docs/TERMS.md#charter) rules as “aspirational.”
- Soft/warn-only gates as satisfaction of a hard [gate](../docs/TERMS.md#gate).
