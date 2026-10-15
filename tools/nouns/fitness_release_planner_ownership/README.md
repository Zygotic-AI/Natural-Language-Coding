# fitness_release_planner_ownership

ADR 0049 fitness. The release planner owns every intentional stop.

`planner_ownership_errors(root)` inspects:

- `goals/hub_release/execute.sh`
- `tools/nouns/release_state/release_state.py`
- `tools/nouns/nlc_release_state/nlc_release_state.py`

A passing executor has no `set -e`, keeps nonzero and dynamic exits inside `dispatch_release_plan`, and runs a planner action loop. Each `REPAIR` action has an `action_result_boundary:<ACTION>` token, and a Python failure reaches a stop only through that boundary. `git merge`, `git push --force`, `git tag -f`, `git stash`, and `git reset --hard` are forbidden automatic repairs.

The planner `ACTION_KINDS` registry is the closed ADR 0049 action set with kinds `REPAIR`, `AWAIT`, `HUMAN_DECISION`, and `TERMINAL`. Each repair also has a non-empty `ACTION_PROGRESS_FACTS` tuple. The observer publishes `main_context` and has no generic runtime-error fact.
