# [Hub](../docs/TERMS.md#hub) semver migrations (adopter contract)

SSOT: [ADR 0014](../adrs/0014-semver-upgrade-steps-and-noop-migrations.md).

Each published [hub](../docs/TERMS.md#hub) version has a [migration unit](../docs/TERMS.md#migration-unit) for the step **from the previous semver** into this version. **Absence is an error**; a release with no adopter-facing changes still ships an explicit **no-op** unit.

## Layout (target)

```text
migrations/
  1.2.2_to_1.2.3/
    migration.yaml    # kind: noop | script | interview
    run               # optional; noop may be manifest-only
```

## `migration.yaml` (sketch)

```yaml
from: 1.2.2
to: 1.2.3
kind: noop
# kind: script → run must exist
# kind: interview → blocking patterns / checklist id
```

## Orchestrator logging

Per step (required):

```text
UPGRADE:STEP from=1.2.2 to=1.2.3 kind=noop
UPGRADE:STEP_COMPLETED to=1.2.3
```

Missing unit:

```text
UPGRADE:NOT_MET
  missing: migration 1.2.2_to_1.2.3
```

Orchestrator: [`tools/nlc-update.py`](../tools/nlc-update.py). [Hub](../docs/TERMS.md#hub) artifact replace and lock bump happen in the same step as the [migration unit](../docs/TERMS.md#migration-unit) runs.

Bootstrap step `0.0.0_to_0.1.0` (noop) documents the first published [hub](../docs/TERMS.md#hub); app locks start at `0.1.0`.
