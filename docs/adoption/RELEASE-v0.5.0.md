# Natural Language Compiler hub v0.5.0

## Highlights

Hub **v0.5.0** is a minor on **v0.4.1**. The `v0.4.1` tag stays on its peel.

- **GitHub name is Natural-Language-Compiler.** Install curl/irm lines, installer defaults, and live clone/fetch slugs use `Zygotic-AI/Natural-Language-Compiler`. The prior GitHub name still redirects.
- **Tag fetch no longer clobbers.** Release observe does not `git fetch --tags`, so a lightweight checkout tag cannot fail against the annotated origin tag.
- **One tag-time signature.** The owner signed `integrity/checker-digest.sha256` for this tag (ADR 0057). Branch `./nlc verify` still does not require that armor.

## Changes since v0.4.1

- Use Natural-Language-Compiler as the live GitHub slug. (`1fdab02`)
- Point install and clone URLs at Natural-Language-Compiler. (`16ee6d3`)
- Stop fetching tags during release observe. (`c0d933d`)

### Diff stat

```
.agents/skills/nlc-hub-audit/SKILL.md              |  2 +-
 .nlc/before-generate-stamp.json                    |  4 +-
 README.md                                          |  6 +-
 adrs/0011-natural-language-coding-naming.md        |  2 +-
 adrs/0016-hub-carries-no-product-requirements.md   |  2 +-
 docs/adoption/BOOTSTRAP.md                         |  2 +-
 docs/adoption/RELEASE-SINGLE-PATH-PLAN.md          |  2 +-
 docs/github-ruleset-release.md                     |  2 +-
 docs/nlc/compiler/GETTING-STARTED.md               |  6 +-
 ...9-25-tag-pushed-no-github-release-shallow-ci.md |  6 +-
 .../2026-10-25-planit-unregistered-skill-edit.md   |  2 +-
 ...2026-11-02-pr-offered-before-fitness-success.md |  2 +-
 goals/hub_install/execute.ps1                      |  2 +-
 goals/hub_install/execute.sh                       |  2 +-
 goals/hub_release/execute.sh                       |  2 +-
 integrity/checker-digest.sha256                    |  2 +-
 integrity/gate-set-baseline.manifest.sha256        | 74 +++++++++++-----------
 integrity/hub-content-tree-hash.txt                |  2 +-
 integrity/nlc-install-hashes.json                  |  6 +-
 integrity/schemas/hub-pack-registry.schema.json    |  2 +-
 .../schemas/nlc-adr-bind-snapshot.schema.json      |  2 +-
 integrity/schemas/nlc-lock.schema.json             |  2 +-
 integrity/schemas/nlc-pack-manifest.schema.json    |  2 +-
 scripts/install.ps1                                |  2 +-
 scripts/install.sh                                 |  2 +-
 .../tools/nouns/owner_sidecar/owner_sidecar.py     |  2 +-
 templates/adopter/README.md                        |  4 +-
 .../fixtures/owner-ratification-sidecar/cases.json |  6 +-
 .../manifest-wrong-key-statement.txt               |  2 +-
 .../pending-as-ratified.json                       |  4 +-
 .../wrong-decision-statement.txt                   |  2 +-
 .../wrong-document-statement.txt                   |  2 +-
 .../wrong-hash-statement.txt                       |  2 +-
 .../wrong-key-statement.txt                        |  2 +-
 .../assert_release_probe_fail_closed.py            | 10 ++-
 .../assert_verifier_change_via_staging_passes.py   |  2 +-
 .../fitness_adr_0039_release_binder.py             | 11 ++++
 tools/nouns/menu_data/menu_data.py                 |  2 +-
 tools/nouns/nlc_distribution/nlc_distribution.py   |  2 +-
 tools/nouns/nlc_init/nlc_init.py                   |  2 +-
 .../nouns/nlc_release_resume/nlc_release_resume.py |  2 +-
 tools/nouns/nlc_release_state/nlc_release_state.py |  5 +-
 tools/nouns/owner_sidecar/owner_sidecar.py         | 10 +--
 tools/nouns/pr_offer_gate.py                       |  4 +-
 44 files changed, 120 insertions(+), 96 deletions(-)
```

