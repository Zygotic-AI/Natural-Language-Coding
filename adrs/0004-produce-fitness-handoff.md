# ADR 0004 — Produce→fitness handoff is default-closed

- Status: needs_review
- Date: 2026-09-05
- Deciders: Reed (Quality Architect) draft; adversarial + ship separately
- Class: F (charter/agent)
- Tags: grokbot, systems, handoff, P-016

## Context

On PR #3, fitness returned FAIL for a missing produce package, then the stream talked about "re-gating." That language is a defect signal.

Value-creation stream: produce → claim ready for fitness → fitness FAIL (missing package) → remediate package → fitness again.

Furthest upstream: Produce→fitness handoff is not default-closed. Produce can signal ready without the review package. Fitness became a discovery loop.

Not the root: one FAIL instance; one forgotten package; "re-gate" as normal ops.

Aligns with: S5 Produce ≠ Audit ≠ Ship; P-015/KD-010; §16.1 Gate ≠ Audit.

## Decision

1. **Produce completion = change artifacts AND produce package** (plan A–F + §6 Step 2; applicability; boundary I/O; self-adversarial notes). Without package → incomplete; no handoff to fitness.

2. **Fitness preflight:** missing/incomplete package → `handoff_refused` / produce incomplete — NOT fitness FAIL discovery. Log produce-handoff defect. Do not open content scoring.

3. **Language:** do not normalize "re-gate" for missing packages.

4. **Cursor/cloud produce DoD and fitness checklist cite the same handoff contract.**

## Consequences

- Producers cannot claim ready without package; fitness receipts distinguish `handoff_refused` vs `MET` vs `FAIL`.
- Auditor does not convert refusal into audit FAIL.
- Metrics: refusals vs slip-throughs.
- Charter §6 Step 2 gains produce package requirement.
- Charter §16.1 gains handoff_refused ≠ fitness FAIL clarification.
- New rule S7 (Produce→fitness handoff default-closed) and checklist item CS7.
- Agent packages (standards-steward, quality-architect, adversarial-auditor) gain handoff contract references.

## Rejected

- Soft FAIL-as-discovery: masks the upstream defect (incomplete produce).
- Folding into PR #3: PR #3 addresses A1/A2 deferred findings; this is a distinct follow-on.
- Fitness inventing package: violates produce ≠ audit.
- "Re-gate" as normal vocabulary: normalizes defect-driven rework.

## Related

- [ADR 0001](0001-zero-variance-integrity.md) — Zero-variance integrity (P1–P7)
- [ADR 0003](0003-systems-extension-agent-nouns.md) — Systems extension: agent nouns
- Charter §6 (Order of agent execution)
- Charter §16.1 (Vocabulary mapping)
- Charter S5 (Produce ≠ Audit ≠ Ship)
