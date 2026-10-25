# ADR 0055 — Staged activation of gate machinery

- Status: Proposed
- Date: 2026-10-25
- Deciders: Human manager
- Class: F (integrity / hub produce)
- Corpus: nlc
- Related: [ADR 0046](0046-repository-planit-identity.md) (repository Planit identity), [ADR 0051](0051-hub-own-produce-principles.md) (hub-own produce), [ADR 0052](0052-owner-openpgp-ratification-amends-0051.md) (owner OpenPGP ratification), [ADR 0054](0054-published-skill-author-contract.md) (published-skill author contract)

## Context

The 2026-10-25 unregistered Planit skill land showed four stacked failures: Skill produce treated one author checklist as done; owner-signature and identity mandates were after-the-fact detectors; the live gating skill was both the mandated artifact and the machinery that must load to ingest a signature; and signing design never required a create–change–sign–ingest–rotate walkthrough or a known-bad of a legitimate verifier change.

Owner-approved remediation (2026-10-24 / 2026-10-25): members of the self-referential set change only through a staging area. The live signed machinery verifies the staged candidate and the owner's signature. One activation commit moves staged bytes into live paths together with the regenerated registry, install hashes, manifest, and the owner's sidecar — or nothing lands.

## Decision

1. **Derived self-referential set.** Membership is computed by `python3 tools/derive-self-ref-set.py` from role detectors (gating skills, owner hook, identity tool and registry, gate-set membership derivation, manifest generator, sidecar verifier, C8, owner keys, install hashes, and the staging/activation tools themselves). The list is not hand-kept. Snapshot: `integrity/self-ref-set.json`.

2. **Staging area.** Candidates live under `staging/<change-id>/` mirroring live paths. That prefix is excluded from `derive_gate_set_paths`. Staging is a candidate, not a loadable Planit skill.

3. **Live verifier stays live.** The previously signed live `/planit`, hook, identity tool, sidecar verifier, and owner keys verify the staged candidate and the pasted owner armor. The staged skill is never loaded as `/planit`.

4. **Atomic activate.** `python3 tools/activate-gate-machinery.py --change-id <id> --armor <pasted-file>` verifies the pasted armor with the live verifier against the pinned key, places the armor file unchanged, then swaps staged bytes into live paths together with the regenerated Planit registry (from bytes), install hashes, and the exact proposed manifest the owner signed. It never creates a signature. Bytes without a valid sidecar refuse and leave live untouched.

5. **Live-member refuse.** Any change to a live self-ref member outside an activation commit is refused at produce time and by `python3 tools/fitness-live-self-ref-activation.py`. The first land of this machinery is the **bootstrap** activation (this record + tools + regenerated pins). After those tools exist on the base, bootstrap is not available.

6. **Mandate inheritance.** `python3 tools/derive-mandated-paths.py` is the one derived list of mandated paths. The Skill type recipe, the skill-author checklist (`mandate-pins`), and `/release` import it. Touching a listed path without moving its pins in the same change is a produce-time refuse. A regenerated-but-unsigned manifest is **INCOMPLETE** produce, not a finished step.

7. **Control-design process.** Planit and the briefing standard require, for any control or gate design, a full lifecycle walkthrough and a known-bad of **legitimate change to the verifier** that must succeed through staging. Those are checked rules (`CONTROL-LIFECYCLE`), not prose only.

## Lifecycle walkthrough (create, change, sign, ingest, rotate, first bootstrap)

### Create (new self-ref member)

1. Author candidate bytes under `staging/<change-id>/` mirroring the intended live path (`python3 tools/stage-gate-machinery.py --change-id <id> --path <live-rel>` then edit the staged copy).
2. Live `/planit` still matches the registry. Owner prompts and Planit intake pass.
3. Live generator computes the proposed gate-set manifest with staged overrides. Do not mark produce done.
4. Owner clearsigns the proposed manifest offline (ADR 0052). Agents never create ratification (C8).
5. Activate: live verifier checks the pasted armor against proposed bytes and the pinned key; one commit swaps bytes + registry + install hashes + manifest + sidecar.
6. After that commit the hook, Planit identity, install-verify, and sidecar P1 go green together.

### Change (existing live member)

Same as create, except stage copies the current live file first. Editing the live path directly is a produce-time and fitness refuse.

### Sign

Owner signs the **proposed** manifest (Document `integrity/gate-set-baseline.manifest.sha256`, Content-SHA256 of proposed bytes) with the pinned key on an offline device. Signing does not need `/planit`. The live identity pin still matches, so the owner can submit a prompt asking the agent to wait for armor.

### Ingest

The activate tool is the ingest path. It verifies pasted armor with the **live** sidecar verifier, writes that armor unchanged, then swaps. There is no unsigned-then-sign playbook on live verifier paths. A split land (bytes, then sidecar later) is refused.

### Rotate (owner key)

Key rotation stays ADR 0052 decision 3: a currently pinned key authorizes a new fingerprint. The key material and `TRUSTED_FINGERPRINTS` are self-ref members. Stage the key change, have the **currently pinned** key sign the proposed manifest, then activate. A manifest signed only by the new unlisted key is NOT_MET.

### First bootstrap (this activation)

The staging prefix, activate tool, derived-set generator, mandate list, and this record cannot be staged by machinery that does not yet exist. The first land is a one-time owner-attended bootstrap: this tree introduces the tools, keeps the nine published `SKILL.md` files, regenerates the Planit registry and install hashes **from bytes**, regenerates the gate-set manifest, and waits on the owner signing statement at `adrs/owner-approvals/staged-signing.statement.txt` for this ADR and that manifest. That unsigned statement is excluded from gate-set derivation, the hub content-tree digest, and verify fingerprints (same class as the manifest sidecar) so it can name the manifest digest without a cycle. After those tools exist on the release-line base, further self-ref edits use staging + activate only.

## Consequences

- Version class **minor** (new produce contract and control-design rules on the 0.4.0 line).
- C8 is unchanged: no tracked tool writes a created `*.approval.asc`; activate only places owner-pasted armor.
- The live Planit registry is generated from skill bytes. Hand-bumping the registry to pass the hook is refused.
- Owner-signature fitness rows stay red until the owner clearsigns the bootstrap statement.

## Rejected

- Bumping the live Planit registry so the hook passes, then signing later (RCA 5 / ADR 0052).
- Disabling or bypassing the identity hook to deliver a sidecar (ADR 0046).
- Unsigned-then-sign on live verifier paths as a complete produce.
- A second loadable Planit skill name for staging.
- Hand-kept self-ref or mandated-path lists.

## Related

- RCA 2026-10-25 unregistered Planit skill edit (Climbs 1–4), kept on `rca/planit-unregistered-skill-edit`.
