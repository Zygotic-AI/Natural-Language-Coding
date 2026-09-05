# Standards Steward — Verbs

Contracted verbs for the standards-steward agent noun. Each verb has input contract, output contract, and failure mode.

---

## Query verbs (read-only)

These verbs provide applicability information to Sessions/Work Units without granting produce authority. A Session may call these verbs to obtain an applicability register before materialize (default-closed). The Session does not become the steward; it receives read-only data.

---

## load-applicability

Return the applicability register for a given scope. A Session/WU calls this verb to learn which charter rules, ADRs, checklists, and agent noun constraints apply before materializing work. This is a query — it does not produce, modify, or ratify any standard.

### Input contract

```yaml
input:
  applicability_request:
    type: object
    required: [scope]
    properties:
      scope:
        type: object
        required: [change_class]
        properties:
          change_class:
            enum: [A, B, C, D, E, F]
            description: Change classification (charter §6 step 1)
          artifact_type:
            enum: [noun, verb, goal, workflow, contract, charter, adr, agent_noun]
            description: Type of artifact being changed
          nouns_in_scope:
            type: array
            items:
              type: string
            description: Noun ids affected (if known)
          agent_nouns_in_scope:
            type: array
            items:
              type: string
            description: Agent noun ids affected (if known)
      include_checklist:
        type: boolean
        default: true
        description: Include applicable confirmation checklist items
      include_adrs:
        type: boolean
        default: true
        description: Include related ADR references
```

### Output contract

```yaml
output:
  applicability_register:
    type: object
    required: [rules_applicable, checklist_applicable, status]
    properties:
      status:
        enum: [loaded, partial, error]
      rules_applicable:
        type: array
        items:
          type: object
          required: [rule_id, statement, surface]
          properties:
            rule_id:
              type: string
              description: Rule identifier (R*, S*, P*)
            statement:
              type: string
            surface:
              enum: [in-force, reference]
            binding_status:
              enum: [bound, unbound]
            binder:
              type: string
              description: Path to binder (if bound)
      checklist_applicable:
        type: array
        items:
          type: object
          required: [item_id, statement, scope]
          properties:
            item_id:
              type: string
              description: Checklist item (C*, CS*)
            statement:
              type: string
            scope:
              enum: [software, systems, both]
            blocking:
              type: boolean
              description: True if this item blocks completion (C4, C5, etc.)
      adrs_applicable:
        type: array
        items:
          type: object
          required: [adr_id, title, status]
          properties:
            adr_id:
              type: string
            title:
              type: string
            status:
              enum: [Accepted, Superseded, Draft]
            path:
              type: string
      gates_required:
        type: array
        items:
          type: string
        description: Gate ids that must complete for this change class (G-PROPOSE, G-REVIEW, etc.)
```

### Failure mode

Returns error result (does not throw):

```yaml
error:
  type: object
  required: [code, message]
  properties:
    code:
      enum: [INVALID_SCOPE, CHARTER_UNAVAILABLE, MATRIX_UNAVAILABLE]
    message:
      type: string
```

### Separation guarantee

This verb is **read-only**. Calling `load-applicability` does NOT:
- Grant the caller produce authority over standards
- Allow the caller to modify charter, ADRs, or binding matrix
- Create any artifact or side effect

The Session obtains an applicability register; it does not become the steward.

---

## Produce verbs (write authority)

These verbs produce or modify standards artifacts. Only the standards-steward agent noun may execute these. A Session that called `load-applicability` does not gain produce authority.

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

## complete-produce

Signal that produce work is complete and ready for fitness handoff.

### Input contract

```yaml
input:
  complete_produce_request:
    type: object
    required: [artifact_path, package_path]
    properties:
      artifact_path:
        type: string
        description: Path to the change artifact (diff, proposal, code)
      package_path:
        type: string
        description: Path to the produce package directory
      classification:
        enum: [A, B, C, D, E, F]
        description: Change class (§6 Step 1)
```

### Output contract

```yaml
output:
  type: object
  required: [status]
  properties:
    status:
      enum: [complete, incomplete]
    handoff_token:
      type: string
      description: Token for fitness handoff (only if complete)
    missing:
      type: array
      items:
        enum: [PLAN, APPLICABILITY, BOUNDARY_IO, ADVERSARIAL_NOTES, VERIFY_SCRIPT, NOTION_EXIT_EVIDENCE]
      description: Missing package elements (only if incomplete)
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

### Failure mode

Returns error result:

```yaml
error:
  type: object
  required: [code, message]
  properties:
    code:
      enum: [ARTIFACT_NOT_FOUND, PACKAGE_NOT_FOUND, PACKAGE_MISSING, NOTION_EVIDENCE_MISSING]
    message:
      type: string
```

**Note:** `handoff_token` is issued when status is `complete` for convenience. Fitness preflight may accept a token OR validate package paths directly; the hard gate is package completeness (S7) and Notion exit evidence (S8, P-020), not token presence. Token is optional on preflight input.

---

## Excluded verbs (no shipping authority)

The following verbs are **explicitly excluded** from standards-steward:

- `ratify` — approve a proposal as final
- `merge` — merge a change to main branch
- `release` — publish or deploy
- `approve` — grant final approval

Standards steward produces proposals. Ship decisions belong to another role.
