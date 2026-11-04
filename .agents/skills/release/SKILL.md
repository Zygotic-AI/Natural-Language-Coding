---
name: release
description: Hub ship entrypoint — run ./release for the six-step unsigned path. Use when the user wants to release, ship, promote, tag, or run ./release.
disable-model-invocation: true
---

# Release (`/release`)

**One command:** `./release`. Chat `/release` means run that command. There is no second checklist.

The human path is six steps (ADR 0058). **Sign is not done.** Merge is accept.

1. A `release/<semver>` branch exists (`./release` may create it).
2. Work merges into that branch.
3. `./release` checks everything and lists sensitive files. Revert, edit, or accept by merging. Stay on this step until every listed file is resolved.
4. After that, never sign another thing.
5. Merge the release pull request to `main`.
6. `./release` tags the merge commit.

## Gate (default-closed)

Do **not** tell the human to sign. Do **not** invent a seventh step.

| Criterion | Blocking? | Pass when | Evidence |
| --------- | --------- | --------- | -------- |
| Repo root | yes | NLC hub workspace | Path |
| Six-step path | yes | Steps 1–6 above; `./release` is the only command | This skill + `docs/adoption/RELEASE.md` |
| Sensitive list | yes when a listed path changed | `python3 tools/nlc_release_sensitive_review.py --check` printed the paths; the pull-request body carries the same list | Command output |
| Machine checks | yes | `./nlc verify` MET inside `./release` | Exit 0 |
| Merge is accept | yes for step 5 | GitHub merge of the release pull request | Merge commit |
| No signature stop | yes | Output does not ask for a signature or OpenPGP armor | `python3 tools/fitness-sign-stop.py` |

**Done signals:** `./release` running, awaiting merge, tagged, or stopped on a named machine/merge decision. Never stopped to request a signature.

## Procedure

Run `./release` from the hub root with no flags. Report its output. If it prints `SENSITIVE_REVIEW:NOT_MET`, the listed paths are the review. The human reverts, edits, or merges. Re-run `./release` after that.

Do not write `Released-by:`. Do not paste armor. Do not run `scripts/sign-adrs.sh`.

Never tell the operator to ignore or reinterpret command output (`.agents/instructions/jidoka-ssot-output.md`).

## CONTROL-LIFECYCLE (control or gate design)

When this skill or `./release` is the control under change, walk **create, change, list, accept, merge**, and **first bootstrap**. Known-bad of a **legitimate change to the verifier:** main's copy still lists a path the branch copy hid (`python3 tools/assert-sensitive-review-hide-fails.py`).

## Routing

| Need | Skill |
| ---- | ----- |
| Compile proof | [`bbp-confirmer`](../bbp-confirmer/SKILL.md) |
| Large hub change plan | [`planit`](../planit/SKILL.md) |

## Reference

- `docs/adoption/RELEASE.md`
- `adrs/0058-six-step-unsigned-release.md`
