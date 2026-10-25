# RCA: Skills contain TERMS-link filler that makes YAML unloadable

**Date:** 2026-10-20  
**Context:** Natural-Language-Coding hub — v0.3.3 install copies `.agents/skills/*/SKILL.md` as-is  
**Status:** open (process named; preventive action tracked, not yet applied)

**Scope (user words):**

- “Run /conduct-root-cause-analysis on why the skills have the text causing load errors”
- “That's not high enough in the causal chain. Why does link_terms_dictionary.py have that defect?”
- “I want that risk added” (repo-relative links that go nowhere after install)
- “prior to release we should have a specific step… list of things that we would check to grow… installer to do the same… exact same checklist”

---

## 1. Error condition

**Observed (bounded, reproducible):**

- Tag `v0.3.3` peel `0ba5fd28cf264b1d39fae7129b51eedabbc435ad`.
- Install (`scripts/install.sh` → `goals/hub_install/execute.sh`) copies `.agents/skills/` into `~/.agents/skills` and copies `planit`, `interview`, `verify`, `bbp-proposer`, `bbp-reviewer`, `bbp-confirmer`, `bbp-recorder` into `~/.cursor/skills`. No rewrite.
- Those seven `SKILL.md` files have glossary-link filler in the YAML `name:` field, for example `name: [planit](../../../docs/TERMS.md#planit)`.
- PyYAML `safe_load` of that frontmatter raises `ParserError` (`expected <block end>, but found '<scalar>'`). `[planit]` is a YAML flow sequence; the leftover `(...)` is not valid after it.
- A skill whose frontmatter does not parse cannot load.

**This climb’s error condition (why the rewriter is shaped that way):**

- `link_terms_dictionary.py` walks `.agents/**/*.md` and treats YAML frontmatter as prose. It skips fenced ` ``` ` and inline backticks only. That is the defect in the tool, not an accident in one `name:` line.

**Not the error condition:** body-prose TERMS links below the closing `---`. Those are markdown. The load failure is the machine `name:` line.

---

## 2. Upstream chain (process before output)

| Step | Artifact / layer | What it did |
| ---- | ---------------- | ----------- |
| (symptom) | Installed `SKILL.md` YAML | `name:` holds `[term](docs/TERMS.md#anchor)` so the file cannot load |
| 6 | Install | Copies hub skill bytes as-is (`rsync` / `cp`) |
| 5 | `link_terms_dictionary.py` (emit) | Walks `.agents/**/*.md`; skips markdown fences / backticks; does **not** skip YAML frontmatter; wraps term-list headings |
| 4 | TERMS-link **contract** | `docs/TERMS.md` line 7 and `tools/README.md`: after editing the term list, “refresh links in **markdown across the repo**.” Input type = `*.md` glob. No prose-vs-machine split. |
| 3 | Content-type index | `content-types/HOW-TO-ADD.md` and `integrity/LEXICON.md` name ADR, integrity doc, agent noun, audit, example. **Skill is not a content type.** `SKILL.md` is therefore generic markdown. |
| 2 | Contribution Gate | CG-R2 / CG-R3 refuse add-X without a type recipe. They cannot fire on skills: Skill is not X. Shared-docs lexicon linking then applies as if skills were SSOT prose. |
| 1 | ADR 0010 (unbound on this emit) | “Never generate without metrics. Never pass generated output downstream before its gate.” Dated 2026-09-16 — before the linker (2026-09-21). Applies to skills and to tools Planit creates. No binder sees “this rewriter named a skill-load metric and the metric ran.” |

**Furthest controllable upstream point:** Skill is not a content type, so the TERMS-link contract is allowed to specify an untyped `*.md` rewriter. The linker has the frontmatter defect **because that contract produced it**.

**Why the linker’s own code looks like this (mechanism):**

- `iter_markdown_files` includes `ROOT / ".agents"` and every `*.md` under it.
- `process_line` skips `in_fence` and `` `code` `` — markdown’s own non-prose syntax.
- YAML frontmatter is **not** markdown syntax. With no Skill type recipe saying “the opening `---` block is machine YAML; `name` is an identifier,” the rewriter had no typed region to exclude.
- First write: `d09ee22` (PR #19, 2026-09-21) added `docs/TERMS.md`, added the linker, and rewrote `name: planit` → `name: [planit](...)` in the same squash. Parent still had `name: planit`.

**Reproduction (emit layer, still true):** `process_line("name: planit\n", …, in_fence=False)` yields the v0.3.3 text and `ParserError`. `name: release` / `name: full-nlc-audit` stay plain — those strings are not term-list headings. The tool is doing exactly what an untyped `*.md` contract asks.

---

## 3. Impact / scope

- A v0.3.3 install delivers unloadable `/planit`, `/interview`, `/verify`, and the four BBP leaf skills.
- Four other installed skills stay loadable only because their `name:` strings are not term-list headings — not because any type protected YAML.
- **Dead links after install (same publish boundary).** Repo-relative `../../../docs/…`, `../../../adrs/…`, `../../../agents/…` links work in the hub checkout. After install, skills live under `~/.agents/skills/`. Those `../..` paths resolve under the home directory, not the hub copy, so the targets do not exist on that machine. Intra-skill links (`references/…`, `../full-nlc-audit/SKILL.md`) travel with the skill tree and stay valid. The TERMS linker created many of the dead `docs/TERMS.md` links; authors also wrote repo links by hand.
- Patching only `process_file` to skip frontmatter leaves the contract intact. The next `*.md` rewriter (or a linker “improvement”) can break `name:` again.
- Hub ships `v0.2.0` through `v0.3.3` carry the rewritten bytes.

---

## 4. Timeline (brief)

| Time | Event |
| ---- | ----- |
| 2026-09-16 | ADR 0010 accepted: generate then gate; applies to skills and later tools |
| 2026-09-21 | `d09ee22` / PR #19: term list + “markdown across the repo” linker + rewritten skill YAML |
| 2026-09-21 → 2026-10-19 | `v0.2.0` … `v0.3.3` ship those bytes; Skill still not a content type |
| 2026-10-20 | Confirm: v0.3.3 install copies unloadable skills |
| 2026-10-20 | First RCA named the linker skip as the one thing (too low) |
| 2026-10-20 | Climb: why the linker has that defect — this record |

---

## 5. Mechanism on reproduction

**Confirmed (emit):** isolated `process_line` on clean `name: planit` produces the tagged bytes; YAML parse fails.

**Confirmed (process):** the linker’s skip set is markdown fences + inline code only; `frontmatter` does not appear in the noun. The written contract is “markdown across the repo.” Skill is absent from `content-types/HOW-TO-ADD.md` and from the LEXICON content-type list. CG-R3 cannot refuse “add/amend skill without a recipe” because Skill is not a named type.

---

## 6. Candidate roots (at most three)

| Candidate | §3 bar | Verdict |
| --------- | ------ | ------- |
| Restore the seven `name:` lines | Output-only | Reject |
| Linker skips YAML frontmatter | Fixes this emit; does not change the contract that produced a `*.md` rewriter | **Too low** (prior answer; contributing follow-up) |
| Skill is a content type whose recipe refuses unloadable YAML `name:`; TERMS-link may rewrite only regions marked prose | One process change; deterministic; earliest controllable; in-repo (Contribution Gate + type recipe) | **Survives** |

ADR 0010 without a rewriter binder is a contributing factor, not a second root: the missing Skill type is why no metric existed to bind.

---

## 7. The one thing

> What **one** deterministic, actionable thing, if it were different, would have **prevented this error condition from arising**?

**Answer:** Portable skill (`SKILL.md`) must be a **content type** with a **type recipe** whose gate refuses a `name:` that is not a plain identifier (frontmatter must parse as YAML). The TERMS-link contract may rewrite only regions that recipe marks as prose. That is the process that produced a linker which treats skill YAML as markdown.

---

## 8. Prevention test

> If **Skill had been a content type with that YAML-`name` gate, and the TERMS-link contract had been limited to recipe-marked prose,** had been in place **before** the linker was specified, **`link_terms_dictionary.py` walking `.agents/**/*.md` and wrapping `name: planit`** could not have occurred because **Contribution Gate CG-R2/CG-R3 would refuse an untyped `*.md` rewrite of a skill, and the linker contract would not have listed skill frontmatter as in-scope markdown.**

**Completed:** yes (mechanism: type boundary + contract scope; emit skip is how the current tool would then be written, not the root).

---

## 9. Contributing factors (optional)

- ADR 0010 already required per-artifact metrics before generate; no fail-capable binder records that a rewriter named and ran a skill-load gate (ADR 0010 text defers a new R id until that binder exists).
- Same squash introduced the term list, the linker, and the rewritten skills.
- Extra aliases `/planit`, `/interview`, `/verify` also wrap `description:` (not the parse break).
- `.cursor/skills` mirrors `.agents/skills`.
- Install copies faithfully (correct); it is not the producer.

---

## 10. Preventive action (single tracked item)

| Field | Value |
| ----- | ----- |
| Action | Add Skill as a content type (type recipe + Contribution Gate refuse) whose gate is: frontmatter parses as YAML and `name` is a plain identifier matching the folder; narrow the TERMS-link contract to recipe-marked prose |
| Owner | hub |
| Path / artifact | `content-types/HOW-TO-ADD.md`, `integrity/LEXICON.md` / `integrity/CONTRIBUTION.md`, `docs/TERMS.md` + `tools/README.md` contract lines; tracked in `TODO` |
| Verification | CG-R3/CG-R2 refuse a skill whose `name:` is a markdown link; linker contract text no longer says unbounded “markdown across the repo”; a landmine fixture with `name: [planit](...)` is NOT_MET |
| Belief / gate touch (ADR 0025) | Unsuitable process: untyped `*.md` lexicon rewrite of a shipped machine artifact. Touches Contribution Gate (CG-R2/CG-R3), content-type / type-recipe lexicon, and the TERMS-link contract. |

Landed on `release/v0.4.0`: Skill recipe in `content-types/HOW-TO-ADD.md`; gate is the same `nlc-skill-author-check.py` list. Live hub skills still fail that gate until the repair step.

---

## 11. Follow-up (the growable check — not a second root)

The Skill type recipe is still the one thing. The **step** that will grow is one checklist, used in two places:

| When | Command |
| ---- | ------- |
| Before release (`release-prep` / `full` audit) | `python3 tools/nlc-skill-author-check.py --root .agents/skills` |
| After install (same list on the copied tree) | `python3 tools/nlc-skill-author-check.py --root ~/.agents/skills` |

Checklist SSOT: `integrity/skill-author-checklist.json`. Add a check id there, then implement it in `tools/nouns/skill_author_check/`. Demand: [ADR 0054](../../adrs/0054-published-skill-author-contract.md) (Proposed published-skill author contract), use-case `goals/hub_skill_author_check`, and `fitness-skill-author-check-presence.py` (install must still invoke that use-case). This is not helper code.

**Checks now (discovered problems):**

1. `frontmatter-yaml` — `SKILL.md` frontmatter parses; `name` is a plain identifier matching the folder.
2. `in-skill-links` — relative markdown links resolve inside the published skills tree (no `../../../` repo paths that vanish after install).

Landmine: `examples/skill-author-check-landmine/` must stay `SKILL_AUTHOR:NOT_MET`.

Current hub skills still fail the live check. Repair `name:` lines and out-of-tree links, then the release step and post-install step can MET. The TERMS linker now skips `.agents/skills/` / `.cursor/skills/` so a refresh cannot rewrite published skills.

- Bind ADR 0010 for rewriter generates (metrics named + gate ran) so the next bulk markdown tool cannot ship without a typed region list.
