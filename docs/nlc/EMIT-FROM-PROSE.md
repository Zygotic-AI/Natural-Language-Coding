# Emit-from-prose (ADR 0027)

The wire (ADR 0026) needs plan/audit/manifest JSON. This compiler produces
them from a constrained prose plan so a real emit can run without
hand-authored JSON.

## Compile

```bash
python3 tools/nlc-emit-from-prose.py \
  --prose examples/emit-from-prose/plan.md \
  --out /tmp/nlc-out
```

Writes `plan.json`, `audit.json`, `emit-manifest.json`, `action-gates.json`.
Then run the wire:

```bash
python3 tools/nlc-pipeline-wire.py \
  --plan /tmp/nlc-out/plan.json \
  --audit /tmp/nlc-out/audit.json \
  --manifest /tmp/nlc-out/emit-manifest.json \
  --action-gates /tmp/nlc-out/action-gates.json
```

## Prose format

```text
# <title>
## Step <id>: <description>
- Action <id>: <description> [adr:<id>,...]
## Emit <id>: <artifact_path>
  trace: <decision>
  anchor: <thought anchor>
```

Every action must name an ADR. Every step must have an action. Every emit
must name a path. Anything else is refused.
