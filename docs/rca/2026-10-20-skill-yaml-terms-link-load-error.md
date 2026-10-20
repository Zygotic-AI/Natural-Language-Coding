# RCA: Skills contain TERMS-link filler that makes YAML unloadable

**Date:** 2026-10-20  
**Context:** Natural-Language-Coding hub — v0.3.3 install copies `.agents/skills/*/SKILL.md` as-is  
**Status:** open (process named; preventive action tracked, not yet applied)

**Scope (user words):** “Run /conduct-root-cause-analysis on why the skills have the text causing load errors”

---

## 1. Error condition

**Observed (bounded, reproducible):**

- Tag `v0.3.3` peel `0ba5fd28cf264b1d39fae7129b51eedabbc435ad`.
- Install (`scripts/install.sh` → `goals/hub_install/execute.sh`) copies `.agents/skills/` into `~/.agents/skills` and copies `planit`, `interview`, `verify`, `bbp-proposer`, `bbp-reviewer`, `bbp-confirmer`, `bbp-recorder` into `~/.cursor/skills`. No rewrite.
- Those seven `SKILL.md` files have glossary-link filler in the YAML `name:` field, for example `name: [planit](../../../docs/TERMS.md#planit)`.
- PyYAML `safe_load` of that frontmatter raises `ParserError` (`expected <block end>, but found '<scalar>'`). `[planit]` is a YAML flow sequence; the leftover `(...)` is not valid after it.
- A skill whose frontmatter does not parse cannot load.

**Inferred (not used as the one thing):**

- Cursor skill discovery treats invalid frontmatter as a load error (same parse failure any YAML loader hits).

**Not the error condition:** body-prose TERMS links below the closing `---`. Those are markdown. The load failure is the machine `name:` line.

---

## 2. Upstream chain (process before output)

| Step | Artifact / layer | What it did |
| ---- | ---------------- | ----------- |
| (symptom) | Installed `SKILL.md` YAML | `name:` holds `[term](docs/TERMS.md#anchor)` so the file cannot load |
| 5 | Install | Copies hub skill bytes as-is (`rsync` / `cp`) |
| 4 | Fitness / ship | No gate that `SKILL.md` frontmatter must parse as YAML with a plain identifier `name` |
| 3 | `tools/nouns/link_terms_dictionary/link_terms_dictionary.py` | Walks `.agents/**/*.md`, skips fenced ` ``` ` only, does **not** skip the opening `---` YAML frontmatter, wraps TERMS headings in `[text](docs/TERMS.md#slug)` |
| 2 | Tool contract | `docs/TERMS.md` + `tools/README.md`: after editing the term list, run the linker “across the repo” |
| 1 | First write | Commit `d09ee22` (PR #19, 2026-09-21) added `docs/TERMS.md`, added the linker, and rewrote existing `name: planit` → `name: [planit](...)` in the same squash. Parent still had `name: planit`. |

**Furthest controllable upstream point:** the linker’s `process_file` / `process_line` path — it treats YAML frontmatter as prose.

**Mechanism confirmed on reproduction:** yes. Calling `process_line("name: planit\n", …, in_fence=False)` yields `name: [planit](../../../docs/TERMS.md#planit)` and that block is `ParserError`. The same function leaves `name: release` and `name: full-nlc-audit` unchanged — those strings are not `docs/TERMS.md` headings. That matches v0.3.3: seven skills with TERMS-heading names cannot load; four without those headings can.

---

## 3. Impact / scope

- A v0.3.3 install delivers unloadable `/planit`, `/interview`, `/verify`, and the four BBP leaf skills into both `~/.agents/skills` and `~/.cursor/skills`.
- `release`, `full-nlc-audit`, `nlc-hub-audit`, and `requirement-pack-ingest` remain loadable only because their `name:` strings are not term-list headings — not because the process protected YAML.
- Re-running the linker on a restored `name: planit` would write the defect again.
- Hub ships `v0.2.0` through `v0.3.3` all carry the rewritten bytes.

---

## 4. Timeline (brief)

| Time | Event |
| ---- | ----- |
| 2026-09-21 | `d09ee22` / PR #19 adds term list + linker and rewrites skill YAML `name:` lines |
| 2026-09-21 → 2026-10-19 | `v0.2.0` … `v0.3.3` ship those bytes; no skill-frontmatter parse gate |
| 2026-10-20 | Confirm: v0.3.3 install copies unloadable skills |
| 2026-10-20 | This RCA |

---

## 5. Mechanism on reproduction

**Confirmed.** Isolated call of the linker’s `process_line` on clean `name: planit` / `interview` / `verify` / `bbp-proposer` produces the exact `name: [term](../../../docs/TERMS.md#…)` text on tag `v0.3.3`. YAML parse then fails with the same `ParserError`. Names that are not term-list headings stay plain and parse.

Log: `/opt/cursor/artifacts/rca-skill-yaml-terms-link-mechanism.log`.

---

## 6. Candidate roots (at most three)

| Candidate | §3 bar | Verdict |
| --------- | ------ | ------- |
| Restore the seven `name:` lines by hand | Output-only; linker will rewrite again | Reject (§3.1 / §2.1) |
| Fitness that `SKILL.md` frontmatter must parse | Would have blocked **ship**; would not have stopped the linker **writing** the text | Contributing detection, not the one thing |
| Linker skips YAML frontmatter so `name:` cannot be wrapped | One, deterministic, actionable, preventive, in-repo | **Survives** |

---

## 7. The one thing

> What **one** deterministic, actionable thing, if it were different, would have **prevented this error condition from arising**?

**Answer:** `tools/nouns/link_terms_dictionary/link_terms_dictionary.py` must skip the opening YAML frontmatter (`---` … `---`) so term linking cannot rewrite `name:` or any other machine key.

---

## 8. Prevention test

> If **the linker skipped YAML frontmatter** had been in place **before** `d09ee22` ran, **`name: [planit](../../../docs/TERMS.md#planit)` (and the six sibling rewrites)** could not have occurred because **`name: planit` would never be passed to `link_segment`.**

**Completed:** yes (mechanism: frontmatter skip; reproduction shows `process_line` is what wraps the name).

---

## 9. Contributing factors (optional)

- Same squash introduced the term list, the linker, and the rewritten skills — no isolated review of machine YAML.
- No fitness/landmine parses `.agents/skills/*/SKILL.md` frontmatter.
- Extra aliases `/planit`, `/interview`, `/verify` also wrap those tokens in `description:` (description text is not the parse break; `name:` is).
- `.cursor/skills` is a copy/symlink of `.agents/skills`, so both trees got the same bytes.
- Install has no transform step (correct for integrity; it faithfully copies a defective producer).

---

## 10. Preventive action (single tracked item)

| Field | Value |
| ----- | ----- |
| Action | Skip YAML frontmatter in `link_terms_dictionary.py` so term linking cannot rewrite `name:` / other machine keys |
| Owner | hub |
| Path / artifact | `tools/nouns/link_terms_dictionary/link_terms_dictionary.py`; tracked in `TODO` |
| Verification | `process_line` / `process_file` leaves `name: planit` unchanged; PyYAML loads every `.agents/skills/*/SKILL.md` frontmatter; `name` is a plain identifier matching the folder |
| Belief / gate touch (ADR 0025) | Unsuitable process: linker treats machine YAML as prose. Closing this RCA also requires a refuse gate that unloadable `SKILL.md` names cannot ship (detection follow-up, not a second root). |

---

## 11. Follow-up (detection only)

- Fitness/landmine: every `.agents/skills/*/SKILL.md` frontmatter parses as YAML; `name` matches the skill folder (plain `[A-Za-z0-9-]+`).
- After the linker skip exists, restore the seven already-written `name:` values and refresh install hashes. Do not treat that restore as the root — without the skip, the next linker run rewrites them.
