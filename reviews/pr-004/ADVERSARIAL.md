# PR-004 Self-Adversarial Notes

Pre-submission adversarial review by the producer against the charter.

## Checklist against charter rules

### R26 (Practice integrity P1–P7)

- [x] **P1 Stand-alone branding:** No foreign brand packages imported
- [x] **P2 Zero variance:** New rules prescribe actions with binary outcomes
- [x] **P3 Hard gates:** `complete-produce` and `preflight-fitness-handoff` have complete/incomplete outcomes
- [x] **P4 Hard boundary I/O:** All new verbs declare input, output, failure mode
- [x] **P5 Binary audits:** S7/CS7 have audit ids (A-S7, A-CS7)
- [x] **P6 Unbound matrix entries listed:** S7/CS7 added as unbound, surface=reference
- [x] **P7 Promote-only-when-bindable:** S7/CS7 are reference surface, not in-force; no false binders

### S5 (Produce ≠ Audit ≠ Ship)

- [x] This PR is produced by agent, to be audited by Reed (fitness), then Koan (adversarial), then shipped separately
- [x] The produce package (this directory) enforces S5 on itself

### S6 (Audit roles have no ship verbs)

- [x] quality-architect verbs exclude ship verbs (ratify, merge, release, approve)
- [x] adversarial-auditor verbs unchanged; still exclude ship verbs

## Potential holes identified

### Hole 1: Missing binder for S7/CS7

**Issue:** S7 and CS7 are added as reference surface, unbound. No CI binder exists.

**Mitigation:** This is intentional. The rules are reference-level until a binder can be written. Adding a false binder would violate P7.

**Reviewer question:** Is reference surface appropriate, or should these be deferred entirely?

### Hole 2: `handoff_token` optional in preflight

**Issue:** `handoff_token` is optional in `preflight-fitness-handoff` input. A producer could skip `complete-produce` and go directly to preflight.

**Mitigation:** Preflight still checks package presence. Token is convenience, not enforcement. Future tightening could require token.

**Reviewer question:** Should token be required to enforce `complete-produce` call?

### Hole 3: Quality-architect is new; no ship-role agent noun exists

**Issue:** Ship-role handoff-in is documented in README but there is no `ship-role/` agent noun package.

**Mitigation:** Ship authority currently belongs to human. Agent noun can be added when ship-role is formalized.

**Reviewer question:** Is README documentation sufficient, or should a stub agent noun be created?

## Self-adversarial rebuttal

This change strengthens the produce→fitness boundary without creating false binders. The holes identified are known limitations, not defects:

1. Reference-surface rules are the correct status for unbindable requirements (P7 compliance)
2. Token-optional allows incremental adoption without breaking existing flows
3. Ship-role documentation is sufficient until a ship-role agent noun is needed
