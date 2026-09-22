# PLANIT pipeline wiring (ADR 0024 / 0026)

The runners X1/X2/X3/X5/X6 are no longer standalone. They are sequenced by
`tools/nlc-pipeline-wire.py`, which the `planit` skill and `nlc maintainer`
invoke around every emit.

## Order

1. **X1** `nlc-action-plan-gate.py` -- action maps to a plan step
2. **X2** `nlc-reverse-audit.py` -- every applicable ADR bound to an action
3. **Emit** -- caller writes the artifact and `emit-manifest.json`
4. **X5** `nlc_emit_audit.py` -- every emit has an audit
5. **X3** `nlc-emit-manifest-enforce.py` -- manifest schema, `unused=na`, gate closed
6. **X6** `nlc-action-gates.py` -- gates of bound ADRs, default-closed

## Invocation

```bash
python3 tools/nlc-pipeline-wire.py \
  --plan <plan.json> \
  --audit <audit.json> \
  --manifest <emit-manifest.json> \
  --action-gates <gates.json>
```

Missing any input file -> `PIPELINE:FAIL` (default-closed, never skipped).

## Skill hook

`.agents/skills/planit/SKILL.md` step 5 (before generate) runs X1+X2.
Step 6.5 (after generate) runs X5+X3+X6 via the same wire.
See `docs/nlc/HARNESS.md` for the command table.
