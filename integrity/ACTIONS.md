# Action

SSOT for the Action noun in Boundary-Based Programming. Actions are named, gated units of work within boundaries.

Rationale: charter §5.8 (practice integrity), R30 (every prescribed step or action has a hard gate). Related: [`GATE.md`](GATE.md), [`BOUNDARY.md`](BOUNDARY.md), [`PRINCIPLES.md`](PRINCIPLES.md) P3 (hard gates).

---

## Definition

An **Action** is a named unit of work that:

1. **Executes through a Gate or Handoff** — no action is paper-only; every action has an enforcement point
2. **Belongs to a Boundary** — the boundary seat that owns the action's laws
3. **Is prescribed** — the action exists in the catalog before it is invoked; ad-hoc work is not an action

Actions connect the pipeline (Plan → Produce → Fitness → Audit → Ship) to specific enforcement points. Charter R30: "Every prescribed step or action has a hard gate whose only outcomes are complete or incomplete, with evidence."

### Action ≠ Task ≠ Step

| Concept | Gated? | Cataloged? | Evidence required? |
|---------|--------|------------|-------------------|
| **Action** | Yes — Gate or Handoff | Yes | Yes |
| Task | No (may be advisory) | Optional | Optional |
| Step | No (may be sub-action) | No | Optional |

**Action ≠ Task.** Tasks are work items in a board or tracker. Actions are named, gated transitions in the pipeline. A task may contain multiple actions; an action is not a task.

---

## Lexicon

### Atomic Action

An **Atomic Action** is an indivisible unit of work that executes through exactly one Gate or Handoff. It either completes or does not — there is no partial execution.

Properties of an atomic action:
- **Single enforcement point** — one Gate or one Handoff
- **Binary outcome** — PASS/REFUSE (for handoffs), PASS/FAIL (for gates), or REFUSE (when check cannot run)
- **No sub-gates** — the action itself is the smallest gated unit

Examples: `preflight-fitness`, `score-fitness`, `refuse-greenlight`, `record-ship-decision`.

### Compound Action

A **Compound Action** is composed of two or more Atomic Actions. It represents a higher-level pipeline stage that spans multiple enforcement points.

Properties of a compound action:
- **Multiple enforcement points** — each constituent atomic action has its own Gate or Handoff
- **Ordered execution** — atomic actions within the compound execute in a defined sequence
- **Complete coverage** — every atomic action must execute; partial execution is incomplete

Examples: `Produce` (includes produce-package, preflight-fitness), `Adversarial-Audit` (includes audit-charter-rules, incomplete-packet-hunt).

### Nesting Rule

**Every Gate in a compound action executes.** No paper-only compounds.

A compound action is not a label for a phase — it is a composition of atomic actions whose gates must all execute. If a compound action is claimed complete but a constituent gate did not run, the compound action is incomplete.

| Compound claim | Gates executed | Outcome |
|----------------|----------------|---------|
| "Produce complete" | produce-package ✓, preflight-fitness ✓ | Complete |
| "Produce complete" | produce-package ✓, preflight-fitness skipped | **Incomplete** |
| "Audit complete" | audit-charter-rules ✓, incomplete-packet-hunt skipped | **Incomplete** |

**Enforcement:** Fitness refuses MET for a compound action when any constituent atomic action is missing evidence. Adversarial audit refuses PASS when any sub-gate was bypassed.

---

## Action Catalog

This catalog names the gated Actions in the BBP pipeline. Each action cites its executing Gate or Handoff, boundary seat, and binder status.

### Pipeline Actions

| Action | Type | Gate/Handoff | Binder | Boundary seat | Evidence |
|--------|------|--------------|--------|---------------|----------|
| **Plan** | Atomic | Plan → Produce handoff | UNWIRED+companion | Plan | Plan exit criteria met; acceptance criteria documented |
| **Bind-ADRs** | Atomic | ADR-binding gate | UNWIRED+companion | Plan | ADR exists with decision and binder |
| **Conduct-RCA** | Atomic | RCA → Raise-Readiness handoff | UNWIRED+companion | Conduct-RCA | Root cause named; investigation complete |
| **Raise-Readiness** | Compound | Raise → HITL Root-Approve handoff (includes P-030 refuse, R3/R4 check) | wired-Bindings ([P-030](https://github.com/richardpickett/BBA-Bindings/pull/9)) | Raise-Readiness | §7 Owner/Path/Verification, R3, R4 present |
| **Produce** | Compound | Produce → Fitness handoff (includes produce-package, SSOT exit evidence) | wired-Bindings ([P-020](https://github.com/richardpickett/BBA-Bindings)) | Produce | Produce package complete; `ssot_leaf_ids` + `ssot_exit_status` |
| **Preflight-Fitness** | Atomic | `handoff_refused` gate (S7) | wired-local (`tools/score-fitness.py`) | Fitness | No `handoff_refused`; package complete |
| **Score-Fitness** | Atomic | Fitness scoring gate | wired-local (`tools/score-fitness.py`) | Fitness | `MET` / `FAIL` with criteria verdicts |
| **Fitness** | Compound | Fitness → Audit handoff (includes preflight + scoring) | wired-local (`tools/score-fitness.py`) | Fitness | `MET` (preflight passed, scoring passed) |
| **Audit-Charter-Rules** | Atomic | Charter-rule audit gate | UNWIRED+companion | Adversarial Audit | Findings report per charter rule |
| **Incomplete-Packet-Hunt** | Atomic | Incomplete-packet gate (GATE.md) | wired-Bindings ([P-030](https://github.com/richardpickett/BBA-Bindings/pull/9)) | Adversarial Audit | No incomplete-packet slips found |
| **Adversarial-Audit** | Compound | Audit → UAT/Promote handoff (includes charter audit + incomplete-packet hunt) | UNWIRED+companion | Adversarial Audit | All audit sub-gates PASS; no unresolved blocker findings |
| **UAT-Greenlight** | Atomic | UAT → Ship handoff | UNWIRED+companion | UAT / Promote Evidence | Suite complete; tip marker match; no soft-green |
| **Ship** | Atomic | Ship decision gate | UNWIRED+companion | Ship | Ship record: who, when, artifact version, findings disposition |
| **Execute-Release** | Atomic | Ship → Execute-Release handoff | UNWIRED+companion | Execute-Release | Ship complete; release preconditions met |
| **Instance-Heal** | Atomic | Execute → Instance Heal handoff | UNWIRED+companion | Instance Heal | Instance verified healthy; rollback confirmed if needed |

### Contribution Actions

| Action | Type | Gate/Handoff | Binder | Boundary seat | Evidence |
|--------|------|--------------|--------|---------------|----------|
| **Contribution/add-X** | Compound | Contribution Gate (TBD) | **UNWIRED — Gate TBD refuse** | Produce | Aligned with CONTRIBUTION.md when tip lands |
| **Contribution-Add-Noun** | Compound | Add-noun gate (includes R1–R9, contract presence) | UNWIRED+companion | Produce | Noun with identity, private state, verbs, invariant tests |
| **Contribution-Add-Goal** | Compound | Add-goal gate (includes R17–R20, fitness checks) | UNWIRED+companion | Produce | Goal with I/O contract, verb-only writes, fitness green |
| **Contribution-Add-Agent-Noun** | Compound | Add-agent-noun gate (includes S1–S6) | UNWIRED+companion | Produce | Agent noun with identity, verbs, handoff-in, completion artifact |
| **Contribution-Add-Audit** | Atomic | Add-audit gate (P5, binding-matrix entry) | wired-local (`tools/audit-binding-matrix.py`) | Produce | Audit definition with binary criteria; matrix row |
| **Contribution-Add-Gate** | Compound | Add-gate gate (includes G1–G4, incomplete-packet fixture) | UNWIRED+companion | Produce | Gate with refuse criteria, fixture, fixture verification |

**Contribution/add-X stub:** This action aligns with the Contribution Gate once `integrity/CONTRIBUTION.md` tip lands. Until then, Gate TBD refuse applies — the action is cataloged by name but its binder is not yet wired.

### Administrative Actions

| Action | Type | Gate/Handoff | Binder | Boundary seat | Evidence |
|--------|------|--------------|--------|---------------|----------|
| **Record-Ship-Decision** | Atomic | Ship record gate (§16.5) | UNWIRED+companion | Ship | Ship record exists with all required fields |
| **Waive-Finding** | Atomic | Waiver gate (finding documented, risk acknowledged) | UNWIRED+companion | Ship | Waiver record: finding, rationale, risk acknowledgement |
| **Escalate-to-HITL** | Atomic | HITL escalation handoff | wired-Bindings ([P-030](https://github.com/richardpickett/BBA-Bindings/pull/9)) | HITL Root-Approve | Escalation packet with readiness evidence |

---

## Nesting Rule Enforcement

### At Fitness

When a compound action is claimed complete, fitness preflight verifies all constituent atomic actions have evidence:

| Compound | Required evidence | Missing any → |
|----------|-------------------|---------------|
| Produce | produce-package, SSOT exit evidence | `handoff_refused` |
| Fitness | preflight PASS, scoring `MET` | `handoff_refused` |
| Adversarial-Audit | charter audit findings, incomplete-packet hunt | Scoring refuses MET |
| Raise-Readiness | §7 fields, R3, R4 | Refuses handoff to HITL |

### At Adversarial Audit

The adversarial auditor verifies no sub-gate was bypassed:

> Did every atomic action in the claimed compound execute?

If any atomic action lacks evidence of gate execution, the adversarial audit returns **FAIL** (incomplete-packet slip via bypassed sub-gate).

---

## Adding Actions to the Catalog

New actions must meet these criteria before catalog entry:

1. **Named** — the action has a unique name in the catalog
2. **Gate/Handoff cited** — a named Gate or Handoff exists; paper-only actions (no Gate name) are refused
3. **Binder status declared** — one of:
   - `wired-local` — binder lives in this repo's `tools/`
   - `wired-Bindings` — binder lives in BBA-Bindings companion repo
   - `UNWIRED+companion` — documented UNWIRED residual with companion tip link
4. **Seated** — the action belongs to a defined Boundary
5. **Evidenced** — execution produces evidence of PASS/FAIL/REFUSE

**Honesty on binder status:** Many pipeline Actions cite Gates/Handoffs whose binders live in BBA-Bindings or are UNWIRED residuals. Catalog rows require a named Gate/Handoff; the binder may be local, companion, or documented UNWIRED. Paper-only entries (no Gate name, no binder status) are refused.

---

## Confirmation Checklist (Action-specific)

For changes that add or modify actions:

- [ ] CA1. Action is named and unique in the catalog.
- [ ] CA2. Action type is specified (atomic or compound).
- [ ] CA3. Executing Gate or Handoff is cited by name (no paper-only).
- [ ] CA4. Boundary seat is identified.
- [ ] CA5. Evidence type is documented.
- [ ] CA6. If compound, all constituent atomic actions are listed.
- [ ] CA7. Nesting rule verified: every sub-gate must execute (no paper-only compounds).
- [ ] CA8. Binder status declared: `wired-local` | `wired-Bindings` | `UNWIRED+companion` (with companion tip link for UNWIRED).

---

## Cross-references

- Charter R30: Every prescribed step or action has a hard gate
- Charter §5.8: Practice integrity (zero variance, hard gates)
- Charter §16: Systems model — agent nouns, vocabulary mapping
- [`GATE.md`](GATE.md): Gate noun, G1–G4, incomplete-packet hunt
- [`BOUNDARY.md`](BOUNDARY.md): Boundary and Handoff nouns, role-bound SOP
- [`PRINCIPLES.md`](PRINCIPLES.md) P3: Hard gates (complete/incomplete only)
- [`binding-matrix.json`](binding-matrix.json): Requirement → audit → binder index
- [`../DESCRIBE.md`](../DESCRIBE.md): Durable project facts
