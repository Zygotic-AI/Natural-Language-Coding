# Boundary-Based Programming

A working spec for software that humans and agents can change without scattering adjectives or widening blast radius.

This document is the charter. Implementation must be confirmable against the rules in [Confirmation checklist](#confirmation-checklist). If a rule cannot be checked, it is not a rule yet — it is a wish.

---

## 1. Purpose

The goal is surgical change.

An agent (or a person) should be able to answer three questions before touching code:

1. What is the unit of change?
2. What is allowed to mutate state?
3. If I change this, what else must still be true?

Boundary-Based Programming organizes a system around **nouns** that own adjectives, **verbs** that are the only legal way to change those nouns, and **goals** that orchestrate work across nouns and the outside world. Boundaries are not documentation. They are contracts plus enforcement.

This exists because AI-assisted engineering fails in two opposite ways:

- The agent sees the whole repository and thrashes.
- The agent sees one folder, makes that folder green, and silently breaks an adjective that lived somewhere else.

We shrink the search space for *use-case* changes without exploding the search space for *concept* changes.

---

## 2. Why this shape

Layered architecture groups code by technical concern. Agents then hunt across controllers, services, and repositories to change one business outcome.

Goal-only architecture groups code by verb. That helps a single use-case edit. It hurts when the adjective is a noun: invoice status, money rounding, eligibility. Those adjectives get copied into every verb folder. Each copy looks correct. The system becomes several slightly different truths.

Object-only architecture concentrates the adjectives and hides the use-case. Agents cannot find “the work to do.” Blast radius becomes “the Invoice class.”

The combined shape:

- **Noun** = identity, state, adjectives. The retrieval key for “how does an invoice work?”
- **Verb on the noun** = a contracted mutation. The only way state changes.
- **Goal** = a use-case that reaches the edge: I/O, other nouns, other goals, events, policy. It calls verbs and other goals' public entrypoints. It does not write fields.
- **Durability** = a runtime property of a goal, not a fourth design primitive. If the goal must wait, retry, compensate, or take a human decision, it runs on a durable engine (Temporal or equivalent). That engine is not a peer of noun / verb / goal.

That is the whole model. Everything else is how we keep it honest.
