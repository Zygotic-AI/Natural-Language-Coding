# ADR 0041 — Hub product completion scope SSOT

- Status: Accepted
- Date: 2026-09-23
- Deciders: Human manager
- Class: F (process / product)
- Corpus: nlc

## Context

[`FINDINGS.md`](../FINDINGS.md) and [`integrity/uc-product-status.json`](../integrity/uc-product-status.json) list overlapping product gaps (Needed, Parked, `expansion_only`). Without a single scope record, continuity audits confuse **ship blockers** with **accepted expansion**, and agents re-litigate the same rows.

## Decision

1. **Scope SSOT:** [`integrity/product-completion-scope.json`](../integrity/product-completion-scope.json) maps every FINDINGS product row and every `expansion_only` / `hub_v02.pack_registry` key to **`in_reach_v2`**, **`remain_expansion`**, or **`waive`**, with wave id and acceptance test string.

2. **Disposition rules:**
   - **`in_reach_v2`** — must close in the cited TODO Product completion wave; same PR updates FINDINGS + `uc-product-status.json`.
   - **`remain_expansion`** — v1 product stays closed; deep gate may stay `gate missing` until acceptance MET.
   - **`waive`** — FINDINGS row struck or marked waived; no fake “done” binder.

3. **Pack registry v1:** Hub-local curated registry [`integrity/hub-pack-registry.json`](../integrity/hub-pack-registry.json) satisfies **Packs registry** Needed row. v1 is **not** a public internet registry; empty `packs` array is valid. When non-empty, `nlc-pack-install` refuses packs not listed (name + version).

4. **Changes to scope** require amending `product-completion-scope.json` and this ADR or a successor ADR in the same PR.

## Consequences

- `tools/fitness-product-completion-scope.py` refuses drift vs `uc-product-status.json` keys.
- `tools/fitness-hub-pack-registry.py` + `validate-hub-pack-registry.py` bind registry v1.
- TODO Product completion plan waves P0–P8 execute against scope rows.

## Rejected

- Closing expansion gaps by editing FINDINGS only without scope disposition.
- Treating “public registry on the internet” as in-reach for hub v0.2.x.
