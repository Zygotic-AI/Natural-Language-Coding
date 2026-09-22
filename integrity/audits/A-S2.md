# A-S2

- [Requirement](../../docs/TERMS.md#requirement): `S2`
- Outcome: **[met](../../docs/TERMS.md#met)** | **not [met](../../docs/TERMS.md#met)** only

## Statement

Every verb on an [agent noun](../../docs/TERMS.md#agent-noun) has an input [contract](../../docs/TERMS.md#contract), output [contract](../../docs/TERMS.md#contract), and failure mode — just like noun-verbs in code (R10).

## Binary criteria

[Met](../../docs/TERMS.md#met) iff every verb in every [agent noun](../../docs/TERMS.md#agent-noun)'s `verbs.md` (or equivalent) declares:
1. Input [contract](../../docs/TERMS.md#contract) (schema or structured definition)
2. Output [contract](../../docs/TERMS.md#contract) (schema or structured definition)
3. Failure mode (how errors are returned)

Not [met](../../docs/TERMS.md#met) if any verb is missing any of the three elements.

## Evidence

On [met](../../docs/TERMS.md#met) or not [met](../../docs/TERMS.md#met), cite `agents/<name>/verbs.md` and the verb name. List each verb checked.
