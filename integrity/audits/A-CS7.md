# A-CS7

- [Requirement](../../docs/TERMS.md#requirement): `CS7`
- Outcome: **[met](../../docs/TERMS.md#met)** | **not [met](../../docs/TERMS.md#met)** only

## Statement

[Produce package](../../docs/TERMS.md#produce-package) present before fitness; incomplete handoffs refused, not soft-failed.

## Binary criteria

[Met](../../docs/TERMS.md#met) iff [produce package](../../docs/TERMS.md#produce-package) is present and complete before fitness scoring opens; incomplete handoffs receive `handoff_refused` status (not fitness FAIL). Not [met](../../docs/TERMS.md#met) if fitness scores content without package or converts missing package to FAIL.

## Evidence

On [met](../../docs/TERMS.md#met) or not [met](../../docs/TERMS.md#met), cite:
- [Produce package](../../docs/TERMS.md#produce-package) path and contents (PLAN, APPLICABILITY, BOUNDARY-IO, ADVERSARIAL, verify.sh)
- Fitness preflight result (`ready` or `handoff_refused`)
- Fitness score result (`MET` or `FAIL`) only present after preflight `ready`
