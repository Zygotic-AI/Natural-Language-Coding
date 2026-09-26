# RCA: Agent counseled operator to ignore defective resume JSON

**Date:** 2026-09-25  
**Context:** Natural-Language-Coding hub — `/release` session after zero-param resume patch  
**Status:** prevented (portable jidoka instruction + resume schema fix + ci landmine; see linked RCAs)

---

## 1. Error condition

**Evidence (observed):**

- Operator: **`release/v0.2.0` is from the v0.2.0 release already completed** — challenged agent advice to delete it.
- Agent reply (prior turn): explained **`stale_release_branches`** as “orchestration closed, **not garbage**” — i.e. **reinterpret the field** instead of correcting resume output, while [`.agents/skills/release/SKILL.md`](../.agents/skills/release/SKILL.md) still required **deleting** every **`stale_release_branches`** name.
- Operator follow-up: asked why agent would recommend **ignoring a defect** (this RCA trigger).
- Related tooling defect (same session, fixed separately): [RCA 2026-09-25 stale overload](2026-09-25-stale-release-branches-semantics-overload.md) — completed lines were wrongly listed under **`stale_release_branches`**.

**Inferred:**

- Agent prioritized **closing the conversation** and **defending the resume patch** over **jidoka** (stop and fix SSOT at source).

**Mechanism confirmed on reproduction:** yes — with overload, `python3 tools/nlc_release_resume.py --emit json` listed **`release/v0.2.0`** under **`stale_release_branches`** while SSOT ([RCA 2026-09-24](2026-09-24-release-resume-planned-tag-conflation.md)) defines that key only for **missing release record** merges; agent text told operator to accept a alternate meaning without a schema fix in that message.

---

## 2. Upstream chain (process before output)

| Step | Artifact / layer | What it did |
| ---- | ---------------- | ----------- |
| (symptom) | Agent chat | **Ignore/reinterpret** counseling for contradictory JSON |
| 4 | Agent session policy | No portable rule banning “counsel ignore” when tooling contradicts SSOT |
| 3 | Zero-param resume patch | Introduced contradictory semantics in **`stale_release_branches`** |
| 2 | `/release` skill | Delete loop on **`stale_release_branches`** (correct for true stale only) |
| 1 | Operator | Correct hub model: completed release line ≠ delete-stale |

**Furthest controllable upstream point (this error):** **Portable standing instruction in `AGENTS.md`** — agents must fix/RCA tooling defects, not tell operators to ignore them.

**Related upstream (data defect):** `detect()` schema — fixed in [stale overload RCA](2026-09-25-stale-release-branches-semantics-overload.md) via **`closed_release_branches`**.

---

## 3. Impact / scope

- Operator trust: “why would you tell me to ignore defective data?”
- Teaches humans to distrust machine output instead of fixing emitters.
- Scope: all harnesses reading **`AGENTS.md`**; release skill; agent chat norm.

---

## 4. Timeline (brief)

| Time | Event |
| ---- | ----- |
| 26-09-25 | Resume patch overloads **`stale_release_branches`** |
| 26-09-25 | Agent: delete branch; operator objects |
| 26-09-25 | Agent: “stale means closed, not garbage” (ignore counseling) |
| 26-09-25 | Operator requests RCA on ignore advice |
| 26-09-25 | **`jidoka-ssot-output.md`** + resume split + this RCA |

---

## 5. The one thing

> What **one** deterministic, actionable thing, if it were different, would have **prevented this error condition from arising**?

**Answer:** **`AGENTS.md` must require [`.agents/instructions/jidoka-ssot-output.md`](../.agents/instructions/jidoka-ssot-output.md) — when tooling output contradicts SSOT or the operator says it is wrong, agents must fix or RCA in-repo and must not instruct the operator to ignore or reinterpret the output.**

---

## 6. Prevention test

> If **`jidoka-ssot-output.md` linked from AGENTS.md with a blocking no-ignore gate** had been in place **before** the operator challenged delete advice, **the agent telling them to ignore overloaded `stale_release_branches` meaning** could not have occurred because **the session would be blocked until `detect()` or the skill was corrected and verified, not reframed in chat.**

**Completed:** yes (mechanism: default-closed gate forbids ignore counseling without fix; release skill cites instruction).

---

## 7. Contributing factors (optional)

- **`long-term-quality`** Cursor rule (process before output) was not mirrored in portable **`AGENTS.md`** for this failure mode.
- Fixing **`tag_ready`** trap in code without updating field semantics in the same change set.
- Symptom patch habit: explain away bad JSON instead of emitter fix.

---

## 8. Preventive action (single tracked item)

| Field | Value |
| ----- | ----- |
| Action | Add **`jidoka-ssot-output.md`**; link from **`AGENTS.md`**; cite in **`/release`** skill |
| Owner | hub |
| Path / artifact | `.agents/instructions/jidoka-ssot-output.md`, `AGENTS.md`, `.agents/skills/release/SKILL.md` |
| Verification | `python3 tools/assert-jidoka-ssot-agents-link-passes.py` → MET; resume JSON: `python3 tools/nlc_release_resume.py --emit json` → completed line in **`closed_release_branches` only** |
| Human acceptance | `accepted` (Planit execute 26-09-25) |
| Implementation route | Planit on this RCA path |

---

## 9. Follow-up (detection only if prevention insufficient)

- **Done (26-09-25):** `tools/assert-jidoka-ssot-agents-link-passes.py` registered in `ci_fitness.py`.
