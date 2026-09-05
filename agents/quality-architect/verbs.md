# Quality Architect — Verbs

Contracted verbs for the quality-architect agent noun. Each verb has input contract, output contract, and failure mode.

---

## preflight-fitness-handoff

Check whether a produce handoff is ready for fitness scoring.

### Input contract

```yaml
input:
  preflight_request:
    type: object
    required: [artifact_path, package_path]
    properties:
      artifact_path:
        type: string
        description: Path to the change artifact (diff, proposal, code)
      package_path:
        type: string
        description: Path to the produce package directory
      handoff_token:
        type: string
        description: Optional. If present must match complete-produce issuance. Absence allowed when package_path supplied and package checks pass.
```

### Output contract

```yaml
output:
  type: object
  required: [status]
  properties:
    status:
      enum: [ready, handoff_refused]
    defect_log:
      type: object
      description: Produce-handoff defect details (only if handoff_refused)
      properties:
        missing:
          type: array
          items:
            enum: [PLAN, APPLICABILITY, BOUNDARY_IO, ADVERSARIAL_NOTES, VERIFY_SCRIPT]
        reason:
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
      enum: [ARTIFACT_NOT_FOUND, PACKAGE_NOT_FOUND]
    message:
      type: string
```

**Note:** `handoff_refused` is NOT an error. It is a valid output status indicating produce-incomplete. Errors are reserved for infrastructure failures.

---

## score-fitness

Score a change artifact against fitness criteria. Precondition: preflight status is `ready`.

### Input contract

```yaml
input:
  score_request:
    type: object
    required: [artifact_path, preflight_status]
    properties:
      artifact_path:
        type: string
        description: Path to the change artifact (diff, proposal, code)
      preflight_status:
        enum: [ready]
        description: Must be ready; handoff_refused artifacts cannot be scored
      checklist_scope:
        enum: [software, systems, both]
        default: software
        description: Which confirmation checklist to apply
      change_class:
        enum: [A, B, C, D, E, F]
        description: Change classification (if known)
```

### Output contract

```yaml
output:
  type: object
  required: [status, checklist_results]
  properties:
    status:
      enum: [MET, FAIL]
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
    blocking_failures:
      type: array
      items:
        type: string
      description: Item ids that caused FAIL status
```

### Failure mode

Returns error result:

```yaml
error:
  type: object
  required: [code, message]
  properties:
    code:
      enum: [ARTIFACT_NOT_FOUND, PREFLIGHT_NOT_READY, SELF_SCORE]
    message:
      type: string
```

**Note:** `PREFLIGHT_NOT_READY` error is returned if `preflight_status` is not `ready`. This enforces the default-closed handoff: no scoring without preflight pass.

---

## Excluded verbs (no shipping authority)

The following verbs are **explicitly excluded** from quality-architect:

- `ratify` — approve a proposal as final
- `merge` — merge a change to main branch
- `release` — publish or deploy
- `approve` — grant final approval
- `implement` — write the artifact being assessed

Quality Architect performs fitness checks and gates. Ship decisions and production belong to other roles.
