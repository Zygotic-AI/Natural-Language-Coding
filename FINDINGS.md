# Findings — what is left

SSOT for undone work. Do not hunt TODO vs HOLES vs USE-CASES.
Charter SSOT remains `CHARTER.md`. In-reach v1 Python gates are closed.
**Do not mint an R id until a binder exists (R27).**

Last pass: `2063ed5` (ADRs 0008–0010). This file records leftovers after that.

---

## Human (not a queue)

| Item | What to do |
|------|------------|
| Ship | Hook `python3 tools/release-audit.py <tree>` in the real pipeline. Write `Released-by:` / `Ratified-by:` yourself. Compile-green ≠ released. |
| Judgment | “Would this noun be a lie?”, “are these related?”, “does this verb belong on *this* noun?” — R1 / C3 / R4. No static gate. |
| Signature | C24 refuses `Ratified-by: agent`. Cryptographic human signature is out of reach. |

---

## Needed (product incomplete without these)

From [`docs/USE-CASES.md`](docs/USE-CASES.md). Not optional polish.

| ID | Gap |
|----|-----|
| UC9 | Orchestrated delta-regen (v1: `nlc-delta-regen.py` plan only). |
| UC14 | Richer conflict model over time (v1: `check-rule-adoption.py` + ADR 0012). |
| UC15 | Brownfield bootstrap automation (greenfield: `nlc-init.py`). |
| UC18 | Deeper harness auto-call of `load-knowledge-domain` (CLI exists). |
| UC19 | Full PCI certification path (v1: PAN worked example). |

---

## Parked (decided, not executable)

| Item | ADR / doc | Missing gate |
|------|-----------|--------------|
| Language scanner | [`docs/LANGUAGE-SCANNER.md`](docs/LANGUAGE-SCANNER.md) | Spec, then thin adapter. Source gates are Python-only. |
| Rule IR | ADR 0007 | If-then runner over tags × primitives × facts. |
| Primitive interiors | ADR 0009, [`integrity/primitives.md`](integrity/primitives.md) | Call-tree inventory; raw I/O outside `write`/`read`/… fails. |
| Per-generate gate | ADR 0010, PLANIT 6.5 | Record that metrics existed and the artifact gate ran before the next statement. |
| No noun inheritance | ADR 0008 | Bindable scan for subclass/mixin between nouns. |

Reviewers treat the parked rows as **findings** until those gates exist.

---

## Housekeeping (not spine)

| Item | Note |
|------|------|
| ADR 0004, 0005 | Status still `needs_review` (AIMS leftover). |
| Repo name | GitHub: `Zygotic-AI/Natural-Language-Coding`. Consumer brand: NLC (ADR 0011). |
| Dual PLANIT | `~/.agents/skills/planit` vs this repo. Prefer newer is a wish, not a gate. |
| Interview skill | `/interview` + [INTERVIEW-PATTERNS.md](docs/ai-compiled-systems/INTERVIEW-PATTERNS.md) v1; grow miss log from compiles. |
| UC15 bootstrap | Doc + template stub shipped; no one-shot CLI yet. |

---

## Explicitly not left undone

- Merge AIMS + BBP into CHARTER
- Binding matrix v1 (all published ids bound)
- In-reach fitness + landmines + `ci-fitness.sh`
- `release-audit.py` (unsigned invoice-correct cannot ship)
- PLANIT 0–7 + 6.5 in PROCESS / skill (ceremony, not the runner)
- ADRs 0006–0010 Accepted
- Primitives SSOT file exists (v1 names)
- Use-case map UC1–UC21
