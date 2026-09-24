# [ADR](../docs/TERMS.md#adr) 0025 — Belief: no blame, climb upstream, buck stops here

- Status: Accepted
- Date: 2026-09-22
- Deciders: Human manager
- Class: F (process)
- Corpus: nlc

## Context

[`docs/nlc/compiler/MANIFESTO.md`](../docs/nlc/compiler/MANIFESTO.md) now states the belief layer. Unbound manifesto text is not a [rule](../docs/TERMS.md#rule). [ADR](../docs/TERMS.md#adr) 0024 is the factory spine. This [ADR](../docs/TERMS.md#adr) reduces the belief to if/then so RCA cannot stop at “the agent” or at a local environment tweak.

No new **R** id (R27). Rules live in [`rules/nlc-0025.json`](../rules/nlc-0025.json).

## Decision

1. A [defect](../docs/TERMS.md#defect) names a process that was not suitable. It does not name an agent or a human as the cause.
2. [RCA](../docs/TERMS.md#rca) climbs: the process that allowed the defect, then the process that produced that process, until this repository.
3. This repo is the last stop. A closed RCA that never touches a belief, principle, [ADR](../docs/TERMS.md#adr), [rule](../docs/TERMS.md#rule), or [gate](../docs/TERMS.md#gate) here is incomplete.
4. Patching emit without changing the process that produced it is a new [defect](../docs/TERMS.md#defect).

## Consequences

- Manifesto Belief section is the prose home.
- v1 binder: this ADR + `rules/nlc-0025.json` + [`integrity/schemas/rca-packet.schema.json`](../integrity/schemas/rca-packet.schema.json) + [`tools/validate-rca-packet.py`](../tools/validate-rca-packet.py) (`fitness-adr-0025-rca-packet.py`).
- Related: [ADR 0024](0024-nlc-factory-spine.md).

## Rejected

- Blame the last session.
- Treat a local env fix as root.
- Two manifesto files.
