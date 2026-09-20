# [ADR](../docs/TERMS.md#adr) 0018 — [Interview](../docs/TERMS.md#interview) the human when input or state is incomplete

- Status: Accepted
- Date: 2026-09-20
- Deciders: Human manager
- Class: F (product UX)

## Context

[ADR 0017](0017-human-command-surface.md) defines jargon-free **human surfaces** (not only `./nlc`). When any of those surfaces lacks required input or hits a problematic state, printing fitness-style tokens (for example `NLC:NOT_MET`, `INSTALL:NOT_MET`) or raw parser errors reads like an internal [gate](../docs/TERMS.md#gate), not a product conversation. Adopters should understand **what went wrong**, **what you need from them**, and **how they can fix it**—including choices when more than one remediation is valid.

**Scope:** Same as [ADR](../docs/TERMS.md#adr) 0017—install and upgrade scripts, launchers, dashboards, [adopter](../docs/TERMS.md#adopter) docs, published prompts, and **any tool or script message** where a human is the intended reader. CI, fitness jobs, hooks, and agents may still consume `TOOL:MET|NOT_MET` and related lines ([`0013-requirements-preflight.md`](0013-requirements-preflight.md), upgrade orchestration) when humans are not the primary audience, provided adopters are not shown those tokens as the main explanation.

## Decision

When a **human surface** stops because something is missing or problematic, respond with a **short [interview](../docs/TERMS.md#interview)**, not a single failure token.

Each response includes, in order:

1. **Problem** — One plain-language sentence: what blocked progress (no gate jargon, no charter ids).
2. **What’s missing or wrong** — Concrete items (paths, flags, files, versions). List every blocking gap in one pass when multiple are known ([`0013`](0013-requirements-preflight.md) spirit).
3. **Ask** — Direct questions for information only the human can supply (“Which folder should the new app use?”, “What name should we use for the app?”).
4. **Remediation choices** — When the system can fix or route the problem in more than one way, state options and ask how they want to proceed (for example: create a new folder vs adopt an existing repo; export vs install a pack; run doctor vs open the menu; skip verify vs fix install). A default suggestion is allowed; forcing a single path without saying so is not.
5. **Examples** — Copy-pasteable commands or agent prompts where that shortens the loop.

**Tone:** Second person (“you”), short sentences, no MET/NOT_MET/DASHBOARD tokens as the **first** line humans see. Success paths may print useful body text without requiring a machine apex line.

**Machine layer:** When the same program serves CI and humans, stable parse lines may appear on stderr, after the [interview](../docs/TERMS.md#interview), or under `--json` / documented env flags. Parsers must not depend on humans reading those tokens.

**Agent bridge:** When remediation needs inference, the [interview](../docs/TERMS.md#interview) ends with an explicit agent step (ADR 0017), not “fix it yourself” with no path.

**Prompts:** Intake or validation sections in human-facing prompts that block execution use the same five-part shape (problem, gaps, ask, choices, examples)—not only shell CLIs.

## Consequences

- [`tools/nlc_cli_help.py`](../tools/nlc_cli_help.py) (or successor) is the reference implementation for `./nlc`; the **pattern** is mandatory everywhere adopters see failures.
- Install, upgrade, pack, and launcher scripts replace gate-first messages with interviews when humans run them.
- [Hub](../docs/TERMS.md#hub) tools invoked on human paths translate or emit interview-shaped output; maintainers may keep `TOOL:NOT_MET` for machine-only exits when no human reads stdout/stderr.
- [`docs/nlc/MENU.md`](../docs/nlc/MENU.md), dashboard copy, and [adopter](../docs/TERMS.md#adopter) onboarding prompts align with [interview](../docs/TERMS.md#interview) wording.
- New human-facing scripts, tools, and prompts document or implement [interview](../docs/TERMS.md#interview) templates for missing args and failed preconditions.

## Rejected

- Leading human-visible output with `*:NOT_MET` (or similar) as the only explanation.
- Argparse-only “error: the following arguments are required” with no problem statement, ask, or remediation choices.
- Silent non-zero exit with no [interview](../docs/TERMS.md#interview) text on human paths.
- Treating “list an example command” as sufficient without stating the problem and what to decide.
- Scoping [ADR](../docs/TERMS.md#adr) 0018 to `./nlc` only while install scripts and tools keep [gate](../docs/TERMS.md#gate) headlines for adopters.
