# Impact graph (R21) and blast radius (UC9)

The **impact graph** is how NLC maps **goals → noun.verb call sites** in generated code so requirement and contract changes touch only the right blast radius.

## Principles

- **Generated, not hand-edited** — Charter R21. Graphs come from [`tools/generate-impact-graph.py`](../../tools/generate-impact-graph.py) (or language-pack scanners later). Fitness forbids checked-in hand-authored graphs as SSOT.
- **Map anything you bind** — Goals call verbs on nouns; nouns live under `domain/`; rules and ADRs bind to tags/primitives. The v1 graph is **goal-centric call edges**; v2+ adds rule/tag edges and cross-repo pack bindings.
- **Delta-regen consumes the graph** — [`tools/nlc-delta-regen.py`](../../tools/nlc-delta-regen.py) plans which goals to re-bind, re-generate, and re-prove after a change.

## v1 graph shape (stdout JSON)

```json
{
  "generated": true,
  "do_not_edit": true,
  "source": "tools/generate-impact-graph.py",
  "goals": {
    "record-bank-payment": {
      "path": "goals/record-bank-payment/main.py",
      "calls": ["invoice.apply_payment"]
    }
  }
}
```

### Build for an adopter repo

```bash
python3 tools/generate-impact-graph.py /path/to/app-repo
# optional persist (derived only):
python3 tools/nlc-impact-graph.py /path/to/app-repo --write
```

[`tools/nlc-impact-graph.py`](../../tools/nlc-impact-graph.py) writes `generated/impact-graph.json` when asked — still derived; regenerate after code changes.

## UC9 change kinds

| `--change` | Blast radius |
| ---------- | ------------- |
| `verb:Invoice.apply_payment` | Goals that call that verb |
| `noun:Invoice` | Goals calling any `Invoice.*` verb |
| `goal:record-bank-payment` | That goal only |
| `rule:<id>` | Goals listed in [`rules/goal-bindings.json`](../../rules/goal-bindings.json) by `rules` / `tags` overlap with the adopted rule’s match tags; else conservative (all goals) |

## Orchestrated regen

Plan only (v1):

```bash
python3 tools/nlc-delta-regen.py . --change verb:Invoice.apply_payment
```

Orchestration (v2 — machine checklist + queue file):

```bash
python3 tools/nlc-delta-regen.py . --change verb:Invoice.apply_payment --orchestrate --write-queue
```

Writes `.nlc/delta-regen-queue.json` and prints `DELTA_REGEN:STEP` lines. Run PLANIT per step; gate after each generate (ADR 0010). Full-tree prove after the queue completes.

## Language packs (future)

Per-stack packs extend **how** edges are discovered (AST instead of regex), not **whether** the graph is generated. See [`docs/nlc/README.md`](../nlc/README.md) roadmap.
