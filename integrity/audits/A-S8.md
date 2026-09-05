# Audit A-S8: Notion exit evidence required

## Rule

**S8.** Produce packages require Notion exit evidence. Packages must include Notion page id(s) and exit status. Missing Notion evidence triggers `handoff_refused`; fitness scoring refuses MET; adversarial audit refuses PASS (P-020).

## Audit criteria

**Met** iff:

1. Every produce package in scope contains `notion_page_ids` field with at least one valid Notion page UUID.
2. Every produce package in scope contains `notion_exit_status` field with a non-empty status value.
3. Fitness preflight returns `handoff_refused` with `NOTION_EXIT_EVIDENCE` in missing enum when Notion evidence is absent.
4. Fitness `score-fitness` returns `FAIL` (not `MET`) when Notion evidence is missing.
5. Adversarial `audit-proposal` and `audit-diff` return error with `NOTION_EVIDENCE_MISSING` when evidence is absent.

**Not met** otherwise; report must enumerate:

- Package paths missing `notion_page_ids`
- Package paths missing `notion_exit_status`
- Fitness receipts that returned `MET` without Notion evidence
- Adversarial audit results that returned `pass` without Notion evidence

## Evidence

- `reviews/pr-*/ADVERSARIAL.md` — `notion_page_ids` and `notion_exit_status` fields
- `agents/quality-architect/verbs.md` — `NOTION_EXIT_EVIDENCE` in missing enum
- `agents/adversarial-auditor/verbs.md` — `NOTION_EVIDENCE_MISSING` in error codes

## Scope

Systems model (§16); agent noun packages; produce packages.

## Related

- S7 — Produce→fitness handoff default-closed
- CS8 — Checklist item for Notion exit evidence
- P-020 — ADR 0005: Notion exit evidence required
