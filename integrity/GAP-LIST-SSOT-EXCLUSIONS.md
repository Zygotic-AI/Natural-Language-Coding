# Live gap list scan exclusions (O10)

`fitness-live-gap-list-ssot.py` refuses gap-queue markers outside **`FINDINGS.md`**.

## Allowed live gap list

| Path | Reason |
|------|--------|
| `FINDINGS.md` | Sole live Human / Needed / Parked / Housekeeping SSOT |

## Excluded from scan (not gap queues)

| Path / prefix | Reason |
|---------------|--------|
| `docs/history/` | Archived work logs and wave ledgers |
| `tools/nouns/live_gap_list_bypass_fixtures/` | Landmine plants (must go red when scanned) |
| `TODO`, `HOLES.md`, `docs/nlc/SESSION-FOLLOWTHROUGH.md` | Stubs → history |
| `integrity/GATE.md`, `ACTIONS.md`, `BOUNDARY.md`, `CONTRIBUTION.md` | Gate/contribution checklists (`- [ ] CGn`) |
| `.agents/skills/full-nlc-audit/`, `nlc-hub-audit/` (and `.cursor/skills` mirrors) | Audit orchestration checklists |
| `AGENTS.md`, `DESCRIBE.md`, `CHARTER.md` | Harness memory / TODO convention (open/ done markers) |
| `.agents/skills/planit/references/` | Planit reference checklists |
| `integrity/BOUNDED_CONTEXT.md`, `integrity/QUALITY_METRIC.md` | Integrity checklists |

Implementation: `tools/nouns/live_gap_list_ssot/live_gap_list_ssot.py`.
