# Boundary-Based Programming

A working spec for software that humans and agents can change without scattering invariants or widening blast radius.

This document is the charter. Implementation must be confirmable against the rules in [Confirmation checklist](#confirmation-checklist). If a rule cannot be checked, it is not a rule yet — it is a wish.

---

## 1. Purpose

> **TODO (vocabulary):** this charter still says *laws* / *invariants*. Settled term is **adjective** — a descriptor on the noun that no verb may violate. Do not rename mid-document; apply in a dedicated pass after §1–§16 are merged.

The goal is surgical change, from intent.

Humans hold intent: goals, requirements, and ADRs. AI compiles that intent into a system. The code is the object file. Generation is incomplete unless the object file is BBA-shaped — nouns own their descriptors, verbs are the only mutation path, goals only call verbs. Locally green, globally wrong — stopped.

An agent (or a person confirming a change) should be able to answer three questions before touching a boundary:

1. What is the unit of change?
2. What is allowed to mutate state?
3. If I change this, what else must still be true?

Boundary-Based Programming organizes a system around **nouns** that own laws, **verbs** that are the only legal way to change those nouns, and **goals** that orchestrate work across nouns and the outside world. Boundaries are not documentation. They are contracts plus enforcement.

This exists because AI-assisted engineering fails in two opposite ways:

- The agent sees the whole repository and thrashes.
- The agent sees one folder, makes that folder green, and silently breaks a law that lived somewhere else.

We shrink the search space for *use-case* changes without exploding the search space for *concept* changes.

