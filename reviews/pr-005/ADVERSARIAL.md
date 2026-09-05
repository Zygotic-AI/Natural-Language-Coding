# Self-adversarial notes — SSOT exit evidence abstract delta

Pre-submission adversarial review by the producer against the charter and principle lock.

## SSOT exit evidence (P-020 dogfood)

This package dogfoods the **abstract** P-020 contract only:

```yaml
ssot_leaf_ids:
  - "3d29d973-ccd7-8158-a1c2-e8d46be9bbef"
ssot_exit_status: "in progress"
```

Opaque leaf id as data. No product field labels. Parked prior leaf is not dogfooded.

---

## Architecture FAIL on prior Notion surface

| Claim | Disposition |
|-------|-------------|
| Prior MET on Notion-named fields clears architecture fitness | **No** — superseded |
| Notion-named fields in BBA charter/agent verbs | **Architecture-scope FAIL** under tool-agnostic lock |
| This delta restores tool-agnostic contract | Target of this change |

Principle lock cited: BBA = architecture definition; no Notion / MCP / Cursor / Grok product bindings in charter, AGENTS.md, or agent verb field names. Bindings repo is out of scope.

---

## Checklist against charter rules

### R26 / P1–P7

- [x] **P1 Stand-alone / tool-agnostic:** Abstract field names; no product brand as required vocabulary
- [x] **P2 Zero variance:** Binary refuse outcomes preserved
- [x] **P3 Hard gates:** Missing evidence → `handoff_refused` / refuse MET / refuse PASS
- [x] **P4 Hard boundary I/O:** Verb contracts declare abstract I/O + failure mode
- [x] **P5 Binary audits:** A-S8 / A-CS8 retained, rewritten
- [x] **P6 Unbound listed:** S8/CS8 remain unbound reference
- [x] **P7 Promote-only-when-bindable:** No false binders

### S5 / S6 / S7

- [x] Produce ≠ Audit ≠ Ship honored
- [x] Audit roles still exclude ship verbs
- [x] S7 refuse class extended by S8 (same class as P-016)

### S8 / CS8 (this delta)

- [x] Prose = task/board SSOT exit evidence
- [x] Fields = `ssot_leaf_ids` + `ssot_exit_status`
- [x] Missing enum = `SSOT_EXIT_EVIDENCE`
- [x] Error = `SSOT_EVIDENCE_MISSING`
- [x] Package dogfoods abstract fields above

---

## Potential holes

### Hole 1: Unbound S8/CS8

**Issue:** Still no CI binder.  
**Mitigation:** Intentional (P7). Reference surface until bindable.  
**Reviewer question:** Confirm reference/unbound remains correct.

### Hole 2: Opaque leaf shape

**Issue:** Leaf ids are opaque strings; no product API validation in BBA.  
**Mitigation:** Correct for architecture repo; API validation belongs in bindings/implementation, not charter.  
**Reviewer question:** Is non-empty opaque leaf (≥1) sufficient for A-CS8?

### Hole 3: Free-form `ssot_exit_status`

**Issue:** Non-empty string, no enum.  
**Mitigation:** Board vocabularies vary by SSOT; hard gate is non-empty.  
**Reviewer question:** Keep free-form, or document common examples as non-normative?

### Hole 4: Residual R1 from prior Notion PASS (envelope FAIL vs error)

**Issue:** score/adversarial refusal envelope wording may still differ (FAIL vs `SSOT_EVIDENCE_MISSING` error).  
**Mitigation:** Primary path (`handoff_refused` + `SSOT_EXIT_EVIDENCE`) agrees; optional cleanup post-land. Non-blocking if no soft-pass path exists.

---

## Self-adversarial rebuttal

This change fixes an architecture defect (product binding in BBA) while preserving the fail-closed evidence gate. Holes 1–3 are known unbound/reference limitations, not defects. Hole 4 is optional envelope alignment.

Dogfood:

- `ssot_leaf_ids`: `["3d29d973-ccd7-8158-a1c2-e8d46be9bbef"]`
- `ssot_exit_status`: `"in progress"`
