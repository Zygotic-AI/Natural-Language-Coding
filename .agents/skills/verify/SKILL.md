---
name: [verify](../../../docs/TERMS.md#verify)
description: [NLC](../../../docs/TERMS.md#nlc) [verify](../../../docs/TERMS.md#verify) — fix compile/requirements issues and refresh fingerprints. Use [/verify](../../../docs/TERMS.md#verify) when ./nlc [verify](../../../docs/TERMS.md#verify) fails or before release.
disable-model-invocation: true
---

# [Verify](../../../docs/TERMS.md#verify)

Human and CI run **`./nlc verify`** (fast fingerprints). When that fails, the human uses **`/verify`** — you fix blockers and run **`./nlc verify-deep`** to refresh `.nlc/verified.json`.

## [Gate](../../../docs/TERMS.md#gate)

| Criterion | Blocking? | Pass when |
| --------- | --------- | --------- |
| `./nlc verify` | yes | Exit 0 after your fixes |
| Fingerprints | yes | `verify-deep` run when intent or goals changed materially |

## Procedure

1. Run **`./nlc`** — read **YOUR QUEUE** (Requirements before Build).
2. Run **`./nlc verify`** — if pass, hand off “ready for release pipeline.”
3. On fail — address each reason (requirements, regen queue, changed files); use **`/interview`** / **`/planit`** as needed.
4. Run **`./nlc verify-deep`** when gates should pass; confirm **`./nlc verify`** is green. Use **`./nlc maintainer`** tools only as needed — not the human's job.

## Done signals

- `./nlc verify` exit 0
- Human knows [verify](../../../docs/TERMS.md#verify) pass means fingerprints match last deep run and pipeline blockers are clear
