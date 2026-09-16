# Unbound matrix rows

Status SSOT: [`binding-matrix.json`](binding-matrix.json).

## Keep unbound (no honest v1 yet)

Classification: R1 R2 R3 R4 R16 C1 C2 C3 C13 C22 C23 C24.
Contracts leftover: R12 C7 C8 C10 C11.
Composition: R15 R17 R18 C15.
Integrity: P2 R20 C16 C17 C18.

A5 (taint) and A7 (escape hatch) have v1 tools. They are **not** matrix ids.

## Bound v1 (surface=reference)

| Id | Tool | Designed fail |
|----|------|----------------|
| R5 C4 R8 R23 | `fitness-no-noun-field-writes.py` | `invoice-violation` (R8 cousin: snapshot field write) |
| R6 C5 | `fitness-verb-path.py` | `invoice-verb-path-violation` |
| R9 R10 | `fitness-contract-presence.py` | `missing-contract` |
| R11 C9 | `fitness-schema-identity.py` | `schema-identity-violation` |
| R13 | `fitness-r13-entrypoints.py` | `extra-goal-entrypoint` |
| R25 | `fitness-r25-noun-tests.py` | `noun-without-tests` |
| C14 | `fitness-goal-imports.py` | (same as C12/R14) |
| C19 | `fitness-duplicated-adjective.py` | `duplicated-adjective-violation` |
| C21 | `fitness-c21.py` | `impact-list-mismatch` |
