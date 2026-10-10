# RCA: `./release` stops and hands the operator another command

**Date:** 2026-10-09  
**Context:** Natural Language Coding hub — `./release`  
**Status:** prevented

---

## 1. Error condition

**Evidence (observed):**

- `./release` stopped with `RELEASE:NOT_MET` and pointed to `/verify`. After `./nlc verify` exited 0, `./release` stopped again on a different check: `RELEASE_CONTEXT:NOT_MET commits on main not in release/v0.3.0`. That fix list was `git fetch` and `./release`.
- `goals/hub_release/execute.sh` has 23 `release_fail` calls and 14 `exit 1` lines (`rg -c`, 2026-10-09).
- The planner `tools/nouns/release_state/release_state.py` reads 8 boolean facts: `dirty`, `migrations_ready`, `notes_valid`, `pr_list_known`, `prep_met`, `remote_known`, `shipped_verify_met`, `target_verify_met`. The release-context check, preflight, shipped-tag audit, full audit, notes block, version-line check, and checkout failures are not among those facts.
- `docs/rca/` holds 10 release RCAs from 2026-09-24 to 2026-10-09. Each one fixed one check or one fix message.
- Record 0045 decision 2 says the planner chooses one phase and one action, and the executor performs only that action. It does not say that every stopping check must be a planner fact.

**Inferred (label clearly):**

- Each new stop point in the shell is a check the planner cannot see, so the planner cannot choose a repair for it. The executor can only print advice and exit.
- `/verify` asks for `verify-deep`. The planner already has `VERIFY_TARGET` and `VERIFY_SHIPPED_BASELINE` actions, so `./release` can run that step itself.

**Mechanism confirmed on reproduction:** yes. `python3 tools/nlc_release_context.py --remote origin --base main --branch release/v0.3.0` exits 1. In `run_prepare_core`, that exit goes to `release_fail`, not to the planner. Planner state at the same time: `PREPARE_DRAFT` / `COMMIT`.

---

## 2. Upstream chain (process before output)

| Step | Artifact / layer | What it did |
| ---- | ---------------- | ----------- |
| (symptom) | Operator loop | `./release` → stop → run another command → `./release` → different stop |
| 4 | `goals/hub_release/execute.sh` | 23 stops that print remediation and exit |
| 3 | Release RCAs 2026-09-24 … 2026-10-09 | Each fixed one stop or one message. None removed the ability to add a stop outside the planner |
| 2 | Record 0045 decision 2 | One planner for phase and action, but stopping checks may still live in the shell |
| 1 | Hub compile (`tools/ci_fitness.py`, binder `fitness-adr-0039-release-binder.py`) | Requires the planner to be called. Does not fail when the executor stops outside a planner phase |

**Furthest controllable upstream point:** the hub compile. It accepts a release executor that can stop on a condition the planner does not observe.

---

## 3. Impact / scope

Every check added to `./release` can become a new human round trip. Repairs to single stops have not ended the class: 10 release RCAs in 16 days. The human surface in record 0039 (one resumable `./release`) does not hold while the shell owns stops.

---

## 4. Timeline (brief)

| Time | Event |
| ---- | ----- |
| 2026-09-24 – 09-25 | Nine release RCAs, each repairing one stop or message |
| 2026-09-26 | Record 0045: one planner for phase and action |
| 2026-10-09 | `./release` → `/verify` → `./release` → release-context stop |

---

## 5. The one thing

> What **one** deterministic, actionable thing, if it were different, would have **prevented this error condition from arising**?

**Answer:** A hub compile gate that fails unless every way `./release` can stop is a planner fact whose action is either a machine repair the executor runs and then re-plans, or a named human decision.

---

## 6. Prevention test

> If **that hub compile gate** had been in place **before** the failure, **`./release` stopping and sending the operator to `/verify`, then to fetch and re-run** could not have occurred because **neither stop could have merged into the executor: verification is already a planner action that `./release` runs itself, and the release-context check would have had to enter as a planner fact with a repair or a named human decision, not as `release_fail` advice.**

**Completed:** yes. Each observed stop is a shell `release_fail` path absent from the planner's eight facts.

---

## 7. Contributing factors (optional)

- `release_fail` defaults to `git fetch` and `./release` when the caller passes no fixes.
- `./nlc verify` and `./release` are separate predicates. A passing verify does not clear release checks.
- Earlier RCAs accepted a better message for one stop as the prevention.
- The release-context check counts a merge commit whose parents are already in the release branch. That is one instance. This record does not choose its repair.

---

## 8. Preventive action (single tracked item)

| Field | Value |
| ----- | ----- |
| Action | Add a hub compile gate: `goals/hub_release/execute.sh` may exit nonzero or call `release_fail` only from the planner dispatch for a planner phase or blocker. Every planner blocker names either an executor repair action, followed by re-planning, or a human decision. The gate fails on any other stop. Move the current stops into planner facts until the gate passes. |
| Owner | hub maintainer |
| Path / artifact | New fitness noun and adapter under `tools/`, wired into `tools/nouns/ci_fitness/ci_fitness.py`; `tools/nouns/release_state/release_state.py`; `tools/nouns/nlc_release_state/nlc_release_state.py`; `goals/hub_release/execute.sh`. A new architecture decision record if record 0045 needs this rule stated. Do not edit 0045 in place. |
| Verification | `python3 tools/fitness-release-planner-ownership.py` exits 0; `python3 tools/assert-release-planner-ownership-fails.py` exits 0 after proving hidden-stop, missing-progress, generic-error, unproved-context, merge, force-push, tag-move, stash, and hard-reset specimens are refused. `python3 tools/assert-release-context-passes.py` proves contained, unique-commit, merge-only-tree, missing-parent, and Git-error outcomes. `./nlc verify-deep` and `./nlc verify` exit 0. |
| Human acceptance | `accepted` by `/planit docs/rca/2026-10-09-release-stops-outside-planner.md` on 2026-10-09 |
| Implementation route | **`/planit`** after acceptance — cite `docs/rca/2026-10-09-release-stops-outside-planner.md` |

---

## 9. Follow-up (detection only if prevention insufficient)

- None. The release-context repair is one instance that the preventive action must cover.

---

## 10. Prevention completion gate

Default closed. Status may be `prevented` only when every blocking row is true.

| Criterion | Blocking? | Pass when | Evidence |
| --- | --- | --- | --- |
| Accepted decision | yes | ADR 0049 is accepted, ratified, approved, and active | ADR record, approval receipt, active binding snapshot |
| Planner ownership | yes | The real executor has no stop, untyped action, generic error fact, or forbidden mutation outside the planner contract | `python3 tools/fitness-release-planner-ownership.py` exits 0 |
| Adversarial prevention | yes | Every hidden-stop, missing-progress, unsafe-mutation, and absent-context specimen is rejected | `python3 tools/assert-release-planner-ownership-fails.py` exits 0 |
| Context closure | yes | Contained, unique-commit, merge-only-tree, missing-parent, and Git-error specimens return the required enum | `python3 tools/assert-release-context-passes.py` exits 0 |
| Planner behavior | yes | Repairs, stalls, invalid merges, permission boundaries, and tag targets satisfy the oracle | `python3 tools/assert-release-state-passes.py` exits 0 |
| Hub compile | yes | All hub fitness and landmine checks pass with the new gates wired | `python3 tools/ci_fitness.py` prints `CI:MET` and exits 0 |
| Verify | yes | Current fingerprints and the deep compile agree | `./nlc verify-deep` then `./nlc verify` both exit 0 |
