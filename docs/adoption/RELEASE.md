# Releasing the [NLC](../TERMS.md#nlc) [hub](../TERMS.md#hub)

**One command:** `./release`. Policy: [ADR 0058](../../adrs/0058-six-step-unsigned-release.md) (six-step unsigned path), [ADR 0039](../../adrs/0039-single-command-human-surfaces.md), [ADR 0044](../../adrs/0044-hub-release-production-trunk.md) (work lives on `release/<semver>`), [ADR 0045](../../adrs/0045-hub-release-identity.md), [ADR 0049](../../adrs/0049-release-planner-owns-stops.md).

## Your workflow (six steps)

1. **A `release/<semver>` branch exists.** `./release` may create it. Do not require a separate start-release ritual.
2. **Everything merges into that branch.** One in-flight release line. Other work merges into it.
3. **One command.** `./release` checks everything that must be checked. If a sensitive file changed, it lists the path. Revert, edit, or accept by merging. Stay on this step until every listed file is resolved. Prefer fewer sensitive files. Do not sign them.
4. **Never sign another thing.** No GPG, no sidecar, no signature prompt.
5. **Merge to `main`.** GitHub merge of the release pull request. That merge is accept. It is the C24 record.
6. **Tag.** `./release` after the merge tags that merge commit and pushes the tag.

Opening the pull request is how GitHub does step 5. It is not a seventh step. `./release` opens or updates it when step 3 is ready.

Never commit to `main` except by that merge. Branch protection: no direct push to `main`.

## Sensitive-file list

The lock that replaces GPG. `./release` runs the copy of `tools/nlc_release_sensitive_review.py` already on `origin/main` (bootstrap: the branch copy, until that merge). Prefixes are the table in [ADR 0058](../../adrs/0058-six-step-unsigned-release.md). The 3,642-row membership list is a machine freshness check, not a human review.

| Action | List after |
| --- | --- |
| Revert so bytes match `origin/main` | Line gone |
| Edit and re-run `./release` | Line stays or updates to the new hash |
| Merge the pull request whose body listed that path + hash | Merge is accept |

## What the command still checks (machine, not extra human steps)

- `./nlc verify` / `python3 tools/ci_fitness.py`
- Unsigned derived freshness (membership list and digest hex). No armor.
- Version, release record, and branch name agree ([ADR 0045](../../adrs/0045-hub-release-identity.md))

Stops that die: a signature request; Highlights placeholder as a tag blocker; a second chat skill that is a different checklist.

## Refusal output

**`RELEASE:NOT_MET`**, **Problem**, **Gaps**, **Fix**, **Re-run: `./release`** — [ADR 0018](../../adrs/0018-human-cli-interview-on-gap.md).

## Appendix — automation overrides

| Flag | Effect |
| ---- | ------ |
| `--no-push` | Local-only execution; reports the branch, pull request, or tag action that is ready |
| `--dry-run` | Log actions, no git write |
| `--message "text"` | Override the release commit message |
| `-h`, `--help` | Show command usage |

[Tag](../TERMS.md#tag) push runs [`.github/workflows/release.yml`](../../.github/workflows/release.yml).
