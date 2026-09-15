# Unbound matrix rows

Living inventory. Source of truth for *status* is still [`binding-matrix.json`](binding-matrix.json).

Counted from the matrix: **85** requirements, **47** `status=bound` with a `binder` path, **38** `status=unbound` and empty `binder`.

`A-BINDING-UNBOUND` already fails and lists the 38. Do not flip `status` to bound to make the list shorter.

---

## Rule for this list

A row may move to `bound` only when all of these are true:

1. A tool exists that can exit 1.
2. The tool's failure mode matches the *statement*, not a cousin of the statement.
3. A known-fail fixture exists, or the confirmer can point at one.

Until then the row stays `surface=reference`, `status=unbound`, `binder=""`.

---

## Keep unbound (38)

### Classification and ownership — reviewer work, not a linter yet

R1 R2 R3 R4 R16 C1 C2 C3 C13 C21 C22 C23 C24.

### Mutation path

| Id | Why it stays unbound |
|----|----------------------|
| R6 | `tools/fitness-verb-path.py` exists (v1: `.save(` / `UPDATE` / `setattr(` in outside trees) with fixture `examples/invoice-verb-path-violation/`. That is a cousin of "every mutation is a public verb," not the statement. **Do not bind.** |
| C5 | Same tool, same reason. |
| R8 | Snapshot-then-write is not an assignment grep and not a `.save(` grep. |

### Contracts

R9 R10 R11 R12 R13 C7 C8 C9 C10 C11.

### Goal composition and durability

R15 R17 R18 C14 C15.

### Integrity of the change

P2 R20 R25 C16 C17 C18 C19.

---

## Bound, but the gate is thinner than the statement

| Id | Registered gate | Gap |
|----|-----------------|-----|
| R24 | `fitness-no-noun-field-writes.py` | Field writes, not copy-pasted status machines. |
| R23 | same tool | Assignment half only. |
| P3 P4 R30 R31 | `fitness-agent-noun-structure.py` | Agent packages, not every code boundary. |
| R14 / C12 | `fitness-goal-imports.py` | Internals only. |

---

## Next bind, in product order

1. Listing — done (this file).
2. R6 / C5 — v1 tool shipped, **not bound**. Grow it (A7) before promoting.
3. R24 — real adjective-locality gate.
4. A5 taint / one-boundary.
5. A7 escape hatches — also how R6 v1 becomes bindable.
6. R9 / R10 / C7 / C8.
7. R11 / C9.
8. C19.

Do not start by binding P2, R1, or C24.
