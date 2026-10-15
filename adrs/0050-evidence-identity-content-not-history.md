# ADR 0050 — Evidence identity: content, not history

- Status: Accepted
- Date: 2026-10-10
- Deciders: Human manager
- Ratified-by: Human manager (evidence identity content-not-history ADR, 2026-10-10)
- Class: F (integrity / gates), A (release and audit evidence)
- Corpus: nlc
- RCA: docs/rca/2026-10-10-sha-pinned-evidence-history-rewrite.md (instance record; analysis in operator packet)

## Context

Hub proof mixed two evidence regimes: content fingerprints (for example `.nlc/verified.json`, release `effective_tree_sha`) and git commit ids (`last_pass_sha`, `audit_sha`, landmine `BAD_COMMIT`, `prepare_head`). An unstated assumption treated history as immutable and complete. When history was rewritten with identical trees, gates that depended on commit ids changed verdict without any content change. Earlier shallow-clone failures were fixed by requiring full clones instead of changing what evidence binds to.

[`MANIFESTO.md`](../MANIFESTO.md) states that code is not the product — intent and emitted content are. [ADR 0007](0007-tags-primitives-reduced-adrs.md) requires naming facts the factory relies on. [`integrity/ACTIONS.md`](../integrity/ACTIONS.md) requires **REFUSE** when a check cannot run, not a substantive finding on unread input.

## Named facts

1. **History may change.** Rewrites, shallow clones, and mirrors can change commit ids while preserving tree content.
2. **A verdict is a pure function of (tree under test, gate set).** No gate outcome may depend on git history identity, clone depth, remote layout, or machine state unless that input is declared in the gate set and recorded in the receipt.
3. **Labels resolve at check time.** Tags, semver strings, and branch names are human labels resolved when the gate runs; they are not stored as proof handles.

## Decision

1. **Evidence binds to content.** Evidence records and fixtures name what was checked: git tree hash (40 hex), blob or path content digests, gate-set hash, and hub version — never a commit id as proof.
2. **Unresolvable input → REFUSE.** When a gate cannot resolve a declared reference (missing object, dangling label), it stops with **REFUSE** and prints the unresolved reference. It does not emit NOT_MET/FAIL for a different substantive reason.
3. **Freshness is content freshness.** “Fresh” means the recorded content hash equals the current content hash of the audited paths, not “an ancestor of HEAD”.
4. **Landmines are self-contained.** Designed-fail fixtures build the world they test (synthetic repository or tree) and assert the specific failure token. Passing for any other reason is a defect.
5. **Enforcement.** Hub CI runs: `fitness-no-history-ids-in-evidence`, `fitness-landmine-self-contained`, `assert-unresolvable-refuses-passes`, and a history-rewrite invariant job that must yield the same fitness verdict before and after rewriting a scratch copy (including shallow clone).

## Consequences

- Evidence JSON schemas and FINDINGS headers use `*_tree_hash` (or path digests), not `*_sha` commit fields.
- Release prepare receipts cite `integrity/hub-content-tree-hash.txt`, not `prepare_head`.
- `fetch-depth: 0` is no longer required to keep SHA-pinned landmines green; shallow clones must MET when content is unchanged.
- Provenance under `docs/history/` and `docs/rca/` may retain historical commit citations; operational gates do not read them.

## Rejected

- **Environment-only fix (full clone forever):** repeats the 2026-09-25 accommodation; does not name the assumption ([`MANIFESTO.md`](../MANIFESTO.md) climb-upstream rule).
- **Dual commit + tree fields:** forks evidence identity; rewrite still leaves commit field false.
- **Optional migration window for commit ids in gates:** would leave two truths on identical trees.

## Related

- [ADR 0005](0005-ssot-exit-evidence.md) — produce package evidence (abstract fields)
- [ADR 0007](0007-tags-primitives-reduced-adrs.md) — name the facts you rely on
- [ADR 0039](0039-single-command-human-surfaces.md) — release binder (amended: landmines synthetic, not SHA-pinned)
- [ADR 0040](0040-process-preflight-remediation.md) — shipped tag audit REFUSE semantics
- [`tools/nouns/evidence_ref/`](../tools/nouns/evidence_ref/) — resolver and tree hashing SSOT
