# PLANIT pipeline wiring (ADR 0024 / 0026 / 0027)

The runners X1/X2/X3/X5/X6 are no longer standalone. They are sequenced by
`tools/nlc-pipeline-wire.py`, which the `planit` skill and `nlc maintainer`
invoke around every emit.

## Order

1. **X1** `nlc-action-plan-gate.py` -- action maps to a plan step
2. **X2** `nlc-reverse-audit.py` -- every applicable ADR bound to an action
3. **Emit-from-prose** `nlc-emit-from-prose.py` (ADR 0027) -- prose plan -> plan/audit/manifest/action-gates JSON
4. **Emit** -- caller writes the artifact beside the manifest
5. **X5** `nlc_emit_audit.py` -- every emit has an audit
6. **X3** `nlc-emit-manifest-enforce.py` -- manifest schema, `unused=na`, gate closed
7. **X6** `nlc-action-gates.py` -- gates of bound ADRs, default-closed

## Invocation

```bash
# 1. compile prose -> JSON
python3 tools/nlc-emit-from-prose.py \
  --prose examples/emit-from-prose/plan.md \
  --out /tmp/nlc-out

# 2. run the wire
python3 tools/nlc-pipeline-wire.py \
  --plan /tmp/nlc-out/plan.json \
  --audit /tmp/nlc-out/audit.json \
  --manifest /tmp/nlc-out/emit-manifest.json \
  --action-gates /tmp/nlc-out/action-gates.json
```

Missing any input file -> `PIPELINE:FAIL` (default-closed, never skipped).

## Skill hook

`.agents/skills/planit/SKILL.md` step 5 may invoke emit-from-prose when the
agent holds prose rather than structured JSON, then runs the wire before
generate (X1+X2) and again after emit (X5+X3+X6).
See `docs/nlc/HARNESS.md` and `docs/nlc/EMIT-FROM-PROSE.md`.
