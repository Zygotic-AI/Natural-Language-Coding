# Architecture

[ACS](../../TERMS.md#acs) is two layers of one architecture.

```text
Goals + requirements + ADRs     ← humans hold (PLANIT)
            ↓
      AI compiler
            ↓
   BBP-shaped system            ← CHARTER (noun, verb, adjective, goal, contract)
            ↓
   Machine gate + audit
            ↓
   Running system
```

If the [compiler](../../TERMS.md#compiler) skips [BBP](../../TERMS.md#bbp), you get two fine goals and two invoices. Traceability of slop is not the product.

## Two citizen lists (both in force)

**Process citizens** — interviewed, signed, versioned by people:

- [Goal](../../TERMS.md#goal)
- [Requirement](../../TERMS.md#requirement)
- [ADR](../../TERMS.md#adr)
- [Interview](../../TERMS.md#interview) (procedure)
- [RCA](../../TERMS.md#rca) (procedure)

**Design citizens** — emitted by the [compiler](../../TERMS.md#compiler), required by the [BBP](../../TERMS.md#bbp) standard:

- [Noun](../../TERMS.md#noun)
- Verb
- Goal-as-boundary
- [Contract](../../TERMS.md#contract)
- [Gate](../../TERMS.md#gate)

[Goal](../../TERMS.md#goal) sits on both lists. A [goal](../../TERMS.md#goal) is an outcome the manager asked for *and* a [boundary](../../TERMS.md#boundary) that may only call published verbs.

Not citizens: workflow-as-a-new-type (goal of goals; durable is a property), knowledge-domain-as-a-new-kind (standing ADRs + requirements + facts), business-need-as-a-document (optional tag on a goal).

## Compile [gate](../../TERMS.md#gate)

Generation is incomplete unless:

1. Output is BBP-shaped.
2. Every invoice-shaped fact lives behind one Invoice [boundary](../../TERMS.md#boundary) (noun inside, verbs on the edge).
3. A [gate](../../TERMS.md#gate) fails a [goal](../../TERMS.md#goal) that implements that [adjective](../../TERMS.md#adjective) itself or writes [noun](../../TERMS.md#noun) fields.

Two [goal](../../TERMS.md#goal) boxes are fine if both only call Invoice verbs.

## Context

The repo may be a monorepo. The window for write, [audit](../../TERMS.md#audit), and graph is one atomic object plus the hard contracts of its neighbors. If a step needs two objects’ internals at once, the cut is wrong.

## What is derived

A particular `Invoice` module, verb bodies, [goal](../../TERMS.md#goal) code, diagrams, most runbooks. Regenerable. Internals behind a stable verb [contract](../../TERMS.md#contract) may be rewritten without the manager opening the file.

A *breaking* change to a [published verb contract](../../TERMS.md#published-verb-contract) is a product event: impact on callers, fix the [requirement](../../TERMS.md#requirement) if the behavior was wrong, regenerate. Do not patch the generated [contract](../../TERMS.md#contract) to hide a [defect](../../TERMS.md#defect).

`CHARTER.md` remains the design SSOT. This page does not replace it.
