# A-CS7

- Requirement: `CS7`
- Outcome: **met** | **not met** only

## Statement

Produce package present before fitness; incomplete handoffs refused, not soft-failed.

## Binary criteria

Met iff produce package is present and complete before fitness scoring opens; incomplete handoffs receive `handoff_refused` status (not fitness FAIL). Not met if fitness scores content without package or converts missing package to FAIL.

## Evidence

On met or not met, cite:
- Produce package path and contents (PLAN, APPLICABILITY, BOUNDARY-IO, ADVERSARIAL, verify.sh)
- Fitness preflight result (`ready` or `handoff_refused`)
- Fitness score result (`MET` or `FAIL`) only present after preflight `ready`
