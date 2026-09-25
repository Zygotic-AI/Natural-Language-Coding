# RCA: Bare UC ids in replies force user lookup

**Date:** 2026-09-25  
**Context:** Natural-Language-Coding hub — agent `/release` and general chat  
**Status:** prevented

---

## 1. Error condition

**Evidence (observed):**

- Agent asked the user to confirm ship with **“UC14, UC16, UC20 expansion-only”** without stating what those use cases mean or ship impact.
- User had to leave the thread to look up ids (cognitive **motion**) before answering — classified as lean **motion** + handoff **defect** (incomplete information for a decision).

**Mechanism confirmed on reproduction:** yes — same pattern appears whenever skills say “list open UC rows” without mandating plain-language rows in the user-facing message.

---

## 2. Upstream chain (process before output)

| Step | Artifact | What it did |
| ---- | -------- | ----------- |
| (symptom) | Chat reply | Bare ids in a confirmation ask |
| 3 | `/release` Step 5 | “One-line impact + yes” — no **blocking** table for cited ids |
| 2 | `AGENTS.md` | No standing rule for decision handoffs |
| 1 | Agent default | Optimizes for SSOT precision (ids) over **information-complete** prompts |

**Furthest controllable upstream point:** **portable instruction SSOT** + **skill gate** on `/release` (and `AGENTS.md` for all harnesses).

---

## 3. Impact / scope

- Wasted user time on every ship/residual confirmation.
- Erodes trust (“do your job” / why am I the lookup layer?).
- Not a code bug — **process defect** in agent materials.

---

## 4. Timeline (brief)

| Time | Event |
| ---- | ----- |
| 26-09-24 | `/release` NO-GO + bare UC list for residuals |
| 26-09-25 | User names lean waste; RCA requested |

---

## 5. The one thing

> What **one** deterministic, actionable thing, if it were different, would have **prevented this error condition from arising**?

**Answer (scope corrected 26-09-25):** **`AGENTS.md` must require [`.agents/instructions/reply-references-plain-language.md`](../.agents/instructions/reply-references-plain-language.md) for every user-facing reply that cites internal ids — not only decision prompts — so each reference carries plain language in the same message.**

---

## 6. Prevention test

> If **`reply-references-plain-language.md` linked from AGENTS.md as an always-on standing rule`** had been in place **before** the failure, **citing UC14/16/20 without explanation in any reply** could not have occurred because **the harness instruction blocks bare id references until each id has a same-message plain-language gloss.**

**Completed:** yes.

---

## 7. Contributing factors (optional)

- SSOT culture favors ids for precision (appropriate in tools, not in human decision lines).
- No reuse of AWL “information completion” for **chat** handoffs.

---

## 8. Preventive action (single tracked item)

| Field | Value |
| ----- | ----- |
| Action | Add instruction + AGENTS pointer + `/release` gate row |
| Owner | hub |
| Path / artifact | `.agents/instructions/reply-references-plain-language.md`, `AGENTS.md`, `.agents/skills/release/SKILL.md` |
| Verification | Next `/release` with residuals includes table; no bare id-only confirmation |

---

## 9. Follow-up (optional)

- Optional: `tools/fitness-*` grep for skills that say “ask user to confirm” without linking decision-handoff (advisory only).
