# Natural Language Coding hub v0.3.0

## Highlights

Hub **v0.3.0** is the zero-parameter ship path. Adopters and hub maintainers run **`./release`** with no `--bump` and no branch menu. The orchestrator infers the next version, the `release/v*` line, and the bump class from git state (ADR 0039, ADR 0044).

- **Production trunk.** `main` stays at the last shipped tag. Unreleased work stays on `release/v*`. If `main` has drifted, `./release` preserves that work on `work/X.Y.Z` and resets local `main` to the shipped tag before continuing. It does not push that reset.
- **Resume matches the remote.** `./release` waits for a pull-request merge only after `release/v*` exists on `origin`. A local-only release branch continues prepare instead of polling for a merge that was never pushed.
- **Shipped baseline is the peeled tag commit.** Annotated tag object ids are not treated as a different release. Trunk normalize, verify-deep, and the shipped-tag audit use that commit. A failed baseline verify returns to the release branch instead of leaving a detached HEAD.
- **NOT_MET is actionable.** Remediation comes from the tool. Agents fix the cited gate or re-run `./release`. They do not tell operators to ignore defective output.

**Explicitly not in v0.3.0**

- A new compiled-system use-case wave beyond v0.2.0.
- Pushing or force-moving the remote `main` or remote tags from trunk normalize.

## Changes since v0.2.0

_No commits in range._

---

Draft commits/range from `python3 tools/nlc_release_notes.py --write-draft --version 0.3.0 --to HEAD`. Edit **Highlights** before merge; `./release finish` refuses to tag without them.
