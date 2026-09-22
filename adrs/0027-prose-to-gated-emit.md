# ADR 0027 — prose to gated emit (goal + policies only)

- Status: Accepted
- Date: 2026-09-22
- Deciders: Human manager
- Class: F (process)
- Corpus: nlc

## Context

The belief: agents write perfect code when the process is suitable. The human
contributes only **goal** and **policies**. Everything else — actions, ADR
bindings, reverse audit, emit, audit, gates — is inference the factory performs.

ADR 0026 gave us the gates. This ADR makes the factory actually run them from
prose, with no LLM in the path.

## Decision

1. `tools/nlc-emit-from-prose.py` compiles a constrained prose plan into
   `plan.json`, `audit.json`, `emit-manifest.json`.
2. The prose author declares `goal:`, optional `policy:`, `action:`, `adr:`,
   `anchor:`. Missing `adr:` defaults to 0024/0025/0026. Missing `action:`
   infers one action from the goal.
3. After compile, `nlc-pipeline-wire.py` runs X1 → X2 → X5 → X3 → X6. Exit 0
   prints `PIPELINE:ALL_MET`.
4. Free-form prose with no `goal:` is refused. The compiler never invents a
   goal — that is the one human input it will not infer.
5. Fitness: `fitness-nlc-emit-from-prose.py` runs `--self-test` and expects
   `SELF_TEST:OK`.

## Consequences

- Prose in, gated emit out, no LLM required for the structural path.
- Semantic X6 gate commands still plug in later; v1 echoes MET.
- X4 hub-interior BBA rewrite remains parked.

## Rejected

- Requiring the human to name every ADR (inference fills defaults).
- Letting the compiler invent the goal (violates "goal is human-only").
- Keeping an LLM in the compile path (process must be deterministic and gated).
