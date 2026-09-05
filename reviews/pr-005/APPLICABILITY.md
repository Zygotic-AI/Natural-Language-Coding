# PR-005 Applicability Statement

## Scope

This change applies to:

1. **Charter document** (`CHARTER.md`) — §6 Step 2, S8, CS8
2. **Binding matrix** (`integrity/binding-matrix.json`) — S8, CS8 entries
3. **Agent noun packages** (`agents/`) — standards-steward, quality-architect, adversarial-auditor
4. **ADR** (`adrs/0005-notion-exit-evidence.md`) — decision record
5. **AGENTS.md** — standing instructions for Cursor agents
6. **Integrity audits** (`integrity/audits/`) — A-S8.md, A-CS8.md

## Exclusions

This change does **not** apply to:

- PR #3 or PR #4 scope (except inheriting current main)
- Product application code
- Session gate implementation (deferred)
- Existing CI tooling (no binder changes)
- External task tracker support (Notion only)

## Applicability rationale

**Charter S7 (Produce→fitness default-closed)** requires complete produce packages. This change extends the completeness requirement to include Notion exit evidence, ensuring traceability from produce work to coordination system.

**P-016 alignment:** Follows the same refuse pattern — missing Notion evidence triggers `handoff_refused` with `NOTION_EXIT_EVIDENCE` in defect log, not soft-fail.

**KD-010 quality north star:** Default-closed boundaries; no discovery loops.

## Backward compatibility

- Existing produce packages without Notion evidence will receive `handoff_refused` (not retroactive FAIL)
- No breaking change to existing bound rules
- New rules S8/CS8 are reference surface (unbound) — no false binders

## Forward compatibility

- Future binders for S8/CS8 will enforce Notion evidence presence
- Future external task tracker support can extend via separate ADR
- This package dogfoods the requirement (includes Notion evidence)
