# Term definition scan exclusions (O11)

`fitness-term-definition-ssot.py` refuses term definitions outside **`docs/TERMS.md`**.

## Allowed definition source

| Path | Role |
|------|------|
| `docs/TERMS.md` | Sole term-definition SSOT |

## Pointer stubs (no definitions)

| Path |
|------|
| `integrity/LEXICON.md` |
| `docs/nlc/compiler/GLOSSARY.md` |
| `docs/nlc/compiler/NAMES.md` |
| `docs/nlc/RULE-VOCAB.md` |

## Excluded from scan

| Path / prefix | Reason |
|---------------|--------|
| `docs/history/`, `docs/rca/`, `theory/history/` | Archive / RCA packets |
| `adrs/` | ADR normative sections use term words as headings |
| `reviews/` | Ephemeral review packets |
| `examples/`, `tools/nouns/term_definition_bypass_fixtures/` | Fixtures and landmines |
| `CHARTER.md` | P/R/C/Q id-prefix table rows, not lexicon entries |
| `integrity/GATE.md` | Gate criteria binder (links `TERMS.md`) |
| Listed `docs/nlc/*` and `docs/bba/*` binders | Operational section titles (`Gate`, `Audit`, `Goal`, …) |
| `integrity/TERM-DEFINITION-SSOT-EXCLUSIONS.md`, `GAP-LIST-SSOT-EXCLUSIONS.md` | Meta docs |

Pointer stubs (`LEXICON.md`, `GLOSSARY.md`, `NAMES.md`, `RULE-VOCAB.md`) are **scanned**; they must stay short pointers with no inline definitions.

Implementation: `tools/nouns/term_definition_ssot/term_definition_ssot.py`.
