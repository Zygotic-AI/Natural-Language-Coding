# PR-004 Boundary I/O Declarations

## New boundaries introduced

### 1. `complete-produce` (standards-steward verb)

**Input:**
```yaml
artifact_path: string (required)
package_path: string (required)
classification: enum [A, B, C, D, E, F] (optional)
```

**Output:**
```yaml
status: enum [complete, incomplete]
handoff_token: string (only if complete)
missing: array of enum [PLAN, APPLICABILITY, BOUNDARY_IO, ADVERSARIAL_NOTES, VERIFY_SCRIPT] (only if incomplete)
```

**Failure mode:** Returns error result with code `ARTIFACT_NOT_FOUND | PACKAGE_NOT_FOUND | PACKAGE_MISSING`

---

### 2. `preflight-fitness-handoff` (quality-architect verb)

**Input:**
```yaml
artifact_path: string (required)
package_path: string (required)
handoff_token: string (optional)
```

**Hard gate:** Package completeness (S7), not token presence. Token is convenience; preflight validates package paths directly when token absent.

**Output:**
```yaml
status: enum [ready, handoff_refused]
defect_log: object (only if handoff_refused)
  missing: array of enum [PLAN, APPLICABILITY, BOUNDARY_IO, ADVERSARIAL_NOTES, VERIFY_SCRIPT]
  reason: string
```

**Failure mode:** Returns error result with code `ARTIFACT_NOT_FOUND | PACKAGE_NOT_FOUND`

---

### 3. `score-fitness` (quality-architect verb)

**Input:**
```yaml
artifact_path: string (required)
preflight_status: enum [ready] (required)
checklist_scope: enum [software, systems, both] (default: software)
change_class: enum [A, B, C, D, E, F] (optional)
```

**Output:**
```yaml
status: enum [MET, FAIL]
checklist_results: array of {item_id, status, evidence}
blocking_failures: array of string (item ids)
```

**Failure mode:** Returns error result with code `ARTIFACT_NOT_FOUND | PREFLIGHT_NOT_READY | SELF_SCORE`

---

## Modified boundaries

### adversarial-auditor handoff-in

**Added conditions:**
- Preflight ready: Fitness preflight returned `ready` (not `handoff_refused`)
- Fitness scored: Fitness `score-fitness` returned `MET` or `FAIL` (not skipped)

---

## Boundary vocabulary

| Term | Input/Output | Boundary |
|------|--------------|----------|
| `handoff_refused` | Output | preflight-fitness-handoff |
| `ready` | Output | preflight-fitness-handoff |
| `complete` | Output | complete-produce |
| `incomplete` | Output | complete-produce |
| `MET` | Output | score-fitness |
| `FAIL` | Output | score-fitness |
| `handoff_token` | Output/Input | complete-produce / preflight-fitness-handoff |
