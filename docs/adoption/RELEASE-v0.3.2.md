# Natural Language Coding hub v0.3.2

## Highlights

Hub **v0.3.2** is a patch on **v0.3.1**. The git tags for v0.3.0 and v0.3.1 stay on the same peels. This tag ships the FINDINGS/DESCRIBE current-ship fitness work and the **0.3.2** identity so the merge into `main` can be tagged.

- **FINDINGS and DESCRIBE current-ship fitness (F1) widened.** The live surfaces compare the last shipped tag on `origin/main` and this tree’s `integrity/nlc-version.json`. A leftover fixture next to the noun stays `NOT_MET`. On `main` and at tag time the phrase must match this line’s version.
- **F1 is not inside shipped-tag `check_static`.** The shipped-tag audit still reuses `check_static` on the historical leftover FINDINGS at `v0.3.1`. F1 runs from the tag-gate main path only.
- **Identity, notes, and record say 0.3.2.** `integrity/nlc-version.json`, `integrity/hub-release-record.json`, and `docs/adoption/RELEASE-v0.3.2.md` match `release/v0.3.2`.
- **Prescribed read order.** `docs/adoption/RELEASE.md` and the release / full-NLC-audit / nlc-hub-audit skills state stale `release/v*` versus closed shipped lines.

**Explicitly not in v0.3.2**

- README diagrams (left: generic intent/policies; right: healthcare HIPAA + SEC). Those stay a later TODO and are not in this signed tree.
- A new compiled-system use-case wave. UC14 / UC16 / UC20 stay expansion-only.
- Moving or rewriting the `v0.3.0` or `v0.3.1` tags.

## Changes since v0.3.1

- Add the owner-signed gate-set manifest sidecar (`89fb12b`)
- Keep F1 out of shipped-tag check_static; refresh install hashes. (`93fcc2c`)
- Refresh content digest and unsigned gate-set manifest. (`9de2d26`)
- Keep FINDINGS and DESCRIBE current-ship prose aligned with the tag. (`3d18ac6`)

### Diff stat

```
.agents/skills/full-nlc-audit/SKILL.md             |   2 +-
 .../full-nlc-audit/references/inference-phases.md  |   5 +-
 .agents/skills/nlc-hub-audit/SKILL.md              |   5 +-
 .agents/skills/release/SKILL.md                    |   1 +
 DESCRIBE.md                                        |   2 +-
 FINDINGS.md                                        |   4 +-
 README.md                                          |   2 +
 docs/adoption/RELEASE.md                           |   4 +-
 integrity/gate-set-baseline.manifest.sha256        |  30 +--
 .../gate-set-baseline.manifest.sha256.approval.asc |  10 +-
 integrity/hub-content-tree-hash.txt                |   2 +-
 integrity/nlc-install-hashes.json                  |   6 +-
 tools/fitness-findings-shipped-tag-sync.py         |   2 +-
 .../fitness_findings_shipped_tag_sync.py           | 233 ++++++++++++++++++---
 .../fixtures/origin-main-current-ship.md           |   3 +
 .../fixtures/origin-main-needed-leftover.md        |   3 +
 .../nlc_release_tag_gate/nlc_release_tag_gate.py   |  19 ++
 17 files changed, 275 insertions(+), 58 deletions(-)
```
