# [ADR](../docs/TERMS.md#adr) 0008 — Nouns do not inherit nouns

- Status: Accepted
- Date: 2026-09-16
- Deciders: Human manager
- Class: F (charter extension)

## Context

Inheritance is how adjectives leave home. A child overrides `status`, the parent still thinks it owns the machine, the [compiler](../docs/TERMS.md#compiler) rewrites Invoice and misses BaseDocument. Context is no longer one [noun](../docs/TERMS.md#noun) plus contracts.

[ACS](../docs/TERMS.md#acs) needs reuse. Reuse of a **[contract](../docs/TERMS.md#contract)** is not reuse of a parent class.

## Decision

**A [noun](../docs/TERMS.md#noun) does not inherit another [noun](../docs/TERMS.md#noun).** No subclass, mixin, or trait that shares [adjective](../docs/TERMS.md#adjective) ownership.

Allowed:

- **Protocol / published [contract](../docs/TERMS.md#contract)** — a [noun](../docs/TERMS.md#noun) *satisfies* `Billable`. No fields inherited.
- **Composition via verbs** — Invoice talks to Money or Party through contracted verbs.
- **Value objects** (Money, Address) — interior data of a [noun](../docs/TERMS.md#noun). No public verbs. Not a peer [noun](../docs/TERMS.md#noun).

Owned nouns (LineItem exists only with Invoice) are still nouns. Mutation goes through the aggregate root’s verbs, not `invoice.lines[0].quantity =`.

## Consequences

- [Charter](../docs/TERMS.md#charter) §4.1. [Compiler](../docs/TERMS.md#compiler) emit that uses class inheritance between nouns is incomplete.
- No **R** id until a bindable [gate](../docs/TERMS.md#gate) exists (R27). v1: reviewers and [PLANIT](../docs/TERMS.md#planit) [plan audit](../docs/TERMS.md#plan-audit) attack inheritance as a finding.

## Rejected

- **Abstract base [noun](../docs/TERMS.md#noun)** — still an ancestor chain.
- **Inherit and “don’t override adjectives”** — unenforceable hope.
