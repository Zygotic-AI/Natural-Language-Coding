# PR-005 Boundary I/O Declarations

## Modified boundaries

### 1. `complete-produce` (standards-steward verb)

**Added to output:**
```yaml
missing:
  items:
    enum: [..., NOTION_EXIT_EVIDENCE]  # Added
notion_page_ids:
  type: array
  items:
    type: string
    format: uuid
  description: Notion page UUIDs from package (echo for traceability)
notion_exit_status:
  type: string
  description: Exit status declared in package (echo for traceability)
```

**Added to failure mode:**
```yaml
code:
  enum: [..., NOTION_EVIDENCE_MISSING]  # Added
```

---

### 2. `preflight-fitness-handoff` (quality-architect verb)

**Added to output:**
```yaml
defect_log:
  missing:
    items:
      enum: [..., NOTION_EXIT_EVIDENCE]  # Added
notion_page_ids:
  type: array
  items:
    type: string
    format: uuid
  description: Notion page UUIDs from package (only if ready)
notion_exit_status:
  type: string
  description: Exit status declared in package (only if ready)
```

---

### 3. `score-fitness` (quality-architect verb)

**Added to input:**
```yaml
notion_page_ids:
  type: array
  items:
    type: string
    format: uuid
  description: Notion page UUIDs from preflight (required for MET)
notion_exit_status:
  type: string
  description: Exit status from preflight (required for MET)
```

**Added to output:**
```yaml
checklist_results:
  items:
    item_id:
      description: Checklist item (C1, C2, CS1, CS8, etc.)  # CS8 added
notion_page_ids:
  type: array
  items:
    type: string
    format: uuid
  description: Notion page UUIDs verified (echo for receipt)
notion_exit_status:
  type: string
  description: Exit status verified (echo for receipt)
```

**Added to failure mode:**
```yaml
code:
  enum: [..., NOTION_EVIDENCE_MISSING]  # Added
```

---

### 4. `audit-proposal` (adversarial-auditor verb)

**Added to input:**
```yaml
notion_page_ids:
  type: array
  items:
    type: string
    format: uuid
  description: Notion page UUIDs from fitness receipt (required for PASS per P-020)
notion_exit_status:
  type: string
  description: Exit status from fitness receipt (required for PASS per P-020)
```

**Added to failure mode:**
```yaml
code:
  enum: [..., NOTION_EVIDENCE_MISSING]  # Added
```

---

### 5. `audit-diff` (adversarial-auditor verb)

**Added to input:**
```yaml
notion_page_ids:
  type: array
  items:
    type: string
    format: uuid
  description: Notion page UUIDs from fitness receipt (required for pass per P-020)
notion_exit_status:
  type: string
  description: Exit status from fitness receipt (required for pass per P-020)
```

**Added to failure mode:**
```yaml
code:
  enum: [..., NOTION_EVIDENCE_MISSING]  # Added
```

---

## Boundary vocabulary

| Term | Input/Output | Boundary |
|------|--------------|----------|
| `notion_page_ids` | Input/Output | complete-produce, preflight-fitness-handoff, score-fitness, audit-* |
| `notion_exit_status` | Input/Output | complete-produce, preflight-fitness-handoff, score-fitness, audit-* |
| `NOTION_EXIT_EVIDENCE` | Output (missing enum) | complete-produce, preflight-fitness-handoff |
| `NOTION_EVIDENCE_MISSING` | Error code | complete-produce, score-fitness, audit-* |
