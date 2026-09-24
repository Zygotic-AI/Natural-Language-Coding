# Full NLC audit

Single entrypoint for **continuity** (belief → decision → requirement → gate → product story), distinct from adopter compile-only checks ([`VERIFY-AND-SHIP.md`](VERIFY-AND-SHIP.md)).

## Commands

| When | Command |
| ---- | ------- |
| Default / CI landmine | `python3 tools/full-nlc-audit.py --check --profile quick` |
| Hub release prepare | `python3 tools/full-nlc-audit.py --check --profile release-prep` (see [`docs/adoption/RELEASE.md`](../adoption/RELEASE.md)) |
| Local pre-ship (verify included) | `python3 tools/full-nlc-audit.py --check --profile full` (clean tree; `--allow-dirty` optional) |
| Inference checklist only | `python3 tools/full-nlc-audit.py --emit-inference-checklist` |
| Agent session | [`.agents/skills/full-nlc-audit/SKILL.md`](../../.agents/skills/full-nlc-audit/SKILL.md) — Step M then Step I |

Pass: stdout line `FULL_NLC_AUDIT:MET`. Fail: `FULL_NLC_AUDIT:NOT_MET` + failed stage ids.

## Manifest (stage inventory SSOT)

**Only** [`integrity/full-nlc-audit-manifest.json`](../../integrity/full-nlc-audit-manifest.json) defines profiles and stages. Do not copy stage lists into handoffs or operator prose.

List stage ids for a profile:

```bash
python3 tools/full-nlc-audit.py --list-stages --profile <quick|release-prep|full>
```

Builtin stage **`integration-leaves`** is implemented in [`tools/full-nlc-audit.py`](../../tools/full-nlc-audit.py) (`integration_leaves`); data SSOT: [`integrity/integration-leaves.json`](../../integrity/integration-leaves.json).

## Planit Phase 7 handoffs

[`.agents/instructions/planit-phase7-handoff-adr-0038.md`](../../.agents/instructions/planit-phase7-handoff-adr-0038.md) (ADR 0038).

## Layers

| Layer | Tool |
| ----- | ---- |
| Machine stack | `tools/full-nlc-audit.py` |
| Compile / fingerprints | Included only in `--profile full` (see manifest) |
| Inference checklist | `.agents/skills/full-nlc-audit/references/inference-phases.md` |
