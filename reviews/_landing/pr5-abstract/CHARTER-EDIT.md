# Proposed charter edits — task/board SSOT exit evidence (P-020 abstract)

## Intent

Replace Notion-named produce-package evidence with **tool-agnostic task/board SSOT exit evidence**. Keep rule ids **S8** and checklist id **CS8**. Preserve fail-closed refuse class identical to S7/P-016. Do not import product brands into the charter.

## 1. §6 Step 2 — Produce package sentence (exact replacement)

**Find (PR #5 Notion surface):**

> **Produce package required for handoff.** Proposal completion includes the produce package: classification (plan A–F as above), applicability statement, boundary I/O declarations, self-adversarial notes, and Notion exit evidence (page id(s) + exit status). A proposal without this package is incomplete. Incomplete proposals do not hand off to fitness or adversarial review.

**Replace with:**

> **Produce package required for handoff.** Proposal completion includes the produce package: classification (plan A–F as above), applicability statement, boundary I/O declarations, self-adversarial notes, and task/board SSOT exit evidence (`ssot_leaf_ids` + `ssot_exit_status`). A proposal without this package is incomplete. Incomplete proposals do not hand off to fitness or adversarial review.

## 2. §16.6 — Rule S8 (exact replacement)

**Find:**

> **S8.** Produce packages require Notion exit evidence. Packages must include Notion page id(s) and exit status. Missing Notion evidence triggers `handoff_refused` (same refuse class as S7); fitness scoring refuses MET; adversarial audit refuses PASS (P-020).

**Replace with:**

> **S8.** Produce packages require task/board SSOT exit evidence. Packages must include `ssot_leaf_ids` (one or more opaque leaf ids from the task/board SSOT) and `ssot_exit_status` (non-empty exit state string). Missing SSOT exit evidence triggers `handoff_refused` (same refuse class as S7); fitness scoring refuses MET; adversarial audit refuses PASS (P-020).

## 3. §16.7 — Checklist CS8 (exact replacement)

**Find:**

> - [ ] CS8. Notion exit evidence present in produce package (page id(s) + exit status); missing evidence refused (P-020).

**Replace with:**

> - [ ] CS8. Task/board SSOT exit evidence present in produce package (`ssot_leaf_ids` + `ssot_exit_status`); missing evidence refused (P-020).

## 4. Binding matrix statement text (same change-set)

Update statements only; keep `surface: reference`, `status: unbound`, `binder: ""`, audit ids A-S8 / A-CS8.

**S8 statement:**

> Produce packages require task/board SSOT exit evidence. Packages must include ssot_leaf_ids (one or more opaque leaf ids from the task/board SSOT) and ssot_exit_status (non-empty exit state string). Missing SSOT exit evidence triggers handoff_refused; fitness scoring refuses MET; adversarial audit refuses PASS (P-020).

**CS8 statement:**

> Task/board SSOT exit evidence present in produce package (ssot_leaf_ids + ssot_exit_status); missing evidence refused (P-020).

## Unchanged

- Step 2.5 preflight refuse ≠ FAIL vocabulary
- S7 / CS7
- Fail-closed pattern (missing → `handoff_refused` / refuse MET / refuse PASS)
- S8/CS8 remain reference/unbound (P7)

## Out of scope for this edit

Product-specific board bindings; MCP/API clients; binders for S8/CS8; inventing a bindings repo.
