# [ADR](../docs/TERMS.md#adr) 0009 — Primitives are interior functions, not verbs

- Status: Accepted
- Date: 2026-09-16
- Deciders: Human manager
- Class: F (charter extension)

## Context

[ADR](../docs/TERMS.md#adr) 0007 reduced ADRs to if-thens over tags, primitives, and facts. Verbs were to *declare* primitives. Declaration without a call tree is hope: the body does `open()` and the verb forgets to say `write`.

The inventory the [compiler](../docs/TERMS.md#compiler) can actually walk is **named interior functions**.

## Decision

1. The closed set lives in [`integrity/primitives.md`](../integrity/primitives.md). Those strings **are** the interior function names (`write`, `read`, `return`, …).
2. [Primitive](../docs/TERMS.md#primitive) functions are **not** public verbs. They are not on the [noun](../docs/TERMS.md#noun)’s contracted verb list. Reserved names.
3. A public verb (e.g. `update_customer`) performs [primitive](../docs/TERMS.md#primitive) work only by **calling** those functions. Raw I/O, `db.save`, `open`, SQL, or retain-in-a-field outside a [primitive](../docs/TERMS.md#primitive) function is a [defect](../docs/TERMS.md#defect) (same family as R33).
4. Each [primitive](../docs/TERMS.md#primitive) function is bound to the if-then rules that apply when that [primitive](../docs/TERMS.md#primitive) runs on tagged data (`pan ∧ write → encrypt`).
5. **Call-tree inventory:** from a verb, the tree of calls below it *is* the [primitive](../docs/TERMS.md#primitive) set for that verb. Extra [primitive](../docs/TERMS.md#primitive) in the tree vs bind list → fail. Missing declared [primitive](../docs/TERMS.md#primitive) → fail. That is the [audit](../docs/TERMS.md#audit) point. Do not trust a comment.

Rules still compile: the `write` function (or the gate on it) applies encrypt; the prompt does not “remember” PCI.

## Consequences

- [Charter](../docs/TERMS.md#charter) §4.2 / §4.7. [PLANIT](../docs/TERMS.md#planit) bind may point at [primitive](../docs/TERMS.md#primitive) names on a statement.
- Language adapters later map `write(` / `self.write(` to this set ([`docs/LANGUAGE-SCANNER.md`](../docs/LANGUAGE-SCANNER.md)). No **R** id until that [gate](../docs/TERMS.md#gate) exists.
- v1 Python: reviewers treat a verb body that writes without calling `write` as a finding.

## Rejected

- **Declare primitives only on the verb, no functions** — inventory is a story.
- **Public verb named `write`** — collides with the reserved set.
- **Helpers that wrap `open()` under another name** — laundering. The leaf call must be the [primitive](../docs/TERMS.md#primitive) name.
