# How to Add X

Index of type recipes for content types in this repository. Each [content type](../docs/TERMS.md#content-type) has prescribed steps and [Gate](../docs/TERMS.md#gate) criteria. Adding or amending an instance of type X requires following the [type recipe](../docs/TERMS.md#type-recipe) for X.

Rationale: [`integrity/CONTRIBUTION.md`](../integrity/CONTRIBUTION.md) [Contribution Gate](../docs/TERMS.md#contribution-gate) (CG-R2, CG-R3); [`integrity/LEXICON.md`](../integrity/LEXICON.md) [Type recipe](../docs/TERMS.md#type-recipe) definition.

---

## [Type Recipe](../docs/TERMS.md#type-recipe) Index

| [Content type](../docs/TERMS.md#content-type) | Recipe status | Path pattern | Summary |
|--------------|---------------|--------------|---------|
| [ADR](#adr) | Complete | `adrs/NNNN-short-slug.md` | Architecture Decision Record |
| [Integrity doc](#integrity-doc) | Complete | `integrity/NAME.md` | [Noun](../docs/TERMS.md#noun) or principle definition |
| [Agent noun](#agent-noun) | Stub | `agents/<name>/AGENT.md` | Durable agent role |
| [Audit](#audit) | Stub | `integrity/audits/A-<id>.md` | Per-requirement [audit](../docs/TERMS.md#audit) definition |
| [Example](#example) | Stub | `examples/<name>/README.md` | [Adopter](../docs/TERMS.md#adopter) sample |

---

## [ADR](../docs/TERMS.md#adr)

Architecture Decision Records capture ratified decisions for this practice or [adopter](../docs/TERMS.md#adopter) systems.

### Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Decision statement | Yes | The choice being made |
| Context | Yes | Why the decision is needed |
| Consequences | Yes | What changes as a result |
| Status | Yes | Proposed / Accepted / Superseded |
| Deciders | Yes | Role names (not person names) |
| Date | Yes | Decision date (YYYY-MM-DD) |

### Steps

1. **Reserve sequence number** — check `adrs/` for next available `NNNN`.
2. **Create file** — `adrs/NNNN-short-slug.md` (lowercase hyphenated slug).
3. **Write [ADR](../docs/TERMS.md#adr)** using template:
   ```markdown
   # ADR NNNN — <Title>

   - Status: Proposed | Accepted | Superseded by ADR NNNN
   - Date: YYYY-MM-DD
   - Deciders: <role names>

   ## Context

   <Why this decision is needed.>

   ## Decision

   <The choice and its details.>

   ## Consequences

   <What changes; tradeoffs.>

   ## Rejected

   <Alternatives considered and why rejected.>
   ```
4. **Update `adrs/README.md`** — add row to [ADR](../docs/TERMS.md#adr) index table.
5. **Cross-link** — update related documents that reference this decision.
6. **Review [gate](../docs/TERMS.md#gate)** — submit for [Contribution Gate](../docs/TERMS.md#contribution-gate) (PR / fitness / audit).

### [Gate](../docs/TERMS.md#gate) Criteria

| Criterion | Check |
|-----------|-------|
| Sequence unique | No duplicate `NNNN` in `adrs/` |
| Slug matches file | Filename matches `NNNN-short-slug.md` pattern |
| Required fields present | Status, Date, Deciders, Context, Decision, Consequences |
| No person names | Deciders are role names only |
| Index updated | `adrs/README.md` includes new [ADR](../docs/TERMS.md#adr) |
| Cross-links updated | Related docs reference [ADR](../docs/TERMS.md#adr) where relevant |

### Incomplete-Packet Fixture

**Scenario:** [ADR](../docs/TERMS.md#adr) submitted without Consequences section.

**Required outcome:** **[REFUSE](../docs/TERMS.md#refuse)** — incomplete (missing required field).

---

## [Integrity](../docs/TERMS.md#integrity) Doc

[Integrity](../docs/TERMS.md#integrity) documents define nouns (Gate, Boundary, Lexicon) and principles (P1–P7) for practice [integrity](../docs/TERMS.md#integrity).

### Inputs

| Input | Required | Description |
|-------|----------|-------------|
| [Noun](../docs/TERMS.md#noun) or principle name | Yes | What the document defines |
| Definition | Yes | Core semantics |
| Rationale | Yes | [Charter](../docs/TERMS.md#charter) or [ADR](../docs/TERMS.md#adr) reference |
| Related links | Yes | Cross-references |
| [Refuse](../docs/TERMS.md#refuse) criteria | Conditional | Required if document defines a [gate](../docs/TERMS.md#gate) or [handoff](../docs/TERMS.md#handoff) |
| Incomplete-packet fixture | Conditional | Required if document defines a [gate](../docs/TERMS.md#gate) or [handoff](../docs/TERMS.md#handoff) |
| Confirmation checklist | Conditional | Required if document requires per-change gating |

### Steps

1. **Determine scope** — is this a new [noun](../docs/TERMS.md#noun), principle, or amendment?
2. **Create or amend file** — `integrity/NAME.md` (UPPERCASE for primary nouns).
3. **Write document** using template:
   ```markdown
   # <Name>

   SSOT for the <Name> noun/principle in Boundary-Based Programming.

   Rationale: <charter section, ADR reference>.

   ---

   ## Definition

   <Core semantics.>

   ---

   ## <Sections as needed>

   ---

   ## Confirmation Checklist (<Name>-specific)

   - [ ] ...

   ---

   ## Cross-references

   - ...
   ```
4. **If gate/handoff tip:** add [refuse](../docs/TERMS.md#refuse) criteria + incomplete-packet fixture.
5. **If [gate](../docs/TERMS.md#gate) tip:** address [G1–G4](../docs/TERMS.md#g1g4) explicitly.
6. **Update `integrity/README.md`** — add row to index table if new file.
7. **Update `LEXICON.md`** — if new terms introduced, add definitions.
8. **Cross-link** — update DESCRIBE.md, AGENTS.md, related docs.
9. **Review [gate](../docs/TERMS.md#gate)** — submit for [Contribution Gate](../docs/TERMS.md#contribution-gate) (PR / fitness / audit).

### [Gate](../docs/TERMS.md#gate) Criteria

| Criterion | Check |
|-----------|-------|
| Path correct | File at `integrity/NAME.md` |
| SSOT declaration | Opens with "SSOT for..." |
| Rationale present | Links to [charter](../docs/TERMS.md#charter) or [ADR](../docs/TERMS.md#adr) |
| Definition present | Core semantics stated (for noun docs) |
| [Refuse](../docs/TERMS.md#refuse) + fixture | Present if gate/handoff tip |
| [G1–G4](../docs/TERMS.md#g1g4) addressed | Present if [gate](../docs/TERMS.md#gate) tip |
| No person names | Role names only |
| Indexes updated | `integrity/README.md`, LEXICON as needed |
| Cross-links updated | DESCRIBE.md, AGENTS.md as relevant |

### Incomplete-Packet Fixture

**Scenario:** [Gate](../docs/TERMS.md#gate) document submitted without incomplete-packet fixture.

**Required outcome:** **[REFUSE](../docs/TERMS.md#refuse)** — [gate](../docs/TERMS.md#gate) tip requires fixture (CG-R5, CG-R7).

---

## [Agent Noun](../docs/TERMS.md#agent-noun)

Durable agent role with identity, adjectives, and contracted verbs.

### Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Role name | Yes | [Agent noun](../docs/TERMS.md#agent-noun) identity (lowercase) |
| Purpose | Yes | What the role does |
| Adjectives | Yes | What the role must never violate |
| Verbs | Yes | Public operations with I/O contracts |
| [Ship](../docs/TERMS.md#ship) authority | Yes | Whether role can authorize release |

### Steps

1. **Create folder** — `agents/<name>/`.
2. **Create `AGENT.md`** — entry point with role definition. Required heading: `## Adjectives`.
3. **Create `verbs.md`** — verb catalog with I/O contracts.
4. **Update `agents/README.md`** — add row to [agent noun](../docs/TERMS.md#agent-noun) index.
5. **Cross-link** — update DESCRIBE.md, role glossary in [BOUNDARY](../docs/TERMS.md#boundary).md SOP.
6. **Review [gate](../docs/TERMS.md#gate)** — submit for [Contribution Gate](../docs/TERMS.md#contribution-gate).

### [Gate](../docs/TERMS.md#gate) Criteria

| Criterion | Check |
|-----------|-------|
| Path correct | `agents/<name>/AGENT.md` exists |
| Adjectives heading | `AGENT.md` has `## Adjectives` |
| Verbs documented | `agents/<name>/verbs.md` exists with I/O contracts |
| No person names | Role language only |
| Indexes updated | `agents/README.md` includes role |

### Incomplete-Packet Fixture

**Scenario:** [Agent noun](../docs/TERMS.md#agent-noun) folder created without `verbs.md`.

**Required outcome:** **[REFUSE](../docs/TERMS.md#refuse)** — incomplete (missing verb contracts).

**Status:** STUB — expand when tooling validates [agent noun](../docs/TERMS.md#agent-noun) structure.

---

## [Audit](../docs/TERMS.md#audit)

Per-requirement [audit](../docs/TERMS.md#audit) definition with binary met/not-met criteria.

### Inputs

| Input | Required | Description |
|-------|----------|-------------|
| [Audit](../docs/TERMS.md#audit) id | Yes | `A-<id>` format |
| [Requirement](../docs/TERMS.md#requirement) id | Yes | What [requirement](../docs/TERMS.md#requirement) this [audit](../docs/TERMS.md#audit) covers |
| [Met](../docs/TERMS.md#met) criteria | Yes | Binary condition for [met](../docs/TERMS.md#met) |
| Not-met criteria | Yes | Binary condition for not [met](../docs/TERMS.md#met) |
| Evidence form | Yes | What evidence the [audit](../docs/TERMS.md#audit) produces |

### Steps

1. **Reserve [audit](../docs/TERMS.md#audit) id** — check `integrity/audits/` for existing ids.
2. **Create file** — `integrity/audits/A-<id>.md`.
3. **Write [audit](../docs/TERMS.md#audit) definition** with met/not-met criteria.
4. **Update `binding-matrix.json`** — link [requirement](../docs/TERMS.md#requirement) to [audit](../docs/TERMS.md#audit).
5. **Update `integrity/audits/README.md`** — add to index.
6. **Review [gate](../docs/TERMS.md#gate)** — submit for [Contribution Gate](../docs/TERMS.md#contribution-gate).

### [Gate](../docs/TERMS.md#gate) Criteria

| Criterion | Check |
|-----------|-------|
| Path correct | `integrity/audits/A-<id>.md` |
| Binary criteria | [Met](../docs/TERMS.md#met) and not-met are mutually exclusive and exhaustive |
| Evidence form stated | How the [audit](../docs/TERMS.md#audit) proves its outcome |
| Matrix updated | `binding-matrix.json` links to this [audit](../docs/TERMS.md#audit) |

### Incomplete-Packet Fixture

**Scenario:** [Audit](../docs/TERMS.md#audit) definition submitted without not-met criteria.

**Required outcome:** **[REFUSE](../docs/TERMS.md#refuse)** — incomplete (not binary).

**Status:** STUB — expand with [audit](../docs/TERMS.md#audit) definition template.

---

## Example

[Adopter](../docs/TERMS.md#adopter) sample demonstrating [BBP](../docs/TERMS.md#bbp) application.

### Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Example name | Yes | Descriptive lowercase folder name |
| Purpose | Yes | What the example demonstrates |
| Nouns + verbs | Yes | At least one [noun](../docs/TERMS.md#noun) with a verb |
| Violation case | Recommended | Deliberate violation that fails fitness |

### Steps

1. **Create folder** — `examples/<name>/`.
2. **Create `README.md`** — entry point explaining the example.
3. **Implement example** — code or config demonstrating [BBP](../docs/TERMS.md#bbp).
4. **Add violation case** (recommended) — `*-violation/` subfolder with failing case.
5. **Update `examples/README.md`** — add row to example index.
6. **Review [gate](../docs/TERMS.md#gate)** — submit for [Contribution Gate](../docs/TERMS.md#contribution-gate).

### [Gate](../docs/TERMS.md#gate) Criteria

| Criterion | Check |
|-----------|-------|
| Path correct | `examples/<name>/README.md` exists |
| Purpose stated | README explains what the example shows |
| At least one [noun](../docs/TERMS.md#noun) | Example includes a [noun](../docs/TERMS.md#noun) definition |
| Index updated | `examples/README.md` includes example |

### Incomplete-Packet Fixture

**Scenario:** Example folder created without README.md.

**Required outcome:** **[REFUSE](../docs/TERMS.md#refuse)** — incomplete (no entry point).

**Status:** STUB — expand with example template.

---

## Adding a New [Content Type](../docs/TERMS.md#content-type)

When a new [content type](../docs/TERMS.md#content-type) is needed:

1. **Propose via [ADR](../docs/TERMS.md#adr)** — rationale for the new [content type](../docs/TERMS.md#content-type).
2. **Define [type recipe](../docs/TERMS.md#type-recipe)** — add section to this document.
3. **Include inputs, steps, [gate](../docs/TERMS.md#gate) criteria, and incomplete-packet fixture**.
4. **Update index table** at top of this document.
5. **[Contribution Gate](../docs/TERMS.md#contribution-gate) applies** — the [type recipe](../docs/TERMS.md#type-recipe) addition is itself a contribution.

Type recipes are themselves governed by the [Contribution Gate](../docs/TERMS.md#contribution-gate). A [type recipe](../docs/TERMS.md#type-recipe) without an incomplete-packet fixture is incomplete (CG-R5 applies to this document too).

---

## Cross-references

- [`../integrity/CONTRIBUTION.md`](../integrity/CONTRIBUTION.md) — [shared docs standard](../docs/TERMS.md#shared-docs-standard), [Contribution Gate](../docs/TERMS.md#contribution-gate)
- [`../integrity/LEXICON.md`](../integrity/LEXICON.md) — locked definitions (Type recipe, Content type)
- [`../integrity/GATE.md`](../integrity/GATE.md) — [G1–G4](../docs/TERMS.md#g1g4) fitness bar
- [`../adrs/README.md`](../adrs/README.md) — [ADR](../docs/TERMS.md#adr) index
- [`../integrity/README.md`](../integrity/README.md) — [integrity](../docs/TERMS.md#integrity) index
- [`../agents/README.md`](../agents/README.md) — [agent noun](../docs/TERMS.md#agent-noun) index
- [`../examples/README.md`](../examples/README.md) — example index
