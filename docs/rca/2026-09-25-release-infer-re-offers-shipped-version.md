# RCA: `./release` infer re-offered shipped v0.2.0 on impure main

**Date:** 2026-09-25  
**Context:** Natural-Language-Coding hub — zero-parameter `./release --dry-run` from `main`  
**Status:** prevented

---

## 1. Error condition

**Evidence (observed):**

- Command: `./release --dry-run` on branch **`main`** (`023bad16c1ff`), remote tag **`v0.2.0`** @ **`d853c4af`** (already shipped).
- Resume: **`prepare`**; `closed_release_branches`: **`release/v0.2.0`**.
- Infer banner:

  ```text
  RELEASE:INFER target=0.2.0 branch=release/v0.2.0 bump=keep (resume or branch state)
  ```

- Operator report: infer **still shows a release that has already been done** (v0.2.0).
- Repro:

  ```bash
  python3 tools/nlc_release_infer.py --emit json
  # target_version: "0.2.0", block: true, block_problem: main purity NOT_MET
  ```

**Inferred:**

- Banner read as “start release 0.2.0 again” though tag **`v0.2.0`** already exists.

**Mechanism confirmed on reproduction:** yes — `infer_release()` on **`main`** used **`integrity/nlc-version.json`** (`0.2.0`) as **`target_version`** for blocked paths instead of **next semver after `last_shipped_version`**.

---

## 2. Upstream chain (process before output)

| Step | Artifact / layer | What it did |
| ---- | ---------------- | ----------- |
| (symptom) | `RELEASE:INFER` banner | **target=0.2.0** while tag shipped |
| 3 | `release_infer.py` | Main-block branch set `target_version=read_version()` |
| 2 | Zero-param infer plan | Main block documented; no rule “never re-offer shipped version” |
| 1 | `integrity/nlc-version.json` | Still **0.2.0** on impure **main** (declared, not next ship) |

**Furthest controllable upstream point:** **`plan_next_release_target()` in `release_infer.py`** — all prepare-phase banners use **next** semver after shipped tag.

---

## 3. Impact / scope

- Operator distrust of zero-param infer (“already done”).
- Correct **`RELEASE:NOT_MET`** on impure main masked by misleading banner.

---

## 4. Timeline (brief)

| Time | Event |
| ---- | ----- |
| 26-09-25 | `./release --dry-run` → INFER **0.2.0** on impure main |
| 26-09-25 | RCA + `plan_next_release_target` + landmine |

---

## 5. The one thing

> What **one** deterministic, actionable thing, if it were different, would have **prevented this error condition from arising**?

**Answer:** **`nlc_release_infer.py` must compute prepare-phase `target_version` with `plan_next_release_target(last_shipped, json)` so `RELEASE:INFER` never names an already-shipped semver when a shipped tag exists.**

---

## 6. Prevention test

> If **`plan_next_release_target()` had been used for main-block (and work-branch) prepare infer** before the failure, **`RELEASE:INFER target=0.2.0` while `v0.2.0` tag exists** could not have occurred because **target would be strictly greater than `last_shipped_version` (e.g. 0.3.0 minor from tree).**

**Completed:** yes — verified on repo: infer JSON `target_version` > `0.2.0` with `block: true` on impure main.

---

## 7. Contributing factors (optional)

- Default infer-line fallback **“resume or branch state”** when `reasons` empty.
- **`integrity/nlc-version.json`** on **main** still at shipped version during forward work.

---

## 8. Preventive action (single tracked item)

| Field | Value |
| ----- | ----- |
| Action | `plan_next_release_target()`; main-block infer uses next semver; extend `assert-release-infer-passes.py` |
| Owner | hub |
| Path / artifact | `tools/nouns/release_infer/release_infer.py`, `tools/nouns/assert_release_infer_passes/` |
| Verification | `python3 tools/assert-release-infer-passes.py`; `python3 tools/nlc_release_infer.py --emit json` on impure main → `target_version` > shipped |
| Human acceptance | `pending` |
| Implementation route | RCA session (26-09-25) |

---

## 9. Follow-up (detection only if prevention insufficient)

- Optional: suppress `RELEASE:INFER` entirely when `INFER_BLOCK=1` (banner vs stderr only) — not required if target is always “next ship.”
