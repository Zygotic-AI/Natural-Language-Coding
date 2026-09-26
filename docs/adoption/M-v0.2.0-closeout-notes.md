# v0.2.0 closeout notes (plan block M)

**Recorded:** 2026-09-25 (Planit execute)

| Item | Value |
| ---- | ----- |
| `origin/main` HEAD | `023bad16c1ff` |
| Release merge commit (PR #54) | `ce7b3a6c1fd5` |
| Remote tag `v0.2.0` | `d853c4af277b` (not on merge commit) |
| Resume phase | `tag_ready` |
| Tag gate @ merge | **NOT_MET** — `verify-deep` / release signed at merge commit |

## Implication

- `./release --bump keep` tag leg targets merge **`ce7b3a6`**, not `main` HEAD.
- Remote **`v0.2.0`** already exists at a **different** commit than the merged release PR — resolve with retag policy (`NLC_RELEASE_ALLOW_RETAG=1`) or delete remote tag per `nlc_release_shipped_tag_audit.py` before re-tagging merge.
- Production-trunk work on `main` (**023bad1**) should ship on a **`release/v*`** line after **`main`** is reset to the canonical tag commit (ADR 0044).

## M3 stop predicate

Tag gate **MET** on **`ce7b3a6`** requires that commit to pass `verify-deep` (as CI would at tag time). Fixes belong **on `release/v0.2.0`** and a **new merge**, not only on post-merge `main`.

## Forward v0.2.1 (zero-parameter M-block)

Treat remote **`v0.2.0`** as shipped baseline. Do **not** re-fight `tag_ready` on `ce7b3a6` unless explicitly retagging.

| Step | Action |
| ---- | ------ |
| M1 | Commit trunk + zero-param release tooling on **any work branch** |
| M2 | **`./release`** → infer sets next semver + `release/v*` (e.g. **0.3.0** minor while ADR/policy tree changed; `RELEASE:INFER` banner) |
| M3 | Fix `RELEASE:NOT_MET` until branch pushed + PR merged |
| M4 | **`./release`** → tag leg → `RELEASE:TAG_PUSHED vX.Y.Z` |
| M5 | Reset **`main`** to remote tag commit; delete stale `release/v0.2.0` when resume `complete` |

Optional one-time tag leg for v0.2.0 mess (out of default path): resolve remote tag vs merge commit per shipped-tag audit, then **`./release`** on resume `tag_ready` only if policy requires closing v0.2.0 on merge commit.
