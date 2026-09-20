# [ADR](../docs/TERMS.md#adr) 0019 — Guided orchestration (one guide, unfinished work resumes)

- Status: Accepted
- Date: 2026-09-20
- Deciders: Human manager
- Class: F (product UX)

## Context

[ADR](../docs/TERMS.md#adr) 0017–0018 require human surfaces that **guide**, not manuals of steps. Adopters should not memorize `check-rules`, `regen-plan`, and ratification order after they say “I added a policy” in `/interview`. Exiting mid-flow must leave **unfinished work** on `./nlc` and `/interview`, with a single prompt to continue or start fresh.

## Decision

1. **Primary human commands** stay short: `./nlc` (status + queue), `/interview` (guide), `/planit` (build & compile), `./nlc verify` (CI). Agents run `./nlc maintainer requirements` after ratification.

2. **`./nlc` preflight:** [Verify](../docs/TERMS.md#verify) install and skills before showing the queue. On failure, stop with **problem + fix** (e.g. `./nlc doctor fix`), per [ADR](../docs/TERMS.md#adr) 0018.

3. **Queue is kanban:** **`/interview` is always-on guide** (not a bucket). Work flows **Requirements → Build & compile → [Verify](../docs/TERMS.md#verify)** (then Maintain). Requirements covers new, updated, and unfinished work (including proposed ADRs) — all before compile. [Verify](../docs/TERMS.md#verify) means prod-ready: requirements ratified and applied, generated goals complete. `.nlc/work-queue.json` refreshes on every `./nlc`. Agents may write `.nlc/pipeline-state.json` and `.nlc/requirements-sync-pending.json`.

4. **Requirements path:** `/interview` drafts and ratifies. Agent runs `./nlc maintainer requirements` (checks + optional regen via `.nlc/last-requirement-change.json`).

5. **Resume:** Any in-flight ratification, regen queue, or guide session appears on `./nlc` and should be picked up by `/interview` (“continue unfinished work or start something new?”).

## Consequences

- [`tools/nlc_requirements_cmd.py`](../tools/nlc_requirements_cmd.py) and `./nlc requirements` replace advertising `check-rules` / `regen-plan` on the short menu.
- Maintainer tools (`check-rule-adoption.py`, `nlc-delta-regen.py`) stay; humans are not trained on their names first.
- Future: [interview](../docs/TERMS.md#interview) writes guide state; hooks call requirements sync after [ADR](../docs/TERMS.md#adr) accept.

## Rejected

- Long menu copy on default `./nlc` output.
- Expecting adopters to run `regen-plan` manually after every policy change.
