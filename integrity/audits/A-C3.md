# A-C3

- Requirement: `C3`
- Outcome: **met** | **not met** only
- Gate: `tools/fitness-c3.py`

## Statement

New orchestration lives in a goal, not as a method on an unrelated noun.

## V1 bind

If `domain/<other>/*.py` calls `.verb(` owned by a different noun, fail.

One noun in the tree → skip (MET). Does not judge "related."

Designed fail: `examples/orchestration-on-noun/`.
Designed pass: `examples/invoice-correct/`.
