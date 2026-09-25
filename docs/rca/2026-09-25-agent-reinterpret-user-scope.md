# RCA: Agent narrowed user scope (references → “when asking you to decide”)

**Date:** 2026-09-25  
**Context:** Natural-Language-Coding hub — agent chat + RCA follow-up  
**Status:** prevented

---

## 1. Error condition

**Evidence (observed):**

- User: *“what the one thing … when it comes to **references in your replies**?”*
- Agent RCA/preventive fix scoped to **“when the agent asks you to decide”** and `decision-handoff-plain-language.md`.
- User correction: they did **not** limit to decisions; rule must apply to **every conversation**.

**Second beat:** User already has **Take me literally** in [`.cursor/rules/take-me-literally.mdc`](../../.cursor/rules/take-me-literally.mdc) (`alwaysApply: true`) — agent still narrowed scope.

**Mechanism:** Portable harnesses read **`AGENTS.md`**, not Cursor-only rules; RCA/planit intake had **no mandatory “Scope (user words)” row**, so reinterpretation shipped as SSOT.

---

## 2. Upstream chain

| Step | Artifact | What it did |
| ---- | -------- | ----------- |
| (symptom) | RCA + instruction | Wrong scope baked into repo |
| 3 | `/conduct-root-cause-analysis` | No gate to quote user scope verbatim before “the one thing” |
| 2 | `AGENTS.md` | Missing portable **take-me-literally** pointer |
| 1 | Agent default | Compress broad ask → familiar pattern (decision/handoff) |

**Furthest controllable upstream point:** **`AGENTS.md` + `.agents/instructions/take-me-literally.md`** with verbatim-scope gate on every plan/RCA/durable write.

---

## 3. Impact / scope

- Wrong preventive fix (decision-only) until user corrected.
- Wasted turn; erodes “take my words at face value.”
- Not sarcasm or unclear user text — **agent reinterpretation**.

---

## 4. Timeline (brief)

| Time | Event |
| ---- | ----- |
| 26-09-25 | Bare-id RCA scoped to decision prompts |
| 26-09-25 | User: scope is **references in replies**, always |
| 26-09-25 | This RCA + portable instruction |

---

## 5. The one thing

> What **one** deterministic, actionable thing, if it were different, would have **prevented this error condition from arising**?

**Answer:** **`AGENTS.md` must require [`.agents/instructions/take-me-literally.md`](../.agents/instructions/take-me-literally.md) with a blocking **Scope (user words)** row in intake/resolution tables before scope-shaping artifacts (RCA, skills, plans) — and one question + stop when ambiguous.**

---

## 6. Prevention test

> If **`take-me-literally.md` linked from AGENTS.md with verbatim-scope gate`** had been in place **before** the references RCA, **scoping the fix to “when asking you to decide”** could not have occurred because **the resolution table would have quoted “references in your replies” and the no-narrowing row would fail until scope matched.**

**Completed:** yes.

---

## 7. Contributing factors (optional)

- Duplicate policy: Cursor rule present but not in portable SSOT (`agents-portable-ssot` policy).
- RCA skill emphasizes “decision” / gates — easy to overfit.

---

## 8. Preventive action (single tracked item)

| Field | Value |
| ----- | ----- |
| Action | Add `.agents/instructions/take-me-literally.md` + AGENTS pointer |
| Owner | hub |
| Path / artifact | `.agents/instructions/take-me-literally.md`, `AGENTS.md` |
| Verification | Next RCA/planit intake shows **Scope (user words)** quoting the user before “the one thing” |

---

## 9. Follow-up (optional)

- Optional: add **Scope (user words)** to `/conduct-root-cause-analysis` skill ICC template (org-global skill in `~/.agents/skills/`).
