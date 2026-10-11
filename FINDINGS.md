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

Last pass (26-09-25): `/release` closeout — agent instructions (literal scope, plain-language refs), integration leaf on_main, CI:MET + release-prep ready. Shipped git tag still **`v0.1.0` only**; `integrity/nlc-version.json` **0.2.0** until `./release`. Inference: [`integrity/full-nlc-audit-inference-record.json`](integrity/full-nlc-audit-inference-record.json). UC14/16/20 expansion remains parked.

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

Hub **no shipped tag** on current `main` history (mistaken `v0.2.0` removed); `integrity/nlc-version.json` is **0.2.0** until the next `./release`. Promotion remains human (`ship-check`, not compile-green alone).

---

## Parked (decided, not executable)

**Scope SSOT:** dispositions and waves — [`integrity/product-completion-scope.json`](integrity/product-completion-scope.json) ([ADR 0041](adrs/0041-product-completion-scope.md)).

**Badge:** every row below is `gate missing` — Accepted ADR / decided expansion ≠ wired deep gate.

| Item | [ADR](docs/TERMS.md#adr) / doc | Missing [gate](docs/TERMS.md#gate) | Badge |
|------|-----------|--------------|-------|
| Hub BBA interiors (X4) | ADR 0024 / [`HUB-BBA-DOGFOOD.md`](docs/nlc/HUB-BBA-DOGFOOD.md) | emit-path + lib + assert + **all** `fitness-*` noun-backed (`fitness-hub-x4-tranche-t4.py`) | **done** (v2 hub dogfood) |
| [Code packs](docs/TERMS.md#code-pack) (UC16) | [`docs/LANGUAGE-SCANNER.md`](docs/LANGUAGE-SCANNER.md) | Reference **typescript** adapter path (`examples/non-python-with-adapter`) | **done** (v1 reference; full scanner spec = expansion) |
| Call-tree packs (UC20) | ADR 0009 | Reference TS pack [`examples/call-tree-pack-reference`](examples/call-tree-pack-reference) | **done** (v1 reference; additional stacks = expansion) |
| [Rule IR](docs/TERMS.md#rule-ir) | ADR 0007 / [0042](adrs/0042-rule-ir-hub-product-boundary.md) | Snapshot + UC4 semantic runner + UC5 semantic apply (`check_semantic_apply`, `nlc:obligation=` receipts) | **done** (v2 hub; UC14 composable IR remains expansion) |
| ADR 0029 lineage tools | ADR 0029 | **Closed** — lineage-check + bind-snapshot + freshness + fitness | done |
| RCA packet schema | ADR 0025 | `validate-rca-packet.py` + schema | done |

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
