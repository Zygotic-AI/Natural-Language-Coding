# Ship Role — Verbs

Contracted verbs for the ship-role agent noun. Each verb has input contract, output contract, and failure mode.

---

## ratify

Accept a proposal as final. This completes the ratification step (charter §6 step 5).

### Input contract

```yaml
input:
  ratify_request:
    type: object
    required: [proposal_path, audit_report_path, mandate]
    properties:
      proposal_path:
        type: string
        description: Path to the proposal being ratified
      audit_report_path:
        type: string
        description: Path to the audit report (findings or clean)
      mandate:
        type: object
        required: [type, reference]
        properties:
          type:
            enum: [charter, delegation]
          reference:
            type: string
            description: ADR path or delegation record path
      findings_disposition:
        type: array
        items:
          type: object
          required: [finding_id, disposition]
          properties:
            finding_id:
              type: string
            disposition:
              enum: [fixed, waived, escalated]
            evidence:
              type: string
              description: How the finding was addressed
```

### Output contract

```yaml
output:
  type: object
  required: [status, ship_record_path]
  properties:
    status:
      enum: [ratified, blocked]
    ship_record_path:
      type: string
      description: Path to the ship record
    ratified_version:
      type: string
      description: Version or commit hash of ratified artifact
    ratified_at:
      type: string
      format: date-time
    ratified_by:
      type: string
      description: Agent or human who ratified
```

### Failure mode

Returns error result:

```yaml
error:
  type: object
  required: [code, message]
  properties:
    code:
      enum: [NO_MANDATE, AUDIT_INCOMPLETE, FINDINGS_UNRESOLVED, SELF_SHIP]
    message:
      type: string
```

---

## merge

Merge a change to the target branch.

### Input contract

```yaml
input:
  merge_request:
    type: object
    required: [branch, target_branch, audit_report_path, mandate]
    properties:
      branch:
        type: string
        description: Source branch to merge
      target_branch:
        type: string
        description: Target branch (e.g., main)
      audit_report_path:
        type: string
        description: Path to the audit report
      ci_status:
        type: object
        properties:
          passing:
            type: boolean
          waiver_path:
            type: string
            description: Path to CI waiver if not passing
      mandate:
        type: object
        required: [type, reference]
        properties:
          type:
            enum: [charter, delegation]
          reference:
            type: string
      findings_disposition:
        type: array
        items:
          type: object
          required: [finding_id, disposition]
          properties:
            finding_id:
              type: string
            disposition:
              enum: [fixed, waived, escalated]
            evidence:
              type: string
```

### Output contract

```yaml
output:
  type: object
  required: [status, ship_record_path]
  properties:
    status:
      enum: [merged, blocked]
    ship_record_path:
      type: string
    merge_commit:
      type: string
      description: Commit SHA of the merge
    merged_at:
      type: string
      format: date-time
    merged_by:
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
      enum: [NO_MANDATE, AUDIT_INCOMPLETE, FINDINGS_UNRESOLVED, CI_FAILING, SELF_SHIP, CONFLICT]
    message:
      type: string
```

---

## release

Publish or deploy an artifact.

### Input contract

```yaml
input:
  release_request:
    type: object
    required: [artifact_path, version, audit_report_path, mandate]
    properties:
      artifact_path:
        type: string
        description: Path to the artifact being released
      version:
        type: string
        description: Semantic version or release tag
      audit_report_path:
        type: string
        description: Path to the audit report
      release_target:
        type: string
        description: Where to release (registry, environment, etc.)
      mandate:
        type: object
        required: [type, reference]
        properties:
          type:
            enum: [charter, delegation]
          reference:
            type: string
      release_criteria:
        type: object
        properties:
          all_tests_passing:
            type: boolean
          security_scan_clean:
            type: boolean
          sign_off_required:
            type: array
            items:
              type: string
            description: Required sign-offs received
```

### Output contract

```yaml
output:
  type: object
  required: [status, ship_record_path]
  properties:
    status:
      enum: [released, blocked]
    ship_record_path:
      type: string
    release_id:
      type: string
      description: Registry ID, deployment ID, or release tag
    released_at:
      type: string
      format: date-time
    released_by:
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
      enum: [NO_MANDATE, AUDIT_INCOMPLETE, CRITERIA_NOT_MET, SELF_SHIP]
    message:
      type: string
```

---

## waive-finding

Accept an audit finding without requiring a fix. Records the waiver with risk acknowledgment.

### Input contract

```yaml
input:
  waive_request:
    type: object
    required: [finding_id, audit_report_path, rationale, mandate]
    properties:
      finding_id:
        type: string
        description: Finding being waived
      audit_report_path:
        type: string
        description: Path to the audit report containing the finding
      rationale:
        type: string
        description: Why this finding does not block release
      risk_acknowledgment:
        type: string
        description: What risk is accepted by waiving
      expiration:
        type: string
        format: date
        description: When this waiver expires (optional)
      mandate:
        type: object
        required: [type, reference]
        properties:
          type:
            enum: [charter, delegation]
          reference:
            type: string
```

### Output contract

```yaml
output:
  type: object
  required: [status, waiver_record_path]
  properties:
    status:
      enum: [waived, rejected]
    waiver_record_path:
      type: string
      description: Path to the waiver record
    waived_at:
      type: string
      format: date-time
    waived_by:
      type: string
    expiration:
      type: string
      format: date
```

### Failure mode

Returns error result:

```yaml
error:
  type: object
  required: [code, message]
  properties:
    code:
      enum: [NO_MANDATE, FINDING_NOT_FOUND, INSUFFICIENT_RATIONALE, BLOCKER_NOT_WAIVABLE]
    message:
      type: string
```

---

## Preconditions (all verbs)

Every ship verb checks before execution:

1. **Mandate exists** — Charter ADR or delegation record cited
2. **Audit complete** — Audit report path valid and status is `findings_found` or `clean`
3. **No self-ship** — Agent calling the verb did not solely produce the artifact
4. **Findings addressed** — Each finding in report has disposition (fixed, waived, or escalated)

Failure of any precondition returns the appropriate error code without executing the verb.
