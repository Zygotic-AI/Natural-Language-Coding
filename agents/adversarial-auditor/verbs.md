# Adversarial Auditor — Verbs

Contracted verbs for the adversarial-auditor agent noun. Each verb has input contract, output contract, and failure mode.

---

## audit-proposal

Audit a proposal (spec, ADR draft, charter edit) against charter rules.

### Input contract

```yaml
input:
  audit_request:
    type: object
    required: [artifact_path, artifact_type]
    properties:
      artifact_path:
        type: string
        description: Path to the proposal or artifact
      artifact_type:
        enum: [proposal, adr_draft, charter_edit, diff]
      rules_in_scope:
        type: array
        items:
          type: string
        description: Specific rules to check (e.g., ["R5", "R6", "S1", "S8"]). If omitted, all applicable rules.
      producer_id:
        type: string
        description: Who produced this artifact (to verify separation)
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

### Output contract

```yaml
output:
  type: object
  required: [status, findings, rules_checked]
  properties:
    status:
      enum: [findings_found, clean]
    findings:
      type: array
      items:
        type: object
        required: [rule_id, location, issue, severity]
        properties:
          rule_id:
            type: string
            description: Rule violated (R*, S*, C*, P*)
          location:
            type: string
            description: File, line, or section
          issue:
            type: string
            description: What the violation is
          severity:
            enum: [blocker, major, minor]
          suggested_fix:
            type: string
            description: How to remediate (optional)
    rules_checked:
      type: array
      items:
        type: object
        required: [rule_id, status]
        properties:
          rule_id:
            type: string
          status:
            enum: [met, not_met, na]
          evidence:
            type: string
            description: Pointer to evidence (file:line or N/A reason)
```

### Failure mode

Returns error result:

```yaml
error:
  type: object
  required: [code, message]
  properties:
    code:
      enum: [ARTIFACT_NOT_FOUND, SELF_AUDIT, SCOPE_EMPTY, NOTION_EVIDENCE_MISSING]
    message:
      type: string
```

**Note:** `NOTION_EVIDENCE_MISSING` error is returned if Notion page id(s) or exit status are absent; audit refuses PASS without Notion exit evidence (S8, P-020).

---

## audit-diff

Audit a code diff against charter rules and confirmation checklist.

### Input contract

```yaml
input:
  diff_audit_request:
    type: object
    required: [diff_ref]
    properties:
      diff_ref:
        type: string
        description: Git ref, PR URL, or path to diff file
      change_class:
        enum: [A, B, C, D, E, F]
        description: Change classification (if known)
      checklist_scope:
        enum: [software, systems, both]
        default: software
        description: Which confirmation checklist to apply
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

### Output contract

```yaml
output:
  type: object
  required: [status, checklist_results, findings]
  properties:
    status:
      enum: [pass, fail]
    checklist_results:
      type: array
      items:
        type: object
        required: [item_id, status]
        properties:
          item_id:
            type: string
            description: Checklist item (C1, C2, CS1, etc.)
          status:
            enum: [PASS, FAIL, N/A]
          evidence:
            type: string
            description: File:line or N/A reason
    findings:
      type: array
      items:
        type: object
        required: [rule_id, location, issue, severity]
        properties:
          rule_id:
            type: string
          location:
            type: string
          issue:
            type: string
          severity:
            enum: [blocker, major, minor]
    blocking_items:
      type: array
      items:
        type: string
      description: Item ids that must pass (C4, C5, C9, C16, C19, C20)
```

### Failure mode

Returns error result:

```yaml
error:
  type: object
  required: [code, message]
  properties:
    code:
      enum: [DIFF_NOT_FOUND, SELF_AUDIT, INVALID_CLASS, NOTION_EVIDENCE_MISSING]
    message:
      type: string
```

**Note:** `NOTION_EVIDENCE_MISSING` error is returned if Notion page id(s) or exit status are absent; audit refuses pass without Notion exit evidence (S8, P-020).

---

## audit-binding-matrix

Audit the binding matrix for unbound, unbindable, or missing requirements.

### Input contract

```yaml
input:
  matrix_audit_request:
    type: object
    properties:
      matrix_path:
        type: string
        default: "integrity/binding-matrix.json"
      charter_path:
        type: string
        default: "CHARTER.md"
      check_coverage:
        type: boolean
        default: true
        description: Check that all charter rules appear in matrix
```

### Output contract

```yaml
output:
  type: object
  required: [status, audits_run]
  properties:
    status:
      enum: [pass, fail]
    audits_run:
      type: array
      items:
        type: object
        required: [audit_id, status]
        properties:
          audit_id:
            enum: [A-BINDING-UNBOUND, A-BINDING-PROMOTE, A-BINDING-COVERAGE]
          status:
            enum: [met, not_met]
          offending_ids:
            type: array
            items:
              type: string
            description: Requirement ids that failed (required when not_met)
```

### Failure mode

Returns error result:

```yaml
error:
  type: object
  required: [code, message]
  properties:
    code:
      enum: [MATRIX_NOT_FOUND, CHARTER_NOT_FOUND, PARSE_ERROR]
    message:
      type: string
```

---

## challenge-finding

Challenge a previous finding (request re-audit with rebuttal).

### Input contract

```yaml
input:
  challenge_request:
    type: object
    required: [finding_id, rebuttal]
    properties:
      finding_id:
        type: string
        description: Identifier of the finding being challenged
      rebuttal:
        type: string
        description: Why the finding is incorrect or should be waived
      evidence:
        type: string
        description: Evidence supporting the rebuttal
```

### Output contract

```yaml
output:
  type: object
  required: [finding_id, resolution]
  properties:
    finding_id:
      type: string
    resolution:
      enum: [upheld, withdrawn, escalate]
    rationale:
      type: string
      description: Why the finding stands, is withdrawn, or needs escalation
```

### Failure mode

Returns error result:

```yaml
error:
  type: object
  required: [code, message]
  properties:
    code:
      enum: [FINDING_NOT_FOUND, SELF_CHALLENGE, INSUFFICIENT_REBUTTAL]
    message:
      type: string
```

---

## Excluded verbs (no shipping authority)

The following verbs are **explicitly excluded** from adversarial-auditor:

- `ratify` — approve a proposal as final
- `merge` — merge a change to main branch
- `release` — publish or deploy
- `approve` — grant final approval
- `implement` — write the artifact being audited

Adversarial auditor produces findings. Ship decisions and production belong to other roles.
