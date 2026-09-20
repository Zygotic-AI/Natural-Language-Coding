# Harness wire-up (UC18)

[Knowledge domains](../TERMS.md#knowledge-domain) must load **before generate**, not discovered during a late [ship](../TERMS.md#ship) [audit](../TERMS.md#audit).

## Required calls

| When | Command / skill |
| ---- | ---------------- |
| [Interview](../TERMS.md#interview) | knowledge-steward `load-knowledge-domain` / `flag-gap` ([`/interview`](../../.agents/skills/interview/SKILL.md)) |
| [Planit](../TERMS.md#planit) step 6 (before emit) | `./nlc maintainer guide before-generate --scope <topic>` (runs `nlc-before-generate.py` + stamp) — [`nlc-before-generate.md`](../../.agents/skills/planit/references/nlc-before-generate.md) |
| [Planit](../TERMS.md#planit) step 6.5 (after gate PASS) | `./nlc maintainer gate-record --artifact <path> --gate-id <id> --command "<cmd>"` |
| Session start (hub work) | `bash tools/session-preflight.sh` |

## [Default-closed](../TERMS.md#default-closed)

If `nlc-before-generate.py` exits non-zero, **do not generate**. Fix facts, waive with explicit `Assumption:`, or continue [interview](../TERMS.md#interview).

## CI (app repo)

On every PR, run **`./nlc verify`**. [Workflow](../TERMS.md#workflow) template: `.github/workflows/nlc-verify.yml` from `nlc-init`.

**Hooks (v2):** `.nlc/hooks.example.json` only — menu actions and optional [UC18](../TERMS.md#uc18) hook shape. [Hub](../TERMS.md#hub) does **not** [ship](../TERMS.md#ship) active Cursor/SDK wiring; copy into your harness when supported.

**Judgment (not automatable):** [`HUMAN-JUDGMENT-GATES.md`](HUMAN-JUDGMENT-GATES.md).

**[UC9](../TERMS.md#uc9) regen queue:** `./nlc maintainer regen-continue` → `/planit` → `./nlc maintainer regen-advance` per [goal](../TERMS.md#goal).

[Ship](../TERMS.md#ship) promotion semantics: [`VERIFY-AND-SHIP.md`](VERIFY-AND-SHIP.md).
