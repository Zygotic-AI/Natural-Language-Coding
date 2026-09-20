# Brownfield adoption (beta)

NLC confidence is **higher for greenfield** than for existing codebases. Brownfield is supported as a **manual** path until inventory, binding, and delta-regen mature.

## Greenfield (supported)

```bash
python3 /path/to/nlc-hub/tools/nlc-init.py ~/projects/my-new-app --name MyApp
```

See [BOOTSTRAP.md](BOOTSTRAP.md).

## Brownfield (beta)

1. Do **not** use `nlc-init` on repos with existing `domain/` or `goals/` content.
2. Follow [BOOTSTRAP.md](BOOTSTRAP.md): charter, CI hooks, interview-first.
3. Introduce **one noun + one goal** behind gates before migrating legacy modules.
4. Use [`tools/nlc-delta-regen.py`](../../tools/nlc-delta-regen.py) after contract changes (UC9 v1 plan).
5. Expect judgment gaps (R1/C3/C4) — no static gate replaces “is this the right noun?”

Record adoption ADR in the app repo when you commit to the shape.
