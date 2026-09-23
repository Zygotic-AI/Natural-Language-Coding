# Atomic verb set

The BBA emit process assigns every mutation to an **atomic verb**. Compound verbs are sequences of atomic verbs, each gated.

## Baseline (hub-shipped)

| Verb | Meaning | Typical primitives |
| ---- | ------- | ----------------- |
| `create` | Bring a noun instance into existence | allocate, construct |
| `read` | Observe state without mutation | fetch, load, get |
| `write` | Replace or set state | store, set, put |
| `update` | Mutate part of existing state | patch, modify |
| `delete` | Remove a noun instance | remove, destroy |
| `validate` | Check a noun or datum against rules | check, verify, assert |
| `emit` | Produce an artifact from intent | generate, compile, render |
| `bind` | Attach a rule, ADR, or contract to an action | link, attach, map |

Eight verbs. That is the entire legal set for a greenfield system.

## Repo-level ownership

The set is **defined at the adopter repo**, not inside the hub:

- Baseline lives with the hub and is pinned by the lock file (ADR 0015).
- The adopter's extension file (e.g. `.nlc/verbs.json`) adds verbs the domain requires.
- Every added verb requires an ADR (or accepted rule) explaining why no compound of existing verbs suffices.
- The contribution gate warns: *extending the verb set is a footgun — each added verb widens the surface the policy overlay and audit must cover.*

## Compound verbs

A compound verb is a **named sequence**, not a new primitive:

```text
process_order =
  validate(order)
  → bind(order, pricing_rule)
  → write(order, status=paid)
  → emit(receipt)
```

Each step has its own gate; the compound has an outer gate. The overlay matches on the **atomic** steps, never on the compound name — that is what makes `if datum=card_number and verb=write then encrypt` work regardless of which compound called `write`.

## Why small

- Composition is where contracts live.
- The policy overlay keys on atomic verbs; a large set fragments matching.
- Audit and RCA climb to atomic steps, not compound names.
