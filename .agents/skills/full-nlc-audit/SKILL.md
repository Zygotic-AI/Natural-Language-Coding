---
name: full-nlc-audit
description: Full NLC continuity audit — machine manifest plus inference phases. ./release step 0c uses profile release-prep (docs/adoption/RELEASE.md). Otherwise python3 tools/full-nlc-audit.py --check --profile quick|release-prep|full.
disable-model-invocation: true
---

# Full NLC audit

**Machine SSOT:** `python3 tools/full-nlc-audit.py --check` (+ `--profile quick|release-prep|full`).  
**Manifest SSOT:** `integrity/full-nlc-audit-manifest.json` — add stages there as new gates land.  
**Inference checklist:** `python3 tools/full-nlc-audit.py --emit-inference-checklist` (prints [`references/inference-phases.md`](references/inference-phases.md)).

**Supersedes** `nlc-hub-audit` as the human/agent entrypoint; hub-audit content lives under [`references/inference-phases.md`](references/inference-phases.md).

## Gate (default-closed)

Do **not** emit the final audit report until every **blocking** row is true.

| Criterion | Blocking? | Pass when | Evidence |
| --------- | --------- | --------- | -------- |
| SHA recorded | yes | Exact commit SHA in report metadata | Section 1 |
| Machine stages | yes | `FULL_NLC_AUDIT:MET` for chosen profile (or each FAIL stage documented) | Command output |
| Inference phases | yes (full audit) | Phases 0–7 in [`references/inference-phases.md`](references/inference-phases.md) run or waived with reason | Report sections |
| Evidence cited | yes | Every finding has path + line/section | Findings list |
| Audit-only | yes | No file fixes same turn unless user invoked execute/planit fix | Procedure |
| No roof reopen | yes | NLC roof unchanged | Hard rules |

**Done signals:** Machine `FULL_NLC_AUDIT:MET` (or explicit FAIL register); inference report sections 1–5; apex **Continuity: PASS | FAIL**.

## Inputs

| Input | Default |
| ----- | ------- |
| Repo root | Workspace root |
| Profile | `quick` (CI landmine); `release-prep` on `./release` prepare; `full` adds clean-tree + verify stages ([`docs/adoption/RELEASE.md`](../../../docs/adoption/RELEASE.md)) |
| Prior findings | Optional diff |

## Procedure

### Step M — Machine manifest

From repo root:

```bash
python3 tools/full-nlc-audit.py --check --profile quick
# ./release prepare (no duplicate verify-deep):
python3 tools/full-nlc-audit.py --check --profile release-prep
# local pre-ship sweep (clean tree; adds verify-deep + verify):
python3 tools/full-nlc-audit.py --check --profile full
# optional with local edits:
python3 tools/full-nlc-audit.py --check --profile full --allow-dirty
```

Record each `--- stage … PASS/FAIL ---` block in the report. On `NOT_MET`, stop **or** continue inference to explain orphans (user choice).

### Step I — Inference

```bash
python3 tools/full-nlc-audit.py --emit-inference-checklist
```

Follow [`references/inference-phases.md`](references/inference-phases.md) in order. Cite evidence; suggest remediation only.

### Step V — Verdict

| Apex | When |
| ---- | ---- |
| **Continuity: PASS** | Machine MET + no P0/P1 inference findings |
| **Continuity: FAIL** | Machine NOT_MET or any P0/P1 inference finding |
| **Continuity: PASS with residuals** | Machine MET + only P2/P3 + listed soft-green |

## Extending the audit

1. Add a row to `integrity/full-nlc-audit-manifest.json` (`stages` + profile list).
2. If the check is novel, implement `tools/…` or `builtin` in `tools/full-nlc-audit.py`.
3. Update `tools/fitness-full-nlc-audit-binder.py` if the stage must stay wired.
4. Optional: add inference checklist items to `references/inference-phases.md`.

## Hard rules

- Machine output is evidence — do not claim MET without the command exit code.
- `FINDINGS.md` is the live gap queue; continuity means **present-complete**, **parked (`gate missing`)**, or **absent** — not partial.
- Integration units: record in `integrity/integration-leaves.json` before deleting long-lived branches.

## When to write leaves

Before deleting or abandoning a **long-lived integration branch** (or remote that represented a bounded initiative), append a leaf to [`integrity/integration-leaves.json`](../../../integrity/integration-leaves.json):

| Field | Requirement |
| ----- | ----------- |
| **claims** | What the branch was meant to integrate or prove (one line per claim). |
| **disposition** | `on_main` \| `parked` \| `rejected` \| `absent` — must match reality on `main`. |
| **evidence** | For `on_main`: merge commit or `sha`. For `parked`: `findings_ref` pointing at a FINDINGS row. For `rejected`/`absent`: short reason. |

If leaves are intentionally empty (e.g. remotes already deleted without records), add [`integrity/integration-leaves-waive.json`](../../../integrity/integration-leaves-waive.json) with `waived`, `reason`, and `audit_sha` — do not leave an empty `leaves` array without waive.

## Reference

- [`docs/nlc/FULL-NLC-AUDIT.md`](../../../docs/nlc/FULL-NLC-AUDIT.md)
- [`docs/nlc/VERIFY-AND-SHIP.md`](../../../docs/nlc/VERIFY-AND-SHIP.md)
- [`docs/ADR-ENFORCEMENT.md`](../../../docs/ADR-ENFORCEMENT.md)
- Legacy alias skill: `.agents/skills/nlc-hub-audit/SKILL.md`
