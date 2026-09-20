# [Boundary](../docs/TERMS.md#boundary)

SSOT for the [Boundary](../docs/TERMS.md#boundary) and [Handoff](../docs/TERMS.md#handoff) nouns in [Boundary-Based Programming](../docs/TERMS.md#bbp). Boundaries own adjectives for a stage; handoffs are [refuse-wired](../docs/TERMS.md#default-closed) gates between Boundaries.

Rationale: [charter](../docs/TERMS.md#charter) §16 vocabulary, §5.8 practice [integrity](../docs/TERMS.md#integrity). Related: [`GATE.md`](GATE.md), [`PRINCIPLES.md`](PRINCIPLES.md) P3 (hard gates).

---

## Definition

A **[Boundary](../docs/TERMS.md#boundary)** is a named stage in a work pipeline that:

1. **Owns adjectives** -- the adjectives, preconditions, and postconditions that govern what may happen at this stage
2. **Is [default-closed](../docs/TERMS.md#default-closed)** -- work does not enter or exit until [handoff](../docs/TERMS.md#handoff) criteria are [met](../docs/TERMS.md#met)
3. **Produces a binary advance** -- work either advances to the next [boundary](../docs/TERMS.md#boundary) or does not; no partial progress

Boundaries exist in code (noun modules, goal entrypoints) and in the agent pipeline (produce, fitness, audit, ship). A [boundary](../docs/TERMS.md#boundary) without an exit [handoff](../docs/TERMS.md#handoff) is a dead end; a [boundary](../docs/TERMS.md#boundary) with a soft exit is not a [boundary](../docs/TERMS.md#boundary).

### [Boundary](../docs/TERMS.md#boundary) ≠ Phase ≠ Checkpoint

| Concept | Owns adjectives? | Binary advance? | Has [handoff](../docs/TERMS.md#handoff)? |
|---------|------------|-----------------|--------------|
| **[Boundary](../docs/TERMS.md#boundary)** | Yes | Yes | Required |
| Phase | No (convenience grouping) | No | Optional |
| Checkpoint | Partially (may be advisory) | Sometimes | Sometimes |

**[Boundary](../docs/TERMS.md#boundary) ≠ Phase.** Phases are convenience groupings for project management. Boundaries own the adjectives of what happens inside them and enforce binary advance at exit.

---

## [Handoff](../docs/TERMS.md#handoff)

A **[Handoff](../docs/TERMS.md#handoff)** is a [refuse-wired](../docs/TERMS.md#default-closed) [gate](../docs/TERMS.md#gate) between two Boundaries. Every [handoff](../docs/TERMS.md#handoff) must meet the [Gate](../docs/TERMS.md#gate) fitness bar (G1--G4).

### [Handoff](../docs/TERMS.md#handoff) requirements

| [Requirement](../docs/TERMS.md#requirement) | Meaning |
|-------------|---------|
| **G1. Incomplete cannot PASS** | If the artifact is incomplete -- missing required fields, missing [SSOT exit evidence](../docs/TERMS.md#ssot-exit-evidence), missing [produce package](../docs/TERMS.md#produce-package) -- the [handoff](../docs/TERMS.md#handoff) refuses. No "proceed with warnings." |
| **G2. Machine-checkable or [refuse-wired](../docs/TERMS.md#default-closed)** | If a check cannot run (missing input, parser failure, network error), the [handoff](../docs/TERMS.md#handoff) refuses. No vibes-only checks. |
| **G3. Incomplete-packet fixture fails** | The [handoff](../docs/TERMS.md#handoff) must fail realistic bad input. The incomplete-packet fixture documents a known-bad case and proves the [handoff](../docs/TERMS.md#handoff) rejects it. |
| **G4. PASS needs no human redo** | A PASS means work is ready for the next [boundary](../docs/TERMS.md#boundary). If PASS requires a human to fix, double-check, or complete something, that is not a PASS. |

### [Handoff](../docs/TERMS.md#handoff) ≠ Review

| Mechanism | Authority | Output | Owns adjectives? |
|-----------|-----------|--------|------------|
| **[Handoff](../docs/TERMS.md#handoff)** | Refuses automatically | PASS / [REFUSE](../docs/TERMS.md#refuse) | Yes -- G1--G4 |
| Review | Human or role judgment | Approval / comments | No |

**[Handoff refused](../docs/TERMS.md#handoff_refused) ≠ fitness FAIL.** When a [handoff](../docs/TERMS.md#handoff) refuses (`handoff_refused`), that is a produce-incomplete signal, not a content [defect](../docs/TERMS.md#defect). The [Gate](../docs/TERMS.md#gate) remains the CI enforcement point for fitness scoring; [handoff](../docs/TERMS.md#handoff) refusal is upstream of [Gate](../docs/TERMS.md#gate). Do not conflate `handoff_refused` with `FAIL`.

### Design [rule](../docs/TERMS.md#rule): [refuse](../docs/TERMS.md#refuse) + incomplete-packet fixture in same tip

When designing or documenting a [handoff](../docs/TERMS.md#handoff), write the **[refuse](../docs/TERMS.md#refuse) criteria** and the **incomplete-packet fixture** in the same section. This forces the [handoff](../docs/TERMS.md#handoff) author to:

1. State what the [handoff](../docs/TERMS.md#handoff) refuses (the REFUSE conditions)
2. Provide a concrete example (incomplete packet) that would [REFUSE](../docs/TERMS.md#refuse)
3. [Prove](../docs/TERMS.md#prove) the [refuse](../docs/TERMS.md#refuse) criteria catch the incomplete packet

A [handoff](../docs/TERMS.md#handoff) tip without a documented incomplete-packet fixture is incomplete.

---

## Incomplete-packet fixture: 15855 without §7/R3/R4

Reference case for handoffs in the raise-to-HITL path (Human Root-Approver escalation).

**Scenario:** Leaf 15855 was raised without:
- §7 Preventive [action](../docs/TERMS.md#action) (Owner / Path / Verification)
- R3 (named actionable preventive)
- R4 (self-heal Y/N + future capture Y/N)

**Required outcome:** Any raise-readiness [handoff](../docs/TERMS.md#handoff) must [REFUSE](../docs/TERMS.md#refuse) this packet at every [boundary](../docs/TERMS.md#boundary):
- Produce → Fitness: `handoff_refused` (produce incomplete)
- Fitness → [Audit](../docs/TERMS.md#audit): refuses [MET](../docs/TERMS.md#met) (required fields missing)
- [Audit](../docs/TERMS.md#audit) → UAT: refuses PASS (R3+R4 absent)
- UAT → [Ship](../docs/TERMS.md#ship): refuses greenlight (incomplete packet)

**Fixture verification under G1--G4:**

| Criterion | Evidence |
|-----------|----------|
| G1 | 15855 is incomplete (missing required fields) → must [REFUSE](../docs/TERMS.md#refuse) |
| G2 | §7/R3/R4 checks require concrete content validation; **[refuse-wired](../docs/TERMS.md#default-closed)** via [P-030](https://github.com/richardpickett/BBA-Bindings/pull/9) on Bindings main |
| G3 | 15855 is the incomplete-packet fixture; [handoff](../docs/TERMS.md#handoff) refuses it → [MET](../docs/TERMS.md#met) |
| G4 | PASS would require Human root-approver to add §7/R3/R4 → not self-sufficient → must [REFUSE](../docs/TERMS.md#refuse) |

**Conclusion:** A [handoff](../docs/TERMS.md#handoff) that would PASS 15855 is not a [handoff](../docs/TERMS.md#handoff). It is a review point with no enforcement.

### Amend fixture: 15855 with case bars only

**Scenario:** 15855 amend PASS contained case bars 1--7 but zero R3/R4 rows.

**Required outcome:** [REFUSE](../docs/TERMS.md#refuse). Case bars are additive; they never replace R3/R4. A readiness checklist with case bars but no R3/R4 is incomplete.

---

## UAT / Promote Evidence: [Refuse](../docs/TERMS.md#refuse) Greenlight

The **UAT / Promote Evidence** [Boundary](../docs/TERMS.md#boundary) is owned by **Release Conductor** (role, never a person name). This [boundary](../docs/TERMS.md#boundary) refuses greenlight -- **soft-green into [Ship](../docs/TERMS.md#ship) = [REFUSE](../docs/TERMS.md#refuse)**.

**UAT / Promote Evidence all-required PASS greenlight lands BEFORE [Ship](../docs/TERMS.md#ship)** (when suite applies). Per Release Conductor lock:
- UAT greenlight is a precondition for [Ship](../docs/TERMS.md#ship)
- Incomplete packet / tip mismatch refuses [Ship](../docs/TERMS.md#ship) [handoff](../docs/TERMS.md#handoff)
- No [Ship](../docs/TERMS.md#ship) without UAT greenlight PASS

### [Refuse](../docs/TERMS.md#refuse) criteria

| Condition | Outcome | Rationale |
|-----------|---------|-----------|
| Missing suite check | [REFUSE](../docs/TERMS.md#refuse) | Cannot greenlight without complete test evidence |
| Tip marker mismatch | [REFUSE](../docs/TERMS.md#refuse) | Evidence does not match the artifact being released |
| Tip-race provisional | [REFUSE](../docs/TERMS.md#refuse) | Provisional results from tip race are not greenlight-ready |
| Wrong tip | [REFUSE](../docs/TERMS.md#refuse) | Evidence is for a different tip than release target |
| Soft-green evidence | [REFUSE](../docs/TERMS.md#refuse) | "Mostly passing" / "close enough" is not binary acceptance |
| Incomplete packet | [REFUSE](../docs/TERMS.md#refuse) | Missing required fields or [SSOT exit evidence](../docs/TERMS.md#ssot-exit-evidence) |

### Soft-green into [Ship](../docs/TERMS.md#ship) = [REFUSE](../docs/TERMS.md#refuse)

**Hard [rule](../docs/TERMS.md#rule):** UAT / Promote Evidence [handoff](../docs/TERMS.md#handoff) never soft-greens into [Ship](../docs/TERMS.md#ship):
- **[Ship](../docs/TERMS.md#ship) [Boundary](../docs/TERMS.md#boundary)** -- [ship](../docs/TERMS.md#ship) authorization requires UAT greenlight PASS
- **Execute-Release [Boundary](../docs/TERMS.md#boundary)** -- downstream of [Ship](../docs/TERMS.md#ship); blocked when [Ship](../docs/TERMS.md#ship) blocked

There is no path from UAT with incomplete or mismatched evidence to [Ship](../docs/TERMS.md#ship). The [handoff](../docs/TERMS.md#handoff) refuses; work returns to the prior [boundary](../docs/TERMS.md#boundary) for remediation.

### Incomplete-packet fixture: UAT greenlight mismatch

**Scenario:** Greenlight request with:
- Suite results from tip `abc123`
- Release target tip `def456`

**Required outcome:** [REFUSE](../docs/TERMS.md#refuse) (tip marker mismatch). The greenlight [handoff](../docs/TERMS.md#handoff) does not soft-pass to "close enough" or "same branch." Evidence must match the exact tip being released.

---

## Incomplete-packet hunt (adversarial half)

When an artifact defines a [Gate](../docs/TERMS.md#gate) or [Handoff](../docs/TERMS.md#handoff) tip, the adversarial [audit](../docs/TERMS.md#audit) includes an **incomplete-packet hunt**:

> Can an incomplete packet still slip the checklist?

**Definition:** Hunt for incomplete-packet slips. If fixture 15855 without §7/R3/R4 can still PASS the checklist → [audit](../docs/TERMS.md#audit) **FAIL**.

If the answer is yes, the [handoff](../docs/TERMS.md#handoff) tip is not [MET](../docs/TERMS.md#met). The incomplete-packet hunt does not design remediations -- it finds holes. Fixes belong to the produce role. See [`GATE.md`](GATE.md) § Incomplete-Packet Hunt.

**Adversarial auditor role:** See [`../agents/adversarial-auditor/AGENT.md`](../agents/adversarial-auditor/AGENT.md). The auditor produces findings. The auditor does not have [ship](../docs/TERMS.md#ship) authority. Verdicts are PASS / FAIL / [REFUSE](../docs/TERMS.md#refuse) only -- no soft PASS. If the auditor finds incomplete-packet slips, those are blocker-level findings → [audit](../docs/TERMS.md#audit) FAIL.

---

## Role-bound SOP: Boundaries and Handoffs

This SOP maps boundaries in the work pipeline to roles. Roles are organizational positions; person names do not appear.

### Role glossary

| Role | Purpose |
|------|---------|
| **Plan Steward** | Owns the plan [boundary](../docs/TERMS.md#boundary); ensures plan exit criteria are [met](../docs/TERMS.md#met) before work enters produce |
| **[RCA](../docs/TERMS.md#rca) Conductor** | Conducts root-cause analysis; raises readiness evidence to meet P-030 bar |
| **Producer** | Creates change artifacts (code tip, standard tip, design tip); owns [produce package](../docs/TERMS.md#produce-package) completion |
| **[Quality](../docs/TERMS.md#quality) Architect** | Gates fitness preflight and scoring; refuses incomplete handoffs; does not have [ship](../docs/TERMS.md#ship) authority |
| **Adversarial Auditor** | Attacks artifacts against [charter](../docs/TERMS.md#charter); produces findings; does not have [ship](../docs/TERMS.md#ship) authority |
| **[Defect](../docs/TERMS.md#defect) Remediator** | Fixes defects identified by [Quality](../docs/TERMS.md#quality) Architect or Adversarial Auditor; re-gates after fix |
| **Release Conductor** | Orchestrates UAT/promote and [ship](../docs/TERMS.md#ship) boundaries; coordinates greenlight, merge, release, deploy; refuses soft-green into [Ship](../docs/TERMS.md#ship) |
| **[Ship](../docs/TERMS.md#ship) Role** | Authorizes release (ratify, merge, release verbs); requires explicit mandate |
| **Escalation Steward** | Handles escalation paths when handoffs cannot advance; owns unblock decisions |
| **Human Root-Approver** | HITL root-approve authority for decisions that exceed agent mandate |

### [Boundary](../docs/TERMS.md#boundary) flow

```text
Plan ─┬─→ Produce ──→ Fitness ──→ Audit ──→ UAT/Promote ──→ Ship ──→ Execute-Release
      │
      └─→ Conduct-RCA ──→ Raise-Readiness (P-030/R3+R4) ──→ HITL Root-Approve ──→ Produce
```

**UAT / Promote Evidence all-required PASS greenlight lands BEFORE [Ship](../docs/TERMS.md#ship)** (when suite applies). Soft-green into [Ship](../docs/TERMS.md#ship) = [REFUSE](../docs/TERMS.md#refuse). Incomplete packet / tip mismatch refuses [Ship](../docs/TERMS.md#ship) [handoff](../docs/TERMS.md#handoff).

Post-approve cohort (system change path):
```text
System-Remediate Design ──→ Produce ──→ Fitness ──→ Audit ──→ UAT/Promote ──→ Ship ──→ Execute-Release ──→ Instance Heal
```

### [Boundary](../docs/TERMS.md#boundary) × Role × [Handoff](../docs/TERMS.md#handoff) map

| # | [Boundary](../docs/TERMS.md#boundary) | Role(s) | Handoff-out | [Refuse](../docs/TERMS.md#refuse) criteria | Incomplete-packet fixture |
|---|----------|---------|-------------|-----------------|---------------------------|
| 1 | **Plan** | Plan Steward | Plan → Produce | *Off [Gate](../docs/TERMS.md#gate) [noun](../docs/TERMS.md#noun) until [refuse-wired](../docs/TERMS.md#default-closed) plan exit exists* | (future: plan without acceptance criteria) |
| 2 | **Conduct-RCA** | [RCA](../docs/TERMS.md#rca) Conductor | [RCA](../docs/TERMS.md#rca) → Raise-Readiness | Investigation incomplete; no root cause named | [RCA](../docs/TERMS.md#rca) report without root cause statement |
| 3 | **Raise-Readiness** | [RCA](../docs/TERMS.md#rca) Conductor, [Quality](../docs/TERMS.md#quality) Architect, Adversarial Auditor, Escalation Steward | Raise → HITL Root-Approve | Missing §7 (Owner/Path/Verification), missing R3, missing R4; Adversarial Auditor refuses P-030 readiness (R3/R4); Escalation Steward refuses NHR packaging; see [P-030](https://github.com/richardpickett/BBA-Bindings/pull/9) | **15855 without §7/R3/R4** |
| 4 | **HITL Root-Approve** | Human Root-Approver | HITL → Produce | Readiness not [MET](../docs/TERMS.md#met); missing root-approve decision; incomplete packet | Raise packet without HITL approval record |
| 5 | **Produce** (code or standard tip) | Producer | Produce → Fitness | Missing [produce package](../docs/TERMS.md#produce-package); missing [SSOT exit evidence](../docs/TERMS.md#ssot-exit-evidence) (S7, S8) | Package without `ssot_leaf_ids` + `ssot_exit_status` |
| 6 | **Fitness** | [Quality](../docs/TERMS.md#quality) Architect | Fitness → [Audit](../docs/TERMS.md#audit) | Preflight `handoff_refused`; scoring not [MET](../docs/TERMS.md#met) | [Produce package](../docs/TERMS.md#produce-package) incomplete → `handoff_refused` (not FAIL) |
| 7 | **Adversarial [Audit](../docs/TERMS.md#audit)** | Adversarial Auditor | [Audit](../docs/TERMS.md#audit) → UAT/Promote | Unresolved blocker findings; incomplete-packet hunt finds slip → FAIL | [Audit](../docs/TERMS.md#audit) with unrebutted charter-rule violation |
| 8 | **UAT / Promote Evidence** | Release Conductor | UAT → [Ship](../docs/TERMS.md#ship) | Incomplete packet; tip mismatch (missing suite check, tip marker mismatch, tip-race provisional, wrong tip); soft-green evidence — **soft-green into [Ship](../docs/TERMS.md#ship) = [REFUSE](../docs/TERMS.md#refuse)** | Greenlight request with missing suite, tip mismatch, or "mostly passing" evidence |
| 9 | **[Ship](../docs/TERMS.md#ship)** | [Ship](../docs/TERMS.md#ship) Role, Release Conductor | [Ship](../docs/TERMS.md#ship) → Execute-Release | No mandate; pipeline not complete; findings not addressed; UAT greenlight not PASS | [Ship](../docs/TERMS.md#ship) request without UAT greenlight record |
| 10 | **Execute-Release** | Release Conductor | Execute → Instance Heal (or Done) | [Ship](../docs/TERMS.md#ship) not complete; release preconditions not [met](../docs/TERMS.md#met) | Execute request without [Ship](../docs/TERMS.md#ship) completion record |
| 11 | **System-Remediate Design** | Producer, [Quality](../docs/TERMS.md#quality) Architect | Design → Produce | Design incomplete; no [boundary](../docs/TERMS.md#boundary) I/O declared | Design doc without input/output/failure mode |
| 12 | **Instance Heal** | Release Conductor, [Defect](../docs/TERMS.md#defect) Remediator | Heal → Done | Instance not verified healthy; rollback not confirmed | Heal report without verification evidence |

### Notes on [boundary](../docs/TERMS.md#boundary) distinctions

1. **Plan [boundary](../docs/TERMS.md#boundary):** Currently off [Gate](../docs/TERMS.md#gate) [noun](../docs/TERMS.md#noun) until a [refuse-wired](../docs/TERMS.md#default-closed) plan exit is implemented. Plan Steward owns completeness criteria; [handoff](../docs/TERMS.md#handoff) to Produce is manual until a [gate](../docs/TERMS.md#gate) exists.

2. **Conduct-RCA → Raise-Readiness:** This is not code Produce. [RCA](../docs/TERMS.md#rca) work feeds the readiness [gate](../docs/TERMS.md#gate) (P-030 / R3+R4) before code work begins. Raise-Readiness includes:
   - **[Quality](../docs/TERMS.md#quality) Architect** -- gates fitness preflight
   - **Adversarial Auditor** -- refuses P-030 readiness (R3/R4 PASS/REFUSE)
   - **Escalation Steward** -- refuses NHR packaging

3. **HITL Root-Approve:** [Refuse-wired](../docs/TERMS.md#default-closed) [boundary](../docs/TERMS.md#boundary) after Raise-Readiness and before Produce on the raise path. Human Root-Approver must approve before work enters Produce. Incomplete packet or missing root-approve = [REFUSE](../docs/TERMS.md#refuse) [handoff](../docs/TERMS.md#handoff) into Produce. This [boundary](../docs/TERMS.md#boundary) appears in the flow diagram and map -- not glossary-only.

4. **Produce [boundary](../docs/TERMS.md#boundary):** Same machinery for code tip, standard tip, or design tip. Producer owns [produce package](../docs/TERMS.md#produce-package); [Quality](../docs/TERMS.md#quality) Architect refuses incomplete handoffs at fitness preflight.

5. **Fitness outcomes:** `MET` / `FAIL` / `handoff_refused`. The `handoff_refused` outcome is upstream of content scoring -- it means produce-incomplete, not content-defective. Do not normalize "re-gate" language for `handoff_refused`; that masks the produce-handoff [defect](../docs/TERMS.md#defect).

6. **Adversarial [audit](../docs/TERMS.md#audit):** [Audit](../docs/TERMS.md#audit) ≠ [Gate](../docs/TERMS.md#gate) ≠ Review. Auditors produce findings; they do not have [ship](../docs/TERMS.md#ship) authority. Verdicts are PASS / FAIL / [REFUSE](../docs/TERMS.md#refuse) only -- no soft PASS. When the artifact is a [Gate](../docs/TERMS.md#gate) tip or [Handoff](../docs/TERMS.md#handoff) tip, adversarial [audit](../docs/TERMS.md#audit) includes the incomplete-packet hunt.

7. **UAT / Promote Evidence:** Own [Boundary](../docs/TERMS.md#boundary) with **Release Conductor** role. **UAT greenlight lands BEFORE [Ship](../docs/TERMS.md#ship)** (when suite applies). Refuses greenlight on incomplete packet or tip mismatch:
   - Missing suite check
   - Tip marker mismatch
   - Tip-race provisional
   - Wrong tip
   - Soft-green evidence (e.g., "80% passing is close enough")
   
   **Soft-green into [Ship](../docs/TERMS.md#ship) = [REFUSE](../docs/TERMS.md#refuse).** Binary acceptance required; no provisional greenlight.

8. **[Ship](../docs/TERMS.md#ship) [boundary](../docs/TERMS.md#boundary):** [Ship](../docs/TERMS.md#ship) is a decision, not a review. [Ship](../docs/TERMS.md#ship) Role decides whether [audit](../docs/TERMS.md#audit) findings block release. [Ship](../docs/TERMS.md#ship) does not re-audit. [Ship](../docs/TERMS.md#ship) authority requires explicit mandate. **[Ship](../docs/TERMS.md#ship) requires UAT greenlight PASS** (when suite applies). No [Ship](../docs/TERMS.md#ship) without greenlight.

9. **Execute-Release:** Follows [Ship](../docs/TERMS.md#ship). Release Conductor executes the release only after [Ship](../docs/TERMS.md#ship) completes. No release without [Ship](../docs/TERMS.md#ship) authorization.

10. **Post-approve cohort:** System remediation follows the same produce→fitness→[audit](../docs/TERMS.md#audit)→UAT→[ship](../docs/TERMS.md#ship)→execute-release path. Instance heal is last -- only after execute-release completes for the system change.

---

## [Handoff](../docs/TERMS.md#handoff) outcomes

| Outcome | Meaning | Evidence |
|---------|---------|----------|
| **PASS** | All [handoff](../docs/TERMS.md#handoff) criteria [met](../docs/TERMS.md#met); work advances to next [boundary](../docs/TERMS.md#boundary) | [Handoff](../docs/TERMS.md#handoff) log with criteria verdicts |
| **[REFUSE](../docs/TERMS.md#refuse)** | Work cannot advance; produce-incomplete or check cannot run | Error log; work returns to prior [boundary](../docs/TERMS.md#boundary) |

There is no:
- `WARN` -- that is a hint, not a [handoff](../docs/TERMS.md#handoff)
- `PROVISIONAL` -- that is "advance now, fix later" (not a handoff)
- `SOFT-PASS` -- that is "close enough" (not a handoff)

---

## Confirmation checklist (Boundary/Handoff-specific)

For changes that add or modify boundaries or handoffs:

- [ ] CB1. [Boundary](../docs/TERMS.md#boundary) owns adjectives (adjectives, preconditions, postconditions stated).
- [ ] CB2. [Boundary](../docs/TERMS.md#boundary) is [default-closed](../docs/TERMS.md#default-closed) (explicit handoff-in and handoff-out).
- [ ] CB3. [Handoff](../docs/TERMS.md#handoff) meets G1--G4 (all-required PASS bar).
- [ ] CB4. [Refuse](../docs/TERMS.md#refuse) criteria stated in the [handoff](../docs/TERMS.md#handoff) tip.
- [ ] CB5. Incomplete-packet fixture documented in the same tip.
- [ ] CB6. Incomplete packet REFUSES under the stated [refuse](../docs/TERMS.md#refuse) criteria.
- [ ] CB7. Incomplete-packet hunt performed when artifact is a Gate/Handoff tip.
- [ ] CB8. No incomplete-packet slips remain (or blocker findings filed).
- [ ] CB9. Role assignments use role names only (no person names in SOP tables).
- [ ] CB10. `handoff_refused` not conflated with `FAIL`.

---

## Cross-references

- [Charter](../docs/TERMS.md#charter) §5.7: Enforcement (gates fail the build)
- [Charter](../docs/TERMS.md#charter) §5.8: Practice [integrity](../docs/TERMS.md#integrity) (zero variance, hard gates)
- [Charter](../docs/TERMS.md#charter) §16: Systems model -- [agent nouns](../docs/TERMS.md#agent-noun), vocabulary mapping
- [Charter](../docs/TERMS.md#charter) §16.1: [Gate](../docs/TERMS.md#gate) ≠ [Audit](../docs/TERMS.md#audit) vocabulary
- [Charter](../docs/TERMS.md#charter) R30: Every prescribed step or [action](../docs/TERMS.md#action) has a hard [gate](../docs/TERMS.md#gate)
- [`GATE.md`](GATE.md): [Gate](../docs/TERMS.md#gate) [noun](../docs/TERMS.md#noun), G1--G4, incomplete-packet hunt
- [`BOUNDED_CONTEXT.md`](BOUNDED_CONTEXT.md): Bounded Context [noun](../docs/TERMS.md#noun) -- living system-as-is knowledge inside a [Boundary](../docs/TERMS.md#boundary)
- [`ACTIONS.md`](ACTIONS.md): [Action](../docs/TERMS.md#action) [noun](../docs/TERMS.md#noun); gated [action](../docs/TERMS.md#action) catalog; nesting [rule](../docs/TERMS.md#rule)
- [`PRINCIPLES.md`](PRINCIPLES.md) P3: Hard gates (complete/incomplete only)
- [`../agents/quality-architect/AGENT.md`](../agents/quality-architect/AGENT.md): Fitness preflight and scoring
- [`../agents/adversarial-auditor/AGENT.md`](../agents/adversarial-auditor/AGENT.md): Adversarial review role
- [`../agents/ship-role/AGENT.md`](../agents/ship-role/AGENT.md): [Ship](../docs/TERMS.md#ship) authority and mandate
- [P-030 (BBA-Bindings)](https://github.com/richardpickett/BBA-Bindings/pull/9): Raise-readiness [refuse](../docs/TERMS.md#refuse) wire
