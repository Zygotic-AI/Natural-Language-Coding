# A-R7

- Requirement: `R7`
- Outcome: **met** | **not met** only

## Statement

Nouns never call goals. Direction is goal → (goal public entrypoint | noun-verb) plus explicit reads. A durable engine may host a goal; it is not a caller above the goal layer.

## Binary criteria

Met iff a gate (CI check, confirmer step, or fitness tool) has verified this requirement against the current change and recorded PASS with evidence. Not met if no gate ran, the gate failed, or evidence is missing.

## Evidence

On met or not met, cite file and symbol (or N/A reason). List failing ids when the audit is a matrix audit.
