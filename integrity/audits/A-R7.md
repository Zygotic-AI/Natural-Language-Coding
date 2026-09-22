# A-R7

- [Requirement](../../docs/TERMS.md#requirement): `R7`
- Outcome: **[met](../../docs/TERMS.md#met)** | **not [met](../../docs/TERMS.md#met)** only

## Statement

Nouns never call goals. Direction is [goal](../../docs/TERMS.md#goal) → (goal public entrypoint | noun-verb) plus explicit reads. A durable engine may host a [goal](../../docs/TERMS.md#goal); it is not a caller above the [goal](../../docs/TERMS.md#goal) layer.

## Binary criteria

[Met](../../docs/TERMS.md#met) iff a [gate](../../docs/TERMS.md#gate) (CI check, confirmer step, or fitness tool) has verified this [requirement](../../docs/TERMS.md#requirement) against the current change and recorded PASS with evidence. Not [met](../../docs/TERMS.md#met) if no [gate](../../docs/TERMS.md#gate) ran, the [gate](../../docs/TERMS.md#gate) failed, or evidence is missing.

## Evidence

On [met](../../docs/TERMS.md#met) or not [met](../../docs/TERMS.md#met), cite file and symbol (or N/A reason). List failing ids when the [audit](../../docs/TERMS.md#audit) is a matrix [audit](../../docs/TERMS.md#audit).
