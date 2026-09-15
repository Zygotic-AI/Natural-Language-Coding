# Manifesto

Software failures are usually not missing `if` statements. They are two truths about the same thing, each locally green.

Code is not the product. Intent is the product: goals, requirements, ADRs. Code is what a compiler emits from that source.

The compiler is AI. That does not mean “autocomplete in a file.” It means: humans keep intent; AI emits a system; a binder fails a quiet fork.

## The source language

Not TypeScript. Not a class diagram.

```text
Intent
  → goals
  → requirements
  → ADRs
  → AI compile
  → BBA-shaped code, tests, ops
```

The source is intent. The code is the object file.

## Why shape still matters

If the object file has no rule for where an invariant lives, two goals will each own `status`. Both goals can match the requirements. Users still find the $100k bug.

So the compiler is not free to emit any structure. It emits Boundary-Based Architecture: small boundaries, noun inside, verbs on the edge, goals only call verbs.

Humans do not maintain those noun files. They hire the compiler. If a human must edit generated code to keep invariants consistent, the architecture failed. The loop is: binder red → RCA → tighter interview / requirement / ADR → regenerate.

## Division of labor

Humans: outcomes, constraints, dated choices, sign-off on RCA and audits.

AI: architecture-shaped code, tests, regeneration, consistency inside a boundary.

## Measure

A healthy system is not “more generated files.” It is: one home per invariant, every goal talking to that home through a contract, and a machine check that fails when that is not true.
