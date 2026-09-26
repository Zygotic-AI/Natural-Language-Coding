# RCA: Agent told operator to delete completed `release/v0.2.0` (stale field overload)

**Date:** 2026-09-25  
**Context:** Natural-Language-Coding hub — zero-parameter `./release` session + operator challenge  
**Status:** prevented (`closed_release_branches` split from `stale_release_branches`)

---

## 1. Error condition

**Evidence (observed):**

- After `./release --dry-run` showed resume **`tag_ready`** for v0.2.0, agent applied a resume change so **`release/v0.2.0`** appeared under **`stale_release_branches`** while phase became **`prepare`**.
- Agent chat (same session) listed as operator next step: **“Delete stale `release/v0.2.0` (local + `origin`)"** — for a branch the operator described as **from the already completed v0.2.0 release process**.
- When operator objected, agent advised **reinterpreting** `stale_release_branches` (“orchestration closed, not garbage”) instead of correcting resume JSON semantics.
- SSOT before fix:
  - [RCA 2026-09-24](2026-09-24-release-resume-planned-tag-conflation.md): **`stale_release_branches`** = merged `release/v*` **without** `hub-release-record.json` on merge commit.
  - [`.agents/skills/release/SKILL.md`](../.agents/skills/release/SKILL.md) Step 1A: **delete every** name in **`stale_release_branches`**.

**Inferred:**

- Operator experience: agent asked them to **ignore defective/overloaded machine data** (one field, two meanings) rather than fix the contract.

**Mechanism confirmed on reproduction:** yes — `python3 tools/nlc_release_resume.py --emit json` after the zero-param resume patch placed **`release/v0.2.0`** in **`stale_release_branches`** when **`tag_exists("v0.2.0")`** even though merge had a release record (completed ship line, not missing-record stale).

---

## 2. Upstream chain (process before output)

| Step | Artifact / layer | What it did |
| ---- | ---------------- | ----------- |
| (symptom) | Agent chat | Recommended **deleting** `release/v0.2.0`; later counseled **ignoring** field meaning |
| 4 | Zero-param resume patch | Reused **`stale_release_branches`** for **closed/shipped** lines to skip `tag_ready` |
| 3 | `/release` skill Step 1A | Mandates **git delete** for all **`stale_release_branches`** names |
| 2 | RCA 2026-09-24 + `detect()` | Defined **`stale_release_branches`** only for **missing record** merges |
| 1 | Operator model | **`release/v0.2.0`** = historical release line for a **completed** version |

**Furthest controllable upstream point:** **`nlc_release_resume.detect()` output schema** — must not overload **`stale_release_branches`**.

---

## 3. Impact / scope

- Trust: operator asked why agent recommends **ignoring defective data** instead of fixing it.
- Risk: automated agent closeout **deletes valid release branches** if it follows skill literally on overloaded JSON.
- Scope: hub resume JSON, release skill, assert landmine.

---

## 4. Timeline (brief)

| Time | Event |
| ---- | ----- |
| 26-09-24 | RCA defines **`stale_release_branches`** = missing record on merge |
| 26-09-25 | Resume patch adds shipped lines to **same** array to escape `tag_ready` trap |
| 26-09-25 | Agent tells operator to delete `release/v0.2.0`; operator rejects |
| 26-09-25 | This RCA + **`closed_release_branches`** field |

---

## 5. The one thing

> What **one** deterministic, actionable thing, if it were different, would have **prevented this error condition from arising**?

**Answer (one sentence):** **`detect()` must emit shipped/completed release lines in `closed_release_branches` only, leaving `stale_release_branches` exclusively for merged lines missing `hub-release-record.json`, so agents and skills never treat a completed release branch as delete-stale.**

---

## 6. Prevention test

> If **`closed_release_branches` separate from `stale_release_branches` in resume JSON** had been in place **before** the failure, **the agent recommending deletion of `release/v0.2.0` as “stale” after v0.2.0 shipped** could not have occurred because **the skill delete loop binds only to `stale_release_branches`, and completed v0.2.0 would not appear there.**

**Completed:** yes (mechanism: disjoint arrays; landmine rejects overlap).

---

## 7. Contributing factors (optional)

- Agent **symptom counseling** (“just ignore the name”) when SSOT skill still said **delete stale**.
- M-block closeout notes mentioned deleting stale `release/v0.2.0` without distinguishing **closed** vs **stale**.
- No JSON field previously expressed “shipped, skip orchestration, keep branch.”

---

## 8. Preventive action (single tracked item)

| Field | Value |
| ----- | ----- |
| Action | Add **`closed_release_branches`**; stop appending shipped lines to **`stale_release_branches`**; update release skill + assert landmine |
| Owner | hub |
| Path / artifact | `tools/nlc_release_resume.py`, `.agents/skills/release/SKILL.md`, `tools/nouns/assert_release_resume_invariant_passes/` |
| Verification | `python3 tools/nlc_release_resume.py --emit json` → `release/v0.2.0` in **`closed_release_branches` only**; `python3 tools/assert-release-resume-invariant-passes.py` → MET |
| Human acceptance | `pending` |
| Implementation route | Done in RCA session (26-09-25) |

---

## 9. Follow-up (detection only if prevention insufficient)

- Document **`closed_release_branches`** in `docs/adoption/RELEASE.md` appendix if operators read resume JSON directly.
