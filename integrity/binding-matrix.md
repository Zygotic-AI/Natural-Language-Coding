# [Binding matrix](../docs/TERMS.md#binding-matrix)

Maps every [requirement](../docs/TERMS.md#requirement) in this repo to an [audit](../docs/TERMS.md#audit) and a binder. The [binding matrix](../docs/TERMS.md#binding-matrix) is the [requirement](../docs/TERMS.md#requirement) index for this practice [hub](../docs/TERMS.md#hub) (requirement → audit → binder); it is not a dependency or impact graph, and R21 applies to generated “what breaks” views in adopting codebases, not to this file.

**In-force** means a fail-capable binder exists. Requirements without a binder stay `surface=reference` (still indexed, still have audit ids and audit markdown); they are not promoted to in-force until a binder can fail the change. Do not mark a row `bound` without that binder.

- Principles: [`PRINCIPLES.md`](PRINCIPLES.md)
- Machine index: [`binding-matrix.json`](binding-matrix.json)
- Ratified by: [`../adrs/0001-zero-variance-integrity.md`](../adrs/0001-zero-variance-integrity.md)

## Row fields

| Field | Required | Meaning |
|-------|----------|---------|
| `id` | yes | [Requirement](../docs/TERMS.md#requirement) id. Prefix: **P** principle, **R** [charter](../docs/TERMS.md#charter) [requirement](../docs/TERMS.md#requirement), **C** confirmation checklist, **S**/**CS** agent-noun structure, **Q** [quality](../docs/TERMS.md#quality). Hyphenated `P-0xx` is a different series (operating policy). |
| `statement` | yes | One-line statement |
| `surface` | yes | `in-force` \| `reference` \| `wish` |
| `audit_id` | yes | [Audit](../docs/TERMS.md#audit) that yields [met](../docs/TERMS.md#met) / not [met](../docs/TERMS.md#met) |
| `audit_def` | yes | Path to [audit](../docs/TERMS.md#audit) definition |
| `binder` | yes when bound | CI check, [confirmer](../docs/TERMS.md#confirmer) step, or tool id that can fail |
| `status` | yes | `bound` \| `unbound` |

`wish` rows are allowed only outside in-force surfaces (e.g. theory backlog). They still need `audit_id` once promoted.

## Mandatory audits of this matrix

### `A-BINDING-UNBOUND`

- **[Met](../docs/TERMS.md#met):** every row with `surface=in-force` has `status=bound` and a non-empty `binder`. Reference and wish rows may be unbound.
- **Not [met](../docs/TERMS.md#met):** any in-force row that is unbound or has an empty binder.
- **Report:** list every unbound in-force `id` (required on not met).

### `A-BINDING-PROMOTE`

- **[Met](../docs/TERMS.md#met):** every row with `surface=in-force` is `bound` and its binder can fail a change.
- **Not [met](../docs/TERMS.md#met):** any in-force row that is unbindable or unbound.
- **Report:** list every offending `id` (required on not met).

### `A-BINDING-COVERAGE`

- **[Met](../docs/TERMS.md#met):** every [requirement](../docs/TERMS.md#requirement) id published in `CHARTER.md`, `integrity/PRINCIPLES.md`, and accepted ADRs appears as a matrix row with an `audit_id`.
- **Not [met](../docs/TERMS.md#met):** any published [requirement](../docs/TERMS.md#requirement) missing from the matrix or missing `audit_id`.
- **Report:** list every missing `id`.

Do not mark a row `bound` or `in-force` early. Promote to in-force only when a fail-capable binder exists.
