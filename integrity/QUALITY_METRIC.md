# Quality Metric

SSOT for the Quality metric in Boundary-Based Programming. Quality measures ops versus defects across agent processes — a binary count, not a continuous score.

Rationale: charter §16.2 success criteria, §16.6 rules (S4, CS4). Related: [`GATE.md`](GATE.md) (binary outcomes), [`PRINCIPLES.md`](PRINCIPLES.md) (hard gates).

---

## Definition

**Quality** measures the rate of defect-free operations across agent processes. The metric is:

```text
Quality = Ops / Opportunities

Where:
  Opportunities = total gate/verb executions in scope
  Ops          = opportunities that completed as specified (PASS, MET, ready)
  Defects      = opportunities that deviated from spec (FAIL, handoff_refused, error)
  Ops + Defects = Opportunities
```

**Unit:** ratio (0.0 – 1.0) or percentage (0% – 100%).

**Defect Rate** is the complement:

```text
Defect Rate = Defects / Opportunities = 1 - Quality
```

This is a DPMO-class metric (Defects Per Million Opportunities) without the academic theater. One opportunity, one outcome: op or defect. No partial credit. No weighting. No continuous scores.

---

## What counts as an Opportunity

An **Opportunity** is a single execution of a gate, verb, or handoff where a binary outcome is recorded.

| Boundary type | Opportunity trigger | Evidence source |
|---------------|---------------------|-----------------|
| Gate (CI, fitness) | Gate evaluation completes | CI log, fitness receipt |
| Verb (agent noun) | Verb execution completes | Verb receipt, audit log |
| Handoff | Handoff evaluation completes | Preflight result, handoff receipt |
| Audit item | Audit item evaluated | Audit findings report |

**Not an opportunity:**

- Internal processing steps without binary outcome
- Advisory warnings (not gates)
- Partial or in-progress states

---

## What counts as a Defect

A **Defect** is an opportunity whose outcome deviates from spec or invariants.

| Outcome | Classification | Reason |
|---------|----------------|--------|
| `PASS` | Op | Completed as specified |
| `MET` | Op | Fitness criteria satisfied |
| `ready` | Op | Preflight passed; proceed |
| `FAIL` | Defect | Did not meet criteria |
| `handoff_refused` | Defect | Produce incomplete; boundary blocked |
| Error (thrown/returned) | Defect | Unexpected failure in evaluation |
| `not met` (audit) | Defect | Audit criterion not satisfied |

**Note:** `handoff_refused` is a produce-side defect, not a fitness defect. The producer's work was incomplete. Classification matters for root-cause attribution, not for the overall defect count.

---

## Measurement Surface

Quality evidence is recorded at these surfaces:

### 1. Gate receipts (CI, fitness)

Each gate execution produces a receipt with:

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
| `verb_id` | string | Verb name on agent noun |
| `outcome` | enum | Op outcomes vs defect outcomes per verb contract |
| `timestamp` | ISO 8601 | When executed |
| `artifact_path` | string | Path to completion artifact |

### 3. Audit findings

Each audit item records:

| Field | Type | Description |
|-------|------|-------------|
| `audit_id` | string | Audit identifier (e.g., `A-R5`) |
| `item_outcome` | enum | `met` \| `not met` |
| `citation` | string | Rule reference |
| `evidence` | string | File:line or artifact |

### 4. Board / SSOT sync

Quality metrics aggregate to the task/board SSOT via:

| Field | Type | Description |
|-------|------|-------------|
| `ssot_leaf_ids` | string[] | Task/board leaf identifiers |
| `quality_snapshot` | object | `{ opportunities, ops, defects, quality }` at exit |

---

## Aggregation Levels

Quality can be computed at multiple scopes:

| Scope | Description | Use |
|-------|-------------|-----|
| **Single boundary** | One gate/verb execution | Debugging, attribution |
| **Produce package** | All gates in one produce cycle | Package quality |
| **Session** | All boundaries in agent session | Session health |
| **Pipeline** | Produce → fitness → audit → ship | End-to-end quality |
| **Period** | Rolling window (hour, day, sprint) | Trend analysis |

Higher scopes aggregate opportunities and defects:

```text
Quality(scope) = sum(Ops in scope) / sum(Opportunities in scope)
```

---

## Refuse Rules

### Q1. Fitness refuses MET without quality evidence

If quality evidence (gate receipt with `outcome` + `timestamp`) is missing from the produce package, fitness scoring refuses MET:

- Preflight: `handoff_refused` with `QUALITY_EVIDENCE` in missing enum
- Score: error `QUALITY_EVIDENCE_MISSING`

### Q2. Adversarial audit refuses PASS without quality evidence

Audit verbs check for quality evidence presence:

- `ssot_leaf_ids` present (≥1 opaque id)
- `quality_snapshot` present with non-zero `opportunities`
- If missing: audit FAIL citing Q2

### Q3. Ship refuses release without quality threshold met

Ship-role verbs verify quality meets threshold (if threshold is defined):

- Default: no minimum threshold (quality is recorded, not enforced)
- ADR may define a threshold for a given pipeline
- Below threshold: ship verb returns error `QUALITY_BELOW_THRESHOLD`

---

## Quality Requirements

### Q1 — Quality evidence required at fitness

Every produce package submitted to fitness preflight must include quality evidence from prior gate executions in the produce cycle.

**Audit `A-Q1`:** Met iff produce package contains at least one gate receipt with valid `outcome` + `timestamp`. Not met if quality evidence is missing.

### Q2 — Quality evidence required at adversarial audit

Every artifact submitted to adversarial audit must have quality evidence traceable to SSOT.

**Audit `A-Q2`:** Met iff `ssot_leaf_ids` are present AND `quality_snapshot` is non-null with `opportunities > 0`. Not met otherwise.

### Q3 — Quality snapshot recorded at boundary exit

Every boundary exit that advances work must record a quality snapshot.

**Audit `A-Q3`:** Met iff boundary completion artifact includes `quality_snapshot` with `{ opportunities, ops, defects, quality }`. Not met if snapshot is missing or incomplete.

### Q4 — Defect classification is binary

Every opportunity outcome is classified as exactly one of: op or defect. No partial, provisional, or weighted outcomes.

**Audit `A-Q4`:** Met iff every recorded outcome in scope maps to exactly `op` or `defect` with no other classification. Not met if any outcome is partial, weighted, or unclassified.

### Q5 — Quality metric is ops/opportunities

The quality metric formula is Ops divided by Opportunities. No alternative formulas (e.g., weighted scores, continuous grades) are used for the canonical quality metric.

**Audit `A-Q5`:** Met iff quality value equals `ops / opportunities` (within floating-point tolerance). Not met if computed differently.

---

## Confirmation Checklist (Quality-specific)

For changes that add or modify quality metrics:

- [ ] CQ1. Quality evidence includes gate receipt with `outcome` + `timestamp`.
- [ ] CQ2. Defect classification is binary (op or defect only).
- [ ] CQ3. Quality formula is `ops / opportunities` — no weighting or continuous scores.
- [ ] CQ4. Quality snapshot recorded at boundary exit includes all four fields.
- [ ] CQ5. Refuse rules implemented: fitness refuses without evidence, audit refuses without snapshot.
- [ ] CQ6. SSOT sync includes `quality_snapshot` for traceability.

---

## Cross-references

- Charter §16.2: Agent noun structure (success criteria)
- Charter §16.6: Rules for agent nouns (S4 — binary success criteria)
- Charter §11: Confirmation checklist (CS4 — ops vs defects)
- [`GATE.md`](GATE.md): Gate definition and binary outcomes
- [`PRINCIPLES.md`](PRINCIPLES.md): P3 (hard gates), P5 (binary audits)
- [`../agents/quality-architect/AGENT.md`](../agents/quality-architect/AGENT.md): Quality Architect role
- [`binding-matrix.json`](binding-matrix.json): Requirement → audit → binder index
