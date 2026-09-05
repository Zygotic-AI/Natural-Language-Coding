# A-S5

- Requirement: `S5`
- Outcome: **met** | **not met** only

## Statement

Produce ≠ Audit ≠ Ship. An agent may not audit its own output as the final gate.

## Binary criteria

Met iff:
1. Agent noun packages do not grant the same agent both produce and audit authority for the same artifact
2. No agent noun is documented as both producer and final auditor of its output
3. Verb lists show clear separation of produce, audit, and ship functions

Not met if any agent noun can both produce and self-audit as final gate, or if an audit role has ship authority.

## Evidence

On met or not met, cite `agents/<name>/AGENT.md` shipping authority section and verb list exclusions. Trace produce → audit → ship path.
