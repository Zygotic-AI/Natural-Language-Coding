# A-C5

- Requirement: `C5`
- Outcome: **met** | **not met** only

## Statement

Every state change of a noun goes through a public verb.

## Binary criteria

Met iff a gate has verified this requirement against the current change and recorded PASS with evidence. Not met if no gate ran, the gate failed, or evidence is missing.

## V1 tool (not a matrix bind)

Same tool as A-R6: `tools/fitness-verb-path.py`. Same fixture: `examples/invoice-verb-path-violation/`.

C5 stays `unbound`. Field assignment remains C4 / R5.

## Evidence

Cite each `VIOLATION <path>:<line> <kind>`, or `RESULT:MET` with scan roots.
