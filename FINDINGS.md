# Findings — what is left

SSOT for undone work. Do not hunt TODO vs HOLES vs USE-CASES.
[Charter](docs/TERMS.md#charter) SSOT remains `CHARTER.md`. In-reach v1 Python gates are closed.
**Do not mint an R id until a binder exists (R27).**

Last pass: `0e57e3a` (release prep; tag v0.1.1 when ready).

---

## Human (not a queue)

| Item | What to do |
|------|------------|
| Promotion / [ship](docs/TERMS.md#ship) | `./nlc verify` on PRs; `./nlc verify-deep` after material changes; `ship-check` at promotion. See [`docs/nlc/VERIFY-AND-SHIP.md`](docs/nlc/VERIFY-AND-SHIP.md), [`APP-VERIFY.md`](docs/nlc/APP-VERIFY.md). |
| Judgment | C24 / ratification / [noun](docs/TERMS.md#noun) honesty — see [ADR](docs/TERMS.md#adr) compliance TODO; fix [`HUMAN-JUDGMENT-GATES.md`](docs/nlc/HUMAN-JUDGMENT-GATES.md) drift (adversarial is machine+skill, not “human only”). |
| Signature | C24 refuses `Ratified-by: agent`. Cryptographic human signature is out of reach. |

---

## Needed (product incomplete without these)

From [`docs/USE-CASES.md`](docs/USE-CASES.md). [Hub](docs/TERMS.md#hub) ships **tools**, not product requirements (ADR 0016).

| ID | Gap |
|----|-----|
| [UC9](docs/TERMS.md#uc9) | Guided path: `./nlc maintainer regen-continue` / `regen-advance` + `/planit` per [goal](docs/TERMS.md#goal). |
| [UC14](docs/TERMS.md#uc14) | Richer conflict model over time (v1: `check-rule-adoption.py` + [ADR](docs/TERMS.md#adr) 0012). |
| [UC15](docs/TERMS.md#uc15) | [Brownfield](docs/TERMS.md#brownfield) bootstrap automation (greenfield: `nlc-init.py`). |
| [UC18](docs/TERMS.md#uc18) | Agent: `./nlc maintainer guide before-generate` before [PLANIT](docs/TERMS.md#planit) generate — documented in [`HARNESS.md`](docs/nlc/HARNESS.md); hooks v2 example only (`.nlc/hooks.example.json`). |
| **Packs v0.2** | [Requirement packs](docs/TERMS.md#requirement-pack): ingest → ratify → export → consume. |

---

## Parked (decided, not executable)

| Item | [ADR](docs/TERMS.md#adr) / doc | Missing [gate](docs/TERMS.md#gate) |
|------|-----------|--------------|
| [Code packs](docs/TERMS.md#code-pack) (UC16) | [`docs/LANGUAGE-SCANNER.md`](docs/LANGUAGE-SCANNER.md) | Per-stack scanner adapter. |
| Call-tree packs (UC20) | [ADR](docs/TERMS.md#adr) 0009, [`integrity/primitives.md`](integrity/primitives.md) | [Primitive](docs/TERMS.md#primitive) interior inventory per language. |
| [Rule IR](docs/TERMS.md#rule-ir) | [ADR](docs/TERMS.md#adr) 0007 | If-then runner over tags × primitives × facts. |
| Per-generate [gate](docs/TERMS.md#gate) binder | [ADR](docs/TERMS.md#adr) 0010, [PLANIT](docs/TERMS.md#planit) 6.5 | Record that metrics existed and the artifact [gate](docs/TERMS.md#gate) ran. **[Work queue](docs/TERMS.md#work-queue):** [`TODO`](TODO) § [ADR](docs/TERMS.md#adr) compliance. |
| No [noun inheritance](docs/TERMS.md#noun-inheritance) | [ADR](docs/TERMS.md#adr) 0008 | Bindable scan for subclass/mixin between nouns. |

---

## Housekeeping (not spine)

| Item | Note |
|------|------|
| Repo name | GitHub: `Zygotic-AI/Natural-Language-Coding`. Consumer brand: [NLC](docs/TERMS.md#nlc) (ADR 0011). |
| Doc map | [`docs/nlc/README.md`](docs/nlc/README.md) |
| Dual [PLANIT](docs/TERMS.md#planit) | `~/.agents/skills/planit` vs this repo. Prefer newer is a wish, not a [gate](docs/TERMS.md#gate). |
| [Interview](docs/TERMS.md#interview) skill | Grow miss log from compiles — [`INTERVIEW-PATTERNS.md`](docs/ai-compiled-systems/INTERVIEW-PATTERNS.md). |

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
