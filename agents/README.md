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
| Adversarial auditor | [`adversarial-auditor/`](adversarial-auditor/) | None |
| Ship role | [`ship-role/`](ship-role/) | Yes — with mandate |

**Produce ≠ Audit ≠ Ship** (§16.3, §16.5): these three agent nouns cover the full pipeline. Standards steward and adversarial auditor produce artifacts and findings; ship-role authorizes release.

Each package contains:

- `AGENT.md` — identity, invariants, handoff-in, completion artifact, success criteria
- `verbs.md` — contracted verbs with input/output/failure mode

See ADR [`0003-systems-extension-agent-nouns.md`](../adrs/0003-systems-extension-agent-nouns.md) for rationale.

## Short-form prompt

[`.agents/bbp-short-form.md`](../.agents/bbp-short-form.md) — attribution copy of charter §15.

## Skills (optional pointers)

Thin Cursor/portable skills under [`.agents/skills/`](../.agents/skills/) point at these role files. They do not duplicate the full text. These instruction files are **not** fail-capable CI binders; do not mark P2/P3 bound because they exist.
