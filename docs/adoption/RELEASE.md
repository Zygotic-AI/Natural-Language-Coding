# Releasing the [NLC](../TERMS.md#nlc) [hub](../TERMS.md#hub)

You should not memorize steps. From a **clone of this repo**, at the root:

```bash
./release
```

That is the only command you need. (`ls` at repo root shows `release` next to `nlc`.)

## What `./release` does

1. Asks **patch / minor / major** (or **keep** current `integrity/nlc-version.json`) and suggests a default from your git changes (e.g. new ADR or PCI text → **minor**).
2. Runs **`./nlc verify-deep`**.
3. Bumps version + creates a **noop migration** folder when needed ([ADR 0014](../../adrs/0014-semver-upgrade-steps-and-noop-migrations.md)).
4. Runs **`scripts/nlc-release-prep.sh`** (fitness, install hashes, smoke, FINDINGS last-pass sha).
5. **Commits** (with your confirmation).
6. **Tags** `vX.Y.Z` and **pushes** `main` + [tag](../TERMS.md#tag) (with your confirmation).

GitHub Actions [`.github/workflows/release.yml`](../../.github/workflows/release.yml) then runs fitness, [verify](../TERMS.md#verify), smoke, builds `dist/nlc-X.Y.Z.tar.gz`, and publishes the Release.

## Options

```bash
./release --help
./release --bump minor --yes --no-push    # CI or advanced: bump, no push
./release --message "Release v0.2.0: requirement packs"
```

Lower-level scripts (you rarely need these):

| Script | Role |
| ------ | ---- |
| `scripts/nlc-release-prep.sh` | Prep only (no commit/tag/push) |
| `scripts/nlc-release-smoke.sh` | Install + [greenfield](../TERMS.md#greenfield) lock smoke |
| `tools/nlc_release_bump.py` | Semver math + bump heuristics |

## After Release

- Curl install without `NLC_VERSION` can resolve the latest GitHub Release tarball.
- App repos upgrade with `nlc-update.py` when a newer [hub](../TERMS.md#hub) version exists.

Historical note: [RELEASE-v0.1.0.md](RELEASE-v0.1.0.md) described the first v0.1.0 cut; use **`./release`** for all versions.
