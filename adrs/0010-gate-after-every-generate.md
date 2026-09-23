# [ADR](../docs/TERMS.md#adr) 0010 — [Gate](../docs/TERMS.md#gate) immediately after every generate

- Status: Accepted
- Date: 2026-09-16
- Deciders: Human manager
- Class: F (process)

## Context

[PLANIT](../docs/TERMS.md#planit) 7 [prove](../docs/TERMS.md#prove) at the *end* lets a bad statement become input to the next. Defects get cheaper the earlier they die. Generated skills, prompts, and code are the same: if it was emitted, it is gated before anything downstream may use it.

[AWL](../docs/TERMS.md#awl) already says [default-closed](../docs/TERMS.md#default-closed). This [ADR](../docs/TERMS.md#adr) makes **per-artifact** generate→[gate](../docs/TERMS.md#gate) mandatory, including work [PLANIT](../docs/TERMS.md#planit) creates (skills, docs, code).

## Decision

**Never generate without metrics. Never pass generated output downstream before its [gate](../docs/TERMS.md#gate) PASS.**

1. **Before generate:** the plan names, for that artifact, the measurable criteria (fitness command, charter rows, skill Gate table, stop predicate). No metrics → do not generate.
2. **Generate** one statement / one artifact (one boundary, or one skill file).
3. **Immediately** run that artifact’s [gate](../docs/TERMS.md#gate). [Default-closed](../docs/TERMS.md#default-closed). Default fail. Exit non-zero or missing evidence = FAIL.
4. **FAIL** → stop (jidoka). [RCA](../docs/TERMS.md#rca) to [interview](../docs/TERMS.md#interview) or bind. Do not start the next statement. Humans do not patch the emit to silence the [gate](../docs/TERMS.md#gate).
5. **PASS** → only then the next statement, or [PLANIT](../docs/TERMS.md#planit) 7 whole-change [prove](../docs/TERMS.md#prove), or [ship](../docs/TERMS.md#ship).

This applies to:

- BBP-shaped code [PLANIT](../docs/TERMS.md#planit) emits
- Skills, prompts, and docs [PLANIT](../docs/TERMS.md#planit) emits
- Any later tool or skill [PLANIT](../docs/TERMS.md#planit) is used to create — they inherit this [rule](../docs/TERMS.md#rule); they do not get a ceremony exemption

[PLANIT](../docs/TERMS.md#planit) 7 remains the **change-level** [prove](../docs/TERMS.md#prove). It does not replace per-artifact gates. [Ship](../docs/TERMS.md#ship) remains `release-audit.py` after a human sign.

## Consequences

- [`docs/nlc/compiler/PROCESS.md`](../docs/nlc/compiler/PROCESS.md) step 6.5.
- [PLANIT](../docs/TERMS.md#planit) skill: after each generate step, that artifact’s [gate](../docs/TERMS.md#gate) before the next row.
- No new **R** id until a binder can see “metrics existed + [gate](../docs/TERMS.md#gate) ran” in the record (R27).

## Rejected

- **Batch generate, [prove](../docs/TERMS.md#prove) once at the end** — defects travel.
- **Metrics invented after the file exists** — that is grading hope.
- **Soft-fail / warn and continue** — not a [gate](../docs/TERMS.md#gate).
