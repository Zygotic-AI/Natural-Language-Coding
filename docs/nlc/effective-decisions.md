# Effective decisions

A later record can amend one decision without editing the earlier record. This page is the readable result. It is not a new decision.

No new decision record: record 0045 stays as accepted. Record 0048 is still Proposed and says it amends only the executor location.

## Record 0045 decision 2, as amended by record 0048 decision 5

Record 0045 decision 2, unchanged in [`adrs/0045-hub-release-identity.md`](../../adrs/0045-hub-release-identity.md):

The planner in `tools/nouns/release_state/release_state.py` is pure: facts in, one phase, one action. `tools/nlc_release_state.py` observes git and GitHub and does not mutate. Infer and resume do not choose a second phase.

Where the executor lives, from record 0048 decision 5 in [`adrs/0048-executable-shape.md`](../../adrs/0048-executable-shape.md):

Release policy lives in `goals/hub_release/execute.sh`. `scripts/nlc-release.sh` is the thin entrypoint. It performs only the planned action. The planner remains the only action selection.

The sentence in record 0045 that names `scripts/nlc-release.sh` as the place the policy lives is the part this amendment replaces. The rest of decision 2 stands.
