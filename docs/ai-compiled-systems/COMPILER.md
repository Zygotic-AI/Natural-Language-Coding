# Compiler

This is not `gcc` with a chatbot.

`gcc` takes source code. ACS takes **intent** (goals, requirements, ADRs) and emits a **system**. The TypeScript (or Python) is an output, like an object file.

## Inputs

- Goals (outcomes)
- Requirements (constraints)
- ADRs (dated choices)
- Knowledge shelf (standing ADRs + requirements the interview already answered)
- BBP standard (always on — `CHARTER.md`)
- Published verb contracts already in the tree

## Outputs

- Boundaries: noun + verbs + adjectives
- Goal implementations that only call those verbs
- Tests on the noun and on the goal
- Generated views (graphs, docs) — never hand-authored impact JSON

## Incomplete generation

The compile is not done if any of these is true:

- A goal assigns a noun field (R5 red).
- An adjective exists in two implementations (C19 / R24 red).
- A product statement from the plan has no binding.
- A published verb contract changed and callers were not part of the plan.
- A public boundary is missing a failure mode (P4/R31 code-side red).

Deterministic *enough* means: same inputs + same standard → same shape and same contracts. Internals behind a contract may change. The edge may not quietly change.

## Failure mode

The compiler does not “almost pass.” Gates exit 0 or 1. RCA consumes the 1. Humans do not negotiate the object file back to green.
