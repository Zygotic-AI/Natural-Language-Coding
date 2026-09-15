# CHARTER.merged.section16.md

> TODO (vocabulary): charter still says *laws* / *invariants*. Settled term is **adjective**. Applied locally in this section; global rename pending.
> TODO (vocabulary): *binder* → **gate**. Applied locally where "fitness check" meant the enforcement mechanism.
> TODO (open question): workflow listed as a peer of noun/verb/goal. ACS says workflow is a goal-of-goals. Confirm before §4 / §5.5.
> TODO (open question): §16.1 mapping table still lists "Invariant" row — should read "Adjective". Pending global pass.

## 16. Systems model — agent nouns

Ratified by [`adrs/0003-systems-extension-agent-nouns.md`](adrs/0003-systems-extension-agent-nouns.md).

The software model (§4) organizes code so agents can change it without scattering adjectives. The same structural discipline organizes **agent fleets** — durable roles that operate a system over time.

### 16.1 Vocabulary mapping

| Software BBP | Systems BBP |
|--------------|-------------|
| Noun | Agent noun — durable role with identity and adjectives |
| Verb (on noun) | Verb — legal function an agent may perform; contracted I/O |
| Goal | Use-case — orchestration across agent nouns or to the outside world |
| Workflow | Workflow — durable composition of use-cases |
| Contract | Boundary artifact — input, output, failure mode, handoff, completion |
| Adjective | Role adjective — what the agent must never violate |
| Fitness check | Gate — automated enforcement; binary pass/fail; CI-bound |
| Adversarial review | Audit — role-based review against charter; produces findings |

**Gate ≠ Audit.** Gates are automated enforcement mechanisms (gates, CI rules) that fail the build. Audits are role-based adversarial reviews (adversarial-auditor agent noun) that produce findings for a ship decision. Both yield binary outcomes (ops vs defects), but differ in mechanism and authority:
- Gates block automatically; no human or role decides.
- Audits produce findings; a ship-role or human decides whether findings block.

For the formal Gate definition, all-required PASS fitness bar (G1--G4), and design rules, see [`integrity/GATE.md`](integrity/GATE.md).

**Handoff refused ≠ gate FAIL.** When gate preflight returns `handoff_refused` (produce package missing/incomplete), that is not a gate FAIL. It is a produce-incomplete signal. The Gate remains the CI enforcement point for gate scoring; preflight refusal is upstream of Gate. Do not normalize "re-gate" language for missing-package rework — that masks the produce-handoff defect.

### 16.2 Agent noun structure

Every agent noun package (under `agents/<name>/`) declares:

| Element | Purpose |
|---------|---------|
| **Identity** | Role name, purpose (one line) |
| **Adjectives** | What the agent must never violate |
| **Verb list** | Each verb has input contract, output contract, failure mode |
| **Handoff-in** | What must be true before this agent receives work |
| **Completion artifact** | What the agent produces to mark work complete |
| **Success criteria** | Ops vs defects; binary auditable outcomes |

Packages may use structured markdown or machine-readable schemas; the boundary declarations must be confirmer-checkable.

### 16.3 Produce ≠ Audit

An agent that **produces** an artifact may not be the final **auditor** of that artifact. The agent that **ships** (ratifies, merges, releases) may not be the same agent that grades itself.

Separate:

1. **Produce** — create the artifact
2. **Audit** — adversarial review against charter/adjectives
3. **Ship** — authorize release

This is §7 applied to systems: proposer ≠ reviewer ≠ confirmer.

### 16.4 Audit roles have no shipping authority

Agent nouns whose purpose is **adversarial review**, **audit**, or **standards enforcement** do not have shipping authority.

- They may **not** ratify, merge, or release.
- They **produce findings**. Another role (or human) decides whether findings block the ship.
- Their verb lists explicitly exclude ship verbs.

### 16.5 Ship noun

Ship is a first-class agent noun, separate from produce and audit. The ship noun authorizes release — it decides whether produced artifacts with audit findings may be released.

#### Identity

**Name:** ship-role (or specific variants: ratify-role, merge-role, release-role)

**Purpose:** Authorize the release of artifacts that have completed produce and audit phases. Decide whether work moves from "done" to "shipped."

#### Adjectives

1. **Ship follows produce and audit.** A ship verb may only execute after the artifact has been produced and audited. Ship does not skip the pipeline.

2. **Ship is a decision, not a review.** Ship decides whether audit findings block release. Ship does not re-audit.

3. **Ship is recorded.** Every ship action records who, when, what artifact version, and what audit findings were accepted or required to be fixed.

4. **Ship authority is granted.** Ship verbs require explicit charter mandate or human delegation. An agent noun does not assume ship authority.

#### Verbs

| Verb | Purpose | Precondition |
|------|---------|--------------|
| `ratify` | Accept a proposal as final | Audit complete; findings addressed or waived |
| `merge` | Merge a change to target branch | Audit complete; CI green (or waiver recorded) |
| `release` | Publish or deploy an artifact | Merge complete; release criteria met |
| `waive-finding` | Accept a finding without fix | Finding documented; risk acknowledged |

Each verb has input contract, output contract, and failure mode. See agent noun package for schemas.

#### Handoff-in

| Condition | Evidence |
|-----------|----------|
| Artifact produced | Path to artifact or proposal |
| Audit complete | Audit report with findings or clean status |
| Ship authority granted | Charter mandate or delegation record |

#### Completion artifact

| Artifact | Contents |
|----------|----------|
| Ship record | Who, when, artifact version, findings disposition |

#### Success criteria

| Measure | Ops (success) | Defect |
|---------|---------------|--------|
| Pipeline honored | Ship followed produce and audit | Ship skipped a phase |
| Decision recorded | Ship record exists with all fields | Ship action without record |
| Authority verified | Ship authority checked before verb | Ship without authority |

### 16.6 Rules for agent nouns

**S1.** Every agent noun has an identity file that states purpose and adjectives.

**S2.** Every verb on an agent noun has an input contract, output contract, and failure mode — just like noun-verbs in code (R10).

**S3.** Every agent noun declares handoff-in (preconditions) and completion artifact (postconditions).

**S4.** Success criteria are binary: ops (work completed as specified) vs defects (deviation from spec or adjectives).

**S5.** Produce ≠ Audit ≠ Ship. An agent may not audit its own output as the final gate.

**S6.** Audit roles have no ship verbs. Adversarial auditors produce findings; another role decides.

**S7.** Produce→gate handoff is default-closed. Produce completion requires change artifacts AND produce package. Without a complete package, gate preflight returns `handoff_refused`; content scoring does not open.

**S8.** Produce packages require task/board SSOT exit evidence. Packages must include `ssot_leaf_ids` (one or more opaque leaf ids from the task/board SSOT) and `ssot_exit_status` (non-empty exit state string). Missing SSOT exit evidence triggers `handoff_refused` (same refuse class as S7); gate scoring refuses MET; adversarial audit refuses PASS (P-020).

### 16.8 Quality metric (ops vs defects)

SSOT: [`integrity/QUALITY_METRIC.md`](integrity/QUALITY_METRIC.md).

Quality measures the rate of defect-free operations across agent processes:

```text
Quality = Ops / Opportunities
```

Where **Opportunities** are gate/verb executions with binary outcomes, **Ops** are opportunities that completed as specified (PASS, MET, ready), and **Defects** are deviations from spec (FAIL, handoff_refused, error). This is DPMO-class without the academic theater.

**Q1.** Quality evidence required at gate. Produce packages must include gate receipts with `outcome` + `timestamp`. Missing evidence triggers `handoff_refused` with `QUALITY_EVIDENCE`.

**Q2.** Quality evidence required at adversarial audit. Artifacts must have `ssot_leaf_ids` present AND `quality_snapshot` with non-zero `opportunities`. Missing evidence causes audit FAIL citing Q2.

**Q3.** Quality snapshot recorded at boundary exit. Completion artifacts include `{ opportunities, ops, defects, quality }`.

**Q4.** Defect classification is binary. Every outcome is exactly op or defect. No partial, weighted, or continuous scores.

**Q5.** Quality formula is ops/opportunities. No alternative formulas for the canonical quality metric.

### 16.9 Confirmation checklist (systems)

For changes that touch agent nouns:

- [ ] CS1. Agent noun has identity and adjectives.
- [ ] CS2. Each verb has input, output, and failure mode.
- [ ] CS3. Handoff-in and completion artifact are declared.
- [ ] CS4. Success criteria are binary (ops vs defects).
- [ ] CS5. Produce ≠ Audit ≠ Ship separation is honored.
- [ ] CS6. Audit roles have no ship verbs.
- [ ] CS7. Produce package present before gate; incomplete handoffs refused, not soft-failed.
- [ ] CS8. Task/board SSOT exit evidence present in produce package (`ssot_leaf_ids` + `ssot_exit_status`); missing evidence refused (P-020).
- [ ] CS9. Quality evidence present in produce package (gate receipts with outcome + timestamp).
- [ ] CS10. Quality snapshot recorded at boundary exit (`{ opportunities, ops, defects, quality }`).

---

## How §16 works in the merge

Section 16 extends BBA from code to agent fleets. The same four primitives — noun, verb, adjective, goal — now describe durable agent roles. An agent noun owns adjectives (what it must never violate), exposes verbs (contracted functions), and is orchestrated by use-cases (goals). The ship noun is a first-class citizen: produce, audit, and ship are separated, mirroring §7's proposer/reviewer/confirmer split.

ACS adds one line: agent nouns are compiled from intent too. A role's adjectives come from requirements and ADRs, not from the agent's own judgment. The gate family (G1–G4) enforces them the same way check 1 enforces noun privacy in code. Swapping an agent implementation is one adjective change on one agent noun — same promise as swapping Logstash for file logging.

Three TODOs carried forward: global vocabulary rename, binder→gate, workflow-as-peer. None block.
