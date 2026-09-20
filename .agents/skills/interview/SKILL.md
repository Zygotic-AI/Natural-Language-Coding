---
name: [interview](../../../docs/TERMS.md#interview)
description: [NLC](../../../docs/TERMS.md#nlc) guided conversation — figure out what the human wants (features, compliance, requirements, which menu path) in plain language; map to patterns internally; hand off to build when ready. Use [/interview](../../../docs/TERMS.md#interview) anytime, not only before first compile.
disable-model-invocation: true
---

# [Interview](../../../docs/TERMS.md#interview) (UC1)

**Human promise (ADR 0017):** the [adopter](../../../docs/TERMS.md#adopter) says what they are trying to accomplish; **you** pick the right [workflow](../../../docs/TERMS.md#workflow) and ask simple questions. Do **not** send them to read `INTERVIEW-PATTERNS.md` or other long docs—load that catalog yourself from [`INTERVIEW-PATTERNS.md`](../../../docs/ai-compiled-systems/INTERVIEW-PATTERNS.md) and match their [goal](../../../docs/TERMS.md#goal) (greenfield vs brownfield, PCI/compliance packs, requirements, stuck on next step, etc.).

Outcome-only intake when the work is bind-before-build. This can be **[PLANIT](../../../docs/TERMS.md#planit) step 1** / [AWL](../../../docs/TERMS.md#awl) Phase 0–1 compressed. Do not generate [noun](../../../docs/TERMS.md#noun) or [goal](../../../docs/TERMS.md#goal) code in this skill.

SSOT: [`docs/ai-compiled-systems/PROCESS.md`](../../../docs/ai-compiled-systems/PROCESS.md) § [Interview](../../../docs/TERMS.md#interview); [`INTENT-SURFACE.md`](../../../docs/ai-compiled-systems/INTENT-SURFACE.md).

## [Gate](../../../docs/TERMS.md#gate) (default-closed)

| Criterion | Blocking? | Pass when |
| --------- | --------- | --------- |
| Outcome one-line | yes | Problem, user, success shape stated |
| Goals named | yes | At least one [goal](../../../docs/TERMS.md#goal) or explicit “no new goals” with reason |
| Requirements / constraints | yes | Stated or `Waived:` with reason |
| [Knowledge domains](../../../docs/TERMS.md#knowledge-domain) | yes | `knowledge-steward` `load-knowledge-domain` / `flag-gap`; gaps closed or `Assumption:` |
| Emit forbidden | yes | No [PLANIT](../../../docs/TERMS.md#planit) generate, no durable code writes |

## Procedure

0. If `./nlc` shows **YOUR QUEUE** items, ask: continue that work or start something new? Do not make them re-read the menu.
1. State **outcome**, not feature list.
2. Name **goals** and **requirements** (standards/policies are requirements until ADR adoption).
3. Call **knowledge-steward** [`load-knowledge-domain`](../../../agents/knowledge-steward/AGENT.md) (`tools/load-knowledge-domain.py` or `nlc-before-generate.py` before generate) / `flag-gap`; new facts via `propose-fact` (human accepts).
4. Record open gaps; loop questions until bind-ready or stop with numbered blockers.
5. Hand off to **build & compile** (**`/planit`**) with a short resolution table when they are ready to generate; or route to another menu step (e.g. `nlc new`, pack install) without codegen.
6. **Queue (CLI, not hand-edited JSON):** Proposed ADRs land in **Requirements** automatically. While requirements are unfinished, do not advance to build. When ratified and bind-ready: `./nlc maintainer guide handoff-build`. After policy edits: `./nlc maintainer guide policy-change --change kind:id` or `./nlc maintainer guide requirements-dirty`.
7. **Shell (you run this, not the human):** `./nlc maintainer requirements` after ratification; `./nlc` to refresh queue; `./nlc verify-deep` then `./nlc verify`. On [verify](../../../docs/TERMS.md#verify) fail the human uses **`/verify`** (ADR 0020–0021). Judgment gates: [`docs/nlc/HUMAN-JUDGMENT-GATES.md`](../../../docs/nlc/HUMAN-JUDGMENT-GATES.md).

## Done signals

- [Gate](../../../docs/TERMS.md#gate) table all blocking rows true when bind-before-build was in scope
- [Handoff](../../../docs/TERMS.md#handoff) block lists [goal](../../../docs/TERMS.md#goal) ids / [requirement](../../../docs/TERMS.md#requirement) refs / knowledge-domain facts in scope when applicable
- Human knows the next step in plain language (often “build the next piece” → `/planit`), not “read a doc”
