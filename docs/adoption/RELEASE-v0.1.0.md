# Releasing hub v0.1.0

Human steps when the tree is ready. **Tag and GitHub Release are last.**

## Before tag

1. `python3 tools/ci_fitness.py` → `CI:MET`
2. `python3 tools/nlc-install-hash-update.py` — commit `integrity/nlc-install-hashes.json` if it changed
3. `bash scripts/nlc-release-smoke.sh` → `RELEASE_SMOKE:MET`
4. Confirm `integrity/nlc-version.json` matches the tag you will push (`0.1.0`)

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
