# RCA: Tag leg NOT_MET — installed 0.0.0 not in published catalog

**Date:** 2026-09-25  
**Context:** Natural-Language-Coding hub — `./release` tag leg after PR #54 merge  
**Status:** prevented (fix on `main` @ `023bad1`)

---

## 1. Error condition

**Evidence (observed):**

- Command: `./release --bump keep` (tag leg after merge wait).
- Merge commit to tag: **`ce7b3a6c1fd5`** (PR #54 `release/v0.2.0` → `main`).
- Exit / signal: **`RELEASE_TAG_GATE:NOT_MET`**
- Log excerpt:
  ```text
  Step 1/3 — release tag gate (record, notes, migrations, verify-deep)
  RELEASE_TAG_GATE:NOT_MET
    Commit: ce7b3a6c1fd5  Tag: v0.2.0
    - installed 0.0.0 not in published catalog
  ```
- Shell cwd branch reported: **`release/v0.2.0`** (up to date with `origin/release/v0.2.0`).
- Reproduction (pre-fix): on `release/v0.2.0` @ `e313a8a`, `python3 tools/nlc_release_tag_gate.py --check --commit ce7b3a6 --tag v0.2.0 --skip-verify-deep` → same **0.0.0** migration error.
- Reproduction (post-fix): on `main` @ `023bad1`, same command → **`RELEASE_TAG_GATE:MET`**.

**Inferred:**

- PR was already merged; orchestrator still printed “Open a PR” / `gh pr create` (stale prepare messaging) before tag leg — confusing but not the gate failure.

**Mechanism confirmed on reproduction:** yes — compare `last_shipped_version(ce7b3a6)` → `None` ( **`v0.1.0` not ancestor of `main`** ) → code used **`0.0.0`** → `migration_steps_blockers(..., "0.0.0", "0.2.0")` raises catalog error.

---

## 2. Upstream chain (process before output)

| Step | Artifact / layer | What it did |
| ---- | ---------------- | ----------- |
| (symptom) | `./release` tag leg | Refused to create/push **`v0.2.0`** |
| `nlc_release_tag_gate.py` | `check_static` | `shipped = last_shipped_version(commit) or "0.0.0"` |
| `nlc_release_tags.py` | `last_shipped_tag` | No **`v*`** tag is ancestor of merge commit on rewritten **`main`** |
| `release_target_preflight.py` | (same ship session, earlier) | Already had **`resolve_shipped_baseline`** fallback on `main` @ `34b72e6` — **not shared** with tag gate |
| Operator | Branch choice | Ran tag leg from **`release/v0.2.0`** tree **without** tag-gate fix (fix landed on **`main`** only in `023bad1`) |

**Furthest controllable upstream point:** **Single shipped-baseline resolver** used by **both** target preflight and tag gate (ADR 0014), not `0.0.0` when git ancestry is empty.

---

## 3. Impact / scope

- **0.2.0** tag not pushed; GitHub Release workflow not triggered.
- Operator confusion: merged PR + “open a PR” text + failure on **`release/v0.2.0`** checkout.

---

## 4. Timeline (brief)

| Time | Event |
| ---- | ----- |
| 26-09-25 | PR #54 merged → `ce7b3a6` on `main` with record + notes |
| 26-09-25 | `./release` tag leg NOT_MET (`0.0.0` catalog) |
| 26-09-25 | Fix: `resolve_shipped_version` in tag gate on `main` `023bad1` |

---

## 5. The one thing

> What **one** deterministic, actionable thing, if it were different, would have **prevented this error condition from arising**?

**Answer (one sentence):** **`nlc_release_tag_gate.py` must resolve shipped semver via `resolve_shipped_version()` (same SSOT as release target preflight), never `last_shipped_version() or "0.0.0"`.**

---

## 6. Prevention test

> If **`check_static` used `resolve_shipped_version(commit)` (fallback to highest semver tag name, e.g. 0.1.0)** had been in place **before** the tag leg, **`installed 0.0.0 not in published catalog`** could not have occurred on **`ce7b3a6`**, because **migration steps would run from 0.1.0 → 0.2.0** with existing `migrations/` units.

**Completed:** Verified on `main` @ `023bad1` — tag gate **MET** on `ce7b3a6`.

---

## 7. Contributing factors (optional)

- Orphan **`v0.1.0`** tag off current `main` history (documented in FINDINGS).
- Tag leg run from **`release/v0.2.0`** branch carrying pre-fix tooling.
- `./release` UX still surfaces prepare-era PR instructions after merge.

---

## 8. Preventive action (single tracked item)

| Field | Value |
| ----- | ----- |
| Action | Share `resolve_shipped_baseline` / `resolve_shipped_version` in `release_tags`; tag gate uses it (no `0.0.0` default) |
| Owner | Hub maintainers |
| Path / artifact | `tools/nouns/release_tags/release_tags.py`, `tools/nlc_release_tag_gate.py` |
| Verification | `python3 tools/nlc_release_tag_gate.py --check --commit ce7b3a6 --tag v0.2.0 --skip-verify-deep` → MET on `main` |
| Human acceptance | `accepted` (landed `023bad1`) |
| Implementation route | Planit remediate 26-09-25 |

---

## 9. Follow-up (detection only if prevention insufficient)

- Resume tag leg from **`main`** at `023bad1+` (not stale `release/v0.2.0` tooling): `./release --bump keep`.
- Optional: `./release` tag leg refuses when `HEAD` branch ≠ `main` and tag gate script differs from merge commit’s tree.
