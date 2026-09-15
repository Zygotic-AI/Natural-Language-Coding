# Architecture

AI-Compiled Systems is two layers of one architecture.

```text
Goals + requirements + ADRs     ← humans hold (process)
            ↓
      AI compiler
            ↓
   BBA-shaped system            ← design CHARTER (noun, verb, goal boundary, contract)
            ↓
   Machine gate + audit
            ↓
   Running system
```

If the compiler skips BBA, you get two fine goals and two invoices. Traceability of slop is not the product.

## Two citizen lists (both in force)

**Process citizens** — interviewed, signed, versioned by people:

- Goal
- Requirement
- ADR
- Interview (procedure)
- RCA (procedure)

**Design citizens** — emitted by the compiler, required by the BBA standard:

- Noun
- Verb
- Goal-as-boundary
- Contract
- Gate

Goal sits on both lists. A goal is an outcome the manager asked for *and* a boundary that may only call published verbs.

Not citizens: workflow-as-a-new-type (goal of goals; durable is a property), knowledge-domain-as-a-new-kind (shelf of ADRs + requirements), business-need-as-a-document (optional tag on a goal).

## Compile gate

Generation is incomplete unless:

1. Output is BBA-shaped.
2. Every invoice-shaped fact lives behind one Invoice boundary (noun inside, verbs on the edge).
3. A gate fails a goal that implements that adjective itself or writes noun fields.

Two goal boxes are fine if both only call Invoice verbs.

## Context

The repo may be a monorepo. The window for write, audit, and graph is one atomic object plus the hard contracts of its neighbors. If a step needs two objects’ internals at once, the cut is wrong.

## What is derived

A particular `Invoice` module, verb bodies, goal code, diagrams, most runbooks. Regenerable. Internals behind a stable verb contract may be rewritten without the manager opening the file.

A *breaking* change to a published verb contract is a product event: impact on callers, fix the requirement if the behavior was wrong, regenerate. Do not patch the generated contract to hide a defect.

CHARTER.md remains the design SSOT. This page does not replace it.
