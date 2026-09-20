# AIMS file map

Source: the 34-file “AI-Managed Software” suite (2026-09-15 zip).
Destination: this folder + `CHARTER.md`.
Name change: do not lead with “AIMS” or “AI-Managed” (ambiguous; ISO 42001 collision). Public name is **AI-Compiled Systems**.

## Folded into these pages

| Old file | Now |
|----------|-----|
| Manifesto | [MANIFESTO.md](MANIFESTO.md) |
| Architecture + Architecture V2 | [ARCHITECTURE.md](ARCHITECTURE.md) |
| AI Compiler spec + compiler ref arch | [COMPILER.md](COMPILER.md) |
| Playbook + Operating Model | [PROCESS.md](PROCESS.md) |
| Governance Framework | Process + CHARTER (no `/governance` product) |
| Ontology + metamodel + reference ontology | ARCHITECTURE citizen lists; CHARTER §§4–5 |
| Repo structure spec | CHARTER §8; generated/ is derived |
| Goal / Requirement authoring, ADR standard | Keep as later pages; CHARTER + PROCESS until written |
| Interview engine + pattern catalog | PROCESS steps 0–1, 5; [INTERVIEW-PATTERNS.md](INTERVIEW-PATTERNS.md) |
| RCA + Regeneration | PROCESS steps 6–7 |
| Traceability + dependency modeling + graph schema | Generated graph only (CHARTER R21) |
| Knowledge domain spec | MERGE.md + `knowledge/facts.json` |
| Roles | PROCESS roles table |

## Drop (do not freshen)

- Certification and maturity model
- Enterprise adoption / transformation / reference architecture
- Portfolio management (both copies)
- Body of Knowledge (AISWBOK)
- Duplicate Compliance / Graph / Portfolio filenames

Those are catalog gravity. They are not the compile gate.

## Still to write in this folder

- Goal authoring (from AIMS Goal Authoring Standard + “goals only call verbs”)
- Requirement authoring (constraints only; adjectives stay on the noun)
- Interview patterns — v1 [INTERVIEW-PATTERNS.md](INTERVIEW-PATTERNS.md); deepen miss log from real compiles
- RCA record shape

CHARTER.md stays the design SSOT while those pages land.
