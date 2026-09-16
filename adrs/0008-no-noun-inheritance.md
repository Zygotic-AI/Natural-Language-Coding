# ADR 0008 — Nouns do not inherit nouns

- Status: Accepted
- Date: 2026-09-16
- Deciders: Human manager
- Class: F (charter extension)

## Context

Inheritance is how adjectives leave home. A child overrides `status`, the parent still thinks it owns the machine, the compiler rewrites Invoice and misses BaseDocument. Context is no longer one noun plus contracts.

ACS needs reuse. Reuse of a **contract** is not reuse of a parent class.

## Decision

**A noun does not inherit another noun.** No subclass, mixin, or trait that shares adjective ownership.

Allowed:

- **Protocol / published contract** — a noun *satisfies* `Billable`. No fields inherited.
- **Composition via verbs** — Invoice talks to Money or Party through contracted verbs.
- **Value objects** (Money, Address) — interior data of a noun. No public verbs. Not a peer noun.

Owned nouns (LineItem exists only with Invoice) are still nouns. Mutation goes through the aggregate root’s verbs, not `invoice.lines[0].quantity =`.

## Consequences

- Charter §4.1. Compiler emit that uses class inheritance between nouns is incomplete.
- No **R** id until a bindable gate exists (R27). v1: reviewers and PLANIT plan audit attack inheritance as a finding.

## Rejected

- **Abstract base noun** — still an ancestor chain.
- **Inherit and “don’t override adjectives”** — unenforceable hope.
