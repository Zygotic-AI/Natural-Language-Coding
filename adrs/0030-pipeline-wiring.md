# ADR 0030 — Pipeline wiring (X1/X2/X3/X5/X6)

## Status
Accepted.

Depends on ADR 0026 (X1–X3 runners promoted to law). This ADR sequences those runners (plus X5/X6) around every emit. Consequences updated: runners are now sequenced by `tools/nlc-pipeline-wire.py`.

## Decision
The five runners (X1 action-plan, X2 reverse-audit, X3 emit-manifest, X5 emit-audit, X6 bound ADR gates) are no longer standalone. A single default-closed wire sequences them around every emit:

1. **Before emit:** X1 (action↔plan) → X2 (every applicable ADR bound)
2. **Emit:** caller writes artifact + `emit-manifest.json`
3. **After emit:** X5 (audit present) → X3 (schema, `unused=na`, gate closed) → X6 (bound ADR gates)

Any stage failing → no emit (before) or no proceed (after). No stage is skippable.

## Consequences
- `tools/nlc-pipeline-wire.py` is the call site; `nlc-action-gates.py` runs X6.
- `planit` skill step 5 runs the wire before generate; step 5c runs it after emit.
- `docs/nlc/HARNESS.md` and `PLANIT-ORCHESTRATION.md` document both calls.
- `fitness-nlc-pipeline-wire.py` + `fitness-nlc-action-gates.py` keep the wire honest in CI.
- Individual runners remain invokable standalone for testing; the wire is what production calls.
