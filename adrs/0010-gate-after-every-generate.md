# ADR 0010 — Gate immediately after every generate

- Status: Accepted
- Date: 2026-09-16
- Deciders: Human manager
- Class: F (process)

## Context

PLANIT 7 prove at the *end* lets a bad statement become input to the next. Defects get cheaper the earlier they die. Generated skills, prompts, and code are the same: if it was emitted, it is gated before anything downstream may use it.

AWL already says default-closed. This ADR makes **per-artifact** generate→gate mandatory, including work PLANIT creates (skills, docs, code).

## Decision

**Never generate without metrics. Never pass generated output downstream before its gate PASS.**

1. **Before generate:** the plan names, for that artifact, the measurable criteria (fitness command, charter rows, skill Gate table, stop predicate). No metrics → do not generate.
2. **Generate** one statement / one artifact (one boundary, or one skill file).
3. **Immediately** run that artifact’s gate. Default-closed. Default fail. Exit non-zero or missing evidence = FAIL.
4. **FAIL** → stop (jidoka). RCA to interview or bind. Do not start the next statement. Humans do not patch the emit to silence the gate.
5. **PASS** → only then the next statement, or PLANIT 7 whole-change prove, or ship.

This applies to:

- BBP-shaped code PLANIT emits
- Skills, prompts, and docs PLANIT emits
- Any later tool or skill PLANIT is used to create — they inherit this rule; they do not get a ceremony exemption

PLANIT 7 remains the **change-level** prove. It does not replace per-artifact gates. Ship remains `release-audit.py` after a human sign.

## Consequences

- [`docs/ai-compiled-systems/PROCESS.md`](../docs/ai-compiled-systems/PROCESS.md) step 6.5.
- PLANIT skill: after each generate step, that artifact’s gate before the next row.
- No new **R** id until a binder can see “metrics existed + gate ran” in the record (R27).

## Rejected

- **Batch generate, prove once at the end** — defects travel.
- **Metrics invented after the file exists** — that is grading hope.
- **Soft-fail / warn and continue** — not a gate.
