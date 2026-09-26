# ADR 0045 — Hub release identity

- Status: Accepted
- Date: 2026-09-26
- Deciders: Human manager
- Ratified-by: Human manager (release-state plan, 2026-09-26)
- Class: A (release identity) with class C orchestration
- Corpus: nlc

## Context

[ADR 0022](0022-hub-release-fail-early.md) orders the release gates. [ADR 0039](0039-single-command-human-surfaces.md) requires one resumable `./release`. [ADR 0040](0040-process-preflight-remediation.md) requires preflight and copy-paste remediation. [ADR 0044](0044-hub-release-production-trunk.md) keeps unreleased work off `main`.

The ship path still re-derived version, branch, candidate SHA, merge SHA, and tag in the shell, infer, resume, bump, and tag gate. Those derivations tagged the wrong commit, waited on a different release line, compared an annotated tag object to its peeled commit, and offered to move a shipped tag. Eight release RCAs patched symptoms of that split identity.

## Decision

1. **One identity.** Desired release state is `{version, branch, planned_tag}`. Observed facts are separate: local and remote branch SHAs, candidate and merge file versions, candidate and merge record version and branch, pull request number, head SHA, merge SHA, and state, local and remote tag peels, publish status, `origin/main`, and the shipped tag peel. The word `tag` is not overloaded: `planned_tag` is the name to create; a peel is an observed commit.

2. **One planner.** [`tools/nouns/release_state/release_state.py`](../tools/nouns/release_state/release_state.py) is pure: facts in, one phase, one action. [`tools/nlc_release_state.py`](../tools/nlc_release_state.py) observes git and GitHub and does not mutate. The executor in [`scripts/nlc-release.sh`](../scripts/nlc-release.sh) performs only the planned action. Infer and resume do not choose a second phase.

3. **Phases.** `PREPARE_DRAFT` may still have the shipped version in the version file. `CANDIDATE_READY_LOCAL`, `AWAIT_PR` (exit and re-run `./release`), `INVALID_MERGED`, `TAG_READY` (`git tag -a planned_tag merge_sha`), `TAG_CREATED_LOCAL` (push only after the peel equals the merge), `TAGGED_PUBLISH_PENDING`, `PUBLISH_FAILED` (retry publication from the existing tag), `SHIPPED_COMPLETE`, `BLOCKED`, and historical `CLOSED_TAGGED`. A line is `CLOSED_TAGGED` when the tagged commit's file version, record version, and record branch agree with that tag. A missing GitHub Release is `PUBLISH_FAILED`, not an open release line.

4. **Invalid merge outranks tagging and main surgery.** When the exact pull request (head SHA equals the candidate) is merged and the merge commit's version file, record version, and record branch do not all equal the desired identity, the phase is `INVALID_MERGED`. The executor does not tag that merge and does not `reset` or force-push `main`. Repair is a new commit on the same `release/vX.Y.Z` line.

5. **Remote branch relation is exhaustive.** Absent: push new. Equal: one exact pull request. Local descendant: fast-forward push. Local ancestor: `BLOCKED_REMOTE_AHEAD`. Diverged: `BLOCKED_DIVERGED`. Unknown: `BLOCKED_REMOTE_UNKNOWN`. No force-push. More than one active release line, or more than one pull request for the same head SHA, is `BLOCKED` with every gap listed. No interactive choice and no `.[0]` selection.

6. **Local `main` repoint** only when `origin/main` equals the shipped tag peel and no invalid merged candidate exists. The executor does not stash and does not detach the active checkout. Shipped-baseline `verify-deep` runs in an isolated worktree.

7. **Amendments.** [ADR 0039](0039-single-command-human-surfaces.md) decision 2: pausing at an open pull request and resuming with the same `./release` is the legal await exit. [ADR 0040](0040-process-preflight-remediation.md) decision 3: for release, several candidate lines are `BLOCKED`, not an interactive pick. [ADR 0044](0044-hub-release-production-trunk.md) local reset of `main` is allowed only under decision 6 of this ADR. Moving an existing tag is not a normal path.

## Acceptance criteria

- `python3 tools/assert-release-state-passes.py` exits 0, including the invalid v0.3 merge oracle (no tag, no main repoint) and a temp-repo annotated tag whose peel is the named commit.
- `./release` calls the planner before mutation. `BLOCKED` and `INVALID_MERGED` exit without `git tag` and without `git reset --hard`.
- An annotated tag command includes the merge SHA. A peel mismatch deletes that new local tag and does not push it.

## Consequences

- [`docs/adoption/RELEASE.md`](../docs/adoption/RELEASE.md) and [`.agents/skills/release/SKILL.md`](../.agents/skills/release/SKILL.md) follow this identity.
- Fitness: ADR 0039 binder requires the planner, `--tag-argv`, a shipped-baseline worktree, and no stash or `git tag -f`.

## Rejected

- **Tagging the invalid v0.3 merge** — the version file on that merge is not 0.3.0.
- **Moving `v0.2.0`** — the shipped tag already peels to its release commit.
- **Resetting `main` while `origin/main` is that invalid merge.**
- **A second planner inside infer or resume.**
