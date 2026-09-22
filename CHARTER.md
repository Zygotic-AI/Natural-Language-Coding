# [Boundary-Based Programming](docs/TERMS.md#bbp)

A working spec for software that humans and agents can change without scattering adjectives or widening [blast radius](docs/TERMS.md#blast-radius).

This document is the [charter](docs/TERMS.md#charter). Implementation must be confirmable against the rules in [Confirmation checklist](#confirmation-checklist). If a [rule](docs/TERMS.md#rule) cannot be checked, it is not a [rule](docs/TERMS.md#rule) yet — it is a wish.

---

## 1. Purpose

The [goal](docs/TERMS.md#goal) is surgical change.

An agent (or a person) should be able to answer three questions before touching code:

1. What is the unit of change?
2. What is allowed to mutate state?
3. If I change this, what else must still be true?

[Boundary-Based Programming](docs/TERMS.md#bbp) organizes a system around **nouns** that own adjectives, **verbs** that are the only legal way to change those nouns, and **goals** that orchestrate work across nouns and the outside world. Boundaries are not documentation. They are contracts plus enforcement.

This exists because AI-assisted engineering fails in two opposite ways:

- The agent sees the whole repository and thrashes.
- The agent sees one folder, makes that folder green, and silently breaks an [adjective](docs/TERMS.md#adjective) that lived somewhere else.

We shrink the search space for *use-case* changes without exploding the search space for *concept* changes.

---

## 2. Why this shape

Layered architecture groups code by technical concern. Agents then hunt across controllers, services, and repositories to change one business outcome.

Goal-only architecture groups code by verb. That helps a single use-case edit. It hurts when the [adjective](docs/TERMS.md#adjective) is a [noun](docs/TERMS.md#noun): invoice status, money rounding, eligibility. Those adjectives get copied into every verb folder. Each copy looks correct. The system becomes several slightly different truths.

Object-only architecture concentrates the adjectives and hides the use-case. Agents cannot find “the work to do.” [Blast radius](docs/TERMS.md#blast-radius) becomes “the Invoice class.”

The combined shape:

- **[Noun](docs/TERMS.md#noun)** = identity, state, adjectives. The retrieval key for “how does an invoice work?”
- **Verb on the [noun](docs/TERMS.md#noun)** = a contracted mutation. The only way state changes.
- **[Goal](docs/TERMS.md#goal)** = a use-case that reaches the edge: I/O, other nouns, other goals, events, policy. It calls verbs and other goals' public entrypoints. It does not write fields.
- **[Durability](docs/TERMS.md#durability)** = a runtime property of a [goal](docs/TERMS.md#goal), not a fourth design [primitive](docs/TERMS.md#primitive). If the [goal](docs/TERMS.md#goal) must wait, retry, compensate, or take a human decision, it runs on a durable engine (Temporal or equivalent). That engine is not a peer of [noun](docs/TERMS.md#noun) / verb / [goal](docs/TERMS.md#goal).

That is the whole model. Everything else is how we keep it honest.

---

## 3. Naming

**Practice name:** [Boundary-Based Programming](docs/TERMS.md#bbp).

**Mechanism:** boundaries are enforced (contracts, privacy of fields, gates, review).

Do not name the practice “governance” or “governed.” Those words imply a committee ruling subjects. The artifacts that hold decisions are a **[charter](docs/TERMS.md#charter)** (this document, plus ADRs). The property we protect is **[integrity](docs/TERMS.md#integrity)**. The act that keeps agents honest is **adversarial review against the [charter](docs/TERMS.md#charter)**.

Useful substitutes if a slot in an older diagram said “Governance Architecture”:

| Avoid | Use |
|---|---|
| Governance | [Charter](docs/TERMS.md#charter), [integrity](docs/TERMS.md#integrity), covenant, protocol |
| Governed system | Bounded system, charter-bound system |
| Governance review | Adversarial review, [integrity](docs/TERMS.md#integrity) check |

**Boundary-Enforced Programming** is a true claim about the pipeline. It is a poor name for the practice. Put enforcement in the rules and the CI [gate](docs/TERMS.md#gate), not in the title.

### Id prefixes

These letters on [requirement](docs/TERMS.md#requirement) ids are not interchangeable.

| Prefix | Stands for | What it is |
|--------|------------|------------|
| **P** | Principle | How *this practice [hub](docs/TERMS.md#hub)* stays honest (P1–P7 in `integrity/PRINCIPLES.md`). |
| **R** | [Requirement](docs/TERMS.md#requirement) | A [charter](docs/TERMS.md#charter) design [rule](docs/TERMS.md#rule) the emit must obey (R1–R31). |
| **C** | Confirmation | A per-change checklist item the [confirmer](docs/TERMS.md#confirmer) scores PASS/FAIL/N/A (C1–C24). |
| **S** / **CS** | Systems / confirmation-systems | Agent-noun package structure (identity, verbs, handoff). |
| **Q** | [Quality](docs/TERMS.md#quality) | Ops/opportunities metric at a [boundary](docs/TERMS.md#boundary). |

`P-016`, `P-020` and other hyphenated **[P-0xx](docs/TERMS.md#p-0xx)** ids are *operating policies* in the companion bindings repo. They are not P1–P7.

An **R** can stand without a matching **C**. A **C** usually restates an **R** as something you can tick on *this* change.

Corpus tags for every published **R** / **C** / **P** id live in [`integrity/rule-corpus.json`](integrity/rule-corpus.json) ([ADR 0024](adrs/0024-nlc-factory-spine.md)): `bba` = emit shape, `nlc` = factory process.

---

## 4. Core model
