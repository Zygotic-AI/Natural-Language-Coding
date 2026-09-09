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
      quality_evidence:
        type: object
        description: Quality evidence from prior gate executions (Q1)
        properties:
          gate_receipts:
            type: array
            items:
              type: object
              required: [gate_id, outcome, timestamp]
              properties:
                gate_id:
                  type: string
                outcome:
                  enum: [PASS, FAIL, MET, REFUSE]
                timestamp:
                  type: string
                  format: date-time
                evidence_path:
                  type: string
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
            enum: [PLAN, APPLICABILITY, BOUNDARY_IO, ADVERSARIAL_NOTES, VERIFY_SCRIPT, SSOT_EXIT_EVIDENCE, QUALITY_EVIDENCE]
        reason:
          type: string
    ssot_leaf_ids:
      type: array
      items:
        type: string
      minItems: 1
      description: Opaque leaf ids from package (only if ready)
    ssot_exit_status:
      type: string
      minLength: 1
      description: Exit state string from package (only if ready)
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

**Note:** `handoff_refused` is NOT an error. It is a valid output status indicating produce-incomplete (includes missing SSOT exit evidence per S8/P-020). Errors are reserved for infrastructure failures.

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
      ssot_leaf_ids:
        type: array
        items:
          type: string
        minItems: 1
        description: SSOT leaf ids from preflight (required for MET)
      ssot_exit_status:
        type: string
        minLength: 1
        description: Exit status from preflight (required for MET)
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
            description: Checklist item (C1, C2, CS1, CS8, etc.)
          status:
            enum: [PASS, FAIL, N/A]
          evidence:
            type: string
            description: File:line or N/A reason
    blocking_failures:
      type: array
      items:
        type: string
      description: Item ids that caused FAIL status (includes CS8 if SSOT exit evidence missing)
    ssot_leaf_ids:
      type: array
      items:
        type: string
      minItems: 1
      description: SSOT leaf ids verified (echo for receipt)
    ssot_exit_status:
      type: string
      minLength: 1
      description: Exit status verified (echo for receipt)
    quality_snapshot:
      type: object
      description: Quality snapshot at fitness exit (Q3)
      required: [opportunities, ops, defects, quality]
      properties:
        opportunities:
          type: integer
          minimum: 0
          description: Total gate/verb executions in scope
        ops:
          type: integer
          minimum: 0
          description: Opportunities completed as specified
        defects:
          type: integer
          minimum: 0
          description: Opportunities that deviated from spec
        quality:
          type: number
          minimum: 0
          maximum: 1
          description: Quality ratio (ops / opportunities)
```

### Failure mode

Returns error result:

```yaml
error:
  type: object
  required: [code, message]
  properties:
    code:
      enum: [ARTIFACT_NOT_FOUND, PREFLIGHT_NOT_READY, SELF_SCORE, SSOT_EVIDENCE_MISSING, QUALITY_EVIDENCE_MISSING]
    message:
      type: string
```

**Note:** `PREFLIGHT_NOT_READY` error is returned if `preflight_status` is not `ready`. This enforces the default-closed handoff: no scoring without preflight pass. `SSOT_EVIDENCE_MISSING` error is returned if `ssot_leaf_ids` or `ssot_exit_status` are absent; scoring refuses MET without SSOT exit evidence (S8, P-020). `QUALITY_EVIDENCE_MISSING` error is returned if quality evidence (gate receipts) is absent; scoring refuses MET without quality evidence (Q1).

---

## Excluded verbs (no shipping authority)

The following verbs are **explicitly excluded** from quality-architect:

- `ratify` — approve a proposal as final
- `merge` — merge a change to main branch
- `release` — publish or deploy
- `approve` — grant final approval
- `implement` — write the artifact being assessed

Quality Architect performs fitness checks and gates. Ship decisions and production belong to other roles.
