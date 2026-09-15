# Unbound matrix rows

Living inventory. Source of truth for *status* is still [`binding-matrix.json`](binding-matrix.json). This file is the human grouping so we do not quietly mark rows `bound` without a gate that actually proves the statement.

Counted from the matrix: **85** requirements, **47** `status=bound` with a `binder` path, **38** `status=unbound` and empty `binder`.

`A-BINDING-UNBOUND` already fails and lists the 38. That is the correct default. Do not flip `status` to bound to make the list shorter.

---

## Rule for this list

A row may move to `bound` only when all of these are true:

1. A tool exists that can exit 1.
2. The tool's failure mode matches the *statement*, not a cousin of the statement.
3. A known-fail fixture exists, or the confirmer can point at one.

Until then the row stays `surface=reference`, `status=unbound`, `binder=""`.

The JSON key remains `binder` until `tools/audit-binding-matrix.py` is updated.

---

## Keep unbound (38)

### Classification and ownership — reviewer work, not a linter yet

| Id | Why it stays unbound |
|----|----------------------|
| R1 | "Would this noun become a lie?" is a design judgment. |
| R2 | Spanning work is a goal — needs classification, not grep. |
| R3 | God-method on the convenient noun — reviewer (A6). |
| R4 | Verb does not need the adjective set — reviewer (A6). |
| R16 | Distinct use-case vs pass-through — reviewer (R16 / C13). |
| C1 | Change class A–F stated — proposal package. |
| C2 | Adjectives on the named noun — proposal + R24 gate later. |
| C3 | Orchestration in a goal — reviewer. |
| C13 | No pass-through goal — reviewer. |
| C21 | Impact list matches generated callers — needs generated graph. |
| C22 | Charter/ADR/code same change — process. |
| C23 | Review findings closed — process. |
| C24 | Ratification recorded — process. |

### Mutation path — next real gates

| Id | Why it stays unbound |
|----|----------------------|
| R6 | Field-write gate (R5/C4) is not "every mutation is a public verb." |
| R8 | Snapshot-then-write is not the same as an assignment grep. |
| C5 | Same as R6. |

### Contracts — next real gates

| Id | Why it stays unbound |
|----|----------------------|
| R9 R10 C7 C8 | Need schema-presence on public entrypoints. |
| R11 C9 | Need same-name / different-type compare. |
| R12 C10 | Version + ADR — process plus schema compare. |
| R13 C11 | One public entrypoint — structural, not written yet. |

### Goal composition and durability

| Id | Why it stays unbound |
|----|----------------------|
| R15 | Shared adjective logic on the noun — cousin of R24 / C19. |
| R17 | "No workflow citizen" is a model rule. Public calls are C14 / R14. |
| R18 C15 | Idempotency of retried verbs — no gate yet. |
| C14 | Public goal-to-goal. `fitness-goal-imports.py` covers *internals* (C12 / R14), not "called the public entrypoint." Do not reuse that tool as a C14 bind. |

### Integrity of the change

| Id | Why it stays unbound |
|----|----------------------|
| P2 | "Every changing action is prescribed and gated" is the whole program. Binding it to the matrix auditor would lie. |
| R20 | Charter/contracts/code agree — no three-way drift gate. |
| R25 | Adjective tests next to the noun, on every verb — no test-layout gate. |
| C16 C17 C18 | Test presence / scope — no test gate. |
| C19 | Duplicated adjective predicates. |

---

## Bound, but the gate is thinner than the statement

Do not treat these as finished product. They stay `bound` because a tool runs; they are not the full claim.

| Id | Registered gate | Gap |
|----|-----------------|-----|
| R24 | `fitness-no-noun-field-writes.py` | Catches field writes, not copy-pasted status machines or money math. |
| R23 | same tool | Assignment half only. Import-of-internals is a sibling. |
| P3 P4 R30 R31 | `fitness-agent-noun-structure.py` | Proves agent-noun packages, not every public code boundary. |
| R14 / C12 | `fitness-goal-imports.py` | Correct for internals. Does not bind R17 or C14. |

---

## Next bind, in product order

1. Leave the 38 listed (this file + matrix auditor). **This item is the listing.**
2. R6 / C5 — verb-path gate.
3. R24 — real adjective-locality gate; then decide whether to keep or split the current R24 bind.
4. A5 taint / one-boundary.
5. A7 escape hatches (also closes part of R6).
6. R9 / R10 / C7 / C8.
7. R11 / C9.
8. C19.

Do not start by binding P2, R1, or C24.
