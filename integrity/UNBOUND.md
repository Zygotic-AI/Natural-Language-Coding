# Unbound matrix rows

Status SSOT: [`binding-matrix.json`](binding-matrix.json).

## Keep unbound (no honest v1 yet)

Classification: R1 R2 R3 R4 R16 C1 C2 C3 C13 C21 C22 C23 C24.
Mutation leftover: R8.
Contracts leftover: R12 R13 C7 C8 C10 C11 (C7/C8 are *changed*-scoped; R9/R10 are tree-wide and bound).
Composition: R15 R17 R18 C14 C15.
Integrity: P2 R20 R25 C16 C17 C18 C19.

A5 (taint) and A7 (escape hatch) have v1 tools. They are **not** matrix ids. Do not add decorative rows.

## Bound this pass (v1, surface=reference)

| Id | Tool | Designed fail |
|----|------|----------------|
| R6 C5 | `fitness-verb-path.py` | `invoice-verb-path-violation` |
| R9 R10 | `fitness-contract-presence.py` | `missing-contract` |
| R11 C9 | `fitness-schema-identity.py` | `schema-identity-violation` |
