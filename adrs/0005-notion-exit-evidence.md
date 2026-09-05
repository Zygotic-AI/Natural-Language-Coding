# ADR 0005 — Notion exit evidence required in produce packages

- Status: needs_review
- Date: 2026-09-05
- Deciders: Reed (Quality Architect) draft; adversarial + ship separately
- Class: F (charter/agent)
- Tags: grokbot, systems, handoff, P-020

## Context

P-016 established that produce→fitness handoff requires a complete produce package. However, packages can still be "complete" structurally while lacking evidence that the work is tracked in the coordination system.

Without Notion exit evidence:
- Work can appear complete without traceability to task board state
- Stage exit validation cannot be audited
- Fitness assessment proceeds on artifacts that have no coordination link
- Adversarial audit cannot verify board-sync

This aligns with: S7 (produce→fitness default-closed); P-016; KD-010 quality north star.

## Decision

1. **Notion exit evidence is a required produce package field.** Produce packages must include:
   - `notion_page_ids`: array of Notion page UUIDs (at least one required)
   - `notion_exit_status`: exit status at produce completion (e.g., "in progress", "done")

2. **Fitness preflight refuses without Notion evidence.** Missing `notion_page_ids` or `notion_exit_status` triggers `handoff_refused` with `NOTION_EXIT_EVIDENCE` in the missing enum — same refuse class as P-016 missing package elements.

3. **Fitness scoring refuses MET without Notion evidence.** Even if preflight passes structurally, score-fitness returns `FAIL` if Notion evidence is missing or invalid.

4. **Adversarial audit refuses PASS without Notion evidence.** audit-proposal and audit-diff verify Notion page id(s) are present and status is declared; missing evidence is a blocker finding citing P-020.

5. **Cursor agents inherit via AGENTS.md.** Standing instructions updated to require Notion exit evidence on all produce work.

## Consequences

- Producers must include Notion page id(s) and exit status in every produce package
- Fitness receipts include Notion evidence fields
- Adversarial audit includes Notion traceability check
- Metrics: packages with/without Notion evidence; refuse rate
- New rule S8 (Notion exit evidence required) and checklist item CS8
- Agent packages (standards-steward, quality-architect, adversarial-auditor) gain Notion evidence requirements
- AGENTS.md gains standing instruction for Cursor inheritance

## Rejected

- Optional Notion fields: does not enforce traceability; defeats the purpose
- Post-fitness Notion link: too late; evidence must be present at produce→fitness handoff
- External task tracker support: scope limited to Notion for now; future ADR can extend
- Warning-only: violates zero variance; hard gate required

## Related

- [ADR 0004](0004-produce-fitness-handoff.md) — Produce→fitness handoff default-closed (P-016)
- [ADR 0001](0001-zero-variance-integrity.md) — Zero-variance integrity (P1–P7)
- Charter §6 (Order of agent execution)
- Charter S7 (Produce→fitness handoff default-closed)
- Notion task page: `3d29d973-ccd7-81fa-9cb1-c7b01cf5a2da`
