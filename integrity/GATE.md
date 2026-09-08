# Gate

SSOT for the Gate noun in Boundary-Based Programming. Gates are automated enforcement mechanisms -- binary, default-closed, machine-checkable.

Rationale: charter §16.1 vocabulary, §5.7 enforcement, §5.8 practice integrity. Related: [`PRINCIPLES.md`](PRINCIPLES.md) P3 (hard gates).

---

## Definition

A **Gate** is a binary checkpoint that blocks work from advancing until the checkpoint criteria are met. Gates are:

1. **Binary** -- outcome is PASS or FAIL only; no partial, provisional, warn-only, or soft-pass
2. **Automated** -- machine-checkable or refuse-wired (if a check cannot run, the gate refuses to open)
3. **Default-closed** -- work does not pass until the gate explicitly opens; incomplete = blocked

Gates exist in code (CI checks, fitness rules) and in the agent pipeline (produce→fitness→audit→ship handoffs). A gate that allows vibes, warn-only, or human judgment in its criteria is not a gate -- it is a review point.

### Gate vs Audit vs Review

| Mechanism | Authority | Output | Binary? |
|-----------|-----------|--------|---------|
| **Gate** | Blocks automatically (CI, fitness) | PASS / FAIL | Yes |
| **Audit** | Produces findings; does not decide ship | Findings report | Yes (per item) |
| **Review** | Human or role judgment | Approval / rejection / comments | Not required |

**Gate ≠ Audit.** Gates block the build. Audits produce findings for a ship-role or human to decide. Both yield binary per-item outcomes, but differ in mechanism: gates are enforcement, audits are adversarial inspection.

**Gate ≠ Human review.** Human reviews may use judgment, suggest improvements, or ask questions. Gates do not deliberate -- they evaluate criteria and return PASS or FAIL.

---

## Hell-Yeah Fitness Bar

A gate is **good** only if it meets the hell-yeah bar:

### G1. Incomplete work cannot PASS

If the artifact is incomplete -- missing required fields, missing SSOT exit evidence, missing produce package -- the gate refuses. There is no "proceed with warnings" or "address in follow-up." Incomplete = FAIL.

### G2. Every required check is machine-checkable or refuse-wired

If a check cannot run (missing input, parser failure, network error), the gate refuses to open. No check may be vibes-only or human-judgment-required in its definition. If human judgment is needed, the gate is actually a review point -- rename it or redesign it.

**Honesty on refuse-wired:** A gate tip must not claim "refuse-wired" for checks whose binders do not yet exist. When binders are absent, document **UNWIRED residual** and cross-link the companion tip that owns the binder. G2 is MET only when refuse surfaces exist and are wired.

### G3. The last oatmeal that reached Richard would FAIL it

Design criterion: the gate must fail realistic bad input. The oatmeal fixture (see below) must document a known-bad case and demonstrate that the gate rejects it.

### G4. PASS does not still need Richard or a human redo

A PASS means the work is ready for the next stage. If PASS requires a human to fix, double-check, or complete something, that is not a PASS -- that is a handoff to review. A true gate PASS is self-sufficient.

---

## Design Rule: Refuse + Oatmeal Fixture in the Same Tip

When designing or documenting a gate, write the **refuse criteria** and the **oatmeal fixture** in the same section. This forces the gate author to:

1. State what the gate refuses (the FAIL conditions)
2. Provide a concrete example (oatmeal) that would FAIL
3. Prove the refuse criteria catch the oatmeal

A gate tip without a documented oatmeal is incomplete. A gate with refuse criteria that do not fail the oatmeal is broken.

---

## Soft-Pass Hunt (Adversarial Half)

The **soft-pass hunt** is the adversarial audit of a gate. The adversarial-auditor role (or a human in that role) asks:

> Can oatmeal still slip the checklist?

If the answer is yes, the gate tip is not MET. The soft-pass hunt does not design remediations -- it finds holes. Fixes belong to the produce role.

**Adversarial auditor role:** See [`../agents/adversarial-auditor/AGENT.md`](../agents/adversarial-auditor/AGENT.md). The auditor produces findings. The auditor does not have ship authority. If the auditor finds soft-pass paths, those are blocker-level findings.

---

## Oatmeal Fixture: 15855

Reference case for raise-to-Richard readiness gates.

**Scenario:** Leaf 15855 was raised to Richard without:
- §7 Preventive action (Owner / Path / Verification)
- Vera readiness R3 (named actionable preventive)
- Vera readiness R4 (self-heal Y/N + future capture Y/N)

**Required outcome:** Any raise-to-Richard readiness gate must FAIL this packet -- at preflight, fitness, **and** adversarial readiness. All raise paths are covered; there is no soft-pass route via "case bars only" or "ship-role decides."

**Gate test:** A packet matching the 15855 shape -- missing §7 fields, missing R3, missing R4 -- fails at every gate in the raise path:
- Preflight refuses handoff (produce incomplete)
- Fitness refuses MET (required fields missing)
- Adversarial readiness refuses PASS (R3+R4 absent)

The gate does not soft-pass to "address later."

### Fixture verification

Under the hell-yeah bar:
- **G1:** 15855 is incomplete (missing required fields) → must FAIL
- **G2:** §7/R3/R4 checks require concrete content validation, not field-presence only (see SP4 below). **Refuse-wired:** raise-to-Richard readiness G2 is MET -- binders exist and are in force on Bindings main ([P-030](https://github.com/richardpickett/BBA-Bindings/pull/9) @ `16104a47`). Binders: worker §7 metric, Vera R3/R4 always-required checklist SSOT, Vale NHR refuse. Skill: [`skills/raise-readiness-refuse.md`](https://github.com/richardpickett/BBA-Bindings/blob/main/skills/raise-readiness-refuse.md). This tip owns refuse criteria and SSOT; Bindings owns the binder.
- **G3:** 15855 is the oatmeal; the gate fails it → MET (by this tip's refuse criteria)
- **G4:** PASS would require Richard to add §7/R3/R4 → not self-sufficient → must FAIL

**Conclusion:** A gate that would PASS 15855 is not a gate. It is a review point with no enforcement.

### Amend oatmeal: 15855 with case bars only

**Scenario:** 15855 amend PASS contained case bars 1--7 but zero R3/R4 rows.

**Required outcome:** FAIL. Case bars are additive; they never replace R3/R4. A Vera readiness checklist with case bars but no R3/R4 is incomplete.

---

## Hard Refuse Criteria: Vera Readiness

### R3 and R4 are always required (SP3)

**R3 (named actionable preventive)** and **R4 (self-heal Y/N + future capture Y/N)** are always required on every Vera readiness checklist. Case-specific bars **add** to R3/R4; they **never replace** R3/R4.

| Condition | Outcome |
|-----------|---------|
| R3 present and concrete, R4 present | Eligible for PASS |
| R3 absent, R4 present | FAIL |
| R3 present, R4 absent | FAIL |
| R3 absent, R4 absent | FAIL |
| Case bars present, R3/R4 absent | FAIL |

**Oatmeal:** 15855 amend PASS (case bars 1--7, zero R3/R4 rows) must FAIL under this criterion.

### R3 must be concrete, not placeholder (SP4)

R3 = **named actionable preventive** at path-level granularity:
- **Owner** -- non-empty, not "TBD", not placeholder
- **Path/Artifact** -- non-empty, not "TBD", not "see later", not placeholder
- **Verification** -- non-empty, not "TBD", not placeholder

Presence of a heading or field with oatmeal text (empty, TBD, placeholder) = FAIL. The same standard applies to §7 Owner/Path/Verification: non-empty and concrete.

| R3 content | Outcome |
|------------|---------|
| Owner: "Jane", Path: "integrity/GATE.md", Verification: "audit A-GATE" | PASS (concrete) |
| Owner: "TBD", Path: "TBD", Verification: "TBD" | FAIL (placeholder) |
| Owner: "", Path: "", Verification: "" | FAIL (empty) |
| Owner: "Jane", Path: "see later", Verification: "later" | FAIL (defer = incomplete) |
| Field heading present, content empty | FAIL (field-presence alone is insufficient) |

**Design note:** Field-presence validation is necessary but not sufficient. Content validation must confirm concrete, actionable values.

---

## Language Split: "Does Not Design Remediations"

Two related statements exist in gate/audit language:

1. **"Does not design remediations"** -- the adversarial auditor finds holes but does not invent fixes. Fixes are produce work.
2. **"No remediate until approve"** -- the producer does not ship without approval; fixes stay in produce until the gate passes.

These statements do **not** waive the requirement for the packet to **name** the preventive change. The packet must declare what will be fixed, who owns it, and how it will be verified. The auditor does not invent this content, but the auditor refuses PASS if the content is missing.

| Statement | Meaning | Does NOT mean |
|-----------|---------|---------------|
| "Does not design remediations" | Auditor finds holes; producer writes fixes | Auditor ignores missing preventive declarations |
| "No remediate until approve" | Don't ship broken; fix then re-gate | Preventive content is optional in the packet |

---

## Gate Outcomes

| Outcome | Meaning | Evidence |
|---------|---------|----------|
| **PASS** | All criteria met; work advances | Gate log with criteria verdicts |
| **FAIL** | One or more criteria not met; work blocked | Gate log listing failures |
| **REFUSE** | Gate cannot evaluate (missing input, check failed to run) | Error log; default-closed |

There is no:
- `WARN` -- that is a hint, not a gate
- `PROVISIONAL` -- that is "ship now, fix later" (not a gate)
- `SOFT-PASS` -- that is "close enough" (not a gate)
- `NEEDS-REVIEW` -- that is a handoff to human judgment (not a gate)

---

## Applying Gates in BBP

### Code / CI gates

- Fitness checks (R23, R24) block PRs if violated
- Contract presence checks (§12.5) block if schema missing
- Binding matrix audits (P6, P7) block if unbound in-force requirements exist

### Pipeline gates

- **Produce → Fitness:** Default-closed (S7). Incomplete produce package → `handoff_refused`.
- **Fitness → Audit:** Fitness must score MET before adversarial audit opens (handoff-in for adversarial-auditor).
- **Audit → Ship:** Audit produces findings; ship-role decides if findings block (but audit itself is binary per item). **Exception:** Adversarial readiness PASS requires R3+R4; missing R3 or R4 → adversarial audit refuses PASS and returns FAIL readiness. Ship-role cannot soft-pass missing R3/R4 -- the audit gate closes before ship-role sees the packet.

**Soft-pass path closed:** The route "fitness skips → Vera case-bars-only → raise" is blocked. Adversarial readiness checks R3+R4 presence and content; missing or placeholder → FAIL. There is no path to Richard that bypasses this gate.

### SSOT exit evidence (S8, P-020)

Every produce package must include `ssot_leaf_ids` and `ssot_exit_status`. Missing evidence:
- Triggers `handoff_refused` at produce→fitness boundary
- Causes fitness to refuse MET
- Causes adversarial audit to refuse PASS

This is a gate, not a suggestion.

---

## Confirmation Checklist (Gate-specific)

For changes that add or modify gates:

- [ ] CG1. Gate criteria are binary (PASS/FAIL only).
- [ ] CG2. Gate is default-closed (refuse if check cannot run).
- [ ] CG3. Hell-yeah bar documented (G1--G4 addressed).
- [ ] CG4. Refuse criteria stated in the gate tip.
- [ ] CG5. Oatmeal fixture documented in the same tip.
- [ ] CG6. Oatmeal FAILs under the stated refuse criteria.
- [ ] CG7. Soft-pass hunt performed (adversarial audit of the gate).
- [ ] CG8. No soft-pass paths remain (or blocker findings filed).
- [ ] CG9. Binder status honest: refuse-wired claimed only when binders exist; UNWIRED residual documented otherwise.
- [ ] CG10. Adversarial readiness binds refuse (not fitness-only); all raise paths covered.
- [ ] CG11. Always-required items (R3/R4) cannot be replaced by case bars.
- [ ] CG12. Content validation required, not field-presence only; TBD/placeholder = FAIL.

---

## Cross-references

- Charter §5.7: Enforcement (fitness checks fail the build)
- Charter §5.8: Practice integrity (zero variance, hard gates)
- Charter §16.1: Vocabulary mapping (Gate = automated enforcement; Audit = role-based review)
- [`PRINCIPLES.md`](PRINCIPLES.md) P3: Hard gates (complete/incomplete only)
- [`../agents/adversarial-auditor/AGENT.md`](../agents/adversarial-auditor/AGENT.md): Adversarial review role
- [`binding-matrix.json`](binding-matrix.json): Requirement → audit → binder index
