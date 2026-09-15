# A-R6

- Requirement: `R6`
- Outcome: **met** | **not met** only

## Statement

The only legal mutation of a noun is a public verb on that noun.

## Binary criteria

Met iff a gate has verified this requirement against the current change and recorded PASS with evidence. Not met if no gate ran, the gate failed, or evidence is missing.

## V1 tool (not a matrix bind)

`tools/fitness-verb-path.py` fails persistence escapes in `goals/` / `adapters/` / `workflows/`:
`.save(`, `.update(`, `.execute(`, `UPDATE <table>`, `INSERT INTO`, `DELETE FROM`, `setattr(`.

Known-fail: `examples/invoice-verb-path-violation/`.
Known-pass: `examples/invoice-correct/` (and the R5 field-write fixture, which this tool does not treat as a verb-path fail).

This is a **subset** of R6. It does not prove every mutation is a public verb. R6 stays `unbound` in the matrix until the gate covers the statement, not a cousin of it.

## Evidence

Cite each `VIOLATION <path>:<line> <kind>`, or `RESULT:MET` with scan roots.
