# Boundary I/O — SSOT exit evidence (abstract)

## Modified boundaries

### 1. `complete-produce` (standards-steward)

**Output missing enum:** include `SSOT_EXIT_EVIDENCE` (replaces any `NOTION_EXIT_EVIDENCE`).

**Output fields:**

```yaml
ssot_leaf_ids:
  type: array
  items:
    type: string
  minItems: 1
  description: Opaque leaf ids from the task/board SSOT (echo for traceability)
ssot_exit_status:
  type: string
  minLength: 1
  description: Exit state string declared in package (echo for traceability)
```

**Failure mode:** include `SSOT_EVIDENCE_MISSING`.

---

### 2. `preflight-fitness-handoff` (quality-architect)

**defect_log.missing enum:** include `SSOT_EXIT_EVIDENCE`.

**Output when ready:** `ssot_leaf_ids`, `ssot_exit_status`.

`handoff_refused` remains a valid output (not an infrastructure error) when SSOT exit evidence is missing.

---

### 3. `score-fitness` (quality-architect)

**Input (required for MET):** `ssot_leaf_ids`, `ssot_exit_status`.

**Output echo:** same fields.

**Failure mode:** include `SSOT_EVIDENCE_MISSING`.

**blocking_failures:** may include `CS8` when SSOT exit evidence missing.

---

### 4. `audit-proposal` / `audit-diff` (adversarial-auditor)

**Input (required for PASS):** `ssot_leaf_ids`, `ssot_exit_status`.

**Failure mode:** include `SSOT_EVIDENCE_MISSING`.

---

## Boundary vocabulary

| Term | Role | Boundaries |
|------|------|------------|
| `ssot_leaf_ids` | I/O field | complete-produce, preflight, score-fitness, audit-* |
| `ssot_exit_status` | I/O field | complete-produce, preflight, score-fitness, audit-* |
| `SSOT_EXIT_EVIDENCE` | Missing enum | complete-produce, preflight |
| `SSOT_EVIDENCE_MISSING` | Error code | complete-produce, score-fitness, audit-* |

## Explicitly removed from BBA contracts

| Removed | Why |
|---------|-----|
| `notion_page_ids` | Product-named field |
| `notion_exit_status` | Product-named field |
| `NOTION_EXIT_EVIDENCE` | Product-named missing token |
| `NOTION_EVIDENCE_MISSING` | Product-named error code |

Product mapping belongs outside BBA (implementation/bindings repo).
