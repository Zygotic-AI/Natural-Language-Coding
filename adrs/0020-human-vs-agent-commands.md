# [ADR](../docs/TERMS.md#adr) 0020 — Human commands vs agent-invoked tools

- Status: Accepted
- Date: 2026-09-20
- Deciders: Human manager
- Class: F (product UX)

## Context

[ADR](../docs/TERMS.md#adr) 0017–0019 describe guide, requirements, build, and [verify](../docs/TERMS.md#verify). If a human runs a shell command that **cannot finish** without inference (drafting ADRs, ratifying, generating code, fixing rule conflicts by judgment), they get sent to the agent anyway — script → paste → script violates “simple for humans.”

## Decision

1. **Human-run commands** (complete without inference; OK in the command map and queue **→** lines):
   - **`./nlc`** — status, preflight, queue refresh
   - **`./nlc doctor`** / **`./nlc doctor fix`** — install repair
   - **`./nlc new`** — [greenfield](../docs/TERMS.md#greenfield) scaffold (args required)
   - **`./nlc adopt-existing`** — [brownfield](../docs/TERMS.md#brownfield) inventory (beta)
   - **`./nlc verify`** — fast fingerprint check (CI); **`./nlc verify-deep`** — full gates + refresh `.nlc/verified.json`
   - **`./nlc upgrade`**, **`./nlc ship-check`**, **`./nlc pack`** (with args) — machine orchestration

2. **Agent-run** (human uses **`/interview`** or **`/planit`**; the agent invokes [hub](../docs/TERMS.md#hub) tools via shell when a machine step is needed — not the human):
   - **Requirements work** — new, update, unfinished, ratify, adopt rules, regen planning after policy change. Human does not start `./nlc requirements` as the primary [action](../docs/TERMS.md#action); the agent runs it (and `check-rule-adoption.py`, `nlc-delta-regen.py`, etc.) inside the guided session.
   - **Build & compile** — `/planit` only for humans; generate, bind, plan audits.
   - **Guide** — `/interview` only for humans; surfaces queue and walks any [workflow](../docs/TERMS.md#workflow).

3. **[Verify](../docs/TERMS.md#verify) (`./nlc verify`)** does not require inference on **pass**; on **fail**, instruct **`/verify`** in the agent (ADR 0021). CI may [gate](../docs/TERMS.md#gate) on `./nlc verify` exit 0.

4. **Human surfaces** (dashboard, menu, queue) must not list agent-only commands as the next step when inference is required. Queue buckets name the **outcome** (“Requirements unfinished”) with **→ [/interview](../docs/TERMS.md#interview)** (or **/planit** for build), not “run `./nlc requirements` then go to agent.”

5. **Maintainer / CI** may call any `tools/*` or `nlc` subcommand directly.

## Consequences

- [`tools/nlc_menu_data.py`](../tools/nlc_menu_data.py) human map: no `./nlc requirements` or hidden build scripts as primary adopters steps.
- [`tools/nlc_dashboard.py`](../tools/nlc_dashboard.py) queue **→** lines follow §4.
- **`/verify`**, **`/interview`**, and **`/planit`** skills document when to run `./nlc requirements`, `./nlc verify-deep`, etc. from the agent.
- `./nlc maintainer requirements` (and `check-rules`, `regen-plan`) for **agents and automation** only.

## Rejected

- Humans alternating `./nlc requirements` and copy-paste `/interview` for one requirements change.
- Advertising `check-rules` / `regen-plan` on the human map.
