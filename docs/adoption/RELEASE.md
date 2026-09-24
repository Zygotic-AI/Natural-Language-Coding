# Releasing the [NLC](../TERMS.md#nlc) [hub](../TERMS.md#hub)

**One entrypoint:** in the agent harness invoke **`/release`** ([`.agents/skills/release/SKILL.md`](../../.agents/skills/release/SKILL.md)) — readiness, open-work impact, inference, then **`./release`** from repo root when **Ship: GO**. Policy: [ADR 0039](../../adrs/0039-single-command-human-surfaces.md), [ADR 0040](../../adrs/0040-process-preflight-remediation.md).

Legacy **`./release prepare`** and **`./release finish`** forward into the same orchestrator; you do not need them.

## What `./release` does

Governed by **[ADR 0022](../../adrs/0022-hub-release-fail-early.md)** (gate order) and **ADR 0038–0040**.

1. **Resume** — if a `release/v*` branch is pushed or already merged, `./release` continues at the right phase (wait for merge, or tag).
2. **Preflight** — on `main`, `integrity/nlc-version.json` must match the last reachable **`v*.*.*` tag** (not ahead of what shipped).
3. **Shipped tag audit** — the newest reachable tag must pass the **tag gate** (static) on its commit; on failure the tool prints delete-or-retag commands (`tools/nlc_release_shipped_tag_audit.py`).
4. **Full NLC audit** — `python3 tools/full-nlc-audit.py --check --profile release-prep` (continuity manifest without duplicating `verify-deep`; ADR 0038). Prepare refuses if `FULL_NLC_AUDIT:NOT_MET`. For a local pre-ship sweep including `verify-deep` + `verify`, use `--profile full` (expect several minutes; use `--allow-dirty` only when intentionally auditing with local edits).
5. **Context** — lists `release/v*` candidates; warns if `main` has commits not in the release branch.
6. **Release class** — you choose patch / minor / major / keep (no default).
7. **Target preflight** — migration chain from last tag to target (`tools/nlc_release_target_preflight.py`).
8. **`verify-deep`** on `main` at the shipped version (before notes or bump).
9. **Release notes** — `docs/adoption/RELEASE-vX.Y.Z.md` with real **Highlights** (blocks until valid).
10. **`release/vX.Y.Z` branch** — version bump, second **`verify-deep`**, prep (`ci_fitness`, install hashes, smoke).
11. **`integrity/hub-release-record.json`** on the release commit (prepare receipt for the tag gate).
12. Push branch → PR link → **wait for merge** (Enter when merged).
13. **Tag gate** on the **merge commit** (`tools/nlc_release_tag_gate.py`: record, notes, migrations, `verify-deep`).
14. Annotated **tag** on that commit (not `main` HEAD if `main` moved on). Push tag → GitHub Actions publishes the tarball.

`--yes` auto-confirms routine prompts; it does **not** skip release notes, the tag gate, or **moving an existing tag** (use `NLC_RELEASE_ALLOW_RETAG=1` only when you intend to retag).

## Refusal output

When a step fails, the tool prints **`NOT_MET`**, what is wrong, and a **fix** (commands or next action). See [ADR 0018](../../adrs/0018-human-cli-interview-on-gap.md).

## Manual checks

```bash
python3 tools/nlc_release_target_preflight.py --check --target 0.2.1
python3 tools/nlc_release_tag_gate.py --check --commit <merge-sha> --tag v0.2.1
python3 tools/nlc_release_context.py --list-branches
python3 tools/nlc_release_shipped_tag_audit.py --check
```

## Release notes helper

```bash
python3 tools/nlc_release_notes.py --write-draft --version X.Y.Z --to HEAD
python3 tools/nlc_release_notes.py --check --version X.Y.Z
```

[Tag](../TERMS.md#tag) push runs [`.github/workflows/release.yml`](../../.github/workflows/release.yml) (fitness, verify, tag gate, smoke, tarball, GitHub Release body from the notes file).
