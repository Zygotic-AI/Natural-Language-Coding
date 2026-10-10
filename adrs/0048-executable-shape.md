# ADR 0048 — Executable shape

- Status: Accepted
- Date: 2026-10-08
- Deciders: Human manager
- Ratified-by: Human manager (practice-enforcement task list, 2026-10-08)
- Class: C (goal shape) with class F enforcement
- Corpus: nlc

## Context

Boundary-Based Programming is the noun, verb, adjective, and goal practice. Boundary-Based Architecture is the boundary and contract shape. Neither is a runtime that executes the code. Hub executables still included policy shells, and nothing counted an unclassified file as a failed compile.

## Decision

1. Executable kinds are Python, shell, workflows, tests, fixtures, generated code, templates, migrations, vendored code, and configuration.
2. Each scanned file is exactly one of: noun implementation, goal, primitive adapter, thin entrypoint, or contained fixture.
3. Deliberate failure specimens are contained fixtures. They are not required to conform.
4. A thin entrypoint may parse input, call one noun verb or goal, and report the result. It may not own policy or a state machine.
5. Release policy lives in `goals/hub_release/execute.sh`. `scripts/nlc-release.sh` is the thin entrypoint. This amends ADR 0045 decision 2 only as to where the executor lives. The planner remains the only action selection.
6. `tools/nouns/executable_shape/` is the kernel. An exemption list that names its own files fails.
7. The hub compile fails when the unclassified count is not zero. The gate is on only because the inventory classifies every scanned file.

## Consequences

- Install, release preparation, release smoke, session preflight, and fitness check 1 policy live under `goals/`.
- Version class for this policy is minor.

## Rejected

- A runtime that executes Boundary-Based Programming.
- An exemption list the kernel can use on itself.
- Turning the gate on while unclassified files remain.
