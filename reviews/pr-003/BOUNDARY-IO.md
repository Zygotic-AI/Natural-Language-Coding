# PR-003 Boundary I/O Audit

**PR:** #3  
**Purpose:** Document each noun/verb boundary crossed with input → output artifact pointers.

---

## Boundaries crossed

### 1. standards-steward agent noun — add verb

**Boundary:** `agents/standards-steward/verbs.md`  
**Action:** Add `load-applicability` query verb

| Element | Input | Output |
|---------|-------|--------|
| Verb name | Finding 1 requirement | `load-applicability` |
| Input contract | Scope request schema | `agents/standards-steward/verbs.md:34-58` |
| Output contract | Applicability register schema | `agents/standards-steward/verbs.md:62-108` |
| Failure mode | Error codes | `agents/standards-steward/verbs.md:112-123` |
| Separation guarantee | No produce leak requirement | `agents/standards-steward/verbs.md:127-133` |

**Verification:** Verb has all three required elements (S2): input contract ✓, output contract ✓, failure mode ✓

---

### 2. standards-steward AGENT.md — update verb table

**Boundary:** `agents/standards-steward/AGENT.md`  
**Action:** Add query/produce verb categorization

| Element | Input | Output |
|---------|-------|--------|
| Query verbs table | New verb list | `agents/standards-steward/AGENT.md:23-28` |
| Produce verbs table | Existing verbs | `agents/standards-steward/AGENT.md:32-38` |

---

### 3. Charter §16 — add Ship noun

**Boundary:** `CHARTER.md` §16  
**Action:** Insert §16.5 Ship noun definition

| Element | Input | Output |
|---------|-------|--------|
| Identity | Ship role requirements | `CHARTER.md:685-689` |
| Invariants | Ship invariant list | `CHARTER.md:691-700` |
| Verbs | Ship verb table | `CHARTER.md:702-709` |
| Handoff-in | Preconditions | `CHARTER.md:713-718` |
| Completion artifact | Ship record | `CHARTER.md:720-723` |
| Success criteria | Binary criteria | `CHARTER.md:725-731` |

**Section renumbering:**
- §16.5 Rules → §16.7 Rules
- §16.6 Confirmation → §16.8 Confirmation

---

### 4. ship-role agent noun — create package

**Boundary:** `agents/ship-role/` (new)  
**Action:** Create agent noun package

| Element | Input | Output |
|---------|-------|--------|
| AGENT.md | §16.2 + §16.5 requirements | `agents/ship-role/AGENT.md` (66 lines) |
| verbs.md | Ship verb contracts | `agents/ship-role/verbs.md` (303 lines) |

**Package structure verification:**

```
agents/ship-role/
├── AGENT.md     # Identity, invariants, handoff-in, completion, success criteria
└── verbs.md     # ratify, merge, release, waive-finding with I/O contracts
```

---

### 5. Charter §16.1 — vocabulary clarification

**Boundary:** `CHARTER.md` §16.1 vocabulary mapping  
**Action:** Distinguish Gate from Audit

| Element | Before | After |
|---------|--------|-------|
| Row 7 | `Fitness check \| Audit — binary ops vs defects` | `Fitness check \| Gate — automated enforcement` |
| Row 8 | (none) | `Adversarial review \| Audit — role-based review` |
| Clarification | (none) | Paragraph explaining Gate ≠ Audit |

**Output:** `CHARTER.md:642-651`

---

### 6. ADR 0003 — vocabulary update

**Boundary:** `adrs/0003-systems-extension-agent-nouns.md`  
**Action:** Update vocabulary mapping to match §16.1

| Element | Before | After |
|---------|--------|-------|
| Fitness check row | `Audit (binary ops vs defects)` | `Gate (automated enforcement)` |
| Adversarial review row | (none) | `Audit (role-based review)` |

**Output:** `adrs/0003-systems-extension-agent-nouns.md:30-31`

---

### 7. Documentation updates

**Boundaries:** `agents/README.md`, `DESCRIBE.md`  
**Action:** Add ship-role, terminology clarification

| File | Change | Output location |
|------|--------|-----------------|
| `agents/README.md` | Add ship-role row + Produce≠Audit≠Ship summary | Lines 14-17 |
| `DESCRIBE.md` | Add ship-role path | Line 37 |
| `DESCRIBE.md` | Add terminology section | Lines 53-59 |

---

## Summary

| Boundary type | Count | All have I/O declared |
|---------------|-------|----------------------|
| Agent noun verb | 1 added | ✓ |
| Agent noun package | 1 created | ✓ (4 verbs, all with I/O) |
| Charter section | 2 modified | N/A (prose) |
| ADR | 1 modified | N/A (prose) |
| Documentation | 2 modified | N/A (prose) |
