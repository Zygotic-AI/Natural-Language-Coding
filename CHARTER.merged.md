# Boundary-Based Programming

A working spec for software that humans and agents can change without scattering invariants or widening blast radius.

> **Working merge copy.** Source of truth remains [`CHARTER.md`](CHARTER.md). This file is the section-by-section ACS ↔ BBA merge. Not ratified until the merge is complete.

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

---

## 2. Why this shape

> **TODO (workflow):** `CHARTER.md` §2 lists workflow as a fourth piece of “the whole model.” ACS treats workflow as a goal of goals — durable is a property, not a new design citizen. Merged here as composition, not as a fourth kind. Confirm before §4 / §5.5 land.

Layered architecture groups code by technical concern. Agents then hunt across controllers, services, and repositories to change one business outcome.

Goal-only architecture groups code by verb. That helps a single use-case edit. It hurts when the law is a noun: invoice status, money rounding, eligibility. Those laws get copied into every verb folder. Each copy looks correct. The system becomes several slightly different truths. Two fine goals. Two invoices.

Object-only architecture concentrates the laws and hides the use-case. Agents cannot find “the work to do.” Blast radius becomes “the Invoice class.”

The compiler makes that worse if it has no required shape: it will emit whichever of those three is easiest for the current goal. That is why BBA is the instruction set the process may not skip.

Two layers, one architecture:

- **Process** (ACS) — humans hold goals, requirements, ADRs. Interview, bind, generate, audit, RCA.
- **Design** (BBA) — the emitted system is nouns, verbs, and goals. A goal is an outcome *and* a boundary that may only call published verbs.

The combined shape the compiler must emit:

- **Noun** = identity, state, invariants. The retrieval key for “how does an invoice work?”
- **Verb on the noun** = a contracted mutation. The only way state changes.
- **Goal** = a use-case that reaches the edge: I/O, other nouns, events, policy. It calls verbs. It does not write fields.
- **Workflow** = a durable sequence of goals when one in-process call is not enough. Not a fourth design citizen. A goal of goals.

Generation is incomplete unless that shape is present and a binder fails a goal that writes noun fields or re-decides a noun’s descriptor. Two goal boxes are fine if both only call Invoice verbs.

The repo may be huge. The window for write, audit, and graph is one boundary plus the published contracts of its neighbors. If a step needs two objects’ internals at once, the cut is wrong.

That is the whole model. Everything else is how we keep it honest.

---

## 3–16

Unchanged from [`CHARTER.md`](CHARTER.md). This working copy currently merges **§1–§2**. Later sections land here as each merge pass completes. Until then, read §3–§16 in `CHARTER.md`.
