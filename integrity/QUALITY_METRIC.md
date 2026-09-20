# [Quality](../docs/TERMS.md#quality) Metric

SSOT for the [Quality](../docs/TERMS.md#quality) metric in [Boundary-Based Programming](../docs/TERMS.md#bbp). [Quality](../docs/TERMS.md#quality) measures ops versus defects across agent processes — a binary count, not a continuous score.

Rationale: [charter](../docs/TERMS.md#charter) §16.2 success criteria, §16.6 rules (S4, CS4). Related: [`GATE.md`](GATE.md) (binary outcomes), [`PRINCIPLES.md`](PRINCIPLES.md) (hard gates).

---

## Definition

**[Quality](../docs/TERMS.md#quality)** measures the rate of defect-free operations across agent processes. The metric is:

```text
Quality = Ops / Opportunities

Where:
  Opportunities = total gate/verb executions in scope
  Ops          = opportunities that completed as specified (PASS, MET, ready)
  Defects      = opportunities that deviated from spec (FAIL, handoff_refused, error)
  Ops + Defects = Opportunities
```

**Unit:** ratio (0.0 – 1.0) or percentage (0% – 100%).

**[Defect](../docs/TERMS.md#defect) Rate** is the complement:

```text
Defect Rate = Defects / Opportunities = 1 - Quality
```

This is a DPMO-class metric (Defects Per Million Opportunities) without the academic theater. One [opportunity](../docs/TERMS.md#opportunity), one outcome: [op](../docs/TERMS.md#op) or [defect](../docs/TERMS.md#defect). No partial credit. No weighting. No continuous scores.

---

## What counts as an [Opportunity](../docs/TERMS.md#opportunity)

An **[Opportunity](../docs/TERMS.md#opportunity)** is a single execution of a [gate](../docs/TERMS.md#gate), verb, or [handoff](../docs/TERMS.md#handoff) where a binary outcome is recorded.

| [Boundary](../docs/TERMS.md#boundary) type | [Opportunity](../docs/TERMS.md#opportunity) trigger | Evidence source |
|---------------|---------------------|-----------------|
| [Gate](../docs/TERMS.md#gate) (CI, fitness) | [Gate](../docs/TERMS.md#gate) evaluation completes | CI log, fitness receipt |
| Verb (agent noun) | Verb execution completes | Verb receipt, [audit](../docs/TERMS.md#audit) log |
| [Handoff](../docs/TERMS.md#handoff) | [Handoff](../docs/TERMS.md#handoff) evaluation completes | Preflight result, [handoff](../docs/TERMS.md#handoff) receipt |
| [Audit](../docs/TERMS.md#audit) item | [Audit](../docs/TERMS.md#audit) item evaluated | [Audit](../docs/TERMS.md#audit) findings report |

**Not an [opportunity](../docs/TERMS.md#opportunity):**

- Internal processing steps without binary outcome
- Advisory warnings (not gates)
- Partial or in-progress states

---

## What counts as a [Defect](../docs/TERMS.md#defect)

A **[Defect](../docs/TERMS.md#defect)** is an [opportunity](../docs/TERMS.md#opportunity) whose outcome deviates from spec or adjectives.

| Outcome | Classification | Reason |
|---------|----------------|--------|
| `PASS` | [Op](../docs/TERMS.md#op) | Completed as specified |
| `MET` | [Op](../docs/TERMS.md#op) | Fitness criteria satisfied |
| `ready` | [Op](../docs/TERMS.md#op) | Preflight passed; proceed |
| `FAIL` | [Defect](../docs/TERMS.md#defect) | Did not meet criteria |
| `handoff_refused` | [Defect](../docs/TERMS.md#defect) | Produce incomplete; [boundary](../docs/TERMS.md#boundary) blocked |
| Error (thrown/returned) | [Defect](../docs/TERMS.md#defect) | Unexpected failure in evaluation |
| `not met` (audit) | [Defect](../docs/TERMS.md#defect) | [Audit](../docs/TERMS.md#audit) criterion not satisfied |

**Note:** `handoff_refused` is a produce-side [defect](../docs/TERMS.md#defect), not a fitness [defect](../docs/TERMS.md#defect). The producer's work was incomplete. Classification matters for root-cause attribution, not for the overall [defect](../docs/TERMS.md#defect) count.

---

## Measurement Surface

[Quality evidence](../docs/TERMS.md#quality-evidence) is recorded at these surfaces:

### 1. [Gate](../docs/TERMS.md#gate) receipts (CI, fitness)

Each [gate](../docs/TERMS.md#gate) execution produces a receipt with:

| Field | Type | Description |
|-------|------|-------------|
| `gate_id` | string | Identifier (e.g., `fitness-preflight`, `fitness-score`) |
| `outcome` | enum | `PASS` \| `FAIL` \| `REFUSE` |
| `timestamp` | ISO 8601 | When evaluated |
| `evidence_path` | string | Path to detailed evidence |

### 2. Verb receipts (agent nouns)

Each verb execution records:

| Field | Type | Description |
|-------|------|-------------|
| `verb_id` | string | Verb name on [agent noun](../docs/TERMS.md#agent-noun) |
| `outcome` | enum | [Op](../docs/TERMS.md#op) outcomes vs [defect](../docs/TERMS.md#defect) outcomes per verb [contract](../docs/TERMS.md#contract) |
| `timestamp` | ISO 8601 | When executed |
| `artifact_path` | string | Path to completion artifact |

### 3. [Audit](../docs/TERMS.md#audit) findings

Each [audit](../docs/TERMS.md#audit) item records:

| Field | Type | Description |
|-------|------|-------------|
| `audit_id` | string | [Audit](../docs/TERMS.md#audit) identifier (e.g., `A-R5`) |
| `item_outcome` | enum | `met` \| `not met` |
| `citation` | string | [Rule](../docs/TERMS.md#rule) reference |
| `evidence` | string | File:line or artifact |

### 4. Board / SSOT sync

[Quality](../docs/TERMS.md#quality) metrics aggregate to the task/board SSOT via:

| Field | Type | Description |
|-------|------|-------------|
| `ssot_leaf_ids` | string[] | Task/board leaf identifiers |
| `quality_snapshot` | object | `{ opportunities, ops, defects, quality }` at exit |

---

## Aggregation Levels

[Quality](../docs/TERMS.md#quality) can be computed at multiple scopes:

| Scope | Description | Use |
|-------|-------------|-----|
| **Single [boundary](../docs/TERMS.md#boundary)** | One gate/verb execution | Debugging, attribution |
| **[Produce package](../docs/TERMS.md#produce-package)** | All gates in one produce cycle | Package [quality](../docs/TERMS.md#quality) |
| **Session** | All boundaries in agent session | Session health |
| **Pipeline** | Produce → fitness → [audit](../docs/TERMS.md#audit) → [ship](../docs/TERMS.md#ship) | End-to-end [quality](../docs/TERMS.md#quality) |
| **Period** | Rolling window (hour, day, sprint) | Trend analysis |

Higher scopes aggregate opportunities and defects:

```text
Quality(scope) = sum(Ops in scope) / sum(Opportunities in scope)
```

---

## [Refuse](../docs/TERMS.md#refuse) Rules

### Q1. Fitness refuses [MET](../docs/TERMS.md#met) without [quality evidence](../docs/TERMS.md#quality-evidence)

If [quality evidence](../docs/TERMS.md#quality-evidence) (gate receipt with `outcome` + `timestamp`) is missing from the [produce package](../docs/TERMS.md#produce-package), fitness scoring refuses [MET](../docs/TERMS.md#met):

- Preflight: `handoff_refused` with `QUALITY_EVIDENCE` in missing enum
- Score: error `QUALITY_EVIDENCE_MISSING`

### Q2. Adversarial [audit](../docs/TERMS.md#audit) refuses PASS without [quality evidence](../docs/TERMS.md#quality-evidence)

[Audit](../docs/TERMS.md#audit) verbs check for [quality evidence](../docs/TERMS.md#quality-evidence) presence:

- `ssot_leaf_ids` present (≥1 opaque id)
- `quality_snapshot` present with non-zero `opportunities`
- If missing: [audit](../docs/TERMS.md#audit) FAIL citing Q2

### Q3. [Ship](../docs/TERMS.md#ship) refuses release without [quality](../docs/TERMS.md#quality) threshold [met](../docs/TERMS.md#met)

Ship-role verbs [verify](../docs/TERMS.md#verify) [quality](../docs/TERMS.md#quality) meets threshold (if threshold is defined):

- Default: no minimum threshold (quality is recorded, not enforced)
- [ADR](../docs/TERMS.md#adr) may define a threshold for a given pipeline
- Below threshold: [ship](../docs/TERMS.md#ship) verb returns error `QUALITY_BELOW_THRESHOLD`

---

## [Quality](../docs/TERMS.md#quality) Requirements

### Q1 — [Quality evidence](../docs/TERMS.md#quality-evidence) required at fitness

Every [produce package](../docs/TERMS.md#produce-package) submitted to fitness preflight must include [quality evidence](../docs/TERMS.md#quality-evidence) from prior [gate](../docs/TERMS.md#gate) executions in the produce cycle.

**[Audit](../docs/TERMS.md#audit) `A-Q1`:** [Met](../docs/TERMS.md#met) iff [produce package](../docs/TERMS.md#produce-package) contains at least one [gate](../docs/TERMS.md#gate) receipt with valid `outcome` + `timestamp`. Not [met](../docs/TERMS.md#met) if [quality evidence](../docs/TERMS.md#quality-evidence) is missing.

### Q2 — [Quality evidence](../docs/TERMS.md#quality-evidence) required at adversarial [audit](../docs/TERMS.md#audit)

Every artifact submitted to adversarial [audit](../docs/TERMS.md#audit) must have [quality evidence](../docs/TERMS.md#quality-evidence) traceable to SSOT.

**[Audit](../docs/TERMS.md#audit) `A-Q2`:** [Met](../docs/TERMS.md#met) iff `ssot_leaf_ids` are present AND `quality_snapshot` is non-null with `opportunities > 0`. Not [met](../docs/TERMS.md#met) otherwise.

### Q3 — [Quality snapshot](../docs/TERMS.md#quality-snapshot) recorded at [boundary](../docs/TERMS.md#boundary) exit

Every [boundary](../docs/TERMS.md#boundary) exit that advances work must record a [quality snapshot](../docs/TERMS.md#quality-snapshot).

**[Audit](../docs/TERMS.md#audit) `A-Q3`:** [Met](../docs/TERMS.md#met) iff [boundary](../docs/TERMS.md#boundary) completion artifact includes `quality_snapshot` with `{ opportunities, ops, defects, quality }`. Not [met](../docs/TERMS.md#met) if snapshot is missing or incomplete.

### Q4 — [Defect](../docs/TERMS.md#defect) classification is binary

Every [opportunity](../docs/TERMS.md#opportunity) outcome is classified as exactly one of: [op](../docs/TERMS.md#op) or [defect](../docs/TERMS.md#defect). No partial, provisional, or weighted outcomes.

**[Audit](../docs/TERMS.md#audit) `A-Q4`:** [Met](../docs/TERMS.md#met) iff every recorded outcome in scope maps to exactly `op` or `defect` with no other classification. Not [met](../docs/TERMS.md#met) if any outcome is partial, weighted, or unclassified.

### Q5 — [Quality](../docs/TERMS.md#quality) metric is ops/opportunities

The [quality](../docs/TERMS.md#quality) metric formula is Ops divided by Opportunities. No alternative formulas (e.g., weighted scores, continuous grades) are used for the canonical [quality](../docs/TERMS.md#quality) metric.

**[Audit](../docs/TERMS.md#audit) `A-Q5`:** [Met](../docs/TERMS.md#met) iff [quality](../docs/TERMS.md#quality) value equals `ops / opportunities` (within floating-point tolerance). Not [met](../docs/TERMS.md#met) if computed differently.

---

## Confirmation Checklist (Quality-specific)

For changes that add or modify [quality](../docs/TERMS.md#quality) metrics:

- [ ] CQ1. [Quality evidence](../docs/TERMS.md#quality-evidence) includes [gate](../docs/TERMS.md#gate) receipt with `outcome` + `timestamp`.
- [ ] CQ2. [Defect](../docs/TERMS.md#defect) classification is binary (op or defect only).
- [ ] CQ3. [Quality](../docs/TERMS.md#quality) formula is `ops / opportunities` — no weighting or continuous scores.
- [ ] CQ4. [Quality snapshot](../docs/TERMS.md#quality-snapshot) recorded at [boundary](../docs/TERMS.md#boundary) exit includes all four fields.
- [ ] CQ5. [Refuse](../docs/TERMS.md#refuse) rules implemented: fitness refuses without evidence, [audit](../docs/TERMS.md#audit) refuses without snapshot.
- [ ] CQ6. SSOT sync includes `quality_snapshot` for traceability.

---

## Cross-references

- [Charter](../docs/TERMS.md#charter) §16.2: [Agent noun](../docs/TERMS.md#agent-noun) structure (success criteria)
- [Charter](../docs/TERMS.md#charter) §16.6: Rules for [agent nouns](../docs/TERMS.md#agent-noun) (S4 — binary success criteria)
- [Charter](../docs/TERMS.md#charter) §11: Confirmation checklist (CS4 — ops vs defects)
- [`GATE.md`](GATE.md): [Gate](../docs/TERMS.md#gate) definition and binary outcomes
- [`PRINCIPLES.md`](PRINCIPLES.md): P3 (hard gates), P5 (binary audits)
- [`../agents/quality-architect/AGENT.md`](../agents/quality-architect/AGENT.md): [Quality](../docs/TERMS.md#quality) Architect role
- [`binding-matrix.json`](binding-matrix.json): [Requirement](../docs/TERMS.md#requirement) → [audit](../docs/TERMS.md#audit) → [gate](../docs/TERMS.md#gate) (JSON key remains `binder` until the auditor is updated)
