# Natural Language Coding hub v0.4.0

## Highlights

Hub **v0.4.0** is a minor on **v0.3.0**. Tags v0.3.1, v0.3.2, and v0.3.3 stay on their peels. This line ships the compiler front door, published-skill authoring, staged gate activation, and per-file ADR owner signatures.

- **Natural Language Compiler install is the same on Linux, macOS, and Windows.** README and GETTING-STARTED show the commands the fitness piped-install jobs run: `scripts/install.sh` via `bash` on Linux, `scripts/install.sh` via `/bin/bash` on macOS, and `scripts/install.ps1` via `irm | iex` on Windows. The GitHub repo URL is unchanged.
- **Published skills are a content type with an author checklist.** ADR 0054 (published-skill author contract — YAML `name` matches the folder; in-tree links only) plus `nlc-skill-author-check.py`. The v0.3.3 terms-linker rewrite that made `/planit` unloadable is repaired. Live published skills pass `SKILL_AUTHOR:MET`.
- **Self-referential gate machinery activates through staging.** ADR 0055 (staged activation): candidates live under `staging/<change-id>/`; `activate-gate-machinery.py` swaps live bytes only with a valid owner sidecar. Mandate inheritance and a derived self-ref set are in force.
- **Each Accepted ADR has its own detached owner signature.** ADR 0056 (per-file detached signatures). `adrs/NNNN-slug.md.asc` by key `9D1BD57770FC3A1DE84702750AFD22B063AE01BC`. The 47-ADR batch statement no longer covers. The gate-set manifest stays one clearsigned sidecar. `scripts/sign-adrs.sh` is the owner catch-up.
- **Patch ships v0.3.1 / v0.3.2 / v0.3.3 are on this line.** Notes files, FINDINGS/DESCRIBE current-ship fitness (F1), ADR 0051 merge-base at the immutable `v0.3.0` tag, and the shipped-notes draft-footer refuse.

**Explicitly not in v0.4.0**

- Fixing the hub-content-tree-hash defect (the whole-tree digest is a signed gate-set member, so ordinary doc edits still need a new owner manifest signature). That is v0.4.1. RCA: `docs/rca/2026-10-25-signed-whole-tree-digest.md`.
- CI optimization.
- README diagrams (left: generic intent/policies; right: healthcare HIPAA + SEC).
- A new compiled-system use-case wave. UC14 / UC16 / UC20 stay expansion-only.
- Renaming the GitHub repo URL.

## Changes since v0.3.0

- Document Linux, macOS, and Windows install for the compiler (`933fecc`)
- Bring in the two RCA docs for the 0.4.0 line (`eb8c385`)
- Add per-file detached owner signatures for Accepted ADRs (`1d34e86`)
- Refresh before-generate stamp and unsigned manifest (`d35f8e3`)
- Make sign-adrs a thin goal and classify staging fixtures (`07f6125`)
- Require per-file detached ADR signatures and add owner sign-adrs script (`90255c5`)
- Place owner clearsignature at both occupancy paths (`5068d42`)
- Accept ADR 0055 and freeze hybrid owner statement (`f84eaea`)
- Give scratch-hub landmines a git identity on CI (`a69c56f`)
- Fix occupancy dry-run and yaml-free skill-author install (`4d46c3b`)
- Place owner clearsigned staged-signing batch armor (`e1a56d8`)
- Add bootstrap owner statement and refresh signed-set hashes (`feb7590`)
- Add staged activation of gate machinery (ADR 0055) (`9f3ef00`)
- Regenerate the unsigned gate-set manifest after the skill repair (`da90b90`)
- Repair published skills so the live author check is MET (`d4b4648`)
- Add the owner-signed sidecar for ADR 0054 (`ae6dcb6`)
- Accept ADR 0054 published-skill author contract (`15c9bb0`)
- Add Skill as a content type pointed at the author checklist (`4f3caf2`)
- Put ADR 0054 on the ACTIVE binder set (`6a5e561`)
- Bind the published-skill author checklist as law (`bcb2f95`)
- Move hub maintainer steps off the consumer README (`6ac954d`)
- Regenerate unsigned gate-set manifest for the checklist tree (`1ee783d`)
- Add growable skill-author checklist for release and install (`11a904c`)
- Update README.md (`b3e6622`)
- Update README.md (`0690d86`)
- Update README.md (`8b30e35`)
- Climb RCA: linker defect comes from untyped skill markdown (`4c94513`)
- Record RCA: skill YAML name lines rewritten by terms linker (`b11ecb0`)
- Add the owner-signed gate-set manifest sidecar (`ce12099`)
- Resolve ADR 0051 merge-base by tree after history rewrite (`ba4a686`)
- Add the owner-signed gate-set manifest sidecar (`fc44e16`)
- Slim the unresolved-merge-base landmine under the adapter cap (`ef12d0b`)
- Add the owner-signed gate-set manifest sidecar (`856a3a6`)
- Regenerate the unsigned gate-set manifest after member edits (`9643b54`)
- Converge the hub content hash after the v0.3.3 notes edit (`d09c944`)
- Record the merge-base fix in the v0.3.3 notes (`2e778b0`)
- Use tag v0.3.0 as the ADR 0051 merge-base after prune (`36bf7f8`)
- Add the owner-signed gate-set manifest sidecar (`3ef968d`)
- Align release/v0.3.3 identity, notes, and record (`5a2f4b1`)
- Strip shipped-notes draft footer and stale binding-matrix percent (`1c5b50f`)
- Add the owner-signed gate-set manifest sidecar (`fc3003a`)
- Align release/v0.3.2 identity, notes, and record (`4520334`)
- Add the owner-signed gate-set manifest sidecar (`89fb12b`)
- Keep F1 out of shipped-tag check_static; refresh install hashes. (`93fcc2c`)
- Refresh content digest and unsigned gate-set manifest. (`9de2d26`)
- Keep FINDINGS and DESCRIBE current-ship prose aligned with the tag. (`3d18ac6`)
- Add the owner-signed gate-set manifest sidecar (`d659910`)
- Refresh content digest and unsigned gate-set manifest (`ffff281`)
- Drop commit peel from FINDINGS last-pass line (`4f60e04`)
- Align release/v0.3.1 identity, notes, and record (`7b93b4b`)
- Require full-history checkout on release tag CI (`065b67c`)
- Add the owner-signed gate-set manifest sidecar (`0f7d896`)
- Refresh the content digest and unsigned gate-set manifest (`0a9bb47`)
- Run tag-commit verify-deep with that commit's tools (`a2adc77`)
- Treat a clean GitHub merge of the release tip as contained (`a0d598d`)

### Diff stat

```
.agents/skills/bbp-confirmer/SKILL.md              |    18 +-
 .agents/skills/bbp-proposer/SKILL.md               |    18 +-
 .agents/skills/bbp-recorder/SKILL.md               |    14 +-
 .agents/skills/bbp-reviewer/SKILL.md               |    18 +-
 .agents/skills/full-nlc-audit/SKILL.md             |    14 +-
 .../full-nlc-audit/references/inference-phases.md  |     5 +-
 .agents/skills/interview/SKILL.md                  |    28 +-
 .agents/skills/nlc-hub-audit/SKILL.md              |     5 +-
 .agents/skills/planit/SKILL.md                     |   217 +-
 .../metaprompts/templates/rca-record-TEMPLATE.md   |     2 +-
 .agents/skills/planit/references/README.md         |    18 +-
 ...agent-failure-modes-and-meta-prompt-patterns.md |     2 +-
 .../references/audited-work-loop-standard.md       |    95 +-
 .../planit/references/domain-first-authoring.md    |    22 +-
 .../skills/planit/references/hub-charter-loop.md   |    32 +-
 .../references/information-completion-contract.md  |    28 +-
 .../references/knowledge-change-review-standard.md |    12 +-
 .../planit/references/lean-operating-principles.md |    30 +-
 .../local-dsi-converge-audit-template.md           |    26 +-
 .../planit/references/nlc-before-generate.md       |    14 +-
 .../references/operation-verdict-standard.md       |    82 +-
 .agents/skills/planit/references/planit-process.md |    40 +-
 .../planit/references/report-pyramid-structure.md  |     2 +-
 .../references/repository-governance-standard.md   |     2 +-
 .../references/root-cause-analysis-standard.md     |    62 +-
 .../vault-pull-request-review-standard.md          |     2 +-
 .agents/skills/release/SKILL.md                    |    22 +-
 .agents/skills/verify/SKILL.md                     |    16 +-
 .github/workflows/release.yml                      |     2 +-
 .nlc/adr-bind-snapshot.json                        |    16 +-
 .nlc/before-generate-stamp.json                    |     4 +-
 .nlc/planit-change-evidence.json                   |     2 +-
 .nlc/produce-package.json                          |     6 +-
 .nlc/verified.json                                 |    27 +-
 AGENTS.md                                          |     2 +-
 CONTRIBUTING.md                                    |    28 +
 DESCRIBE.md                                        |    34 +-
 FINDINGS.md                                        |     5 +-
 README.md                                          |    49 +-
 TODO                                               |    66 +
 adrs/0001-zero-variance-integrity.md.asc           |     7 +
 adrs/0002-p2-scope.md.asc                          |     7 +
 adrs/0003-systems-extension-agent-nouns.md.asc     |     7 +
 adrs/0004-produce-fitness-handoff.md.asc           |     7 +
 adrs/0005-ssot-exit-evidence.md.asc                |     7 +
 adrs/0006-contract-change-notice.md.asc            |     7 +
 adrs/0007-tags-primitives-reduced-adrs.md.asc      |     7 +
 adrs/0008-no-noun-inheritance.md.asc               |     7 +
 adrs/0009-primitive-interior-functions.md.asc      |     7 +
 adrs/0010-gate-after-every-generate.md.asc         |     7 +
 adrs/0011-natural-language-coding-naming.md.asc    |     7 +
 adrs/0012-rule-adoption-conflicts.md.asc           |     7 +
 adrs/0013-requirements-preflight.md.asc            |     7 +
 ...semver-upgrade-steps-and-noop-migrations.md.asc |     7 +
 ...0015-distribution-lock-and-version-store.md.asc |     7 +
 ...0016-hub-carries-no-product-requirements.md.asc |     7 +
 adrs/0017-human-command-surface.md.asc             |     7 +
 adrs/0018-human-cli-interview-on-gap.md.asc        |     7 +
 adrs/0019-guided-orchestration.md.asc              |     7 +
 adrs/0020-human-vs-agent-commands.md.asc           |     7 +
 adrs/0021-verify-fast-and-deep.md.asc              |     7 +
 adrs/0022-hub-release-fail-early.md.asc            |     7 +
 ...e-instance-trace-and-instant-audit-scope.md.asc |     7 +
 adrs/0024-nlc-factory-spine.md.asc                 |     7 +
 adrs/0025-belief-no-blame-climb.md.asc             |     7 +
 adrs/0026-promote-x1-x3-runners.md.asc             |     7 +
 adrs/0027-emit-from-prose.md.asc                   |     7 +
 ...d-atomic-verb-set-and-policy-adr-lineage.md.asc |     7 +
 ...adr-lineage-active-set-and-bind-snapshot.md.asc |     7 +
 adrs/0030-pipeline-wiring.md.asc                   |     7 +
 adrs/0031-charter-ratification-program.md.asc      |     7 +
 adrs/0032-charter-ownership-and-mutation.md.asc    |     7 +
 adrs/0033-charter-contracts.md.asc                 |     7 +
 .../0034-charter-goal-shape-and-composition.md.asc |     7 +
 adrs/0035-charter-knowledge-and-enforcement.md.asc |     7 +
 adrs/0036-inference-only-human-surface.md.asc      |     7 +
 adrs/0037-charter-non-r-surfaces.md.asc            |     7 +
 adrs/0038-no-memory-in-process.md.asc              |     7 +
 adrs/0039-single-command-human-surfaces.md.asc     |     7 +
 adrs/0040-process-preflight-remediation.md.asc     |     7 +
 adrs/0041-product-completion-scope.md.asc          |     7 +
 adrs/0042-rule-ir-hub-product-boundary.md.asc      |     7 +
 adrs/0043-uc14-composable-adopt-boundary.md.asc    |     7 +
 adrs/0044-hub-release-production-trunk.md.asc      |     7 +
 adrs/0045-hub-release-identity.md.asc              |     7 +
 adrs/0046-repository-planit-identity.md.asc        |     7 +
 adrs/0047-adr-approval-receipts.md.asc             |     7 +
 adrs/0048-executable-shape.md.asc                  |     7 +
 adrs/0049-release-planner-owns-stops.md.asc        |     7 +
 ...50-evidence-identity-content-not-history.md.asc |     7 +
 adrs/0051-hub-own-produce-principles.md.asc        |     7 +
 ...2-owner-openpgp-ratification-amends-0051.md.asc |     7 +
 adrs/0053-0051-0052-text-retrofit.md.asc           |     7 +
 ...54-published-skill-author-contract.approval.asc |    17 +
 adrs/0054-published-skill-author-contract.md       |    48 +
 adrs/0054-published-skill-author-contract.md.asc   |     7 +
 adrs/0055-staged-activation-of-gate-machinery.md   |    80 +
 ...0055-staged-activation-of-gate-machinery.md.asc |     7 +
 adrs/0056-per-file-adr-detached-signatures.md      |    78 +
 adrs/0056-per-file-adr-detached-signatures.md.asc  |     7 +
 adrs/ACTIVE.md                                     |     2 +
 adrs/CATALOG.md                                    |     3 +
 adrs/INDEX.md                                      |     3 +
 adrs/README.md                                     |     3 +
 adrs/owner-approvals/adr-batch-47.approval.asc     |    64 -
 adrs/owner-approvals/fix-pr.approval.asc           |   297 -
 adrs/owner-approvals/staged-signing.approval.asc   |    21 +
 adrs/owner-approvals/staged-signing.statement.txt  |    11 +
 content-types/HOW-TO-ADD.md                        |    51 +
 docs/ADR-ENFORCEMENT.md                            |     2 +
 docs/TERMS.md                                      |     4 +-
 docs/adoption/RELEASE-v0.3.1.md                    |    51 +
 docs/adoption/RELEASE-v0.3.2.md                    |    46 +
 docs/adoption/RELEASE-v0.3.3.md                    |    27 +
 docs/adoption/RELEASE.md                           |     6 +-
 docs/github-ruleset-release.json                   |    41 +
 docs/github-ruleset-release.md                     |    60 +
 docs/nlc/README.md                                 |     1 +
 docs/nlc/compiler/GETTING-STARTED.md               |    10 +-
 .../2026-10-20-skill-yaml-terms-link-load-error.md |   162 +
 .../2026-10-25-planit-unregistered-skill-edit.md   |   746 ++
 docs/rca/2026-10-25-signed-whole-tree-digest.md    |   368 +
 examples/README.md                                 |     1 +
 .../.agents/skills/demo/SKILL.md                   |     8 +
 examples/skill-author-check-landmine/README.md     |     3 +
 goals/hub_install/execute.ps1                      |    18 +
 goals/hub_install/execute.sh                       |    17 +
 goals/hub_skill_author_check/execute.ps1           |    32 +
 goals/hub_skill_author_check/execute.sh            |    27 +
 goals/sign_adrs/execute.sh                         |   238 +
 integrity/CONTRIBUTION.md                          |     4 +-
 integrity/LEXICON.md                               |     2 +-
 integrity/adr-gates.json                           |     8 +
 integrity/full-nlc-audit-inference-record.json     |     4 +-
 integrity/full-nlc-audit-manifest.json             |     8 +
 integrity/gate-set-baseline.manifest.sha256        |   330 +-
 ...baseline.manifest.sha256.approval-statement.txt |     5 +-
 .../gate-set-baseline.manifest.sha256.approval.asc |    19 +-
 integrity/hub-content-tree-hash.txt                |     2 +-
 integrity/hub-release-record.json                  |     4 +-
 integrity/mandated-paths.json                      | 11547 +++++++++++++++++++
 integrity/nlc-install-hashes.json                  |    21 +-
 integrity/nlc-version.json                         |     2 +-
 integrity/planit-skill-registry.json               |     2 +-
 integrity/releasable-gates.json                    |     9 +-
 integrity/self-ref-set.json                        |    36 +
 integrity/skill-author-checklist.json              |    22 +
 migrations/0.3.0_to_0.3.1/migration.yaml           |     3 +
 migrations/0.3.1_to_0.3.2/migration.yaml           |     3 +
 migrations/0.3.2_to_0.3.3/migration.yaml           |     3 +
 scripts/sign-adrs.sh                               |     5 +
 signing/adr-batch-statement.txt                    |    54 -
 signing/fix-pr-statement.txt                       |   287 -
 staging/README.md                                  |     5 +
 staging/per-file-adr-sigs/STAGED.json              |    10 +
 .../tools/nouns/owner_sidecar/owner_sidecar.py     |   676 ++
 tools/README.md                                    |     4 +-
 ...pproval-fails.py => activate-gate-machinery.py} |     5 +-
 tools/assert-activation-split-land-fails.py        |    13 +
 tools/assert-adr-approval-mismatch-fails.py        |    40 +-
 tools/assert-adr-detached-sig-fails.py             |    13 +
 tools/assert-adr-status-heading-fails.py           |     4 +-
 ...assert-hub-scope-unresolved-merge-base-fails.py |     5 +-
 tools/assert-live-self-ref-direct-edit-fails.py    |    13 +
 .../assert-mandate-skill-without-registry-fails.py |    13 +
 tools/assert-sign-adrs-script-passes.py            |    13 +
 tools/assert-skill-author-check-fails.py           |    12 +
 tools/assert-verifier-change-via-staging-passes.py |    13 +
 tools/derive-mandated-paths.py                     |    13 +
 tools/derive-self-ref-set.py                       |    13 +
 tools/fitness-control-lifecycle.py                 |    13 +
 tools/fitness-findings-shipped-tag-sync.py         |     2 +-
 tools/fitness-live-self-ref-activation.py          |    13 +
 tools/fitness-mandate-inheritance.py               |    13 +
 tools/fitness-skill-author-check-presence.py       |    12 +
 tools/fitness-skill-author-checklist.py            |    12 +
 tools/fitness-skill-content-type.py                |    12 +
 tools/fixtures/staged-activation/README.md         |     1 +
 .../staged-activation/TEST-ONLY-FINGERPRINT        |     1 +
 tools/fixtures/staged-activation/test-only.pub.asc |    10 +
 tools/fixtures/staged-activation/test-only.sec.asc |    10 +
 tools/generate-planit-identity-registry.py         |    20 +
 tools/nlc-skill-author-check.py                    |    14 +
 tools/nlc_release_notes.py                         |     2 +-
 tools/nouns/adr_approval/README.md                 |     2 +-
 tools/nouns/adr_approval/adr_approval.py           |     9 +-
 tools/nouns/adr_file_sig/README.md                 |     5 +
 tools/nouns/adr_file_sig/__init__.py               |     1 +
 tools/nouns/adr_file_sig/adjectives.txt            |     1 +
 tools/nouns/adr_file_sig/adr_file_sig.py           |   151 +
 tools/nouns/adr_file_sig/fields.txt                |     1 +
 .../assert_activation_split_land_fails/README.md   |     1 +
 .../assert_activation_split_land_fails/__init__.py |     1 +
 .../adjectives.txt                                 |     1 +
 .../assert_activation_split_land_fails.py          |    90 +
 .../assert_activation_split_land_fails/fields.txt  |     1 +
 .../assert_adr_batch_approval_fails/README.md      |     3 -
 .../assert_adr_batch_approval_fails/__init__.py    |     1 -
 .../assert_adr_batch_approval_fails/adjectives.txt |     1 -
 .../assert_adr_batch_approval_fails.py             |   320 -
 .../assert_adr_batch_approval_fails/fields.txt     |     1 -
 .../nouns/assert_adr_detached_sig_fails/README.md  |     9 +
 .../assert_adr_detached_sig_fails/__init__.py      |     1 +
 .../assert_adr_detached_sig_fails/adjectives.txt   |     1 +
 .../assert_adr_detached_sig_fails.py               |   225 +
 .../nouns/assert_adr_detached_sig_fails/fields.txt |     1 +
 ..._gate_set_manifest_placeholder_sidecar_fails.py |    45 +-
 .../README.md                                      |     1 +
 .../__init__.py                                    |     1 +
 .../adjectives.txt                                 |     1 +
 .../assert_live_self_ref_direct_edit_fails.py      |    62 +
 .../fields.txt                                     |     1 +
 .../README.md                                      |     1 +
 .../__init__.py                                    |     1 +
 .../adjectives.txt                                 |     1 +
 .../assert_mandate_skill_without_registry_fails.py |    70 +
 .../fields.txt                                     |     1 +
 .../assert_release_context_passes.py               |    51 +
 .../nouns/assert_sign_adrs_script_passes/README.md |     3 +
 .../assert_sign_adrs_script_passes/__init__.py     |     1 +
 .../assert_sign_adrs_script_passes/adjectives.txt  |     1 +
 .../assert_sign_adrs_script_passes.py              |   264 +
 .../assert_sign_adrs_script_passes/fields.txt      |     1 +
 .../assert_skill_author_check_fails/README.md      |     1 +
 .../assert_skill_author_check_fails/__init__.py    |     1 +
 .../assert_skill_author_check_fails/adjectives.txt |     1 +
 .../assert_skill_author_check_fails.py             |    39 +
 .../assert_skill_author_check_fails/fields.txt     |     0
 .../README.md                                      |     1 +
 .../__init__.py                                    |     1 +
 .../adjectives.txt                                 |     1 +
 .../assert_verifier_change_via_staging_passes.py   |   210 +
 .../fields.txt                                     |     1 +
 tools/nouns/ci_fitness/ci_fitness.py               |    52 +-
 tools/nouns/evidence_ref/sync_content_tree_hash.py |    10 +-
 tools/nouns/executable_shape/executable_shape.py   |     2 +
 .../fitness_adr_0039_release_binder.py             |     9 +
 tools/nouns/fitness_adr_owner_sidecar/README.md    |     2 +
 .../fitness_adr_owner_sidecar.py                   |    19 +-
 tools/nouns/fitness_control_lifecycle/README.md    |     1 +
 tools/nouns/fitness_control_lifecycle/__init__.py  |     1 +
 .../nouns/fitness_control_lifecycle/adjectives.txt |     1 +
 tools/nouns/fitness_control_lifecycle/fields.txt   |     1 +
 .../fitness_control_lifecycle.py                   |    92 +
 .../fitness_findings_shipped_tag_sync.py           |   233 +-
 .../fixtures/origin-main-current-ship.md           |     3 +
 .../fixtures/origin-main-needed-leftover.md        |     3 +
 .../fitness_known_bad_ssot.py                      |     5 +-
 .../fitness_live_self_ref_activation/README.md     |     1 +
 .../fitness_live_self_ref_activation/__init__.py   |     1 +
 .../adjectives.txt                                 |     1 +
 .../fitness_live_self_ref_activation/fields.txt    |     1 +
 .../fitness_live_self_ref_activation.py            |   148 +
 tools/nouns/fitness_mandate_inheritance/README.md  |     1 +
 .../nouns/fitness_mandate_inheritance/__init__.py  |     1 +
 .../fitness_mandate_inheritance/adjectives.txt     |     1 +
 tools/nouns/fitness_mandate_inheritance/fields.txt |     1 +
 .../fitness_mandate_inheritance.py                 |    50 +
 .../fitness_owner_key_trust.py                     |    14 +-
 .../fitness_owner_ratification_known_bad.py        |     5 +-
 .../fitness_skill_author_check_presence/README.md  |     3 +
 .../__init__.py                                    |     1 +
 .../adjectives.txt                                 |     1 +
 .../fitness_skill_author_check_presence/fields.txt |     0
 .../fitness_skill_author_check_presence.py         |    62 +
 .../nouns/fitness_skill_author_checklist/README.md |     1 +
 .../fitness_skill_author_checklist/__init__.py     |     1 +
 .../fitness_skill_author_checklist/adjectives.txt  |     1 +
 .../fitness_skill_author_checklist/fields.txt      |     0
 .../fitness_skill_author_checklist.py              |    60 +
 tools/nouns/fitness_skill_content_type/README.md   |     3 +
 tools/nouns/fitness_skill_content_type/__init__.py |     1 +
 .../fitness_skill_content_type/adjectives.txt      |     1 +
 tools/nouns/fitness_skill_content_type/fields.txt  |     0
 .../fitness_skill_content_type.py                  |    80 +
 tools/nouns/gate_activate/README.md                |     1 +
 tools/nouns/gate_activate/__init__.py              |     1 +
 tools/nouns/gate_activate/adjectives.txt           |     1 +
 tools/nouns/gate_activate/fields.txt               |     1 +
 tools/nouns/gate_activate/gate_activate.py         |   188 +
 tools/nouns/gate_set/gate_set.py                   |    27 +-
 tools/nouns/gate_stage/README.md                   |     1 +
 tools/nouns/gate_stage/__init__.py                 |     1 +
 tools/nouns/gate_stage/adjectives.txt              |     1 +
 tools/nouns/gate_stage/fields.txt                  |     1 +
 tools/nouns/gate_stage/gate_stage.py               |   127 +
 tools/nouns/hub_own_produce/hub_own_produce.py     |    79 +-
 .../link_terms_dictionary/link_terms_dictionary.py |     2 +
 tools/nouns/mandated_paths/README.md               |     1 +
 tools/nouns/mandated_paths/__init__.py             |     1 +
 tools/nouns/mandated_paths/adjectives.txt          |     1 +
 tools/nouns/mandated_paths/fields.txt              |     1 +
 tools/nouns/mandated_paths/mandated_paths.py       |   284 +
 .../nlc_release_context/nlc_release_context.py     |    26 +-
 .../nlc_release_tag_gate/nlc_release_tag_gate.py   |    22 +-
 tools/nouns/planit_identity/planit_identity.py     |    18 +
 tools/nouns/release_notes/release_notes.py         |    15 +-
 tools/nouns/self_ref_set/README.md                 |     1 +
 tools/nouns/self_ref_set/__init__.py               |     1 +
 tools/nouns/self_ref_set/adjectives.txt            |     1 +
 tools/nouns/self_ref_set/fields.txt                |     1 +
 tools/nouns/self_ref_set/self_ref_set.py           |   247 +
 tools/nouns/skill_author_check/README.md           |     3 +
 tools/nouns/skill_author_check/__init__.py         |     1 +
 tools/nouns/skill_author_check/adjectives.txt      |     1 +
 tools/nouns/skill_author_check/fields.txt          |     0
 .../nouns/skill_author_check/skill_author_check.py |   188 +
 tools/nouns/verify/verify.py                       |     9 +-
 tools/stage-gate-machinery.py                      |    13 +
 309 files changed, 19373 insertions(+), 1761 deletions(-)
```

