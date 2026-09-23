# ADR 0027 — Emit-from-prose compiler

## Status
Accepted.

## Decision
The pipeline wire (ADR 0026) sequences X1/X2/X3/X5/X6 around an emit, but it
assumes the skill hand-authors plan.json, audit.json, and emit-manifest.json.
That assumption is the gap: the factory cannot run on prose alone.

This ADR adds `tools/nlc-emit-from-prose.py`, a deterministic v1 compiler that
parses a constrained prose plan into the three JSON artifacts the wire
consumes, plus action-gates.json for X6. Output is fully determined by input,
so it is testable without an LLM.

## Consequences
- `tools/nlc-emit-from-prose.py` is the compiler; `fitness-nlc-emit-from-prose.py`
  proves compile + wire end-to-end on a specimen.
- `planit` skill step 5 may invoke it when the agent has a prose plan rather
  than structured JSON.
- The constrained prose format is the contract; free-form prose is refused
  (default-closed).
- This does not replace the wire; it feeds it. Emit-from-prose -> wire -> emit.
