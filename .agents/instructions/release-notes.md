# [Hub](../../docs/TERMS.md#hub) release notes

Before a [hub](../../docs/TERMS.md#hub) [tag](../../docs/TERMS.md#tag) ships, **`docs/adoption/RELEASE-vX.Y.Z.md`** must exist on the merged release branch with a real **Highlights** section (not the HTML placeholder).

## Draft from last [tag](../../docs/TERMS.md#tag) to current

```bash
VER=0.2.0   # match integrity/nlc-version.json after bump
python3 tools/nlc_release_notes.py --write-draft --version "${VER}" --to HEAD
```

Replace the Highlights comment with adopter-facing summary. Refresh commit list only:

```bash
python3 tools/nlc_release_notes.py --refresh-changes --version "${VER}" --to HEAD
```

Validate:

```bash
python3 tools/nlc_release_notes.py --check --version "${VER}"
```

`./release` runs this flow after release class is chosen and **before** `verify-deep` ([ADR 0022](../../adrs/0022-hub-release-fail-early.md)). Changelog baseline is the **last shipped git [tag](../../docs/TERMS.md#tag)**, not `integrity/nlc-version.json`.
