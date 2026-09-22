# Operating Bindings Index

Index of operating policies from the companion [BBA-Bindings](TERMS.md#bba-bindings) repository. This document provides discoverability without duplicating full [binding](TERMS.md#binding) text.

## Architecture note

**[BBA](TERMS.md#bba)** (Boundary-Based Architecture) is the roof doctrine — confirmable rules that define how boundaries, handoffs, and [integrity](TERMS.md#integrity) work. [BBA](TERMS.md#bba) lives in this repo (`CHARTER.md`, `integrity/`, `agents/`).

**Bindings** is the operating policy map consumed by agent processes — concrete P-series policies that wire [refuse](TERMS.md#refuse) criteria, evidence requirements, and [handoff](TERMS.md#handoff) contracts to executable gates. Bindings live in the companion repo.

## Locating BINDING-MAP

The authoritative operating bindings live in the companion repository:

- **Primary location:** `richardpickett/BBA-Bindings` on GitHub
- **BINDING-MAP:** `docs/BINDING-MAP.md` (verified)
- **PR links:** Individual policies reference PRs on that repo (e.g., `BBA-Bindings/pull/9` for P-030)

**Status:** [BBA-Bindings](TERMS.md#bba-bindings) is published (private). Verified BINDING-MAP path: `docs/BINDING-MAP.md`. If the repo URL changes, search the org for repositories named `BBA-Bindings`, `Bindings`, or containing `BINDING-MAP`.

## Operating policy index (P-016…P-031 class)

Policies in this class govern [handoff](TERMS.md#handoff) gates, evidence requirements, and [refuse](TERMS.md#refuse) criteria consumed by agent processes.

| Policy | Name | Purpose |
|--------|------|---------|
| **P-015** | Bot-auditable packages | All PR packages must be fully bot-auditable; no human reviewer in the loop |
| **P-016** | Produce→fitness [handoff](TERMS.md#handoff) [default-closed](TERMS.md#default-closed) | Producers cannot claim ready without complete [produce package](TERMS.md#produce-package); `handoff_refused` not `FAIL` |
| **[P-020](TERMS.md#ssot-exit-evidence)** | [SSOT exit evidence](TERMS.md#ssot-exit-evidence) required | Produce packages require `ssot_leaf_ids` + `ssot_exit_status`; missing evidence triggers [refuse](TERMS.md#refuse) |
| **P-024** | Decision grain | A board leaf is one decision when one Status flip unlocks one value-stream [gate](TERMS.md#gate) for one accountable role with one evidence packet; leaf-create + fitness [refuse](TERMS.md#refuse) duplicates |
| **P-030** | Raise-readiness [refuse](TERMS.md#refuse) | R3/R4 checks; 15855 without §7/R3/R4 must [REFUSE](TERMS.md#refuse) at raise-readiness [handoff](TERMS.md#handoff) |
| **P-031** | Promote release packet [refuse](TERMS.md#refuse) | Incomplete-packet [refuse](TERMS.md#refuse) on promote greenlight/fitness [MET](TERMS.md#met) unless five fields present and valid (`change_ref`, `what_changed`, `prove_steps`, `uat_tip_marker`, `result`); [refuse](TERMS.md#refuse) result fail/blocked |

### Policy details referenced in this repo

**P-015 (Bot-auditable packages)**
- Referenced in: `reviews/README.md`
- Aligned with: KD-010 [quality](TERMS.md#quality) north star
- Human Root-Approver / operator does not review PRs; packages must be bot-auditable

**P-016 (Produce→fitness handoff default-closed)** — [ADR](TERMS.md#adr) 0004
- [Charter](TERMS.md#charter) [rule](TERMS.md#rule): S7, CS7
- [Handoff](TERMS.md#handoff): `handoff_refused` (produce-incomplete) ≠ `FAIL` (content defect)
- Aligned with: S5 [Produce ≠ Audit ≠ Ship](TERMS.md#produce-audit-ship)

**[P-020](TERMS.md#ssot-exit-evidence) (SSOT exit evidence)** — [ADR](TERMS.md#adr) 0005
- [Charter](TERMS.md#charter) [rule](TERMS.md#rule): S8, CS8
- Evidence: `ssot_leaf_ids` (opaque leaf ids) + `ssot_exit_status` (non-empty exit state)
- [Refuse](TERMS.md#refuse): Fitness refuses [MET](TERMS.md#met); adversarial [audit](TERMS.md#audit) refuses PASS
- Same [refuse](TERMS.md#refuse) class as P-016

**P-024 (Decision grain)**
- One board leaf = one decision
- One Status flip unlocks one value-stream [gate](TERMS.md#gate)
- One accountable role with one evidence packet
- Fitness refuses duplicate leaf-create

**P-030 (Raise-readiness refuse)**
- Binder: [BBA-Bindings/pull/9](https://github.com/richardpickett/BBA-Bindings/pull/9)
- Fixture: 15855 without §7/R3/R4 must FAIL any raise-readiness [handoff](TERMS.md#handoff)
- G2: [refuse-wired](TERMS.md#default-closed) via P-030

**P-031 (Promote release packet refuse)**
- [Refuse](TERMS.md#refuse) on promote greenlight/fitness [MET](TERMS.md#met) unless five fields present and valid:
  - `change_ref` — reference to the change being promoted
  - `what_changed` — description of what changed
  - `prove_steps` — verification steps performed
  - `uat_tip_marker` — UAT tip marker for evidence alignment
  - `result` — outcome (refuse if fail/blocked)
- Incomplete packet → [refuse](TERMS.md#refuse) greenlight

## Cross-references

- [`CHARTER.md`](../CHARTER.md) — roof doctrine; confirmable rules
- [`integrity/binding-matrix.json`](../integrity/binding-matrix.json) — local [requirement](TERMS.md#requirement) → [audit](TERMS.md#audit) → binder matrix
- [`integrity/BOUNDARY.md`](../integrity/BOUNDARY.md) — Boundary/Handoff nouns; P-030 fixture
- [`adrs/0004-produce-fitness-handoff.md`](../adrs/0004-produce-fitness-handoff.md) — P-016 decision
- [`adrs/0005-ssot-exit-evidence.md`](../adrs/0005-ssot-exit-evidence.md) — [P-020](TERMS.md#ssot-exit-evidence) decision
