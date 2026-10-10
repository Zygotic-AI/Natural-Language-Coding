# ADR 0049 — Release planner owns every intentional stop

- Status: Accepted
- Date: 2026-10-09
- Deciders: Human manager
- Ratified-by: Human manager (release planner ownership and no automatic local-main repoint, 2026-10-09)
- Class: A (release state), F (enforcement), and C (goal orchestration)
- Corpus: nlc
- RCA: [`docs/rca/2026-10-09-release-stops-outside-planner.md`](../docs/rca/2026-10-09-release-stops-outside-planner.md)

## Context

[ADR 0039](0039-single-command-human-surfaces.md) requires one resumable `./release`.
[ADR 0040](0040-process-preflight-remediation.md) requires a real remediation for a
release stop. [ADR 0045](0045-hub-release-identity.md) makes
`tools/nouns/release_state/release_state.py` the only phase and action planner.

The executor can still stop on checks that the planner does not observe. The
operator can therefore run `./release`, follow a request to run `/verify`, and
then encounter another stop whose proposed fix is fetch plus another
`./release`. Fixing individual messages does not prevent another stop from
being added outside the planner.

## Decision

1. **The planner owns every intentional stop.** Every expected condition that
   can end one `./release` invocation is a closed observation fact consumed by
   the pure release planner. The executor does not select a phase, action, or
   action kind.

2. **Action kinds are closed.** Every planner action has exactly one kind:

   | Kind | Meaning |
   | --- | --- |
   | `REPAIR` | The executor performs one allowlisted action and re-plans in the same `./release` invocation. |
   | `AWAIT` | An external asynchronous event is required. Only pull-request merge and release publication may use this kind. It exits 0 and resumes with the same `./release`. |
   | `HUMAN_DECISION` | No allowlisted automatic action is safe. The planner names the condition and the exact decision or repair; it exits nonzero. It does not send the operator to `/verify`, `./nlc verify`, or another release subcommand. |
   | `TERMINAL` | The release is complete and no action remains. |

3. **Existing actions are classified.**

   - `REPAIR`: `ENSURE_MIGRATIONS`, `VERIFY_SHIPPED_BASELINE`, `WRITE_NOTES`,
     `ALIGN_VERSION`, `VERIFY_TARGET`, `PREP`, `WRITE_RECORD`, `COMMIT`,
     `CREATE_RELEASE_LINE`, `CREATE_REPAIR_COMMIT`, `FETCH_REMOTE`,
     `FAST_FORWARD_LOCAL`, `PUSH_NEW`, `PUSH_FAST_FORWARD`, `CREATE_PR`,
     `CREATE_LOCAL_TAG`, `PUSH_TAG`, and `RETRY_PUBLISH`.
   - `AWAIT`: `EXIT_AWAIT` and `OBSERVE_PUBLISH`.
   - `HUMAN_DECISION`: `BLOCKED`.
   - `TERMINAL`: `NONE`.

4. **Repair means same-invocation progress.** After a `REPAIR`, the executor
   observes fresh facts and calls the planner again without returning control to
   the operator. Each repair action declares the fact tuple that proves
   progress. If the same action recurs with an unchanged tuple, the planner
   returns the closed blocker `BLOCKED_<ACTION>_STALLED`, kind
   `HUMAN_DECISION`.

5. **Observations are closed, not generic.** There is no generic runtime-error
   payload and no executor-supplied action kind. Each expected failure has a
   named observation with a typed value. A missing required observation is
   unknown and cannot produce PASS.

6. **Automatic mutations are allowlisted.** The executor may automatically run
   audits, write release notes, align the version, write the release record,
   create a commit, fast-forward a local branch when ancestry proves it safe,
   push an ordinary branch or tag, and create a pull request. Automatic merge,
   force-push, tag movement, stash, and hard reset are forbidden. This decision
   closes the earlier optional local-`main` repoint in ADR 0045 decision 6:
   no closed planner action authorizes it.

7. **Main context is a required enum.** The observer reports
   `main_context = contained | not_contained | unknown`.

   - `contained` is true only when every commit reachable from `origin/main`
     but absent from the release branch is a merge whose every parent is an
     ancestor of the release branch and whose result tree equals its
     second-parent tree.
   - A non-merge or squash commit, unique second-parent content, or a
     merge-only tree change is `not_contained`.
   - A Git error, missing parent, missing tree, or absent fact is `unknown`.
   - Only `contained` permits preparation to continue. The other values are
     named `HUMAN_DECISION` blockers. The observer does not cap the commit set.

8. **Invalid merged candidates never become tag targets.** If an exact merged
   candidate has invalid release identity, unmet preparation predicates remain
   ordinary `REPAIR` actions. If all content predicates are met, the planner
   emits `CREATE_REPAIR_COMMIT`, which creates a named allow-empty commit on the
   same release line. Its progress tuple includes candidate SHA, pull-request
   head SHA, merge SHA, merge file version, merge record version, and merge
   record branch. The changed candidate then follows ordinary push and
   pull-request actions. The invalid merge is never tagged.

9. **The executor has one action loop.** It observes facts, plans, performs
   exactly one planner action, and repeats. It does not rely on `set -e` to
   express expected control flow. Every external operation crosses an
   action-specific result boundary whose nonzero result becomes its named
   observation before re-planning.

10. **Hub compile enforces the shape.** A release-planner-ownership fitness
    fails when an intentional stop bypasses the planner, an action or fact is
    untyped, a forbidden mutation is reachable as automatic repair, context can
    fail open, or an action result can terminate the executor directly.

## Gate

Default closed. Implementation may proceed only after human ratification.
Completion requires every blocking row to be true.

| Criterion | Blocking? | Pass when | Evidence |
| --- | --- | --- | --- |
| Ratification | yes | Status is `Accepted` and `Ratified-by: Human manager` is present | This ADR |
| Closed actions | yes | Every planner action appears once in the action-kind registry | Release-state fitness |
| Closed facts | yes | Every expected stop maps to one typed observation; absent values block | Release-state fitness |
| Same-invocation repair | yes | Repair specimens re-plan without asking for another command | Release executor fitness |
| Hidden stop prevention | yes | Renamed helper, `return 1`, dynamic exit, and direct Python failure specimens are refused | Negative fixture |
| Mutation safety | yes | Automatic merge, force-push, tag move, stash, hard reset, and local-`main` repoint specimens are refused | Negative fixture |
| Context closure | yes | Git failure, missing parent, unique commit, and merge-only tree-change specimens do not return `contained` | Context fixture |
| Contained merge | yes | The pull-request merge whose result tree equals its contained second parent returns `contained` | Context fixture |
| Invalid merge | yes | Invalid merge produces repair commit or named stall; never tag action | Release-state oracle |
| Hub compile | yes | Full hub fitness exits 0 | `python3 tools/ci_fitness.py` |

## Refuse criteria

- Any intentional nonzero exit or remediation path that does not originate in a
  planner decision.
- Any catch-all failure fact, executor-selected action kind, or missing fact
  treated as success.
- Any automatic mutation outside the allowlist.
- Any automatic local-`main` repoint or hard reset.
- Any repair that tells the operator to run `/verify`, `./nlc verify`, or a
  release subcommand instead of re-planning in the same invocation.
- Any path that can tag an invalid merged candidate.

## Incomplete-packet fixture

A specimen executor invokes a renamed failure helper after a Python command
returns nonzero, without recording a named observation or re-planning.
Required outcome: release-planner-ownership fitness prints `RESULT:NOT_MET` and
exits nonzero.

## Consequences

- `./release` performs known audits and repairs itself. The operator runs no
  secondary verify or prepare command.
- A stop is evidence that the planner reached a named human-only decision, not
  that the shell discovered another hidden phase.
- New release checks require a fact, planner action, action kind, executor
  boundary, and positive and negative fitness in one change.
- The executor becomes simpler because it is an action interpreter, not a
  second state machine.

## Rejected

- Improving one remediation message while leaving the stop outside the planner.
- A generic runtime-error fact.
- Static checks that only search for the name `release_fail`.
- Automatic merge or destructive Git recovery.
- Editing ADR 0045 in place.
