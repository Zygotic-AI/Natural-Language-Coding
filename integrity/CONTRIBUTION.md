# Contribution

SSOT for the shared docs standard and Contribution Gate in Boundary-Based Programming. Governs how content is added or amended to this repository.

Rationale: charter §5.8 practice integrity (zero variance, hard gates); [`LEXICON.md`](LEXICON.md) locked definitions.

---

## Shared Docs Standard

Every SSOT document in this repository follows the shared docs standard. The standard has seven components:

### 1. Structure

Consistent layout across document types:

| Section | Required? | Purpose |
|---------|-----------|---------|
| Title (H1) | Yes | Document identity |
| Preamble | Yes | SSOT declaration, rationale, related links |
| Definition | Conditional | Core semantics (required for noun documents) |
| Refuse criteria | Conditional | What causes FAIL/REFUSE (required for gate/handoff documents) |
| Incomplete-packet fixture | Conditional | Example that must FAIL (required for gate/handoff documents) |
| Confirmation checklist | Conditional | Per-change verification (required when contribution needs gating) |
| Cross-references | Yes | Links to related documents |

### 2. Naming

Predictable paths and slugs:

| Content type | Path pattern | Slug rules |
|--------------|--------------|------------|
| ADR | `adrs/NNNN-short-slug.md` | Four-digit sequence, lowercase hyphenated slug |
| Integrity doc | `integrity/NAME.md` | UPPERCASE for primary nouns (GATE, BOUNDARY, LEXICON) |
| Agent noun | `agents/<name>/AGENT.md` | Lowercase folder, AGENT.md entry point |
| Audit | `integrity/audits/A-<id>.md` | A- prefix, uppercase id |
| Example | `examples/<name>/README.md` | Lowercase folder, README.md entry point |

Superseded documents retain their path with a `<!-- SUPERSEDED by ... -->` marker at the top (charter R22).

### 3. Lexicon

Terms from [`LEXICON.md`](LEXICON.md) carry stable meanings:

- **Action, Atomic action, Compound action** — units of work with gates
- **Content type** — first-class artifact class (ADR, integrity doc, agent noun, audit, example)
- **Contribution / add-X** — gated action of adding/amending type X
- **Shared docs standard** — this standard
- **Type recipe** — prescribed steps + gate criteria for type X
- **Contribution Gate** — refuse-wired gate for contributions
- **Audit receipt** — gate evidence produced by an audit; audit ≠ gate
- **Gate** — binary enforcement checkpoint; gate ≠ audit

When prose uses these terms, readers may rely on the lexicon definition without re-reading the full standard.

### 4. Evidence

Claims cite sources:

| Claim type | Evidence form |
|------------|---------------|
| Requirement met | Audit id and outcome (e.g., "A-P4 met") |
| Binder exists | Binder path or PR link |
| Fixture fails | Fixture id and expected outcome |
| Role responsibility | Role name from agent noun or SOP |

Unsourced claims are incomplete work.

### 5. Role Language

SSOT surfaces use role names only. Person names do not appear.

| Surface | Rule |
|---------|------|
| Charter | Role names only |
| Integrity docs | Role names only |
| Agent nouns | Role names only |
| SOP tables | Role names only |
| ADR Deciders | Role names or pseudonymous handle (not real names in SSOT copy) |

**Rationale:** SSOT is durable; person assignments change. The SSOT carries the role; a separate assignment register (outside SSOT) maps roles to people.

### 6. Incomplete-Packet Refuse

Every gate or handoff tip documents:

1. **Refuse criteria** — enumerated conditions that cause REFUSE
2. **Incomplete-packet fixture** — a concrete example that exercises the refuse path

A tip without both is incomplete. See [`GATE.md`](GATE.md) design rule: refuse + incomplete-packet fixture in the same tip.

### 7. Supersede Rules

Superseded content is marked, not deleted (charter R22).

| Action | How |
|--------|-----|
| Supersede a document | Add `<!-- SUPERSEDED by <path> as of <date> -->` at top; retain file |
| Supersede a section | Add `**SUPERSEDED** by [<new-section>](<link>).` inline; retain text |
| Supersede an ADR | Status line: `Status: Superseded by ADR NNNN` |

Deletion removes audit trail. Mark-as-superseded preserves context.

---

## Contribution Gate

The Contribution Gate is the refuse-wired gate that governs all add-X contributions. It meets the all-required PASS fitness bar (G1–G4) from [`GATE.md`](GATE.md).

### Refuse Criteria

A contribution is **REFUSED** if any of the following hold:

| # | Refuse condition | Rationale |
|---|------------------|-----------|
| CG-R1 | Shared docs standard not met | Structure, naming, lexicon, evidence, role language, incomplete-packet refuse, or supersede rules violated |
| CG-R2 | Type recipe for content type X not followed | Each content type has prescribed steps; skipping a step = incomplete |
| CG-R3 | Type recipe for content type X does not exist | Cannot add-X without a recipe; publish recipe first |
| CG-R4 | Person names appear in SSOT surfaces | Role language only; no person names |
| CG-R5 | Required incomplete-packet fixture missing | Gate/handoff tips require a fixture |
| CG-R6 | SSOT exit evidence missing | `ssot_leaf_ids` + `ssot_exit_status` required (S8, P-020) |
| CG-R7 | Gate criteria incomplete (G1–G4 not addressed) | Gate documents must address all four criteria |

### Gate Outcomes

| Outcome | Meaning |
|---------|---------|
| **PASS** | All refuse criteria clear; contribution advances |
| **REFUSE** | One or more refuse criteria triggered; contribution blocked |

There is no WARN, PROVISIONAL, or SOFT-PASS.

### All-Required PASS Bar (G1–G4)

The Contribution Gate satisfies G1–G4:

| Criterion | Evidence |
|-----------|----------|
| **G1** Incomplete cannot PASS | CG-R1 through CG-R7 enumerate incomplete conditions → REFUSE |
| **G2** Machine-checkable or refuse-wired | Structure checks can lint; recipe presence checked by index; person-name checks can grep; missing SSOT exit evidence checked by fitness |
| **G3** Incomplete-packet fixture fails | See fixture below |
| **G4** PASS needs no human redo | PASS means contribution is complete per type recipe; no follow-up fix required |

---

## Incomplete-Packet Fixture: add-X without Type Recipe

Reference case for the Contribution Gate.

### Scenario

A producer attempts to add content type **"runbook"** to the repository. The contribution includes:
- File at `runbooks/deploy-prod.md`
- Follows general markdown style
- No type recipe exists for "runbook" in `content-types/HOW-TO-ADD.md`

### Required Outcome

**REFUSE** under CG-R3 (type recipe does not exist).

The Contribution Gate cannot evaluate whether the contribution is complete without a type recipe. The producer must first contribute the type recipe for "runbook" (which itself passes the Contribution Gate for type-recipe as a content type), then contribute the runbook instance.

### Fixture Verification

| Refuse criterion | Applies? | Outcome |
|------------------|----------|---------|
| CG-R1 | Maybe (no recipe to check against) | Defer to CG-R3 |
| CG-R2 | Cannot evaluate (no recipe) | Defer to CG-R3 |
| CG-R3 | **Yes** — no type recipe for "runbook" | **REFUSE** |
| CG-R4 | Maybe | Not primary blocker |
| CG-R5 | N/A (not a gate/handoff tip) | — |
| CG-R6 | Applies separately at fitness | — |
| CG-R7 | N/A (not a gate document) | — |

**Conclusion:** A contribution for content type X without a type recipe for X is incomplete. The Contribution Gate refuses it.

### Second Fixture: add-ADR with Person Names

**Scenario:** A producer contributes `adrs/0099-new-decision.md` with:
- Correct path pattern
- ADR type recipe steps followed
- `Deciders: Jane Doe, Bob Smith` (real names in SSOT surface)

**Required outcome:** **REFUSE** under CG-R4 (person names in SSOT).

**Fix:** Use role names (`Deciders: Quality Architect, Standards Steward`) or pseudonymous handles. Person-to-role mapping lives outside SSOT.

---

## Contribution Gate Incomplete-Packet Hunt

The adversarial half: can an incomplete contribution still slip through?

| Slip path | Blocked by |
|-----------|------------|
| Add-X with no recipe | CG-R3 |
| Add-X skipping recipe steps | CG-R2 |
| SSOT with person names | CG-R4 |
| Gate tip without refuse+fixture | CG-R5, CG-R7 |
| Missing SSOT exit evidence | CG-R6 (enforced at fitness) |
| Violates structure/naming | CG-R1 |

No known incomplete-packet slip remains. If a slip is discovered, it becomes a blocker finding → Contribution Gate amended.

---

## Confirmation Checklist (Contribution-Specific)

For any contribution (add-X) to this repository:

- [ ] CC1. Content type X has a type recipe in `content-types/HOW-TO-ADD.md`.
- [ ] CC2. Type recipe steps for X are followed.
- [ ] CC3. Shared docs standard met (structure, naming, lexicon, evidence, role language, incomplete-packet refuse, supersede rules).
- [ ] CC4. No person names in SSOT surfaces.
- [ ] CC5. If artifact is a gate/handoff tip: refuse criteria + incomplete-packet fixture documented.
- [ ] CC6. If artifact is a gate tip: G1–G4 addressed.
- [ ] CC7. SSOT exit evidence present (`ssot_leaf_ids`, `ssot_exit_status`).
- [ ] CC8. Cross-references updated (DESCRIBE.md, AGENTS.md, integrity/README.md, relevant indexes).

---

## Cross-references

- [`LEXICON.md`](LEXICON.md) — locked definitions (Action, Content type, Type recipe, Contribution Gate, etc.)
- [`GATE.md`](GATE.md) — gate noun, G1–G4 fitness bar, incomplete-packet hunt
- [`BOUNDARY.md`](BOUNDARY.md) — boundary and handoff nouns
- [`PRINCIPLES.md`](PRINCIPLES.md) — practice integrity principles (P1–P7)
- [`../content-types/HOW-TO-ADD.md`](../content-types/HOW-TO-ADD.md) — type recipe index
- [`../CHARTER.md`](../CHARTER.md) §5.8 — practice integrity rules
- [`../CHARTER.md`](../CHARTER.md) R22 — superseded content marked, not deleted
- [`../AGENTS.md`](../AGENTS.md) — standing instructions for agents
