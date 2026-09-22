# Natural Language Coding hub v0.2.0

  v0.2.0 is the compiled-system + verify/CI hardening release: real UC product gates, SSOT-backed TODO honesty, safer hub ship mechanics, and partial v0.2 pack ingest — not full v0.2 consume/registry or ADR 0007 semantics.

## Highlights

Highlights

Compiled-system product (UC1–UC21 v1)
Use cases move from binder-only to closed product rows with machine blockers, landmine examples, and CI assert/fitness wiring: interview packet and requirements sync, ADR traceability, rule IR/runner/apply/coverage, goal-bindings and delta regen, upstream-hand-patch and generate-provenance on verify paths, durable-engine rules, non-Python adapter refusal, rule adoption conflicts, adopter verify-fast-green specimen, and related hub compliance hooks.

Verify and produce handoff
Stronger verify / verify-deep pipeline: produce-package preflight, role separation, contract/breaking/stamp gates, rule markers and skill gates, hub .nlc produce evidence, and expanded ci_fitness coverage so regressions fail in CI, not only at release.

SSOT and honesty
TODO ↔ use-case alignment (uc-product-status, todo SSOT fitness, proof index), jobs/todo sync, and process docs so “done” on compiled-system work requires evidence, not checkbox theater (incl. RCA on false UC completion).

Hub v0.2 foundations (partial)
Pack ingest product path closed in status; consume/regen after install and public registry stay out of this release (still open in product status).

Release and governance
ADR 0022 fail-early hub release flow, release preflight/notes/tag helpers, release workflow alignment, ADR 0023 rule-instance trace / instant-audit scope, ADR enforcement and rule-trace docs.

Agent harness
Portable updates to planit, verify, interview, bbp-*, requirement-pack-ingest skill, and related standing instructions for gate scope and confirmer SSOT.

Distribution
Install scripts, install hashes, and hub distribution tooling updated for the new surface area.

Explicitly not in v0.2.0

  • Full ADR 0007 semantic rule runner / apply (expansion-only; structural blockers remain).
  • UC14/UC15 v2 expansion (composable obligations, brownfield migrate automation beyond inventory).
  • Hub v0.2 consume (pack install → UC9 regen) and optional registry (out of band).

## Changes since v0.1.0

- Release v0.1.1 (`aaf6304`)
- TODO: note local v0.1.0 tag pending push. (`0e57e3a`)

### Diff stat

```
.agents/README.md                                  |   6 +-
 .agents/bbp-short-form.md                          |   4 +-
 .agents/instructions/change-version-class.md       |  19 +
 .agents/skills/README.md                           |   4 +-
 .agents/skills/bbp-confirmer/SKILL.md              |  14 +-
 .agents/skills/bbp-proposer/SKILL.md               |  14 +-
 .agents/skills/bbp-recorder/SKILL.md               |  12 +-
 .agents/skills/bbp-reviewer/SKILL.md               |  16 +-
 .agents/skills/interview/SKILL.md                  |  31 +-
 .agents/skills/planit/SKILL.md                     | 196 +++----
 .agents/skills/planit/references/README.md         |  16 +-
 .../references/audited-work-loop-standard.md       |  92 ++--
 .../planit/references/domain-first-authoring.md    |  14 +-
 .../skills/planit/references/hub-charter-loop.md   |  28 +-
 .../references/information-completion-contract.md  | 122 ++---
 .../references/knowledge-change-review-standard.md |  10 +-
 .../planit/references/lean-operating-principles.md |  28 +-
 .../local-dsi-converge-audit-template.md           |  22 +-
 .../planit/references/nlc-before-generate.md       |  16 +-
 .../references/operation-verdict-standard.md       |  82 +--
 .agents/skills/planit/references/planit-process.md |  34 +-
 .../references/root-cause-analysis-standard.md     |  62 +--
 .agents/skills/verify/SKILL.md                     |  28 +
 .cursor/hooks/nlc-goal-write-gate.sh               |  49 ++
 .cursor/hooks/nlc-session-remind.sh                |   9 +
 .github/workflows/fitness.yml                      |   3 +
 .github/workflows/release.yml                      |   3 +
 .nlc/hooks.example.json                            |  15 +
 .nlc/pipeline-state.json                           |   4 +
 .nlc/produce-package.json                          |  19 +
 .nlc/verified.json                                 |  32 ++
 .nlc/work-queue.json                               |   4 +
 AGENTS.md                                          |  32 +-
 CHARTER.md                                         | 538 +++++++++----------
 DESCRIBE.md                                        | 128 ++---
 FINDINGS.md                                        |  46 +-
 README.md                                          | 114 ++--
 TODO                                               |  88 +++-
 adrs/0001-zero-variance-integrity.md               |  30 +-
 adrs/0002-p2-scope.md                              |  18 +-
 adrs/0003-systems-extension-agent-nouns.md         |  62 +--
 adrs/0004-produce-fitness-handoff.md               |  42 +-
 adrs/0005-ssot-exit-evidence.md                    |  60 +--
 adrs/0006-contract-change-notice.md                |  28 +-
 adrs/0007-tags-primitives-reduced-adrs.md          |  54 +-
 adrs/0008-no-noun-inheritance.md                   |  18 +-
 adrs/0009-primitive-interior-functions.md          |  20 +-
 adrs/0010-gate-after-every-generate.md             |  30 +-
 adrs/0011-natural-language-coding-naming.md        |  22 +-
 adrs/0012-adr-precedence-and-rule-conflicts.md     |  10 +-
 adrs/0013-requirements-preflight.md                |  10 +-
 ...014-semver-upgrade-steps-and-noop-migrations.md |  16 +-
 adrs/0015-distribution-lock-and-version-store.md   |  18 +-
 adrs/0016-hub-carries-no-product-requirements.md   |  20 +-
 adrs/0017-human-command-surface.md                 |  44 ++
 adrs/0018-human-cli-interview-on-gap.md            |  48 ++
 adrs/0019-guided-orchestration.md                  |  33 ++
 adrs/0020-human-vs-agent-commands.md               |  43 ++
 adrs/0021-verify-fast-and-deep.md                  |  35 ++
 adrs/README.md                                     |  25 +-
 agents/README.md                                   |  34 +-
 agents/adversarial-auditor/AGENT.md                |  32 +-
 agents/adversarial-auditor/verbs.md                |  30 +-
 agents/confirmer.md                                |  16 +-
 agents/knowledge-steward/AGENT.md                  |  22 +-
 agents/knowledge-steward/verbs.md                  |  14 +-
 agents/proposer.md                                 |  12 +-
 agents/quality-architect/AGENT.md                  |  38 +-
 agents/quality-architect/verbs.md                  |  18 +-
 agents/recorder.md                                 |  10 +-
 agents/reviewer.md                                 |   8 +-
 agents/ship-role/AGENT.md                          |  42 +-
 agents/ship-role/verbs.md                          |  28 +-
 agents/standards-steward/AGENT.md                  |  48 +-
 agents/standards-steward/verbs.md                  |  46 +-
 content-types/HOW-TO-ADD.md                        | 160 +++---
 docs/LANGUAGE-SCANNER.md                           |  20 +-
 docs/OPERATING_BINDINGS.md                         |  52 +-
 docs/RISKS-AND-CONCERNS.md                         | 146 +++---
 docs/TERMS.md                                      | 571 +++++++++++++++++++++
 docs/USE-CASES.md                                  |  68 +--
 docs/adoption/BOOTSTRAP.md                         |  40 +-
 docs/adoption/BROWNFIELD.md                        |  18 +-
 docs/adoption/RELEASE-v0.1.0.md                    |  29 +-
 docs/adoption/RELEASE.md                           |  43 ++
 docs/ai-compiled-systems/AIMS-FILE-MAP.md          |  32 +-
 docs/ai-compiled-systems/ARCHITECTURE.md           |  38 +-
 docs/ai-compiled-systems/COMPILER.md               |  28 +-
 docs/ai-compiled-systems/GETTING-STARTED.md        |  15 +-
 docs/ai-compiled-systems/GLOSSARY.md               |  30 +-
 docs/ai-compiled-systems/HOW-IT-CODES.md           |  36 +-
 docs/ai-compiled-systems/INTENT-SURFACE.md         |  68 +--
 docs/ai-compiled-systems/INTERVIEW-PATTERNS.md     |  58 +--
 docs/ai-compiled-systems/MANIFESTO.md              |  34 +-
 docs/ai-compiled-systems/MERGE.md                  |  70 +--
 docs/ai-compiled-systems/MIGRATION.md              |  76 +--
 docs/ai-compiled-systems/NAMES.md                  |  18 +-
 docs/ai-compiled-systems/PLANIT-ORCHESTRATION.md   |  62 +--
 docs/ai-compiled-systems/PROCESS.md                |  68 +--
 docs/ai-compiled-systems/QUALITY-PROCESSES.md      |  42 +-
 docs/ai-compiled-systems/README.md                 |  22 +-
 docs/nlc/APP-VERIFY.md                             |  30 ++
 docs/nlc/GATE-RECORD-BINDER.md                     |  33 ++
 docs/nlc/HARNESS.md                                |  21 +-
 docs/nlc/HUMAN-JUDGMENT-GATES.md                   |  27 +
 docs/nlc/MENU.md                                   |  11 +
 docs/nlc/PROVE-AND-SHIP.md                         |  40 +-
 docs/nlc/README.md                                 |  42 +-
 docs/nlc/REQUIREMENT-PACKS.md                      |  10 +-
 docs/nlc/VERIFY-AND-SHIP.md                        |  38 ++
 docs/spine/IMPACT-GRAPH.md                         |  22 +-
 docs/spine/README.md                               |  10 +-
 docs/worked-examples/pan-handling/README.md        |  18 +-
 examples/README.md                                 |  42 +-
 examples/adjective-untested/README.md              |   2 +-
 examples/adjectives-in-goal/README.md              |   2 +-
 examples/agent-ratified/CONFIRM.md                 |   4 +-
 examples/agent-ratified/README.md                  |   2 +-
 examples/breaking-no-adr/README.md                 |   2 +-
 examples/c22-na-with-both/CHARTER.md               |   2 +-
 examples/c22-na-with-both/CONFIRM.md               |   6 +-
 examples/c22-na-with-both/README.md                |   2 +-
 examples/card-taint-alias/README.md                |   2 +-
 examples/card-taint-crossfile/README.md            |   2 +-
 examples/card-taint-helper/README.md               |   2 +-
 examples/card-taint-violation/README.md            |   6 +-
 examples/changed-missing-schema/CONFIRM.md         |   2 +-
 examples/changed-missing-schema/README.md          |   2 +-
 examples/changed-only-ok/CONFIRM.md                |   2 +-
 examples/changed-only-ok/README.md                 |   2 +-
 examples/class-c-on-charter/CHARTER.md             |   2 +-
 examples/class-c-on-charter/CONFIRM.md             |   6 +-
 examples/class-c-on-charter/README.md              |   2 +-
 examples/confirmer-open-fail/CONFIRM.md            |   2 +-
 examples/confirmer-open-fail/README.md             |   2 +-
 examples/copied-goal-helper/README.md              |   2 +-
 examples/duplicated-adjective-violation/README.md  |   8 +-
 examples/extra-goal-entrypoint/README.md           |   2 +-
 examples/goal-test-no-call/README.md               |   2 +-
 examples/goal-tests-copy-adjectives/README.md      |   2 +-
 examples/goal-untested/README.md                   |   2 +-
 examples/impact-list-mismatch/CONFIRM.md           |   2 +-
 examples/impact-list-mismatch/README.md            |   2 +-
 examples/imported-goal-helper/README.md            |   2 +-
 examples/invoice-correct/CONFIRM.md                |  54 +-
 examples/invoice-correct/README.md                 |   2 +-
 examples/invoice-escape-hatch-violation/README.md  |   2 +-
 examples/invoice-locality-violation/README.md      |   4 +-
 examples/invoice-verb-path-violation/README.md     |   4 +-
 examples/invoice-violation/README.md               |   8 +-
 examples/mention-only-verb/README.md               |   2 +-
 examples/missing-c22/CONFIRM.md                    |   4 +-
 examples/missing-c22/README.md                     |   2 +-
 examples/missing-change-class/CONFIRM.md           |   4 +-
 examples/missing-change-class/README.md            |   2 +-
 examples/missing-contract/README.md                |   4 +-
 examples/missing-failure-mode/README.md            |   4 +-
 examples/noun-retries/README.md                    |   2 +-
 examples/noun-without-tests/README.md              |   2 +-
 examples/open-findings/FINDINGS.md                 |   2 +-
 examples/open-findings/README.md                   |   2 +-
 examples/orchestration-on-noun/README.md           |   2 +-
 examples/product-no-confirm/README.md              |   2 +-
 .../.nlc/delta-regen-queue.json                    |  13 +
 examples/regen-queue-pending/README.md             |   5 +
 examples/retrying-goal/README.md                   |   2 +-
 examples/retrying-key-unused/README.md             |   2 +-
 examples/retrying-nested-no-key/README.md          |   2 +-
 examples/retrying-no-key/README.md                 |   2 +-
 examples/schema-field-missing/README.md            |   2 +-
 examples/schema-identity-violation/README.md       |   6 +-
 examples/schema-type-mismatch/README.md            |   2 +-
 examples/schema-unannotated/README.md              |   2 +-
 examples/sql-escape-hatch/README.md                |   2 +-
 examples/stray-verb/README.md                      |   2 +-
 examples/unsigned-class-a/CONFIRM.md               |   2 +-
 examples/unsigned-class-a/README.md                |   2 +-
 examples/unversioned-contract/README.md            |   2 +-
 examples/verb-no-preserve/README.md                |   2 +-
 examples/verb-success-only/README.md               |   2 +-
 examples/verb-untested/README.md                   |   2 +-
 examples/version-bump-no-adr/README.md             |   2 +-
 examples/workflow-as-goal/README.md                |   2 +-
 examples/wrapper-goal/README.md                    |   2 +-
 integrity/ACTIONS.md                               | 162 +++---
 integrity/BOUNDARY.md                              | 242 ++++-----
 integrity/BOUNDED_CONTEXT.md                       |  62 +--
 integrity/CONTRIBUTION.md                          | 150 +++---
 integrity/GATE.md                                  | 150 +++---
 integrity/KNOWLEDGE-FACTS.md                       |   8 +-
 integrity/LEXICON.md                               |  94 ++--
 integrity/PRINCIPLES.md                            |  58 +--
 integrity/QUALITY_METRIC.md                        | 152 +++---
 integrity/README.md                                |  22 +-
 integrity/audits/A-C1.md                           |  12 +-
 integrity/audits/A-C10.md                          |   8 +-
 integrity/audits/A-C11.md                          |   6 +-
 integrity/audits/A-C12.md                          |  10 +-
 integrity/audits/A-C13.md                          |  12 +-
 integrity/audits/A-C14.md                          |   8 +-
 integrity/audits/A-C15.md                          |  10 +-
 integrity/audits/A-C16.md                          |  10 +-
 integrity/audits/A-C17.md                          |  12 +-
 integrity/audits/A-C18.md                          |  10 +-
 integrity/audits/A-C19.md                          |   8 +-
 integrity/audits/A-C2.md                           |  10 +-
 integrity/audits/A-C20.md                          |   6 +-
 integrity/audits/A-C21.md                          |   6 +-
 integrity/audits/A-C22.md                          |   6 +-
 integrity/audits/A-C23.md                          |   8 +-
 integrity/audits/A-C24.md                          |   8 +-
 integrity/audits/A-C25.md                          |   6 +-
 integrity/audits/A-C26.md                          |   6 +-
 integrity/audits/A-C3.md                           |  12 +-
 integrity/audits/A-C4.md                           |  14 +-
 integrity/audits/A-C5.md                           |   8 +-
 integrity/audits/A-C6.md                           |  12 +-
 integrity/audits/A-C7.md                           |   6 +-
 integrity/audits/A-C8.md                           |   6 +-
 integrity/audits/A-C9.md                           |   6 +-
 integrity/audits/A-CS1.md                          |  10 +-
 integrity/audits/A-CS10.md                         |  14 +-
 integrity/audits/A-CS2.md                          |   8 +-
 integrity/audits/A-CS3.md                          |   8 +-
 integrity/audits/A-CS4.md                          |   8 +-
 integrity/audits/A-CS5.md                          |  10 +-
 integrity/audits/A-CS6.md                          |  10 +-
 integrity/audits/A-CS7.md                          |  12 +-
 integrity/audits/A-CS8.md                          |  14 +-
 integrity/audits/A-CS9.md                          |  28 +-
 integrity/audits/A-P1.md                           |  10 +-
 integrity/audits/A-P2.md                           |   8 +-
 integrity/audits/A-P3.md                           |  10 +-
 integrity/audits/A-P4.md                           |   8 +-
 integrity/audits/A-P5.md                           |  10 +-
 integrity/audits/A-Q1.md                           |  26 +-
 integrity/audits/A-Q2.md                           |  14 +-
 integrity/audits/A-Q3.md                           |  18 +-
 integrity/audits/A-Q4.md                           |  18 +-
 integrity/audits/A-Q5.md                           |  22 +-
 integrity/audits/A-R1.md                           |   8 +-
 integrity/audits/A-R10.md                          |   8 +-
 integrity/audits/A-R11.md                          |   8 +-
 integrity/audits/A-R12.md                          |  12 +-
 integrity/audits/A-R13.md                          |  10 +-
 integrity/audits/A-R14.md                          |  10 +-
 integrity/audits/A-R15.md                          |   8 +-
 integrity/audits/A-R16.md                          |   8 +-
 integrity/audits/A-R17.md                          |  14 +-
 integrity/audits/A-R18.md                          |  12 +-
 integrity/audits/A-R19.md                          |  12 +-
 integrity/audits/A-R2.md                           |   8 +-
 integrity/audits/A-R20.md                          |   8 +-
 integrity/audits/A-R21.md                          |   4 +-
 integrity/audits/A-R22.md                          |  10 +-
 integrity/audits/A-R23.md                          |  10 +-
 integrity/audits/A-R24.md                          |  14 +-
 integrity/audits/A-R25.md                          |  10 +-
 integrity/audits/A-R26.md                          |  10 +-
 integrity/audits/A-R3.md                           |   8 +-
 integrity/audits/A-R30.md                          |  10 +-
 integrity/audits/A-R31.md                          |  10 +-
 integrity/audits/A-R32.md                          |   8 +-
 integrity/audits/A-R33.md                          |   8 +-
 integrity/audits/A-R4.md                           |  10 +-
 integrity/audits/A-R5.md                           |  18 +-
 integrity/audits/A-R6.md                           |   8 +-
 integrity/audits/A-R7.md                           |  10 +-
 integrity/audits/A-R8.md                           |  10 +-
 integrity/audits/A-R9.md                           |  12 +-
 integrity/audits/A-S1.md                           |  12 +-
 integrity/audits/A-S2.md                           |  16 +-
 integrity/audits/A-S3.md                           |  12 +-
 integrity/audits/A-S4.md                           |  12 +-
 integrity/audits/A-S5.md                           |  18 +-
 integrity/audits/A-S6.md                           |  16 +-
 integrity/audits/A-S7.md                           |  22 +-
 integrity/audits/A-S8.md                           |  22 +-
 integrity/audits/A5-TAINT.md                       |   2 +-
 integrity/audits/A7-ESCAPE.md                      |   2 +-
 integrity/audits/README.md                         |   2 +-
 integrity/binding-matrix.md                        |  24 +-
 integrity/nlc-install-hashes.json                  |  42 +-
 integrity/nlc-version.json                         |   2 +-
 integrity/primitives.md                            |  12 +-
 integrity/schemas/nlc-verified.schema.json         |  17 +
 integrity/schemas/nlc-work-queue.schema.json       |  27 +
 migrations/0.1.0_to_0.1.1/migration.yaml           |   3 +
 migrations/README.md                               |   8 +-
 nlc                                                |   5 +
 nlc.cmd                                            |   6 +
 release                                            |   4 +
 scripts/install.ps1                                |  35 +-
 scripts/install.sh                                 |  28 +-
 scripts/nlc-launcher.sh                            |   6 +
 scripts/nlc-release-prep.sh                        |  13 +-
 scripts/nlc-release-smoke.sh                       |   6 +-
 scripts/nlc-release.sh                             | 189 +++++++
 templates/adopter/README.md                        |  25 +-
 templates/adopter/change-adversarial.json.example  |  11 +
 templates/adopter/github-workflows-nlc-prove.yml   |  29 +-
 templates/adopter/github-workflows-nlc-verify.yml  |  27 +
 templates/adopter/hooks.example.json               |  15 +
 templates/adopter/nlc                              |  14 +
 templates/adopter/nlc.cmd                          |  10 +
 templates/adopter/verify-suite.json.example        |   5 +
 tools/README.md                                    |  12 +-
 tools/assert-batch-generate-policy-fails.py        |  29 ++
 tools/assert-verify-gate-record-fails.py           |  30 ++
 tools/assert-verify-regen-queue-fails.py           |  34 ++
 tools/changeset.py                                 |  13 +-
 tools/ci_fitness.py                                |  29 ++
 tools/fitness-c1.py                                |   5 +-
 tools/fitness-c24.py                               |   3 +-
 tools/fitness-contract-presence.py                 |   2 +-
 tools/fitness-r13-entrypoints.py                   |   2 +-
 tools/link-terms-dictionary.py                     | 288 +++++++++++
 tools/markdown_plain.py                            |  11 +
 tools/nlc-brownfield-inventory.py                  |   4 +
 tools/nlc-init.py                                  |  38 +-
 tools/nlc-install-hash-update.py                   |   5 +
 tools/nlc-install-verify.py                        |  25 +-
 tools/nlc-pack-export.py                           |  10 +-
 tools/nlc-pack-install.py                          |  21 +-
 tools/nlc-release-build.py                         |   2 +
 tools/nlc-update.py                                |  17 +-
 tools/nlc.py                                       | 422 +++++++++++++++
 tools/nlc_adr_scan.py                              |  22 +
 tools/nlc_cli_help.py                              |  58 +++
 tools/nlc_compliance.py                            | 242 +++++++++
 tools/nlc_dashboard.py                             | 362 +++++++++++++
 tools/nlc_distribution.py                          |   6 +-
 tools/nlc_gate_record.py                           |  98 ++++
 tools/nlc_guide_cmd.py                             |  78 +++
 tools/nlc_guide_state.py                           |  94 ++++
 tools/nlc_human_gap.py                             |  28 +
 tools/nlc_menu_data.py                             |  44 ++
 tools/nlc_pipeline.py                              | 108 ++++
 tools/nlc_plan_audit.py                            |  60 +++
 tools/nlc_preflight.py                             |  62 +++
 tools/nlc_produce_package.py                       |  80 +++
 tools/nlc_regen_continue.py                        |  88 ++++
 tools/nlc_release_bump.py                          | 209 ++++++++
 tools/nlc_requirements.py                          |  10 +-
 tools/nlc_requirements_cmd.py                      |  90 ++++
 tools/nlc_verify.py                                | 216 ++++++++
 tools/release-audit.py                             |   3 +-
 347 files changed, 7738 insertions(+), 3283 deletions(-)
```

---

Draft commits/range from `python3 tools/nlc_release_notes.py --write-draft --version 0.2.0 --to HEAD`. Edit **Highlights** before merge; `./release finish` refuses to tag without them.
