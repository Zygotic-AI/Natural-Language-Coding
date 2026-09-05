# Agents

How Boundary-Based Programming is applied in agentic programming. Charter §§6–7, §15, and §16 are authoritative for the loop, short-form prompt, and systems model.

## Role packs (agent loop)

Roles for the agent execution loop (§6–7). One model may play them in sequence, but not in the same pass as both author and skeptic of its own work.

| Role | File | Gate |
|------|------|------|
| Proposer | [`proposer.md`](proposer.md) | `G-PROPOSE` |
| Reviewer | [`reviewer.md`](reviewer.md) | `G-REVIEW` |
| Confirmer | [`confirmer.md`](confirmer.md) | `G-CONFIRM` |
| Recorder | [`recorder.md`](recorder.md) | `G-RECORD` |

## Agent nouns (systems model)

Durable organizational positions with identity, invariants, and contracted verbs (§16). Agent nouns are not loop roles — they are persistent capabilities with boundary artifacts.

| Agent noun | Package | Shipping authority |
|------------|---------|-------------------|
| Standards steward | [`standards-steward/`](standards-steward/) | None |
| Quality architect | [`quality-architect/`](quality-architect/) | None |
| Adversarial auditor | [`adversarial-auditor/`](adversarial-auditor/) | None |

Each package contains:

- `AGENT.md` — identity, invariants, handoff-in, completion artifact, success criteria
- `verbs.md` — contracted verbs with input/output/failure mode

See ADR [`0003-systems-extension-agent-nouns.md`](../adrs/0003-systems-extension-agent-nouns.md) for rationale.

## Ship-role handoff-in

Ship authority (ratify, merge, release) belongs to a human or designated ship-role. Before ship:

| Condition | Evidence |
|-----------|----------|
| Fitness `MET` | Fitness `score-fitness` returned `MET` |
| No open `handoff_refused` | All preflight refusals resolved; no produce-incomplete artifacts pending |
| Adversarial audit clean or rebutted | Findings addressed; no unresolved blockers |

Ship-role does not receive work with open `handoff_refused` status. The producer fixes and resubmits.

## Vocabulary

| Term | Meaning | Use |
|------|---------|-----|
| `handoff_refused` | Produce package missing/incomplete; preflight did not pass | Fitness preflight output; NOT a FAIL |
| `MET` | Fitness criteria satisfied | Fitness score output |
| `FAIL` | Fitness criteria not satisfied (content defect) | Fitness score output |
| `Gate` | CI enforcement point for fitness scoring | Charter §12; downstream of preflight |
| `re-gate` | **Forbidden.** Do not use for missing-package rework | Masks produce-handoff defect |

## Short-form prompt

[`.agents/bbp-short-form.md`](../.agents/bbp-short-form.md) — attribution copy of charter §15.

## Skills (optional pointers)

Thin Cursor/portable skills under [`.agents/skills/`](../.agents/skills/) point at these role files. They do not duplicate the full text. These instruction files are **not** fail-capable CI binders; do not mark P2/P3 bound because they exist.
