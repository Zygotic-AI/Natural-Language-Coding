# Agent package edits — SSOT exit evidence (abstract P-020)

Concrete find/replace map. Apply on the PR #5 tree (or superseding branch). Do not leave Notion-named field names as required vocabulary.

## Canonical tokens

| Role | Token |
|------|--------|
| Fields | `ssot_leaf_ids`, `ssot_exit_status` |
| Missing enum | `SSOT_EXIT_EVIDENCE` |
| Error code | `SSOT_EVIDENCE_MISSING` |
| Prose | “task/board SSOT exit evidence” / “SSOT exit evidence” |

---

## AGENTS.md

**Find** the P-020 standing-instruction paragraph (Notion exit evidence required…).

**Replace with:**

> **SSOT exit evidence required (P-020, S8).** Every produce package must include task/board SSOT exit evidence: `ssot_leaf_ids` (one or more opaque leaf ids) and `ssot_exit_status` (non-empty exit state string). Fitness refuses MET without this evidence; adversarial audit refuses PASS. Missing SSOT exit evidence triggers `handoff_refused` with `SSOT_EXIT_EVIDENCE` in the defect log. Do not normalize leaving SSOT exit evidence for later.

Also remove any “Cursor inherit” / product-harness brand binding as a requirement; keep the existing generic “any coding harness” framing at the top of AGENTS.md.

---

## agents/standards-steward/AGENT.md

| Location | Find | Replace |
|----------|------|---------|
| Completion artifact table / prose | `including Notion exit evidence` | `including SSOT exit evidence` |
| Completion sentence | `Notion exit evidence` | `task/board SSOT exit evidence` (`ssot_leaf_ids` + `ssot_exit_status`) |
| Handoff-out row | `Notion exit evidence present` / `Notion page id(s) + exit status in package (S8, P-020)` | `SSOT exit evidence present` / `ssot_leaf_ids` + `ssot_exit_status` in package (S8, P-020) |
| Incomplete handoffs sentence | `missing Notion evidence` | `missing SSOT exit evidence` |

---

## agents/standards-steward/verbs.md (`complete-produce`)

| Kind | Find | Replace |
|------|------|---------|
| Missing enum item | `NOTION_EXIT_EVIDENCE` | `SSOT_EXIT_EVIDENCE` |
| Output field | `notion_page_ids` | `ssot_leaf_ids` |
| Field description | Notion page UUIDs… | Opaque leaf ids from the task/board SSOT (echo for traceability) |
| Output field | `notion_exit_status` | `ssot_exit_status` |
| Field description | Exit status declared in package… | Exit state string declared in package (echo for traceability) |
| Error code | `NOTION_EVIDENCE_MISSING` | `SSOT_EVIDENCE_MISSING` |
| Note under verb | `Notion exit evidence (S8, P-020)` | `SSOT exit evidence (S8, P-020)` |

Keep `format: uuid` on leaf id items only if desired as a shape hint for opaque ids; do **not** describe them as Notion page UUIDs. Prefer description: “opaque leaf id string (≥1)”.

---

## agents/quality-architect/verbs.md

### `preflight-fitness-handoff`

| Kind | Find | Replace |
|------|------|---------|
| Missing enum | `NOTION_EXIT_EVIDENCE` | `SSOT_EXIT_EVIDENCE` |
| Output fields | `notion_page_ids` / `notion_exit_status` | `ssot_leaf_ids` / `ssot_exit_status` |
| Descriptions | Notion page UUIDs… / Exit status… | Opaque leaf ids from package (only if ready) / Exit state string from package (only if ready) |
| Note | `missing Notion exit evidence per S8/P-020` | `missing SSOT exit evidence per S8/P-020` |

### `score-fitness`

| Kind | Find | Replace |
|------|------|---------|
| Input fields | `notion_page_ids` / `notion_exit_status` | `ssot_leaf_ids` / `ssot_exit_status` |
| Descriptions | Notion… required for MET | SSOT leaf ids / exit status from preflight (required for MET) |
| Output echo fields | `notion_page_ids` / `notion_exit_status` | `ssot_leaf_ids` / `ssot_exit_status` |
| blocking_failures note | `CS8 if Notion evidence missing` | `CS8 if SSOT exit evidence missing` |
| Error code | `NOTION_EVIDENCE_MISSING` | `SSOT_EVIDENCE_MISSING` |
| Failure note | Notion page id(s) or exit status… Notion evidence (S8, P-020) | `ssot_leaf_ids` or `ssot_exit_status` absent; scoring refuses MET without SSOT exit evidence (S8, P-020) |

`agents/quality-architect/AGENT.md` has no Notion-named fields today — no required edit unless a Notion string appears after other merges.

---

## agents/adversarial-auditor/AGENT.md

| Location | Find | Replace |
|----------|------|---------|
| Handoff-in row | `Notion exit evidence present` / `Notion page id(s) + exit status in fitness receipt (S8, P-020)` | `SSOT exit evidence present` / `ssot_leaf_ids` + `ssot_exit_status` in fitness receipt (S8, P-020) |
| Handoff-in note | `refuses PASS without Notion exit evidence (P-020)` | `refuses PASS without SSOT exit evidence (P-020)` |

---

## agents/adversarial-auditor/verbs.md

### `audit-proposal` and `audit-diff`

| Kind | Find | Replace |
|------|------|---------|
| Input fields | `notion_page_ids` / `notion_exit_status` | `ssot_leaf_ids` / `ssot_exit_status` |
| Descriptions | Notion page UUIDs from fitness receipt… | Opaque leaf ids from fitness receipt (required for PASS per P-020) / Exit state string from fitness receipt (required for PASS per P-020) |
| Error code | `NOTION_EVIDENCE_MISSING` | `SSOT_EVIDENCE_MISSING` |
| Notes | Notion exit evidence / Notion page id(s) | SSOT exit evidence / `ssot_leaf_ids` |

---

## integrity/audits/A-S8.md

Rewrite title + body to abstract surface. Skeleton:

```markdown
# Audit A-S8: Task/board SSOT exit evidence required

## Rule

**S8.** Produce packages require task/board SSOT exit evidence. Packages must include `ssot_leaf_ids` (one or more opaque leaf ids) and `ssot_exit_status` (non-empty exit state string). Missing SSOT exit evidence triggers `handoff_refused`; fitness scoring refuses MET; adversarial audit refuses PASS (P-020).

## Audit criteria

**Met** iff:

1. Every produce package in scope contains `ssot_leaf_ids` with at least one opaque leaf id.
2. Every produce package in scope contains `ssot_exit_status` with a non-empty status value.
3. Fitness preflight returns `handoff_refused` with `SSOT_EXIT_EVIDENCE` in missing enum when SSOT exit evidence is absent.
4. Fitness `score-fitness` returns `FAIL` (not `MET`) when SSOT exit evidence is missing.
5. Adversarial `audit-proposal` and `audit-diff` return error with `SSOT_EVIDENCE_MISSING` when evidence is absent.

**Not met** otherwise; report must enumerate missing `ssot_leaf_ids` / `ssot_exit_status`, MET without evidence, PASS without evidence.

## Evidence

- `reviews/pr-*/ADVERSARIAL.md` — `ssot_leaf_ids` and `ssot_exit_status`
- `agents/quality-architect/verbs.md` — `SSOT_EXIT_EVIDENCE` in missing enum
- `agents/adversarial-auditor/verbs.md` — `SSOT_EVIDENCE_MISSING` in error codes

## Related

- S7, CS8, P-020 — ADR 0005: SSOT exit evidence required
```

---

## integrity/audits/A-CS8.md

```markdown
# Audit A-CS8: Task/board SSOT exit evidence checklist item

## Checklist item

**CS8.** Task/board SSOT exit evidence present in produce package (`ssot_leaf_ids` + `ssot_exit_status`); missing evidence refused (P-020).

## Audit criteria

**Met** iff:

1. The produce package directory declares SSOT exit evidence (in ADVERSARIAL.md or dedicated SSOT evidence file).
2. `ssot_leaf_ids` present with ≥1 opaque leaf id.
3. `ssot_exit_status` present with non-empty status value.
4. Leaf ids are non-empty opaque strings (shape may be UUID; product API validation is out of BBA scope).

**Not met** otherwise; enumerate missing/empty fields.

## Evidence

- `reviews/pr-*/ADVERSARIAL.md` — `ssot_leaf_ids` / `ssot_exit_status`
- Or `reviews/pr-*/SSOT-EXIT.md` — dedicated evidence file (optional)

## Related

- S8, CS7, P-020 — ADR 0005
```

Do **not** require a product-named evidence file (e.g. NOTION.md).

---

## integrity/binding-matrix.json

For requirements `S8` and `CS8` only:

- Replace `statement` with the abstract statements from `CHARTER-EDIT.md` §4
- Keep: `"surface": "reference"`, `"status": "unbound"`, `"binder": ""`, audit ids / audit_def paths unchanged

---

## ADR file ops

1. Write `adrs/0005-ssot-exit-evidence.md` from kit `ADR-0005-ssot-exit-evidence.md`
2. Delete `adrs/0005-notion-exit-evidence.md`
3. Grep for `0005-notion-exit-evidence` and fix links

---

## Global grep gate (before handoff)

Fail the land if these appear as **required** vocabulary in charter / AGENTS.md / agents/*/AGENT.md|verbs.md / integrity/audits/A-S8.md|A-CS8.md / binding-matrix S8|CS8 statements:

- `notion_page_ids`, `notion_exit_status`
- `NOTION_EXIT_EVIDENCE`, `NOTION_EVIDENCE_MISSING`
- Prose requiring “Notion exit evidence” / “Notion page”

Historical mentions inside superseded ADR trail notes are discouraged in this delta; prefer clean rewrite. Rejected section of ADR 0005 may name Notion once as a rejected option.
