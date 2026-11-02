# RCA: `./release` push of `release/v0.4.1` rejected, then accepted

**Date:** 2026-10-31  
**Context:** Natural Language Compiler hub. `./release` on local `release/v0.4.1` at `adf223e`.  
**Status:** open (RCA only; no remediation in this record)

**Scope (manifest):** Analysis only. New file `docs/rca/2026-10-31-release-line-push-without-pr.md`. No tool, planner, or workflow change.

---

## 1. Error condition

**Observed.** `./release` selected a direct update of the release branch and GitHub rejected it.

```text
Planner: phase=CANDIDATE_READY_LOCAL action=PUSH_FAST_FORWARD kind=REPAIR
remote: - Changes must be made through a pull request.
remote: - Required status check "fitness" is expected.
 ! [remote rejected] release/v0.4.1 -> release/v0.4.1 (push declined due to repository rule violations)
RELEASE:NOT_MET phase=BLOCKED action=BLOCKED
Problem: Release repair PUSH_FAST_FORWARD failed.
Gap: BLOCKED_PUSH_FAST_FORWARD_FAILED
```

Ruleset evaluation `4828955661` (actor `richardpickett`, `refs/heads/release/v0.4.1`, `247dba5` → `adf223e`, `2026-10-30T23:16:40-05:00`):

| Rule | Result | Detail |
| --- | --- | --- |
| `pull_request` on ruleset `release-line-no-direct-push` (`25824126`) | fail | Changes must be made through a pull request. |
| `required_status_checks` on the same ruleset | fail | Required status check "fitness" is expected. |
| `non_fast_forward` on the same ruleset | pass | The update was a fast-forward. |

The executor that sent the push is `goals/hub_release/execute.sh`: for `PUSH_NEW` and `PUSH_FAST_FORWARD` it runs `git push -u origin <desired_branch>`. The desired branch was `release/v0.4.1`. The planner chooses `PUSH_FAST_FORWARD` when `remote_relation` is `ahead` (`tools/nouns/release_state/release_state.py`).

**Same push later.** Evaluation `4834872297` (`2026-10-31T13:33:35-05:00`) is the same actor, the same ref, and the same `247dba5` → `adf223e` range. All four rules passed, and `git push origin release/v0.4.1` exited 0. Between the two evaluations, pull request #46 existed with head `adf223e`, and the `fitness` check on that commit had completed successfully at `2026-10-31T04:22:25Z`.

---

## 2. Upstream chain

| Step | Producer | What it did |
| --- | --- | --- |
| Symptom | GitHub ruleset `25824126` | Rejected the first push of `adf223e` onto `release/v0.4.1` |
| 4 | `goals/hub_release/execute.sh` `PUSH_FAST_FORWARD` | Ran `git push` of `release/v0.4.1` with no pull request and no `fitness` result on that commit |
| 3 | `tools/nouns/release_state/release_state.py` | When the local release branch is ahead of the remote, the only action is `PUSH_FAST_FORWARD` |
| 2 | `docs/github-ruleset-release.md` | Says a producer session must not push `release/*`. The live rule is narrower: a fast-forward is allowed once those commits are already a pull-request head and `fitness` has passed |
| 1 | No contract between the planner and the ruleset | Nothing stops `./release` from publishing `release/*` as the first time those commits are seen |

**Furthest controllable point:** the planner action for "local release branch is ahead of origin". That action is a direct push. It does not first put the commits on a non-release branch and open a pull request.

---

## 3. Impact / scope

`./release` cannot land the first publication of release-line commits. Re-running `./release` without a pull request repeats the same rejection. After a pull request and a green `fitness` check exist for that exact commit, the same direct push is legal. This record does not cover the later push-event `fitness` failure on run `41230009783` (ADR 0039 binder). That run started after the second push and is a separate failure.

---

## 4. Timeline

| Time | Event |
| --- | --- |
| 2026-10-25T21:13:59-05:00 | Ruleset `25824126` last updated. Enforcement active. Bypass is only the start-release app (`actor_id` 5473379). `current_user_can_bypass` for `richardpickett` is `never`. |
| 2026-10-30T23:16:40-05:00 | `./release` push `247dba5` → `adf223e` failed. Suite `4828955661`. |
| After that failure | Branch `cursor/v041-diagram-onto-release-line` pushed. Pull request #46 opened into `release/v0.4.1`. |
| 2026-10-31T04:22:25Z | `fitness` on `adf223e` completed with conclusion `success` (pull-request checks). |
| 2026-10-31T13:33:35-05:00 | RCA reproduction ran `git push origin release/v0.4.1`. Suite `4834872297` passed. `origin/release/v0.4.1` is `adf223e`. GitHub records pull request #46 merged at `2026-10-31T18:33:37Z` because that head is now on the base. |
| 2026-10-31T18:33:38Z | Push-event workflow run `41230009783` started. Its `fitness` job failed. Not this error condition. |

---

## 5. Mechanism on reproduction

**Confirmed.** Two ruleset suites, one rejected push and one accepted push:

- Before any pull request contained `adf223e`, `pull_request` and `required_status_checks` failed.
- After pull request #46 and a successful `fitness` check on that same commit, both rules passed for the identical fast-forward.
- Immediately before the second push, `python3 tools/nlc_release_state.py` still printed `action: PUSH_FAST_FORWARD`.

The rejection is not "this user can never push `release/*`". The ruleset allows the fast-forward when the new commit is already on a pull request and `fitness` has already succeeded.

---

## 6. The one thing

`PUSH_FAST_FORWARD` in `goals/hub_release/execute.sh` must not run `git push` of a `release/*` branch until that commit is already the head of a pull request whose `fitness` check has succeeded. The planner must open that pull request from a branch that is not `release/*` before any release-branch push.

---

## 7. Prevention test

If that order had been in place before `2026-10-30T23:16:40-05:00`, the remote rejection could not have occurred. `git push` of `release/v0.4.1` would not have been sent until pull request #46 (or an equivalent) existed and `fitness` on `adf223e` had succeeded, which is the state in which suite `4834872297` passed the same rules.

**Completed:** yes. The two suites hold the before and after of that condition on one commit range.

---

## 8. Contributing factors

- `BLOCKED_PUSH_FAST_FORWARD_FAILED` tells the operator to inspect and re-run `./release`. Re-running repeats the same push.
- `docs/github-ruleset-release.md` says not to push `release/*` at all from a producer session. The live rule accepts the push after a pull request and a green `fitness` check. The doc is stricter than the rule that actually fired.
- The reproduction push in this RCA did update `origin/release/v0.4.1` to `adf223e`. That was not a remediation commit. It is the second suite above.
- Repository admin on `richardpickett` did not bypass the ruleset. `current_user_can_bypass` is `never`.

---

## 9. Preventive action

| Field | Value |
| --- | --- |
| Action | Change the ahead-of-remote release action so the first publication is a non-`release/*` branch plus a pull request into `release/*`. Do not `git push` the release branch until `fitness` has succeeded on that commit. |
| Owner | hub maintainer |
| Path | `tools/nouns/release_state/release_state.py`, `goals/hub_release/execute.sh` |
| Verification | A specimen whose commit is not a pull-request head must not execute `git push` of `release/*`. A specimen that already has a pull request and a successful `fitness` check may fast-forward. Re-run is the ruleset suite for a first push, which must not be `fail` on `pull_request` or `required_status_checks`. |
| Human acceptance | not requested by this record |
| Implementation route | not in this record |

---

## 10. Follow-up

Push-event run `41230009783` on `adf223e` failed `fitness-adr-record-gate` (`GH_TOKEN: ${{ github.token }}` in the ADR 0039 binder fixture). The pull-request `fitness` check on the same commit had succeeded at `04:22:25Z`. That disagreement is a separate failure. It is not the reason the first push was rejected.
