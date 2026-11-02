# Releasing the [NLC](../TERMS.md#nlc) [hub](../TERMS.md#hub)

**One entrypoint:** invoke **`/release`** in chat, then **`./release`** when **Ship: GO**. Policy: [ADR 0039](../../adrs/0039-single-command-human-surfaces.md), [ADR 0044](../../adrs/0044-hub-release-production-trunk.md) (production trunk), [ADR 0045](../../adrs/0045-hub-release-identity.md) (one release identity and one next action), [ADR 0049](../../adrs/0049-release-planner-owns-stops.md) (the planner owns every intentional stop), and [ADR 0040](../../adrs/0040-process-preflight-remediation.md).

## Your workflow (seven steps)

1. **Never commit to `main`** — only merges (use branch protection).
2. **`main` HEAD = last tagged release** — no unreleased work on `main`. What is shipped? = semver tag reachable from `origin/main` + `integrity/nlc-version.json` + `integrity/hub-release-record.json` at that commit. `FINDINGS.md` is gap narrative only and must not contradict those three. `DESCRIBE.md` “Current ship” is narrative and must not contradict them either. Disagreement is a factory FAIL, not a reader FAIL.
3. **Branch from `main`:** `git checkout main && git pull && git checkout -b my-work` (any branch name).
4. **Do all ship work on your branch** (or on `release/v*` after `./release` normalizes the line).
5. **When another release ships:** `git fetch origin main && git merge origin/main` on your release line.
6. **Run `./release`** — no flags required. The planner names one version, one `release/v*` branch, and one tag. It does not merge, hard-reset, or otherwise repoint local `main`.
7. **Follow the result** — known audits and repairs run inside this invocation. `RELEASE:NOT_MET` means the planner reached a named decision that cannot be performed safely. An open PR exits successfully; run the same `./release` after the merge.

The tool runs gates ([ADR 0022](../../adrs/0022-hub-release-fail-early.md), 0038–0040, 0045, 0049) internally; you do not run `/verify`, `./nlc verify`, or a release subcommand between planner actions.

**Human in GitHub:** merge the **release PR** (`release/v* → main`) whose head SHA is the candidate `./release` pushed. The tag is created on that merge commit only when the version file, release record, and branch name all match. An existing tag is not moved.

## Checklist rule (ordinary content after the signed set)

A content-only change (paths that are not gate-set members) must not require a new owner gate-set signature. The whole-tree freshness stamp [`integrity/hub-content-tree-hash.txt`](../../integrity/hub-content-tree-hash.txt) is not a gate-set member. Sync it when content changes; do not remanifest or ask the owner to re-sign for that stamp.

A change to a real gate-set file still fails closed: missing tool, empty result, or unknown result counts as false (not a pass). The owner sidecar is required only when gate-set member bytes change.

Known-bad: `python3 tools/assert-content-only-change-does-not-trip-gate-set-signature-passes.py` (content-only plus hash sync leaves the signed manifest alone) and `python3 tools/assert-gate-set-member-change-fails-closed.py` (a real member edit is NOT_MET).

## Creating a release branch

Release branches (`release/vX.Y.Z`) are created only via the **start-release** workflow ([`.github/workflows/start-release.yml`](../../.github/workflows/start-release.yml)). Run it from the Actions tab with a version that matches `^v\d+\.\d+\.\d+$`. The workflow creates `release/<version>` from the current `main` HEAD and does nothing else (no commits, no tags). Do not create `release/*` refs by hand or by toggling the ruleset.

The ADR 0050 history rewrite drill runs at release tag time on the same self-hosted runner labels as start-release (vhost11), not on every pull request or push.

## Sync after someone else ships (step 5)

```bash
git fetch origin main
git checkout release/vX.Y.Z
git merge origin/main
```

## What the orchestrator does (internal)

Planner (`nlc_release_state.py`) chooses the one next action. The executor performs exactly that action, observes fresh facts, and plans again in the same invocation. Then: preflight → shipped-tag audit → release-prep audit (includes the published-skill author checklist `nlc-skill-author-check.py`, same list as post-install) → read-only `./nlc verify` in a worktree at the **shipped tag** → release notes → version on the release line → read-only `./nlc verify` on the release line → prep → record → commit → push → exact PR → tag gate on **that merge commit** (`./nlc verify` in a worktree, not `verify-deep`) → `git tag -a` on that SHA → tag push → GitHub Actions. `verify-deep` is a writer. Run it once, before the owner gate-set signature, and do not run it again after that signature.

A merged PR whose version file does not match the release branch is `INVALID_MERGED`. It is never tagged. The planner repairs the release line and creates a new candidate pull request, or names the human decision when no safe repair exists.

Details: [ADR 0045](../../adrs/0045-hub-release-identity.md) and [ADR 0049](../../adrs/0049-release-planner-owns-stops.md). Older plan notes: [RELEASE-ZERO-PARAMS-PLAN.md](RELEASE-ZERO-PARAMS-PLAN.md), [RELEASE-PRODUCTION-TRUNK-PLAN.md](RELEASE-PRODUCTION-TRUNK-PLAN.md).

## Refusal output

**`RELEASE:NOT_MET`**, **Problem**, **Gaps**, **Fix**, **Re-run: `./release`** — [ADR 0018](../../adrs/0018-human-cli-interview-on-gap.md).

## Appendix — automation overrides

Optional flags for scripts and recovery (not part of the seven-step contract):

| Flag | Effect |
| ---- | ------ |
| `--no-push` | Local-only execution; reports the branch, pull request, or tag action that is ready |
| `--dry-run` | Log actions, no git write |
| `--message "text"` | Override the release commit message |
| `-h`, `--help` | Show command usage |

## Appendix — manual checks

```bash
python3 tools/nlc_release_main_purity.py --check
python3 tools/nlc_release_infer.py --emit json
python3 tools/nlc_release_resume.py --emit json   # closed_release_branches vs stale_release_branches
python3 tools/nlc_release_target_preflight.py --check --target 0.2.1
python3 tools/nlc_release_tag_gate.py --check --commit <merge-sha> --tag v0.2.1
python3 tools/nlc_release_context.py --list-branches
python3 tools/nlc_release_shipped_tag_audit.py --check
```

## Release notes helper

```bash
python3 tools/nlc_release_notes.py --write-draft --version X.Y.Z --to HEAD
python3 tools/nlc_release_notes.py --check --version X.Y.Z
```

[Tag](../TERMS.md#tag) push runs [`.github/workflows/release.yml`](../../.github/workflows/release.yml).

## Branch protection (recommended)

- `main`: require PR, no direct push, required CI.
- Allow force-push **nowhere** on `main`. Delete a `release/v*` only when resume lists it in `stale_release_branches` (merged to `main` without `hub-release-record.json` on the merge). Keep `closed_release_branches` (a git tag exists for that version) unless a human asks to prune.
