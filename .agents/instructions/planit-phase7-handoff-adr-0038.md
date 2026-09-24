# Planit Phase 7 handoff (ADR 0038)

Binding rules for **chat** and **durable** Planit Phase 7 handoffs in this hub. Memory is not a process step ([ADR 0038](../../adrs/0038-no-memory-in-process.md)).

## Gate (default-closed)

| Criterion | Blocking? | Pass when |
| --------- | --------- | --------- |
| Full commands | yes | Every runnable step includes the full command line (no “above”, “below”, “same as before”) |
| SSOT paths | yes | Leaf skills cite repo-relative paths under `.agents/skills/…` |
| Machine evidence | yes | Exit code + pass token (`FULL_NLC_AUDIT:MET`, `CI:MET`, etc.) before inference or **Continuity:** apex |
| No ritual duplicate | yes | Leaf skill exists → handoff says “run skill X”; does not restate skill procedure |
| No manifest inventory | yes | Stage lists only via `integrity/full-nlc-audit-manifest.json` + `python3 tools/full-nlc-audit.py --list-stages --profile <quick\|release-prep\|full>` |

## Forbidden in handoffs

- Deictic references to commands (“run the command above”).
- Copy-pasted manifest stage inventories (“Quick includes: …”).
- Inference-only apex without machine block (**Continuity: PASS** without `FULL_NLC_AUDIT:MET` or equivalent).
- “Remember” / “don’t forget” / “keep in mind” for ordering or gates ([`tools/fitness-adr-0038-no-memory.py`](../../tools/fitness-adr-0038-no-memory.py)).

## Required handoff shape

1. **Produced paths** (repo-relative).
2. **Machine evidence** — command, exit code, pass/fail token.
3. **Gate-standard** — per-path PASS / FAIL / N/A for operation-verdict §2.
4. **Open fix list** if any FAIL.
5. **Verdict — Planit process** — PASS only when phase verdicts PASS.

## Template: `full-nlc-audit` leaf

Machine (Step M):

```bash
python3 tools/full-nlc-audit.py --check --profile quick
```

Hub release prepare uses **`--profile release-prep`**; local verify sweep uses **`--profile full`** (see [`docs/adoption/RELEASE.md`](../../docs/adoption/RELEASE.md)); pass token: `FULL_NLC_AUDIT:MET`, exit code `0`.

Inference (Step I): run [`.agents/skills/full-nlc-audit/SKILL.md`](../skills/full-nlc-audit/SKILL.md) after machine MET — checklist [`.agents/skills/full-nlc-audit/references/inference-phases.md`](../skills/full-nlc-audit/references/inference-phases.md).

Verdict (Step V): **Continuity: PASS | FAIL | PASS with residuals** per skill Step V table, only after machine evidence is recorded.

Stage ids: `python3 tools/full-nlc-audit.py --list-stages --profile quick` (manifest SSOT: `integrity/full-nlc-audit-manifest.json`).
