# [ADR](../docs/TERMS.md#adr) 0005 — Task/board [SSOT exit evidence](../docs/TERMS.md#ssot-exit-evidence) required in produce packages

- Status: Accepted
- Date: 2026-09-05
- Deciders: Human manager; [Quality](../docs/TERMS.md#quality) Architect role; Adversarial auditor role
- Class: F (charter/agent)
- Tags: systems, [handoff](../docs/TERMS.md#handoff), [P-020](../docs/TERMS.md#ssot-exit-evidence)
- File: `adrs/0005-ssot-exit-evidence.md` (replaces Notion-named ADR 0005 filename)

## Context

P-016 established that produce→fitness [handoff](../docs/TERMS.md#handoff) requires a complete [produce package](../docs/TERMS.md#produce-package). Packages can still be structurally "complete" while lacking evidence that the work is tracked in the task/board single source of truth (SSOT).

Without [SSOT exit evidence](../docs/TERMS.md#ssot-exit-evidence):

- Work can appear complete without traceability to task/board state
- Stage exit validation cannot be audited
- Fitness assessment proceeds on artifacts that have no coordination link
- Adversarial [audit](../docs/TERMS.md#audit) cannot [verify](../docs/TERMS.md#verify) board-sync against the SSOT

An earlier draft of this decision named a specific board product and product-shaped field names inside the [BBA](../docs/TERMS.md#bba) [charter](../docs/TERMS.md#charter) and agent contracts. That violates the architecture principle lock: **[BBA](../docs/TERMS.md#bba) is tool-agnostic**. Product bindings belong in a separate implementation/bindings repo, not in charter/agent vocabulary.

This aligns with: S7 (produce→fitness default-closed); P-016; KD-010 [quality](../docs/TERMS.md#quality) north star; stand-alone [BBP](../docs/TERMS.md#bbp) branding (P1).

## Decision

1. **[SSOT exit evidence](../docs/TERMS.md#ssot-exit-evidence) is a required [produce package](../docs/TERMS.md#produce-package) field.** Produce packages must include:
   - `ssot_leaf_ids`: array of opaque leaf ids from the task/board SSOT (at least one required)
   - `ssot_exit_status`: non-empty exit state string at produce completion

2. **Fitness preflight refuses without [SSOT exit evidence](../docs/TERMS.md#ssot-exit-evidence).** Missing `ssot_leaf_ids` or `ssot_exit_status` triggers `handoff_refused` with `SSOT_EXIT_EVIDENCE` in the missing enum — same [refuse](../docs/TERMS.md#refuse) class as P-016 missing package elements.

3. **Fitness scoring refuses [MET](../docs/TERMS.md#met) without [SSOT exit evidence](../docs/TERMS.md#ssot-exit-evidence).** Even if preflight passes structurally, score-fitness returns `FAIL` (or refuses MET via the contracted error envelope) if [SSOT exit evidence](../docs/TERMS.md#ssot-exit-evidence) is missing or invalid.

4. **Adversarial [audit](../docs/TERMS.md#audit) refuses PASS without [SSOT exit evidence](../docs/TERMS.md#ssot-exit-evidence).** audit-proposal and audit-diff [verify](../docs/TERMS.md#verify) `ssot_leaf_ids` are present (≥1 opaque leaf id) and `ssot_exit_status` is declared non-empty; missing evidence is a blocker citing [P-020](../docs/TERMS.md#ssot-exit-evidence) / error `SSOT_EVIDENCE_MISSING`.

5. **Standing instructions inherit via AGENTS.md.** Harness standing instructions require [SSOT exit evidence](../docs/TERMS.md#ssot-exit-evidence) on all produce work, using the abstract field names — not a product brand.

6. **[Rule](../docs/TERMS.md#rule) and [audit](../docs/TERMS.md#audit) identity preserved.** [Charter](../docs/TERMS.md#charter) rules remain **S8** and **CS8**; audits remain **A-S8** and **A-CS8**; this decision remains **[P-020](../docs/TERMS.md#ssot-exit-evidence)** / [ADR](../docs/TERMS.md#adr) **0005**. Content and [ADR](../docs/TERMS.md#adr) filename are rewritten to the abstract surface.

## Consequences

- Producers must include `ssot_leaf_ids` and `ssot_exit_status` in every [produce package](../docs/TERMS.md#produce-package)
- Fitness receipts echo [SSOT exit evidence](../docs/TERMS.md#ssot-exit-evidence) fields
- Adversarial [audit](../docs/TERMS.md#audit) includes SSOT exit-evidence / board-sync check against the abstract [contract](../docs/TERMS.md#contract)
- Metrics: packages with/without [SSOT exit evidence](../docs/TERMS.md#ssot-exit-evidence); [refuse](../docs/TERMS.md#refuse) rate
- Agent packages (standards-steward, quality-architect, adversarial-auditor) use abstract field names and tokens
- Concrete how-to for a given board product lives outside [BBA](../docs/TERMS.md#bba) (implementation/bindings repo); [BBA](../docs/TERMS.md#bba) only defines the [contract](../docs/TERMS.md#contract)
- S8/CS8 remain reference/unbound until a fail-capable binder exists (P7)

## Rejected

- Optional [SSOT exit evidence](../docs/TERMS.md#ssot-exit-evidence) fields: does not enforce traceability; defeats the purpose
- Post-fitness link of leaf ids: too late; evidence must be present at produce→fitness [handoff](../docs/TERMS.md#handoff)
- Warning-only: violates [zero variance](../docs/TERMS.md#zero-variance); hard [gate](../docs/TERMS.md#gate) required
- **Notion-named fields in [BBA](../docs/TERMS.md#bba) [charter](../docs/TERMS.md#charter)** (`notion_page_ids`, `notion_exit_status`, `NOTION_EXIT_EVIDENCE`, `NOTION_EVIDENCE_MISSING`, and "Notion" as required prose): product [binding](../docs/TERMS.md#binding) inside architecture definition; breaks tool-agnostic lock
- Dual required vocabulary (product-named **and** abstract fields): forks the [contract](../docs/TERMS.md#contract); agents thrash
- Encoding MCP / IDE / agent-product bindings in [charter](../docs/TERMS.md#charter) or verb field names: same class of architecture [defect](../docs/TERMS.md#defect)

## Related

- [ADR 0004](0004-produce-fitness-handoff.md) — Produce→fitness [handoff](../docs/TERMS.md#handoff) [default-closed](../docs/TERMS.md#default-closed) (P-016)
- [ADR 0001](0001-zero-variance-integrity.md) — [Zero-variance](../docs/TERMS.md#zero-variance) [integrity](../docs/TERMS.md#integrity) (P1–P7)
- [Charter](../docs/TERMS.md#charter) §6 (Order of agent execution)
- [Charter](../docs/TERMS.md#charter) S7 (Produce→fitness handoff default-closed)
- [Charter](../docs/TERMS.md#charter) S8 / CS8 (this decision)
