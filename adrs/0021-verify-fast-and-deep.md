# [ADR](../docs/TERMS.md#adr) 0021 — [Verify](../docs/TERMS.md#verify) fast (fingerprints) and [verify-deep](../docs/TERMS.md#verify-deep) (full gates)

- Status: Accepted
- Date: 2026-09-20
- Deciders: Human manager
- Class: F (product UX)

## Context

[ADR](../docs/TERMS.md#adr) 0020 splits human shell from agent workflows. **[Verify](../docs/TERMS.md#verify)** is the exception: CI and release pipelines need a **machine true/false** without inference. `prove` mixed compile gates with the human label “[verify](../docs/TERMS.md#verify).” Re-reading the whole tree on every pipeline run is too slow.

## Decision

1. **Human and CI command:** `./nlc verify` (replaces `./nlc prove` for adopters). Exit **0** = pass, **non-zero** = fail. No inference required on pass.

2. **Fast path (`verify`):** Compare current sha256 fingerprints of intent + compiled paths (`adrs/`, `rules/`, `knowledge/`, `goals/`, `domain/`) to **`.nlc/verified.json`**, plus cheap pipeline blockers (unfinished requirements, open regen queue). Does not run full fitness.

3. **Deep path (`verify-deep`):** Run full compile/fitness gates (hub `ci_fitness.py` or adopter-bound suite when wired), then **rewrite** `.nlc/verified.json`. Use after material changes or when fast [verify](../docs/TERMS.md#verify) reports stale/missing fingerprints.

4. **On failure:** Print plain reasons; instruct **`/verify` in your agent** for fixes. Exit non-zero so CI stops.

5. **`prove`:** Removed from the human CLI. [PLANIT](../docs/TERMS.md#planit) step 7 still means “[verify](../docs/TERMS.md#verify)” internally. `nlc prove` prints removal guidance (hidden from help).

6. **Agent skill `/verify`:** Walks fixes and runs `verify-deep` when fingerprints should be refreshed.

## Consequences

- [`tools/nlc_verify.py`](../tools/nlc_verify.py), schema [`nlc-verified.schema.json`](../integrity/schemas/nlc-verified.schema.json).
- [`.agents/skills/verify/SKILL.md`](../.agents/skills/verify/SKILL.md).
- Menu and queue use `./nlc verify` only.

## Rejected

- Fast [verify](../docs/TERMS.md#verify) re-running full `ci_fitness.py` every time.
- Human-only [verify](../docs/TERMS.md#verify) with no agent path on failure.
