# PR-003 Applicability Register

**PR:** #3  
**Change class:** F (charter extension)

---

## Charter rules in scope

### Change classification (§6)

| Rule | Status | Evidence |
|------|--------|----------|
| Class F stated | ✓ | PLAN.md:6 |
| ADR required for charter change | ✓ | Extends ADR 0003 vocabulary; no new ADR needed (clarification, not new decision) |

### Systems model rules (§16)

| Rule | Applies | Status | Evidence |
|------|---------|--------|----------|
| S1 | Yes — ship-role is agent noun | MET | `agents/ship-role/AGENT.md` has identity + invariants |
| S2 | Yes — ship-role verbs | MET | `agents/ship-role/verbs.md` has I/O contracts + failure modes |
| S3 | Yes — ship-role | MET | `agents/ship-role/AGENT.md` has handoff-in + completion artifact |
| S4 | Yes — ship-role | MET | `agents/ship-role/AGENT.md` has binary success criteria |
| S5 | Yes — ship-role separation | MET | Ship-role has invariant "No self-ship" |
| S6 | N/A | — | Ship-role is not an audit role; has ship authority |

### Confirmation checklist (systems) — §16.8

| Item | Applies | Status | Evidence |
|------|---------|--------|----------|
| CS1 | Yes — ship-role | MET | Identity and invariants declared |
| CS2 | Yes — ship-role verbs | MET | Each verb has input, output, failure mode |
| CS3 | Yes — ship-role | MET | Handoff-in and completion artifact declared |
| CS4 | Yes — ship-role | MET | Success criteria are binary |
| CS5 | Yes — separation | MET | Produce≠Audit≠Ship honored; three distinct agent nouns |
| CS6 | N/A | — | Ship-role is not an audit role |

---

## ADRs in scope

| ADR | Status | Relevance |
|-----|--------|-----------|
| 0001-zero-variance-integrity | Reference | P2-P7 principles; no change |
| 0002-p2-scope | Reference | Defines hub vs adopter scope; no change |
| 0003-systems-extension-agent-nouns | **Modified** | Vocabulary mapping updated (Fitness check → Gate, Adversarial review → Audit) |

---

## Binding matrix rows affected

| Requirement | Surface | Change |
|-------------|---------|--------|
| S1-S6 | reference | Ship-role must satisfy; no matrix row change |
| CS1-CS6 | reference | Ship-role changes must satisfy; no matrix row change |
| P1-P7 | reference/in-force | No change |
| R* | reference/in-force | No change |
| C* | reference/in-force | No change |

**Matrix audit status:** All audits MET (see VERIFY.md command output).

---

## Unbound reference rows (acknowledged)

These rows remain unbound as documented in the binding matrix. This PR does not add false binders:

- S1-S6, CS1-CS6 (no fail-capable binder exists yet)
- P1-P5 (principles; binders are TODO)
- R6, C5 (verb-path binder TODO)
- Most C* items (confirmer-checkable, not CI-automated)

No new unbound rows were added by this PR.
