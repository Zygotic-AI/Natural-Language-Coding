# ADR 0026 — promote X1–X3 expansion runners to law

- Status: Accepted
- Date: 2026-09-22
- Deciders: Human manager
- Class: F (process)
- Corpus: nlc

## Context

ADR 0024 named action↔plan validation, reverse-audit, and full emit-manifest
enforcement as expansion. The runners now exist and are specimen-tested. Leaving
them marked "expansion" would be a soft-green: the law says the gate exists, the
gate exists, but the rule file still says "expansion."

## Decision

1. NLC-0024-04 gate becomes `tools/nlc-action-plan-gate.py` (fitness:
   `fitness-nlc-action-plan-gate.py`).
2. NLC-0024-05 gate becomes `tools/nlc-reverse-audit.py` (fitness:
   `fitness-nlc-reverse-audit.py`).
3. NLC-0024-06 gate becomes `tools/nlc-emit-manifest-enforce.py` (fitness:
   `fitness-nlc-emit-manifest-enforce.py`), which enforces
   `docs/nlc/emit-manifest.schema.json` on every `emit-manifest.json`.
4. `fitness-nlc-0024-expansion-parked.py` is retired: it asserted the rules
   stayed expansion, which is now false. It is deleted in this change.
5. FINDINGS Parked rows for X1–X3 move to "done" in the same change set.

## Consequences

- Pipeline steps 2, 4, and 5–6 of ADR 0024 are now machine-enforced, not
  aspirational.
- Emit still does not select rules; selection remains plan → actions → ADR
  bindings → reverse audit.

## Rejected

- Keeping "expansion" labels after the runners landed (soft-green).
- Requiring manifests on trees with zero emits (default-closed: empty passes).
