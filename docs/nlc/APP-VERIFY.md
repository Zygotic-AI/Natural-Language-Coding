# [App repo](../TERMS.md#adopter) [verify](../TERMS.md#verify)

[Hub](../TERMS.md#hub) specimens use `ci_fitness.py`. **Your app** uses a layered [verify](../TERMS.md#verify) story:

1. **`./nlc verify`** — on an app repo, fast fingerprints (`.nlc/verified.json`) + pipeline blockers. On the hub, this is the one merge command: it runs `tools/ci_fitness.py`. The hub does not also fail on `.nlc/verified.json`; the content-tree stamp covers those bytes.
2. **`./nlc verify-deep`** — full gates, then refresh fingerprints. The fingerprint file and its `recorded_at` are rewritten only when a recorded file hash changed. A second run on the same bytes leaves `.nlc/verified.json` untouched. Run it once before an owner gate-set signature, not after.

## Default deep [gate](../TERMS.md#gate) (app with `.nlc/lock.json`)

`verify-deep` runs [hub](../TERMS.md#hub) **`release-audit.py`** on your repo tree (compile + promotion bundle checks).

## Optional: custom fitness command

Create **`.nlc/verify-suite.json`**:

```json
{
  "schema": 1,
  "command": ["python3", "tools/my-adopter-fitness.py"],
  "cwd": "."
}
```

`verify-deep` runs this **before** `release-audit` when the file exists. Use the same command in CI as in `.github/workflows/nlc-verify.yml`.

## CI

`nlc-init` copies `github-workflows-nlc-verify.yml` → `.github/workflows/nlc-verify.yml`.

After first green deep [verify](../TERMS.md#verify) locally, commit **`.nlc/verified.json`** so PRs can run **`./nlc verify`** only.
