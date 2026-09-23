# [Compiler](../../TERMS.md#compiler)

This is not `gcc` with a chatbot.

`gcc` takes source code. [ACS](../../TERMS.md#acs) takes **intent** (goals, requirements, ADRs) and emits a **system**. The TypeScript (or Python) is an output, like an object file.

## Inputs

- Goals (outcomes)
- Requirements (constraints)
- ADRs (dated choices)
- [Knowledge domains](../../TERMS.md#knowledge-domain) (standing ADRs + requirements the interview already answered)
- [BBP](../../TERMS.md#bbp) standard (always on — `CHARTER.md`)
- Published verb contracts already in the tree

## Outputs

- Boundaries: [noun](../../TERMS.md#noun) + verbs + adjectives
- [Goal](../../TERMS.md#goal) implementations that only call those verbs
- Tests on the [noun](../../TERMS.md#noun) and on the [goal](../../TERMS.md#goal)
- Generated views (graphs, docs) — never hand-authored impact JSON

## Incomplete generation

The compile is not done if any of these is true:

- A [goal](../../TERMS.md#goal) assigns a [noun](../../TERMS.md#noun) field (R5 red).
- An [adjective](../../TERMS.md#adjective) exists in two implementations (C19 / R24 red).
- A product statement from the plan has no [binding](../../TERMS.md#binding).
- A [published verb contract](../../TERMS.md#published-verb-contract) changed and callers were not part of the plan ([ADR 0006](../../../adrs/0006-contract-change-notice.md): breaking = [prove](../../TERMS.md#prove) stays red; additive = impact graph only).
- A public [boundary](../../TERMS.md#boundary) is missing a failure mode (P4/R31 code-side red).

Deterministic *enough* means: same inputs + same standard → same shape and same contracts. Internals behind a [contract](../../TERMS.md#contract) may change. The edge may not quietly change.

## Failure mode

The [compiler](../../TERMS.md#compiler) does not “almost pass.” Gates exit 0 or 1. [RCA](../../TERMS.md#rca) consumes the 1. Humans do not negotiate the object file back to green.
