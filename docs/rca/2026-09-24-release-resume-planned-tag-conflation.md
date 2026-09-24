# RCA: Agent conflated resume `tag` with existing git tag (v0.2.0)

**Date:** 2026-09-24  
**Context:** Natural-Language-Coding hub — `/release` skill session  
**Status:** prevented (resume JSON + `/release` skill Step 0 + stale-branch skip in `detect()`)

---

## 1. Error condition

**Evidence (observed):**

- User: `git tag` → only **`v0.1.0`**; no **`v0.2.0`**.
- Agent `/release` summary treated **`v0.2.0`** as an existing or in-flight **git tag** (“tag v0.2.0”, “tag_ready for v0.2.0”) and tied ship narrative to that ref.
- Resume probe output (reproduced):

  ```bash
  python3 tools/nlc_release_resume.py --emit json
  # {"phase": "tag_ready", "tag": "v0.2.0", "release_branch": "release/v0.2.0", ...}
  ```

- `integrity/nlc-version.json` on `main`: `"version": "0.2.0"` (declared version, not a tag).
- Branch **`release/v0.2.0`** exists locally and on `origin`; tip equals `main` @ `5eedc34` (ordinary PR merge, not a completed prepare leg).

**Inferred:**

- Agent merged three symbols: **semver in JSON**, **release branch name**, and **git tag**.

**Mechanism confirmed on reproduction:** yes — `git tag -l` shows only `v0.1.0`; resume JSON still emits `"tag": "v0.2.0"` while `phase` is `tag_ready` (which by code means `tag_on_commit` is **false**).

---

## 2. Upstream chain (process before output)

| Step | Artifact / layer | What it did |
| ---- | ---------------- | ----------- |
| (symptom) | Agent chat | Spoke as if **`v0.2.0` git tag** existed or was the current ship artifact |
| 4 | `/release` skill Step 0 | Ran resume JSON; echoed **`tag`** without mandatory **`git tag -l`** evidence or **planned vs existing** wording |
| 3 | `nlc_release_resume.py` | Emits key **`tag`** = derived from branch `release/v0.2.0` → **`v0.2.0`** for **all** non-`prepare` phases; **`tag_ready`** explicitly means tag is **not** on merge commit |
| 2 | `integrity/nlc-version.json` + TODO/FINDINGS | Document **target 0.2.0** and **`release/v*`** workflow — easy to read as “already tagged” |
| 1 | User expectation | Ship state = **`git tag`**, not branch names or JSON version |

**Furthest controllable upstream point:** **resume machine output + skill evidence rule** — before agent prose.

---

## 3. Impact / scope

- Operator distrust (“where are you getting this fucking v0.2.0 tag?”).
- Wrong mental model for `./release` (tag leg vs fresh prepare).
- Not a false `git tag` in the repo — **misread of tooling output**.

---

## 4. Timeline (brief)

| Time | Event |
| ---- | ----- |
| 26-09-24 | `/release` run; resume `tag_ready` + JSON `"tag": "v0.2.0"` |
| 26-09-24 | User corrects: local tags only `v0.1.0` |
| 26-09-24 | RCA + preventive resume field + skill Step 0 |

---

## 5. The one thing

> What **one** deterministic, actionable thing, if it were different, would have **prevented this error condition from arising**?

**Answer (one sentence):** **`nlc_release_resume.py` must emit an explicit boolean `git_tag_on_merge` (and `/release` must require `git tag -l` + “planned tag” wording when that boolean is false), so agents cannot treat the resume `tag` field as an existing git ref.**

---

## 6. Prevention test

> If **`git_tag_on_merge` in resume JSON plus `/release` Step 0 git tag evidence** had been in place **before** the failure, **the agent claiming an existing v0.2.0 git tag** could not have occurred because **user-facing copy would be blocked until `git tag -l` was cited and `git_tag_on_merge: false` forced “planned tag” language.**

**Completed:** yes (mechanism: `tag_ready` ⟺ `not tag_on_commit(...)` in `detect()`).

---

## 7. Contributing factors (optional)

- **`tag_ready` name** sounds like “tag exists and is ready” rather than “merge done, **git tag not yet applied**”.
- Stale **`release/v0.2.0`** at `main` tip without `hub-release-record.json` (false resume path — separate hardening candidate).
- FINDINGS/TODO prose “0.2.0 until `./release`” without always pairing “no `v0.2.0` tag yet”.

---

## 8. Preventive action (single tracked item)

| Field | Value |
| ----- | ----- |
| Action | Add `git_tag_on_merge` + `planned_tag` to resume JSON/shell; `/release` Step 0 requires `git tag -l` and planned-tag diction when false |
| Owner | hub |
| Path / artifact | `tools/nlc_release_resume.py`, `.agents/skills/release/SKILL.md` |
| Verification | `python3 tools/nlc_release_resume.py --emit json \| python3 -c "import sys,json; d=json.load(sys.stdin); assert d['git_tag_on_merge'] is False and d['planned_tag']=='v0.2.0'"` on current repo state; skill text requires tag list in Step 0 |

---

## 9. Follow-up (detection only if prevention insufficient)

- Optional: rename phase `tag_ready` → `merge_ready_tag_pending` in a breaking ADR (human surface + script strings).
- **Done (26-09-24):** `detect()` skips merged `release/v*` when merge commit lacks `hub-release-record.json`; emits `stale_release_branches`. Landmine: `tools/assert-release-resume-invariant-passes.py`.
