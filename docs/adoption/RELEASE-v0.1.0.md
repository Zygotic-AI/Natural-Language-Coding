# Releasing hub v0.1.0

Human steps when the tree is ready. **Tag and GitHub Release are last.**

## Before tag

Run once from repo root:

```bash
bash scripts/nlc-release-prep.sh
```

That runs fitness, verifies install hashes are committed, smoke test, and updates FINDINGS last-pass sha. Commit any FINDINGS change, then tag.

## Tag (last)

```bash
git tag -a v0.1.0 -m "Natural Language Coding hub v0.1.0"
git push origin main
git push origin v0.1.0
```

GitHub Actions [`.github/workflows/release.yml`](../../.github/workflows/release.yml) runs fitness, checks tag vs `nlc-version.json`, builds `dist/nlc-0.1.0.tar.gz`, and attaches it to the Release.

## After Release

- Remote install without `NLC_VERSION` resolves latest semver and downloads the tarball.
- App repos upgrade with `python3 ~/.local/share/nlc/hub/tools/nlc-update.py` once `0.1.1+` exists.
