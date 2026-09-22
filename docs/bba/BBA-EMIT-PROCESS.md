# BBA emit process

**Status:** draft, in review with Richard
**Corpus:** `bba` (shape of what the factory emits) — not NLC process law
**Depends on:** ADR 0024 spine, ADR 0026 (X1–X3 runners), ADR 0027 (prose→emit)

## The fractal principle

Every step that produces an artifact is itself an emit. Therefore every step gets the full spine:

- **artifact** — the thing this step produces
- **manifest** — full schema, optional fields present as `na`, decision trace + thought anchors
- **audit** — the step's own audit, non-pending
- **counterpoint gate** — default-closed, specific to what this step produced, run immediately
- **bound ADRs** — selected at plan time, reverse-audited, never chosen by the emit

The BBA emit process is not one pipeline with gates at the end. It is a **chain of mini-pipelines**, each producing a manifest the next step consumes.

## The three roles

| Role | What it is | Where it lives |
|---|---|---|
| **Noun** | an entity the system must know about | vocabulary SSOT |
| **Adjective** | a qualifier on a noun; never stands alone | declared with its noun, read as a data-type tag |
| **Verb** | one atomic operation, one contract | closed atomic verb set |

Adjectives are the bridge between a noun's identity and the rules that constrain it. A policy rule matches on an adjective (e.g. `card_number`) attached to a datum noun — never on the noun alone.

## Step sequence

1. **Noun inventory** — derive every entity the goal tree requires; match each against the vocabulary SSOT; reuse existing nouns, declare missing ones. *Gate:* every noun has an SSOT entry, no duplicates.
2. **Adjective attachment** — attach each noun's qualifier set. *Gate:* every adjective is declared in the vocabulary; no orphan adjectives.
3. **Verb assignment** — assign atomic verbs from the closed set (`create`, `write`, `read`, `update`, `delete`, `validate`, …). No compound verbs. *Gate:* every verb is in the set; composition is sequencing, not invention.
4. **Data-type tagging** — tag every datum a policy might match, reading adjectives as tags. *Gate:* no untagged datum that an applicable policy rule would have matched.
5. **Policy overlay** — evaluate conditional rules over (tagged datum × atomic verb). Example: if datum tagged `card_number` and verb is `write`, obligation `encrypt_at_rest` fires. *Gate:* every applicable rule fired; no silent skip.
6. **Code generation** — emit the BBA-shaped artifact (nouns, verbs, contracts, no inheritance) from the resolved graph, plus its manifest.

Each step's counterpoint gate is **specific**, not generic: the noun gate checks SSOT membership, the verb gate checks the atomic set, the tagging gate checks policy-match coverage, the overlay gate checks rule firing. None of them are "did it work" checks.

## Why the overlay runs before generation

Catching a missing encryption step at emit time is cheap. Catching it in production is not. The policy overlay is the last gate before code exists, so it is the last chance to refuse.

## Open questions

- Exact closed atomic verb set (starter list above is illustrative).
- Whether adjective declarations live in the same SSOT file as nouns or a sibling.
- How policy rules are versioned relative to the vocabulary they match against.

---
_Ara · 2026-09-22_
