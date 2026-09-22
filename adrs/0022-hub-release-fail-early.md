# [ADR](../docs/TERMS.md#adr) 0022 — [Hub](../docs/TERMS.md#hub) release fail-early ([gate](../docs/TERMS.md#gate) order)

- Status: Accepted
- Date: 2026-09-20
- Deciders: Human manager
- Class: F (process / release)

## Context

[`./release`](../release) orchestrates branch, PR, [tag](../docs/TERMS.md#tag), and GitHub Release assets. Operators reported releases continuing without release notes, version confusion between [`integrity/nlc-version.json`](../integrity/nlc-version.json) and git tags, and heavy work (`verify-deep`) running before cheap gates.

[ADR 0013](0013-requirements-preflight.md) requires fail-fast preflight before expensive work. [ADR 0010](0010-gate-after-every-generate.md) requires gates before downstream steps. [ADR 0015](0015-distribution-lock-and-version-store.md) names `nlc-version.json` as artifact SSOT but **published** semver is whatever `v*.*.*` [tag](../docs/TERMS.md#tag) exists on the remote.

## Decision

1. **Preflight first:** `./release` runs [`tools/nlc_release_preflight.py`](../tools/nlc_release_preflight.py) before release type, notes, or `verify-deep`. On **`main`**, `integrity/nlc-version.json` **must equal** the semver of the newest reachable `v*.*.*` [tag](../docs/TERMS.md#tag); version bumps happen on `release/v*` (merged with the tag), not on `main` between tags.

2. **Shipped baseline = git [tag](../docs/TERMS.md#tag) only:** Changelog drafts and “since” ranges use the newest reachable **`v*.*.*` [tag](../docs/TERMS.md#tag)** ([`tools/nlc_release_tags.py`](../tools/nlc_release_tags.py)), never the version file alone.

3. **Release target preflight (right after class):** Once the operator picks release class, [`tools/nlc_release_target_preflight.py`](../tools/nlc_release_target_preflight.py) checks the full **shipped tag → target** migration chain (ADR 0014) **before** notes, branch, or version write. `./release` may offer **`--ensure-noop`** scaffolding or print an **agent prompt**; it must not continue in a half-baked state.

4. **`verify-deep` before notes and bump:** On **`main`** at the shipped version, `./release` runs **`verify-deep`** after target preflight. Compile gates must pass before release notes or any version write.

5. **Release notes before version write:** After target + compile gates, **blocks** until [`docs/adoption/RELEASE-vX.Y.Z.md`](../docs/adoption/RELEASE.md) has valid **Highlights** ([`tools/nlc_release_notes.py`](../tools/nlc_release_notes.py)). Runs **before** checkout of `release/v*`, version bump, post-bump `verify-deep`, prep, commit, or [tag](../docs/TERMS.md#tag). `--yes` does not skip this [gate](../docs/TERMS.md#gate).

6. **Version file on `release/v*` only:** `nlc-version.json` is updated only on the release branch, after notes pass and **before** the post-bump `verify-deep` (except `keep`, which still requires notes for that version). [`tools/nlc_release_bump.py`](../tools/nlc_release_bump.py) writes **every semver hop** in the chain, not only a direct folder.

7. **[Tag](../docs/TERMS.md#tag) push:** CI and `./release finish` re-check release notes on the merge commit; GitHub Release body uses the committed notes file.

## Consequences

- Maintainers reset mistaken version bumps on `main` to match the last [tag](../docs/TERMS.md#tag), or finish the release on `release/v*`.
- [`docs/adoption/RELEASE.md`](../docs/adoption/RELEASE.md) documents operator steps; [`.agents/instructions/release-notes.md`](../.agents/instructions/release-notes.md) documents agent drafting.

## Rejected

- **Defer release notes to [tag](../docs/TERMS.md#tag) time** — too late; PR and adopters need the file on the release branch.
- **Use `nlc-version.json` as changelog baseline** — conflates working copy with what shipped.
- **Suggest semver class as default choice** — operator must pick explicitly.
