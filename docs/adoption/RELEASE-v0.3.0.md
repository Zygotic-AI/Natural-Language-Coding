# Natural Language Coding hub v0.3.0

## Highlights

Hub **v0.3.0** is the zero-parameter ship path. Adopters and hub maintainers run **`./release`** with no `--bump` and no branch menu. The orchestrator infers the next version, the `release/v*` line, and the bump class from git state (ADR 0039, ADR 0044).

- **Production trunk.** `main` stays at the last shipped tag. Unreleased work stays on `release/v*`. `./release` resets local `main` to that tag only when `origin/main` is already the shipped tag. It does not stash, detach the checkout, or move an existing tag.
- **Resume matches the remote.** `./release` waits for a pull-request merge only after `release/v*` exists on `origin`. A local-only release branch continues prepare instead of polling for a merge that was never pushed.
- **One release identity.** The planner names the version, the `release/v*` branch, and the tag. A merged pull request is not tagged when the version file, release record, and branch disagree (ADR 0045). The tag command names the merge commit. An existing tag is not moved.
- **Shipped baseline is the peeled tag commit.** Annotated tag object ids are not treated as a different release. Trunk normalize, verify-deep, and the shipped-tag audit use that commit. Baseline verify-deep runs in a separate worktree, so the release branch stays checked out.
- **NOT_MET is actionable.** Remediation comes from the tool. Agents fix the cited gate or re-run `./release`. They do not tell operators to ignore defective output.

**Explicitly not in v0.3.0**

- A new compiled-system use-case wave beyond v0.2.0.
- Pushing or force-moving the remote `main` or remote tags from trunk normalize.

## Changes since v0.2.0

- Release v0.3.0 (`0ca1bce`)

### Diff stat

```
.agents/instructions/jidoka-ssot-output.md         |  28 ++
 .agents/skills/release/SKILL.md                    |  22 +-
 .github/workflows/release.yml                      |   2 +
 .nlc/verified.json                                 |   7 +-
 AGENTS.md                                          |   2 +
 adrs/0039-single-command-human-surfaces.md         |   2 +
 adrs/0044-hub-release-production-trunk.md          |  53 +++
 adrs/INDEX.md                                      |   1 +
 docs/adoption/M-v0.2.0-closeout-notes.md           |  35 ++
 docs/adoption/RELEASE-PRODUCTION-TRUNK-PLAN.md     | 281 +++++++++++
 docs/adoption/RELEASE-SINGLE-PATH-PLAN.md          | 179 +++++++
 docs/adoption/RELEASE-TRUNK-SMOKE.md               |  31 ++
 docs/adoption/RELEASE-ZERO-PARAMS-PLAN.md          |  29 ++
 docs/adoption/RELEASE-v0.3.0.md                    |  23 +
 docs/adoption/RELEASE.md                           |  71 ++-
 ...-09-25-agent-counseled-ignore-tooling-defect.md | 101 ++++
 ...9-25-release-infer-re-offers-shipped-version.md | 104 +++++
 ...09-25-release-not-met-fetch-only-remediation.md |  97 ++++
 ...09-25-release-tag-gate-zero-shipped-baseline.md | 106 +++++
 ...25-stale-release-branches-semantics-overload.md | 100 ++++
 ...9-25-tag-pushed-no-github-release-shallow-ci.md | 124 +++++
 ...trunk-normalize-local-tag-not-remote-shipped.md | 114 +++++
 integrity/hub-release-record.json                  |   6 +-
 integrity/hub-x4-remainder.json                    |  74 ++-
 integrity/nlc-install-hashes.json                  |   2 +-
 migrations/0.2.0_to_0.3.0/migration.yaml           |   3 +
 scripts/nlc-release.sh                             | 513 +++++++++++++++------
 tools/assert-jidoka-ssot-agents-link-passes.py     |  12 +
 tools/assert-release-infer-passes.py               |  12 +
 tools/assert-release-main-purity-passes.py         |  12 +
 ...ssert-release-main-purity-remediation-passes.py |  11 +
 tools/nlc_release_context.py                       |   9 +-
 tools/nlc_release_infer.py                         |  14 +
 tools/nlc_release_main_purity.py                   |  16 +
 tools/nlc_release_remediate.py                     |  48 ++
 tools/nlc_release_resume.py                        |  70 ++-
 tools/nlc_release_shipped_tag_audit.py             |  40 +-
 .../nouns/assert_jidoka_ssot_agents_link/README.md |   3 +
 .../assert_jidoka_ssot_agents_link/__init__.py     |   1 +
 .../assert_jidoka_ssot_agents_link/adjectives.txt  |   2 +
 .../assert_jidoka_ssot_agents_link.py              |  53 +++
 .../assert_jidoka_ssot_agents_link/fields.txt      |   1 +
 .../schemas/verbs.schema.json                      |  10 +
 tools/nouns/assert_release_infer_passes/README.md  |   3 +
 .../nouns/assert_release_infer_passes/__init__.py  |   1 +
 .../assert_release_infer_passes/adjectives.txt     |   2 +
 .../assert_release_infer_passes.py                 |  62 +++
 tools/nouns/assert_release_infer_passes/fields.txt |   1 +
 .../schemas/verbs.schema.json                      |  10 +
 .../assert_release_main_purity_passes/README.md    |   3 +
 .../assert_release_main_purity_passes/__init__.py  |   1 +
 .../adjectives.txt                                 |   2 +
 .../assert_release_main_purity_passes.py           |  28 ++
 .../assert_release_main_purity_passes/fields.txt   |   1 +
 .../schemas/verbs.schema.json                      |  10 +
 .../README.md                                      |   3 +
 .../__init__.py                                    |   1 +
 .../adjectives.txt                                 |   2 +
 .../assert_release_main_purity_remediation.py      |  33 ++
 .../fields.txt                                     |   1 +
 .../schemas/verbs.schema.json                      |  10 +
 .../assert_release_resume_invariant_passes.py      |  23 +-
 tools/nouns/ci_fitness/ci_fitness.py               |  16 +
 .../fitness_adr_0039_release_binder.py             |  65 ++-
 tools/nouns/release_infer/README.md                |   3 +
 tools/nouns/release_infer/__init__.py              |   1 +
 tools/nouns/release_infer/adjectives.txt           |   2 +
 tools/nouns/release_infer/fields.txt               |   1 +
 tools/nouns/release_infer/release_infer.py         | 313 +++++++++++++
 .../nouns/release_infer/schemas/verbs.schema.json  |  10 +
 tools/nouns/release_main_purity/README.md          |   3 +
 tools/nouns/release_main_purity/__init__.py        |   1 +
 tools/nouns/release_main_purity/adjectives.txt     |   2 +
 tools/nouns/release_main_purity/fields.txt         |   1 +
 .../release_main_purity/release_main_purity.py     | 117 +++++
 .../release_main_purity/schemas/verbs.schema.json  |  10 +
 tools/nouns/release_remediate/README.md            |   3 +
 tools/nouns/release_remediate/__init__.py          |   1 +
 tools/nouns/release_remediate/adjectives.txt       |   2 +
 tools/nouns/release_remediate/fields.txt           |   1 +
 tools/nouns/release_remediate/release_remediate.py |  81 ++++
 .../release_remediate/schemas/verbs.schema.json    |  10 +
 tools/nouns/release_tags/release_tags.py           |  57 +++
 83 files changed, 3095 insertions(+), 226 deletions(-)
```

---

Draft commits/range from `python3 tools/nlc_release_notes.py --write-draft --version 0.3.0 --to HEAD`. Edit **Highlights** before merge; `./release` refuses to tag without them.
