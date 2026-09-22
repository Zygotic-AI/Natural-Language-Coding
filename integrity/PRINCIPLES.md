# Practice [integrity](../docs/TERMS.md#integrity) principles (BBP)

SSOT for how this repo keeps itself honest. Ratified by [`../adrs/0001-zero-variance-integrity.md`](../adrs/0001-zero-variance-integrity.md). [Charter](../docs/TERMS.md#charter) rules: [`../CHARTER.md`](../CHARTER.md) §5.8.

## P1 — Stand-alone branding

[BBP](../docs/TERMS.md#bbp) artifacts use [BBP](../docs/TERMS.md#bbp) names only. Useful shapes from elsewhere are copied and re/unbranded here. Foreign brand packages are not imported into this [integrity](../docs/TERMS.md#integrity) system.

**[Audit](../docs/TERMS.md#audit) `A-P1`:** [Met](../docs/TERMS.md#met) iff no [BBP](../docs/TERMS.md#bbp) integrity/charter/agent/tool path depends on a foreign-branded package name or path as a required binder. Not [met](../docs/TERMS.md#met) otherwise.

## P2 — [Zero variance](../docs/TERMS.md#zero-variance)

P2 binds (a) changes to this practice [hub](../docs/TERMS.md#hub)’s in-force surfaces and [integrity](../docs/TERMS.md#integrity) machinery, and (b) the prescribed agent-loop gates for change classes A, B, D, E, F; it does not require a prescribed [action](../docs/TERMS.md#action) for every edit inside an already-ratified noun-verb or [goal](../docs/TERMS.md#goal) implementation, while unprescribed [boundary](../docs/TERMS.md#boundary) crossings remain incomplete work (ADR [`0002-p2-scope.md`](../adrs/0002-p2-scope.md)).

**[Audit](../docs/TERMS.md#audit) `A-P2`:** [Met](../docs/TERMS.md#met) iff required [hub](../docs/TERMS.md#hub) and class A/B/D/E/F gates ran or an [ADR](../docs/TERMS.md#adr) named an exemption, and [noun](../docs/TERMS.md#noun) fields are written only through public verbs; not [met](../docs/TERMS.md#met) if a required [gate](../docs/TERMS.md#gate) was skipped or a [noun](../docs/TERMS.md#noun) [boundary](../docs/TERMS.md#boundary) was crossed without a verb — not merely because code was written without a ticket.

## P3 — Hard gates (complete / incomplete)

Every step and every [action](../docs/TERMS.md#action) has a hard [gate](../docs/TERMS.md#gate). The [gate](../docs/TERMS.md#gate) outcome is only **complete** or **incomplete**.

**[Audit](../docs/TERMS.md#audit) `A-P3`:** [Met](../docs/TERMS.md#met) iff each [gate](../docs/TERMS.md#gate)’s definition states binary complete/incomplete criteria and produces evidence that points at a file or symbol (or an explicit N/A reason). Not [met](../docs/TERMS.md#met) if any [gate](../docs/TERMS.md#gate) allows warn-only, partial, or vibes.

## P4 — Hard [boundary](../docs/TERMS.md#boundary) I/O

Every [boundary](../docs/TERMS.md#boundary) declares input [contract](../docs/TERMS.md#contract), output [contract](../docs/TERMS.md#contract), and failure mode: returned error, thrown exception, or process exit (when the boundary is code).

**[Audit](../docs/TERMS.md#audit) `A-P4`:** [Met](../docs/TERMS.md#met) iff each public [boundary](../docs/TERMS.md#boundary) in scope has those three declarations machine-checkable or confirmer-checkable. Not [met](../docs/TERMS.md#met) if any public [boundary](../docs/TERMS.md#boundary) omits failure mode or forks shared field meaning (charter R11).

## P5 — Binary [requirement](../docs/TERMS.md#requirement) audits

Every [requirement](../docs/TERMS.md#requirement) in this repo has an [audit](../docs/TERMS.md#audit) that yields **[met](../docs/TERMS.md#met)** or **not [met](../docs/TERMS.md#met)**.

**[Audit](../docs/TERMS.md#audit) `A-P5`:** [Met](../docs/TERMS.md#met) iff every row in the [binding matrix](../docs/TERMS.md#binding-matrix) has a non-empty `audit_id` and an [audit](../docs/TERMS.md#audit) definition with binary criteria. Not [met](../docs/TERMS.md#met) if any [requirement](../docs/TERMS.md#requirement) lacks an [audit](../docs/TERMS.md#audit) definition.

## P6 — [Binding matrix](../docs/TERMS.md#binding-matrix); unbound is failure

The [binding matrix](../docs/TERMS.md#binding-matrix) lists every [requirement](../docs/TERMS.md#requirement), its [audit](../docs/TERMS.md#audit), and its binder. **Unbound entries fail the matrix [audit](../docs/TERMS.md#audit).** The [audit](../docs/TERMS.md#audit) output **lists** each unbound entry by [requirement](../docs/TERMS.md#requirement) id.

**[Audit](../docs/TERMS.md#audit) `A-BINDING-UNBOUND`:** [Met](../docs/TERMS.md#met) iff zero matrix rows have `binder` empty or `status=unbound`. Not [met](../docs/TERMS.md#met) otherwise; report must enumerate all unbound [requirement](../docs/TERMS.md#requirement) ids.

## P7 — Promote-only-when-bindable

A [requirement](../docs/TERMS.md#requirement) is promoted to an in-force surface only when a binder can fail the change. **In-force-but-unbindable entries fail the promote [audit](../docs/TERMS.md#audit).** The [audit](../docs/TERMS.md#audit) output **lists** each such entry.

**[Audit](../docs/TERMS.md#audit) `A-BINDING-PROMOTE`:** [Met](../docs/TERMS.md#met) iff every row with `surface=in-force` has `status=bound` and a binder that can fail (CI check, confirmer gate, or fitness tool). Not [met](../docs/TERMS.md#met) otherwise; report must enumerate all in-force unbindable [requirement](../docs/TERMS.md#requirement) ids.

## Vocabulary

| Term | Meaning |
|------|---------|
| [Requirement](../docs/TERMS.md#requirement) | A confirmable [rule](../docs/TERMS.md#rule) or principle with an id |
| [Audit](../docs/TERMS.md#audit) | Procedure that yields [met](../docs/TERMS.md#met) / not [met](../docs/TERMS.md#met) with evidence; produces findings for [ship](../docs/TERMS.md#ship) decision |
| Binder | Mechanism that can fail a change when the [audit](../docs/TERMS.md#audit) would be not [met](../docs/TERMS.md#met) |
| Bound | [Requirement](../docs/TERMS.md#requirement) has [audit](../docs/TERMS.md#audit) + binder |
| Unbound | [Requirement](../docs/TERMS.md#requirement) missing [audit](../docs/TERMS.md#audit) and/or binder |
| In-force | Published on the [charter](../docs/TERMS.md#charter) or other mandatory surface |
| [Gate](../docs/TERMS.md#gate) | Binary PASS/FAIL enforcement checkpoint; see [`GATE.md`](GATE.md) for formal definition and all-required PASS fitness bar |

**[Gate](../docs/TERMS.md#gate) vs [Audit](../docs/TERMS.md#audit):** Gates block automatically (CI, fitness); audits produce findings for a ship-role or human to decide. Both are binary per item, but differ in mechanism and authority. See [`GATE.md`](GATE.md) §Definition.
