# ADR 0056 — Per-file detached owner signatures for ADRs

- Status: Proposed
- Date: 2026-10-25
- Deciders: Human manager
- Class: F (integrity / hub produce)
- Corpus: nlc
- Amends: [ADR 0052](0052-owner-openpgp-ratification-amends-0051.md) (ADR-file ratification shape only)
- Related: [ADR 0055](0055-staged-activation-of-gate-machinery.md) (staged activation of gate machinery)

## Context

The 2026-10-13 owner act ratified 47 Accepted ADRs in one clearsigned statement that listed each path and its sha256. That batch lived under `adrs/owner-approvals/` and was accepted by `fitness-adr-owner-sidecar` when a per-file sidecar was absent. Editing one Accepted ADR voided only that hash line, but the ratification object was still a single batch statement.

The gate-set baseline manifest already uses a different, correct shape: one owner signature over one document (the manifest). That model stays.

## Decision

1. **One detached signature per ADR file.** An Accepted numbered ADR is ratified only by a valid OpenPGP detached signature from the pinned owner key `9D1BD57770FC3A1DE84702750AFD22B063AE01BC` (Ed25519) over the exact current bytes of that ADR file. Sibling convention: `adrs/NNNN-slug.md` → `adrs/NNNN-slug.md.asc`.

2. **Batch statements do not cover ADRs.** A clearsigned batch under `adrs/owner-approvals/` (or anywhere else) is not ratification for an ADR, even when it lists the path and a matching sha256.

3. **Gate-set manifest stays single-signed.** `integrity/gate-set-baseline.manifest.sha256` keeps the existing clearsigned sidecar model (one signature over the manifest). ADR 0052 / ADR 0055 occupancy paths for that sidecar are unchanged.

4. **Owner script, not a tool-written signature.** The owner runs `scripts/sign-adrs.sh` locally (once for catch-up, then per release). The script signs only missing or stale ADR files, is idempotent, supports `--dry-run`, refuses when the key is not in the local keyring, and never stores a passphrase. The passphrase is prompted at most once: an upfront unlock (throwaway detach-sign to `/dev/null`) lets gpg-agent cache it for `default-cache-ttl` (GnuPG default 600 seconds). After that, each ADR sign uses `--pinentry-mode error` and refuses if a prompt would recur. Optional `NLC_SIGN_ADRS_PINENTRY_LOOPBACK=1` selects loopback pinentry for the unlock only. A `--test-fingerprint` override exists for automated tests only and requires `--allow-test-key`. Agents do not create ratification (C8).

5. **Staged activation.** Changing the live sidecar verifier (`tools/nouns/owner_sidecar/owner_sidecar.py`) follows ADR 0055: stage the candidate, regenerate the gate-set manifest, do not sign. Owner catch-up signs ADR files and then clearsigns the regenerated manifest statement.

## Lifecycle walkthrough (create, change, sign, ingest, rotate, first catch-up)

### First catch-up (this change)

1. Land the check, the script, the Proposed ADR, and the staged verifier candidate.
2. Owner checks out the branch and runs `scripts/sign-adrs.sh` (one passphrase prompt at unlock; gpg-agent `default-cache-ttl` covers the rest of the run).
3. Owner commits the new `*.md.asc` files and pushes.
4. Owner clearsigns the regenerated gate-set manifest statement (one document, unchanged model) and pastes the armor. Agents never create that signature.

### Create (new ADR in a later release)

1. Author `adrs/NNNN-slug.md` with Status Proposed. No signature is required.
2. When the record is Accepted, the owner runs `scripts/sign-adrs.sh`. The script signs only the new or stale file.
3. Commit the sibling `adrs/NNNN-slug.md.asc`.

### Change (edit an Accepted ADR)

1. Edit the ADR bytes. The existing `.md.asc` no longer verifies.
2. Fitness is NOT_MET until the owner re-runs `scripts/sign-adrs.sh` (it re-signs only the stale file).
3. Commit the refreshed `.md.asc`.

### Sign

Owner signs on a machine that holds the pinned private key. The script calls `gpg --local-user <pin> --detach-sign --armor`. Signing does not need `/planit`.

### Ingest

The committed `.md.asc` is the ingested artifact. Fitness verifies it against current ADR bytes and the pinned key. There is no batch ingest path.

### Rotate (owner key)

Key rotation stays ADR 0052 decision 3: a currently pinned key authorizes a new fingerprint. After the new key is allowlisted, the owner re-runs `scripts/sign-adrs.sh` so each Accepted ADR carries a detached signature from the in-force pin. The gate-set manifest is re-signed as one document under the unchanged sidecar model.

## Consequences

- Version class **minor** (ratification policy for ADR files on the 0.4.0 line).
- C8 is unchanged: no tracked Python tool writes created ratification armor. The bash script is owner-run.
- CI stays red on missing owner signatures until the owner runs the script and signs the regenerated manifest.
- `integrity/hub-content-tree-hash.txt` being in the gate set is a known open defect (PR #30). An ordinary doc-only PR after activation still changes that digest member, so the signed manifest is voided and the owner must re-sign the manifest. This record does not fix that defect.

## Rejected

- Keeping the 47-ADR batch statement as a covering ratification object.
- Clearsigned per-ADR approval statements (`*.approval.asc` with Content-SHA256 fields) as the in-force ADR model. Detached signatures over exact current bytes replace that for numbered ADRs.
- Changing the gate-set manifest to a per-member signature set.

## Related

- [ADR 0052](0052-owner-openpgp-ratification-amends-0051.md) — owner OpenPGP ratification (amended here for ADR files only)
- [ADR 0055](0055-staged-activation-of-gate-machinery.md) — staged activation of gate machinery
