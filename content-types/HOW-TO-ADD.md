# How to Add X

Index of type recipes for content types in this repository. Each content type has prescribed steps and Gate criteria. Adding or amending an instance of type X requires following the type recipe for X.

Rationale: [`integrity/CONTRIBUTION.md`](../integrity/CONTRIBUTION.md) Contribution Gate (CG-R2, CG-R3); [`integrity/LEXICON.md`](../integrity/LEXICON.md) Type recipe definition.

---

## Type Recipe Index

| Content type | Recipe status | Path pattern | Summary |
|--------------|---------------|--------------|---------|
| [ADR](#adr) | Complete | `adrs/NNNN-short-slug.md` | Architecture Decision Record |
| [Integrity doc](#integrity-doc) | Complete | `integrity/NAME.md` | Noun or principle definition |
| [Agent noun](#agent-noun) | Stub | `agents/<name>/AGENT.md` | Durable agent role |
| [Audit](#audit) | Stub | `integrity/audits/A-<id>.md` | Per-requirement audit definition |
| [Example](#example) | Stub | `examples/<name>/README.md` | Adopter sample |

---

## ADR

Architecture Decision Records capture ratified decisions for this practice or adopter systems.

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
3. **Write ADR** using template:
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
4. **Update `adrs/README.md`** — add row to ADR index table.
5. **Cross-link** — update related documents that reference this decision.
6. **Review gate** — submit for Contribution Gate (PR / fitness / audit).

### Gate Criteria

| Criterion | Check |
|-----------|-------|
| Sequence unique | No duplicate `NNNN` in `adrs/` |
| Slug matches file | Filename matches `NNNN-short-slug.md` pattern |
| Required fields present | Status, Date, Deciders, Context, Decision, Consequences |
| No person names | Deciders are role names only |
| Index updated | `adrs/README.md` includes new ADR |
| Cross-links updated | Related docs reference ADR where relevant |

### Incomplete-Packet Fixture

**Scenario:** ADR submitted without Consequences section.

**Required outcome:** **REFUSE** — incomplete (missing required field).

---

## Integrity Doc

Integrity documents define nouns (Gate, Boundary, Lexicon) and principles (P1–P7) for practice integrity.

### Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Noun or principle name | Yes | What the document defines |
| Definition | Yes | Core semantics |
| Rationale | Yes | Charter or ADR reference |
| Related links | Yes | Cross-references |
| Refuse criteria | Conditional | Required if document defines a gate or handoff |
| Incomplete-packet fixture | Conditional | Required if document defines a gate or handoff |
| Confirmation checklist | Conditional | Required if document requires per-change gating |

### Steps

1. **Determine scope** — is this a new noun, principle, or amendment?
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
4. **If gate/handoff tip:** add refuse criteria + incomplete-packet fixture.
5. **If gate tip:** address G1–G4 explicitly.
6. **Update `integrity/README.md`** — add row to index table if new file.
7. **Update `LEXICON.md`** — if new terms introduced, add definitions.
8. **Cross-link** — update DESCRIBE.md, AGENTS.md, related docs.
9. **Review gate** — submit for Contribution Gate (PR / fitness / audit).

### Gate Criteria

| Criterion | Check |
|-----------|-------|
| Path correct | File at `integrity/NAME.md` |
| SSOT declaration | Opens with "SSOT for..." |
| Rationale present | Links to charter or ADR |
| Definition present | Core semantics stated (for noun docs) |
| Refuse + fixture | Present if gate/handoff tip |
| G1–G4 addressed | Present if gate tip |
| No person names | Role names only |
| Indexes updated | `integrity/README.md`, LEXICON as needed |
| Cross-links updated | DESCRIBE.md, AGENTS.md as relevant |

### Incomplete-Packet Fixture

**Scenario:** Gate document submitted without incomplete-packet fixture.

**Required outcome:** **REFUSE** — gate tip requires fixture (CG-R5, CG-R7).

---

## Agent Noun

Durable agent role with identity, invariants, and contracted verbs.

### Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Role name | Yes | Agent noun identity (lowercase) |
| Purpose | Yes | What the role does |
| Invariants | Yes | What the role must always maintain |
| Verbs | Yes | Public operations with I/O contracts |
| Ship authority | Yes | Whether role can authorize release |

### Steps

1. **Create folder** — `agents/<name>/`.
2. **Create `AGENT.md`** — entry point with role definition.
3. **Create `verbs.md`** — verb catalog with I/O contracts.
4. **Update `agents/README.md`** — add row to agent noun index.
5. **Cross-link** — update DESCRIBE.md, role glossary in BOUNDARY.md SOP.
6. **Review gate** — submit for Contribution Gate.

### Gate Criteria

| Criterion | Check |
|-----------|-------|
| Path correct | `agents/<name>/AGENT.md` exists |
| Verbs documented | `agents/<name>/verbs.md` exists with I/O contracts |
| No person names | Role language only |
| Indexes updated | `agents/README.md` includes role |

### Incomplete-Packet Fixture

**Scenario:** Agent noun folder created without `verbs.md`.

**Required outcome:** **REFUSE** — incomplete (missing verb contracts).

**Status:** STUB — expand when tooling validates agent noun structure.

---

## Audit

Per-requirement audit definition with binary met/not-met criteria.

### Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Audit id | Yes | `A-<id>` format |
| Requirement id | Yes | What requirement this audit covers |
| Met criteria | Yes | Binary condition for met |
| Not-met criteria | Yes | Binary condition for not met |
| Evidence form | Yes | What evidence the audit produces |

### Steps

1. **Reserve audit id** — check `integrity/audits/` for existing ids.
2. **Create file** — `integrity/audits/A-<id>.md`.
3. **Write audit definition** with met/not-met criteria.
4. **Update `binding-matrix.json`** — link requirement to audit.
5. **Update `integrity/audits/README.md`** — add to index.
6. **Review gate** — submit for Contribution Gate.

### Gate Criteria

| Criterion | Check |
|-----------|-------|
| Path correct | `integrity/audits/A-<id>.md` |
| Binary criteria | Met and not-met are mutually exclusive and exhaustive |
| Evidence form stated | How the audit proves its outcome |
| Matrix updated | `binding-matrix.json` links to this audit |

### Incomplete-Packet Fixture

**Scenario:** Audit definition submitted without not-met criteria.

**Required outcome:** **REFUSE** — incomplete (not binary).

**Status:** STUB — expand with audit definition template.

---

## Example

Adopter sample demonstrating BBP application.

### Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Example name | Yes | Descriptive lowercase folder name |
| Purpose | Yes | What the example demonstrates |
| Nouns + verbs | Yes | At least one noun with a verb |
| Violation case | Recommended | Deliberate violation that fails fitness |

### Steps

1. **Create folder** — `examples/<name>/`.
2. **Create `README.md`** — entry point explaining the example.
3. **Implement example** — code or config demonstrating BBP.
4. **Add violation case** (recommended) — `*-violation/` subfolder with failing case.
5. **Update `examples/README.md`** — add row to example index.
6. **Review gate** — submit for Contribution Gate.

### Gate Criteria

| Criterion | Check |
|-----------|-------|
| Path correct | `examples/<name>/README.md` exists |
| Purpose stated | README explains what the example shows |
| At least one noun | Example includes a noun definition |
| Index updated | `examples/README.md` includes example |

### Incomplete-Packet Fixture

**Scenario:** Example folder created without README.md.

**Required outcome:** **REFUSE** — incomplete (no entry point).

**Status:** STUB — expand with example template.

---

## Adding a New Content Type

When a new content type is needed:

1. **Propose via ADR** — rationale for the new content type.
2. **Define type recipe** — add section to this document.
3. **Include inputs, steps, gate criteria, and incomplete-packet fixture**.
4. **Update index table** at top of this document.
5. **Contribution Gate applies** — the type recipe addition is itself a contribution.

Type recipes are themselves governed by the Contribution Gate. A type recipe without an incomplete-packet fixture is incomplete (CG-R5 applies to this document too).

---

## Cross-references

- [`../integrity/CONTRIBUTION.md`](../integrity/CONTRIBUTION.md) — shared docs standard, Contribution Gate
- [`../integrity/LEXICON.md`](../integrity/LEXICON.md) — locked definitions (Type recipe, Content type)
- [`../integrity/GATE.md`](../integrity/GATE.md) — G1–G4 fitness bar
- [`../adrs/README.md`](../adrs/README.md) — ADR index
- [`../integrity/README.md`](../integrity/README.md) — integrity index
- [`../agents/README.md`](../agents/README.md) — agent noun index
- [`../examples/README.md`](../examples/README.md) — example index
