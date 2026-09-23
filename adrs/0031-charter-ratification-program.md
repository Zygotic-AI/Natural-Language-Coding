# ADR 0031 — Charter ratification program

- Status: Accepted
- Date: 2026-09-23
- Deciders: Human manager
- Class: F (process)
- Corpus: nlc

## Context

Charter **R** rules are in force via the [binding matrix](../docs/TERMS.md#binding-matrix), but many still lack a named [ADR](../docs/TERMS.md#adr) decision trail (Evaluate-NLC A1). Binding alone is not ratification of the *decision* that the rule exists in that form. New **R** ids must not appear without a binder (R27).

## Decision

1. **Every charter rule eventually has a ratifying ADR** (one ADR may cover a coherent cluster of R ids).
2. **Backlog SSOT:** [`integrity/charter-ratify-backlog.json`](../integrity/charter-ratify-backlog.json) lists each published R id, covering ADR (or `open`), and notes. Closing A1 full means zero `open` rows.
3. **No new R id** without a binder and a backlog row pointing at a ratifying ADR (or an explicit parked gap row). Do not mint R ids that are unbindable (R27 / R29).
4. **Tranche execution is legal:** partial ratification is MET for the program leaf when the backlog exists, ADR 0031 is Accepted, and at least one tranche of previously bare rules is cited from CHARTER document control. Remaining `open` rows stay soft-green residual — not fake-closed.

## Consequences

- First tranche ADRs: 0032–0035 (ownership/mutation, contracts, goals, knowledge/enforcement).
- R26–R31 remain ratified by [ADR 0001](0001-zero-variance-integrity.md) (already named).
- Process/belief layers already named: [ADR 0024](0024-nlc-factory-spine.md), [ADR 0025](0025-belief-no-blame-climb.md).
- FINDINGS A1 retargets to “backlog remains” until `open` is empty.

## Rejected

- Claiming A1 complete while backlog still has `open` rows.
- One mega-ADR that only re-quotes the entire charter without cluster decisions.
- Minting new R ids in this program ADR.
