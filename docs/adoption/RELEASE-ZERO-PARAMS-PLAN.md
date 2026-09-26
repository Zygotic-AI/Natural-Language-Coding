# Zero-parameter hub release (executed)

**Outcome:** Human runs only **`./release`** from whatever branch they worked on; [`tools/nlc_release_infer.py`](../../tools/nlc_release_infer.py) infers version + `release/v*`, runs gates, prints **`RELEASE:NOT_MET`** with **Re-run: `./release`**, or completes through tag push.

## Implemented

| Piece | Location |
| ----- | -------- |
| Infer API | [`tools/nouns/release_infer/`](../../tools/nouns/release_infer/), [`tools/nlc_release_infer.py`](../../tools/nlc_release_infer.py) |
| Orchestrator | [`scripts/nlc-release.sh`](../../scripts/nlc-release.sh) — `apply_release_infer`, no required `--bump` |
| Remediation | [`tools/nlc_release_remediate.py`](../../tools/nlc_release_remediate.py) — Re-run `./release` only |
| Landmine | [`tools/assert-release-infer-passes.py`](../../tools/assert-release-infer-passes.py) |
| Docs | [`RELEASE.md`](RELEASE.md) seven-step hero; flags in appendix |
| ADRs | [0044](../../adrs/0044-hub-release-production-trunk.md), [0039](../../adrs/0039-single-command-human-surfaces.md) |

## Infer rules (ordered)

1. Resume `tag_ready` / `await_merge` / `complete` — no bump inference.
2. On `release/v*` — stay; align version file in prepare gates.
3. On `main` — purity NOT_MET or “no work” → block with remediation (no `--bump` quiz).
4. Any other branch — `suggest_bump` + shipped tag → `release/v{target}`; create or merge into release line.

## Prove

```bash
python3 tools/fitness-adr-0039-release-binder.py
python3 tools/assert-release-infer-passes.py
./release --dry-run   # from work branch or release/v*
```
