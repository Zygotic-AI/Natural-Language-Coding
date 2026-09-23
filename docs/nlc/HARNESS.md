# Harness wire-up (UC18)

[Knowledge domains](../TERMS.md#knowledge-domain) must load **before generate**, not discovered during a late [ship](../TERMS.md#ship) [audit](../TERMS.md#audit).

## Required calls

| When | Command / skill |
| ---- | ---------------- |
| [Interview](../TERMS.md#interview) | knowledge-steward `load-knowledge-domain` / `flag-gap` ([`/interview`](../../.agents/skills/interview/SKILL.md)) |
| [Planit](../TERMS.md#planit) step 6 (before emit) | `./nlc maintainer guide before-generate --scope <topic>` (runs `nlc-before-generate.py` + stamp) — [`nlc-before-generate.md`](../../.agents/skills/planit/references/nlc-before-generate.md) |
| [Planit](../TERMS.md#planit) pipeline wire (ADR 0024/0030) — **before emit** | `python3 tools/nlc-pipeline-wire.py --plan <plan.json> --audit <audit.json> --manifest <emit-manifest.json> --action-gates <gates.json>` — runs X1 (action↔plan) + X2 (reverse audit). **FAIL → do not emit.** See [`PIPELINE-WIRING.md`](PIPELINE-WIRING.md). |
| [Planit](../TERMS.md#planit) pipeline wire (ADR 0024/0030) — **after emit** | same command; now runs X5 (emit audit) + X3 (manifest schema, `unused=na`) + X6 (bound ADR gates, default-closed). **FAIL → stop.** |
| [Planit](../TERMS.md#planit) step 6 (scope) ([ADR 0010](../../adrs/0010-gate-after-every-generate.md)) | `./nlc maintainer gate-scope --add <path>` |
| [Planit](../TERMS.md#planit) step 6.5 (after gate PASS) ([ADR 0010](../../adrs/0010-gate-after-every-generate.md)) | `./nlc maintainer gate-record --artifact <path> --gate-id <id> --command "<cmd>"` — [`GATE-RECORD-BINDER.md`](GATE-RECORD-BINDER.md) |
| Rule instance audit ([ADR 0023](../../adrs/0023-rule-instance-trace-and-instant-audit-scope.md)) | `./nlc maintainer rule-coverage --adr <id> [--tag <t>] [--check]` — [`RULE-TRACE.md`](RULE-TRACE.md) |
| Rule receipt emit ([ADR 0023](../../adrs/0023-rule-instance-trace-and-instant-audit-scope.md)) | `./nlc maintainer rule-marker --id <rule_id> [--lang python\|js\|ts]` |
| Goal implementation scaffold ([ADR 0023](../../adrs/0023-rule-instance-trace-and-instant-audit-scope.md)) | `./nlc maintainer goal-scaffold --goal <id>` |
| Breaking published contract ([ADR 0006](../../adrs/0006-contract-change-notice.md)) | `./nlc maintainer contract-break-accept --schema <path> --adr <id> --accepted-by 'role:…'` |
| Session start (hub work) | `bash tools/session-preflight.sh` |

## [Default-closed](../TERMS.md#default-closed)

If `nlc-before-generate.py` exits non-zero, **do not generate**. Fix facts, waive with explicit `Assumption:`, or continue [interview](../TERMS.md#interview).
If `nlc-pipeline-wire.py` exits non-zero at any stage, **do not emit** (before) or **do not proceed** (after). No stage is skippable.

## CI (app repo)

On every PR, run **`./nlc verify`**. [Workflow](../TERMS.md#workflow) template: `.github/workflows/nlc-verify.yml` from `nlc-init`.

**Hooks (v2):** `.nlc/hooks.example.json` only — menu actions and optional [UC18](../TERMS.md#uc18) hook shape. [Hub](../TERMS.md#hub) does **not** [ship](../TERMS.md#ship) active Cursor/SDK wiring; copy into your harness when supported.

**Judgment (not automatable):** [`HUMAN-JUDGMENT-GATES.md`](HUMAN-JUDGMENT-GATES.md).

**[UC9](../TERMS.md#uc9) regen queue:** `./nlc maintainer regen-continue` → `/planit` → `./nlc maintainer regen-advance` per [goal](../TERMS.md#goal).

[Ship](../TERMS.md#ship) promotion semantics: [`VERIFY-AND-SHIP.md`](VERIFY-AND-SHIP.md).
