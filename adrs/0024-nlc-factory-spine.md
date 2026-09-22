# [ADR](../docs/TERMS.md#adr) 0024 — [NLC](../docs/TERMS.md#nlc) factory spine

- Status: Accepted
- Date: 2026-09-22
- Deciders: Human manager
- Class: F (process)
- Corpus: nlc

## Context

[BBA](../docs/TERMS.md#bba) is the emit *shape* (what the factory may build). [NLC](../docs/TERMS.md#nlc) is how the factory runs. Mixing them hid the product: the process.

Unbound prose is not a [rule](../docs/TERMS.md#rule). [Emit](../docs/TERMS.md#compiler) must not invent applicability. Applicability is decided on [actions](../docs/TERMS.md#action), then [audited](../docs/TERMS.md#audit), then gated.

## Decision

1. **One [ADR](../docs/TERMS.md#adr) list** in a repo. Two [rule](../docs/TERMS.md#rule) corpora: `nlc` (process) and `bba` (emit shape). [BBP](../docs/TERMS.md#bbp) is a BBA profile, not a third corpus.
2. **Bind or remove.** A published [rule](../docs/TERMS.md#rule) or [ADR](../docs/TERMS.md#adr) has testable [gates](../docs/TERMS.md#gate) or is deleted. Parked is legal only as a bound gap row.
3. A **[rule](../docs/TERMS.md#rule)** is an adopted if/then: **condition** (`if`) + **obligation** (`then`) + **[gate](../docs/TERMS.md#gate)**.
4. **Pipeline**
   1. Plan
   2. Atomic [actions](../docs/TERMS.md#action) — each [gated](../docs/TERMS.md#gate) and validated against the plan
   3. Bind [ADRs](../docs/TERMS.md#adr) to those actions
   4. Reverse [audit](../docs/TERMS.md#audit) — every applicable ADR is bound to an action
   5. Emit — artifact + JSON manifest (schema predefined on the emit; unused fields = `na`; decision trace + thought anchors)
   6. [Audit](../docs/TERMS.md#audit) the emit — every emit has an audit
   7. [Gates](../docs/TERMS.md#gate) of the ADRs bound to that action — [default-closed](../docs/TERMS.md#default-closed), immediately after emit
5. Emit does **not** select [rules](../docs/TERMS.md#rule) from corpora. Selection is plan → actions → ADR bindings → reverse audit.
6. Existing Charter **R** / **C** / **P** ids are tagged in [`integrity/rule-corpus.json`](../integrity/rule-corpus.json). No new **R** id in this ADR (R27).

## Consequences

- v1 binder: [`tools/fitness-adr-0024-binder.py`](../tools/fitness-adr-0024-binder.py) — spine files exist; corpus map covers published R/C/P; rules file lists NLC-0024-* ids.
- Full action↔plan and emit-audit runners remain expansion; they do not weaken this decision.
- [`docs/ADR-ENFORCEMENT.md`](../docs/ADR-ENFORCEMENT.md) row 0024.

## Rejected

- Emit scans both corpora for applicable rules.
- BBA as the load-bearing architecture of NLC.
- Two ADR directories.
- Unbound “should” left in Charter/README as a live [rule](../docs/TERMS.md#rule).

## Related

- [ADR 0004](0004-produce-fitness-handoff.md) — default-closed handoff
- [ADR 0005](0005-ssot-exit-evidence.md) — produce package evidence
- [ADR 0010](0010-gate-after-every-generate.md) — gate after generate
- [ADR 0023](0023-rule-instance-trace-and-instant-audit-scope.md) — rule receipts
