# A-S2

- Requirement: `S2`
- Outcome: **met** | **not met** only

## Statement

Every verb on an agent noun has an input contract, output contract, and failure mode — just like noun-verbs in code (R10).

## Binary criteria

Met iff every verb in every agent noun's `verbs.md` (or equivalent) declares:
1. Input contract (schema or structured definition)
2. Output contract (schema or structured definition)
3. Failure mode (how errors are returned)

Not met if any verb is missing any of the three elements.

## Evidence

On met or not met, cite `agents/<name>/verbs.md` and the verb name. List each verb checked.
