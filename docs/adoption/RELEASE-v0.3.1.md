# Natural Language Coding hub v0.3.1

## Highlights

Hub **v0.3.1** is a patch on **v0.3.0**. The git tag for v0.3.0 stays on the same peel. This tag ships the post-tag release-line work and the tag-publish path that v0.3.0 missed.

- **Clean GitHub merge is contained.** A merge commit whose tree matches the release tip is treated as contained, so `./release` can continue after GitHub merges `release/v*` into `main`.
- **Tag gate uses the tag commit's tools.** `verify-deep` on the tag worktree runs that commit's `tools/nlc.py`, not the agent's later worktree.
- **Tag CI fetches full history.** `.github/workflows/release.yml` checks out with `fetch-depth: 0`. The ADR 0039 binder refuses any fitness-suite workflow that stays shallow, so historic landmines and merge-base checks can resolve on tag push.
- **GitHub Release for an existing tag.** Publishing notes and the tarball uses the already-pushed tag. The tag is not moved.

**Explicitly not in v0.3.1**

- A new compiled-system use-case wave. UC14 / UC16 / UC20 stay expansion-only.
- Moving or rewriting the `v0.3.0` tag.

## Changes since v0.3.0

- Drop commit peel from FINDINGS last-pass line (`4f60e04`)
- Align release/v0.3.1 identity, notes, and record (`7b93b4b`)
- Require full-history checkout on release tag CI (`065b67c`)
- Add the owner-signed gate-set manifest sidecar (`0f7d896`)
- Refresh the content digest and unsigned gate-set manifest (`0a9bb47`)
- Run tag-commit verify-deep with that commit's tools (`a2adc77`)
- Treat a clean GitHub merge of the release tip as contained (`a0d598d`)

### Diff stat

```
.github/workflows/release.yml                      |  2 +-
 DESCRIBE.md                                        |  4 ++
 FINDINGS.md                                        |  2 +-
 TODO                                               | 11 +++++
 docs/adoption/RELEASE-v0.3.1.md                    | 38 ++++++++++++++++
 integrity/full-nlc-audit-inference-record.json     |  4 +-
 integrity/gate-set-baseline.manifest.sha256        | 10 ++---
 .../gate-set-baseline.manifest.sha256.approval.asc | 10 ++---
 integrity/hub-content-tree-hash.txt                |  2 +-
 integrity/hub-release-record.json                  |  4 +-
 integrity/nlc-version.json                         |  2 +-
 migrations/0.3.0_to_0.3.1/migration.yaml           |  3 ++
 .../assert_release_context_passes.py               | 51 ++++++++++++++++++++++
 .../fitness_adr_0039_release_binder.py             |  9 ++++
 .../nlc_release_context/nlc_release_context.py     | 26 ++++++-----
 .../nlc_release_tag_gate/nlc_release_tag_gate.py   |  3 +-
 16 files changed, 152 insertions(+), 29 deletions(-)
```

---

Draft commits/range from `python3 tools/nlc_release_notes.py --write-draft --version 0.3.1 --to HEAD`. Edit **Highlights** before merge; `./release finish` refuses to tag without them.
