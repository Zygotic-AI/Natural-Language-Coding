# History rewrite commit map (2026-10-10)

This file is **provenance only**. Gates and evidence do not read it (ADR 0050).

On 2026-10-10 the public hub history was rewritten (author mailmap / filter-repo). **Trees are byte-identical**; only commit ids changed.

## Known tip mapping

| Label | Before rewrite | After rewrite |
| --- | --- | --- |
| `release/v0.3.0` tip | `63c55dfa60d93bffd657ff3afc30576de9720acc` | `22486289f160e91ca9a42a84fad982ce382bc173` |
| `main` (same era) | `ddd99726c051e377d926ee26b0144ac8a449d91a` | (see current `main` on the remote) |

Release notes, closeout notes, and RCAs under `docs/rca/` may cite **old** ids on purpose. Do not edit those documents to chase new SHAs.

## Full old→new map

No `filter-repo/commit-map` artifact was checked in for this remediation. To regenerate a complete map from a pair of clones (original mirror and rewritten remote):

```bash
# On a machine that still has both histories:
git -C /path/to/original-repo log --format='%H' | while read old; do
  # Match by tree hash (content identity):
  tree=$(git -C /path/to/original-repo rev-parse "${old}^{tree}")
  new=$(git -C /path/to/rewritten-repo rev-list -n 1 "$tree" 2>/dev/null || true)
  printf '%s %s\n' "$old" "$new"
done > commit-map.txt
```

Install [`git-filter-repo`](https://github.com/newren/git-filter-repo) and use its emitted `commit-map` when the rewrite was performed with `--commit-callback` or mailmap export; that file is the authoritative bulk mapping.
