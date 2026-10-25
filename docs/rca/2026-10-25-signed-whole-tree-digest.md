# RCA: Whole-tree digest is a signed gate-set member, so any tracked edit needs an owner signature

**Date:** 2026-10-25  
**Context:** Natural-Language-Coding hub — `release/v0.4.0` at `bfe327c` (PR #29 merge)  
**Status:** open (analysis only; no remediation in this record)

**Scope (user words):**

- “ANALYSIS ONLY: write an RCA doc on a new branch and open a draft PR; change no other file.”
- “PR #28 adds only `docs/rca/2026-10-25-planit-unregistered-skill-edit.md` (not a gate-set member per derive tooling). CI `hub-content-tree-fresh` fails because `integrity/hub-content-tree-hash.txt` digests every tracked file. That hash file is itself listed in the owner-signed `integrity/gate-set-baseline.manifest.sha256` … So syncing it changes the signed manifest, meaning ANY repo edit, even a doc, requires a new owner signature.”
- “Find: (1) the defective product (which design ties a whole-tree digest into the signed set); (2) the process that produced it, climbing until the root is a process/principle gap, not a file.”
- “Check whether ADR 0055's lifecycle walkthrough … covered 'ordinary non-gate change after activation'; whether PR #29's finish line or Helix's brief should have caught it; and the relation to the earlier cycle fix that excluded approval armor from the digest.”
- “Enumerate every other signed or digest artifact with the same property, derived from code, not by hand.”
- “Offer remediation options with tradeoffs, each with a lifecycle walkthrough and the known-bad case 'a doc-only PR must go green with no owner signature while a gate-set edit still requires one'. Do not implement.”

**Resolution table (this record):**

| Criterion | This record |
| --------- | ----------- |
| Scope (user words) | Quoted above; outcome is this RCA + draft PR only |
| No narrowing | Product, process climb, ADR 0055 check, PR #29 / Helix, cycle-fix relation, derived list, options — all present |
| Question vs implement | Analysis only; no product, process, or hash-file change |
| Their vocabulary | Defective product, climb, ordinary non-gate change after activation, finish line, Helix's brief, cycle fix, signed or digest artifact, known-bad as given |
| Version class | Patch (instance record only) |

---

## 1. Error condition

**Observed (bounded, reproducible) at `bfe327c`:**

1. PR #28 adds only `docs/rca/2026-10-25-planit-unregistered-skill-edit.md`.
2. `python3 tools/derive-gate-set-closure-reference.py .` / `is_gate_set_path` = False for that path. `docs/rca/` is a documented exclusion in `GATE_SET_EXCLUSIONS` (`tools/nouns/gate_set/gate_set.py`): provenance, never a pass/fail grading input (ADR 0051 table).
3. CI `hub-content-tree-fresh` (releasable verify profile → `tools/fitness-findings-last-pass-fresh.py`) is NOT_MET: recorded `integrity/hub-content-tree-hash.txt` ≠ `content_digest_excluding` over `git ls-files` minus a small exclude set.
4. That hash file is a member of the owner-signed gate-set manifest `integrity/gate-set-baseline.manifest.sha256` (line 732 at `bfe327c`: `integrity/hub-content-tree-hash.txt c62e96ee…`). Membership equals `derive_gate_set_paths` (3812 paths; path column == derive).
5. Syncing the hash (`python3 tools/sync-hub-content-tree-hash.py`) changes a signed member. `fitness-gate-set-manifest` then requires remanifest + a new owner sidecar. C8 forbids tools writing `*.approval.asc`. The owner must clearsign again.

**This climb’s error condition:** after the signed set is activated, an ordinary non-gate change cannot complete produce without a new owner signature.

**Not the error condition:** PR #28’s Climbs 1–4 (unregistered Planit skill, mandate-as-detector, bootstrap deadlock, signing design that missed verifier-update). Those are recorded on `rca/planit-unregistered-skill-edit`. This record is the next climb: the activated signed set plus a whole-tree digest.

---

## 2. Defective product

The design that ties a **whole-tree digest** into the **owner-signed set** is the conjunction of three accepted decisions, not a stray path:

| Decision | What it did | Path |
| -------- | ----------- | ---- |
| ADR 0050 (evidence identity: content, not history) | Freshness is “recorded content hash equals current content hash of the audited paths.” The hub stamp is `integrity/hub-content-tree-hash.txt`. Coverage is `git ls-files` minus a cycle-break exclude set (`tools/nouns/evidence_ref/sync_content_tree_hash.py`). | Whole tree is the audited object |
| ADR 0051 SG2 / ADR 0052 | Gate-set member bytes are ratified. Membership is the transitive **CI load closure** (`derive_gate_set_paths`), never a hand-kept list. Owner OpenPGP sidecar is the receipt. | Whatever CI loads is signed |
| Releasable profile | `integrity/releasable-gates.json` puts `hub-content-tree-fresh` on both `verify` and `release`. That gate loads the hash file. Closure therefore includes the hash file. | The digest artifact becomes a signed member |

**Mechanism:**

- Non-member edit (any tracked path not in `_content_exclude_rel()`) → digest changes → hash file must move → hash file is in S → manifest bytes change → owner sidecar is stale → produce is INCOMPLETE without a new signature.
- At `bfe327c`, 77 tracked paths sit in the hub digest and **not** in S (derived below). Every one of them has this property. `docs/rca/*` is 18 of those 77.

**What the hash file is not:** it is not a self-ref member (`integrity/self-ref-set.json` has 29 paths; the hash file is absent). ADR 0055 staging therefore does not apply to it. Live-self-ref refuse does not fire when it is synced. Mandate inheritance pins it as `content_tree` (`tools/nouns/mandated_paths/mandated_paths.py`) but does not require a sidecar on the hash file itself — the sidecar sits on the manifest that *lists* it.

---

## 3. Upstream chain (process before output)

| Step | Artifact / layer | What it did |
| ---- | ---------------- | ----------- |
| (symptom) | PR #28 + `hub-content-tree-fresh` | One RCA file, not a gate-set member, red CI; syncing the hash demands a new owner signature |
| 7 | Activated signed set (PR #29 / `bfe327c`) | Owner sidecar on the 3812-member manifest, including the hash file. Routine work now hits a live ratification gate |
| 6 | ADR 0055 lifecycle + CONTROL-LIFECYCLE | Walks create / change / sign / ingest / rotate / first bootstrap for **self-ref members**. Known-bad is **legitimate change to the verifier** through staging. “Change” = existing live member. No row for ordinary non-gate change after activation |
| 5 | PR #29 finish line and the owner-approved remediation brief | Finish-line proofs: derived self-ref print; live-member edit REFUSE; verifier change via staging + test-only key; split-land REFUSE; mandate-without-registry REFUSE; signing-order dry-run; one owner statement; CI green except sidecar rows. No proof that a doc-only PR stays green without a new signature |
| 4 | Cycle fix (armor / statement excluded from digest) | `241e3ec` (“exclude manifest approval.asc from closure and hub digest”), `9030b16` (restore exclude set; hash cycle), occupancy extension in PR #29 (batch armor + unsigned statement). Known-bad: placing armor must not change hub digest or closure. Solved **signing-order cycle**, not **non-member → remanifest amplification** |
| 3 | ADR 0050 + 0051 composed | Whole-tree freshness stamp became a CI-loaded path, therefore a signed member. No brief asked whether provenance paths could still land without the owner |
| 2 | Climb 4 (PR #28 RCA) | Named the process gap: designs reviewed as a finished signed state; required a lifecycle walkthrough + verifier-change known-bad. That remediation landed as CONTROL-LIFECYCLE. It defined “change” as verifier/self-ref change |
| 1 | Principle gap | A control-design lifecycle that does not walk **ordinary work under the activated signed set** cannot refuse a design that makes every tracked edit an owner-signature event |

**Furthest controllable upstream point:** the control-design process (Planit CONTROL-LIFECYCLE, briefing standard, finish-line known-bads). The hash file and the manifest line are outputs of that process.

---

## 4. Checks the user named

### 4.1 Did ADR 0055’s lifecycle walkthrough cover “ordinary non-gate change after activation”?

**No.**

ADR 0055 section “Lifecycle walkthrough (create, change, sign, ingest, rotate, first bootstrap)”:

| Subsection | What it walks | Ordinary non-gate after activation? |
| ---------- | ------------- | ----------------------------------- |
| Create | New **self-ref member** under `staging/<change-id>/` | No |
| Change | Existing **live member**; live edit is refuse | No — “change” means self-ref member |
| Sign | Owner signs the **proposed** gate-set manifest | Assumes the change is already a manifest member |
| Ingest | Activate tool; live verifier; no split land | Self-ref activate only |
| Rotate | Owner key; self-ref members | No |
| First bootstrap | One-time land of the staging tools; statement excluded from digest/closure “so it can name the manifest digest without a cycle” | Mentions the cycle class; does not walk a later docs/rca PR |

After bootstrap the ADR says further **self-ref** edits use staging + activate only. It does not say what happens when the change is *not* a self-ref member and *not* a gate-set member.

CONTROL-LIFECYCLE (`tools/nouns/fitness_control_lifecycle/fitness_control_lifecycle.py`) greps Planit, AWL, and the briefing validator for the needles `create, change, sign, ingest, rotate`, `first bootstrap`, and `legitimate change to the verifier`. It cannot fail a walkthrough that never mentions ordinary non-gate work.

### 4.2 Should PR #29’s finish line have caught it?

**Yes, if the finish line had included the known-bad in this record’s title. It did not.**

The owner-approved remediation brief that produced PR #29 (cloud agent `bc-7f194854`, first user message) required:

- Derived self-ref set + live-member-edit known-bad
- Known-bad “legitimate change to the verifier” through staging
- Known-bad split land
- Mandate-inheritance known-bad
- Signing order (local CI → `write_verified` → content-tree sync → remanifest → placeholder dry-run)
- One owner statement for the ADR and the manifest
- “All PR checks green except the owner-signature rows”

That list is exactly Climb 4’s P+L (lifecycle + verifier-change known-bad). It treats “green except signature” as success for the **bootstrap** land. It never asks: after that sidecar is in, can a **later** non-gate PR stay green **without** another sidecar?

The finish line therefore **should** have caught this if ordinary-after-activation had been a required row. Under the rows that were written, the agent could (and did) treat hash-file membership as a signing-order detail: when armor occupancy changed the digest, remanifest and wait for the owner. That is the correct move *during bootstrap*. It is the defect *after activation*.

### 4.3 Helix’s brief

**No Helix design brief is in this tree or in the PR #29 transcript.**

The only Helix mention in the PR #29 agent transcript (`bc-7f194854`, user message 9) is the owner reporting that Helix verified the clearsignature (`Good signature from 9D1BD577…`, signed-body sha256 `c1e196e4…`). That is ingest verification, not a control-design brief.

The brief that produced ADR 0055 is the owner-approved remediation quoted in §4.2. Notion topic-stack lookup was not available in this environment (MCP unauthenticated). If Helix holds a separate brief outside this repo, it is not reconstructable from hub files or that transcript.

What that in-repo brief should have caught is the same gap as the finish line: it required a lifecycle walkthrough of the **staging machinery itself**, not ordinary non-gate change after activation.

### 4.4 Relation to the earlier cycle fix

The cycle fix and this defect are the same *class* (a digest member that moves when a ratification artifact moves) and opposite *directions*.

| | Cycle fix | This defect |
| | --------- | ----------- |
| Trigger | Placing owner armor / the statement that *names* the manifest digest | Editing a tracked file that is **not** in the signed set |
| Direction | Signature → digest → hash file → remanifest → signature (does not converge) | Non-member → digest → hash file → remanifest → **one** new signature (converges, but every time) |
| Commits | `241e3ec` exclude `approval.asc` from closure and hub digest; `9030b16` restore exclude set (Planit evidence + manifest + hash file must not digest each other); PR #29 occupancy (`armor_occupancy_paths`, bootstrap statement) | Never asked |
| Known-bad that landed | `assert-gate-set-manifest-placeholder-sidecar-fails`: placeholder armor must not widen closure or hub digest; failure must be signature-only | Missing: doc-only PR green with the existing sidecar |
| What still protects excluded armor | Sidecar P1 (trusted key, Content-SHA256, Decision), C8, occupancy dry-run | Not applicable — the hash file was **kept** in S |

The cycle fix asked: “can the owner finish signing without the stamp moving under the pen?” It answered by excluding the files that *name* the digest. It did not ask: “after the pen is down, can anyone else change a provenance file without calling the owner back?”

PR #29’s later occupancy work **re-discovered** that the hash file is a signed member (PM try 2: “Adding `adrs/owner-approvals/staged-signing.approval.asc` changed the content tree, and `integrity/hub-content-tree-hash.txt` is a signed manifest member”). The remediation was to exclude the new occupancy path from the digest — another cycle-break — not to take the hash file out of S or to narrow coverage.

---

## 5. Impact / scope

- Any tracked edit outside `_content_exclude_rel()` (the hash file, Planit evidence, the manifest, approval armor, bootstrap statement/armor) stale-dates the signed hash file.
- Provenance paths that ADR 0051 and `GATE_SET_EXCLUSIONS` call “never a pass/fail grading input” (`docs/rca/`, `docs/history/`, `reviews/`) still force owner ratification.
- Routine docs, RCA instance records, reviews, `CONTRIBUTING.md`, `MANIFESTO.md`, `LICENSE`, and similar cannot merge green without the owner. That is the “routine work is impossible” condition.
- This record is itself that case: adding this file without touching the hash file leaves `hub-content-tree-fresh` red. Refreshing the hash file would be a second file and a signed-member edit, which this run was told not to do.

---

## 6. Timeline (brief)

| Time | Event |
| ---- | ----- |
| 2026-10-10 | ADR 0050: evidence binds to content; hub stamp is `hub-content-tree-hash.txt` |
| 2026-10-11 | ADR 0051: gate-set = CI load closure; member-byte change needs owner receipt |
| 2026-10-11+ | ADR 0052: receipt is owner OpenPGP sidecar on the manifest |
| `241e3ec` | Exclude manifest `approval.asc` from closure and hub digest (cycle) |
| `9030b16` | Restore exclude set; comment “The exclusion breaks a hash cycle.” |
| 2026-10-25 | PR #28 Climbs 1–4; Climb 4 one thing = lifecycle walkthrough + verifier-change known-bad |
| 2026-10-25 | ADR 0055 + CONTROL-LIFECYCLE land that one thing for self-ref members (PR #29) |
| 2026-10-25 | Occupancy cycle: batch armor was a digest member; excluded; owner signs; `bfe327c` |
| 2026-10-25 | PR #28 (still draft) adds one RCA file; `hub-content-tree-fresh` red; this climb |

---

## 7. Mechanism on reproduction

**Confirmed (product), at `bfe327c`:**

```text
is_gate_set_path(docs/rca/README.md) == False
"integrity/hub-content-tree-hash.txt" in manifest path column == True   # line 732
len(derive_gate_set_paths) == len(manifest path column) == 3812
hub digest coverage == 3886 tracked paths
hub digest ∩ complement(S) == 77 paths   # includes all docs/rca/*.md
```

Writers: `content_digest_excluding` (`tools/nouns/evidence_ref/sync_content_tree_hash.py`); `derive_gate_set_paths` (`tools/nouns/gate_set/gate_set.py`); `manifest_bytes` (`tools/nouns/gate_set_manifest/gate_set_manifest.py`). Seed of closure: `.github/workflows/*`. `hub-content-tree-fresh` is in `integrity/releasable-gates.json` profiles `verify` and `release`.

**Confirmed (process):** ADR 0055 walkthrough text and CONTROL-LIFECYCLE needles contain no “ordinary non-gate change after activation.” PR #29 finish-line bullets (brief text in `bc-7f194854` message 1) contain none. Cycle-fix known-bad asserts occupancy does not change the hub digest; it does not assert a provenance add leaves the sidecar valid.

---

## 8. Derived list — signed or digest artifacts with the same property

**Property (code, not a hand list):** digest artifact D is a member of the owner-signed set S (`integrity/gate-set-baseline.manifest.sha256` path column == `derive_gate_set_paths`), and D’s coverage C includes tracked paths that are not in S. Changing such a path forces D to change, which changes S, which requires a new owner signature.

**How derived:** import the writers; compute S from the on-disk manifest; compute each C from the function that writes D; classify.

| Id | Artifact D | Writer | In S? | Coverage C | C − S | Hits known-bad (docs/rca in C)? |
| -- | ---------- | ------ | ----- | ---------- | ----- | ------------------------------- |
| hub-content-tree-hash | `integrity/hub-content-tree-hash.txt` | `content_digest_excluding` | **yes** | 3886 (`git ls-files` minus exclude set) | **77** | **yes** |
| planit-change-evidence-source-tree | `.nlc/planit-change-evidence.json` | `source_tree_hash` | **yes** | ~3891 (rglob minus skip dirs and self) | **80** | **yes** (structural) |
| gate-set-manifest | `integrity/gate-set-baseline.manifest.sha256` | `manifest_bytes` | yes | 3811 (S minus self line) | 0 | no |
| verify-fingerprints | `.nlc/verified.json` | `build_fingerprint_manifest` / `iter_verify_paths` | yes | 77 (`adrs`, `rules`, `knowledge`, `goals`, `domain`; bootstrap statement/armor skipped) | 0 | no |
| install-hashes | `integrity/nlc-install-hashes.json` | `install_hash_update` + `gate_activate._refresh_install_hashes` | yes | 45 (fixed globs + `tools/nlc-*.py` + published `SKILL.md`) | 0 | no |
| planit-identity-registry | `integrity/planit-skill-registry.json` | `registry_from_bytes` | yes | 1 (`.agents/skills/planit/SKILL.md`) | 0 | no |
| findings-last-pass-ref | `FINDINGS.md` | `fitness-findings-last-pass-fresh` | yes | path citation of the hash file; **does not embed the digest value** | 0 | no |

**Hits (same property): two.**

1. **`integrity/hub-content-tree-hash.txt`** — live CI path. `hub-content-tree-fresh` is on every verify/release run. This is the symptom.
2. **`.nlc/planit-change-evidence.json`** — same structural property (whole-tree digest, member of S, also a self-ref member). **Latent on the PR #28 path:** releasable `planit-skill-identity` invokes `fitness-planit-identity.py --skill-only`, which skips `evidence_errors`. Default (no `--skill-only`) and `--check-evidence` compare `source_tree_sha256` to the whole tree. `--record` rewrites D after any file change and would then require remanifest + owner signature. Not the red row on PR #28; same coupling if that check is ever the wired default.

**Not the same property (in S, but coverage ⊆ S or not a content digest of a wider set):**

| Artifact | Why it is not a hit |
| -------- | ------------------- |
| Gate-set manifest | Digests S only (by construction) |
| `.nlc/verified.json` | Fingerprints compile-identity dirs; all 77 current paths are in S |
| `integrity/nlc-install-hashes.json` | 45 install subjects; all in S |
| `integrity/planit-skill-registry.json` | Digests one self-ref skill already in S |
| `FINDINGS.md` | Must contain the string `hub-content-tree-hash.txt`; does not store the hex. A doc-only add does not force a FINDINGS edit |
| `integrity/full-nlc-audit-inference-record.json`, `integrity/hub-release-record.json`, `integrity/integration-leaves.json` | Cite the hash **path** (`content_tree_hash_ref` / `tree_hash_ref`), not a live digest of non-S bytes |
| `integrity/mandated-paths.json`, `integrity/self-ref-set.json` | Derived path lists / pin maps, not content digests of provenance files. A new `docs/rca/*` file does not change them |
| Accepted-ADR OpenPGP sidecars | Separate signed set (C6). At `bfe327c`, one sidecar-signed ADR; it is already in S. Not a whole-tree digest |

**The 77 non-S paths inside the hub digest** (complete, from the same script):

`.agents/README.md`, `.cursor/environment.json`, `.cursor/rules/agents-portable-ssot.mdc`, `.cursor/rules/change-version-class.mdc`, `.nlc/briefs/hub-material-0051-0052.md`, `.nlc/gate-scope.json`, `CONTRIBUTING.md`, `HOLES.md`, `LICENSE`, `MANIFESTO.md`, `docs/LANGUAGE-SCANNER.md`, `docs/OPERATING_BINDINGS.md`, `docs/RISKS-AND-CONCERNS.md`, `docs/USE-CASES-PROOF.md`, `docs/ai-compiled-systems/README.md`, `docs/bba/BBA-EMIT-PROCESS.md`, `docs/bba/POLICY-ADR-LINEAGE.md`, `docs/bba/POLICY-OVERLAY-SCHEMA.md`, `docs/bba/VERB-SET.md`, `docs/github-ruleset-release.json`, `docs/github-ruleset-release.md`, `docs/history/SHA-MAP.md`, eighteen `docs/rca/*.md` files, `docs/worked-examples/pan-handling/README.md`, thirty `reviews/**` files, `scripts/nlc-launcher.sh`, `signing/adr-batch-statement.txt`, `signing/fix-pr-statement.txt`, `staging/README.md`, `theory/README.md`, `tools/ci-fitness-check1.sh`.

Prefixes: `docs` 31, `reviews` 30, `.cursor` 3, `.nlc` 2, `signing` 2, plus one each of `.agents`, `CONTRIBUTING.md`, `HOLES.md`, `LICENSE`, `MANIFESTO.md`, `scripts`, `staging`, `theory`, `tools`.

Hub digest exclude set at `bfe327c` (`_content_exclude_rel`): the hash file, `.nlc/planit-change-evidence.json`, the manifest, `integrity/gate-set-baseline.manifest.sha256.approval.asc`, `adrs/owner-approvals/staged-signing.statement.txt`, `adrs/owner-approvals/staged-signing.approval.asc`.

---

## 9. Candidate roots (at most three)

| Candidate | §3 bar | Verdict |
| --------- | ------ | ------- |
| Sync the hash file on PR #28 / this PR | Output-only; next doc still needs the owner | Reject |
| Exclude the hash file from S, or narrow the digest to S | Fixes this emit; the next control design can re-tie a whole-tree stamp into the signed set | Too low (product follow-up) |
| CONTROL-LIFECYCLE / brief / finish line must walk **ordinary non-gate change after activation** and carry the known-bad “doc-only PR green with no owner signature; gate-set edit still requires one” | One process change; deterministic; earliest controllable; in-repo (same layer Climb 4 added, incomplete definition of “change”) | **Survives** |

---

## 10. The one thing

> What **one** deterministic, actionable thing, if it were different, would have **prevented this error condition from arising**?

**Answer:** The control-design process (Planit CONTROL-LIFECYCLE, the briefing standard, and any finish line for a pin / sidecar / digest / signed set) must treat **ordinary non-gate change after activation** as a blocking lifecycle row, with the known-bad: **a doc-only PR must go green with no owner signature while a gate-set edit still requires one.**

Climb 4 required create / change / sign / ingest / rotate and a known-bad of legitimate **verifier** change. ADR 0055 compiled that as self-ref staging. “Change” was defined as “change to a live member.” The missed question is the complementary case: change that is **intentionally not** a member.

**Prevention test:** If **ordinary-non-gate-after-activation + that known-bad** had been a blocking CONTROL-LIFECYCLE row **before** ADR 0050’s whole-tree stamp was placed on the CI-closure signed set (and **before** PR #29 activated that set), **“any tracked edit requires a new owner signature”** could not have been the designed path because **the finish line would have REFUSED a produce whose only green path for `docs/rca/*` is remanifest + owner sidecar.**

**Completed:** yes (mechanism: design-process requirement). Product shapes that would then pass the known-bad are options A–C below. Do not implement here.

**Class:** process (design briefing / known-bad class). Same family as Climb 4; different missed question. Climb 4 asked how a **legitimate verifier** is updated. This climb asks how **ordinary work** proceeds after the signed set is live.

---

## 11. Contributing factors

- ADR 0051’s “CI load closure” rule is working as written: the freshness gate loads the hash file, so the file is a member. The defect is composing that rule with a whole-tree C.
- Cycle-fix known-bads trained review on “does signing move the digest?” not “does a provenance add move a signed member?”
- `hub-content-tree-hash.txt` is not in the self-ref set, so ADR 0055 live-member refuse never looks at it.
- FINDINGS last-pass freshness is implemented by checking the hash file, not by embedding the hex in FINDINGS — a good split that was not applied to ratification.
- Helix’s visible role in PR #29 was signature verification, which cannot see this class of gap.
- C8 is correct (tools must not write armor). It makes the amplification expensive rather than causing it.

---

## 12. Remediation options (not done)

Every option below is required to pass the same **known-bad**: add only a `docs/rca/*.md` file (or any other current non-S tracked path); CI `hub-content-tree-fresh` and `fitness-gate-set-manifest` are MET; the existing owner sidecar still verifies; a deliberate gate-set member edit is still INCOMPLETE without a new sidecar.

The process row in the one thing is a prerequisite for all of them: without it, a later design can reintroduce the coupling.

### Shared lifecycle skeleton (instantiate per option)

| Phase | Must show |
| ----- | --------- |
| Create | How a new digest stamp or signed member is born; who signs what |
| Change (ordinary non-gate) | A provenance / docs edit after activation: which files move, which do not, no owner action |
| Change (gate-set / self-ref) | Staging or remanifest; owner signs; activate or sidecar land |
| Sign | Owner signs **only** proposed gate-set (or self-ref) bytes, never the ordinary doc |
| Ingest | Live verifier; C8; no split land on verifier paths |
| Rotate | Key rotation still ADR 0052; ordinary docs still unsigned |
| First bootstrap | One-time land may still exclude files that name the digest (cycle class stays solved) |

### Option A — Keep a whole-tree freshness stamp; take it out of S

**Product:** Exclude `integrity/hub-content-tree-hash.txt` from `derive_gate_set_paths` (exact-path exclusion, same class as `approval.asc`), and from the manifest. Keep `hub-content-tree-fresh` as a CI gate that compares recorded hex to `content_digest_excluding`. Do the same for `.nlc/planit-change-evidence.json` or keep `--skill-only` as the only wired invocation **and** exclude it from S.

**Lifecycle:** Create = write the stamp (unsigned). Ordinary change = edit the doc, run `sync-hub-content-tree-hash`, commit two files, no sidecar. Gate-set change = stage/remanifest, owner signs S (which no longer lists the stamp). Sign / ingest / rotate / bootstrap unchanged for remaining members. Bootstrap still excludes armor/statement from the digest.

**Tradeoffs:** The stamp is no longer owner-ratified. Tampering **only** the hex fails freshness (computed ≠ recorded). Tampering content without moving the hex fails the same gate. Trust for “what is a gate” stays on the signed manifest. Risk: reviewers may treat the unsigned stamp as a second source of truth; bind it as freshness-only in FINDINGS / release receipts (already the ADR 0050 role).

**Known-bad:** doc-only PR + hash sync, no remanifest, sidecar still MET; edit `tools/nouns/gate_set/gate_set.py`, remanifest without sidecar → NOT_MET.

### Option B — Narrow C to S (digest only what is signed)

**Product:** `content_digest_excluding` hashes `derive_gate_set_paths` minus the existing cycle exclusions (and minus the hash file itself). Provenance prefixes stay out of C because they are already out of S. Hash file may remain in S; a docs/rca add does not change it.

**Lifecycle:** Create = digest of S. Ordinary change = no hash move, no remanifest, no sign. Gate-set change = member bytes + hash + remanifest + owner sign. Sign/ingest/rotate/bootstrap as ADR 0055 for self-ref; ordinary path never enters staging.

**Tradeoffs:** Loses ADR 0050 “the audited object is the whole tree” for provenance. That matches ADR 0051’s “`docs/rca/` is never a grading input.” Risk: a non-S, non-excluded path that later becomes load-bearing (new CI seed) must enter S **and** C together; derive already does that for membership — C would follow. Also fixes the 77-path set completely, not only `docs/rca/`.

**Known-bad:** doc-only PR, hash file unchanged, sidecar MET; gate-set edit without new sidecar NOT_MET.

### Option C — Two stamps (split freshness from ratification)

**Product:** Keep whole-tree `hub-content-tree-hash.txt` as an **unsigned** freshness stamp (Option A). Keep the signed manifest as the **only** ratified digest (already Option B’s C = S). Name the split in ADR 0050/0051 so FINDINGS, release receipts, and verify profiles cannot collapse them again.

**Lifecycle:** Create = two artifacts with different roles. Ordinary change = refresh unsigned stamp only. Gate-set change = remanifest + sign. Sign never covers the whole-tree stamp. Ingest/rotate/bootstrap as ADR 0055. First bootstrap keeps cycle exclusions on files that name the signed digest.

**Tradeoffs:** Clearest product story; two fingerprints to teach. Slightly more produce steps than B on ordinary PRs (must still sync the unsigned stamp). Lowest chance of silent re-coupling if the process row is bound.

**Known-bad:** same as A for the unsigned stamp; same as today’s manifest gate for S.

### Option D — Exclude only `docs/rca/` (and maybe `docs/history/`, `reviews/`) from C

**Product:** Add those prefixes to `_content_exclude_rel()`. Hash file stays in S.

**Lifecycle:** Ordinary **RCA** change = no hash move. Ordinary **other** doc (`CONTRIBUTING.md`, `MANIFESTO.md`, `docs/OPERATING_BINDINGS.md`, …) still remanifests. Gate-set path unchanged.

**Tradeoffs:** Makes PR #28 mergeable; fails the stated known-bad if “a doc-only PR” means any non-gate doc. Leaves 59 of the 77 non-S digest paths amplifying. Reject unless the owner narrows the known-bad.

**Known-bad (as stated):** **FAIL** for `CONTRIBUTING.md` / `MANIFESTO.md`.

### Option E — Status quo (owner signs every PR that touches a digest member, including the hash file)

**Lifecycle:** Ordinary change = remanifest + owner sign. Gate-set change = the same. Sign is the only ingest path for docs.

**Tradeoffs:** No product change. Routine work stays blocked on the owner. Climb 4’s “legitimate change” known-bad still passes (verifier staging). This record’s known-bad **FAIL**.

**Rejected** as a remediation; recorded so “just sign this RCA” is not mistaken for a fix.

### Option F — CI auto-resync of the hash file while it remains in S

**Product:** A bot rewrites `hub-content-tree-hash.txt` on every PR.

**Tradeoffs:** Does not help while D ∈ S: the bot’s rewrite is a signed-member edit and still needs a sidecar (or a tool-written sidecar, which C8 refuses). Only works if paired with A or C. Alone it is a symptom patch.

**Known-bad:** **FAIL** unless combined with A/C.

### Latent second hit

Options A–C must name `.nlc/planit-change-evidence.json`. Either exclude it from S and from whole-tree identity checks on ordinary PRs, or stop storing a whole-tree `source_tree_sha256` in a signed file. Leaving it latent keeps a second copy of this defect behind `--skill-only`.

---

## 13. Preventive action (single tracked item — not done)

| Field | Value |
| ----- | ----- |
| Action | Extend CONTROL-LIFECYCLE (Planit, AWL, briefing validator) so “ordinary non-gate change after activation” is a blocking walkthrough row, with known-bad: doc-only PR MET without a new owner sidecar; gate-set edit NOT_MET without one. Then pick a product option that passes that known-bad (A, B, or C). |
| Owner | hub |
| Path / artifact | `.agents/skills/planit/SKILL.md`, `.agents/skills/planit/references/audited-work-loop-standard.md`, `tools/nouns/hub_own_produce/hub_own_produce.py`, `tools/nouns/fitness_control_lifecycle/`; product follow-up on `sync_content_tree_hash.py` / `gate_set.py` / ADR 0050–0055 |
| Verification | A fixture that adds only `docs/rca/…` is MET on `hub-content-tree-fresh` and `fitness-gate-set-manifest` with the existing sidecar; a gate-set member edit without a new sidecar is NOT_MET; CONTROL-LIFECYCLE fails an ADR walkthrough that omits the ordinary-after-activation row |
| Belief / gate touch (ADR 0025) | Unsuitable process: control lifecycle that never walks ordinary work under an activated signed set. Touches CONTROL-LIFECYCLE and, after Accept, the digest/signed-set composition |

---

## 14. Follow-up (detection only)

- This PR and PR #28 are live specimens of the known-bad (red `hub-content-tree-fresh` on an RCA-only diff). Do not “fix” them by syncing the hash under the current design.
- If Helix holds a brief not in this repo, attach it to the remediation produce; the in-repo brief is already evaluated.

RCA only. No remediation commit.
