# ADR 0014 — Semver upgrade steps; explicit no-op migrations

- Status: Accepted
- Date: 2026-09-20
- Deciders: Human manager
- Class: F (process / distribution)

## Context

NLC will ship as **versioned artifacts** (pip/npm mental model), not as a git submodule inside adopter repos. Upgrades advance **one semver step at a time** in the orchestrator (`1.2.2 → 1.2.3 → …`), with deterministic scripts and optional interview gates for conflicts.

If a release has **no** adopter-contract migration, operators cannot tell whether that is intentional or a **missing** migration file. Absence is ambiguous.

## Decision

1. **Adjacent semver coverage:** For every published hub version `vX.Y.Z`, there must be a migration unit for the step **from the previous published semver** `(X.Y.(Z-1) or prior minor/patch per semver rules)` → `X.Y.Z`. The upgrade orchestrator refuses to skip a step that has no unit.

2. **No-op is explicit:** When an upgrade changes only the hub artifact (replace tree, lock bump) and does not mutate adopter intent or schema, the migration unit still exists and is marked **`kind: noop`** internally. A missing unit is **not** treated as no-op.

3. **Logging (normative):** Each step emits machine- and human-visible lines:
   - Start: `UPGRADE:STEP from=<semver> to=<semver> kind=<noop|script|interview>`
   - Success: `UPGRADE:STEP_COMPLETED to=<semver>`
   - Failure: `UPGRADE:STEP_FAILED to=<semver>` (non-zero exit; do not advance lock)
   - Optional summary: `UPGRADE:MET to=<semver>` when the full chain to the target finishes.

   Human-facing text may mirror the same facts (e.g. `upgrading to v1.2.3… completed`).

4. **Fail closed:** If the orchestrator needs step `1.2.2 → 1.2.3` and no migration unit is present, emit `UPGRADE:NOT_MET` with `  missing: migration 1.2.2_to_1.2.3` (and list any other gaps), then exit non-zero. Same spirit as ADR 0013 (list all gaps, one failure).

5. **Hub replace vs migrate:** No-op (and most steps) still **replace** the hub artifact from the target version’s bundle. The migration unit governs **adopter contract** changes and **declared** interview gates—not editing files inside the shipped hub tree by hand.

6. **Distribution (directional):** Consumer install/update uses immutable release artifacts and a project **lock** pin; `nlc update` runs the semver chain. Two layouts: per-repo install (default) and workspace-root shared store. Detail lands in adoption docs and tools when implemented.

## Consequences

- Maintainers ship an empty or `noop` migration entry for every release, even patch-only hub swaps.
- CI on tag must verify the migration graph is complete for the new version (gate to be added with `nlc update`).
- [`migrations/README.md`](../migrations/README.md) describes the unit shape until the orchestrator exists.

## Rejected

- **Implicit no-op** when a migration file is absent.
- **Silent skip** of semver hops without a logged `UPGRADE:STEP` line per hop.
