# Boundary

SSOT for the Boundary and Handoff nouns in Boundary-Based Programming. Boundaries own laws for a stage; handoffs are refuse-wired gates between Boundaries.

Rationale: charter §16 vocabulary, §5.8 practice integrity. Related: [`GATE.md`](GATE.md), [`PRINCIPLES.md`](PRINCIPLES.md) P3 (hard gates).

---

## Definition

A **Boundary** is a named stage in a work pipeline that:

1. **Owns laws** -- the invariants, preconditions, and postconditions that govern what may happen at this stage
2. **Is default-closed** -- work does not enter or exit until handoff criteria are met
3. **Produces a binary advance** -- work either advances to the next boundary or does not; no partial progress

Boundaries exist in code (noun modules, goal entrypoints) and in the agent pipeline (produce, fitness, audit, ship). A boundary without an exit handoff is a dead end; a boundary with a soft exit is not a boundary.

### Boundary ≠ Phase ≠ Checkpoint

| Concept | Owns laws? | Binary advance? | Has handoff? |
|---------|------------|-----------------|--------------|
| **Boundary** | Yes | Yes | Required |
| Phase | No (convenience grouping) | No | Optional |
| Checkpoint | Partially (may be advisory) | Sometimes | Sometimes |

**Boundary ≠ Phase.** Phases are convenience groupings for project management. Boundaries own the laws of what happens inside them and enforce binary advance at exit.

---

## Handoff

A **Handoff** is a refuse-wired gate between two Boundaries. Every handoff must meet the Gate fitness bar (G1--G4).

### Handoff requirements

| Requirement | Meaning |
|-------------|---------|
| **G1. Incomplete cannot PASS** | If the artifact is incomplete -- missing required fields, missing SSOT exit evidence, missing produce package -- the handoff refuses. No "proceed with warnings." |
| **G2. Machine-checkable or refuse-wired** | If a check cannot run (missing input, parser failure, network error), the handoff refuses. No vibes-only checks. |
| **G3. Incomplete-packet fixture fails** | The handoff must fail realistic bad input. The incomplete-packet fixture documents a known-bad case and proves the handoff rejects it. |
| **G4. PASS needs no human redo** | A PASS means work is ready for the next boundary. If PASS requires a human to fix, double-check, or complete something, that is not a PASS. |

### Handoff ≠ Review

| Mechanism | Authority | Output | Owns laws? |
|-----------|-----------|--------|------------|
| **Handoff** | Refuses automatically | PASS / REFUSE | Yes -- G1--G4 |
| Review | Human or role judgment | Approval / comments | No |

**Handoff refused ≠ fitness FAIL.** When a handoff refuses (`handoff_refused`), that is a produce-incomplete signal, not a content defect. The Gate remains the CI enforcement point for fitness scoring; handoff refusal is upstream of Gate. Do not conflate `handoff_refused` with `FAIL`.

### Design rule: refuse + incomplete-packet fixture in same tip

When designing or documenting a handoff, write the **refuse criteria** and the **incomplete-packet fixture** in the same section. This forces the handoff author to:

1. State what the handoff refuses (the REFUSE conditions)
2. Provide a concrete example (incomplete packet) that would REFUSE
3. Prove the refuse criteria catch the incomplete packet

A handoff tip without a documented incomplete-packet fixture is incomplete.

---

## Incomplete-packet fixture: 15855 without §7/R3/R4

Reference case for handoffs in the raise-to-Richard path.

**Scenario:** Leaf 15855 was raised without:
- §7 Preventive action (Owner / Path / Verification)
- R3 (named actionable preventive)
- R4 (self-heal Y/N + future capture Y/N)

**Required outcome:** Any raise-readiness handoff must REFUSE this packet at every boundary:
- Produce → Fitness: `handoff_refused` (produce incomplete)
- Fitness → Audit: refuses MET (required fields missing)
- Audit → Ship: refuses PASS (R3+R4 absent)

**Fixture verification under G1--G4:**

| Criterion | Evidence |
|-----------|----------|
| G1 | 15855 is incomplete (missing required fields) → must REFUSE |
| G2 | §7/R3/R4 checks require concrete content validation; **refuse-wired** via [P-030](https://github.com/richardpickett/BBA-Bindings/pull/9) on Bindings main |
| G3 | 15855 is the incomplete-packet fixture; handoff refuses it → MET |
| G4 | PASS would require Human root-approver to add §7/R3/R4 → not self-sufficient → must REFUSE |

**Conclusion:** A handoff that would PASS 15855 is not a handoff. It is a review point with no enforcement.

### Amend fixture: 15855 with case bars only

**Scenario:** 15855 amend PASS contained case bars 1--7 but zero R3/R4 rows.

**Required outcome:** REFUSE. Case bars are additive; they never replace R3/R4. A readiness checklist with case bars but no R3/R4 is incomplete.

---

## Soft-pass hunt (adversarial half)

When an artifact defines a Gate or Handoff tip, the adversarial audit includes a **soft-pass hunt**:

> Can an incomplete packet still slip the checklist?

If the answer is yes, the handoff tip is not MET. The soft-pass hunt does not design remediations -- it finds holes. Fixes belong to the produce role. See [`GATE.md`](GATE.md) § Soft-Pass Hunt.

**Adversarial auditor role:** See [`../agents/adversarial-auditor/AGENT.md`](../agents/adversarial-auditor/AGENT.md). The auditor produces findings. The auditor does not have ship authority. If the auditor finds soft-pass paths, those are blocker-level findings.

---

## Role-bound SOP: Boundaries and Handoffs

This SOP maps boundaries in the work pipeline to roles. Roles are organizational positions; person names do not appear.

### Role glossary

| Role | Purpose |
|------|---------|
| **Plan Steward** | Owns the plan boundary; ensures plan exit criteria are met before work enters produce |
| **RCA Conductor** | Conducts root-cause analysis; raises readiness evidence to meet P-030 bar |
| **Producer** | Creates change artifacts (code tip, standard tip, design tip); owns produce package completion |
| **Quality Architect** | Gates fitness preflight and scoring; refuses incomplete handoffs; does not have ship authority |
| **Adversarial Auditor** | Attacks artifacts against charter; produces findings; does not have ship authority |
| **Defect Remediator** | Fixes defects identified by Quality Architect or Adversarial Auditor; re-gates after fix |
| **Release Conductor** | Orchestrates the ship boundary; coordinates merge, release, deploy |
| **Ship Role** | Authorizes release (ratify, merge, release verbs); requires explicit mandate |
| **Escalation Steward** | Handles escalation paths when handoffs cannot advance; owns unblock decisions |
| **Human Root-Approver** | HITL root-approve authority for decisions that exceed agent mandate |
| **UAT Conductor** | Owns UAT boundary; refuses soft-green promotion evidence |

### Boundary flow

```text
Plan ─┬─→ Produce ──→ Fitness ──→ Audit ──→ Ship ──→ UAT/Promote
      │
      └─→ Conduct-RCA ──→ Raise-Readiness (P-030/R3+R4)
                              │
                              └─→ (rejoins Produce when readiness MET)
```

Post-approve cohort (system change path):
```text
System-Remediate Design ──→ Produce ──→ Fitness ──→ Audit ──→ Ship ──→ Instance Heal
```

### Boundary × Role × Handoff map

| # | Boundary | Role(s) | Handoff-out | Refuse criteria | Incomplete-packet fixture |
|---|----------|---------|-------------|-----------------|---------------------------|
| 1 | **Plan** | Plan Steward | Plan → Produce | *Off Gate noun until refuse-wired plan exit exists* | (future: plan without acceptance criteria) |
| 2 | **Conduct-RCA** | RCA Conductor | RCA → Raise-Readiness | Investigation incomplete; no root cause named | RCA report without root cause statement |
| 3 | **Raise-Readiness** | RCA Conductor, Quality Architect | Raise → Produce | Missing §7 (Owner/Path/Verification), missing R3, missing R4; see [P-030](https://github.com/richardpickett/BBA-Bindings/pull/9) | **15855 without §7/R3/R4** |
| 4 | **Produce** (code or standard tip) | Producer | Produce → Fitness | Missing produce package; missing SSOT exit evidence (S7, S8) | Package without `ssot_leaf_ids` + `ssot_exit_status` |
| 5 | **Fitness** | Quality Architect | Fitness → Audit | Preflight `handoff_refused`; scoring not MET | Produce package incomplete → `handoff_refused` (not FAIL) |
| 6 | **Adversarial Audit** | Adversarial Auditor | Audit → Ship | Unresolved blocker findings; soft-pass hunt positive | Audit with unrebutted charter-rule violation |
| 7 | **Ship** | Ship Role, Release Conductor | Ship → UAT/Promote | No mandate; pipeline not complete; findings not addressed | Ship request without audit completion record |
| 8 | **UAT / Promote Evidence** | UAT Conductor | UAT → Production | Soft-green evidence; no binary acceptance | Promotion request with "mostly passing" evidence |
| 9 | **System-Remediate Design** | Producer, Quality Architect | Design → Produce | Design incomplete; no boundary I/O declared | Design doc without input/output/failure mode |
| 10 | **Instance Heal** | Release Conductor, Defect Remediator | Heal → Done | Instance not verified healthy; rollback not confirmed | Heal report without verification evidence |

### Notes on boundary distinctions

1. **Plan boundary:** Currently off Gate noun until a refuse-wired plan exit is implemented. Plan Steward owns completeness criteria; handoff to Produce is manual until binder exists.

2. **Conduct-RCA → Raise-Readiness:** This is not code Produce. RCA work feeds the readiness gate (P-030 / R3+R4) before code work begins. Quality Architect gates the Raise-Readiness handoff.

3. **Produce boundary:** Same machinery for code tip, standard tip, or design tip. Producer owns produce package; Quality Architect refuses incomplete handoffs at fitness preflight.

4. **Fitness outcomes:** `MET` / `FAIL` / `handoff_refused`. The `handoff_refused` outcome is upstream of content scoring -- it means produce-incomplete, not content-defective. Do not normalize "re-gate" language for `handoff_refused`; that masks the produce-handoff defect.

5. **Adversarial audit:** Audit ≠ Gate ≠ Review. Auditors produce findings; they do not have ship authority. When the artifact is a Gate tip or Handoff tip, adversarial audit includes the soft-pass hunt.

6. **Ship boundary:** Ship is a decision, not a review. Ship Role decides whether audit findings block release. Ship does not re-audit. Ship authority requires explicit mandate.

7. **UAT / Promote Evidence:** Own verb boundary. Refuses soft-green promotion evidence (e.g., "80% passing is close enough"). Binary acceptance required.

8. **Post-approve cohort:** System remediation follows the same produce→fitness→audit→ship path. Instance heal is last -- only after ship completes for the system change.

---

## Handoff outcomes

| Outcome | Meaning | Evidence |
|---------|---------|----------|
| **PASS** | All handoff criteria met; work advances to next boundary | Handoff log with criteria verdicts |
| **REFUSE** | Work cannot advance; produce-incomplete or check cannot run | Error log; work returns to prior boundary |

There is no:
- `WARN` -- that is a hint, not a handoff
- `PROVISIONAL` -- that is "advance now, fix later" (not a handoff)
- `SOFT-PASS` -- that is "close enough" (not a handoff)

---

## Confirmation checklist (Boundary/Handoff-specific)

For changes that add or modify boundaries or handoffs:

- [ ] CB1. Boundary owns laws (invariants, preconditions, postconditions stated).
- [ ] CB2. Boundary is default-closed (explicit handoff-in and handoff-out).
- [ ] CB3. Handoff meets G1--G4 (all-required PASS bar).
- [ ] CB4. Refuse criteria stated in the handoff tip.
- [ ] CB5. Incomplete-packet fixture documented in the same tip.
- [ ] CB6. Incomplete packet REFUSES under the stated refuse criteria.
- [ ] CB7. Soft-pass hunt performed when artifact is a Gate/Handoff tip.
- [ ] CB8. No soft-pass paths remain (or blocker findings filed).
- [ ] CB9. Role assignments use role names only (no person names in SOP tables).
- [ ] CB10. `handoff_refused` not conflated with `FAIL`.

---

## Cross-references

- Charter §5.7: Enforcement (fitness checks fail the build)
- Charter §5.8: Practice integrity (zero variance, hard gates)
- Charter §16: Systems model -- agent nouns, vocabulary mapping
- Charter §16.1: Gate ≠ Audit vocabulary
- [`GATE.md`](GATE.md): Gate noun, G1--G4, soft-pass hunt
- [`PRINCIPLES.md`](PRINCIPLES.md) P3: Hard gates (complete/incomplete only)
- [`../agents/quality-architect/AGENT.md`](../agents/quality-architect/AGENT.md): Fitness preflight and scoring
- [`../agents/adversarial-auditor/AGENT.md`](../agents/adversarial-auditor/AGENT.md): Adversarial review role
- [`../agents/ship-role/AGENT.md`](../agents/ship-role/AGENT.md): Ship authority and mandate
- [P-030 (BBA-Bindings)](https://github.com/richardpickett/BBA-Bindings/pull/9): Raise-readiness refuse wire binder
