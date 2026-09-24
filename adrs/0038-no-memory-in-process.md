# ADR 0038 — No memory in process (humans and agents)

- Status: Accepted
- Date: 2026-09-23
- Deciders: Human manager
- Class: F (process)
- Corpus: nlc

## Context

Instructions that tell a human or an agent to “remember” a rule, order, or ritual outsource correctness to volatile memory. That is not [zero-variance](0001-zero-variance-integrity.md) and it fails under [ADR 0025](0025-belief-no-blame-climb.md): the defect is in the process that allowed reliance on memory, not in the operator.

Example: hub release allowed `./release finish` to push a `v*.*.*` [tag](../docs/TERMS.md#tag) without machine proof that the full release ritual ran on that commit—operators were expected to “know” not to use finish alone.

## Decision

1. **Memory is not a process step.** Humans and agents may not be required to retain state, ordering, or tribal rules that are not recorded in durable artifacts or enforced by runnable [gates](../docs/TERMS.md#gate).

2. **If you write “remember” (or equivalent: “don’t forget”, “always”, “never unless”) in SSOT, skills, or operator docs**, you must either:
   - encode the rule in a **machine gate** (tool, script, schema, CI) in the same change, or
   - open a **TODO** item that names the encoding work and blocks claiming the surrounding program complete until the gate exists.

3. **Agent-facing prose** in this repo follows the same rule: handoffs describe what tools do and what files prove PASS—not what the reader must keep in mind.

## Consequences

- [`TODO`](../TODO) gains a standing row for release tag-gate remediation (see Process ADRs 0038–0040 section).
- v1 binder: [`tools/fitness-adr-0038-no-memory.py`](../tools/fitness-adr-0038-no-memory.py) + [`rules/nlc-0038.json`](../rules/nlc-0038.json).
- Related: [ADR 0013](0013-requirements-preflight.md), [ADR 0018](0018-human-cli-interview-on-gap.md), [ADR 0036](0036-inference-only-human-surface.md).

## Rejected

- Training and culture as the primary enforcement for release or safety ordering.
- “Document it in README” without a refusing tool when the rule is violated.
