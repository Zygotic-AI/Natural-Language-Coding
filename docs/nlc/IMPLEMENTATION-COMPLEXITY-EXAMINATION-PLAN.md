# Plan: examine implementation complexity

**Status:** executed 2026-10-09. Post-execution audit is in the last section.  
**Date:** 2026-10-09  
**Tier:** T2 (staged examination of the whole hub; not a one-file edit and not an organization-wide policy change)  
**Charter class of this file:** none. This file is the examination plan. A later simplification is class A–F only when a finding proposes a change. Class A changes an adjective (a status or value rule on a noun). Class F changes a charter rule.  
**Version class of this file:** patch. Documentation only. Do not bump `integrity/nlc-version.json` for this file.  
**Planit identity:** `.agents/skills/planit/SKILL.md`  
**Workspace:** repository root

This plan measures complexity. It does not simplify anything. Execution fills the records in this file. The post-execution audit in the last section decides whether the examination is done.

## Gate

Default-closed. Do not start step 2 until step 1 is PASS or `skip:` with a reason. Do not write a simplification, edit an architecture decision record, commit, tag, or run `./release` under this plan.

| Criterion | Blocking? | Pass when |
| --- | --- | --- |
| Six steps remain | yes | Steps 1–6 are present and none was dropped without `skip:` plus a reason |
| Stop predicate per step | yes | Each step can be marked PASS or FAIL from the evidence recorded in that step |
| During-execution record | yes | Each executed step has the command, the exit code, and the filled table |
| Candidate rule | yes | Every simplification candidate is one of: delete a second authority, collapse a duplicate map into the import it already performs, split one module along an existing noun boundary, or leave it |
| Surviving gate | yes | Every candidate names the measurement and the gate that must still pass |
| Post-execution audit | yes | The checklist at the end of this file is complete and its result is PASS or FAIL |

**Done signals:** the post-execution audit result line is PASS, and the working tree contains no simplification produced by this plan.

## Outcome

One filled examination in this file. A simplification is allowed in the candidate table only when a measurement shows a second copy of the same decision, or a module whose lines mix two nouns. Length by itself is not a candidate.

## In scope / out of scope

| In | Out |
| --- | --- |
| How to measure `tools/`, `tools/nouns/`, `goals/`, `scripts/`, workflows, and the fitness and architecture-decision gates that read them | Implementing a simplification |
| Whether a second copy of one decision can be removed without dropping a bound gate | Editing architecture decision records 0001–0048 |
| The open rows in `TODO` under “Practice enforcement residuals,” counted as observations already named | Commit, tag, or `./release` |
| Read-only commands and filling this file | A new charter rule |

## Applicability

| Id | Applies because | Disposition |
| --- | --- | --- |
| Charter §5.8 | Zero variance: a simplification may not delete a prescribed gate | Every candidate |
| Charter §6 | A later code change needs a class A–F before implementation | Only if a finding proposes a change |
| Record 0007 | Rules stay applied; do not simplify the rule runner away | Step 5 rejection rule |
| Record 0008 | Do not merge two nouns by inheritance | Step 5 rejection rule |
| Record 0009 | Interior functions stay the named primitives | Step 5 rejection rule |
| Record 0010 | This plan generates no product code. A filled record in this file is the examination artifact | Steps 1–6 |
| Record 0028 | Do not edit an accepted record in place | Step 5 |
| Record 0045 | Release phase selection is one planner. A second selector is a finding | Step 2 |
| Record 0046 | The examination uses this repository’s Planit | This file |
| Record 0048 | Census uses the five shape classes already defined | Step 1 |
| Vault knowledge-change review | No vault layer is in this plan | Excluded |
| Ship | Not a release | Excluded |

## Bindings

Each step binds to `CHARTER.md` §5.8. Step 1 also binds to record 0048 (executable shape). Step 2 also binds to record 0045 (one release identity). Step 5 also binds to records 0007 (rules), 0008 (no noun inheritance), 0009 (primitive interior functions), and 0028 (do not edit an accepted record in place).

## Snapshot to remeasure

These counts were taken on 2026-10-09. Step 1 replaces them. They are not findings.

| Surface | Count |
| --- | --- |
| `tools/*.py` | 372 |
| `tools/nouns/` packages | 366 |
| Python files | 1209 |
| `goals/` | 6 |
| `scripts/` | 6 |

Longest Python modules in that snapshot: `tools/nouns/ci_fitness/ci_fitness.py` (639 lines), `tools/nouns/nlc_hub_cli/nlc_hub_cli.py` (623), `tools/nouns/release_state/release_state.py` (462).

## Step 1 — Census

**Procedure.** From the repository root, run:

```bash
python3 tools/fitness-executable-shape.py
```

Then count lines of Python, shell, and workflow files, excluding `.git`, `__pycache__`, `.venv`, and `node_modules`. Group every scanned file into exactly one class from record 0048 (executable shape): noun implementation, goal, primitive adapter, thin entrypoint, or contained fixture.

**Stop predicate.** PASS when the unclassified count is recorded and every file in the count is in exactly one class. FAIL when any scanned file has no class.

**During-execution record**

| Field | Value |
| --- | --- |
| Disposition | PASS |
| Command | `python3 tools/fitness-executable-shape.py` |
| Exit code | 0 (`UNCLASSIFIED:0`, `RESULT:MET`) |
| Unclassified count | 0 |
| noun implementation | 744 |
| goal | 22 |
| primitive adapter | 372 |
| thin entrypoint | 20 |
| contained fixture | 90 |
| Result | PASS. 1248 scanned files, each in one class. Line counts from the same scan: Python 1105 files, 37652 lines; shell 20 files, 1540 lines; workflow 2 files, 78 lines. |

## Step 2 — One outcome, how many authorities

**Procedure.** For each command below, list every module that selects a phase or owns policy. Mark exactly one row authoritative, or write that the code has more than one.

| Command | Modules to open |
| --- | --- |
| `./release` | `goals/hub_release/execute.sh`, `scripts/nlc-release.sh`, `tools/nouns/release_state/release_state.py`, `tools/nouns/nlc_release_state/nlc_release_state.py`, `tools/nouns/nlc_release_resume/nlc_release_resume.py`, `tools/nouns/release_infer/release_infer.py` |
| `./nlc` | `tools/nouns/nlc_hub_cli/nlc_hub_cli.py` and the noun each subcommand calls |
| install | `scripts/install.sh`, `scripts/install.ps1`, `goals/hub_install/execute.sh`, `goals/hub_install/execute.ps1` |
| hub compile | `tools/ci_fitness.py`, `tools/nouns/ci_fitness/ci_fitness.py` |

**Stop predicate.** PASS when each command has a filled table and exactly one row is marked authoritative, or the table states that more than one module selects the phase. FAIL when a module in the list above is missing from the table.

**During-execution record**

| Command | Authoritative module | Other selectors | Result |
| --- | --- | --- | --- |
| `./release` | Record 0045 (one release identity) names `tools/nouns/release_state/release_state.py` `plan_release()` | More than one. `tools/nouns/nlc_release_resume/nlc_release_resume.py` `detect()` selects a phase. `tools/nouns/release_infer/release_infer.py` `infer_release()` repeats that phase. `goals/hub_release/execute.sh` runs the planner and then falls through to `detect()`. `tools/nouns/nlc_release_state/nlc_release_state.py` `observe()` hard-codes `shipped_verify_met`, `target_verify_met`, and `prep_met` to false. `scripts/nlc-release.sh` only starts the goal. | PASS |
| `./nlc` | `tools/nouns/nlc_hub_cli/nlc_hub_cli.py` | None. Callees, not selectors: `nlc_distribution`, `nlc_cli_help`, `nlc_dashboard`, `nlc_human_gap`, `nlc_menu_data`, `nlc_preflight`, `nlc_requirements`, `nlc_requirements_cmd`, `nlc_guide_cmd`, `nlc_regen_continue`, `nlc_verify`. | PASS |
| install | More than one. `goals/hub_install/execute.sh` and `goals/hub_install/execute.ps1` each own the platform policy. | `scripts/install.sh` and `scripts/install.ps1` only start those goals. | PASS |
| hub compile | `tools/nouns/ci_fitness/ci_fitness.py` | `tools/ci_fitness.py` only calls `main`. | PASS |

## Step 3 — Duplicate decision

**Procedure.** Compare these three pairs. For each pair, record the paths and either “same decision, one copy” or “same decision, N copies.”

| Pair | Left | Right |
| --- | --- | --- |
| Release phase | `tools/nouns/nlc_release_resume/nlc_release_resume.py` `detect()` | `tools/nouns/release_state/release_state.py` `plan_release()` |
| Adapter routing | `ADAPTER_TO_NOUN` in `tools/nouns/fitness_hub_source/fitness_hub_source.py` | the `from nouns.<slug> import` line in each `tools/*.py` adapter |
| Record fixture | `integrity/adr-gates.json` fixture path for each active record | the behavioral fitness that already fails when that record’s decision is violated |

**Stop predicate.** PASS when each pair has paths and a copy count. FAIL when a pair is described without paths.

**During-execution record**

| Pair | Copy count | Paths | Result |
| --- | --- | --- | --- |
| Release phase | 3 | Same decision, 3 copies: `plan_release()` in `tools/nouns/release_state/release_state.py`; `detect()` in `tools/nouns/nlc_release_resume/nlc_release_resume.py`; `infer_release()` in `tools/nouns/release_infer/release_infer.py` (it copies `detect()`). | PASS |
| Adapter routing | 2 | Same decision, 2 copies. `ADAPTER_TO_NOUN` has 199 entries. Of 372 `tools/*.py` files, 189 imports match the map, 10 imports disagree with the map (`nlc-pack-export.py`, `nlc-pack-install.py`, `nlc_distribution.py`, `nlc_requirements.py`, `nlc_rule_coverage.py`, `nlc_rule_emit.py`, plus `nlc_gate_record.py`, `nlc_gate_scope.py`, `nlc_rule_marker.py`, and `nlc_rule_runner.py` which are mapped but have no `from nouns.<slug> import`), and 173 adapters import a noun and are absent from the map. | PASS |
| Record fixture | 2 | Same decision, 2 copies for most records. `integrity/adr-gates.json` has 48 records and 6 distinct fixture paths. 43 records use `tools/assert-adr-approval-mismatch-fails.py`. The enforcement table in `docs/ADR-ENFORCEMENT.md` names that fixture, or the record’s gate, on 6 rows (0007, 0009, 0028, 0046, 0047, 0048). 35 numbered rows name a different behavioral tool. Ranges 0017–0018 and 0031–0035 also name other tools. | PASS |

## Step 4 — Change cost

**Procedure.** For each policy, list every file that must change together for one policy change. The count is the length of that list.

| Policy | Start here |
| --- | --- |
| Release phase | the modules in step 2 for `./release` |
| Planit identity (record 0046) | `.agents/skills/planit/SKILL.md`, `integrity/planit-skill-registry.json`, `tools/nouns/planit_identity/planit_identity.py` |
| Approval receipts (record 0047) | `tools/nouns/adr_approval/adr_approval.py` (receipts file retired; C6 sidecar/batch only) |
| Executable class (record 0048) | `tools/nouns/executable_shape/executable_shape.py` |
| Hub-command preflight (record 0013) | `tools/nouns/fitness_requirements_hub_entrypoints/fitness_requirements_hub_entrypoints.py` and the commands it checks |

**Stop predicate.** PASS when each policy has an integer and the path list. FAIL when the count is a guess.

**During-execution record**

| Policy | File count | Paths | Result |
| --- | --- | --- | --- |
| Release phase | 9 | `goals/hub_release/execute.sh`; `tools/nouns/release_state/release_state.py`; `tools/nouns/nlc_release_state/nlc_release_state.py`; `tools/nouns/nlc_release_resume/nlc_release_resume.py`; `tools/nouns/release_infer/release_infer.py`; `tools/nouns/nlc_release_context/nlc_release_context.py`; `tools/nouns/assert_release_state_passes/assert_release_state_passes.py`; `tools/nouns/assert_release_resume_invariant_passes/assert_release_resume_invariant_passes.py`; `tools/nouns/fitness_adr_0039_release_binder/fitness_adr_0039_release_binder.py`. Thin starters `scripts/nlc-release.sh`, `tools/nlc_release_state.py`, `tools/nlc_release_resume.py`, and `tools/nlc_release_infer.py` are not in the count. | PASS |
| Planit identity (record 0046) | 10 | `.agents/skills/planit/SKILL.md` (`.cursor/skills/planit/SKILL.md` is the same file); `integrity/planit-skill-registry.json`; `tools/nouns/planit_identity/planit_identity.py`; `.cursor/hooks/nlc-planit-identity.sh`; `.cursor/hooks.json`; `tools/assert-planit-other-skill-fails.py`; `tools/nouns/ci_fitness/ci_fitness.py`; `docs/ADR-ENFORCEMENT.md`; `integrity/adr-gates.json`; `adrs/0046-repository-planit-identity.md` (do not edit in place). `tools/fitness-planit-identity.py` only imports the noun. | PASS |
| Approval receipts (record 0047) | 7 | `tools/nouns/adr_approval/adr_approval.py`; `tools/nouns/adr_record_gate/adr_record_gate.py`; `tools/assert-adr-approval-mismatch-fails.py`; `tools/nouns/ci_fitness/ci_fitness.py`; `integrity/adr-gates.json`; `docs/ADR-ENFORCEMENT.md`; `adrs/0047-adr-approval-receipts.md` (do not edit in place). Receipts file retired; C6 sidecar/batch only. | PASS |
| Executable class (record 0048) | 6 | `tools/nouns/executable_shape/executable_shape.py`; `tools/assert-executable-kernel-exempt-fails.py`; `tools/nouns/ci_fitness/ci_fitness.py`; `integrity/adr-gates.json`; `docs/ADR-ENFORCEMENT.md`; `adrs/0048-executable-shape.md` (do not edit in place). | PASS |
| Hub-command preflight (record 0013) | 5 | `tools/nouns/fitness_requirements_hub_entrypoints/fitness_requirements_hub_entrypoints.py`; `tools/nouns/assert_requirements_hub_entrypoints_passes/assert_requirements_hub_entrypoints_passes.py`; `tools/nouns/ci_fitness/ci_fitness.py`; `docs/ADR-ENFORCEMENT.md`; `adrs/0013-requirements-preflight.md` (do not edit in place). The fitness globs `tools/nlc*.py`; those command files are the subjects of the rule, not part of this count. `tools/fitness-requirements-hub-entrypoints.py` and `tools/assert-requirements-hub-entrypoints-passes.py` only import the nouns. | PASS |

## Step 5 — Candidate rule

**Procedure.** Admit a row only when steps 2–4 show a second copy of one decision, or a module whose lines mix two nouns. Reject a row that would delete a bound gate, edit an accepted record in place, or merge two nouns that record 0008 (no noun inheritance) keeps apart.

Allowed actions:

| Action | Meaning |
| --- | --- |
| delete-second-authority | One module stops selecting a phase that another module already selects |
| collapse-map | A hand-kept map is replaced by the import the adapter already has |
| split-module | One file is split on a noun boundary that already exists |
| leave | Measured, and no second copy was found |

**Stop predicate.** PASS when every candidate row has one allowed action, a measurement from steps 2–4, and the gate that must still pass. FAIL when a row’s only reason is that a file is long.

**During-execution record**

| Candidate | Action | Measurement | Surviving gate | Result |
| --- | --- | --- | --- | --- |
| Release phase selection | delete-second-authority | Step 2: more than one selector. Step 3: 3 copies. Step 4: 9 files. Keep `plan_release()`. Stop `detect()` and `infer_release()` from choosing a phase, and stop `execute.sh` from falling through. | `python3 tools/assert-release-state-passes.py` and `python3 tools/fitness-adr-0039-release-binder.py` stay MET. Record 0045 is not edited. The invalid-merge case in `assert-release-state-passes.py` stays. | PASS |
| `ADAPTER_TO_NOUN` | collapse-map | Step 3: 189 matches, 10 disagreements, 173 import-only adapters. The import is already the route. | `python3 tools/fitness-hub-bba-dogfood.py`, `python3 tools/fitness-interview-gap-shape.py`, and `python3 tools/fitness-requirements-hub-entrypoints.py` stay MET. | PASS |
| Record fixture column in `integrity/adr-gates.json` | collapse-map | Step 3: 43 of 48 records share `tools/assert-adr-approval-mismatch-fails.py`, while `docs/ADR-ENFORCEMENT.md` names another behavioral tool on 35 numbered rows and on ranges 0017–0018 and 0031–0035. | `python3 tools/fitness-adr-record-gate.py` and `python3 tools/fitness-adr-enforcement-table-sync.py` stay MET. Do not remove the behavioral tools named in the enforcement table. | PASS |
| Hub compile | leave | Step 2: one authority, `tools/nouns/ci_fitness/ci_fitness.py`. The adapter only calls `main`. Length is not the reason. | `tools/ci_fitness.py` stays a one-call adapter. | PASS |
| `./nlc` dispatch | leave | Step 2: one dispatcher. Imported modules are callees. 623 lines is not a candidate. | No split. The dispatcher remains `tools/nouns/nlc_hub_cli/nlc_hub_cli.py`. | PASS |
| Install goals | leave | Step 2: `scripts/install.sh` and `scripts/install.ps1` do not select. The two files under `goals/hub_install/` are one goal per shell, not a second phase selector. | `python3 tools/fitness-interview-gap-shape.py` stays MET. | PASS |

Counted, not admitted as new work: the open `TODO` rows under “Practice enforcement residuals” match the release-phase candidate and the record-fixture candidate. The effective-decision view for record 0045 decision 2 as amended by record 0048 is still an open row. This examination does not close those rows.

Known observations the examination must count, not new work: the open `TODO` rows under “Practice enforcement residuals” (per-record behavior fixtures, the effective-decision view for record 0045 decision 2 as amended by record 0048, and the `./release` planner/resume split).

## Step 6 — Report

**Procedure.** Confirm steps 1–5 are PASS or `skip:` with a reason. The report is this file with those records filled. Do not add a second report.

**Stop predicate.** PASS when the gate at the top of this file is true for the filled records. FAIL when any candidate lacks a measurement or a surviving gate.

**During-execution record**

| Field | Value |
| --- | --- |
| Disposition | PASS |
| Steps 1–5 result | PASS, PASS, PASS, PASS, PASS |
| Result | PASS. This file is the report. No second report was added. |

## Post-execution audit

Run this after step 6, as a separate pass from the person or session that filled the records.

| Check | Result | Evidence |
| --- | --- | --- |
| Unclassified count in step 1 matches a fresh `python3 tools/fitness-executable-shape.py` | PASS | Re-run after the records were filled: exit 0, `UNCLASSIFIED:0`, `RESULT:MET`. Step 1 records 0. |
| Each step is PASS, FAIL, or `skip:` with a reason | PASS | Steps 1–6 result lines are PASS. No `skip:`. |
| No step was dropped | PASS | Headings `## Step 1` through `## Step 6` are present. |
| Every candidate action is one of the four allowed actions | PASS | delete-second-authority, collapse-map, collapse-map, leave, leave, leave. |
| Every candidate cites a measurement and a surviving gate | PASS | Each candidate row has a step measurement and a named command or module that must stay MET. |
| No accepted architecture decision record was edited | PASS | This execution did not write `adrs/`. Records 0046–0048 were already untracked from earlier work and were not modified here. |
| No simplification was implemented | PASS | This execution wrote this plan file only. No second authority was removed and no map was collapsed. |
| `TODO` residual rows are still open unless a separate change closed them | PASS | “Practice enforcement residuals” still has 10 open rows. |

**Post-execution result:** PASS

FAIL on any row blocks calling the examination done. Fix the record and run this audit again.
