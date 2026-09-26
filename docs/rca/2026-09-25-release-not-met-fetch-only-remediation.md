# RCA: `./release` NOT_MET remediation was only `git fetch` + re-run

**Date:** 2026-09-25  
**Context:** Natural-Language-Coding hub — `./release` on impure `main` (ADR 0044)  
**Status:** prevented

---

## 1. Error condition

**Evidence (observed):**

- Operator on **`main`**: `main(+396/-195)+*` locally; **`main` HEAD** `023bad16c1ff` ≠ tag **`v0.2.0`** commit `d853c4af277b`.
- `./release` → **`RELEASE:NOT_MET`** — main not production-trunk pure (expected).
- **Fix** block (before change):

  ```text
  1. git fetch origin main --tags
  2. cd …/Natural-Language-Coding && ./release
  ```

- Operator ran step **1** (`git fetch origin main --tags`); **`./release`** unchanged — same NOT_MET (19:21 session).
- Gaps correctly described trunk impurity and “next ship 0.3.0”, but **Fix** did not move work off **`main`** or reset **`main`** to tag.

**Mechanism confirmed on reproduction:** yes — `release_fail()` in `scripts/nlc-release.sh` always passed **`git fetch`** and **`./release`** as the only fix lines; infer main-purity block did not override them.

---

## 2. Upstream chain (process before output)

| Step | Artifact / layer | What it did |
| ---- | ---------------- | ----------- |
| (symptom) | NOT_MET Fix list | **Fetch + re-run** (no-op for purity) |
| 3 | `release_fail()` | Universal default fixes for every failure class |
| 2 | `apply_release_infer` | Called `release_fail` without `--` custom fixes |
| 1 | ADR 0044 | Impure **main** requires move-work + **local** reset to tag (or run from work branch) |

**Furthest controllable upstream point:** **`main_purity_remediation()` wired into infer production-trunk block** + **`release_fail` accepts explicit fix lines after `--`**.

---

## 3. Impact / scope

- Operator loop: follow Fix, no progress, distrust remediation (ADR 0018 / 0040).
- **`git fetch`** cannot make **`main` HEAD** equal tag commit when **`main`** is ahead locally/remotely.

---

## 4. Timeline (brief)

| Time | Event |
| ---- | ----- |
| 26-09-25 19:17 | `./release` NOT_MET on impure main |
| 26-09-25 19:21 | `git fetch` + `./release` — same NOT_MET |
| 26-09-25 | RCA + main-purity remediation lines |

---

## 5. The one thing

> What **one** deterministic, actionable thing, if it were different, would have **prevented this error condition from arising**?

**Answer:** **When infer blocks on production-trunk purity, `./release` must emit `main_purity_remediation()` fix lines (branch work off `main`, reset local `main` to last shipped tag, `./release` from work branch) instead of only `git fetch` + `./release`.**

---

## 6. Prevention test

> If **`main_purity_remediation()` had been bound to the production-trunk infer block** before the operator ran fetch, **“follow Fix then re-run ./release with no change”** could not have occurred because **step 1 would include `git branch … HEAD` and `git reset --hard v*^{commit}` on `main`, which changes the preconditions fetch alone cannot change.**

**Completed:** yes — `./release` on impure main now prints six-step fix including branch + reset.

---

## 7. Contributing factors (optional)

- Generic **`release_fail`** default suited resume/network gaps, not ADR 0044 trunk shape.
- Gap text mentioned “branch from tag baseline” but **Fix** did not mirror it.

---

## 8. Preventive action (single tracked item)

| Field | Value |
| ----- | ----- |
| Action | `main_purity_remediation()`; `release_fail` `--` overrides; infer trunk block uses `--print-main-purity-fixes` |
| Owner | hub |
| Path / artifact | `tools/nouns/release_remediate/`, `scripts/nlc-release.sh`, `tools/nlc_release_remediate.py` |
| Verification | `./release` on impure main → Fix includes `git reset --hard` + work branch; not fetch-only |
| Human acceptance | `pending` |
| Implementation route | RCA session (26-09-25) |

---

## 9. Follow-up (detection only if prevention insufficient)

- Landmine: assert fix list from `--print-main-purity-fixes` contains `reset --hard`.
