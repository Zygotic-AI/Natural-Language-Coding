# ADR 0015 — Distribution: version store, lock file, two layouts

- Status: Accepted
- Date: 2026-09-20
- Deciders: Human manager
- Class: F (process / distribution)

## Context

Adopters work in **their** application repos. NLC must not require a git submodule of the hub (git-in-git). Distribution should resemble **pip / npm**: immutable semver artifacts, a small committed lock in the app repo, and install/update commands—not `git pull` on the hub inside the product tree.

Two supported layouts:

1. **Per repo (default)** — lock at `.nlc/lock.json`; hub payloads live in the **user store** (`~/.local/share/nlc/versions/<semver>/`, active `hub` pointer).
2. **Workspace root** — shared store at a workspace path; child repos use `store: workspace` and `store_path` in the lock.

## Decision

1. **Hub semver SSOT:** [`integrity/nlc-version.json`](../integrity/nlc-version.json) in each release artifact.

2. **Project lock:** [`.nlc/lock.json`](../integrity/schemas/nlc-lock.schema.json) — `schema`, `hub` (semver), `store` (`user` | `workspace` | `project`), optional `store_path`.

3. **User store layout:**
   - `versions/<semver>/` — full hub tree for that release
   - `current` — single-line active semver
   - `hub` — symlink (or copy on Windows) to `versions/<current>/`

4. **Remote install:** [`tools/nlc-fetch-hub.py`](../tools/nlc-fetch-hub.py) downloads release tarball `nlc-<semver>.tar.gz` (or registers a local checkout with `--from-path`). Shell installers call this instead of `git clone` for consumers.

5. **Upgrade:** [`tools/nlc-update.py`](../tools/nlc-update.py) advances the lock along the published semver catalog, one hop at a time, per [ADR 0014](0014-semver-upgrade-steps-and-noop-migrations.md). Migration units ship in the **target** release tree.

6. **Release build:** Tag `vX.Y.Z` triggers CI fitness + [`tools/nlc-release-build.py`](../tools/nlc-release-build.py) + GitHub Release asset upload.

7. **Greenfield:** [`tools/nlc-init.py`](../tools/nlc-init.py) writes `.nlc/lock.json` pinned to the installed hub version.

## Consequences

- Consumer curl URL may stay on `main` for the bootstrap script; **pin is the app lock**, not the one-liner.
- Maintainers bump `integrity/nlc-version.json` and add `migrations/<from>_to_<to>/` for every release.
- `NLC_REF` / `NLC_VERSION` remain overrides for install; default resolves latest published semver.

## Rejected

- Hub as git submodule inside adopter repos.
- Implicit “latest” with no lock in the application repo.
