# Practice integrity principles (BBP)

SSOT for how this repo keeps itself honest. Ratified by [`../adrs/0001-zero-variance-integrity.md`](../adrs/0001-zero-variance-integrity.md). Charter rules: [`../CHARTER.md`](../CHARTER.md) §5.8.

## P1 — Stand-alone branding

BBP artifacts use BBP names only. Useful shapes from elsewhere are copied and re/unbranded here. Foreign brand packages are not imported into this integrity system.

**Audit `A-P1`:** Met iff no BBP integrity/charter/agent/tool path depends on a foreign-branded package name or path as a required binder. Not met otherwise.

## P2 — Zero variance

P2 binds (a) changes to this practice hub’s in-force surfaces and integrity machinery, and (b) the prescribed agent-loop gates for change classes A, B, D, E, F; it does not require a prescribed action for every edit inside an already-ratified noun-verb or goal implementation, while unprescribed boundary crossings remain incomplete work (ADR [`0002-p2-scope.md`](../adrs/0002-p2-scope.md)).

**Audit `A-P2`:** Met iff required hub and class A/B/D/E/F gates ran or an ADR named an exemption, and noun fields are written only through public verbs; not met if a required gate was skipped or a noun boundary was crossed without a verb — not merely because code was written without a ticket.

## P3 — Hard gates (complete / incomplete)

Every step and every action has a hard gate. The gate outcome is only **complete** or **incomplete**.

**Audit `A-P3`:** Met iff each gate’s definition states binary complete/incomplete criteria and produces evidence that points at a file or symbol (or an explicit N/A reason). Not met if any gate allows warn-only, partial, or vibes.

## P4 — Hard boundary I/O

Every boundary declares input contract, output contract, and failure mode: returned error, thrown exception, or process exit (when the boundary is code).

**Audit `A-P4`:** Met iff each public boundary in scope has those three declarations machine-checkable or confirmer-checkable. Not met if any public boundary omits failure mode or forks shared field meaning (charter R11).

## P5 — Binary requirement audits

Every requirement in this repo has an audit that yields **met** or **not met**.

**Audit `A-P5`:** Met iff every row in the binding matrix has a non-empty `audit_id` and an audit definition with binary criteria. Not met if any requirement lacks an audit definition.

## P6 — Binding matrix; unbound is failure

The binding matrix lists every requirement, its audit, and its binder. **Unbound entries fail the matrix audit.** The audit output **lists** each unbound entry by requirement id.

**Audit `A-BINDING-UNBOUND`:** Met iff zero matrix rows have `binder` empty or `status=unbound`. Not met otherwise; report must enumerate all unbound requirement ids.

## P7 — Promote-only-when-bindable

A requirement is promoted to an in-force surface only when a binder can fail the change. **In-force-but-unbindable entries fail the promote audit.** The audit output **lists** each such entry.

**Audit `A-BINDING-PROMOTE`:** Met iff every row with `surface=in-force` has `status=bound` and a binder that can fail (CI check, confirmer gate, or fitness tool). Not met otherwise; report must enumerate all in-force unbindable requirement ids.

## Vocabulary

| Term | Meaning |
|------|---------|
| Requirement | A confirmable rule or principle with an id |
| Audit | Procedure that yields met / not met with evidence |
| Binder | Mechanism that can fail a change when the audit would be not met |
| Bound | Requirement has audit + binder |
| Unbound | Requirement missing audit and/or binder |
| In-force | Published on the charter or other mandatory surface |
| Gate | Binary complete/incomplete check on a prescribed step |
