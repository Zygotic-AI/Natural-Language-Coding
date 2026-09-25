# Reply references — plain language (always)

**Applies to:** **every** user-facing agent message in this hub (and any chat where the human has loaded these standing instructions). Not only ship, not only “please decide.” **Whenever you reference something**, the human must not need a side trip to learn what it means.

**Lean:** bare internal ids in replies create **motion** (lookup) and **defect** (incomplete communication). You hold SSOT; **translate at the point of use**.

## What counts as a reference

Any user-visible mention of:

- **UC\***, **ADR\***, **P-\***, **R\***, **C\***, wave ids (P5, X4), tool-only names without role
- Repo paths that are not self-explanatory, when used as the main noun (“see `fitness-uc14-…`”)
- Acronyms (BBP, BBA, NLC, ASC) **on first use in the message** unless the thread already defined them

Deep links are fine **after** the gloss, not instead of it.

## Gate (default-closed)

Before sending a user-facing reply, every **blocking** row must be true:

| Criterion | Blocking? | Pass when |
| --------- | --------- | --------- |
| No bare ids | yes | No id-only list or id-only bullet as the **explanation** |
| Plain language | yes | Each cited id has a **same-message** gloss: one short sentence of **what it is / does** |
| Reader-complete | yes | A reader who has **not** opened USE-CASES, FINDINGS, or ADRs understands the point of the paragraph |
| Format | yes when ≥2 ids | Use a table (below); one id may be inline: **UC14** (composable rule IR across primitives — still expansion) |

## Table (two or more ids in one reply)

| Reference | Plain language |
| --------- | -------------- |

Add **Impact** or **Why it matters here** column when the reply is about ship, risk, or scope.

## Inline (single id)

**UC5** — rules applied on emit (markers + obligations), not only coverage landmines.

## Examples

**Fail:** “UC14, UC16, and UC20 remain expansion-only.”

**Pass:** “Three areas stay **expansion-only** (not in this tag’s scope): **UC14** — composable rule IR across primitives; **UC16** — per-language code-pack scanners; **UC20** — call-tree packs beyond Python `domain/`.”

**Fail:** “Re-run release-prep per ADR 0038.”

**Pass:** “Re-run **release-prep** (continuity manifest `./release` uses at prepare — ADR 0038 full-NLC audit profile).”

## Skills

All skills that produce user-facing text **inherit** this rule. [`/release`](../skills/release/SKILL.md) adds ship **impact** when citing product residuals.
