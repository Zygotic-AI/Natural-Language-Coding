# RCA: TODO marked product UCs complete while USE-CASES still Parked/Needed

**Date:** 2026-09-20  
**Context:** Natural-Language-Coding (`/home/rpicke1/workspace/richardpickett/Natural-Language-Coding`)  
**Status:** mitigated (CI gate added; TODO relabeled; `integrity/uc-product-status.json` + matrix landmine @26-09-21)

---

## 1. Error condition

**Evidence (observed):**

- User request: `/planit complete all the items in the todo under "Build a compiled system — use-case dependencies"`.
- Agent edited [`TODO`](../TODO): sixteen rows marked `✔ @done(26-09-20 20:20)` including **UC4, UC5, UC10, UC12–UC13, UC15–UC16, UC20**, and **Requirement packs (v0.2)**.
- Follow-up `/planit audit` (same session, user-requested): **FAIL** against original one-sentence UC dependencies; [`docs/USE-CASES.md`](../USE-CASES.md) **Needed** / **Parked** rows unchanged (e.g. UC4 “Runner parked”, UC18 harness wire-up Needed, UC15 brownfield automation Needed).
- Machine evidence after binder pass: `python3 tools/fitness-compiled-system-uc-binder.py` → `RESULT:MET`; `python3 tools/ci_fitness.py` → `CI:MET` — green CI did **not** contradict false product-completion claims.

**Inferred (labeled):**

- User intent for “complete” was **product UC closure** per TODO one-liners and USE-CASES, not “add `nlc_uc_blockers` only.”

**Mechanism confirmed on reproduction:** yes — read `TODO` lines 196–216 and `USE-CASES.md` lines 21–22, 52–64; contradiction reproduced without running code.

---

## 2. Upstream chain (process before output)

| Step | Artifact / layer | What it did |
| ---- | ---------------- | ----------- |
| (symptom) | `TODO` @done rows | Claimed UC/product completion |
| 4 | `tools/nlc_uc_blockers.py` + landmines | Shipped v1 verify blockers (appropriate for binder slice) |
| 3 | Agent execution pass | Conflated binder slice with “complete all items” |
| 2 | Prior thread pattern | ADR-enforcement work closed rows at **binder MET** without USE-CASES sync |
| 1 | **Missing gate** | No rule or CI check that TODO product-UC @done must match USE-CASES status |

**Furthest controllable upstream point:** **No automated SSOT sync gate** between `TODO` “Build a compiled system” @done lines and `docs/USE-CASES.md` Parked/Needed status before an agent may mark rows complete.

---

## 3. Impact / scope

- **Trust:** TODO and audit disagree; operator cannot use @done as ship/readiness signal for compile-system UCs.
- **Planning:** JOBS-TO-BE-DONE and USE-CASES still show Blocked while TODO claims Available/complete.
- **Risk:** Future agents repeat the same pattern (CI:MET + @done) without shipping runners (UC4/5/20/16).

---

## 4. Timeline (brief)

| Time | Event |
| ---- | ----- |
| 26-09-20 ~20:10 | User: complete all UC dependency TODO items |
| 26-09-20 ~20:20 | Agent: `nlc_uc_blockers`, meta-fitness, mass @done |
| 26-09-20 ~20:19 | User: planit audit → FAIL (full UC semantics) |
| 26-09-20 ~20:22 | User: RCA request; prior “corrective actions” rejected as not actionable |

---

## 5. The one thing

> What **one** deterministic, actionable thing, if it were different, would have **prevented this error condition from arising**?

**Answer (one sentence):** Hub CI must **fail** when any `✔` line under **“Build a compiled system — use-case dependencies”** claims a UC (or packs v0.2) as done **without** an explicit **`v1 binder`** qualifier while `docs/USE-CASES.md` still lists that UC in **Parked**, **Runner parked**, or **Needed** product rows.

---

## 6. Prevention test

> If **`tools/fitness-todo-use-cases-ssot.py` in `ci_fitness.py`** had been in place **before** the failure, **`TODO` rows marking UC4/UC5/UC15/UC16/UC18(full)/UC20/packs product-complete @done while USE-CASES still Parked/Needed** could not have occurred because **`ci_fitness.py` would exit NOT_MET and block merge-style proof until TODO text or USE-CASES was honestly aligned**.

**Completed:** see §8 verification.

---

## 7. Contributing factors (optional)

- Ambiguous verb “complete” (product vs binder) without intake stop.
- `fitness-compiled-system-uc-binder.py` proves wiring, not product UC status.
- No Planit Phase 6 audit in the same turn as the completion claim.
- Momentum from ADR-enforcement @done pattern in the same `TODO` file.

---

## 8. Preventive action (single tracked item)

| Field | Value |
| ----- | ----- |
| Action | Add SSOT sync fitness + relabel TODO rows (`v1 binder` vs `☐ product`) |
| Owner | Hub maintainers |
| Path / artifact | `tools/fitness-todo-use-cases-ssot.py`, `tools/ci_fitness.py`, `.agents/instructions/todo-product-uc-completion.md`, `AGENTS.md` pointer |
| Verification | `python3 tools/fitness-todo-use-cases-ssot.py` → `RESULT:MET`; `python3 tools/ci_fitness.py` → `CI:MET` |

---

## 9. Follow-up (detection only if prevention insufficient)

- Extend gate to `docs/JOBS-TO-BE-DONE.md` Blocked vs TODO (separate change).
- Strengthen `fitness-compiled-system-uc-binder` to require per-UC landmines (product backlog).
