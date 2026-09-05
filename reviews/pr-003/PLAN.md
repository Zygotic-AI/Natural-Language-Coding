# PR-003 Plan

**PR:** #3 — Close deferred findings from PR #2 adversarial audit  
**Author:** cursor/close-deferred-audit-findings-9be0  
**Date:** 2026-09-05  
**Change class:** F (charter extension)

---

## Goal

Close three deferred findings from the adversarial audit of PR #2:

1. **Standards steward missing Session `load_applicability` verbs** — steward package must expose query verbs so a Session/WU can obtain an applicability register before materialize (default-closed).

2. **Ship noun** — charter/agent model lacks a first-class ship noun (separate from produce and audit). Add the boxed noun definition.

3. **Fitness ≠ audit naming** — ensure fitness/gate language is not conflated with adversarial audit terminology.

---

## Charter §6 Step 2 — Proposal fields

Per charter §6 "Propose (spec, not code)":

### Classification

**Class F** — Charter rule change (§16 systems model extension)

### Nouns touched

| Noun type | Noun | Action |
|-----------|------|--------|
| Agent noun | standards-steward | Add query verb `load-applicability` |
| Agent noun | ship-role | **Create** (new agent noun) |
| Charter section | §16 Systems model | Extend with §16.5 Ship noun, vocabulary clarification |

### Verbs touched

| Agent noun | Verb | Action |
|------------|------|--------|
| standards-steward | `load-applicability` | **Add** (query verb) |
| ship-role | `ratify` | **Add** (new) |
| ship-role | `merge` | **Add** (new) |
| ship-role | `release` | **Add** (new) |
| ship-role | `waive-finding` | **Add** (new) |

### Goals touched

None. This change is agent noun / charter extension, not use-case orchestration.

### Workflows touched

None.

### Draft contracts

All verb contracts defined in:
- `agents/standards-steward/verbs.md` (load-applicability)
- `agents/ship-role/verbs.md` (ratify, merge, release, waive-finding)

Each verb has:
- Input contract (YAML schema)
- Output contract (YAML schema)
- Failure mode (error codes)

### Invariants that must hold

| Invariant | Location | Check |
|-----------|----------|-------|
| Steward never ships | `agents/standards-steward/AGENT.md` | Shipping authority = None |
| Auditor never ships | `agents/adversarial-auditor/AGENT.md` | Shipping authority = None |
| Ship follows audit | `agents/ship-role/AGENT.md` invariant 1 | Handoff-in requires audit complete |
| No self-ship | `agents/ship-role/AGENT.md` invariant 5 | Verb failure mode SELF_SHIP |
| Query ≠ produce | `agents/standards-steward/verbs.md` | Separation guarantee section |

### Explicit non-goals

| Non-goal | Reason |
|----------|--------|
| New binding-matrix requirements S7+ | Ship-role satisfies existing S1-S6 |
| Machine-readable JSON Schema | Future work (TODO) |
| Session gate wiring | Future work (TODO, marked OUT OF SCOPE) |
| Binders for S1-S6, CS1-CS6 | Future work (TODO) |
| Changes to R1-R25, C1-C24 | Software BBP unchanged |

### Test names that will prove it

No automated tests added (charter/agent packages are markdown). Verification via:

| Check | Command |
|-------|---------|
| Matrix audits | `python3 tools/audit-binding-matrix.py` |
| Package structure | `bash reviews/pr-003/verify.sh` |

### Impact list

| Changed boundary | Callers affected |
|------------------|------------------|
| standards-steward verbs | Sessions calling steward (none yet; new capability) |
| ship-role package | Ratify/merge workflows (none yet; new capability) |
| §16 vocabulary | ADR 0003, DESCRIBE.md (both updated) |
| §16 section numbers | §16.6 Rules, §16.7 Checklist (renumbered) |

---

## Success criteria

| ID | Criterion | Binary check |
|----|-----------|--------------|
| SC-1 | `agents/standards-steward/verbs.md` contains `load-applicability` verb | grep confirms |
| SC-2 | `load-applicability` has input, output, failure mode | grep confirms 3 sections |
| SC-3 | `load-applicability` has separation guarantee | grep confirms section |
| SC-4 | CHARTER.md §16.5 defines Ship noun | grep confirms section |
| SC-5 | §16 section numbers consecutive (16.1–16.7) | grep confirms no gaps |
| SC-6 | `agents/ship-role/AGENT.md` exists with §16.2 elements | file exists + grep |
| SC-7 | `agents/ship-role/verbs.md` has 4 verbs with I/O contracts | grep count = 4 |
| SC-8 | CHARTER.md §16.1 distinguishes Gate from Audit | grep confirms both terms |
| SC-9 | ADR 0003 vocabulary matches §16.1 | grep confirms Gate/Audit |
| SC-10 | ADR 0003 Consequences mentions ship-role | grep confirms |
| SC-11 | Existing rule numbers preserved | no R*/S*/C*/P* renumbered |
| SC-12 | `python3 tools/audit-binding-matrix.py` exits 0 | command output RESULT:MET |

---

## Out of scope

| Item | Reason |
|------|--------|
| New binding-matrix requirements S7+ for ship-role | Ship-role is an agent noun; existing S1-S6 apply. No new rules needed. |
| Machine-readable JSON Schema for verb contracts | TODO item; future work |
| Session gate wiring | TODO item marked OUT OF SCOPE |
| Binders for S1-S6, CS1-CS6 | TODO item; existing rows remain unbound reference |
| Changes to software BBP rules (R1-R25, C1-C24) | Only systems model (§16) extended |
