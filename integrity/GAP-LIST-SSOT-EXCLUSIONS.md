# Live gap list scan exclusions (O10)

`fitness-live-gap-list-ssot.py` refuses gap-queue markers outside **`FINDINGS.md`**.

## Allowed live gap list

| Path | Reason |
|------|--------|
| `FINDINGS.md` | Sole live Human / Needed / Parked / Housekeeping SSOT |

## Path prefix exclusions

| Path | Reason |
|------|--------|
| `docs/history/` | Archived work logs and wave ledgers |
| `docs/rca/` | RCA packets (not live gap queues) |
| `theory/history/` | Frozen theory archive |
| `tools/nouns/live_gap_list_bypass_fixtures/` | Gap-list landmine plants |
| `node_modules/` | Third-party |
| `.git/` | VCS metadata |

## Exact path exclusions

| Path | Reason |
|------|--------|
| `integrity/GAP-LIST-SSOT-EXCLUSIONS.md` | Meta: documents exclusions |
| `examples/open-findings/FINDINGS.md` | C23 specimen: adversarial open FINDINGS (not live SSOT) |

## Skill-tree prefix exclusions

| Path | Reason |
|------|--------|
| `.agents/skills/full-nlc-audit/` | Full NLC audit skill checklists |
| `.agents/skills/nlc-hub-audit/` | Hub audit skill checklists |
| `.cursor/skills/full-nlc-audit/` | Cursor mirror of full-nlc-audit checklists |
| `.cursor/skills/nlc-hub-audit/` | Cursor mirror of nlc-hub-audit checklists |
| `.agents/skills/planit/references/` | Planit reference checklists |

## Line exemptions (file scanned; matching lines ignored)

| Path | Reason |
|------|--------|
| `line:CHARTER.md` | Charter change confirmation checklist (C1–C26) |
| `line:CHARTER.md` | Charter agent-noun confirmation checklist (CS1–CS10) |
| `line:AGENTS.md` | Documents TODO `☐` convention (not an open-work queue) |
| `line:DESCRIBE.md` | Documents TODO `☐` convention (not an open-work queue) |
| `line:integrity/CONTRIBUTION.md` | Contribution gate checklist (CC1–CC8) |
| `line:integrity/BOUNDARY.md` | Boundary tip checklist (CB1–CB7) |
| `line:integrity/GATE.md` | Gate tip checklist (CG1–CG4) |
| `line:integrity/ACTIONS.md` | Action tip checklist |
| `line:integrity/PRINCIPLES.md` | Principle checklist lines |
| `line:integrity/BOUNDED_CONTEXT.md` | Bounded-context checklist |
| `line:integrity/QUALITY_METRIC.md` | Quality metric checklist |
| `line:.agents/instructions/todo-product-uc-completion.md` | Product UC completion instruction checklist |
| `line:.agents/instructions/todo-product-uc-completion.md` | Documents TODO `☐` product-row convention (not live gap queue) |
| `line:TODO` | Root TODO stub convention (points at history) |
| `line:HOLES.md` | Stub pointer only |
| `line:docs/nlc/SESSION-FOLLOWTHROUGH.md` | Stub pointer to history SESSION-FOLLOWTHROUGH |

Implementation: `tools/nouns/live_gap_list_ssot/gap_list_exclusions.py`.
