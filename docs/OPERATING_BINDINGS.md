# Operating bindings index (hub-local)

Index of **P-0xx** operating policies consumed by agent processes in this repository. Full [charter](TERMS.md#charter) rules remain in [`CHARTER.md`](../CHARTER.md); this document is the SSOT for operating-policy prose referenced by [`AGENTS.md`](../AGENTS.md), [`integrity/ACTIONS.md`](../integrity/ACTIONS.md), and [`integrity/GATE.md`](../integrity/GATE.md).

## Architecture note

**[NLC](TERMS.md#nlc)** is the product roof. **[BBA](TERMS.md#bba)** is the under-covers integrity architecture in this repo (`CHARTER.md`, `integrity/`, `agents/`). **Operating bindings** are P-series policies that wire [refuse](TERMS.md#refuse) criteria and evidence requirements to executable gates—indexed here, not in an external companion repo.

## Operating policy index (P-016…P-031 class)

| Policy | Name | Purpose |
|--------|------|---------|
| **P-015** | Bot-auditable packages | PR packages must be fully bot-auditable |
| **P-016** | Produce→fitness [handoff](TERMS.md#handoff) [default-closed](TERMS.md#default-closed) | Producers cannot claim ready without complete [produce package](TERMS.md#produce-package); `handoff_refused` not `FAIL` |
| **[P-020](TERMS.md#ssot-exit-evidence)** | [SSOT exit evidence](TERMS.md#ssot-exit-evidence) required | Produce packages require `ssot_leaf_ids` + `ssot_exit_status`; missing evidence triggers [refuse](TERMS.md#refuse) |
| **P-024** | Decision grain | One board leaf = one decision; fitness refuses duplicate leaf-create |
| **P-030** | Raise-readiness [refuse](TERMS.md#refuse) | R3/R4 checks; incomplete raise packets must [REFUSE](TERMS.md#refuse) at raise-readiness [handoff](TERMS.md#handoff) |
| **P-031** | Promote release packet [refuse](TERMS.md#refuse) | Incomplete promote packets must [refuse](TERMS.md#refuse) greenlight |

### P-016 (Produce→fitness handoff default-closed) — [ADR](TERMS.md#adr) 0004

- [Charter](TERMS.md#charter) [rule](TERMS.md#rule): S7, CS7
- [Handoff](TERMS.md#handoff): `handoff_refused` (produce-incomplete) ≠ `FAIL` (content defect)

### [P-020](TERMS.md#ssot-exit-evidence) (SSOT exit evidence) — [ADR](TERMS.md#adr) 0005

- [Charter](TERMS.md#charter) [rule](TERMS.md#rule): S8, CS8
- Evidence: `ssot_leaf_ids` (one or more opaque leaf ids) + `ssot_exit_status` (non-empty exit state string)
- [Refuse](TERMS.md#refuse): Fitness refuses [MET](TERMS.md#met); adversarial [audit](TERMS.md#audit) refuses PASS (same class as P-016)

### P-030 (Raise-readiness refuse)

- Raise-readiness [handoff](TERMS.md#handoff) must validate §7 (Owner/Path/Verification), R3, and R4 with concrete content—not field presence only
- Fixture **15855 without §7/R3/R4** must FAIL any raise-readiness path (see [`integrity/BOUNDARY.md`](../integrity/BOUNDARY.md))
- G2 in [`integrity/GATE.md`](../integrity/GATE.md) is [refuse-wired](TERMS.md#default-closed) to this policy in this repo

### P-031 (Promote release packet refuse)

- [Refuse](TERMS.md#refuse) on promote greenlight/fitness [MET](TERMS.md#met) unless five fields are present and valid: `change_ref`, `what_changed`, `prove_steps`, `uat_tip_marker`, `result`

## Cross-references

- [`CHARTER.md`](../CHARTER.md) — NLC-roof charter
- [`integrity/binding-matrix.json`](../integrity/binding-matrix.json) — [requirement](TERMS.md#requirement) → [audit](TERMS.md#audit) → binder matrix
- [`adrs/0004-produce-fitness-handoff.md`](../adrs/0004-produce-fitness-handoff.md) — P-016
- [`adrs/0005-ssot-exit-evidence.md`](../adrs/0005-ssot-exit-evidence.md) — P-020
