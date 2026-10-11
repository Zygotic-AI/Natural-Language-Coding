## Planit Evaluate-NLC wave-1 (audit → door)

**Audit SHA:** `d83c64a` (`origin/main`). **A1–A4:** PASS (plan audit constrained R6/R7 to wave-2).

### Landed before this wave (not re-opened)

| Notion / FINDINGS id | Status |
|----------------------|--------|
| P2.1 ADR 0024 corpus | Landed #31 |
| P2.2 X1–X6 runners | Landed #32–#35 |
| P2.3 wire ADR 0030 | Landed #36 |
| P2.4 ADR 0027–0029 | Landed #1 |
| A2 binding matrix | **89/89** (stale “51%” claim retired) |
| E1/E2 housekeeping | Closed in this wave |

### Still open after door wave (wave-2)

| Id | Note |
|----|------|
| A7 / A12 interiors | **Remain expansion** — wave P5; dogfood exists; full tools rewrite open ([`product-completion-scope.json`](integrity/product-completion-scope.json)) |
| P1.2 heroes | **Waived** — `bbp-*` ids under ADR 0011; NLC door done |
| Soft-green multi-lang | **Remain expansion** — wave P7.2; adapters parked until UC16/UC20 waves |

---

## Planit Evaluate-NLC wave-2 (residuals)

**Base:** `main` after #38 (`a5287e2`). **Branch:** `fix/eval-nlc-wave2-residuals`.

### Closed / soft-green this wave

| Id | Status |
|----|--------|
| A8–A10 RCA climb / buck-stops | **Bound** by [ADR 0025](adrs/0025-belief-no-blame-climb.md) + `rules/nlc-0025.json`; cited from CHARTER document control. RCA packet schema **done** (validate + fitness). |
| A11 door | **Done** #38 + permanence gate `fitness-charter-nlc-door.py` |
| A12 hub self-verify | **Soft-green closed for “exists”** — hub is subject of `./nlc verify`; see [`docs/nlc/HUB-BBA-DOGFOOD.md`](docs/nlc/HUB-BBA-DOGFOOD.md). Full tools noun/verb rewrite still open. |
| A7 dogfood (door + principles) | PRINCIPLES NLC-first preface; X4 dogfood docs; interior rewrite still parked |
| P1.1 ACS path | **Done** — content under `docs/nlc/compiler/`; stub at `docs/ai-compiled-systems/` |
| P1.2 hero audit | Table below |
| Soft-green multi-lang | Unchanged — adapters parked |

### P1.2 Consumer BBA/BBP hero audit (wave-2)

| Path | Issue | Fix |
|------|-------|-----|
| `CHARTER.md` | Was BBP-only H1 | NLC door (#38) + door fitness |
| `DESCRIBE.md` | BBP title | NLC hub title (#38) |
| `integrity/PRINCIPLES.md` | “(BBP)” title as product | NLC-roof preface; P1 clarified under-covers |
| `docs/nlc/compiler/*` | ACS folder name | Residue banner; rename parked |
| `README.md` / `docs/nlc/*` | NLC-first already | No change |
| `bbp-*` tool/skill ids | Under-covers nouns | Leave (ADR 0011) |

### Still parked after wave-2

| Item | Why |
|------|-----|
| ACS path rename | **Done** — `docs/nlc/compiler/`; stub at old path |
| RCA packet schema binder | ADR 0025 expansion gate |
| Hub tools noun/verb rewrite | X4 BOUNDARY tranche + **RuleReceipt noun pilot**; remainder open |
| A1 per-rule ADRs | **Done** — ADR 0031–0037; R backlog + non-R (`0037`) in [`charter-ratify-backlog.json`](integrity/charter-ratify-backlog.json) |

---

## Planit Evaluate-NLC wave-3 (coverage close)

**Branch:** `fix/eval-nlc-coverage-close`. Closes download/child gaps from the coverage audit.

| Item | Status |
|------|--------|
| Notion `manifesto.md` attachment | Merged Principles 5–6 + layer stack into docs SSOT; **full body at root** `MANIFESTO.md` |
| `nlc-hub-audit` skill | Replaced with Notion draft + Gate section (`.agents/skills/nlc-hub-audit/`) |
| P2.6 `gate missing` badges | USE-CASES expansion + FINDINGS Parked + JTBD pointer |
| Notion Status sync | Evaluate-NLC leaf + children (this PR) |
| Still parked | X4 full noun/verb rewrite; packs registry (out-of-band); ADR 0007/0009/UC16/UC20 expansion |

---

## Planit parked residual queue (post wave-3)

One produce leaf / PR per row. Do not soft-green as done without evidence.

| Todo id | Work | Primary home |
|---------|------|--------------|
| **park-a1** | **Done** — ADR 0031–0037; backlog SSOT | [`integrity/charter-ratify-backlog.json`](integrity/charter-ratify-backlog.json) |
| **park-x4** | **Tranche-done** — emit-path BOUNDARY batch + remainder inventory; full noun/verb rewrite soft-green residual | [`integrity/hub-x4-remainder.json`](integrity/hub-x4-remainder.json) |
| **park-0029** | **Done** — lineage-check + bind-snapshot + freshness | ADR 0029 tools |
| **park-acs** | **Done** — content under `docs/nlc/compiler/`; `docs/ai-compiled-systems/` stub redirects only | [`docs/nlc/compiler/README.md`](docs/nlc/compiler/README.md) |
| **park-packs** | Consume **closed**; `pack_registry` remains **open** (out-of-band expansion) | FINDINGS Needed / hub_v02 |

---

## Parked residuals tranche — Phase 6 execution audit

**Verdict: PASS** (serial packs → 0029 → ACS → A1 → X4; each PR CI green before merge).

| Leaf | PR | Evidence |
|------|----|----------|
| park-packs | #42 | `pack_consume_regen` closed; registry out-of-band |
| park-0029 | #43 + #44 | lineage-check, bind-snapshot, freshness; hub_tool fix |
| park-acs | #45 | `docs/nlc/compiler/`; stub redirects |
| park-a1 | #46 | ADR 0031–0035 + `charter-ratify-backlog.json` |
| park-x4 | #47 | emit-path BOUNDARY batch + `hub-x4-remainder.json` |

### Soft-green residuals (explicitly out of this conclusion)

| Residual | Status |
|----------|--------|
| `hub_v02.pack_registry` public product | open / out-of-band |
| A1 non-R charter prose (§6, §16) | **Done** — [ADR 0037](adrs/0037-charter-non-r-surfaces.md) |
| X4 emit-path noun rewrite | **Complete** (`emit_path_complete`); **assert tranche complete** (`assert_tranche_complete`); fitness-only interior residual |
| ADR 0025 RCA packet schema binder | expansion |
| Full charter rule ADR coverage beyond R-ids | **Waived** — binding matrix (`audit-binding-matrix.py`) is SSOT; no numeric ADR coverage claim ([ADR 0041](adrs/0041-product-completion-scope.md)) |

**Handoff:** Notion Evaluate-NLC + this Last pass. `ssot_leaf_ids`: park-packs, park-0029, park-acs, park-a1, park-x4. `ssot_exit_status`: `program-complete-tranche`.

