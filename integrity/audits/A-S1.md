# A-S1

- Requirement: `S1`
- Outcome: **met** | **not met** only

## Statement

Every agent noun has an identity file that states purpose and invariants.

## Binary criteria

Met iff every agent noun package under `agents/<name>/` contains an `AGENT.md` (or equivalent) that states:
1. Role name
2. Purpose (one line)
3. Invariants (list)

Not met if any agent noun package is missing identity or invariants, or if they are vague/missing binary criteria.

## Evidence

On met or not met, cite `agents/<name>/AGENT.md` and the relevant sections. List each agent noun checked.
