# Releasing the [NLC](../TERMS.md#nlc) [hub](../TERMS.md#hub)

**One entrypoint:** invoke **`/release`** in chat, then **`./release`** when **Ship: GO**. Policy: [ADR 0039](../../adrs/0039-single-command-human-surfaces.md), [ADR 0044](../../adrs/0044-hub-release-production-trunk.md) (production trunk), [ADR 0045](../../adrs/0045-hub-release-identity.md) (one release identity and one next action), [ADR 0040](../../adrs/0040-process-preflight-remediation.md).

Legacy **`./release prepare`** / **`finish`** forward into the same orchestrator.

## Your workflow (seven steps)

1. **Never commit to `main`** — only merges (use branch protection).
2. **`main` HEAD = last tagged release** — no unreleased work on `main`.
3. **Branch from `main`:** `git checkout main && git pull && git checkout -b my-work` (any branch name).
4. **Do all ship work on your branch** (or on `release/v*` after `./release` normalizes the line).
5. **When another release ships:** `git fetch origin main && git merge origin/main` on your release line.
6. **Run `./release`** — no flags required. The planner names one version, one `release/v*` branch, and one tag. It fast-forwards local `main` to the shipped tag only when `origin/main` is already that tag (ADR 0044, ADR 0045).
7. **Follow stderr** — `RELEASE:NOT_MET` + copy-paste fix, or success through PR merge and tag push. An open PR exits; run `./release` again after the merge.

The tool runs gates ([ADR 0022](../../adrs/0022-hub-release-fail-early.md), 0038–0040, 0045) internally; you do not need a separate checklist.

**Human in GitHub:** merge the **release PR** (`release/v* → main`) whose head SHA is the candidate `./release` pushed. The tag is created on that merge commit only when the version file, release record, and branch name all match. An existing tag is not moved.

## Sync after someone else ships (step 5)

```bash
git fetch origin main
git checkout release/vX.Y.Z
git merge origin/main
```

## What the orchestrator does (internal)

Planner (`nlc_release_state.py`) chooses the one next action. Infer still suggests the next version when no release line exists. Then: preflight → shipped-tag audit → release-prep audit → `verify-deep` in a worktree at the **shipped tag** → release notes → version on the release line → `verify-deep` → prep → record → push → exact PR → tag gate on **that merge commit** → `git tag -a` on that SHA → tag push → GitHub Actions.

A merged PR whose version file does not match the release branch is `INVALID_MERGED`. `./release` stops. It does not tag that merge and it does not reset `main`.

Details: [ADR 0045](../../adrs/0045-hub-release-identity.md). Older plan notes: [RELEASE-ZERO-PARAMS-PLAN.md](RELEASE-ZERO-PARAMS-PLAN.md), [RELEASE-PRODUCTION-TRUNK-PLAN.md](RELEASE-PRODUCTION-TRUNK-PLAN.md).

## Refusal output

**`RELEASE:NOT_MET`**, **Problem**, **Gaps**, **Fix**, **Re-run: `./release`** — [ADR 0018](../../adrs/0018-human-cli-interview-on-gap.md).

## Appendix — automation overrides

Optional flags for scripts and recovery (not part of the seven-step contract):

| Flag | Effect |
| ---- | ------ |
| `--bump patch\|minor\|major\|keep` | Override inferred bump |
| `--from-branch release/vX.Y.Z` | Force release line branch |
| `--no-push` | Local only; prints push commands |
| `--dry-run` | Log actions, no git write |
| `--yes` | Deprecated; default is non-interactive |

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
- Allow force-push **nowhere** on `main`; delete stale `release/v*` after ship.
