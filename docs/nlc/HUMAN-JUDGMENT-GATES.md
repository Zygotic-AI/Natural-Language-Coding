# Human judgment vs machine gates

**[Default-closed](../TERMS.md#default-closed):** compile and `./nlc verify` fail when machine gates fail. Humans do not patch generated files to green.

## Machine (automated + planit skills)

| [Gate](../TERMS.md#gate) | Enforcement |
| ---- | ------------- |
| Per-artifact generate → [gate](../TERMS.md#gate) (ADR 0010) | Plan metrics → generate → **immediate [gate](../TERMS.md#gate)**; `./nlc maintainer gate-record` + `verify` checks `.nlc/gate-records.json` |
| Before generate (UC18) | `./nlc maintainer guide before-generate` + stamp; `verify` fails if `goals/` / `domain/` changed after stamp |
| [Plan audit](../TERMS.md#plan-audit) (planit active) | **[bbp-reviewer](../TERMS.md#bbp-reviewer)** Q2 JSON → `./nlc maintainer plan-audit`; `verify` requires `.nlc/plan-audit.json` |
| Adversarial / produce | [Hub](../TERMS.md#hub): `.nlc/produce-package.json`; app with goals: `.nlc/change-adversarial.json` + [produce package](../TERMS.md#produce-package) — **[verify-deep](../TERMS.md#verify-deep)** (Q1/Q2 + SSOT) |
| Empty `Waived:` in ADRs | `verify` fails until reason recorded or [ADR](../TERMS.md#adr) ratified |
| Ratification pending | [ADR](../TERMS.md#adr) `Proposed` / `needs_review` → `verify` fails |
| [Rule](../TERMS.md#rule) conflicts | `check-rule-adoption` → `verify` fails |
| Fitness / [verify](../TERMS.md#verify) | `ci_fitness.py`, `./nlc verify`, `./nlc verify-deep` |
| Sensitive-file list (ADR 0058) | `python3 tools/nlc_release_sensitive_review.py --check` prints unresolved paths; `origin/main`'s copy is the grader |

## Human only (cannot be forged by agents)

| [Gate](../TERMS.md#gate) | Enforcement |
| ---- | ------------- |
| **C24 / release** | The GitHub **merge commit** of the release pull request onto `main` is the record. Merge is accept. No sidecar. |
| **[ADR](../TERMS.md#adr) / [rule](../TERMS.md#rule) adoption** | Human sets [ADR](../TERMS.md#adr) **Accepted**; agent does not ratify |
| **Sensitive-file accept** | Human reverts, edits, or merges the listed paths. Agents cannot perform that merge when branch protection requires the owner |
| **“Would this [noun](../TERMS.md#noun) be a lie?”** | [Interview](../TERMS.md#interview) / plan; do not codegen around unresolved doubt |
| **Waivers** | Explicit `Waived:` with reason in [handoff](../TERMS.md#handoff); machine gates still apply unless [waived](../TERMS.md#waived) criteria documented |

[Ship](../TERMS.md#ship) is the six-step unsigned path in [`docs/adoption/RELEASE.md`](../adoption/RELEASE.md). Compile green is not shipped.
