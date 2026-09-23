# Findings — what is left

**Live gap SSOT.** Human / Needed / Parked / Housekeeping live here.
Do not treat [`HOLES.md`](HOLES.md), root [`TODO`](TODO), or [`docs/USE-CASES.md`](docs/USE-CASES.md) as a second queue.

| File | Role |
|------|------|
| **This file** | Live undone-work SSOT |
| [`docs/USE-CASES.md`](docs/USE-CASES.md) | Narrative UC map (what the practice *does*) |
| [`integrity/uc-product-status.json`](integrity/uc-product-status.json) | Machine product/binder status; CI gates TODO `@done` |
| [`TODO`](TODO) | Historical work log + CI evidence rows — **not** a second queue |
| [`HOLES.md`](HOLES.md) | Historical closed-gate ledger — **not** live SSOT |
| [`docs/nlc/SESSION-FOLLOWTHROUGH.md`](docs/nlc/SESSION-FOLLOWTHROUGH.md) | Eval-session execution queue (E/X ids) |

[Charter](docs/TERMS.md#charter) SSOT remains `CHARTER.md`. In-reach v1 Python gates are closed.
**Do not mint an R id until a binder exists (R27).**

Last pass: `feat/nlc-pipeline-wiring-clean` (ADR 0030 wires X1/X2/X3/X5/X6 via `nlc-pipeline-wire.py`).

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
| **Packs v0.2 consume** | `hub_v02.pack_consume_regen` is **open**: scope data/tags + auto UC9 regen hook after pack install. Ingest is closed. |
| **Packs registry** | `hub_v02.pack_registry` is **open** (optional / out of band). |

Hub ship remains a **human** last step (`./release`).

---

## Parked (decided, not executable)

| Item | [ADR](docs/TERMS.md#adr) / doc | Missing [gate](docs/TERMS.md#gate) |
|------|-----------|--------------|
| Hub BBA interiors (X4) | ADR 0024 corpus `bba` | rewrite `tools/*.py` as noun/verb packages |
| [Code packs](docs/TERMS.md#code-pack) (UC16) | [`docs/LANGUAGE-SCANNER.md`](docs/LANGUAGE-SCANNER.md) | Per-stack scanner adapter |
| Call-tree packs (UC20) | ADR 0009 | Per-stack packs beyond Python `domain/` |
| [Rule IR](docs/TERMS.md#rule-ir) | ADR 0007 | Full semantic runners |

---

## Housekeeping (not spine)

| Item | Note |
|------|------|
| E1 CHARTER corpus sentence | Two-line insert still open if not on `CHARTER.md` |
| E2 TERMS obligation/corpus | Drafted; land with TERMS edit |
| E3 explicit ci_fitness 0024 | Glob already runs `fitness-*.py`; explicit run optional |
| CHARTER / DESCRIBE door | Still opens as BBP |

---

## Explicitly not left undone

- ADR 0024 factory spine + corpus map + v1 binder
- ADR 0025 no-blame / climb / buck-stops rules file
- ADR 0026: X1 action-plan, X2 reverse-audit, X3 emit-manifest
- ADR 0030: X1/X2/X3/X5/X6 sequenced by `nlc-pipeline-wire.py`
- Manifesto Belief section
- `nlc-hub-audit` skill
- FINDINGS as sole live gap queue
- PLANIT skill + HARNESS + PROCESS + ORCHESTRATION wired to the pipeline
