# Lexicon

Locked definitions for Boundary-Based Programming. Terms in this lexicon have stable, versioned meanings. When a term appears in the charter, integrity, or agents surfaces, it carries the definition here.

Rationale: charter §5.8 practice integrity requires zero variance on prescribed actions and hard gates. That extends to language: the same word must carry the same meaning across every surface.

Related: [`CONTRIBUTION.md`](CONTRIBUTION.md) shared docs standard, [`GATE.md`](GATE.md) gate noun.

---

## A

### Action

A named unit of work with contracted I/O. Every Action has a completion Gate that yields binary outcome (complete / incomplete). Actions appear at multiple scales (atomic, compound) and in multiple contexts (producer work, agent verbs, contribution flows).

**Audit `A-LEXICON-ACTION`:** Met iff every artifact labeled "Action" declares input, output, and Gate. Not met if any Action omits Gate.

### Atomic action

An Action that cannot decompose further without losing a meaningful Gate. If you split an atomic action, one of the fragments would lack a binary gate, making it ungated work.

**Audit `A-LEXICON-ATOMIC`:** Met iff no atomic action definition permits decomposition into gated sub-parts. Not met if an atomic action can be meaningfully split and each part still gated.

### Audit

Role-based adversarial review that produces findings for a ship decision. Audits yield binary per-item outcomes (met / not met) but do not block automatically—they inform the ship-role or human who decides.

**Audit ≠ Gate.** Gates block the build; audits produce findings. See [`GATE.md`](GATE.md) §Definition.

### Audit receipt

Evidence artifact produced by an Audit. An audit receipt is **Gate evidence**—it satisfies a Gate's input requirement when the Gate needs proof that an audit occurred. The receipt documents the audit outcome (PASS / FAIL / REFUSE) and the findings.

**Audit receipt is Gate evidence; Audit is not a Gate.** The audit process produces findings. The receipt of that process is evidence. A downstream Gate may require the receipt as input; the audit itself remains a review, not a gate.

---

## C

### Compound action

An Action composed of other Actions, yet still possessing its own completion Gate. Every inner Action executes its own Gate; the compound action also executes its outer Gate. No gate is skipped.

**Audit `A-LEXICON-COMPOUND`:** Met iff every compound action definition (a) names its constituent actions, (b) each constituent has a Gate, and (c) the compound has its own outer Gate. Not met if any inner or outer gate is absent.

### Content type

A first-class artifact class in the repository. Content types include ADR, integrity doc, agent noun, audit definition, example. Each content type has a type recipe prescribing how to add or amend instances.

**Audit `A-LEXICON-CONTENT-TYPE`:** Met iff each content type named in `content-types/` has a type recipe. Not met if a content type is named without a recipe.

### Contribution / add-X

The Action of adding or amending an instance of content type X. A contribution is gated by the Contribution Gate, which refuses incomplete packets.

**Audit `A-LEXICON-CONTRIBUTION`:** Met iff every add-X instruction links to the type recipe and states the Contribution Gate. Not met if add-X bypasses the shared docs standard.

### Contribution Gate

The refuse-wired gate for contributions. The Contribution Gate refuses if:
- Shared docs standard is not met (structure, naming, lexicon, evidence, role language, incomplete-packet refuse, supersede rules)
- Type recipe for content type X is not followed
- Person names appear in SSOT surfaces
- Required fixture is missing

See [`CONTRIBUTION.md`](CONTRIBUTION.md) for full refuse criteria and incomplete-packet fixture.

**Audit `A-LEXICON-CONTRIB-GATE`:** Met iff the Contribution Gate definition states refuse criteria and an incomplete-packet fixture. Not met if gate definition is incomplete.

---

## G

### Gate

Binary enforcement checkpoint. A Gate is PASS / FAIL / REFUSE only—no partial, provisional, warn-only, or soft-pass. Gates are default-closed (work does not pass until the gate explicitly opens) and refuse-wired (if a check cannot run, the gate refuses).

See [`GATE.md`](GATE.md) for formal definition and all-required PASS fitness bar (G1–G4).

**Gate ≠ Audit.** Gates block automatically; audits produce findings for a decision-maker. Both are binary per item, but differ in mechanism and authority.

---

## S

### Shared docs standard

The structure, naming, lexicon, evidence, role language, incomplete-packet refuse, and supersede rules that govern all SSOT documents in this repository. The shared docs standard ensures:

1. **Structure** — consistent layout (purpose, definition, refuse criteria, fixture, checklist, cross-references)
2. **Naming** — predictable file paths and slugs
3. **Lexicon** — terms from this LEXICON.md carry stable meanings
4. **Evidence** — claims cite audits, binders, or fixture references
5. **Role language** — role names only (Quality Architect, Adversarial Auditor, etc.); no person names in SSOT surfaces
6. **Incomplete-packet refuse** — every gate/handoff tip documents refuse criteria and an incomplete-packet fixture
7. **Supersede rules** — superseded content is marked, not deleted (charter R22)

See [`CONTRIBUTION.md`](CONTRIBUTION.md) for full specification.

**Audit `A-LEXICON-SHARED-DOCS`:** Met iff shared docs standard is documented and contribution gates enforce it. Not met if standard is undefined or unenforced.

---

## T

### Type recipe

Prescribed steps and Gate criteria for adding or amending content type X. Every type recipe specifies:
1. **Inputs** — what the producer must provide
2. **Steps** — ordered atomic/compound actions
3. **Gate criteria** — what the Contribution Gate checks
4. **Incomplete-packet fixture** — example that must FAIL

See [`content-types/HOW-TO-ADD.md`](../content-types/HOW-TO-ADD.md) for the index of type recipes.

**Audit `A-LEXICON-TYPE-RECIPE`:** Met iff every type recipe documents inputs, steps, gate criteria, and incomplete-packet fixture. Not met if any element is missing.

---

## Cross-references

- [`CONTRIBUTION.md`](CONTRIBUTION.md) — shared docs standard, Contribution Gate
- [`GATE.md`](GATE.md) — gate noun, G1–G4 fitness bar
- [`BOUNDARY.md`](BOUNDARY.md) — boundary and handoff nouns
- [`PRINCIPLES.md`](PRINCIPLES.md) — practice integrity principles
- [`../content-types/HOW-TO-ADD.md`](../content-types/HOW-TO-ADD.md) — type recipe index
- [`../CHARTER.md`](../CHARTER.md) §5.8 — practice integrity rules
