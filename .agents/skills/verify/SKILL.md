---
name: [verify](../../../docs/TERMS.md#verify)
description: [NLC](../../../docs/TERMS.md#nlc) [verify](../../../docs/TERMS.md#verify) — fix compile/requirements issues and refresh fingerprints. Use [/verify](../../../docs/TERMS.md#verify) when ./nlc [verify](../../../docs/TERMS.md#verify) fails or before release.
disable-model-invocation: true
---

# [Verify](../../../docs/TERMS.md#verify)

Human and CI run **`./nlc verify`** (fingerprints + hub releasable **`verify`** profile from [`integrity/releasable-gates.json`](../../../integrity/releasable-gates.json)). When that fails, run the **`Reproduce:`** line from stderr verbatim (often **`./nlc verify --project .`** or **`./nlc gate <id> --tree .`**). Fix blockers, then **`./nlc verify-deep`** to refresh `.nlc/verified.json` when compile gates must pass.

## [Gate](../../../docs/TERMS.md#gate)

| Criterion | Blocking? | Pass when |
| --------- | --------- | --------- |
| `./nlc verify` | yes | Exit 0 after your fixes |
| Fingerprints | yes | `verify-deep` run when intent or goals changed materially |

## Procedure

1. Run **`./nlc`** — read **YOUR QUEUE** (Requirements before Build).
2. Run **`./nlc verify`** — if pass, hand off “ready for release pipeline.”
3. On fail — run the printed **`Reproduce:`** command first; address each **`FAILED`** gate or reason (requirements, regen queue, changed files); use **`/interview`** / **`/planit`** as needed.
4. **Gate after generate ([ADR 0010](../../../adrs/0010-gate-after-every-generate.md)):** if verify cites a stale `implementation.py` or scoped skill path, run the plan's fitness, then `./nlc maintainer gate-record --artifact <path> --gate-id <id> --command "<cmd>"`.
5. **Rule trace ([ADR 0023](../../../adrs/0023-rule-instance-trace-and-instant-audit-scope.md)):** `./nlc maintainer rule-coverage --check` for missing `nlc:rule=` markers; emit via `./nlc maintainer rule-marker --id <rule_id>` on regen, not hand-edited comments.
6. Run **`./nlc verify-deep`** when gates should pass; confirm **`./nlc verify`** is green. Use **`./nlc maintainer`** tools only as needed — not the human's job.

## Done signals

- `./nlc verify` exit 0
- Human knows [verify](../../../docs/TERMS.md#verify) pass means fingerprints match last deep run and pipeline blockers are clear
