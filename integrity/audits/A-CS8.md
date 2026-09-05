# Audit A-CS8: Notion exit evidence checklist item

## Checklist item

**CS8.** Notion exit evidence present in produce package (page id(s) + exit status); missing evidence refused (P-020).

## Audit criteria

**Met** iff:

1. The produce package directory contains Notion evidence declaration (in ADVERSARIAL.md or dedicated NOTION.md).
2. `notion_page_ids` is present with at least one valid Notion page UUID.
3. `notion_exit_status` is present with a non-empty status value.
4. The Notion page id(s) are verifiable (UUID format, optionally validated against Notion API).

**Not met** otherwise; report must enumerate:

- Missing `notion_page_ids` field
- Missing `notion_exit_status` field
- Invalid UUID format in `notion_page_ids`
- Empty or missing status value

## Evidence

For each produce package in scope:

- `reviews/pr-*/ADVERSARIAL.md` — `notion_page_ids` and `notion_exit_status` fields
- Or `reviews/pr-*/NOTION.md` — dedicated Notion evidence file

## Scope

Systems confirmation checklist (§16.7); produce packages.

## Related

- S8 — Produce packages require Notion exit evidence
- CS7 — Produce package present before fitness
- P-020 — ADR 0005: Notion exit evidence required
