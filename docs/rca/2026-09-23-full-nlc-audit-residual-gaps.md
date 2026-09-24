# RCA: Full NLC audit residuals (F1–F5 + product improvements)

**Date:** 2026-09-23  
**Context:** Natural-Language-Coding hub — first `full-nlc-audit --profile full` @ `5eedc34`  
**Status:** mitigated (26-09-23) — F1–F4 + product improvements landed; F5 skipped; see [`TODO`](../TODO) @done rows and `python3 tools/ci_fitness.py` → CI:MET

---

## 1. Error condition

**Evidence (observed):**

- Machine audit: `python3 tools/full-nlc-audit.py --check --profile full` → **FULL_NLC_AUDIT:MET** (exit 0).
- Inference pass: **PASS with residuals** — doc/SSOT drift and v1 product limits listed in TODO (F1–F5 + five improvements).
- Examples: [`FINDINGS.md`](../FINDINGS.md) line 41 claims `v0.2.0` on origin while shipped-tag stage reports no reachable `v*.*.*` on `main`; [`docs/ADR-ENFORCEMENT.md`](../docs/ADR-ENFORCEMENT.md) lists ADR 0029 as `gap` while FINDINGS marks 0029 tools done; `integrity/integration-leaves.json` empty after branch hygiene; audit report noted dirty tree and manual inference phases.

**Mechanism:** residuals are **latent SSOT drift** and **v1 scope limits**, not compile failures. They appeared on first holistic continuity audit because nothing in CI required cross-document or git-tag coherence for FINDINGS / enforcement prose.

---

## 2. Ecosystem pattern (what allowed the class of defect)

| Layer | What the environment allowed |
| ----- | ---------------------------- |
| **Multiple prose SSOTs** | `FINDINGS.md`, `docs/ADR-ENFORCEMENT.md`, `TODO`, and git tags evolve independently; fitness targets TODO↔UC and ADR↔FINDINGS gaps for **enforcement table** only, not FINDINGS ship narrative vs `git tag`. |
| **Incident without FINDINGS gate** | Mistaken `v0.2.0` tag + deletion updated tools/TODO but not FINDINGS “Needed” ship line — no “on tag change, refresh FINDINGS” binder. |
| **Human “Last pass” fields** | No machine check that FINDINGS header SHA/narrative matches `HEAD` or release state. |
| **ADR-ENFORCEMENT as manual table** | Row status updated asynchronously from binder landings; 0029 closed in product work without editing enforcement table. |
| **Scaffold without workflow** | `integration-leaves.json` added as empty registry with builtin audit stage but no **required** populate step in branch-delete / Planit hygiene. |
| **full-nlc-audit v1 scope** | Machine manifest only; inference, git cleanliness, and FINDINGS/tag lint deliberately deferred to TODO. |
| **Release wiring speed** | `./release` step 0c runs `full` profile (includes `verify-deep`) before later prepare `verify-deep` — no release-engineering gate on duplicate expensive stages. |

Root is not “audit missed it” — **no refusing gate existed** for most residuals until the first full audit made them visible.

---

## 3. Per-item: allowed → one preventive change

Each row is the **single** change that would have **prevented that residual from being possible** (or from persisting undetected).

### Doc / SSOT hygiene (inference F1–F5)

| ID | What allowed it | **The one thing** (preventive) |
| ---- | ---------------- | ------------------------------ |
| **F1** FINDINGS claims `v0.2.0` on origin; tags on `main` show none | FINDINGS edited by humans/agents; no CI reads FINDINGS ship lines against `nlc_release_shipped_tag_audit` / reachable tags | **`tools/fitness-findings-shipped-tag-sync.py`** in `ci_fitness.py`: fail if FINDINGS asserts a `vX.Y.Z` “tagged on origin” (or equivalent) when newest reachable tag on `HEAD` ≠ that version or is absent |
| **F2** “Last pass” narrative stale vs `5eedc34` and local batch | FINDINGS header is free text; no freshness criterion | **`tools/fitness-findings-last-pass-fresh.py`**: require “Last pass” block to cite `git rev-parse --short HEAD` of audited ref (or explicit `last_pass_sha:` frontmatter) within one merge of material hub changes |
| **F3** ADR-ENFORCEMENT 0029 `gap` vs FINDINGS “done” | Two tables; updating FINDINGS on close without enforcement-table sync step in Definition of Done | **`tools/fitness-adr-enforcement-table-sync.py`**: for each ADR id marked `done` / `bound` in FINDINGS Parked or `fitness-*` landmine list, ADR-ENFORCEMENT row must not be bare `gap` unless `expansion` / `docs/backlog` qualifier matches |
| **F4** Empty `integration-leaves.json` after branch work | Registry optional; branch hygiene TODO did not block “delete remote” until leaf row or `waived` | **Planit / branch-hygiene gate**: before marking branch cleanup done, require `integration-leaves.json` entry per deleted initiative **or** `waived: no claims` row in TODO with SHA — enforced by **`tools/fitness-integration-leaves-hygiene.py`** (non-empty or explicit waive file) |
| **F5** `nlc-version.json` 0.2.0, no shipped tag | By design between releases; only confusing in prose | **Waived** as defect — **one thing** if you want zero ambiguity: **`RELEASE.md` + preflight** already encode match rules; optional **`fitness-release-version-without-tag.py`** only when on `main` with no `release/v*` branch (document expected state, fail only if version **ahead** of tag without open release branch) |

### `full-nlc-audit` product improvements

| ID | What allowed it | **The one thing** (preventive) |
| ---- | ---------------- | ------------------------------ |
| **Inference manual** | v1 shipped machine-only; skill phases 0–7 not in manifest | **`full-nlc-audit.py --emit-inference-checklist`**: print fixed checklist path + empty JSON template; CI landmine asserts command exists and skill references it |
| **Dirty tree** | Audit does not inspect `git status`; verify-deep mutates `.nlc/verified.json` on dirty tree | **Manifest builtin `git_worktree_clean`** (default blocking; `--allow-dirty` for local) before other stages |
| **FINDINGS ↔ tag** | Same root as **F1** | Same fitness as F1 — do not duplicate; one tool |
| **Release `full` duplicate `verify-deep`** | Step 0c added for ADR 0038 without step-order review | **Split manifest profile `release-prep`**: same as `full` minus `verify-deep`/`verify` for `./release` 0c only; keep `full` for standalone audit — **or** document + accept duplicate (then **one thing** = RELEASE.md “~N min” + comment in manifest only) |
| **Integration-leaves guidance** | Feature landed without skill “when to populate” | **`.agents/skills/full-nlc-audit/SKILL.md` § When to write leaves** (blocking Done signal) + drift fitness fails if section missing |

---

## 4. Roll-up “one thing” (if only one program change)

If the hub can only ship **one** program change for the whole residual class:

> **Hub CI must run a `fitness-findings-ssot-sync.py` suite** that refuses merge-green when `FINDINGS.md` ship/tag narrative, ADR-ENFORCEMENT `gap` rows, and git reachable tags disagree — with F1/F3 as first rules and F2 as second tranche.

That would have surfaced F1–F3 before the first full-audit inference pass.

---

## 5. Prevention tests (samples)

- **F1:** If `fitness-findings-shipped-tag-sync.py` had existed before tag deletion, FINDINGS line 41 could not stay “v0.2.0 on origin” while shipped-tag audit reports none — **CI:NOT_MET**.
- **F3:** If enforcement-table sync existed, merging 0029 tools without updating ADR-ENFORCEMENT would fail CI.
- **Dirty tree:** If `git_worktree_clean` ran first, audit report would flag dirty tree before claiming a reproducible SHA audit.

---

## 6. repo_touch (ADR 0025)

| Layer | Citation |
| ----- | -------- |
| ADR | [0038](../adrs/0038-no-memory-in-process.md) (SSOT in gates, not prose) |
| Gate | `full-nlc-audit` machine MET; gaps = missing cross-SSOT fitness |
| Process | First continuity audit as detection; prevention = TODO fitness rows |

---

## 7. Tracked work

[`TODO`](../TODO) → **Full audit feedback (26-09-23)** — implement each **one thing** or close as `skip:` with fitness id.
