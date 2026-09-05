# Landing brief — abstract SSOT exit evidence (P-020 rewrite)

Draft owner: Reed, Quality Architect  
Land via Koan/cloud agent; adversarial separate; Richard ratifies after bot PASS only.  
Tags: grokbot, architecture, P-020

## Goal

Abstract PR #5’s tool-coupled P-020 surface into **tool-agnostic task/board SSOT exit evidence** inside the BBA architecture repo.

BBA remains an **architecture definition**. Field names, charter prose, AGENTS.md standing instructions, and agent verb contracts must not require a specific task-board product. Concrete tool bindings belong in a **separate implementation/bindings repo** (out of scope for this PR — do not invent that repo’s contents).

## Why prior MET is superseded (FAIL reason)

PR #5 landed (or is landable as) a Notion-named surface: `notion_page_ids`, `notion_exit_status`, `NOTION_EXIT_EVIDENCE`, `NOTION_EVIDENCE_MISSING`, and charter/AGENTS/agent prose that names Notion as the required vocabulary.

That is an **architecture-scope FAIL**: BBA charter/agent contracts imported a product binding. Prior fitness MET / adversarial PASS on that surface are superseded for architecture fitness; they do not authorize keeping Notion-named fields in BBA.

This delta keeps the **same refuse class** as S7/P-016 (fail-closed; missing evidence → `handoff_refused` / refuse MET / refuse PASS) and the same rule ids **S8** / **CS8**, audit ids **A-S8** / **A-CS8**, and decision id **P-020** / **ADR 0005**. Only the vocabulary and ADR file name change.

## Sequencing

**Preferred:** delta commit on the PR #5 branch (or follow-on commits on that branch) that rewrite the Notion surface in place.

**Alternative:** superseding PR that replaces Notion-named artifacts with the abstract surface before or instead of merging the Notion-coupled head.

Do **not** leave both Notion-named and abstract fields as dual required vocabulary. One SSOT exit-evidence contract only.

## File list (expected touch)

| Path | Action |
|------|--------|
| `CHARTER.md` | Replace §6 Step 2 package sentence; rewrite **S8** and **CS8** to abstract prose |
| `adrs/0005-notion-exit-evidence.md` | **Delete** (or replace by rename) |
| `adrs/0005-ssot-exit-evidence.md` | **Add** — full replacement ADR (tool-agnostic) |
| `AGENTS.md` | Rewrite P-020 standing instruction; no product brand |
| `agents/standards-steward/AGENT.md` | Completion + handoff-out → SSOT exit evidence |
| `agents/standards-steward/verbs.md` | `complete-produce` fields/enums/errors |
| `agents/quality-architect/verbs.md` | `preflight-fitness-handoff`, `score-fitness` |
| `agents/adversarial-auditor/AGENT.md` | Handoff-in + note |
| `agents/adversarial-auditor/verbs.md` | `audit-proposal`, `audit-diff` |
| `integrity/audits/A-S8.md` | Rewrite criteria to abstract fields |
| `integrity/audits/A-CS8.md` | Rewrite criteria to abstract fields |
| `integrity/binding-matrix.json` | Update S8/CS8 `statement` text only; keep `surface=reference`, `status=unbound`, `binder=""` |
| `reviews/pr-005/` (or new review dir for this delta) | Produce package dogfoods abstract fields |

## ADR rename

- From: `adrs/0005-notion-exit-evidence.md`
- To: `adrs/0005-ssot-exit-evidence.md`
- Keep ADR number **0005** and P-020 identity; rewrite content.

## Canonical vocabulary (use exactly)

| Kind | Token |
|------|--------|
| Fields | `ssot_leaf_ids` (array of opaque leaf ids from the task/board SSOT; ≥1), `ssot_exit_status` (non-empty exit state string) |
| Missing enum | `SSOT_EXIT_EVIDENCE` |
| Error code | `SSOT_EVIDENCE_MISSING` |
| Rule prose | “task/board SSOT exit evidence” / “SSOT exit evidence” |
| Rule / audit ids | **S8**, **CS8**, **A-S8**, **A-CS8** (unchanged) |

Leaf id values may be UUID strings used as **opaque data**. Do not label fields or charter prose with a product name.

## What NOT to include

- Notion brand (or any other board product brand) as required vocabulary in charter, AGENTS.md, agent AGENT.md/verbs.md field names, audit defs, or matrix statements
- MCP, Cursor, or Grok product bindings as architecture requirements
- Dual required fields (`notion_*` **and** `ssot_*`)
- Implementation/bindings repo contents, binders, or API clients
- False binders for S8/CS8 (remain **reference** / **unbound**, P7)
- Product application code

## Verify expectations

After land, structural verify must show:

1. No required `notion_page_ids` / `notion_exit_status` / `NOTION_EXIT_EVIDENCE` / `NOTION_EVIDENCE_MISSING` in BBA charter/agents/audits/matrix statements (stale mentions in superseded notes may be removed in the same change).
2. Abstract fields and tokens present in steward/QA/auditor verb contracts and A-S8/A-CS8.
3. Charter Step 2, S8, CS8 use “task/board SSOT exit evidence” prose.
4. ADR file is `adrs/0005-ssot-exit-evidence.md`; old Notion-named ADR file gone.
5. Produce package dogfoods `ssot_leaf_ids` / `ssot_exit_status` (opaque leaf allowed).
6. S8/CS8 still `reference` + `unbound`.

Draft verify script: `PRODUCE_PACKAGE/verify.sh` in this kit.

## Source drafts (this kit)

- `CHARTER-EDIT.md`
- `ADR-0005-ssot-exit-evidence.md`
- `AGENT-PACKAGE-EDITS.md`
- `PRODUCE_PACKAGE/`
- `FITNESS_NOTE.md`

## Out of scope

- Inventing the bindings/implementation repo
- CI binders for S8/CS8
- Session gate wiring
- Reopening unrelated PR scopes
