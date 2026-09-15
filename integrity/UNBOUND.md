# Unbound matrix rows

Status SSOT: [`binding-matrix.json`](binding-matrix.json). 85 rows, 47 bound, 38 unbound.

A row moves to `bound` only when the tool proves *that statement*, can exit 1, and has a fixture.

---

## Keep unbound (38)

Classification: R1 R2 R3 R4 R16 C1 C2 C3 C13 C21 C22 C23 C24.

Mutation: R6 C5 R8 — verb-path v1 exists, not the full statement.

Contracts: R9 R10 R11 R12 R13 C7 C8 C9 C10 C11.

Composition: R15 R17 R18 C14 C15.

Integrity: P2 R20 R25 C16 C17 C18 C19.

---

## Bound, gate now matches better

| Id | Should be | Notes |
|----|-----------|-------|
| R24 | `tools/fitness-adjective-locality.py` | Tool + fixture shipped. **JSON still says field-writes.** Flip the binder field. |
| R23 | `fitness-no-noun-field-writes.py` | Assignment half. |
| R5 C4 | same | Correct. |

---

## Next

Flip `R24.binder`. Then A5 taint / A7 escapes. Do not bind P2, R1, or C24.
