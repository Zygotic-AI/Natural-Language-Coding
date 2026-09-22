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

[Charter](docs/TERMS.md#charter) SSOT remains `CHARTER.md`. In-reach v1 Python gates are closed.
**Do not mint an R id until a binder exists (R27).**

Last pass: `397b1a0` (A13 tracker alignment; eval baseline). Update this SHA on the landing commit of the alignment PR.

---

## Human (not a queue)

| Item | What to do |
|------|------------|
| Promotion / [ship](docs/TERMS.md#ship) | `./nlc verify` on PRs; `./nlc verify-deep` after material changes; `ship-check` at promotion. See [`docs/nlc/VERIFY-AND-SHIP.md`](docs/nlc/VERIFY-AND-SHIP.md), [`APP-VERIFY.md`](docs/nlc/APP-VERIFY.md). |
| Judgment | C24 / ratification / [noun](docs/TERMS.md#noun) honesty. Machine vs human split is current in [`docs/nlc/HUMAN-JUDGMENT-GATES.md`](docs/nlc/HUMAN-JUDGMENT-GATES.md) (rewritten 2026-09-20; drift row **closed**). |
| Signature | C24 refuses `Ratified-by: agent`. Cryptographic human signature is out of reach. |

---

## Needed (product incomplete without these)

v1 binders for UC9 / UC14 / UC15 / UC18 are **product-closed** in [`integrity/uc-product-status.json`](integrity/uc-product-status.json). Do not relist them here as if the spine is missing.

Remaining open product gaps:

| ID | Gap |
|----|-----|
| **Packs v0.2 consume** | `hub_v02.pack_consume_regen` is **open**: scope data/tags + auto UC9 regen hook after pack install. Ingest is closed. |
| **Packs registry** | `hub_v02.pack_registry` is **open** (optional / out of band). |

Hub ship itself remains a **human** last step (`./release`) — see Human row, not a missing compiler feature.

---

## Parked (decided, not executable)

Expansion-only leftovers. Accepted ADR ≠ wired deep gate. See USE-CASES “Needed (expansion)”.

| Item | [ADR](docs/TERMS.md#adr) / doc | Missing [gate](docs/TERMS.md#gate) |
|------|-----------|--------------|
| [Code packs](docs/TERMS.md#code-pack) (UC16) | [`docs/LANGUAGE-SCANNER.md`](docs/LANGUAGE-SCANNER.md) | Per-stack scanner adapter (step 2). v1 `language-scan` inventory is in force. |
| Call-tree packs (UC20) | [ADR](docs/TERMS.md#adr) 0009, [`integrity/primitives.md`](integrity/primitives.md) | Per-stack packs beyond Python `domain/` scan. |
| [Rule IR](docs/TERMS.md#rule-ir) | [ADR](docs/TERMS.md#adr) 0007 | Full semantic runners (encrypt/taint/engine) on every emit path. v1 snapshot runner is in force. |
| UC14 composable IR | [ADR](docs/TERMS.md#adr) 0012 | Cross-primitive policy beyond adopt-time conflicts. |
| UC15 brownfield full automation | [`docs/adoption/BROWNFIELD.md`](docs/adoption/BROWNFIELD.md) | Beyond inventory + migrate plan. |
| UC18 every-agent generate hook | [`docs/nlc/HARNESS.md`](docs/nlc/HARNESS.md) | Hooks beyond `.nlc/hooks.example.json` + stamp on compiled repos. |
| No [noun inheritance](docs/TERMS.md#noun-inheritance) | [ADR](docs/TERMS.md#adr) 0008 | Bindable scan for subclass/mixin between nouns (binder fitness exists; deep scan parked). |

Per-generate [gate](docs/TERMS.md#gate) binder (ADR 0010 / UC21) is **in force** (`gate-record` + verify blockers). Do not keep it in this parked table as if the gate were missing.

---

## Housekeeping (not spine)

| Item | Note |
|------|------|
| Repo name | GitHub: `Zygotic-AI/Natural-Language-Coding`. Consumer brand: [NLC](docs/TERMS.md#nlc) (ADR 0011). |
| Doc map | [`docs/nlc/README.md`](docs/nlc/README.md) |
| Dual [PLANIT](docs/TERMS.md#planit) | `~/.agents/skills/planit` vs this repo. Prefer newer is a wish, not a [gate](docs/TERMS.md#gate). |
| [Interview](docs/TERMS.md#interview) skill | Grow miss log from compiles — [`INTERVIEW-PATTERNS.md`](docs/ai-compiled-systems/INTERVIEW-PATTERNS.md). |
| CHARTER / DESCRIBE door | Still opens as BBP; NLC-first preface is a separate produce leaf (A11 / P0.1). Not this tracker pass. |

---

## Explicitly not left undone

- Merge [AIMS](docs/TERMS.md#aims) + [BBP](docs/TERMS.md#bbp) into [CHARTER](docs/TERMS.md#charter)
- [Binding matrix](docs/TERMS.md#binding-matrix) v1 (all published ids bound)
- In-reach fitness + landmines + `ci_fitness.py`
- `release-audit.py` (unsigned invoice-correct cannot ship)
- [PLANIT](docs/TERMS.md#planit) 0–7 + 6.5 in PROCESS / skill
- ADRs 0004–0006, 0008–0016 Accepted (0004/0005 accepted 2026-09-20)
- Primitives SSOT file exists (v1 names)
- Use-case map [UC1–UC21](docs/TERMS.md#uc1uc21) (UC19 retired per ADR 0016)
- `HUMAN-JUDGMENT-GATES.md` machine vs human split (closed 2026-09-20)
- In-reach HOLES row set (see historical [`HOLES.md`](HOLES.md))
