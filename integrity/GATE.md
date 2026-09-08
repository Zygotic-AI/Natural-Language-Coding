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

**Required outcome:** Any raise-to-Richard readiness gate must FAIL this packet.

**Gate test:** A packet matching the 15855 shape -- missing §7 fields, missing R3, missing R4 -- fails preflight or fitness. The gate does not soft-pass to "address later."

### Fixture verification

Under the hell-yeah bar:
- **G1:** 15855 is incomplete (missing required fields) → must FAIL
- **G2:** §7/R3/R4 checks are machine-checkable (field presence) → refuse-wired
- **G3:** 15855 is the oatmeal; the gate fails it → MET
- **G4:** PASS would require Richard to add §7/R3/R4 → not self-sufficient → must FAIL

**Conclusion:** A gate that would PASS 15855 is not a gate. It is a review point with no enforcement.

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
- **Audit → Ship:** Audit produces findings; ship-role decides if findings block (but audit itself is binary per item).

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
- [ ] CG3. Hell-yeah bar documented (G1–G4 addressed).
- [ ] CG4. Refuse criteria stated in the gate tip.
- [ ] CG5. Oatmeal fixture documented in the same tip.
- [ ] CG6. Oatmeal FAILs under the stated refuse criteria.
- [ ] CG7. Soft-pass hunt performed (adversarial audit of the gate).
- [ ] CG8. No soft-pass paths remain (or blocker findings filed).

---

## Cross-references

- Charter §5.7: Enforcement (fitness checks fail the build)
- Charter §5.8: Practice integrity (zero variance, hard gates)
- Charter §16.1: Vocabulary mapping (Gate = automated enforcement; Audit = role-based review)
- [`PRINCIPLES.md`](PRINCIPLES.md) P3: Hard gates (complete/incomplete only)
- [`../agents/adversarial-auditor/AGENT.md`](../agents/adversarial-auditor/AGENT.md): Adversarial review role
- [`binding-matrix.json`](binding-matrix.json): Requirement → audit → binder index
