# A-S6

- Requirement: `S6`
- Outcome: **met** | **not met** only

## Statement

Audit roles have no ship verbs. Adversarial auditors produce findings; another role decides.

## Binary criteria

Met iff:
1. Every agent noun whose purpose is audit/review has "Shipping authority: None" or equivalent
2. Their verb lists explicitly exclude: ratify, merge, release, approve
3. Verbs.md contains an "Excluded verbs" section listing ship verbs that are not allowed

Not met if any audit-purpose agent noun has ship verbs or ambiguous authority.

## Evidence

On met or not met, cite `agents/<name>/AGENT.md` shipping authority and `verbs.md` excluded verbs section. List each audit-role agent noun checked.
