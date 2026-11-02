# Natural Language Compiler hub v0.4.1

## Highlights

Hub **v0.4.1** is a patch on **v0.4.0**. The `v0.4.0` tag stays on its peel. This line removes the owner signature from ordinary edits. The branch suite stays green without armor. One signature over the checker digest is required only at tag time, and only after this checker is on `main`.

- **The whole-tree digest is no longer an owner signature.** Ordinary edits refresh `integrity/hub-content-tree-hash.txt` without a new gate-set manifest signature. Record: `docs/rca/2026-10-25-signed-whole-tree-digest.md`.
- **One tag-time signature.** ADR 0057 (tag-time checker digest). The owner signs `integrity/checker-digest.sha256`. That file lists the checker programs, the fitness workflow, and the numbered decision records. `./nlc verify` checks the digest bytes and does not require the armor. `./release` refuses a later tag when `main`'s checker rejects the armor. This tag is the bootstrap: `main` does not yet contain that checker, so this tag adds no signature failure.
- **Per-file decision signatures are not a gate.** `adrs/*.md.asc` is not required for a green branch or a tag. ADR 0056 stays Proposed and is not the branch rule.
- **One regenerator.** `python3 tools/regen-derived-release-state.py` rewrites the digest, the gate-set manifest, mandated paths, the self-ref snapshot, install hashes, and the hub content-tree digest. Drift of those files is one check.
- **README product picture.** Generic intent and policies, and the same path with HIPAA and SEC named.
- **Effective decision for the release executor.** Record 0045 is unchanged. Record 0048 moves release policy to `goals/hub_release/execute.sh`. The view is `docs/nlc/effective-decisions.md`.

**Explicitly not in v0.4.1**

- v1.0.0 dogfood of this repo (brownfield install, full requirement import, trace graph, precise rewrite, policy in the generated code).
- A signature on this tag. The next tag after this checker is on `main` is the first one that requires it.
- A new compiled-system use-case wave. UC14 / UC16 / UC20 stay expansion-only.
- Moving or rewriting the `v0.4.0` tag.

## Changes since v0.4.0

- Notes are filled by the release tool after this file lands.
