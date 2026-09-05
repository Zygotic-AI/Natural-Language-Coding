# Binding matrix

Maps every requirement in this repo to an audit and a binder. The binding matrix is the requirement index for this practice hub (requirement → audit → binder); it is not a dependency or impact graph, and R21 applies to generated “what breaks” views in adopting codebases, not to this file.

**In-force** means a fail-capable binder exists. Requirements without a binder stay `surface=reference` (still indexed, still have audit ids and audit markdown); they are not promoted to in-force until a binder can fail the change. Do not mark a row `bound` without that binder.

- Principles: [`PRINCIPLES.md`](PRINCIPLES.md)
- Machine index: [`binding-matrix.json`](binding-matrix.json)
- Ratified by: [`../adrs/0001-zero-variance-integrity.md`](../adrs/0001-zero-variance-integrity.md)

## Row fields

| Field | Required | Meaning |
|-------|----------|---------|
| `id` | yes | Requirement id (`P*`, `R*`, `C*`, …) |
| `statement` | yes | One-line statement |
| `surface` | yes | `in-force` \| `reference` \| `wish` |
| `audit_id` | yes | Audit that yields met / not met |
| `audit_def` | yes | Path to audit definition |
| `binder` | yes when bound | CI check, confirmer step, or tool id that can fail |
| `status` | yes | `bound` \| `unbound` |

`wish` rows are allowed only outside in-force surfaces (e.g. theory backlog). They still need `audit_id` once promoted.

## Mandatory audits of this matrix

### `A-BINDING-UNBOUND`

- **Met:** every row with `surface=in-force` has `status=bound` and a non-empty `binder`. Reference and wish rows may be unbound.
- **Not met:** any in-force row that is unbound or has an empty binder.
- **Report:** list every unbound in-force `id` (required on not met).

### `A-BINDING-PROMOTE`

- **Met:** every row with `surface=in-force` is `bound` and its binder can fail a change.
- **Not met:** any in-force row that is unbindable or unbound.
- **Report:** list every offending `id` (required on not met).

### `A-BINDING-COVERAGE`

- **Met:** every requirement id published in `CHARTER.md`, `integrity/PRINCIPLES.md`, and accepted ADRs appears as a matrix row with an `audit_id`.
- **Not met:** any published requirement missing from the matrix or missing `audit_id`.
- **Report:** list every missing `id`.

Do not mark a row `bound` or `in-force` early. Promote to in-force only when a fail-capable binder exists.
