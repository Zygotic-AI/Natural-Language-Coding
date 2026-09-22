# [ADR](../docs/TERMS.md#adr) 0017 — Human surface (menu, language, and entry)

- Status: Accepted
- Date: 2026-09-20
- Deciders: Human manager
- Class: F (product UX)

## Context

Adopters are not [hub](../docs/TERMS.md#hub) maintainers. Exposing dozens of `python3 tools/*.py` scripts and internal acronyms (BBP, UC*, ASC) fails the product promise. Humans need one place to see work in flight, [workflow](../docs/TERMS.md#workflow) order, and the **next [action](../docs/TERMS.md#action)**—often a single agent instruction, not a shell command.

This [ADR](../docs/TERMS.md#adr) applies to **every human surface**: anything an [adopter](../docs/TERMS.md#adopter) (or other non-maintainer) reads or runs without an explicit “machine/CI mode.” That includes the `./nlc` launcher and dashboard, install and upgrade scripts, [adopter](../docs/TERMS.md#adopter) templates, [hub](../docs/TERMS.md#hub) and app docs written for adopters, copy-paste agent prompts shown in menus or getting-started flows, and **user-visible text** from tools when a human is the audience—not only [`tools/nlc.py`](../tools/nlc.py).

## Decision

1. **Preferred entry:** Humans run **`./nlc`** at the repo root (or `nlc` on PATH after install). Do not document or train adopters on `python3 tools/…` as the primary path. Technical scripts remain for CI, agents, and hooks; when a human still invokes them, their **stdout/stderr meant for the human** must follow this [ADR](../docs/TERMS.md#adr) and [ADR 0018](0018-human-cli-interview-on-gap.md).

2. **Jargon-free labels:** Human-visible strings avoid [BBP](../docs/TERMS.md#bbp), UC numbers, [PLANIT](../docs/TERMS.md#planit), [charter](../docs/TERMS.md#charter) ids, and fitness [gate](../docs/TERMS.md#gate) vocabulary (`MET`, `NOT_MET`, `TOOL:*` apex lines) as headlines. Internal docs, maintainer runbooks, and agent-only skills may keep technical names; anything shown or copied by adopters maps to plain language.

3. **Ordered menu:** Sections follow typical adoption and compile order. Numbers imply sequence within a section; section breaks mean a phase completed (e.g. after “Adopt repo”, next section is “Build”). Same ordering rules apply wherever the [workflow](../docs/TERMS.md#workflow) is surfaced (dashboard, `MENU.md`, onboarding prompts).

4. **Queue / dashboard:** Persist in-app state under `.nlc/` (work queue, locks, pack installs). Surfaces that show work in flight use the same jargon-free labels and suggest the next [action](../docs/TERMS.md#action).

5. **Agent bridge (v1):** When work needs inference, human surfaces print an explicit step: `In your agent chat, run: /skill …` (copy-paste). v2: harness hooks invoke the agent without paste. Published prompts and skills **shown to adopters** use the same bridge wording, not internal skill codenames.

5b. **Human vs harness names:** Menu and dashboard use [adopter](../docs/TERMS.md#adopter) language (**build & compile**, **get guided**). Harness slash commands may differ (`/planit` = build & compile; `/interview` = guided conversation for any [goal](../docs/TERMS.md#goal), not a narrow “intent only” phase). Do not point adopters at maintainer docs as the primary next step.

6. **Hooks (future):** Menu actions may trigger Cursor hooks / SDK; not required for v0.1 menu text.

7. **Gaps and failures:** Any human surface that stops because input or state is incomplete follows [ADR 0018](0018-human-cli-interview-on-gap.md).

## Consequences

- [`tools/nlc.py`](../tools/nlc.py) is the primary human CLI; install adds it to PATH when possible.
- [`docs/nlc/MENU.md`](../docs/nlc/MENU.md) and related [NLC](../docs/TERMS.md#nlc) docs comply with this [ADR](../docs/TERMS.md#adr).
- Install scripts ([`scripts/install.sh`](../scripts/install.sh), [`scripts/install.ps1`](../scripts/install.ps1)), [adopter](../docs/TERMS.md#adopter) launchers ([`templates/adopter/`](../templates/adopter/)), and human-oriented README / getting-started paths use jargon-free copy.
- [BBP](../docs/TERMS.md#bbp) skills (`bbp-*`) are **not** shown to humans by name; menus and prompts use plain-language aliases.
- New human-facing scripts, prompts, or tool messages are reviewed against [ADR](../docs/TERMS.md#adr) 0017 and 0018 before [ship](../docs/TERMS.md#ship).

## Rejected

- Teaching adopters the `tools/` directory layout as the product UX.
- Human-facing “[bbp-confirmer](../docs/TERMS.md#bbp-confirmer)” or similar skill names in product UI.
- Treating [ADR](../docs/TERMS.md#adr) 0017 as applying only to `nlc.py` while other adopters paths keep [gate](../docs/TERMS.md#gate) jargon.
