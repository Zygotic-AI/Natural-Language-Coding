# ADR 0058 — Six-step unsigned hub release

- Status: Accepted
- Date: 2026-11-03
- Deciders: Human manager
- Accepted: Human manager (chat Accept, 2026-11-03)
- Class: F (integrity / hub produce), process
- Corpus: nlc
- Version class: **minor**
- Supersedes: [ADR 0052](0052-owner-openpgp-ratification-amends-0051.md) (OpenPGP ratification), [ADR 0055](0055-staged-activation-of-gate-machinery.md) (staged activate + armor), [ADR 0056](0056-per-file-adr-detached-signatures.md) (per-file ADR signatures), [ADR 0057](0057-tag-time-checker-digest.md) (tag-time digest signature)
- Amends: [ADR 0051](0051-hub-own-produce-principles.md) SG2 (owner receipt is the merge, not a sidecar), [ADR 0039](0039-single-command-human-surfaces.md) (the one command is `./release` and it is the whole of steps 3–6), [ADR 0044](0044-hub-release-production-trunk.md) (human contract is six steps; work still lives on `release/<semver>`), [ADR 0049](0049-release-planner-owns-stops.md) (a stop may not be “please sign”), [ADR 0022](0022-hub-release-fail-early.md) (Highlights text is not a tag blocker)

## Context

The hub accumulated GPG sidecars, a 3,642-row signed file list, per-file architecture-decision signatures, staged activation, and a tag-time checker-digest signature. Ordinary work became an owner-phone ceremony. Most of that already does not block a green branch. One live ship blocker remains: tagging refuses without a GPG sidecar on `integrity/checker-digest.sha256`.

The required human path is six steps and zero signatures:

1. A `release/<semver>` branch exists.
2. Everything merges into that branch.
3. One command checks everything that must be checked. If a sensitive file changed, the command lists it. The human reverts, edits, or accepts. Stay on this step until every listed file is resolved. Prefer fewer sensitive files. Do not sign them.
4. After that, never sign another thing.
5. Merge to `main`.
6. Tag.

No other human steps. No GPG. GitHub merge after the list is the lock.

## Decision

### 1. The human path is exactly those six steps

| Step | Who | Done when |
| --- | --- | --- |
| 1. `release/<semver>` exists | anyone | branch name matches `release/` + the version that will be tagged |
| 2. Work merges into that branch | anyone | the release branch contains the work |
| 3. One command | `./release` | all machine checks pass, and every sensitive-file line is reverted, edited, or left for the owner to accept by merging |
| 4. No signing after that | everyone | no GPG, no sidecar, no “Sign this”, no `Released-by:` as a ship gate |
| 5. Merge to `main` | human who can merge `main` | GitHub merge of the release pull request |
| 6. Tag | `./release` after the merge | annotated tag on that merge commit, then tag push |

Opening the pull request is how GitHub does step 5. It is not a seventh step. `./release` opens or updates it when step 3 is ready.

`./release` may create `release/<semver>` if it does not exist yet. That is step 1, not a separate GitHub Actions ritual. The start-release workflow is not required.

Work stays on `release/<semver>` until step 5. That is the production-trunk rule from ADR 0044, kept as an internal invariant, not as extra human ceremony. There is one in-flight `release/<semver>` at a time. Other work merges into it (step 2).

### 2. Zero signatures

No file requires an OpenPGP clearsignature or detached signature to compile, to merge, or to tag.

Deleted as gates (after this record is Accepted):

- Tag-time checker-digest sidecar (`integrity/checker-digest.sha256.approval.asc`)
- Gate-set manifest sidecar
- Per-file `adrs/*.md.asc` and any `*.approval.asc` requirement
- “Unsigned produce is incomplete”
- Tools-must-not-write-sidecars (C8) as a ship rule
- Staged activation that waits on pasted armor
- Sign-this chat protocol
- `Released-by:` / `Ratified-by:` as a ship or compile gate

The GitHub merge commit is the record that the owner accepted the bytes. Charter confirmation C24 (ratification is recorded for classes that require it) is satisfied by that merge, not by a phone key.

### 3. The one command is `./release`

`./release` with no flags is the only human release command. It does step 3, and after step 5 it does step 6.

Inside the command (not extra human steps): infer the version and `release/<semver>` branch; run the real pass/fail suite; refresh unsigned derived files (gate-set membership list, checker digest hex, install hashes) when they drift; print the sensitive-file list; open or update the pull request; after merge, tag the merge commit; push the tag.

Stops that die:

- “Owner must sign”
- “Highlights still placeholder”
- A second chat skill (`/release`) that is a different checklist from `./release`
- A separate PR-offer command the human must know about

Stops that stay, inside the same command:

- Machine checks not green
- Sensitive-file list not resolved (see decision 4)
- Cannot merge (human has not merged)
- Tag already exists for that version

### 4. Sensitive-file review (the lock that replaces GPG)

**What it is.** A short, named set of paths that an agent must not silently rewrite: architecture-decision files, the programs that decide pass/fail, the CI workflows that run them, the release command, and the list-builder itself.

**What it is not.** The 3,642-row CI-load closure. That list may still be regenerated as a machine freshness check. Humans do not review 3,642 rows.

**SSOT prefixes** (edit this table in this ADR if the set must change; do not grow it in code only):

| Prefix or path | Why it is on the list |
| --- | --- |
| `adrs/[0-9][0-9][0-9][0-9]-*.md` | Architecture decisions |
| `CHARTER.md` | Charter |
| `integrity/PRINCIPLES.md` | Integrity principles |
| `integrity/releasable-gates.json` | Which checks actually run |
| `integrity/known-bad-cases.json` | Designed-fail specimens |
| `tools/ci_fitness.py`, `tools/nlc.py` | Pass/fail entrypoints |
| `tools/fitness-*.py`, `tools/assert-*.py` | Pass/fail adapters |
| `tools/nouns/` | Pass/fail implementations (the referee). One prefix so a noun cannot be weakened off-list |
| `./release`, `scripts/nlc-release.sh` | The one command |
| `tools/nlc_release_sensitive_review.py` | The list-builder (must list itself) |
| `.github/workflows/fitness.yml`, `.github/workflows/release.yml` | CI that grades and tags |
| `.agents/skills/release/SKILL.md` | Agent instructions for the one command |
| `.agents/skills/planit/SKILL.md` | Compiler orchestrator |
| `.agents/skills/planit/references/audited-work-loop-standard.md` | Control-lifecycle text |

A path not in this table is not a sensitive-review line. Ordinary docs, examples, RCA notes, and generated ledgers are not on the list.

Do not split `tools/nouns/` into a hand-kept subset. A subset is how an agent hides a check.

**How the list is built (cannot be cheated by the branch).** `./release` runs the copy of `tools/nlc_release_sensitive_review.py` that is already on `origin/main` against the release-branch tree. The branch’s own copy is never the grader. Editing the list-builder on the branch cannot hide files.

**How a line is resolved.**

| Action | What happens | List after |
| --- | --- | --- |
| (a) Revert | File bytes match `origin/main` | Line gone |
| (b) Edit | File still differs; re-run the command | Line stays or updates to the new hash |
| (c) Accept | Owner merges the pull request whose body listed that path + hash | Merge is accept. No GPG. No extra receipt file. |

Until every line is gone (revert/edit until empty) or the owner is merging the remaining lines as accept, stay on step 3. The command prints the full list on every run. The same list is copied into the pull-request body. Tagging is forbidden until that pull request is merged.

Do not add an accept-JSON or hash-receipt file. Agents can write those. Agents cannot perform the owner’s GitHub merge if branch protection requires the owner.

### 5. First bootstrap of the list-builder

`origin/main` does not yet contain `tools/nlc_release_sensitive_review.py`. The first merge that lands this tool is the bootstrap:

- That pull request’s own CI may use the branch copy of the lister (there is no `main` copy yet).
- After that merge, every later `./release` uses `origin/main`’s copy.
- The bootstrap pull request itself is still a human merge. The files it adds include the lister, so they are on the list.

### 6. CONTROL-LIFECYCLE is rewritten to match this decision

After Accept, Planit / AWL / the briefing check must **not** require: create, change, **sign**, ingest, rotate, staging, or “unsigned manifest is incomplete.”

New blocking walkthrough for a control or gate design:

| Old word | New meaning |
| --- | --- |
| create | The check or list-builder exists |
| change | Someone edits a sensitive path |
| sign | **Not done.** Replaced by **list** (main’s copy prints the path) |
| ingest | **Merge to `main`** (accept) |
| rotate | **N/A.** No owner keys in the gate |
| first bootstrap | Land the list-builder on `main` once (decision 5) |

Known-bad of a **legitimate change to the verifier:** edit the list-builder on a branch so it omits a path that still changed; `origin/main`’s copy must still list that path and the list-builder itself. Staging + pasted armor is not the path. `tools/assert-verifier-change-via-staging-passes.py` is deleted after Accept.

### 7. What the one command still checks (machine, not human steps)

Keep running, inside `./release` / `./nlc verify`:

- The real fitness and assert suite (minus signature rows)
- Unsigned derived-file freshness: gate-set membership list matches the tree; checker-digest **hex file** matches the tree if that file is kept as a machine digest. No armor.
- Release identity: version file, release record, branch name, tag name agree (ADR 0045)

Do not keep as human or tag blockers:

- GPG
- Release-notes Highlights placeholder
- Inference “please confirm residuals” as a second ritual (if the suite is red, step 3 fails; if it is green, proceed)

## Lifecycle walkthrough (create, change, list, accept, merge, first bootstrap)

This section exists so the control-design gate can see the walkthrough. **Sign is not performed. Rotate is not performed.** A **legitimate change to the verifier** is listed by `origin/main`'s copy.

### Create

Add `tools/nlc_release_sensitive_review.py` and the prefix table in this ADR. No signature is created.

### Change

Edit a path in the prefix table. The next `./release` lists it.

### Sign

Not used. A phone key is not a release step.

### Ingest

The owner merges the release pull request. That merge is accept.

### Rotate

Not used. Owner-key allowlists are not gates. Public key files may remain in history; nothing reads them as a ship rule.

### First bootstrap

Decision 5. Land the lister, merge, then `main` grades later branches.

## Known-bads (must exist before wiring)

| Id | Setup | Required result |
| --- | --- | --- |
| KB-0058-hide | Branch copy of the lister drops `adrs/` from the prefix table; an ADR file changed | Main’s copy still lists the ADR and the lister. Command NOT_MET |
| KB-0058-self | Only the lister file changed | Main’s copy lists the lister. Command NOT_MET until merge |
| KB-0058-doc | Only `docs/rca/*` or other non-prefix docs changed | Sensitive list empty. Signature sidecar not required. Suite can be MET |
| KB-0058-unsigned-tag | Merge commit has no `*.approval.asc` | Tag gate MET (no signature check). Opposite of today’s tag-time digest signature |
| KB-0058-sign-stop | `./release` output or `/release` skill tells the human to sign | FAIL the skill/docs gate |

## Implementation plan (after this record is Accepted)

Do not implement the deletions or `./release` rewrite while this record is Proposed. Class F: ratify first.

| # | Step | Stop predicate |
| - | ---- | -------------- |
| 1 | This Proposed ADR + index rows | File exists; README / INDEX / CATALOG list 0058 as Proposed |
| 2 | Human Accepts this ADR | Status line is Accepted; human said Accept |
| 3 | Put 0058 on `adrs/ACTIVE.md`. Mark 0052, 0055, 0056, 0057 superseded. Retrofit 0051 SG2 with a text record so 0051 file bytes are not silently rewritten | ACTIVE lists 0058; superseded rows point at 0058 |
| 4 | Rewrite CONTROL-LIFECYCLE (Planit skill, AWL, briefing validator, `fitness-control-lifecycle.py`) to list/accept/merge. Remove sign/staging/unsigned-incomplete needles | `python3 tools/fitness-control-lifecycle.py` MET on the new needles; old “must sign” strings gone |
| 5 | Add sensitive-review noun + CLI; grader is `origin/main`’s copy | `python3 tools/nlc_release_sensitive_review.py --check` exits 0 on empty list, 1 with printed paths otherwise |
| 6 | Land KB-0058-hide, KB-0058-self, KB-0058-doc | Each assert prints `ASSERT:PASS` |
| 7 | Fold into `./release`. Remove checker-digest signature from the tag gate. Remove Highlights as a tag blocker | `./release --dry-run` shows checks + sensitive list + PR/tag; no sign step |
| 8 | Stop calling every signature fitness/assert (see Delete list) | `integrity/releasable-gates.json` has no sidecar/GPG rows |
| 9 | Delete armor files, `scripts/sign-adrs.sh`, signature-text-handoff instruction and Cursor rule, AGENTS.md signature-text paragraph | `git ls-files '*.approval.asc' 'adrs/*.md.asc'` empty except maybe fixtures that the suite no longer loads |
| 10 | Rewrite `docs/adoption/RELEASE.md`, `.agents/skills/release/SKILL.md`, and `docs/nlc/HUMAN-JUDGMENT-GATES.md` to the six steps only; C24 is the merge commit | Those files contain the six steps and do not tell the human to sign |
| 11 | Regen derived state; update known-bad SSOT | `python3 tools/regen-derived-release-state.py` then derived-state fitness MET |
| 12 | Prove | `python3 tools/ci_fitness.py` and `./nlc verify` exit 0 with no signature files |
| 13 | Record (produce package SSOT exit evidence; recorder) | `ssot_leaf_ids` and `ssot_exit_status` present |

## Delete list (after Accept)

Stop calling, then delete when nothing imports them:

- `tools/check-checker-digest-signature.py` and the call in `tools/nouns/nlc_release_tag_gate/nlc_release_tag_gate.py`
- `tools/fitness-adr-owner-sidecar.py` sidecar verification (heading-format checks may remain)
- `tools/fitness-no-tool-writes-ratification.py`
- `tools/fitness-owner-key-trust.py`, `tools/fitness-retired-key-denylist.py`
- `tools/fitness-owner-ratification-known-bad.py`
- `tools/assert-release-signed-passes.py`, `tools/assert-release-unsigned-fails.py`
- `tools/assert-sign-adrs-script-passes.py`, `tools/assert-tag-digest-signature-required-fails.py`
- `tools/assert-gate-set-manifest-missing-sidecar-fails.py`, `tools/assert-gate-set-manifest-placeholder-sidecar-fails.py` (replace with “no sidecar required”)
- `tools/assert-content-only-change-does-not-trip-gate-set-signature-passes.py` (replace with KB-0058-doc)
- `tools/assert-verifier-change-via-staging-passes.py`, `tools/fitness-live-self-ref-activation.py`, `tools/activate-gate-machinery.py`
- `scripts/sign-adrs.sh`, `goals/sign_adrs/`
- `.agents/instructions/signature-text-handoff.md`, `.cursor/rules/signature-text-handoff.mdc`
- Live `*.approval.asc`, `adrs/*.md.asc`, `adrs/owner-approvals/` armor
- Planit CONTROL-LIFECYCLE rows that require sign/staging/unsigned-incomplete
- `/release` skill rows about mandated pins / unsigned manifest incomplete as a finish line

## Keep list

- `./release` as the one command (ADR 0039)
- `release/<semver>` as the work line (ADR 0044, stripped of extra human steps)
- One version identity (ADR 0045)
- Planner owns stops (ADR 0049), but those stops are checks and merge-wait, never sign
- `./nlc verify` / `python3 tools/ci_fitness.py` as the suite inside step 3
- Branch protection: no direct push to `main`; owner merges
- Unsigned derived freshness (membership list / digest hex), not signed

## Rejected

- Keeping one GPG sidecar “just for the checkers.” Merge after the list is the lock. A second proof of the same bytes is the noise this record removes.
- An accept-JSON or hash receipt. Agents can write it. That is RCA 5 again.
- Per-file ADR signatures (ADR 0056).
- Tag-time digest signature (ADR 0057).
- Staging + armor to change the verifier (ADR 0055).
- Highlights-required tag gate.
- Extra human steps beyond the six.
- Making `main` hygiene a separate operator ritual. It stays an internal check of `./release`.

## Consequences

- First tag that ships this rule is a **minor** version (owner, 2026-11-03). Same class as adding the locks (v0.4.0). **v1.0.0** stays parked for dogfood.
- Produce-package leaves C6/C8 that demand sidecars are retired with the fitness rows.
- Charter C24 remains: ratification is recorded. The record is the merge commit.
- Integrity P3 / charter R30 remain: hard gates, complete or incomplete. The one command failing is the gate.

## Related

- Prior analysis in chat: impact of removing every signed gate; six-step path; zero files to sign.
- [ADR 0039](0039-single-command-human-surfaces.md), [ADR 0044](0044-hub-release-production-trunk.md), [ADR 0045](0045-hub-release-identity.md), [ADR 0051](0051-hub-own-produce-principles.md)
