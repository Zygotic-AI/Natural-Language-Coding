# Standards Steward — Verbs

Contracted verbs for the standards-steward agent noun. Each verb has input contract, output contract, and failure mode.

---

## draft-adr

Draft an ADR for a decision that constrains future work.

### Input contract

```yaml
input:
  decision_request:
    type: object
    required: [context, decision_summary]
    properties:
      context:
        type: string
        description: Why this decision is needed
      decision_summary:
        type: string
        description: What is being decided
      options_considered:
        type: array
        items:
          type: string
        description: Alternatives evaluated (optional at input; required in output)
      related_adrs:
        type: array
        items:
          type: string
        description: ADR ids this relates to or supersedes
```

### Output contract

```yaml
output:
  type: object
  required: [adr_path, status]
  properties:
    adr_path:
      type: string
      description: Path to draft ADR file
    status:
      enum: [draft, needs_review]
    adr_content:
      type: object
      required: [title, context, decision, consequences, rejected]
      properties:
        title:
          type: string
        context:
          type: string
        decision:
          type: string
        consequences:
          type: array
          items:
            type: string
        rejected:
          type: array
          items:
            type: string
```

### Failure mode

Returns error result (does not throw):

```yaml
error:
  type: object
  required: [code, message]
  properties:
    code:
      enum: [MISSING_CONTEXT, DUPLICATE_ADR, CONFLICTING_PROPOSAL]
    message:
      type: string
```

---

## draft-charter-edit

Propose an edit to the charter.

### Input contract

```yaml
input:
  charter_edit_request:
    type: object
    required: [section, change_type, rationale]
    properties:
      section:
        type: string
        description: Charter section reference (e.g., "§5.2", "§16.3")
      change_type:
        enum: [add_rule, modify_rule, remove_rule, clarify]
      current_text:
        type: string
        description: Existing text (for modify/remove)
      proposed_text:
        type: string
        description: New or modified text
      rationale:
        type: string
        description: Why this change is needed
      adr_reference:
        type: string
        description: ADR that ratifies this change (required for rule changes)
```

### Output contract

```yaml
output:
  type: object
  required: [diff_path, status, adr_required]
  properties:
    diff_path:
      type: string
      description: Path to proposed diff or draft
    status:
      enum: [draft, needs_adr, needs_review]
    adr_required:
      type: boolean
      description: True if this change requires an ADR
    affected_rules:
      type: array
      items:
        type: string
      description: Rule ids affected (R*, S*, C*)
```

### Failure mode

Returns error result:

```yaml
error:
  type: object
  required: [code, message]
  properties:
    code:
      enum: [SECTION_NOT_FOUND, NO_RATIONALE, MISSING_ADR, WISH_NOT_RULE]
    message:
      type: string
```

---

## supersede-adr

Mark an ADR as superseded and record the successor.

### Input contract

```yaml
input:
  supersede_request:
    type: object
    required: [adr_id, successor_adr_id, reason]
    properties:
      adr_id:
        type: string
        description: ADR being superseded (e.g., "0002")
      successor_adr_id:
        type: string
        description: ADR that replaces it
      reason:
        type: string
        description: Why the supersession is needed
```

### Output contract

```yaml
output:
  type: object
  required: [adr_path, status_before, status_after]
  properties:
    adr_path:
      type: string
    status_before:
      type: string
    status_after:
      enum: [Superseded]
    successor_link:
      type: string
      description: Markdown link to successor ADR
```

### Failure mode

Returns error result:

```yaml
error:
  type: object
  required: [code, message]
  properties:
    code:
      enum: [ADR_NOT_FOUND, SUCCESSOR_NOT_FOUND, ALREADY_SUPERSEDED]
    message:
      type: string
```

---

## review-drift

Check whether charter, ADRs, and code agree. Report drift.

### Input contract

```yaml
input:
  drift_review_request:
    type: object
    required: [scope]
    properties:
      scope:
        enum: [charter, adrs, binding_matrix, all]
      specific_paths:
        type: array
        items:
          type: string
        description: Specific files to check (optional)
```

### Output contract

```yaml
output:
  type: object
  required: [status, findings]
  properties:
    status:
      enum: [no_drift, drift_found]
    findings:
      type: array
      items:
        type: object
        required: [location, issue, severity]
        properties:
          location:
            type: string
            description: File and section
          issue:
            type: string
            description: What disagrees
          severity:
            enum: [error, warning]
          suggested_fix:
            type: string
```

### Failure mode

Returns error result:

```yaml
error:
  type: object
  required: [code, message]
  properties:
    code:
      enum: [SCOPE_INVALID, PATH_NOT_FOUND]
    message:
      type: string
```

---

## Excluded verbs (no shipping authority)

The following verbs are **explicitly excluded** from standards-steward:

- `ratify` — approve a proposal as final
- `merge` — merge a change to main branch
- `release` — publish or deploy
- `approve` — grant final approval

Standards steward produces proposals. Ship decisions belong to another role.
