---
name: interview
description: NLC interview — bind goals, requirements, and knowledge domains before compile. Use as /interview before /planit.
disable-model-invocation: true
---

# Interview (UC1)

Outcome-only intake. This is **PLANIT step 1** and AWL Phase 0–1 compressed for consumers. Do not generate noun or goal code in this skill.

SSOT: [`docs/ai-compiled-systems/PROCESS.md`](../../../docs/ai-compiled-systems/PROCESS.md) § Interview; [`INTENT-SURFACE.md`](../../../docs/ai-compiled-systems/INTENT-SURFACE.md). Pattern catalog: [`INTERVIEW-PATTERNS.md`](../../../docs/ai-compiled-systems/INTERVIEW-PATTERNS.md).

## Gate (default-closed)

| Criterion | Blocking? | Pass when |
| --------- | --------- | --------- |
| Outcome one-line | yes | Problem, user, success shape stated |
| Goals named | yes | At least one goal or explicit “no new goals” with reason |
| Requirements / constraints | yes | Stated or `Waived:` with reason |
| Knowledge domains | yes | `knowledge-steward` `load-knowledge-domain` / `flag-gap`; gaps closed or `Assumption:` |
| Emit forbidden | yes | No PLANIT generate, no durable code writes |

## Procedure

1. State **outcome**, not feature list.
2. Name **goals** and **requirements** (standards/policies are requirements until ADR adoption).
3. Call **knowledge-steward** [`load-knowledge-domain`](../../../agents/knowledge-steward/AGENT.md) (`tools/load-knowledge-domain.py` or `nlc-before-generate.py` before generate) / `flag-gap`; new facts via `propose-fact` (human accepts).
4. Record open gaps; loop questions until bind-ready or stop with numbered blockers.
5. Hand off to **`/planit`** with a short resolution table (goals, requirements, knowledge domains, assumptions).

## Done signals

- Gate table all blocking rows true
- Handoff block lists goal ids / requirement refs / knowledge-domain facts in scope
- User knows next step is `/planit`, not ship
