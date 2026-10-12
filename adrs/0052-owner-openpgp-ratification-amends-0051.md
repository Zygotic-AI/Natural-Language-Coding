# ADR 0052 — Owner OpenPGP ratification (amends 0051)

- Status: Accepted
- Date: 2026-10-11
- Deciders: Human manager
- Class: F (integrity / hub produce)
- Corpus: nlc
- Amends: [ADR 0051](0051-hub-own-produce-principles.md) (SG2 ratification model and ADR 0047 receipt replacement when wired)
- Supersedes in part: hash-only receipt semantics in [ADR 0047](0047-adr-approval-receipts.md) and gate-set receipt rows in ADR 0051 SG2 — **when codified constraints land** (step 2); ADR 0051 file text is unchanged.

## Context

RCA 5, root confirmed and remediation plan approved by the human manager 2026-10-11 (the RCA record is kept outside this repository): the two-actor principle (human manager ratifies, agents produce) was not carried into approval controls. Hash-only registries let producers rewrite stamps without the owner's act.

This record **amends policy** in ADR 0051: ratification is the human manager's **clearsigned approval statement** only. Private key stays on the owner's phone (PGPony). Agents commit pasted armor **unchanged**; they never create ratification.

Bootstrap trust anchor: Ed25519 public key `Richard Pickett <Richard@RichardPickett.com>`, fingerprint **`9D1BD57770FC3A1DE84702750AFD22B063AE01BC`**, committed under `integrity/owner-keys/` with `integrity/owner-keys/TRUSTED_FINGERPRINTS`.

## Approval statement format (zyprompt-compatible)

Each ratification uses a **plain-text statement** (clearsigned in PGPony), with these fields:

```text
Repo: <org>/<repo>
Document: <repo-relative path>
Content-SHA256: <SHA-256 hex of document bytes exactly as committed>
Decision: <must match document Status line, e.g. Accepted>
Date: <YYYY-MM-DD>
Summary: <one line>
```

The signed artifact is committed **unchanged** beside the document:

```text
<document-path>.approval.asc
```

Example: `adrs/0052-owner-openpgp-ratification-amends-0051.approval.asc` next to this file.

**Zyprompt consistency:** The document **Status** line is **Accepted** before merge. CI (step 2) will **NOT_MET** any `Status: Accepted` document lacking a valid sidecar whose **Decision** matches **Status** and whose **Content-SHA256** matches the file. Until the owner pastes the sidecar, the PR stays unmergeable under that gate.

## Decision

1. **Ratification SSOT:** Only the owner's clearsigned approval statement (format above) counts as ratification. No JSON hash row, registry field, or tool output substitutes.

2. **Pinned key:** Fingerprint `9D1BD57770FC3A1DE84702750AFD22B063AE01BC` is the in-force owner ratification key at adoption. Public key material lives in `integrity/owner-keys/richard-pickett.asc`; allowlist in `integrity/owner-keys/TRUSTED_FINGERPRINTS`.

3. **Key rotation / add:** A new fingerprint may enter `TRUSTED_FINGERPRINTS` only with a committed clearsigned statement **from a currently pinned key** authorizing the change, plus updated `.asc` if needed.

4. **Stamp / fitness (completion confirmation only):** After step-2 wiring, checks verify: (a) valid clearsignature from a pinned fingerprint; (b) **Content-SHA256** in the statement matches the document (or manifest) bytes in the tree; (c) **Decision** matches the document **Status**. Unsigned, wrong key, hash mismatch, tampered manifest, or **pending** → **NOT_MET**. **No tool may write a ratified entry.**

5. **Replace hash-only receipts:** Supersedes ADR 0047 hash-only JSON and ADR 0051 SG2 hash-only gate-set receipts **when implemented** — same OpenPGP sidecar model for ADR files and gate-set batches (manifest + single-line signature when many paths).

6. **PM independent verify:** At each review and release, the PM re-verifies signatures with an **out-of-repo copy** of the owner public key (not only CI), before treating ratification as real.

7. **Verifier implementation (step 2, not this PR):** Python-first hub verifier, self-contained: import key from `integrity/owner-keys/`, pin against `TRUSTED_FINGERPRINTS`, verify sidecars via **GnuPG** (`gpg --verify`) or **Sequoia** (`sqv`); choose simplest dependable option in implementation PR.

8. **Bootstrap:** First in-force ratification under this ADR is the owner's clearsigned statement for **this document** at PR head bytes, committed as this file's `.approval.asc`.

## Consequences

- ADR 0051 remains Accepted; its ratified text and existing stamps are untouched.
- Version class **minor** when fully wired.
- Step 1 (this ADR + keys only): no fitness or receipt changes until owner signs and step 2 lands.

## Rejected

- Hash-only approval receipts as ratification evidence.
- Producer or maintainer tools that set ratified/pending registry state without a sidecar.
- Any retired or unpinned key fingerprint in `TRUSTED_FINGERPRINTS`.

## Related

- [ADR 0051](0051-hub-own-produce-principles.md) — hub-own produce (amended in force by this record)
- [ADR 0047](0047-adr-approval-receipts.md) — prior hash receipt model (superseded when wired)
- RCA 5 — kept outside this repository.
