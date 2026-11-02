# ADR 0057 — One tag-time signature over the checker digest

- Status: Proposed
- Date: 2026-10-31
- Deciders: Human manager
- Class: F (integrity / hub produce)
- Corpus: nlc
- Supersedes in part: [ADR 0056](0056-per-file-adr-detached-signatures.md) (per-file ADR signatures are not a branch or tag requirement)
- Amends: [ADR 0052](0052-owner-openpgp-ratification-amends-0051.md) (when the owner signature is required)
- Related: [ADR 0055](0055-staged-activation-of-gate-machinery.md)

## Context

The hub asked the owner to clearsign a 3,627-row gate-set manifest on every branch, and to detached-sign each Accepted architecture decision as well. Those decision records were already rows in the manifest, so each one was signed twice. ADR 0056, which requires the second signature, is still Proposed. A one-line instruction file was enough to void the manifest and turn the pull-request suite red.

The threat that remains is an agent editing the code that decides pass/fail and then reporting that the edit passed. One owner signature over those bytes, checked at tag time by the checker already on `main`, stops that. A pull request does not need the private key.

Version class of this change is **major**: it removes the per-file signature obligation and the mid-branch clearsign obligation.

## Decision

1. **Signed set.** The owner signs one document, `integrity/checker-digest.sha256`. Its bytes are the sha256 of a canonical listing of: checker programs (`tools/ci_fitness.py`, `tools/fitness-*.py`, `tools/assert-*.py`, and the checker nouns named in `tools/nouns/checker_digest/checker_digest.py`), `.github/workflows/fitness.yml`, and numbered records `adrs/NNNN-*.md`. Examples, generated ledgers, and instruction files are not in that listing. A listed path that is not a pass/fail input is a defect in the rule.

2. **Branch suite.** `./nlc verify` checks that the digest file matches the tree. It does not require `integrity/checker-digest.sha256.approval.asc`. It does not require `adrs/*.md.asc`. It does not require the gate-set manifest sidecar.

3. **Tag.** `./release` refuses to tag until the digest signature verifies. The verifier is the copy of `tools/check-checker-digest-signature.py` on `origin/main`, run against the commit being tagged. The commit's own copy of that script is not the verifier. Until `origin/main` contains that script, the tag gate does not add this requirement (first bootstrap: the signature already on `main`).

4. **One regenerator.** `python3 tools/regen-derived-release-state.py` rewrites the digest, the gate-set manifest, mandated paths, the self-ref snapshot, install hashes, and the hub content-tree digest. The suite reports drift of those files as one check, `fitness-derived-release-state`.

5. **Product ship.** `Released-by:` on `CONFIRM.md`, checked by `tools/release-audit.py`, is unchanged.

## Lifecycle (create, change, sign, ingest, rotate, first bootstrap)

### Create

The digest file is written by the regenerator. No signature is created by a tool.

### Change

A checker, workflow, or numbered decision-record edit changes the digest. The branch suite fails until the regenerator rewrites the digest file. The branch stays green with no armor.

### Sign

The owner clearsigns `integrity/checker-digest.sha256` with the pinned key. The statement's Content-SHA256 is the sha256 of that file.

### Ingest

The armor is `integrity/checker-digest.sha256.approval.asc`. The tag gate ingests it by running `main`'s checker. A legitimate change to the verifier must succeed through that path: editing the verifier on the branch stays machine-testable without a signature, and the tag refuses until `main`'s checker accepts the armor. The new verifier does not accept its own signature.

### Rotate

Key rotation stays ADR 0052 decision 3. After the new fingerprint is allowlisted on `main`, the owner re-signs the digest. A digest signed only by an unlisted key is NOT_MET.

### First bootstrap

`origin/main` does not yet contain `tools/check-checker-digest-signature.py`. The tag gate adds no digest-signature problem until that file is on `main`. The signature already on `main` is the bootstrap anchor.

## Consequences

- Per-file `adrs/*.md.asc` files may remain in history. The suite does not read them.
- The gate-set manifest remains a machine membership list. Its sidecar is not a branch gate.
- The next hub ship that tags this rule is a **major** version.

## Rejected

- Keeping a per-file detached signature for every Accepted decision record.
- Requiring the owner signature before a pull request can be green.
- Letting the commit being tagged run its own signature check.

## Related

- [ADR 0052](0052-owner-openpgp-ratification-amends-0051.md)
- [ADR 0055](0055-staged-activation-of-gate-machinery.md)
- [ADR 0056](0056-per-file-adr-detached-signatures.md)
