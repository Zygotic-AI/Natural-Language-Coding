# Contribution

SSOT for the [shared docs standard](../docs/TERMS.md#shared-docs-standard) and [Contribution Gate](../docs/TERMS.md#contribution-gate) in [Boundary-Based Programming](../docs/TERMS.md#bbp). Governs how content is added or amended to this repository.

Rationale: [charter](../docs/TERMS.md#charter) §5.8 practice [integrity](../docs/TERMS.md#integrity) (zero variance, hard gates); [`LEXICON.md`](LEXICON.md) locked definitions.

---

## [Shared Docs Standard](../docs/TERMS.md#shared-docs-standard)

Every SSOT document in this repository follows the [shared docs standard](../docs/TERMS.md#shared-docs-standard). The standard has seven components:

### 1. Structure

Consistent layout across document types:

| Section | Required? | Purpose |
|---------|-----------|---------|
| Title (H1) | Yes | Document identity |
| Preamble | Yes | SSOT declaration, rationale, related links |
| Definition | Conditional | Core semantics (required for noun documents) |
| [Refuse](../docs/TERMS.md#refuse) criteria | Conditional | What causes FAIL/REFUSE (required for gate/handoff documents) |
| Incomplete-packet fixture | Conditional | Example that must FAIL (required for gate/handoff documents) |
| Confirmation checklist | Conditional | Per-change verification (required when contribution needs gating) |
| Cross-references | Yes | Links to related documents |

### 2. Naming

Predictable paths and slugs:

| [Content type](../docs/TERMS.md#content-type) | Path pattern | Slug rules |
|--------------|--------------|------------|
| [ADR](../docs/TERMS.md#adr) | `adrs/NNNN-short-slug.md` | Four-digit sequence, lowercase hyphenated slug |
| [Integrity](../docs/TERMS.md#integrity) doc | `integrity/NAME.md` | UPPERCASE for primary nouns (GATE, BOUNDARY, LEXICON) |
| [Agent noun](../docs/TERMS.md#agent-noun) | `agents/<name>/AGENT.md` | Lowercase folder, AGENT.md entry point |
| [Audit](../docs/TERMS.md#audit) | `integrity/audits/A-<id>.md` | A- prefix, uppercase id |
| Example | `examples/<name>/README.md` | Lowercase folder, README.md entry point |

Superseded documents retain their path with a `<!-- SUPERSEDED by ... -->` marker at the top (charter R22).

### 3. Lexicon

Terms from [`LEXICON.md`](LEXICON.md) carry stable meanings:

- **[Action](../docs/TERMS.md#action), [Atomic action](../docs/TERMS.md#atomic-action), [Compound action](../docs/TERMS.md#compound-action)** — units of work with gates
- **[Content type](../docs/TERMS.md#content-type)** — first-class artifact class (ADR, integrity doc, agent noun, audit, example)
- **Contribution / [add-X](../docs/TERMS.md#contribution-gate)** — gated [action](../docs/TERMS.md#action) of adding/amending type X
- **[Shared docs standard](../docs/TERMS.md#shared-docs-standard)** — this standard
- **[Type recipe](../docs/TERMS.md#type-recipe)** — prescribed steps + [gate](../docs/TERMS.md#gate) criteria for type X
- **[Contribution Gate](../docs/TERMS.md#contribution-gate)** — [refuse-wired](../docs/TERMS.md#default-closed) [gate](../docs/TERMS.md#gate) for contributions
- **[Audit receipt](../docs/TERMS.md#audit-receipt)** — [gate](../docs/TERMS.md#gate) evidence produced by an [audit](../docs/TERMS.md#audit); [audit](../docs/TERMS.md#audit) ≠ [gate](../docs/TERMS.md#gate)
- **[Gate](../docs/TERMS.md#gate)** — binary enforcement checkpoint; [gate](../docs/TERMS.md#gate) ≠ [audit](../docs/TERMS.md#audit)

When prose uses these terms, readers may rely on the lexicon definition without re-reading the full standard.

### 4. Evidence

Claims cite sources:

| Claim type | Evidence form |
|------------|---------------|
| [Requirement](../docs/TERMS.md#requirement) [met](../docs/TERMS.md#met) | [Audit](../docs/TERMS.md#audit) id and outcome (e.g., "A-P4 met") |
| Binder exists | Binder path or PR link |
| Fixture fails | Fixture id and expected outcome |
| Role responsibility | Role name from [agent noun](../docs/TERMS.md#agent-noun) or SOP |

Unsourced claims are incomplete work.

### 5. Role Language

SSOT surfaces use role names only. Person names do not appear.

| Surface | [Rule](../docs/TERMS.md#rule) |
|---------|------|
| [Charter](../docs/TERMS.md#charter) | Role names only |
| [Integrity](../docs/TERMS.md#integrity) docs | Role names only |
| [Agent nouns](../docs/TERMS.md#agent-noun) | Role names only |
| SOP tables | Role names only |
| [ADR](../docs/TERMS.md#adr) Deciders | Role names or pseudonymous handle (not real names in SSOT copy) |

**Rationale:** SSOT is durable; person assignments change. The SSOT carries the role; a separate assignment register (outside SSOT) maps roles to people.

### 6. Incomplete-Packet [Refuse](../docs/TERMS.md#refuse)

Every [gate](../docs/TERMS.md#gate) or [handoff](../docs/TERMS.md#handoff) tip documents:

1. **[Refuse](../docs/TERMS.md#refuse) criteria** — enumerated conditions that cause [REFUSE](../docs/TERMS.md#refuse)
2. **Incomplete-packet fixture** — a concrete example that exercises the [refuse](../docs/TERMS.md#refuse) path

A tip without both is incomplete. See [`GATE.md`](GATE.md) design [rule](../docs/TERMS.md#rule): [refuse](../docs/TERMS.md#refuse) + incomplete-packet fixture in the same tip.

### 7. Supersede Rules

Superseded content is marked, not deleted (charter R22).

| [Action](../docs/TERMS.md#action) | How |
|--------|-----|
| Supersede a document | Add `<!-- SUPERSEDED by <path> as of <date> -->` at top; retain file |
| Supersede a section | Add `**SUPERSEDED** by [<new-section>](<link>).` inline; retain text |
| Supersede an [ADR](../docs/TERMS.md#adr) | Status line: `Status: Superseded by ADR NNNN` |

Deletion removes [audit](../docs/TERMS.md#audit) trail. Mark-as-superseded preserves context.

---

## [Contribution Gate](../docs/TERMS.md#contribution-gate)

The [Contribution Gate](../docs/TERMS.md#contribution-gate) is the [refuse-wired](../docs/TERMS.md#default-closed) [gate](../docs/TERMS.md#gate) that governs all [add-X](../docs/TERMS.md#contribution-gate) contributions. It meets the all-required PASS fitness bar (G1–G4) from [`GATE.md`](GATE.md).

### [Refuse](../docs/TERMS.md#refuse) Criteria

A contribution is **REFUSED** if any of the following hold:

| # | [Refuse](../docs/TERMS.md#refuse) condition | Rationale |
|---|------------------|-----------|
| CG-R1 | [Shared docs standard](../docs/TERMS.md#shared-docs-standard) not [met](../docs/TERMS.md#met) | Structure, naming, lexicon, evidence, role language, incomplete-packet [refuse](../docs/TERMS.md#refuse), or supersede rules violated |
| CG-R2 | [Type recipe](../docs/TERMS.md#type-recipe) for [content type](../docs/TERMS.md#content-type) X not followed | Each [content type](../docs/TERMS.md#content-type) has prescribed steps; skipping a step = incomplete |
| CG-R3 | [Type recipe](../docs/TERMS.md#type-recipe) for [content type](../docs/TERMS.md#content-type) X does not exist | Cannot [add-X](../docs/TERMS.md#contribution-gate) without a recipe; publish recipe first |
| CG-R4 | Person names appear in SSOT surfaces | Role language only; no person names |
| CG-R5 | Required incomplete-packet fixture missing | Gate/handoff tips require a fixture |
| CG-R6 | [SSOT exit evidence](../docs/TERMS.md#ssot-exit-evidence) missing | `ssot_leaf_ids` + `ssot_exit_status` required (S8, P-020) |
| CG-R7 | [Gate](../docs/TERMS.md#gate) criteria incomplete (G1–G4 not addressed) | [Gate](../docs/TERMS.md#gate) documents must address all four criteria |

### [Gate](../docs/TERMS.md#gate) Outcomes

| Outcome | Meaning |
|---------|---------|
| **PASS** | All [refuse](../docs/TERMS.md#refuse) criteria clear; contribution advances |
| **[REFUSE](../docs/TERMS.md#refuse)** | One or more [refuse](../docs/TERMS.md#refuse) criteria triggered; contribution blocked |

There is no WARN, PROVISIONAL, or SOFT-PASS.

### All-Required PASS Bar (G1–G4)

The [Contribution Gate](../docs/TERMS.md#contribution-gate) satisfies [G1–G4](../docs/TERMS.md#g1g4):

| Criterion | Evidence |
|-----------|----------|
| **G1** Incomplete cannot PASS | CG-R1 through CG-R7 enumerate incomplete conditions → [REFUSE](../docs/TERMS.md#refuse) |
| **G2** Machine-checkable or [refuse-wired](../docs/TERMS.md#default-closed) | Structure checks can lint; recipe presence checked by index; person-name checks can grep; missing [SSOT exit evidence](../docs/TERMS.md#ssot-exit-evidence) checked by fitness |
| **G3** Incomplete-packet fixture fails | See fixture below |
| **G4** PASS needs no human redo | PASS means contribution is complete per [type recipe](../docs/TERMS.md#type-recipe); no follow-up fix required |

---

## Incomplete-Packet Fixture: [add-X](../docs/TERMS.md#contribution-gate) without [Type Recipe](../docs/TERMS.md#type-recipe)

Reference case for the [Contribution Gate](../docs/TERMS.md#contribution-gate).

### Scenario

A producer attempts to add [content type](../docs/TERMS.md#content-type) **"runbook"** to the repository. The contribution includes:
- File at `runbooks/deploy-prod.md`
- Follows general markdown style
- No [type recipe](../docs/TERMS.md#type-recipe) exists for "runbook" in `content-types/HOW-TO-ADD.md`

### Required Outcome

**[REFUSE](../docs/TERMS.md#refuse)** under CG-R3 (type recipe does not exist).

The [Contribution Gate](../docs/TERMS.md#contribution-gate) cannot evaluate whether the contribution is complete without a [type recipe](../docs/TERMS.md#type-recipe). The producer must first contribute the [type recipe](../docs/TERMS.md#type-recipe) for "runbook" (which itself passes the Contribution Gate for type-recipe as a content type), then contribute the runbook instance.

### Fixture Verification

| [Refuse](../docs/TERMS.md#refuse) criterion | Applies? | Outcome |
|------------------|----------|---------|
| CG-R1 | Maybe (no recipe to check against) | Defer to CG-R3 |
| CG-R2 | Cannot evaluate (no recipe) | Defer to CG-R3 |
| CG-R3 | **Yes** — no [type recipe](../docs/TERMS.md#type-recipe) for "runbook" | **[REFUSE](../docs/TERMS.md#refuse)** |
| CG-R4 | Maybe | Not primary blocker |
| CG-R5 | N/A (not a gate/handoff tip) | — |
| CG-R6 | Applies separately at fitness | — |
| CG-R7 | N/A (not a gate document) | — |

**Conclusion:** A contribution for [content type](../docs/TERMS.md#content-type) X without a [type recipe](../docs/TERMS.md#type-recipe) for X is incomplete. The [Contribution Gate](../docs/TERMS.md#contribution-gate) refuses it.

### Second Fixture: add-ADR with Person Names

**Scenario:** A producer contributes `adrs/0099-new-decision.md` with:
- Correct path pattern
- [ADR](../docs/TERMS.md#adr) [type recipe](../docs/TERMS.md#type-recipe) steps followed
- `Deciders: Jane Doe, Bob Smith` (real names in SSOT surface)

**Required outcome:** **[REFUSE](../docs/TERMS.md#refuse)** under CG-R4 (person names in SSOT).

**Fix:** Use role names (`Deciders: Quality Architect, Standards Steward`) or pseudonymous handles. Person-to-role mapping lives outside SSOT.

---

## [Contribution Gate](../docs/TERMS.md#contribution-gate) Incomplete-Packet Hunt

The adversarial half: can an incomplete contribution still slip through?

| Slip path | Blocked by |
|-----------|------------|
| Add-X with no recipe | CG-R3 |
| Add-X skipping recipe steps | CG-R2 |
| SSOT with person names | CG-R4 |
| [Gate](../docs/TERMS.md#gate) tip without [refuse](../docs/TERMS.md#refuse)+fixture | CG-R5, CG-R7 |
| Missing [SSOT exit evidence](../docs/TERMS.md#ssot-exit-evidence) | CG-R6 (enforced at fitness) |
| Violates structure/naming | CG-R1 |

No known incomplete-packet slip remains. If a slip is discovered, it becomes a blocker finding → [Contribution Gate](../docs/TERMS.md#contribution-gate) amended.

---

## Confirmation Checklist (Contribution-Specific)

For any contribution (add-X) to this repository:

- [ ] CC1. [Content type](../docs/TERMS.md#content-type) X has a [type recipe](../docs/TERMS.md#type-recipe) in `content-types/HOW-TO-ADD.md`.
- [ ] CC2. [Type recipe](../docs/TERMS.md#type-recipe) steps for X are followed.
- [ ] CC3. [Shared docs standard](../docs/TERMS.md#shared-docs-standard) [met](../docs/TERMS.md#met) (structure, naming, lexicon, evidence, role language, incomplete-packet refuse, supersede rules).
- [ ] CC4. No person names in SSOT surfaces.
- [ ] CC5. If artifact is a gate/handoff tip: [refuse](../docs/TERMS.md#refuse) criteria + incomplete-packet fixture documented.
- [ ] CC6. If artifact is a [gate](../docs/TERMS.md#gate) tip: [G1–G4](../docs/TERMS.md#g1g4) addressed.
- [ ] CC7. [SSOT exit evidence](../docs/TERMS.md#ssot-exit-evidence) present (`ssot_leaf_ids`, `ssot_exit_status`).
- [ ] CC8. Cross-references updated (DESCRIBE.md, AGENTS.md, integrity/README.md, relevant indexes).

---

## Cross-references

- [`LEXICON.md`](LEXICON.md) — locked definitions (Action, Content type, Type recipe, Contribution Gate, etc.)
- [`GATE.md`](GATE.md) — [gate](../docs/TERMS.md#gate) [noun](../docs/TERMS.md#noun), [G1–G4](../docs/TERMS.md#g1g4) fitness bar, incomplete-packet hunt
- [`BOUNDARY.md`](BOUNDARY.md) — [boundary](../docs/TERMS.md#boundary) and [handoff](../docs/TERMS.md#handoff) nouns
- [`PRINCIPLES.md`](PRINCIPLES.md) — practice [integrity](../docs/TERMS.md#integrity) principles (P1–P7)
- [`../content-types/HOW-TO-ADD.md`](../content-types/HOW-TO-ADD.md) — [type recipe](../docs/TERMS.md#type-recipe) index
- [`../CHARTER.md`](../CHARTER.md) §5.8 — practice [integrity](../docs/TERMS.md#integrity) rules
- [`../CHARTER.md`](../CHARTER.md) R22 — superseded content marked, not deleted
- [`../AGENTS.md`](../AGENTS.md) — standing instructions for agents
