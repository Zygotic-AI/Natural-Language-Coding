# Natural Language Compiler hub v0.6.0

## Highlights

Hub **v0.6.0** is a minor on **v0.5.0**. Same class as adding the locks (v0.4.0). **v1.0.0** stays parked for dogfood.

- **Six-step unsigned hub release (ADR 0058).** A `release/<semver>` branch exists; work merges into it; `./release` checks everything and lists sensitive files; never sign after that; merge to `main`; tag. Merge is accept. Zero GPG.
- **Sensitive-file list replaces signatures.** Graded by `origin/main`'s copy of `tools/nlc_release_sensitive_review.py`. Revert, edit, or accept by merging. Stay on that step until the list is resolved.
- **CONTROL-LIFECYCLE is create, change, list, accept, merge.** Staging-plus-armor and mandate pins are not ship gates.
- **C24 is the GitHub merge commit.** No sidecar, no `Released-by:` as a ship gate. Highlights text is not a tag blocker.
- **Supersedes ADR 0052 / 0055 / 0056 / 0057.** ADR 0051 bytes stay. Live armor, `scripts/sign-adrs.sh`, and signature fitness are gone.

## Changes since v0.5.0

- Regenerate unsigned derived hashes after rebase onto v0.5.0. (`3936b7c`)
- Keep the release skill links inside the skills tree. (`91fb94d`)
- Reclass ADR 0058 from major to minor. (`ad10eda`)
- Accept ADR 0058 and implement the six-step unsigned hub release. (`1334813`)
- Propose ADR 0058: six-step unsigned hub release. (`9e4bffa`)

### Diff stat

```
.agents/instructions/signature-text-handoff.md     |  34 --
 .agents/skills/planit/SKILL.md                     |  14 +-
 .../references/audited-work-loop-standard.md       |   4 +-
 .agents/skills/release/SKILL.md                    | 138 +----
 .cursor/rules/signature-text-handoff.mdc           |  13 -
 .nlc/before-generate-stamp.json                    |   7 +-
 .nlc/briefs/hub-material-0051-0052.md              |   6 +-
 .nlc/produce-package.json                          |  32 +-
 AGENTS.md                                          |   2 -
 DESCRIBE.md                                        |   2 +-
 TODO                                               |  18 +
 adrs/0001-zero-variance-integrity.md.asc           |   7 -
 adrs/0002-p2-scope.md.asc                          |   7 -
 adrs/0003-systems-extension-agent-nouns.md.asc     |   7 -
 adrs/0004-produce-fitness-handoff.md.asc           |   7 -
 adrs/0005-ssot-exit-evidence.md.asc                |   7 -
 adrs/0006-contract-change-notice.md.asc            |   7 -
 adrs/0007-tags-primitives-reduced-adrs.md.asc      |   7 -
 adrs/0008-no-noun-inheritance.md.asc               |   7 -
 adrs/0009-primitive-interior-functions.md.asc      |   7 -
 adrs/0010-gate-after-every-generate.md.asc         |   7 -
 adrs/0011-natural-language-coding-naming.md.asc    |   7 -
 adrs/0012-rule-adoption-conflicts.md.asc           |   7 -
 adrs/0013-requirements-preflight.md.asc            |   7 -
 ...semver-upgrade-steps-and-noop-migrations.md.asc |   7 -
 ...0015-distribution-lock-and-version-store.md.asc |   7 -
 ...0016-hub-carries-no-product-requirements.md.asc |   7 -
 adrs/0017-human-command-surface.md.asc             |   7 -
 adrs/0018-human-cli-interview-on-gap.md.asc        |   7 -
 adrs/0019-guided-orchestration.md.asc              |   7 -
 adrs/0020-human-vs-agent-commands.md.asc           |   7 -
 adrs/0021-verify-fast-and-deep.md.asc              |   7 -
 adrs/0022-hub-release-fail-early.md.asc            |   7 -
 ...e-instance-trace-and-instant-audit-scope.md.asc |   7 -
 adrs/0024-nlc-factory-spine.md.asc                 |   7 -
 adrs/0025-belief-no-blame-climb.md.asc             |   7 -
 adrs/0026-promote-x1-x3-runners.md.asc             |   7 -
 adrs/0027-emit-from-prose.md.asc                   |   7 -
 ...d-atomic-verb-set-and-policy-adr-lineage.md.asc |   7 -
 ...adr-lineage-active-set-and-bind-snapshot.md.asc |   7 -
 adrs/0030-pipeline-wiring.md.asc                   |   7 -
 adrs/0031-charter-ratification-program.md.asc      |   7 -
 adrs/0032-charter-ownership-and-mutation.md.asc    |   7 -
 adrs/0033-charter-contracts.md.asc                 |   7 -
 .../0034-charter-goal-shape-and-composition.md.asc |   7 -
 adrs/0035-charter-knowledge-and-enforcement.md.asc |   7 -
 adrs/0036-inference-only-human-surface.md.asc      |   7 -
 adrs/0037-charter-non-r-surfaces.md.asc            |   7 -
 adrs/0038-no-memory-in-process.md.asc              |   7 -
 adrs/0039-single-command-human-surfaces.md.asc     |   7 -
 adrs/0040-process-preflight-remediation.md.asc     |   7 -
 adrs/0041-product-completion-scope.md.asc          |   7 -
 adrs/0042-rule-ir-hub-product-boundary.md.asc      |   7 -
 adrs/0043-uc14-composable-adopt-boundary.md.asc    |   7 -
 adrs/0044-hub-release-production-trunk.md.asc      |   7 -
 adrs/0045-hub-release-identity.md.asc              |   7 -
 adrs/0046-repository-planit-identity.md.asc        |   7 -
 adrs/0047-adr-approval-receipts.md.asc             |   7 -
 adrs/0048-executable-shape.md.asc                  |   7 -
 adrs/0049-release-planner-owns-stops.md.asc        |   7 -
 ...50-evidence-identity-content-not-history.md.asc |   7 -
 adrs/0051-hub-own-produce-principles.md.asc        |   7 -
 .../0052-owner-openpgp-ratification-amends-0051.md |   3 +-
 ...2-owner-openpgp-ratification-amends-0051.md.asc |   7 -
 adrs/0053-0051-0052-text-retrofit.md.asc           |   7 -
 ...54-published-skill-author-contract.approval.asc |  17 -
 adrs/0054-published-skill-author-contract.md.asc   |   7 -
 adrs/0055-staged-activation-of-gate-machinery.md   |   3 +-
 ...0055-staged-activation-of-gate-machinery.md.asc |   7 -
 adrs/0056-per-file-adr-detached-signatures.md      |   3 +-
 adrs/0056-per-file-adr-detached-signatures.md.asc  |   7 -
 adrs/0057-tag-time-checker-digest.md               |   3 +-
 adrs/0058-six-step-unsigned-release.md             | 275 ++++++++++
 adrs/ACTIVE.md                                     |   2 +-
 adrs/CATALOG.md                                    |   9 +-
 adrs/INDEX.md                                      |   9 +-
 adrs/README.md                                     |   9 +-
 adrs/owner-approvals/staged-signing.approval.asc   |  21 -
 docs/ADR-ENFORCEMENT.md                            |   2 +-
 docs/adoption/RELEASE.md                           |  83 +--
 docs/nlc/HUMAN-JUDGMENT-GATES.md                   |   6 +-
 goals/hub_release/execute.sh                       |  14 +-
 goals/sign_adrs/execute.sh                         | 273 ----------
 integrity/adr-0051-0052-rules.json                 | 138 ++---
 integrity/adr-gates.json                           |   4 +
 integrity/audits/A-C24.md                          |  10 +-
 integrity/check-inputs.json                        | 272 +++-------
 integrity/checker-digest.sha256                    |   2 +-
 integrity/checker-digest.sha256.approval.asc       |  16 -
 integrity/gate-set-baseline.manifest.sha256        | 283 ++++-------
 .../gate-set-baseline.manifest.sha256.approval.asc |  17 -
 integrity/hub-content-tree-hash.txt                |   2 +-
 integrity/hub-stamp-scopes.json                    |   3 +-
 integrity/hub-x4-remainder.json                    | 102 +++-
 integrity/mandated-paths.json                      | 560 +++++----------------
 integrity/nlc-install-hashes.json                  |   4 +-
 integrity/planit-skill-registry.json               |   2 +-
 integrity/releasable-gates.json                    |   9 +-
 integrity/self-ref-set.json                        |   2 -
 integrity/skill-author-checklist.json              |   5 -
 scripts/sign-adrs.sh                               |   5 -
 tools/assert-activation-split-land-fails.py        |  13 -
 ...ange-does-not-trip-gate-set-signature-passes.py |  12 -
 ...sert-gate-set-manifest-missing-sidecar-fails.py |  43 --
 tools/assert-live-self-ref-direct-edit-fails.py    |  13 -
 .../assert-mandate-skill-without-registry-fails.py |  13 -
 tools/assert-release-probe-sig-ok-fails.py         |  12 -
 tools/assert-release-probe-sig-ok-passes.py        |  12 -
 tools/assert-release-signed-passes.py              |  13 -
 tools/assert-release-unsigned-fails.py             |  13 -
 ... => assert-sensitive-review-doc-only-passes.py} |   6 +-
 ...ls.py => assert-sensitive-review-hide-fails.py} |   5 +-
 ...es.py => assert-sensitive-review-self-fails.py} |   5 +-
 .../assert-tag-digest-signature-required-fails.py  |  13 -
 ...-machinery.py => assert-unsigned-tag-passes.py} |   5 +-
 tools/assert-verifier-change-via-staging-passes.py |  13 -
 tools/check-checker-digest-signature.py            |  42 --
 tools/fitness-live-self-ref-activation.py          |  13 -
 tools/fitness-mandate-inheritance.py               |  13 -
 tools/fitness-owner-key-trust.py                   |  13 -
 tools/fitness-owner-ratification-known-bad.py      |  13 -
 tools/fitness-retired-key-denylist.py              |  13 -
 ...writes-ratification.py => fitness-sign-stop.py} |   5 +-
 tools/nlc_release_sensitive_review.py              |  14 +
 tools/nouns/adr_approval/adr_approval.py           |  10 +-
 tools/nouns/adr_record_gate/adr_record_gate.py     |   2 +-
 .../assert_activation_split_land_fails/README.md   |   1 -
 .../assert_activation_split_land_fails/__init__.py |   1 -
 .../adjectives.txt                                 |   1 -
 .../assert_activation_split_land_fails.py          |  90 ----
 .../assert_activation_split_land_fails/fields.txt  |   1 -
 .../nouns/assert_adr_detached_sig_fails/README.md  |   9 -
 .../assert_adr_detached_sig_fails/__init__.py      |   1 -
 .../assert_adr_detached_sig_fails/adjectives.txt   |   1 -
 .../assert_adr_detached_sig_fails.py               | 217 --------
 .../nouns/assert_adr_detached_sig_fails/fields.txt |   1 -
 .../README.md                                      |   3 -
 .../__init__.py                                    |   1 -
 .../adjectives.txt                                 |   1 -
 ...ange_does_not_trip_gate_set_signature_passes.py | 114 -----
 .../fields.txt                                     |   1 -
 .../README.md                                      |   3 -
 .../__init__.py                                    |   1 -
 .../adjectives.txt                                 |   1 -
 ..._gate_set_manifest_placeholder_sidecar_fails.py | 122 -----
 .../fields.txt                                     |   1 -
 .../assert_hub_only_fitness_scope_passes.py        |  13 +-
 .../README.md                                      |   1 -
 .../__init__.py                                    |   1 -
 .../adjectives.txt                                 |   1 -
 .../assert_live_self_ref_direct_edit_fails.py      |  68 ---
 .../fields.txt                                     |   1 -
 .../README.md                                      |   1 -
 .../__init__.py                                    |   1 -
 .../adjectives.txt                                 |   1 -
 .../assert_mandate_skill_without_registry_fails.py |  70 ---
 .../fields.txt                                     |   1 -
 .../assert_release_probe_fail_closed.py            |   3 -
 tools/nouns/assert_release_signed_passes/README.md |   3 -
 .../nouns/assert_release_signed_passes/__init__.py |   2 -
 .../assert_release_signed_passes/adjectives.txt    |   1 -
 .../assert_release_signed_passes.py                |  44 --
 .../nouns/assert_release_signed_passes/fields.txt  |   1 -
 .../nouns/assert_release_unsigned_fails/README.md  |   3 -
 .../assert_release_unsigned_fails/__init__.py      |   2 -
 .../assert_release_unsigned_fails/adjectives.txt   |   1 -
 .../assert_release_unsigned_fails.py               |  37 --
 .../nouns/assert_release_unsigned_fails/fields.txt |   1 -
 .../README.md                                      |   1 +
 .../__init__.py                                    |   1 +
 .../adjectives.txt                                 |   1 +
 .../assert_sensitive_review_doc_only_passes.py     |  28 ++
 .../fields.txt                                     |   1 +
 .../schemas/verbs.schema.json                      |   0
 .../assert_sensitive_review_hide_fails/README.md   |   1 +
 .../assert_sensitive_review_hide_fails/__init__.py |   1 +
 .../adjectives.txt                                 |   1 +
 .../assert_sensitive_review_hide_fails.py          |  41 ++
 .../assert_sensitive_review_hide_fails/fields.txt  |   1 +
 .../schemas/verbs.schema.json                      |   0
 .../assert_sensitive_review_self_fails/README.md   |   1 +
 .../assert_sensitive_review_self_fails/__init__.py |   1 +
 .../adjectives.txt                                 |   1 +
 .../assert_sensitive_review_self_fails.py          |  31 ++
 .../assert_sensitive_review_self_fails/fields.txt  |   1 +
 .../schemas/verbs.schema.json                      |  10 +
 .../nouns/assert_sign_adrs_script_passes/README.md |   3 -
 .../assert_sign_adrs_script_passes/__init__.py     |   1 -
 .../assert_sign_adrs_script_passes/adjectives.txt  |   1 -
 .../assert_sign_adrs_script_passes.py              | 264 ----------
 .../assert_sign_adrs_script_passes/fields.txt      |   1 -
 .../assert_tag_digest_signature_required_fails.py  |  68 ---
 tools/nouns/assert_unsigned_tag_passes/README.md   |   1 +
 tools/nouns/assert_unsigned_tag_passes/__init__.py |   1 +
 .../assert_unsigned_tag_passes/adjectives.txt      |   1 +
 .../assert_unsigned_tag_passes.py                  |  25 +
 tools/nouns/assert_unsigned_tag_passes/fields.txt  |   1 +
 .../schemas/verbs.schema.json                      |  10 +
 .../README.md                                      |   1 -
 .../__init__.py                                    |   1 -
 .../adjectives.txt                                 |   1 -
 .../assert_verifier_change_via_staging_passes.py   | 210 --------
 .../fields.txt                                     |   1 -
 tools/nouns/checker_digest/checker_digest.py       |   1 -
 tools/nouns/ci_fitness/ci_fitness.py               |  72 +--
 .../fitness_adr_0051_0052_rules.py                 |   2 +-
 .../fitness_adr_owner_sidecar.py                   |  11 +-
 .../fitness_control_lifecycle.py                   |  21 +-
 .../fitness_known_bad_ssot.py                      |   2 +-
 .../fitness_live_self_ref_activation/README.md     |   1 -
 .../fitness_live_self_ref_activation/__init__.py   |   1 -
 .../adjectives.txt                                 |   1 -
 .../fitness_live_self_ref_activation/fields.txt    |   1 -
 .../fitness_live_self_ref_activation.py            | 150 ------
 tools/nouns/fitness_mandate_inheritance/README.md  |   1 -
 .../nouns/fitness_mandate_inheritance/__init__.py  |   1 -
 .../fitness_mandate_inheritance/adjectives.txt     |   1 -
 tools/nouns/fitness_mandate_inheritance/fields.txt |   1 -
 .../fitness_mandate_inheritance.py                 |  50 --
 tools/nouns/fitness_sign_stop/README.md            |   1 +
 tools/nouns/fitness_sign_stop/__init__.py          |   1 +
 tools/nouns/fitness_sign_stop/adjectives.txt       |   1 +
 tools/nouns/fitness_sign_stop/fields.txt           |   1 +
 tools/nouns/fitness_sign_stop/fitness_sign_stop.py |  57 +++
 .../fitness_sign_stop/schemas/verbs.schema.json    |  10 +
 tools/nouns/hub_own_produce/hub_own_produce.py     |   2 +-
 tools/nouns/nlc_release_state/nlc_release_state.py |   3 +-
 .../nlc_release_tag_gate/nlc_release_tag_gate.py   |  69 ---
 tools/nouns/sensitive_review/README.md             |   1 +
 tools/nouns/sensitive_review/__init__.py           |   1 +
 tools/nouns/sensitive_review/adjectives.txt        |   1 +
 tools/nouns/sensitive_review/fields.txt            |   1 +
 .../sensitive_review/schemas/verbs.schema.json     |  10 +
 tools/nouns/sensitive_review/sensitive_review.py   | 213 ++++++++
 .../nouns/skill_author_check/skill_author_check.py |   4 +-
 235 files changed, 1363 insertions(+), 4030 deletions(-)
```

