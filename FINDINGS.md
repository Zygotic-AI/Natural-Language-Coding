# Findings — what is left

SSOT for undone work. Do not hunt TODO vs HOLES vs USE-CASES.
Charter SSOT remains `CHARTER.md`. In-reach v1 Python gates are closed.
**Do not mint an R id until a binder exists (R27).**

Last pass: `16578c3` (release prep; tag v0.1.0 when ready).

---

## Human (not a queue)

| Item | What to do |
|------|------------|
| Promotion / ship | Run fitness on every PR; gate each generate (ADR 0010); use `release-audit.py` at QA/promotion — not only production. See [`docs/nlc/PROVE-AND-SHIP.md`](docs/nlc/PROVE-AND-SHIP.md). |
| Judgment | “Would this noun be a lie?”, “are these related?”, “does this verb belong on *this* noun?” — R1 / C3 / R4. No static gate. |
| Signature | C24 refuses `Ratified-by: agent`. Cryptographic human signature is out of reach. |

---

## Needed (product incomplete without these)

From [`docs/USE-CASES.md`](docs/USE-CASES.md). Hub ships **tools**, not product requirements (ADR 0016).

| ID | Gap |
|----|-----|
| UC9 | Rule-tagged blast radius (v2); orchestrate queue shipped — execute via Planit per step. |
| UC14 | Richer conflict model over time (v1: `check-rule-adoption.py` + ADR 0012). |
| UC15 | Brownfield bootstrap automation (greenfield: `nlc-init.py`). |
| UC18 | Harness must call `nlc-before-generate` every generate — see [`docs/nlc/HARNESS.md`](docs/nlc/HARNESS.md). |
| **Packs v0.2** | Requirement packs: ingest → ratify → export → consume. |

---

## Parked (decided, not executable)

| Item | ADR / doc | Missing gate |
|------|-----------|--------------|
| Language packs (UC16) | [`docs/LANGUAGE-SCANNER.md`](docs/LANGUAGE-SCANNER.md) | Per-stack scanner adapter. |
| Call-tree packs (UC20) | ADR 0009, [`integrity/primitives.md`](integrity/primitives.md) | Primitive interior inventory per language. |
| Rule IR | ADR 0007 | If-then runner over tags × primitives × facts. |
| Per-generate gate binder | ADR 0010, PLANIT 6.5 | Record that metrics existed and the artifact gate ran. |
| No noun inheritance | ADR 0008 | Bindable scan for subclass/mixin between nouns. |

---

## Housekeeping (not spine)

| Item | Note |
|------|------|
| Repo name | GitHub: `Zygotic-AI/Natural-Language-Coding`. Consumer brand: NLC (ADR 0011). |
| Doc map | [`docs/nlc/README.md`](docs/nlc/README.md) |
| Dual PLANIT | `~/.agents/skills/planit` vs this repo. Prefer newer is a wish, not a gate. |
| Interview skill | Grow miss log from compiles — [`INTERVIEW-PATTERNS.md`](docs/ai-compiled-systems/INTERVIEW-PATTERNS.md). |

---

## Explicitly not left undone

- Merge AIMS + BBP into CHARTER
- Binding matrix v1 (all published ids bound)
- In-reach fitness + landmines + `ci_fitness.py`
- `release-audit.py` (unsigned invoice-correct cannot ship)
- PLANIT 0–7 + 6.5 in PROCESS / skill
- ADRs 0004–0006, 0008–0016 Accepted (0004/0005 accepted 2026-09-20)
- Primitives SSOT file exists (v1 names)
- Use-case map UC1–UC21 (UC19 retired per ADR 0016)
