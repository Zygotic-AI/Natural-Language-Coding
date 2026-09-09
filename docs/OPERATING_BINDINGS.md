# Operating Bindings Index

Index of operating policies from the companion BBA-Bindings repository. This document provides discoverability without duplicating full binding text.

## Architecture note

**BBA** (Boundary-Based Architecture) is the roof doctrine — confirmable rules that define how boundaries, handoffs, and integrity work. BBA lives in this repo (`CHARTER.md`, `integrity/`, `agents/`).

**Bindings** is the operating policy map consumed by agent processes — concrete P-series policies that wire refuse criteria, evidence requirements, and handoff contracts to executable gates. Bindings live in the companion repo.

## Locating BINDING-MAP

The authoritative operating bindings live in the companion repository:

- **Primary location:** `richardpickett/BBA-Bindings` on GitHub
- **BINDING-MAP:** Root or `policies/BINDING-MAP.md` in that repository
- **PR links:** Individual policies reference PRs on that repo (e.g., `BBA-Bindings/pull/9` for P-030)

If the companion repo is inaccessible or the URL has changed, search the org for repositories named `BBA-Bindings`, `Bindings`, or containing `BINDING-MAP`.

## Operating policy index (P-016…P-031 class)

Policies in this class govern handoff gates, evidence requirements, and refuse criteria consumed by agent processes.

| Policy | Name | Purpose |
|--------|------|---------|
| **P-015** | Bot-auditable packages | All PR packages must be fully bot-auditable; no human reviewer in the loop |
| **P-016** | Produce→fitness handoff default-closed | Producers cannot claim ready without complete produce package; `handoff_refused` not `FAIL` |
| **P-020** | SSOT exit evidence required | Produce packages require `ssot_leaf_ids` + `ssot_exit_status`; missing evidence triggers refuse |
| **P-024** | Decision grain boundary | (Confirm in BBA-Bindings) Granularity at which decisions are recorded and traced |
| **P-030** | Raise-readiness refuse | R3/R4 checks; 15855 without §7/R3/R4 must REFUSE at raise-readiness handoff |
| **P-031** | Promote packet refuse | (Confirm in BBA-Bindings) Incomplete promote packets refuse Ship handoff |

### Policy details referenced in this repo

**P-015 (Bot-auditable packages)**
- Referenced in: `reviews/README.md`
- Aligned with: KD-010 quality north star
- Richard does NOT review PRs; packages must be bot-auditable

**P-016 (Produce→fitness handoff default-closed)** — ADR 0004
- Charter rule: S7, CS7
- Handoff: `handoff_refused` (produce-incomplete) ≠ `FAIL` (content defect)
- Aligned with: S5 Produce ≠ Audit ≠ Ship

**P-020 (SSOT exit evidence)** — ADR 0005
- Charter rule: S8, CS8
- Evidence: `ssot_leaf_ids` (opaque leaf ids) + `ssot_exit_status` (non-empty exit state)
- Refuse: Fitness refuses MET; adversarial audit refuses PASS
- Same refuse class as P-016

**P-030 (Raise-readiness refuse)**
- Binder: [BBA-Bindings/pull/9](https://github.com/richardpickett/BBA-Bindings/pull/9)
- Fixture: 15855 without §7/R3/R4 must FAIL any raise-readiness handoff
- G2: refuse-wired via P-030

## Cross-references

- [`CHARTER.md`](../CHARTER.md) — roof doctrine; confirmable rules
- [`integrity/binding-matrix.json`](../integrity/binding-matrix.json) — local requirement → audit → binder matrix
- [`integrity/BOUNDARY.md`](../integrity/BOUNDARY.md) — Boundary/Handoff nouns; P-030 fixture
- [`adrs/0004-produce-fitness-handoff.md`](../adrs/0004-produce-fitness-handoff.md) — P-016 decision
- [`adrs/0005-ssot-exit-evidence.md`](../adrs/0005-ssot-exit-evidence.md) — P-020 decision
