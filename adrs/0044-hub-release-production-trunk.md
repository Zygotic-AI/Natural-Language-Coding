# ADR 0044 — Hub release production trunk

- Status: Accepted
- Date: 2026-09-25
- Deciders: Human manager
- Ratified-by: Human manager (hub F process; Planit production-trunk plan)
- Class: F (process)
- Corpus: nlc

## Context

[ADR 0022](0022-hub-release-fail-early.md) orders release gates and keeps version bumps on `release/v*`. [ADR 0039](0039-single-command-human-surfaces.md) requires one resumable `./release` command. [ADR 0040](0040-process-preflight-remediation.md) requires preflight and copy-paste remediation.

Operators still had to remember branch policy: feature work landed on `main`, then release tooling expected a different shape (`release/v*`, merge commit tagging). The human contract should be:

1. Never commit to `main` (only merges).
2. `main` HEAD equals last tagged release.
3. Branch from `main`, work on the release line, sync `main` into that branch when others ship.
4. Run `./release`; follow `RELEASE:NOT_MET` or success.

## Decision

1. **Production trunk.** `main` is **tagged production only**: `main` HEAD commit must equal the newest reachable `v*.*.*` tag commit (or there is no tag yet). Unreleased work lives on **`release/v*`** (release line), not on `main`.

2. **Prepare leg source branch (inferred).** `./release` with **no arguments** uses [`nlc_release_infer.py`](../tools/nlc_release_infer.py):
   - Any work branch → inferred `release/vX.Y.Z` (create from branch tip or merge into existing release line).
   - If current branch is `release/vX.Y.Z`, continue there.
   - If current branch is `main` and purity NOT_MET, exit with remediation (move commits to a release branch; reset `main` to tag).
   - If `main` is pure with no release work, exit NOT_MET (branch from `main`, commit, re-run `./release`).
   - Optional `--bump` is **automation override** only ([`RELEASE.md`](../docs/adoption/RELEASE.md) appendix).

3. **Preserved gates ([ADR 0022](0022-hub-release-fail-early.md)).** Order unchanged in substance: preflight → target preflight → `verify-deep` at **shipped baseline** → notes → version on release line → post-bump `verify-deep` → prep → record → PR → tag gate on **merge commit** → tag push.

4. **Human surface.** Seven-step contract in [`docs/adoption/RELEASE.md`](../docs/adoption/RELEASE.md); disambiguation via tools (`nlc_release_main_purity.py`, context listing), not operator memory.

## Acceptance criteria

- `python3 tools/nlc_release_main_purity.py --check` returns MET when `main` HEAD equals last shipped tag commit; NOT_MET when `main` is ahead of tag.
- `./release --dry-run` from an arbitrary work branch prints `RELEASE:INFER` with inferred `release/vX.Y.Z` and bump class; no interactive menus.
- `./release --dry-run` from an existing `release/v*` branch does not force checkout to impure `main` for prepare.

## Consequences

- [`scripts/nlc-release.sh`](../scripts/nlc-release.sh): `apply_release_infer`, shipped-baseline `verify-deep` via tag checkout.
- [`tools/nlc_release_main_purity.py`](../tools/nlc_release_main_purity.py) and preflight wiring.
- [`.agents/skills/release/SKILL.md`](../.agents/skills/release/SKILL.md): agent closeout on release line; no ship commits to `main`.
- Fitness: ADR 0039 binder cites production-trunk docs and `release_fail` / purity tools.

## Rejected

- **Feature integration on `main` between tags** — unreleased commits on `main` break production-trunk preflight.
- **Prepare from impure `main` with silent checkout** — must fail with `RELEASE:NOT_MET` and move-work remediation.
- **Replacing tag-on-merge-commit** — merge commit remains the tagged artifact for consumers and CI.
