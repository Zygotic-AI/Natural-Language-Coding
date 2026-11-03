# RCA — 2026-11-02-pr-offered-before-fitness-success

## Verdict

**Result:** PASS

**Evidence:** `node /home/rpickett/workspace/Zygotic-AI/zyprompt/metaprompts/scripts/validate-rca-record.mjs docs/rca/2026-11-02-pr-offered-before-fitness-success.md` → exit 0

**The one thing:** release/SKILL.md gate exits non-zero and blocks gh pr create until pr-offer-gate.py reports nlc verify and fitness success on that HEAD.

**Next:** Apply §8 in a separate run (`/planit` or an explicit apply). This record does not change the skill, the offer script, or any open pull request.

---

## 1. Error condition

error_condition: A hub pull request is offered as the merge step when the GitHub `fitness` check on that head is not success.

Repo: `/home/rpickett/workspace/Zygotic-AI/Natural-Language-Coding`. Subpath: `.agents/skills/release/SKILL.md` offer path and `gh pr create`. Severity: incident.

Not every recent pull request failed. Of the last 15, these heads have a `fitness` conclusion of success and are merged: #38, #40, #41, #42, #45, #48, #51. The defect is the offer that precedes a failure.

Observed offers whose `fitness` run failed:

| PR | Head | Fitness evidence |
| --- | --- | --- |
| #52 | `57fb634` `cursor/v041-checker-digest-signature` | Runs `41385442250` (push) and `41385448794` (pull_request), both failure. First violation: `hub-content-tree-hash 1c5630518f59a8e7611e4418d2f714388f44651e290a64409ec4b29feeaef76b != content digest bde9f4fb622a852b534766dd7d62e4e18f210ddf30003a77836b5e63ecd0a479`. Also `integrity/gate-set-baseline.manifest.sha256: missing 1 derived gate-set path(s); first='integrity/checker-digest.sha256.approval.asc'`. |
| #50 | `release/v0.4.1` | Run `41380597161` failure: `VIOLATION 0039` … `GH_TOKEN: ${{ github.token }}`. Other runs on that pull request succeeded. Recorded in `docs/rca/2026-11-02-release-recompiles-after-green-fitness.md`. |
| #47 | `cursor/v041-ship-bcb29bd` | Run `41372014469` failure, same `GH_TOKEN` binder line. Later runs succeeded and the pull request merged. |
| #46 | `cursor/v041-diagram-onto-release-line` | Run `41230009783` failure, same `GH_TOKEN` binder line. Later runs succeeded and the pull request merged. |
| #43 | `cursor/v041-dogfood-license-rename` | Runs `41149846998` and `41149842731` failure: `CI:FAIL fitness-mandate-inheritance`. Merged anyway. |
| #39 | `cursor/pr38-masked-shape-rca-8ecd` | Run `40445127425` failure: `hub-content-tree-fresh` `RESULT:NOT_MET`. Still open. |

Pull request #52 is the offer in this session. The commands before `gh pr create` were `python3 tools/check-checker-digest-signature.py` (exit 0, `CHECKER_DIGEST_SIGNATURE:MET`) and `git commit` of `integrity/checker-digest.sha256.approval.asc`. `./nlc verify` was not run. `python3 tools/sync-hub-content-tree-hash.py` was not run. The pull request URL was then given as the step that unblocks the `v0.4.1` tag. Both fitness runs finished failure within about two minutes.

`.agents/skills/release/SKILL.md` step 1A already says to sync the content-tree stamp and to run `./nlc verify` before `./release`. That text did not run, and nothing exited non-zero in front of `gh pr create`. The release-branch `gh` failure class is already bounded in `docs/rca/2026-11-02-release-recompiles-after-green-fitness.md`. This record is the offer that happens before `fitness` on that commit is success.

## 2. Impact / scope

The operator is told a pull request is the next merge, then the required `fitness` check on that head fails. Each red head on `release/v0.4.1` needs another pull request because that branch rejects a direct push (`docs/rca/2026-10-31-release-line-push-without-pr.md`). The ship of `v0.4.1` stays untagged across those runs. Local `check-checker-digest-signature.py` does not grade `hub-content-tree-fresh` or the gate-set manifest, so a MET from that command is not a fitness result.

## 3. Timeline

| Time (UTC) | Event |
| --- | --- |
| 2026-10-27T03:36:25Z | Pull request #39 fitness runs fail on `hub-content-tree-fresh`. |
| 2026-10-31T00:22:51Z | Pull request #43 fitness runs fail on `fitness-mandate-inheritance`. |
| 2026-10-31T18:33:40Z | Run `41230009783` on pull request #46 fails the ADR 0039 binder with the `GH_TOKEN` hint. |
| 2026-11-02T01:17:25Z | Pull request #47 records both a failed fitness run (`41372014469`) and later successes, then merges. |
| 2026-11-02T02:59:28Z | Run `41380597161` on pull request #50 fails the same binder line. |
| 2026-11-02T03:53:06Z | Pull request #52 opens on `57fb634`. |
| 2026-11-02T03:55:26Z | Both fitness runs for #52 are failure. The chat had already named #52 as the merge that can take the tag. |

## 4. The one thing

one_thing: release/SKILL.md gate exits non-zero and blocks gh pr create until pr-offer-gate.py reports nlc verify and fitness success on that HEAD.

## 4b. System layer classification

| Layer | Implicated? | Evidence | Recommended control (summary) |
| ----- | ----------- | -------- | ----------------------------- |
| L0 Symptom | Y | Pull request #52 runs `41385442250` and `41385448794` print `FAILED hub-content-tree-fresh` and `RESULT:NOT_MET`. Runs `41380597161`, `41372014469`, and `41230009783` print the `GH_TOKEN` binder line. | The offer command prints those violation lines and does not print a pull request URL. Secondary. |
| L1 Local system | Y | `tools/check-checker-digest-signature.py` exited 0 on `57fb634` while `hub-content-tree-fresh` and `fitness-derived-release-state` are the CI failures. `python3 tools/sync-hub-content-tree-hash.py` was not part of the offer. No script stands between the shell and `gh pr create`. | `tools/pr-offer-gate.py` exits non-zero unless `./nlc verify` passed on that HEAD and the push `fitness` run for that SHA succeeded, and only then calls `gh pr create`. |
| L2 Meta-system | Y | `.agents/skills/release/SKILL.md` step 1A lists `./nlc verify` and the content-tree stamp as prose. The offer of #52 did not run them. No skill row, planit phase, or harness check exits non-zero when `gh pr create` runs without those results and without a successful `fitness` run on that SHA. L2 is not ruled out. | The skill's only offer step is `tools/pr-offer-gate.py`. A non-zero exit blocks the pull request and blocks the ready sentence. |

## 5. Prevention test

If `tools/pr-offer-gate.py` had been the only offer step, pull request #52 could not have been created: `./nlc verify` on `57fb634` fails `hub-content-tree-fresh` and the missing gate-set path, and push run `41385442250` concluded failure. The ready sentence could not have been sent, because the gate would have exited non-zero before `gh pr create`.

```
prevention_test:
cmd: git grep -n "pr-offer-gate.py" -- .agents/skills/release/SKILL.md
```

## 6. Poke-yoke (mandatory — apex)

| Field | Value |
|-------|-------|
| poke_yoke | `.agents/skills/release/SKILL.md` has one offer step, `python3 tools/pr-offer-gate.py`. That command exits non-zero and does not call `gh pr create` unless `./nlc verify` has exited 0 on the candidate HEAD and `gh run list --commit <sha> --workflow fitness.yml --json conclusion,event` shows a completed push run with `conclusion=success` and no completed `fitness` run on that SHA with any other conclusion. The ready sentence is allowed only after that exit 0. |
| on_trip | remediate:Add `tools/pr-offer-gate.py` that runs `./nlc verify` for the candidate HEAD, then `gh run list --commit <sha> --workflow fitness.yml --json databaseId,conclusion,event,status`, and exits 1 with the verify or run lines when verify is non-zero, when no push run is success, or when any completed fitness run is not success. On exit 0 it runs `gh pr create`. In `.agents/skills/release/SKILL.md`, delete any offer path that calls `gh pr create` directly and name `python3 tools/pr-offer-gate.py` as the only offer command. |
| guarantee | After that gate, a pull request cannot be offered as ready, and `gh pr create` cannot run from the skill path, unless `./nlc verify` passed on that HEAD and the push `fitness` run for that SHA succeeded. The #52 offer (signature check only, then `gh pr create`, then a failed fitness run) cannot be entered without hitting this non-zero exit. |

## 7. Contributing factors

- The #52 offer used `tools/check-checker-digest-signature.py` as if it were the fitness suite. That command does not grade the content-tree stamp or the gate-set manifest.
- `release/v0.4.1` rejects a direct push, so the signature commit had to become a pull request. The branch rule is in `docs/rca/2026-10-31-release-line-push-without-pr.md`.
- Release-branch `gh` calls still fail when no token is exported. That class stays in `docs/rca/2026-11-02-release-recompiles-after-green-fitness.md` and is why several heads showed a failed fitness run beside a later success.
- Skill step 1A already named `./nlc verify`. Naming it did not stop the shell from calling `gh pr create`.

## 8. Recommended preventive actions

status: recommended

### 8.1 Meta-system (L2)

| Field | Value |
|-------|-------|
| layer | L2 |
| status | recommended |
| Owner | hub maintainer |
| Path / artifact | `.agents/skills/release/SKILL.md` |
| poke_yoke | The skill cannot call a pull request ready and cannot call `gh pr create`. The only offer command is `python3 tools/pr-offer-gate.py`. A non-zero exit from that command ends the offer. |
| on_trip | remediate:In `.agents/skills/release/SKILL.md`, replace every `gh pr create` instruction with `python3 tools/pr-offer-gate.py`, and state that a ready sentence is forbidden unless that command exits 0. |
| guarantee | The skill path that offered pull request #52 cannot create a pull request or say it is ready unless the offer gate exited 0 for that HEAD. |
| Verification command | `cmd: git grep -n "pr-offer-gate.py" -- .agents/skills/release/SKILL.md` |
| Apply via | separate `/planit` / `/awl-run` / `/zp-do` / explicit apply — **not** `/conduct-rca` |

### 8.2 Local system (L1)

| Field | Value |
|-------|-------|
| layer | L1 |
| status | recommended |
| Owner | hub maintainer |
| Path / artifact | `tools/pr-offer-gate.py` |
| poke_yoke | `tools/pr-offer-gate.py` exits non-zero and does not invoke `gh pr create` when `./nlc verify` is non-zero for the candidate HEAD, when the content-tree stamp does not match, when no push `fitness` run for that SHA has `conclusion=success`, or when any completed `fitness` run for that SHA is not success. |
| on_trip | remediate:Write `tools/pr-offer-gate.py` to run `./nlc verify`, require `integrity/hub-content-tree-hash.txt` to match the tree, then require `gh run list --commit <sha> --workflow fitness.yml --json conclusion,event,status` to show one successful push run and zero non-success completed runs. Print the verify `RESULT:NOT_MET` lines or the run ids on failure. Call `gh pr create` only after those checks exit 0. |
| guarantee | A head like `57fb634`, where `check-checker-digest-signature.py` is MET and `hub-content-tree-fresh` is NOT_MET, cannot become a pull request through this command. A head whose push `fitness` run failed, as in runs `41385442250`, `41380597161`, `41372014469`, and `41230009783`, cannot become a pull request through this command. |
| Verification command | `cmd: git grep -n "gh pr create" -- tools/pr-offer-gate.py` |
| Apply via | separate `/planit` / `/awl-run` / `/zp-do` / explicit apply — **not** `/conduct-rca` |

### 8.3 Symptom containment (L0)

| Field | Value |
|-------|-------|
| layer | L0 |
| status | recommended |
| Owner | hub maintainer |
| Path / artifact | `tools/pr-offer-gate.py` stdout |
| poke_yoke | On a non-zero exit the command prints the fitness `VIOLATION` and `RESULT:NOT_MET` lines, or the failing run id and conclusion, and prints no pull request URL. |
| on_trip | remediate:In `tools/pr-offer-gate.py`, write those lines to stdout before returning 1, and do not print a `https://github.com/` pull request URL on that path. |
| guarantee | A failed offer cannot show a pull request URL as the next merge step. |
| Verification command | `cmd: git grep -n "RESULT:NOT_MET" -- tools/pr-offer-gate.py` |
| Apply via | separate `/planit` / `/awl-run` / `/zp-do` / explicit apply — **not** `/conduct-rca` |
| note | secondary / not sufficient alone |

## 9. Follow-up

Printing the violation text is §8.3 only. It does not replace the skill gate in §8.1 or the offer command in §8.2. The release-branch token probe stays in `docs/rca/2026-11-02-release-recompiles-after-green-fitness.md`. Do not apply either record from `/conduct-rca`.
