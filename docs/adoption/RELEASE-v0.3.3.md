# Natural Language Coding hub v0.3.3

## Highlights

Hub **v0.3.3** is a patch on **v0.3.2**. The git tags for v0.3.0, v0.3.1, and v0.3.2 stay on the same peels.

- **Shipped notes do not look unfinished.** The notes helper no longer writes a “Draft commits/range…” footer. `python3 tools/nlc_release_notes.py --check` refuses that footer so a later ship cannot keep it. The v0.3.2 notes file in this tree is stripped the same way.
- **No frozen binding-matrix percentage in DESCRIBE.** The 40/78 (51.3%) line and the stale “38 unbound” lists are gone. Live status is `python3 tools/audit-binding-matrix.py`.
- **README Status history is labeled.** The current-ship line is unchanged. The v0.1.0 / v0.2 sentences are marked as history, not the current product state.
- **Closed `release/v*` branches pruned.** Tags and GitHub Releases for v0.3.0 / v0.3.1 / v0.3.2 stay. The live line is `release/v0.3.3`.
- **ADR 0051 merge-base is the immutable `v0.3.0` tag.** Produce and owner-key-trust no longer require `origin/release/v0.3.0`. The unresolved-merge-base landmine also hides that tag.

**Explicitly not in v0.3.3**

- README diagrams (left: generic intent/policies; right: healthcare HIPAA + SEC).
- A new compiled-system use-case wave. UC14 / UC16 / UC20 stay expansion-only.
- Moving or rewriting the `v0.3.0`, `v0.3.1`, or `v0.3.2` tags.

## Changes since v0.3.2

- Strip shipped-notes draft footer and stale binding-matrix percent (`1c5b50f`)

### Diff stat

```
 DESCRIBE.md                                 | 28 +---------------------------
 README.md                                   |  2 +-
 docs/adoption/RELEASE-v0.3.2.md             |  4 ----
 integrity/gate-set-baseline.manifest.sha256 | 14 +++++++-------
 integrity/hub-content-tree-hash.txt         |  2 +-
 tools/nlc_release_notes.py                  |  2 +-
 tools/nouns/release_notes/release_notes.py  | 15 ++++-----------
 7 files changed, 15 insertions(+), 52 deletions(-)
```
