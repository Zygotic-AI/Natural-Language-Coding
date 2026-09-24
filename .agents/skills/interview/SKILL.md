---
name: [interview](../../../docs/TERMS.md#interview)
description: [NLC](../../../docs/TERMS.md#nlc) guided conversation — extract the human's **goal** and **policies** in plain language; map to patterns internally; hand off to build when ready. Use [/interview](../../../docs/TERMS.md#interview) anytime, not only before first compile. [ADR 0036](../../../adrs/0036-inference-only-human-surface.md) goal + policy only; everything else is inference.
disable-model-invocation: true
---

# [Interview](../../../docs/TERMS.md#interview) (UC1)

**Human promise (ADR 0017 + ADR 0036):** the [adopter](../../../docs/TERMS.md#adopter) says what they are trying to accomplish and what constrains it; **you** extract **goal** and **policy**, derive everything else, and ask simple questions. Do **not** ask them to name ADRs, rule ids, thought anchors, manifests, or tags. Do **not** send them to read `INTERVIEW-PATTERNS.md` or other long docs—load that catalog yourself from [`INTERVIEW-PATTERNS.md`](../../../docs/nlc/compiler/INTERVIEW-PATTERNS.md) and match their [goal](../../../docs/TERMS.md#goal) (greenfield vs brownfield, PCI/compliance packs, stuck on next step, etc.).

Outcome-only intake when the work is bind-before-build. This can be **[PLANIT](../../../docs/TERMS.md#planit) step 1** / [AWL](../../../docs/TERMS.md#awl) Phase 0–1 compressed. Do not generate [noun](../../../docs/TERMS.md#noun) or [goal](../../../docs/TERMS.md#goal) code in this skill.

SSOT: [`docs/nlc/compiler/PROCESS.md`](../../../docs/nlc/compiler/PROCESS.md) § [Interview](../../../docs/TERMS.md#interview); [`INTENT-SURFACE.md`](../../../docs/nlc/compiler/INTENT-SURFACE.md).

## [Gate](../../../docs/TERMS.md#gate) (default-closed)

| Criterion | Blocking? | Pass when |
| --------- | --------- | --------- |
| Outcome one-line | yes | Problem, user, success shape stated |
| Goal named | yes | At least one [goal](../../../docs/TERMS.md#goal) in the human's words or explicit “no new goals” with reason |
| Policies stated | yes | Constraints / standards / “must / must not” stated or `Waived:` with reason |
| Knowledge gaps | yes | `knowledge-steward` `load-knowledge-domain` / `flag-gap`; facts derived from policy; gaps closed or `Assumption:` |
| Emit forbidden | yes | No [PLANIT](../../../docs/TERMS.md#planit) generate, no durable code writes |
| No derived authorship | yes | Human was not asked to author plans, ADR ids, rule ids, anchors, manifests, or tags |

## When you block (ADR 0018)

When you must stop before bind-ready, speak to the human in **plain language**—not `MET` / `NOT_MET` tokens as the only explanation. Use this order:

1. **Problem** — one sentence: what blocked progress.
2. **What's wrong** — concrete gaps (files, facts, decisions), all known blockers in one pass.
3. **Ask** — direct questions only they can answer.
4. **Choices** — valid remediation paths when more than one exists (default suggestion OK).
5. **Example** — copy-paste `./nlc …` or agent prompts (`/planit`, `/verify`) that shorten the loop.

## Procedure

0. If `./nlc` shows **YOUR QUEUE** items, ask: continue that work or start something new? Do not make them re-read the menu.
1. State **outcome** — this is the **goal**, not a feature list.
2. Elicit **policy** — standards, constraints, “must / must not.” Propose ADRs and rules yourself from policy; do not ask the human to name them.
3. Call **knowledge-steward** [`load-knowledge-domain`](../../../agents/knowledge-steward/AGENT.md) — facts are derived from policy, not a third human input. `flag-gap`; new facts via `propose-fact` (human accepts).
4. Record open gaps; loop until bind-ready or stop with numbered blockers. If you cannot infer a binding, **refuse and report the gap** — never ask the human to supply derived artifacts.
5. Hand off to **build & compile** (**`/planit`**) with a short resolution table when they are ready to generate; or route to another menu step (e.g. `nlc new`, pack install) without codegen. When bind-ready, write `.nlc/interview-packet.json` (`outcome`, `goals`, `requirements`, `bind_ready: true`) — UC1; `./nlc verify` refuses generate without it.
6. **Queue (CLI, not hand-edited JSON):** Proposed ADRs land in **Requirements** automatically. While requirements are unfinished, do not advance to build. When ratified and bind-ready: `./nlc maintainer guide handoff-build`. After policy edits: `./nlc maintainer guide policy-change --change kind:id` or `./nlc maintainer guide requirements-dirty`.
7. **Shell (you run this, not the human):** `./nlc maintainer requirements` after ratification; `./nlc` to refresh queue; `./nlc verify-deep` then `./nlc verify`. On [verify](../../../docs/TERMS.md#verify) fail the human uses **`/verify`** (ADR 0020–0021). Judgment gates: [`docs/nlc/HUMAN-JUDGMENT-GATES.md`](../../../docs/nlc/HUMAN-JUDGMENT-GATES.md).
8. **Version class:** before ratifying material policy or scope changes, confirm patch / minor / major with the human when unclear — [`.agents/instructions/change-version-class.md`](../../../.agents/instructions/change-version-class.md).

## Done signals

- [Gate](../../../docs/TERMS.md#gate) table all blocking rows true when bind-before-build was in scope
- [Handoff](../../../docs/TERMS.md#handoff) block lists [goal](../../../docs/TERMS.md#goal) ids / [requirement](../../../docs/TERMS.md#requirement) refs / knowledge-domain facts in scope when applicable
- Human knows the next step in plain language (often “build the next piece” → `/planit`), not “read a doc”
