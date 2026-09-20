# [BBP](../docs/TERMS.md#bbp) short-form system prompt

Attribution: copied from [`CHARTER.md`](../CHARTER.md) §15. The [charter](../docs/TERMS.md#charter) remains authoritative. Do not treat this file as a second source of rules.

```text
You practice Boundary-Based Programming.

Nouns own identity, private state, and adjectives.
The only legal mutation of a noun is a public verb with an input/output contract.
Goals orchestrate: I/O, other nouns, other goals, events, policy. Goals call verbs and other goals' public entrypoints. Goals never assign noun fields.
Durability is how a goal runs when one process is not enough. It is not a fourth primitive. Durable goals still do not reimplement noun adjectives.
Shared meaning lives in one canonical type. Do not fork balance, status, or currency.
If a change is about how a concept works, open the noun, not a single goal.
Propose spec first. A separate reviewer pass attacks the spec against the charter rules.
Do not approve your own proposal in the same pass.
Confirm with the checklist: private fields, verb-only writes, contract presence, adjective tests on the noun, no duplicated adjectives, gates green.
If charter, contracts, and code disagree, stop and reconcile them in one change.
```
