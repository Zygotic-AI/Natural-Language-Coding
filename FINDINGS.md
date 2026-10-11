# Findings — what is left

**Live gap SSOT.** Human / Needed / Parked / Housekeeping live here.
Do not treat [`HOLES.md`](HOLES.md), root [`TODO`](TODO), or [`docs/USE-CASES.md`](docs/USE-CASES.md) as a second queue.

| File | Role |
|------|------|
| **This file** | Live undone-work SSOT (Human / Needed / Parked / Housekeeping only) |
| [`docs/USE-CASES.md`](docs/USE-CASES.md) | UC narrative — **status gaps:** see this file |
| [`docs/JOBS-TO-BE-DONE.md`](docs/JOBS-TO-BE-DONE.md) | Adopter jobs — **blocking gaps:** see this file |
| [`integrity/uc-product-status.json`](integrity/uc-product-status.json) | Machine binder/product closure; **narrative gaps:** see this file |
| [`TODO`](TODO) | Stub → [`docs/history/TODO-work-log.md`](docs/history/TODO-work-log.md) |
| [`HOLES.md`](HOLES.md) | Stub → [`docs/history/HOLES.md`](docs/history/HOLES.md) |
| [`docs/nlc/SESSION-FOLLOWTHROUGH.md`](docs/nlc/SESSION-FOLLOWTHROUGH.md) | Stub → [`docs/history/SESSION-FOLLOWTHROUGH.md`](docs/history/SESSION-FOLLOWTHROUGH.md) |

[Charter](docs/TERMS.md#charter) SSOT remains `CHARTER.md`. In-reach v1 Python gates are closed.
**Do not mint an R id until a binder exists (R27).**

`last_pass_tree_hash:` see [`integrity/hub-content-tree-hash.txt`](integrity/hub-content-tree-hash.txt) (ADR 0050 content fingerprint; not a commit id).

Last pass (26-09-25): `/release` closeout — agent instructions (literal scope, plain-language refs), integration leaf on_main, CI:MET + release-prep ready. **Shipped tag prose:** generate from git only (`python3 tools/nlc_release_tags.py` / `fitness-findings-shipped-tag-sync.py` on HEAD — do not hand-write origin tag claims). `integrity/nlc-version.json` **0.2.0** until `./release`. Inference: [`integrity/full-nlc-audit-inference-record.json`](integrity/full-nlc-audit-inference-record.json).

---

## Human (not a queue)

| Item | What to do |
|------|------------|
| Promotion / [ship](docs/TERMS.md#ship) | `./nlc verify` on PRs; `./nlc verify-deep` after material changes; `ship-check` at promotion. |
| Judgment | C24 / ratification / [noun](docs/TERMS.md#noun) honesty. Machine vs human split is current in [`docs/nlc/HUMAN-JUDGMENT-GATES.md`](docs/nlc/HUMAN-JUDGMENT-GATES.md). |
| Signature | C24 refuses `Ratified-by: agent`. Cryptographic human signature is out of reach. |

---

## Needed (product incomplete without these)

v1 binders for UC9 / UC14 / UC15 / UC18 are **product-closed** in [`integrity/uc-product-status.json`](integrity/uc-product-status.json).

| ID | Gap |
|----|-----|
| **Packs v0.2 consume** | **Closed** — `nlc-pack-install` writes `.nlc/pack-consume-status.json` (scope + UC9 hint). |
| **Packs registry** | **Closed (v1)** — hub-local curated registry [`integrity/hub-pack-registry.json`](integrity/hub-pack-registry.json) ([ADR 0041](adrs/0041-product-completion-scope.md), [`docs/nlc/PACK-REGISTRY.md`](docs/nlc/PACK-REGISTRY.md)). Not a public internet registry. |
| **UC18 goal-write hook coverage** | **Partial (v0.3.0)** — Cursor `preToolUse` on `Write\|Delete` only (see [Cursor hooks](https://cursor.com/docs/hooks)). **Not covered:** `Shell` redirects into `goals/`, MCP tool writes, subagent `Task` writes. |
| **0045 ⊕ 0048 effective-decision view** | **Open** — Record [0045](adrs/0045-hub-release-identity.md) decision 2 still names `scripts/nlc-release.sh` as executor; [0048](adrs/0048-executable-shape.md) amends: policy in `goals/hub_release/execute.sh`, shell is thin entrypoint only. Need a read-only **effective-decision** view (do not edit 0045 receipts in place). |
| **Per-record behavior fixtures (D9)** | **Open** — each active ADR gate path needs a behavior fixture; the record gate must run its fixtures (see [`docs/history/TODO-work-log.md`](docs/history/TODO-work-log.md) Practice enforcement). |

Hub **no shipped tag** on current `main` history (mistaken `v0.2.0` removed); `integrity/nlc-version.json` is **0.2.0** until the next `./release`. Promotion remains human (`ship-check`, not compile-green alone).

---

## Parked (decided, not executable)

**Scope SSOT:** dispositions and waves — [`integrity/product-completion-scope.json`](integrity/product-completion-scope.json) ([ADR 0041](adrs/0041-product-completion-scope.md)).

**Badge:** every row below is `gate missing` — Accepted ADR / decided expansion ≠ wired deep gate.

| Item | [ADR](docs/TERMS.md#adr) / doc | Missing [gate](docs/TERMS.md#gate) | Badge |
|------|-----------|--------------|-------|
| Hub BBA interiors (X4) | ADR 0024 / [`HUB-BBA-DOGFOOD.md`](docs/nlc/HUB-BBA-DOGFOOD.md) | **Not done** — emit-path tranche MET; **368 of 370** hub `tools/nouns/*/` packages have **empty** `fields.txt` (two non-empty); **15** packages lack `fields.txt` entirely among **396** dirs. Full noun/verb interior + populated `fields.txt` still open ([`integrity/hub-x4-remainder.json`](integrity/hub-x4-remainder.json)). | **gate missing** |
| [Code packs](docs/TERMS.md#code-pack) (UC16) | [`docs/LANGUAGE-SCANNER.md`](docs/LANGUAGE-SCANNER.md) | Reference **typescript** adapter path (`examples/non-python-with-adapter`) | **done** (v1 reference; full scanner spec = expansion) |
| Call-tree packs (UC20) | ADR 0009 | Reference TS pack [`examples/call-tree-pack-reference`](examples/call-tree-pack-reference) | **done** (v1 reference; additional stacks = expansion) |
| [Rule IR](docs/TERMS.md#rule-ir) | ADR 0007 / [0042](adrs/0042-rule-ir-hub-product-boundary.md) | UC4/UC5 **v2 semantic** runner/apply MET on hub; [ADR 0042](adrs/0042-rule-ir-hub-product-boundary.md) **product boundary** still limits full semantic apply on every ad-hoc emit — composable UC14 IR expansion remains | **gate missing** (UC14 composable) |
| ADR 0029 lineage tools | ADR 0029 | **Closed** — lineage-check + bind-snapshot + freshness + fitness | done |
| RCA packet schema | ADR 0025 | `validate-rca-packet.py` + schema | done |

---

## Parked — JTBD blocking gaps (from jobs map)

Live narrative for adopters; mechanisms stay in [`docs/JOBS-TO-BE-DONE.md`](docs/JOBS-TO-BE-DONE.md).

| Job | Blocking gap |
|-----|----------------|
| **J1 — semantic apply** | Full ADR 0007 **semantic** apply on every emit path (not only hub specimens) — [`docs/ADR-ENFORCEMENT.md`](docs/ADR-ENFORCEMENT.md). |
| **J2 — tag blast radius** | UC16 adapters + full tag blast radius — [`docs/spine/IMPACT-GRAPH.md`](docs/spine/IMPACT-GRAPH.md). |
| **J7 — full product verify** | Full product `./nlc verify` (non-specimen) still evolving. |
| **J8 — rule-tagged narrowing** | Rule-tagged narrowing v2 (delta regen) expansion. |
| **J20 — bare `engine.runtime`** | Bare `engine.runtime` tag insufficient when goal declares `engine_runtime` (strict pairing). |

---

## Parked — session / holes leftovers

| Source | Gap |
|--------|-----|
| SESSION-FOLLOWTHROUGH | **hub tool interiors still open** — X4 v1 dogfood done; hub tool noun/verb interiors not rewritten. |
| SESSION-FOLLOWTHROUGH | **full noun/verb rewrite open** — remainder in [`integrity/hub-x4-remainder.json`](integrity/hub-x4-remainder.json). |
| HOLES (out of reach) | **R4 — verb belongs on this noun** — static gates cannot enforce “verb belongs on *this* noun” (judgment / design). |
| HOLES (out of reach) | **Python-only language limit** — source-level gates are Python-only; other languages need [`docs/LANGUAGE-SCANNER.md`](docs/LANGUAGE-SCANNER.md) spec + adapter (UC16 expansion). |

---

## Roadmap §2.4 reconciliations (live)

| Topic | True status (this tree) |
|-------|-------------------------|
| **Shipped tag prose** | **Machine SSOT** — `fitness-findings-shipped-tag-sync.py` + reachable tags on HEAD; do not hand-write “vX on origin” in FINDINGS. |
| **Rule IR vs ADR 0042** | Hub UC4/UC5 semantic gates MET; ADR 0042 draws product boundary — not every emit path is semantically bound; UC14 composable IR still **Parked** above. |
| **`uc-product-status` `expansion_only` vs FINDINGS UC14/16/20** | JSON binder closure for UC14/16/20 product rows must match **Parked** rows here (no `expansion_only` leftovers claiming open product when FINDINGS says parked). |
| **X4 “done” claim** | **Rejected** — empty `fields.txt` majority (368/370 review spot-check; 169/381 empty files in inventory) means interiors **not** done. |

---

## Housekeeping (not spine)

| Item | Note |
|------|------|
| E1 CHARTER corpus sentence | **Done** — corpus pointer on `CHARTER.md` (§3) |
| E2 TERMS obligation/corpus | **Done** — Corpus/Condition/Obligation in TERMS |
| E3 explicit ci_fitness 0024 | Glob already runs `fitness-*.py`; explicit run optional |
| CHARTER / DESCRIBE door | **Done** — #38 NLC-first door (BBP body retained) |

---

## Explicitly not left undone

- ADR 0024 factory spine + corpus map + v1 binder
- ADR 0025 no-blame / climb / buck-stops rules file
- ADR 0026: X1 action-plan, X2 reverse-audit, X3 emit-manifest
- ADR 0030: X1/X2/X3/X5/X6 sequenced by `nlc-pipeline-wire.py`
- Manifesto Belief section
- `full-nlc-audit` skill + `tools/full-nlc-audit.py` (replaces hub-audit entrypoint)
- FINDINGS as sole live gap queue
- PLANIT skill + HARNESS + PROCESS + ORCHESTRATION wired to the pipeline



---

Historical Planit wave ledgers (not live gaps): [`docs/history/findings-planit-waves-archive.md`](docs/history/findings-planit-waves-archive.md).
