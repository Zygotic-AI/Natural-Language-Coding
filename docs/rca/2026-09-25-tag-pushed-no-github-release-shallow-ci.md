# RCA: Tag pushed — no GitHub Release (release workflow fitness landmine on shallow checkout)

**Date:** 2026-09-25  
**Context:** Natural-Language-Coding hub — `./release` tag leg + GitHub Actions `release` workflow  
**Status:** prevented (fix pending merge; `/planit` 2026-09-25)

---

## 1. Error condition

**Evidence (observed):**

- Operator signal: after `./release` tag leg, terminal reported **`RELEASE:TAG_PUSHED v0.2.0 @ ce7b3a6c1fd5`** and *“GitHub Actions will build the tarball and publish the Release.”*
- Product outcome: **`gh release list`** for `Zygotic-AI/Natural-Language-Coding` returns **no releases** (empty).
- CI: GitHub Actions workflow **`release`** on tag push **`v0.2.0`** → **`failure`** (~13s), run [36192457449](https://github.com/Zygotic-AI/Natural-Language-Coding/actions/runs/36192457449).
- Failed step: **Hub fitness suite** (`python3 tools/ci_fitness.py`).
- Log excerpt:
  ```text
  ASSERT:FAIL expected hub-release-record blocker
  CI:FAIL tools/assert-release-tag-gate-fails.py
  ##[error]Process completed with exit code 1.
  ```
- Same tag push triggered workflow **`fitness`** → **`success`** (full history checkout).
- Workflow diff (observed in repo):
  - `.github/workflows/fitness.yml` — `actions/checkout@v4` with **`fetch-depth: 0`**
  - `.github/workflows/release.yml` — `actions/checkout@v4` **without** `fetch-depth: 0` (default shallow)
- Reproduction (local, observed):
  ```bash
  git clone --depth 1 --branch v0.2.0 https://github.com/Zygotic-AI/Natural-Language-Coding /tmp/nlc-shallow-test
  cd /tmp/nlc-shallow-test
  python3 tools/nlc_release_tag_gate.py --check --commit 397b1a0 --tag v0.2.0 --skip-verify-deep
  # → RELEASE_TAG_GATE:NOT_MET — "no nlc-version.json at commit" (not hub-release-record)
  python3 tools/assert-release-tag-gate-fails.py
  # → ASSERT:FAIL expected hub-release-record blocker
  ```
- Binder gap (observed on workspace `main`):
  ```bash
  python3 tools/nouns/fitness_adr_0039_release_binder/fitness_adr_0039_release_binder.py
  # → RESULT:MET while release.yml still lacks fetch-depth: 0
  ```

**Inferred (label clearly):**

- `./release` does not wait for or verify the **`release`** workflow conclusion after tag push; success messaging is optimistic.

**Mechanism confirmed on reproduction:** yes — shallow tag checkout cannot `git show 397b1a0:…`; landmine `assert_release_tag_gate_fails.py` expects stderr/stdout to mention **`hub-release-record`**, but the tag gate returns a different NOT_MET path first.

---

## 2. Upstream chain (process before output)

| Step | Artifact / layer | What it did |
| ---- | ---------------- | ----------- |
| (symptom) | GitHub Releases UI | No release artifact despite pushed tag |
| `release.yml` job | Step “Publish GitHub Release” | **Never ran** — prior step failed |
| `release.yml` | “Hub fitness suite” | Ran `ci_fitness.py` including release landmines |
| `assert_release_tag_gate_fails.py` | Landmine ADR 0039 | Requires historic commit **`397b1a0`** reachable via git |
| `release.yml` checkout | `actions/checkout@v4` default depth | **Shallow** clone on tag push — **`397b1a0` not in object database** |
| `fitness.yml` checkout | `fetch-depth: 0` | Same landmines **pass** on PR/main pushes |
| `fitness_adr_0039_release_binder.py` | ADR 0039 binder | Enforces **`fetch-depth: 0` only on `fitness.yml`**, not on **`release.yml`** even though **`release.yml` also runs `ci_fitness.py`** |
| `./release` / docs | Tag leg complete | Declared tag pushed; implied publish would follow |

**Furthest controllable upstream point:** **Release binder (ADR 0039)** — parity rule for checkout depth on **every** workflow that runs the hub fitness suite, not only `fitness.yml`.

---

## 3. Impact / scope

- **v0.2.0** git tag exists on remote; **no** GitHub Release tarball or release notes page.
- Operator belief: ship completed (`RELEASE:TAG_PUSHED` + publish message) while publish pipeline failed.
- Class risk: any future workflow running `ci_fitness.py` / `ci-fitness.sh` without full history can pass PR **`fitness`** and still fail on tag **`release`**, or fail landmines with misleading assert text.

---

## 4. Timeline (brief)

| Time (UTC) | Event |
| ---------- | ----- |
| 2026-09-25 ~21:13 | PR #54 merged (`release/v0.2.0` → `main`) |
| 2026-09-25 ~21:36 | Tag **`v0.2.0`** pushed; **`release`** workflow **failed**; **`fitness`** on same tag **passed** |
| 2026-09-25 | Operator: “there’s no release” after successful local tag leg |

---

## 5. The one thing

> What **one** deterministic, actionable thing, if it were different, would have **prevented this error condition from arising**?

**Answer (one sentence):** **`fitness_adr_0039_release_binder` must require `actions/checkout` with `fetch-depth: 0` on `.github/workflows/release.yml` whenever that workflow runs the hub fitness suite (`tools/ci_fitness.py`), using the same rule already applied to `fitness.yml` for historic-commit landmines.**

---

## 6. Prevention test

> If **`the release binder enforced full-history checkout on release.yml before merge`** had been in place **before** the failure, **`tag v0.2.0 pushed with no GitHub Release because release workflow failed assert-release-tag-gate-fails on shallow clone`** could not have occurred because **PR/main fitness would NOT_MET on the binder violation until `release.yml` matched `fitness.yml`, blocking merge/tag with a fix visible before tag push.**

**Completed:** Mechanism verified via shallow clone reproduction and binder **MET** with **`release.yml` still shallow** (observed commands above).

---

## 7. Contributing factors (optional)

- `./release` does not poll `gh run watch` / release workflow success after tag push.
- Success copy implies publish is imminent without linking to the **`release`** workflow or requiring green status.
- Landmine assert message assumes full history; shallow checkout surfaces a **different** NOT_MET string (assert brittleness — secondary; full history is the intended contract).

---

## 8. Preventive action (single tracked item)

| Field | Value |
| ----- | ----- |
| Action | Extend **`tools/nouns/fitness_adr_0039_release_binder/fitness_adr_0039_release_binder.py`** to fail when **`release.yml` runs `ci_fitness.py`** (or `ci-fitness.sh`) without **`fetch-depth: 0`** on checkout; then add **`fetch-depth: 0`** to **`.github/workflows/release.yml`** as the minimal config fix the binder demands. |
| Owner | TBD (hub maintainer) |
| Path / artifact | `fitness_adr_0039_release_binder.py`, `.github/workflows/release.yml` |
| Verification | (1) With shallow `release.yml`, `python3 tools/nouns/fitness_adr_0039_release_binder/fitness_adr_0039_release_binder.py` → **`RESULT:NOT_MET`**. (2) After fix, binder → **`RESULT:MET`**. (3) Shallow-clone repro: `python3 tools/assert-release-tag-gate-fails.py` → **`ASSERT:PASS`**. (4) After tag push (or workflow_dispatch if added later), **`release`** workflow reaches **Publish GitHub Release** or documented re-run path. |
| Human acceptance | `accepted` (via `/planit` scope on this RCA path) |
| Implementation route | **`/planit`** after acceptance — cite this RCA path in the plan |

---

## 9. Follow-up (detection only if prevention insufficient)

- Optional: `./release` post-tag leg waits for **`release`** workflow success via `gh` (detection/closer loop — not substitute for binder parity).
