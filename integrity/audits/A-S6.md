# A-S6

- [Requirement](../../docs/TERMS.md#requirement): `S6`
- Outcome: **[met](../../docs/TERMS.md#met)** | **not [met](../../docs/TERMS.md#met)** only

## Statement

[Audit](../../docs/TERMS.md#audit) roles have no [ship](../../docs/TERMS.md#ship) verbs. Adversarial auditors produce findings; another role decides.

## Binary criteria

[Met](../../docs/TERMS.md#met) iff:
1. Every [agent noun](../../docs/TERMS.md#agent-noun) whose purpose is audit/review has "Shipping authority: None" or equivalent
2. Their verb lists explicitly exclude: ratify, merge, release, approve
3. Verbs.md contains an "Excluded verbs" section listing [ship](../../docs/TERMS.md#ship) verbs that are not allowed

Not [met](../../docs/TERMS.md#met) if any audit-purpose [agent noun](../../docs/TERMS.md#agent-noun) has [ship](../../docs/TERMS.md#ship) verbs or ambiguous authority.

## Evidence

On [met](../../docs/TERMS.md#met) or not [met](../../docs/TERMS.md#met), cite `agents/<name>/AGENT.md` shipping authority and `verbs.md` excluded verbs section. List each audit-role [agent noun](../../docs/TERMS.md#agent-noun) checked.
