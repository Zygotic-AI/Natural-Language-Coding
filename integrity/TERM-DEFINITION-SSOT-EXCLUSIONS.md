# Term definition scan exclusions (O11)

`fitness-term-definition-ssot.py` refuses term definitions outside **`docs/TERMS.md`**.

## Allowed definition source

| Path | Reason |
|------|--------|
| `docs/TERMS.md` | Sole term-definition SSOT |

## Path prefix exclusions

| Path | Reason |
|------|--------|
| `docs/history/` | Archive |
| `docs/rca/` | RCA packets |
| `theory/history/` | Frozen theory |
| `tools/nouns/term_definition_bypass_fixtures/` | Term landmine plants |
| `reviews/` | Ephemeral review packets |
| `node_modules/` | Third-party |
| `.git/` | VCS |

## Exact path exclusions

| Path | Reason |
|------|--------|
| `integrity/TERM-DEFINITION-SSOT-EXCLUSIONS.md` | Meta exclusions doc |
| `integrity/GAP-LIST-SSOT-EXCLUSIONS.md` | Gap exclusions meta |

## Line exemptions (file scanned; matching lines ignored)

| Path | Reason |
|------|--------|
| `line:CHARTER.md` | Charter id-prefix table (P/R/C/Q), not term defs |
| `line:CHARTER.md` | Charter confirmation checklist |
| `line:CHARTER.md` | Charter agent-noun checklist |
| `line:integrity/GATE.md` | Gate tip checklist (CG1–CG4) |
| `line:integrity/GATE.md` | Gate binder link headings to TERMS |
| `line:integrity/CONTRIBUTION.md` | Contribution gate checklist |
| `line:integrity/BOUNDARY.md` | Boundary checklist |
| `line:integrity/PRINCIPLES.md` | Principle checklist |
| `line:docs/nlc/RULE-TRACE.md` | Operational binder section title cross-ref |
| `line:docs/nlc/RCA-PACKET.md` | RCA packet gate section title |
| `line:docs/nlc/IMPLEMENTATION-COMPLEXITY-EXAMINATION-PLAN.md` | Examination plan gate section title |
| `line:docs/adoption/RELEASE-ZERO-PARAMS-PLAN.md` | Release plan prove section title |
| `line:docs/bba/BBA-EMIT-PROCESS.md` | Emit process table column headers |
| `line:docs/bba/POLICY-ADR-LINEAGE.md` | Lineage doc section title |
| `line:docs/nlc/compiler/INTENT-SURFACE.md` | Intent surface comparison table header |
| `line:examples/` | Specimen trees (negative/positive fixtures) |
| `line:adrs/` | ADR boilerplate headings |

Pointer stubs (`integrity/LEXICON.md`, `docs/nlc/compiler/GLOSSARY.md`, `NAMES.md`, `RULE-VOCAB.md`) are **scanned**; they must stay short pointers with no inline definitions.

Implementation: `tools/nouns/term_definition_ssot/term_definition_exclusions.py`.
