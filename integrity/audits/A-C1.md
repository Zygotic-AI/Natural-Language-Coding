# A-C1

- Requirement: `C1`
- Outcome: **met** | **not met** only
- Gate: `tools/fitness-c1.py`

## Statement

Change class (A–F) is stated.

## V1 bind

If `PROPOSAL.md` or `CONFIRM.md` exists at the scan root, it must match
`change class` + A–F.

No note file → skip (MET). That is not proof the change was classified.

Does not check the class is *correct*.

Designed fail: `examples/missing-change-class/`.
Designed pass: `examples/invoice-correct/`.
