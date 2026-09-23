# Rule vocabulary (E2 / ADR 0024)

Landed here so TERMS can absorb the same text.

**Rule** — adopted if/then: **condition** (`if`) + **obligation** (`then`) + **gate**. May close over tags, primitives, and facts (ADR 0007). Each rule belongs to one **corpus** (`nlc` | `bba`).

**Condition** — the `if`. When the rule applies.

**Obligation** — the `then`. What must be true when the condition holds.

**Corpus** — `nlc` = factory process. `bba` = emit shape. SSOT map: [`integrity/rule-corpus.json`](../../integrity/rule-corpus.json). Not a second ADR list.

**BBA** — emit shape of compiled systems (noun / verb / adjective / goal). Not NLC process law.
