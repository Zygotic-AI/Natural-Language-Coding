# [Action](../docs/TERMS.md#action)

SSOT for the [Action](../docs/TERMS.md#action) [noun](../docs/TERMS.md#noun) in [Boundary-Based Programming](../docs/TERMS.md#bbp). Actions are named, gated units of work within boundaries.

Rationale: [charter](../docs/TERMS.md#charter) §5.8 (practice integrity), R30 (every prescribed step or action has a hard gate). Related: [`GATE.md`](GATE.md), [`BOUNDARY.md`](BOUNDARY.md), [`PRINCIPLES.md`](PRINCIPLES.md) P3 (hard gates).

---

## Definition

An **[Action](../docs/TERMS.md#action)** is a named unit of work that:

1. **Executes through a [Gate](../docs/TERMS.md#gate) or [Handoff](../docs/TERMS.md#handoff)** — no [action](../docs/TERMS.md#action) is paper-only; every [action](../docs/TERMS.md#action) has an enforcement point
2. **Belongs to a [Boundary](../docs/TERMS.md#boundary)** — the [boundary](../docs/TERMS.md#boundary) seat that owns the [action](../docs/TERMS.md#action)'s adjectives
3. **Is prescribed** — the [action](../docs/TERMS.md#action) exists in the catalog before it is invoked; ad-hoc work is not an [action](../docs/TERMS.md#action)

Actions connect the pipeline (Plan → Produce → Fitness → Audit → Ship) to specific enforcement points. [Charter](../docs/TERMS.md#charter) R30: "Every prescribed step or [action](../docs/TERMS.md#action) has a hard [gate](../docs/TERMS.md#gate) whose only outcomes are complete or incomplete, with evidence."

### [Action](../docs/TERMS.md#action) ≠ Task ≠ Step

| Concept | Gated? | Cataloged? | Evidence required? |
|---------|--------|------------|-------------------|
| **[Action](../docs/TERMS.md#action)** | Yes — [Gate](../docs/TERMS.md#gate) or [Handoff](../docs/TERMS.md#handoff) | Yes | Yes |
| Task | No (may be advisory) | Optional | Optional |
| Step | No (may be sub-action) | No | Optional |

**[Action](../docs/TERMS.md#action) ≠ Task.** Tasks are work items in a board or tracker. Actions are named, gated transitions in the pipeline. A task may contain multiple actions; an [action](../docs/TERMS.md#action) is not a task.

---

## Lexicon

### [Atomic Action](../docs/TERMS.md#atomic-action)

An **[Atomic Action](../docs/TERMS.md#atomic-action)** is an indivisible unit of work that executes through exactly one [Gate](../docs/TERMS.md#gate) or [Handoff](../docs/TERMS.md#handoff). It either completes or does not — there is no partial execution.

Properties of an [atomic action](../docs/TERMS.md#atomic-action):
- **Single enforcement point** — one [Gate](../docs/TERMS.md#gate) or one [Handoff](../docs/TERMS.md#handoff)
- **Binary outcome** — PASS/REFUSE (for handoffs), PASS/FAIL (for gates), or [REFUSE](../docs/TERMS.md#refuse) (when check cannot run)
- **No sub-gates** — the [action](../docs/TERMS.md#action) itself is the smallest gated unit

Examples: `preflight-fitness`, `score-fitness`, `refuse-greenlight`, `record-ship-decision`.

### [Compound Action](../docs/TERMS.md#compound-action)

A **[Compound Action](../docs/TERMS.md#compound-action)** is composed of two or more Atomic Actions. It represents a higher-level pipeline stage that spans multiple enforcement points.

Properties of a [compound action](../docs/TERMS.md#compound-action):
- **Multiple enforcement points** — each constituent [atomic action](../docs/TERMS.md#atomic-action) has its own [Gate](../docs/TERMS.md#gate) or [Handoff](../docs/TERMS.md#handoff)
- **Ordered execution** — atomic actions within the compound execute in a defined sequence
- **Complete coverage** — every [atomic action](../docs/TERMS.md#atomic-action) must execute; partial execution is incomplete

Examples: `Produce` (includes produce-package, preflight-fitness), `Adversarial-Audit` (includes audit-charter-rules, incomplete-packet-hunt).

### Nesting [Rule](../docs/TERMS.md#rule)

**Every [Gate](../docs/TERMS.md#gate) in a [compound action](../docs/TERMS.md#compound-action) executes.** No paper-only compounds.

A [compound action](../docs/TERMS.md#compound-action) is not a label for a phase — it is a composition of atomic actions whose gates must all execute. If a [compound action](../docs/TERMS.md#compound-action) is claimed complete but a constituent [gate](../docs/TERMS.md#gate) did not run, the [compound action](../docs/TERMS.md#compound-action) is incomplete.

| Compound claim | Gates executed | Outcome |
|----------------|----------------|---------|
| "Produce complete" | produce-package ✓, preflight-fitness ✓ | Complete |
| "Produce complete" | produce-package ✓, preflight-fitness skipped | **Incomplete** |
| "[Audit](../docs/TERMS.md#audit) complete" | audit-charter-rules ✓, incomplete-packet-hunt skipped | **Incomplete** |

**Enforcement:** Fitness refuses [MET](../docs/TERMS.md#met) for a [compound action](../docs/TERMS.md#compound-action) when any constituent [atomic action](../docs/TERMS.md#atomic-action) is missing evidence. Adversarial [audit](../docs/TERMS.md#audit) refuses PASS when any sub-gate was bypassed.

---

## [Action](../docs/TERMS.md#action) Catalog

This catalog names the gated Actions in the [BBP](../docs/TERMS.md#bbp) pipeline. Each [action](../docs/TERMS.md#action) cites its executing [Gate](../docs/TERMS.md#gate) or [Handoff](../docs/TERMS.md#handoff), [boundary](../docs/TERMS.md#boundary) seat, and binder status.

### Pipeline Actions

| [Action](../docs/TERMS.md#action) | Type | Gate/Handoff | Binder | [Boundary](../docs/TERMS.md#boundary) seat | Evidence |
|--------|------|--------------|--------|---------------|----------|
| **Plan** | Atomic | Plan → Produce [handoff](../docs/TERMS.md#handoff) | UNWIRED+companion | Plan | Plan exit criteria [met](../docs/TERMS.md#met); acceptance criteria documented |
| **Bind-ADRs** | Atomic | ADR-binding [gate](../docs/TERMS.md#gate) | UNWIRED+companion | Plan | [ADR](../docs/TERMS.md#adr) exists with decision and binder |
| **Conduct-RCA** | Atomic | [RCA](../docs/TERMS.md#rca) → Raise-Readiness [handoff](../docs/TERMS.md#handoff) | UNWIRED+companion | Conduct-RCA | Root cause named; investigation complete |
| **Raise-Readiness** | Compound | Raise → HITL Root-Approve [handoff](../docs/TERMS.md#handoff) (includes P-030 refuse, R3/R4 check) | wired-Bindings ([P-030](https://github.com/richardpickett/BBA-Bindings/pull/9)) | Raise-Readiness | §7 Owner/Path/Verification, R3, R4 present |
| **Produce** | Compound | Produce → Fitness [handoff](../docs/TERMS.md#handoff) (includes produce-package, SSOT exit evidence) | wired-Bindings ([P-020](https://github.com/richardpickett/BBA-Bindings)) | Produce | [Produce package](../docs/TERMS.md#produce-package) complete; `ssot_leaf_ids` + `ssot_exit_status` |
| **Preflight-Fitness** | Atomic | `handoff_refused` [gate](../docs/TERMS.md#gate) (S7) | wired-local (`tools/score-fitness.py`) | Fitness | No `handoff_refused`; package complete |
| **Score-Fitness** | Atomic | Fitness scoring [gate](../docs/TERMS.md#gate) | wired-local (`tools/score-fitness.py`) | Fitness | `MET` / `FAIL` with criteria verdicts |
| **Fitness** | Compound | Fitness → [Audit](../docs/TERMS.md#audit) [handoff](../docs/TERMS.md#handoff) (includes preflight + scoring) | wired-local (`tools/score-fitness.py`) | Fitness | `MET` (preflight passed, scoring passed) |
| **Audit-Charter-Rules** | Atomic | Charter-rule [audit](../docs/TERMS.md#audit) [gate](../docs/TERMS.md#gate) | UNWIRED+companion | Adversarial [Audit](../docs/TERMS.md#audit) | Findings report per [charter](../docs/TERMS.md#charter) [rule](../docs/TERMS.md#rule) |
| **Incomplete-Packet-Hunt** | Atomic | Incomplete-packet [gate](../docs/TERMS.md#gate) (GATE.md) | wired-Bindings ([P-030](https://github.com/richardpickett/BBA-Bindings/pull/9)) | Adversarial [Audit](../docs/TERMS.md#audit) | No incomplete-packet slips found |
| **Adversarial-Audit** | Compound | [Audit](../docs/TERMS.md#audit) → UAT/Promote [handoff](../docs/TERMS.md#handoff) (includes charter audit + incomplete-packet hunt) | UNWIRED+companion | Adversarial [Audit](../docs/TERMS.md#audit) | All [audit](../docs/TERMS.md#audit) sub-gates PASS; no unresolved blocker findings |
| **UAT-Greenlight** | Atomic | UAT → [Ship](../docs/TERMS.md#ship) [handoff](../docs/TERMS.md#handoff) | UNWIRED+companion | UAT / Promote Evidence | Suite complete; tip marker match; no soft-green |
| **[Ship](../docs/TERMS.md#ship)** | Atomic | [Ship](../docs/TERMS.md#ship) decision [gate](../docs/TERMS.md#gate) | UNWIRED+companion | [Ship](../docs/TERMS.md#ship) | [Ship](../docs/TERMS.md#ship) record: who, when, artifact version, findings disposition |
| **Execute-Release** | Atomic | [Ship](../docs/TERMS.md#ship) → Execute-Release [handoff](../docs/TERMS.md#handoff) | UNWIRED+companion | Execute-Release | [Ship](../docs/TERMS.md#ship) complete; release preconditions [met](../docs/TERMS.md#met) |
| **Instance-Heal** | Atomic | Execute → Instance Heal [handoff](../docs/TERMS.md#handoff) | UNWIRED+companion | Instance Heal | Instance verified healthy; rollback confirmed if needed |

### Contribution Actions

| [Action](../docs/TERMS.md#action) | Type | Gate/Handoff | Binder | [Boundary](../docs/TERMS.md#boundary) seat | Evidence |
|--------|------|--------------|--------|---------------|----------|
| **Contribution/add-X** | Compound | [Contribution Gate](../docs/TERMS.md#contribution-gate) (TBD) | **UNWIRED — [Gate](../docs/TERMS.md#gate) TBD [refuse](../docs/TERMS.md#refuse)** | Produce | Aligned with CONTRIBUTION.md when tip lands |
| **Contribution-Add-Noun** | Compound | Add-noun [gate](../docs/TERMS.md#gate) (includes R1–R9, contract presence) | UNWIRED+companion | Produce | [Noun](../docs/TERMS.md#noun) with identity, private state, verbs, [adjective](../docs/TERMS.md#adjective) tests |
| **Contribution-Add-Goal** | Compound | Add-goal [gate](../docs/TERMS.md#gate) (includes R17–R20, fitness checks) | UNWIRED+companion | Produce | [Goal](../docs/TERMS.md#goal) with I/O [contract](../docs/TERMS.md#contract), verb-only writes, fitness green |
| **Contribution-Add-Agent-Noun** | Compound | Add-agent-noun [gate](../docs/TERMS.md#gate) (includes S1–S6) | UNWIRED+companion | Produce | [Agent noun](../docs/TERMS.md#agent-noun) with identity, verbs, handoff-in, completion artifact |
| **Contribution-Add-Audit** | Atomic | Add-audit [gate](../docs/TERMS.md#gate) (P5, binding-matrix entry) | wired-local (`tools/audit-binding-matrix.py`) | Produce | [Audit](../docs/TERMS.md#audit) definition with binary criteria; matrix row |
| **Contribution-Add-Gate** | Compound | Add-gate [gate](../docs/TERMS.md#gate) (includes G1–G4, incomplete-packet fixture) | UNWIRED+companion | Produce | [Gate](../docs/TERMS.md#gate) with [refuse](../docs/TERMS.md#refuse) criteria, fixture, fixture verification |

**Contribution/add-X stub:** This [action](../docs/TERMS.md#action) aligns with the [Contribution Gate](../docs/TERMS.md#contribution-gate) once `integrity/CONTRIBUTION.md` tip lands. Until then, [Gate](../docs/TERMS.md#gate) TBD [refuse](../docs/TERMS.md#refuse) applies — the [action](../docs/TERMS.md#action) is cataloged by name but its binder is not yet wired.

### Administrative Actions

| [Action](../docs/TERMS.md#action) | Type | Gate/Handoff | Binder | [Boundary](../docs/TERMS.md#boundary) seat | Evidence |
|--------|------|--------------|--------|---------------|----------|
| **Record-Ship-Decision** | Atomic | [Ship](../docs/TERMS.md#ship) record [gate](../docs/TERMS.md#gate) (§16.5) | UNWIRED+companion | [Ship](../docs/TERMS.md#ship) | [Ship](../docs/TERMS.md#ship) record exists with all required fields |
| **Waive-Finding** | Atomic | Waiver [gate](../docs/TERMS.md#gate) (finding documented, risk acknowledged) | UNWIRED+companion | [Ship](../docs/TERMS.md#ship) | Waiver record: finding, rationale, risk acknowledgement |
| **Escalate-to-HITL** | Atomic | HITL escalation [handoff](../docs/TERMS.md#handoff) | wired-Bindings ([P-030](https://github.com/richardpickett/BBA-Bindings/pull/9)) | HITL Root-Approve | Escalation packet with readiness evidence |

---

## Nesting [Rule](../docs/TERMS.md#rule) Enforcement

### At Fitness

When a [compound action](../docs/TERMS.md#compound-action) is claimed complete, fitness preflight verifies all constituent atomic actions have evidence:

| Compound | Required evidence | Missing any → |
|----------|-------------------|---------------|
| Produce | produce-package, [SSOT exit evidence](../docs/TERMS.md#ssot-exit-evidence) | `handoff_refused` |
| Fitness | preflight PASS, scoring `MET` | `handoff_refused` |
| Adversarial-Audit | [charter](../docs/TERMS.md#charter) [audit](../docs/TERMS.md#audit) findings, incomplete-packet hunt | Scoring refuses [MET](../docs/TERMS.md#met) |
| Raise-Readiness | §7 fields, R3, R4 | Refuses [handoff](../docs/TERMS.md#handoff) to HITL |

### At Adversarial [Audit](../docs/TERMS.md#audit)

The adversarial auditor verifies no sub-gate was bypassed:

> Did every [atomic action](../docs/TERMS.md#atomic-action) in the claimed compound execute?

If any [atomic action](../docs/TERMS.md#atomic-action) lacks evidence of [gate](../docs/TERMS.md#gate) execution, the adversarial [audit](../docs/TERMS.md#audit) returns **FAIL** (incomplete-packet slip via bypassed sub-gate).

---

## Adding Actions to the Catalog

New actions must meet these criteria before catalog entry:

1. **Named** — the [action](../docs/TERMS.md#action) has a unique name in the catalog
2. **Gate/Handoff cited** — a named [Gate](../docs/TERMS.md#gate) or [Handoff](../docs/TERMS.md#handoff) exists; paper-only actions (no Gate name) are refused
3. **Binder status declared** — one of:
   - `wired-local` — binder lives in this repo's `tools/`
   - `wired-Bindings` — binder lives in [BBA-Bindings](../docs/TERMS.md#bba-bindings) companion repo
   - `UNWIRED+companion` — documented UNWIRED residual with companion tip link
4. **Seated** — the [action](../docs/TERMS.md#action) belongs to a defined [Boundary](../docs/TERMS.md#boundary)
5. **Evidenced** — execution produces evidence of PASS/FAIL/REFUSE

**Honesty on binder status:** Many pipeline Actions cite Gates/Handoffs whose binders live in [BBA-Bindings](../docs/TERMS.md#bba-bindings) or are UNWIRED residuals. Catalog rows require a named Gate/Handoff; the binder may be local, companion, or documented UNWIRED. Paper-only entries (no Gate name, no binder status) are refused.

---

## Confirmation Checklist (Action-specific)

For changes that add or modify actions:

- [ ] CA1. [Action](../docs/TERMS.md#action) is named and unique in the catalog.
- [ ] CA2. [Action](../docs/TERMS.md#action) type is specified (atomic or compound).
- [ ] CA3. Executing [Gate](../docs/TERMS.md#gate) or [Handoff](../docs/TERMS.md#handoff) is cited by name (no paper-only).
- [ ] CA4. [Boundary](../docs/TERMS.md#boundary) seat is identified.
- [ ] CA5. Evidence type is documented.
- [ ] CA6. If compound, all constituent atomic actions are listed.
- [ ] CA7. Nesting [rule](../docs/TERMS.md#rule) verified: every sub-gate must execute (no paper-only compounds).
- [ ] CA8. Binder status declared: `wired-local` | `wired-Bindings` | `UNWIRED+companion` (with companion tip link for UNWIRED).

---

## Cross-references

- [Charter](../docs/TERMS.md#charter) R30: Every prescribed step or [action](../docs/TERMS.md#action) has a hard [gate](../docs/TERMS.md#gate)
- [Charter](../docs/TERMS.md#charter) §5.8: Practice [integrity](../docs/TERMS.md#integrity) (zero variance, hard gates)
- [Charter](../docs/TERMS.md#charter) §16: Systems model — [agent nouns](../docs/TERMS.md#agent-noun), vocabulary mapping
- [`GATE.md`](GATE.md): [Gate](../docs/TERMS.md#gate) [noun](../docs/TERMS.md#noun), [G1–G4](../docs/TERMS.md#g1g4), incomplete-packet hunt
- [`BOUNDARY.md`](BOUNDARY.md): [Boundary](../docs/TERMS.md#boundary) and [Handoff](../docs/TERMS.md#handoff) nouns, role-bound SOP
- [`PRINCIPLES.md`](PRINCIPLES.md) P3: Hard gates (complete/incomplete only)
- [`binding-matrix.json`](binding-matrix.json): [Requirement](../docs/TERMS.md#requirement) → [audit](../docs/TERMS.md#audit) → [gate](../docs/TERMS.md#gate) (JSON key remains `binder` until the auditor is updated)
- [`../DESCRIBE.md`](../DESCRIBE.md): Durable project facts
