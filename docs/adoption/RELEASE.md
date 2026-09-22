# Releasing the [NLC](../TERMS.md#nlc) [hub](../TERMS.md#hub)

From repo root:

```bash
./release                 # default: one session (branch → PR → wait → tag)
./release prepare         # two-step: push branch, stop
./release finish          # two-step: after merge, on main
```

## Single session (default)

Governed by **[ADR 0022](../adrs/0022-hub-release-fail-early.md)** (fail-early order).

1. **Preflight** — on `main`, `integrity/nlc-version.json` must match the last **`v*.*.*` [tag](../TERMS.md#tag)** (not ahead of what shipped).
2. Choose release class (no default) → **target preflight** (`tools/nlc_release_target_preflight.py`: migration chain from last tag to target; optional noop scaffold).
3. **`verify-deep`** on `main` at the shipped version (fail before notes or bump).
4. **Release notes** for the target version (draft from **last shipped git tag** → `HEAD`; fill **Highlights** before version write).
5. Check out **`release/vX.Y.Z`**, write `nlc-version.json` (full migration chain on disk), **`verify-deep`** again, prep; commit (notes file must be on the release commit) and push the release branch.
6. Prints a **compare/PR link** (and `gh pr create` if installed).
7. You open/merge the PR; **press Enter** when merged.
8. Resolves the **PR merge commit** on `main` (via `gh` or git ancestry — **not** `main` HEAD if something else landed after merge), runs **`verify`** on that commit, tags **`vX.Y.Z`** there, pushes the [tag](../TERMS.md#tag).

Manual target check:

```bash
python3 tools/nlc_release_target_preflight.py --check --target 0.2.0
python3 tools/nlc_release_target_preflight.py --ensure-noop --target 0.2.0
```

Use **Ctrl-C** after the push if you cannot merge immediately; resume with **`./release finish`**.

`--yes` auto-confirms prompts; it does **not** skip the Enter wait after the PR (by design).

## Two-step

**`./release prepare`** (or **`./release --two-step`**) — same branch push as above, then exit with PR instructions.

**`./release finish`** — on `main` after merge: `verify`, [tag](../TERMS.md#tag), push [tag](../TERMS.md#tag).

## Release notes (required)

- Path: `docs/adoption/RELEASE-vX.Y.Z.md` (committed on the release branch).
- `./release` creates a draft if missing (`tools/nlc_release_notes.py`) from the **previous reachable git [tag](../TERMS.md#tag)** (`v*.*.*`, not `integrity/nlc-version.json`) to `HEAD`, lists commits and a diff stat, and **blocks** until **Highlights** is a real summary (`--yes` does not skip this).
- **Suggested bump** is a heuristic from your working-tree diff (policy paths only for major); it is not a default choice and is often **patch** for tooling/docs work.
- `./release finish` and the [tag](../TERMS.md#tag) [workflow](../../.github/workflows/release.yml) [refuse](../TERMS.md#refuse) to [ship](../TERMS.md#ship) without that file and Highlights.

Manual draft (e.g. for an agent or second terminal):

```bash
python3 tools/nlc_release_notes.py --print-draft --version 0.2.0 --to HEAD
python3 tools/nlc_release_notes.py --write-draft --version 0.2.0 --to HEAD
# edit docs/adoption/RELEASE-v0.2.0.md — replace Highlights placeholder
python3 tools/nlc_release_notes.py --check --version 0.2.0
```

## Options

```bash
./release --help
./release --bump minor --yes
./release prepare --no-push
```

[Tag](../TERMS.md#tag) push triggers [`.github/workflows/release.yml`](../../.github/workflows/release.yml).

**Squash-merge PRs:** install [`gh`](https://cli.github.com/) so the script can read `mergeCommit` from GitHub; the git-only fallback needs a merge commit that still contains the branch tip in history.
