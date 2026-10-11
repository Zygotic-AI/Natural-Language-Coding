# ADR 0051 — Hub-own produce compiles NLC principles

- Status: Proposed
- Date: 2026-10-11
- Deciders: Human manager
- Class: F (integrity / hub produce), A (release stabilization scope)
- Corpus: nlc
- RCA: RCA 4 (agents weakening checks), root confirmed by the human manager 2026-10-11; the RCA record is kept outside this repository.

## Context

During v0.3.0 stabilization, hub material work repeatedly reached CI MET by weakening fitness tools, broadening exemptions, rewriting approval receipts, or self-referential checks—while roadmap finish lines described **properties** the checks were meant to prove. The root cause (confirmed by the human manager): hub-own produce did not compile [MANIFESTO.md](../MANIFESTO.md) principles as compile-time sub-goals; **CI green** acted as the terminal finish line.

RCA 4 remediation (approved, amended): bind **SG1–SG3** only; drop SG4 gate-mutation suites (re-judging gate logic) in favor of the human manager’s **rule against regress** and **owner-ratified known-bad cases** on each codified constraint.

## Top-line goal (compile-time intent)

**G0 — `hub_own_integrity`:** All work on the NLC hub itself meets NLC's principles.

- **Kind:** [goal](../docs/TERMS.md#goal) (compile-time intent for hub material changes: stabilization, integrity surfaces, gate-set edits, cloud-agent produce on this repository).
- **Default:** incomplete until sub-goals **SG1**, **SG2**, and **SG3** are each MET.
- **Actors:** human manager (ratify policies and known-bad cases), produce role (emit), adversarial auditor role (counterpoint), [gates](../docs/TERMS.md#gate) ([verify](../docs/TERMS.md#verify) on Candidates).

Sub-goals below use only [nouns](../docs/TERMS.md#noun), [verbs](../docs/TERMS.md#verb), [adjectives](../docs/TERMS.md#adjective), and [goals](../docs/TERMS.md#goal). **Verify** runs on a **Candidate** (produce package, gate-set member bytes, or known-bad fixture); there is no separate “test” type.

## Rule against regress (applies to all codified constraints under this ADR)

1. A [gate](../docs/TERMS.md#gate) may grade **only work** or a **work product**. It may **never** judge another check’s **quality or validity** (logic, exemptions, or whether the check is “good”).
2. **Completion confirmation (allowed):** A gate whose **only** job is to confirm that a prior step **completed**—so the next step may run—is valid. It must not re-judge or re-certify the prior check. Example: step 2 must not run until step 1’s final QA check is **complete**; the confirmation gate asks *did step 1 complete?*, not *was step 1’s check correct?*
3. **Forbidden (“check on a check”):** No codified constraint may MET by running one fitness or assert tool to evaluate another fitness or assert tool’s **correctness** (including mutation landmines that re-grade gate logic).
4. **Known-bad case (required):** Every codified constraint introduced or amended under this ADR carries an **owner-ratified known-bad Candidate** (fixture bytes or pinned specimen) declared in the ADR or an integrity SSOT list at ratification time. **Nothing gates that known-bad case**—no wrapper fitness tool, no meta-landmine. [Verify](../docs/TERMS.md#verify) on the constraint runs against the known-bad Candidate directly and must REFUSE or NOT_MET for the named reason.
5. This replaces SG4 gate-mutation landmines that re-judged gate logic via another check.

## Gate set (paths)

**Gate-set member** means any path that grades hub or adopter work products in CI or `./nlc verify` releasable profiles:

| Category | Paths (repo-relative) |
|---|---|
| Hub fitness nouns | `tools/nouns/fitness_*/**` |
| Hub assert nouns | `tools/nouns/assert_*/**` |
| Thin fitness adapters | `tools/fitness-*.py` |
| Thin assert adapters | `tools/assert-*.py` |
| Exclusion registries | `integrity/*EXCLUSIONS*.md`, `integrity/*-exclusions*.json` (when present) |
| Releasable profile SSOT | `integrity/releasable-gates.json` |

Edits under `docs/history/`, `docs/rca/`, and `reviews/` are provenance, not gate-set members, unless promoted into the table above.

---

## SG1 — Property leaf goals; CI green is never terminal

| Layer | Id | Statement |
|---|---|---|
| **Principle** | Manifesto P5 — Dogfood | “**Dogfood or don't preach.** The hub must pass its own gates — BBA/BBP at the foundation of *emit*, under the NLC roof — or the claim is unproven.” ([`MANIFESTO.md`](../MANIFESTO.md) lines 58–59) |
| **Principle** | Manifesto gate thesis | “A red gate is a success. A green file that no longer matches intent is the defect.” ([`MANIFESTO.md`](../MANIFESTO.md) line 19) |
| **Policy** | **P-HUB-OWN** | Hub material produce is first-class compile scope: principles P2–P7 and the gate thesis bind to hub-own packages with the same force as adopter emit. |
| **Standard** | **S-HUB-GOAL-TREE** | Every hub material `.nlc/produce-package.json` declares a goal tree for **G0** with **property leaf goals** (opaque ids + text) copied from roadmap “done when” / finish lines. |
| **Rule** | **R-HUB-EXIT** | Terminal package exit may not name **only** CI MET, fitness green, or GitHub Actions success; every property leaf goal must MET or REFUSE with evidence. |
| **Rule** | **R-HUB-BRIEF-FORBID-WEAKEN** | Stabilization and cloud-agent briefs must name property leaf goals and **forbid** weakening a check, broadening exemptions, or rewriting receipts to obtain MET. |
| **Codified constraint** | (to implement) `fitness-hub-own-principle-subgoals`, `fitness-hub-own-property-exit`, extend `assert-produce-handoff-refused` hub profile | Default-closed [verify](../docs/TERMS.md#verify) on produce-package Candidate. Each carries an owner-ratified known-bad case per **Rule against regress**. |

---

## SG2 — Gate-set edits require owner ratification receipt (ADR 0047 pattern)

| Layer | Id | Statement |
|---|---|---|
| **Principle** | Integrity P3 — Hard gates | “Every step and every [action](../docs/TERMS.md#action) has a hard [gate](../docs/TERMS.md#gate). The [gate](../docs/TERMS.md#gate) outcome is only **complete** or **incomplete**.” ([`integrity/PRINCIPLES.md`](../integrity/PRINCIPLES.md) lines 20–22) |
| **Principle** | Charter R30 | “Every prescribed step or [action](../docs/TERMS.md#action) has a hard [gate](../docs/TERMS.md#gate) whose only outcomes are complete or incomplete, with evidence.” ([`CHARTER.md`](../CHARTER.md) line 297) |
| **Policy** | **P-GATE-SET-RATIFY** | Gate-set member bytes are ratified; content hash change requires human manager receipt before merge. |
| **Standard** | **S-GATE-SET-REGISTRY** | Registry `integrity/gate-change-receipts.json` keys each gate-set member path to SHA-256 of file contents (or declared bundle hash for split nouns), ratifier role, and date. |
| **Rule** | **R-GATE-SET-NO-SILENT-WEAKEN** | A produce package that changes gate-set member bytes without a matching receipt is incomplete (handoff REFUSE). |
| **Codified constraint** | (to implement) `fitness-gate-change-receipt` | **Completion confirmation** (not a quality judgment on gate logic): confirms the gate-set bytes in the tree match the bytes the human manager ratified in `integrity/gate-change-receipts.json` (ratification is the start of the chain). NOT_MET when diff touches gate-set paths and receipt missing or hash mismatch; it does **not** evaluate whether a gate-set member’s grading logic is correct. Known-bad: diff without receipt Candidate. |

### Amendment to [ADR 0047](0047-adr-approval-receipts.md)

[ADR 0047](0047-adr-approval-receipts.md) remains the SSOT for **ADR file** approval receipts in `integrity/adr-approval-receipts.json`. This ADR **extends the same receipt pattern** to gate-set members:

1. Separate registry (`integrity/gate-change-receipts.json`); ADR 0047 JSON is unchanged.
2. Same semantics as 0047 §Decision (1)–(3): hash-keyed receipt; edit without new receipt → `receipt_holds` false → hub compile NOT_MET when the codified constraint is wired.
3. Receipt **writing** follows maintainer path after human manager ratification—produce roles do not hand-edit hashes (RCA 4 instance I1 class).

---

## SG3 — Graded party cannot change the grading check without separate reviewer

| Layer | Id | Statement |
|---|---|---|
| **Principle** | [ADR 0003](0003-systems-extension-agent-nouns.md) — Produce ≠ Audit | “Three [agent nouns](../docs/TERMS.md#agent-noun) implement Produce ≠ Audit ≠ Ship” ([`adrs/0003-systems-extension-agent-nouns.md`](0003-systems-extension-agent-nouns.md) line 61) |
| **Policy** | **P-HUB-ROLE-SEP** | On hub material packages, `producer_role` and `adversarial_auditor_role` must differ whenever the diff touches both gate-set members and graded subject paths. |
| **Standard** | **S-HUB-GATE-DIFF** | Gate-set path set and “subject under grade” path set are declared in hub produce profile SSOT under `integrity/` (not ad-hoc per PR). |
| **Rule** | **R-HUB-SAME-PACKAGE-REFUSE** | Same produce package + same actor modifying gate-set and subject → REFUSE (extends planit / verify-deep role separation to hub stabilization). |
| **Codified constraint** | (to implement) `assert-produce-role-separation` hub gate-diff profile | REFUSE on combined diff without adversarial role receipt. Known-bad: single-package gate+subject diff Candidate. |

---

## Decision (summary)

1. Adopt **G0** with sub-goals **SG1**, **SG2**, **SG3** as binding hub-own produce law when this ADR is Accepted.
2. Adopt **Rule against regress** and **known-bad case** requirements for all codified constraints under SG1–SG3.
3. Define **gate set** paths in the table above.
4. Extend [ADR 0047](0047-adr-approval-receipts.md) receipt **pattern** to gate-set registry without merging registries.
5. **Implementation** of codified constraints is follow-on work; this Proposed record does not wire CI.

## Consequences

- When Accepted, version class **minor** (new policy surface on hub produce).
- Stabilization briefs and cloud-agent instructions must align with **R-HUB-BRIEF-FORBID-WEAKEN** and **R-HUB-EXIT** before hub material PRs MET under the new profile.
- Instance re-proof of stabilization PRs (RCA 4 batch 1/2) runs **last**, under SG1–SG3 plus human manager review—not via a separate instance-bundle fitness gate.
- Binding matrix and `integrity/adr-gates.json` rows for new audits are added when codified constraints land (promote-only-when-bindable).

## Rejected

- **SG4 gate-mutation landmine:** re-judges another check’s quality or validity; violates rule against regress §2–3; replaced by owner-ratified known-bad Candidates verified directly on each constraint.
- **CI green as terminal finish line** for hub-own produce.
- **Producer hand-update of gate-change or ADR approval receipts** without ratification event.
- **Single actor** changing gate-set and graded subject in one package without adversarial role.

## Related

- [ADR 0003](0003-systems-extension-agent-nouns.md) — produce ≠ audit ≠ ship
- [ADR 0004](0004-produce-fitness-handoff.md) — produce handoff
- [ADR 0047](0047-adr-approval-receipts.md) — receipt pattern extended for gate set
- [ADR 0050](0050-evidence-identity-content-not-history.md) — verdict pure function of tree + gate set
- [`MANIFESTO.md`](../MANIFESTO.md) — dogfood and gate thesis
- [`integrity/PRINCIPLES.md`](../integrity/PRINCIPLES.md) — P2, P3, P7
