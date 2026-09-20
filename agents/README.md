# Agents

How [Boundary-Based Programming](../docs/TERMS.md#bbp) is applied in agentic programming. [Charter](../docs/TERMS.md#charter) §§6–7, §15, and §16 are authoritative for the loop, short-form prompt, and systems model.

## Role packs (agent loop)

Roles for the agent execution loop (§6–7). One model may play them in sequence, but not in the same pass as both author and skeptic of its own work.

| Role | File | [Gate](../docs/TERMS.md#gate) |
|------|------|------|
| Proposer | [`proposer.md`](proposer.md) | `G-PROPOSE` |
| Reviewer | [`reviewer.md`](reviewer.md) | `G-REVIEW` |
| [Confirmer](../docs/TERMS.md#confirmer) | [`confirmer.md`](confirmer.md) | `G-CONFIRM` |
| Recorder | [`recorder.md`](recorder.md) | `G-RECORD` |

## [Agent nouns](../docs/TERMS.md#agent-noun) (systems model)

Durable organizational positions with identity, adjectives, and contracted verbs (§16). [Agent nouns](../docs/TERMS.md#agent-noun) are not loop roles — they are persistent capabilities with [boundary](../docs/TERMS.md#boundary) artifacts.

| [Agent noun](../docs/TERMS.md#agent-noun) | Package | Shipping authority |
|------------|---------|-------------------|
| Standards steward | [`standards-steward/`](standards-steward/) | None |
| [Quality](../docs/TERMS.md#quality) architect | [`quality-architect/`](quality-architect/) | None |
| Adversarial auditor | [`adversarial-auditor/`](adversarial-auditor/) | None |
| Knowledge steward | [`knowledge-steward/`](knowledge-steward/) | None |
| [Ship](../docs/TERMS.md#ship) role | [`ship-role/`](ship-role/) | Yes — with mandate |


**[Produce ≠ Audit ≠ Ship](../docs/TERMS.md#produce-audit-ship)** (§16.3, §16.5). Knowledge steward holds knowledge-domain facts for interview/bind, not a fourth pipeline phase.


Each package contains:

- `AGENT.md` — identity, adjectives, handoff-in, completion artifact, success criteria
- `verbs.md` — contracted verbs with input/output/failure mode
- `schemas/` (optional) — machine-readable JSON Schema for verb contracts

See [ADR](../docs/TERMS.md#adr) [`0003-systems-extension-agent-nouns.md`](../adrs/0003-systems-extension-agent-nouns.md) for rationale.

### Validation

Use [`tools/validate-agent-noun-packages.py`](../tools/validate-agent-noun-packages.py) to validate package completeness:

```bash
python3 tools/validate-agent-noun-packages.py
```

The validator checks:
- `AGENT.md` contains required sections (Identity, Adjectives, Handoff-in, Completion artifact, Success criteria)
- `verbs.md` declares Input [contract](../docs/TERMS.md#contract), Output [contract](../docs/TERMS.md#contract), and Failure mode for every verb (per S2 / R31)

See [`tools/README.md`](../tools/README.md#agent-noun-package-validation) for full documentation.

## Ship-role handoff-in

[Ship](../docs/TERMS.md#ship) authority (ratify, merge, release) belongs to a human or designated ship-role. Before [ship](../docs/TERMS.md#ship):

| Condition | Evidence |
|-----------|----------|
| Fitness `MET` | Fitness `score-fitness` returned `MET` |
| No open `handoff_refused` | All preflight refusals resolved; no produce-incomplete artifacts pending |
| Adversarial [audit](../docs/TERMS.md#audit) clean or rebutted | Findings addressed; no unresolved blockers |

Ship-role does not receive work with open `handoff_refused` status. The producer fixes and resubmits.

## Vocabulary

| Term | Meaning | Use |
|------|---------|-----|
| `handoff_refused` | [Produce package](../docs/TERMS.md#produce-package) missing/incomplete; preflight did not pass | Fitness preflight output; NOT a FAIL |
| `MET` | Fitness criteria satisfied | Fitness score output |
| `FAIL` | Fitness criteria not satisfied (content defect) | Fitness score output |
| `Gate` | CI enforcement point for fitness scoring | [Charter](../docs/TERMS.md#charter) §12; downstream of preflight |
| `re-gate` | **Forbidden.** Do not use for missing-package rework | Masks produce-handoff [defect](../docs/TERMS.md#defect) |

## Short-form prompt

[`.agents/bbp-short-form.md`](../.agents/bbp-short-form.md) — attribution copy of [charter](../docs/TERMS.md#charter) §15.

## Skills (optional pointers)

Thin Cursor/portable skills under [`.agents/skills/`](../.agents/skills/) point at these role files. They do not duplicate the full text. These instruction files are **not** fail-capable CI gates; do not mark P2/P3 bound because they exist.
