# Lexicon

Locked definitions for [Boundary-Based Programming](../docs/TERMS.md#bbp). Terms in this lexicon have stable, versioned meanings. When a term appears in the [charter](../docs/TERMS.md#charter), [integrity](../docs/TERMS.md#integrity), or agents surfaces, it carries the definition here.

Rationale: [charter](../docs/TERMS.md#charter) §5.8 practice [integrity](../docs/TERMS.md#integrity) requires [zero variance](../docs/TERMS.md#zero-variance) on prescribed actions and hard gates. That extends to language: the same word must carry the same meaning across every surface.

Related: [`CONTRIBUTION.md`](CONTRIBUTION.md) [shared docs standard](../docs/TERMS.md#shared-docs-standard), [`GATE.md`](GATE.md) [gate](../docs/TERMS.md#gate) [noun](../docs/TERMS.md#noun).

---

## A

### [Action](../docs/TERMS.md#action)

A named unit of work with contracted I/O. Every [Action](../docs/TERMS.md#action) has a completion [Gate](../docs/TERMS.md#gate) that yields binary outcome (complete / incomplete). Actions appear at multiple scales (atomic, compound) and in multiple contexts (producer work, agent verbs, contribution flows).

**[Audit](../docs/TERMS.md#audit) `A-LEXICON-ACTION`:** [Met](../docs/TERMS.md#met) iff every artifact labeled "[Action](../docs/TERMS.md#action)" declares input, output, and [Gate](../docs/TERMS.md#gate). Not [met](../docs/TERMS.md#met) if any [Action](../docs/TERMS.md#action) omits [Gate](../docs/TERMS.md#gate).

### [Atomic action](../docs/TERMS.md#atomic-action)

An [Action](../docs/TERMS.md#action) that cannot decompose further without losing a meaningful [Gate](../docs/TERMS.md#gate). If you split an [atomic action](../docs/TERMS.md#atomic-action), one of the fragments would lack a binary [gate](../docs/TERMS.md#gate), making it ungated work.

**[Audit](../docs/TERMS.md#audit) `A-LEXICON-ATOMIC`:** [Met](../docs/TERMS.md#met) iff no [atomic action](../docs/TERMS.md#atomic-action) definition permits decomposition into gated sub-parts. Not [met](../docs/TERMS.md#met) if an [atomic action](../docs/TERMS.md#atomic-action) can be meaningfully split and each part still gated.

### [Audit](../docs/TERMS.md#audit)

Role-based adversarial review that produces findings for a [ship](../docs/TERMS.md#ship) decision. Audits yield binary per-item outcomes (met / not met) but do not block automatically—they inform the ship-role or human who decides.

**[Audit](../docs/TERMS.md#audit) ≠ [Gate](../docs/TERMS.md#gate).** Gates block the build; audits produce findings. See [`GATE.md`](GATE.md) §Definition.

### [Audit receipt](../docs/TERMS.md#audit-receipt)

Evidence artifact produced by an [Audit](../docs/TERMS.md#audit). An [audit receipt](../docs/TERMS.md#audit-receipt) is **[Gate](../docs/TERMS.md#gate) evidence**—it satisfies a [Gate](../docs/TERMS.md#gate)'s input [requirement](../docs/TERMS.md#requirement) when the [Gate](../docs/TERMS.md#gate) needs proof that an [audit](../docs/TERMS.md#audit) occurred. The receipt documents the [audit](../docs/TERMS.md#audit) outcome (PASS / FAIL / REFUSE) and the findings.

**[Audit receipt](../docs/TERMS.md#audit-receipt) is [Gate](../docs/TERMS.md#gate) evidence; [Audit](../docs/TERMS.md#audit) is not a [Gate](../docs/TERMS.md#gate).** The [audit](../docs/TERMS.md#audit) process produces findings. The receipt of that process is evidence. A downstream [Gate](../docs/TERMS.md#gate) may require the receipt as input; the [audit](../docs/TERMS.md#audit) itself remains a review, not a [gate](../docs/TERMS.md#gate).

---

## C

### [Compound action](../docs/TERMS.md#compound-action)

An [Action](../docs/TERMS.md#action) composed of other Actions, yet still possessing its own completion [Gate](../docs/TERMS.md#gate). Every inner [Action](../docs/TERMS.md#action) executes its own [Gate](../docs/TERMS.md#gate); the [compound action](../docs/TERMS.md#compound-action) also executes its outer [Gate](../docs/TERMS.md#gate). No [gate](../docs/TERMS.md#gate) is skipped.

**[Audit](../docs/TERMS.md#audit) `A-LEXICON-COMPOUND`:** [Met](../docs/TERMS.md#met) iff every [compound action](../docs/TERMS.md#compound-action) definition (a) names its constituent actions, (b) each constituent has a [Gate](../docs/TERMS.md#gate), and (c) the compound has its own outer [Gate](../docs/TERMS.md#gate). Not [met](../docs/TERMS.md#met) if any inner or outer [gate](../docs/TERMS.md#gate) is absent.

### [Content type](../docs/TERMS.md#content-type)

A first-class artifact class in the repository. Content types include [ADR](../docs/TERMS.md#adr), [integrity](../docs/TERMS.md#integrity) doc, [agent noun](../docs/TERMS.md#agent-noun), [audit](../docs/TERMS.md#audit) definition, example. Each [content type](../docs/TERMS.md#content-type) has a [type recipe](../docs/TERMS.md#type-recipe) prescribing how to add or amend instances.

**[Audit](../docs/TERMS.md#audit) `A-LEXICON-CONTENT-TYPE`:** [Met](../docs/TERMS.md#met) iff each [content type](../docs/TERMS.md#content-type) named in `content-types/` has a [type recipe](../docs/TERMS.md#type-recipe). Not [met](../docs/TERMS.md#met) if a [content type](../docs/TERMS.md#content-type) is named without a recipe.

### Contribution / [add-X](../docs/TERMS.md#contribution-gate)

The [Action](../docs/TERMS.md#action) of adding or amending an instance of [content type](../docs/TERMS.md#content-type) X. A contribution is gated by the [Contribution Gate](../docs/TERMS.md#contribution-gate), which refuses incomplete packets.

**[Audit](../docs/TERMS.md#audit) `A-LEXICON-CONTRIBUTION`:** [Met](../docs/TERMS.md#met) iff every [add-X](../docs/TERMS.md#contribution-gate) instruction links to the [type recipe](../docs/TERMS.md#type-recipe) and states the [Contribution Gate](../docs/TERMS.md#contribution-gate). Not [met](../docs/TERMS.md#met) if [add-X](../docs/TERMS.md#contribution-gate) bypasses the [shared docs standard](../docs/TERMS.md#shared-docs-standard).

### [Contribution Gate](../docs/TERMS.md#contribution-gate)

The [refuse-wired](../docs/TERMS.md#default-closed) [gate](../docs/TERMS.md#gate) for contributions. The [Contribution Gate](../docs/TERMS.md#contribution-gate) refuses if:
- [Shared docs standard](../docs/TERMS.md#shared-docs-standard) is not [met](../docs/TERMS.md#met) (structure, naming, lexicon, evidence, role language, incomplete-packet refuse, supersede rules)
- [Type recipe](../docs/TERMS.md#type-recipe) for [content type](../docs/TERMS.md#content-type) X is not followed
- Person names appear in SSOT surfaces
- Required fixture is missing

See [`CONTRIBUTION.md`](CONTRIBUTION.md) for full [refuse](../docs/TERMS.md#refuse) criteria and incomplete-packet fixture.

**[Audit](../docs/TERMS.md#audit) `A-LEXICON-CONTRIB-GATE`:** [Met](../docs/TERMS.md#met) iff the [Contribution Gate](../docs/TERMS.md#contribution-gate) definition states [refuse](../docs/TERMS.md#refuse) criteria and an incomplete-packet fixture. Not [met](../docs/TERMS.md#met) if [gate](../docs/TERMS.md#gate) definition is incomplete.

---

## G

### [Gate](../docs/TERMS.md#gate)

Binary enforcement checkpoint. A [Gate](../docs/TERMS.md#gate) is PASS / FAIL / [REFUSE](../docs/TERMS.md#refuse) only—no partial, provisional, warn-only, or soft-pass. Gates are [default-closed](../docs/TERMS.md#default-closed) (work does not pass until the gate explicitly opens) and [refuse-wired](../docs/TERMS.md#default-closed) (if a check cannot run, the gate refuses).

See [`GATE.md`](GATE.md) for formal definition and all-required PASS fitness bar (G1–G4).

**[Gate](../docs/TERMS.md#gate) ≠ [Audit](../docs/TERMS.md#audit).** Gates block automatically; audits produce findings for a decision-maker. Both are binary per item, but differ in mechanism and authority.

---

## S

### [Shared docs standard](../docs/TERMS.md#shared-docs-standard)

The structure, naming, lexicon, evidence, role language, incomplete-packet [refuse](../docs/TERMS.md#refuse), and supersede rules that govern all SSOT documents in this repository. The [shared docs standard](../docs/TERMS.md#shared-docs-standard) ensures:

1. **Structure** — consistent layout (purpose, definition, refuse criteria, fixture, checklist, cross-references)
2. **Naming** — predictable file paths and slugs
3. **Lexicon** — terms from this LEXICON.md carry stable meanings
4. **Evidence** — claims cite audits, binders, or fixture references
5. **Role language** — role names only (Quality Architect, Adversarial Auditor, etc.); no person names in SSOT surfaces
6. **Incomplete-packet [refuse](../docs/TERMS.md#refuse)** — every gate/handoff tip documents [refuse](../docs/TERMS.md#refuse) criteria and an incomplete-packet fixture
7. **Supersede rules** — superseded content is marked, not deleted (charter R22)

See [`CONTRIBUTION.md`](CONTRIBUTION.md) for full specification.

**[Audit](../docs/TERMS.md#audit) `A-LEXICON-SHARED-DOCS`:** [Met](../docs/TERMS.md#met) iff [shared docs standard](../docs/TERMS.md#shared-docs-standard) is documented and contribution gates enforce it. Not [met](../docs/TERMS.md#met) if standard is undefined or unenforced.

---

## T

### [Type recipe](../docs/TERMS.md#type-recipe)

Prescribed steps and [Gate](../docs/TERMS.md#gate) criteria for adding or amending [content type](../docs/TERMS.md#content-type) X. Every [type recipe](../docs/TERMS.md#type-recipe) specifies:
1. **Inputs** — what the producer must provide
2. **Steps** — ordered atomic/compound actions
3. **[Gate](../docs/TERMS.md#gate) criteria** — what the [Contribution Gate](../docs/TERMS.md#contribution-gate) checks
4. **Incomplete-packet fixture** — example that must FAIL

See [`content-types/HOW-TO-ADD.md`](../content-types/HOW-TO-ADD.md) for the index of type recipes.

**[Audit](../docs/TERMS.md#audit) `A-LEXICON-TYPE-RECIPE`:** [Met](../docs/TERMS.md#met) iff every [type recipe](../docs/TERMS.md#type-recipe) documents inputs, steps, [gate](../docs/TERMS.md#gate) criteria, and incomplete-packet fixture. Not [met](../docs/TERMS.md#met) if any element is missing.

---

## Cross-references

- [`CONTRIBUTION.md`](CONTRIBUTION.md) — [shared docs standard](../docs/TERMS.md#shared-docs-standard), [Contribution Gate](../docs/TERMS.md#contribution-gate)
- [`GATE.md`](GATE.md) — [gate](../docs/TERMS.md#gate) [noun](../docs/TERMS.md#noun), [G1–G4](../docs/TERMS.md#g1g4) fitness bar
- [`BOUNDARY.md`](BOUNDARY.md) — [boundary](../docs/TERMS.md#boundary) and [handoff](../docs/TERMS.md#handoff) nouns
- [`PRINCIPLES.md`](PRINCIPLES.md) — practice [integrity](../docs/TERMS.md#integrity) principles
- [`../content-types/HOW-TO-ADD.md`](../content-types/HOW-TO-ADD.md) — [type recipe](../docs/TERMS.md#type-recipe) index
- [`../CHARTER.md`](../CHARTER.md) §5.8 — practice [integrity](../docs/TERMS.md#integrity) rules
