# RCA: `./release` pushed `release/v0.3.0` then waited and offered to move tag `v0.2.0`

**Date:** 2026-09-25  
**Context:** Natural-Language-Coding hub — single-session `./release` after pushing `release/v0.3.0`  
**Status:** mitigated

---

## 1. Error condition

**Evidence (observed):**

- Command: `./release` on `release/v0.3.0`.
- Push succeeded:

  ```text
  RELEASE:BRANCH_PUSHED release/v0.3.0 @ 0ca1bceb0ae434543e10a55b520e5afa15a64944
  ```

- The same session then:

  ```text
  Waiting for merged PR: release/v0.2.0 → main
  Merge commit to tag: ce7b3a6c1fd5
  Version from commit: 0.2.0  Tag: v0.2.0
  Tag v0.2.0 exists at 023bad16c1ff (not merge commit).
  Move tag v0.2.0 to merge commit ce7b3a6c1fd5?
  ```

- Commit `0ca1bce` (message `Release v0.3.0`) contains `integrity/nlc-version.json` **`0.2.0`**.
- Repro of the handoff (file still `0.2.0`):

  ```bash
  python3 tools/nlc_release_bump.py --matches-branch release/v0.3.0
  # RELEASE_VERSION:NOT_MET release/v0.3.0 file=0.2.0 expected=0.3.0
  ```

**Inferred:**

- Answering yes would move the already-shipped `v0.2.0` tag onto the old v0.2.0 merge `ce7b3a6`.

**Mechanism confirmed on reproduction:** yes — `cmd_single` after push set `TARGET` from `nlc_release_bump.py --current` (`0.2.0`) and `RELEASE_BRANCH=release/v0.2.0`. `resolve_merged_commit_sha` then found the already-merged v0.2.0 PR. Tag leg read version `0.2.0` at `ce7b3a6`.

---

## 2. Upstream chain (process before output)

| Step | Artifact / layer | What it did |
| ---- | ---------------- | ----------- |
| (symptom) | Wait + tag prompt | `release/v0.2.0` and tag `v0.2.0` after a v0.3.0 push |
| 4 | `cmd_single` | Replaced `RELEASE_BRANCH` from `--current` after the push |
| 3 | Step 6 `bump=keep` | Printed "Keeping 0.3.0" and did not write the file |
| 2 | `release_infer` on `release/v0.3.0` | `bump=keep` because the branch name is the target, while the file was still `0.2.0` |
| 1 | `apply_bump(..., keep=True)` | Returns the file version unchanged |

**Furthest controllable upstream point:** **`cmd_single` must keep the release branch it pushed, and that commit's `integrity/nlc-version.json` must equal that branch version before wait or tag.**

---

## 3. Impact / scope

- One session mixed an in-flight **v0.3.0** push with the already-shipped **v0.2.0** tag move prompt.
- Accepting the prompt would retag `v0.2.0` onto `ce7b3a6`.

---

## 4. Timeline (brief)

| Time | Event |
| ---- | ----- |
| 26-09-25 | Infer `bump=keep` on `release/v0.3.0` while file is `0.2.0` |
| 26-09-25 | Commit `0ca1bce` pushed as `release/v0.3.0` with version file `0.2.0` |
| 26-09-25 | Same `./release` waited on `release/v0.2.0` and prompted to move `v0.2.0` |
| 26-09-25 | RCA + refuse mismatched wait/tag; align file to release-line version on prepare |

---

## 5. The one thing

> What **one** deterministic, actionable thing, if it were different, would have **prevented this error condition from arising**?

**Answer:** **After pushing a `release/vX.Y.Z` branch, `./release` must wait and tag that same branch, and must refuse unless `integrity/nlc-version.json` on that commit is `X.Y.Z` — it must not recompute the branch from a stale version file.**

---

## 6. Prevention test

> If **`cmd_single` kept the pushed `RELEASE_BRANCH` and refused when the commit version differed** before the failure, **waiting for `release/v0.2.0` and prompting to move tag `v0.2.0` after pushing `release/v0.3.0`** could not have occurred because **the wait argument would stay `release/v0.3.0` and the `0.2.0` file on `0ca1bce` would stop the session before `resolve_merged_commit_sha` for `release/v0.2.0`.**

**Completed:** yes — `python3 tools/nlc_release_bump.py --matches-branch release/v0.3.0` exits 1 on this commit; `assert-release-infer-passes` rejects pairing `release/v0.3.0` with file `0.2.0`.

---

## 7. Contributing factors (optional)

- Infer `bump=keep` on an existing release line does not mean "leave the shipped version in the file." Step 6 now aligns the file to the release-line version before commit. Commit `0ca1bce` was already pushed without that alignment.
- `resolve_merged_commit_sha` correctly finds a merged PR for the branch name it is given. The wrong name was `release/v0.2.0`.

---

## 8. Preventive action (single tracked item)

| Field | Value |
| ----- | ----- |
| Action | Wait/tag use the pushed `release/v*` branch; refuse when `integrity/nlc-version.json` on that commit disagrees; prepare aligns the file to the release-line version before commit |
| Owner | TBD (hub maintainers) |
| Path / artifact | `scripts/nlc-release.sh`, `tools/nouns/release_bump/release_bump.py` |
| Verification | `python3 tools/nlc_release_bump.py --matches-branch release/v0.3.0` (expect NOT_MET on `0ca1bce`); `python3 tools/assert-release-infer-passes.py` |
| Human acceptance | `pending` |
| Implementation route | **`/planit`** after acceptance — cite this RCA path in the plan |

---

## 9. Follow-up (detection only if prevention insufficient)

- Do not answer yes to `Move tag v0.2.0`.
- `origin/release/v0.3.0` at `0ca1bce` still has version `0.2.0`. The next `./release` must refuse resume until a new commit on `release/v0.3.0` sets `integrity/nlc-version.json` to `0.3.0` and is pushed. Do not merge `0ca1bce` as the ship commit.
