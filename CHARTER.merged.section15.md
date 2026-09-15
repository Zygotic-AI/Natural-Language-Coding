# CHARTER.merged.md — Section 15

> TODO (vocabulary): charter still says *laws* / *invariants*. Settled term is **adjective**. Whole-document rename pending; not applied here.
> TODO (vocabulary): *binder* → **gate**. Pending.
> TODO (open question): workflow listed as a peer of noun/verb/goal. ACS says workflow is a goal-of-goals. Confirm before §4 / §5.5.

## 15. Short form for an agent system prompt

You may paste this block into an agent. The rest of this file remains authoritative.

```text
You practice Boundary-Based Programming.

Nouns own identity, private state, and adjectives.
The only legal mutation of a noun is a public verb with an input/output contract.
Goals orchestrate: I/O, other nouns, events, policy. Goals call verbs. Goals never assign noun fields.
Workflows compose goals. They do not reimplement noun adjectives.
Shared meaning lives in one canonical type. Do not fork balance, status, or currency.
If a change is about how a concept works, open the noun, not a single goal.
Propose spec first. A separate reviewer pass attacks the spec against the charter rules.
Do not approve your own proposal in the same pass.
Confirm with the checklist: private fields, verb-only writes, contract presence, adjective tests on the noun, no duplicated adjectives, gates green.
If charter, contracts, and code disagree, stop and reconcile them in one change.
```

---

## How §15 works in the merge

The short-form block is the one artifact an agent reads first. It now uses **adjective** instead of invariant/law, and **gate** instead of fitness check. The block tells the agent: nouns own adjectives, verbs are the only mutation path, goals call verbs and never re-decide adjectives, and confirmation is gate-backed, not vibe-backed.

The three TODOs above are carried forward from earlier sections. None block this section.
