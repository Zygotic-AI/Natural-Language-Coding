# Boundary-Based Programming

Central home for the practice: theory, agentic application, and tools — so humans and agents can change software without scattering invariants or widening blast radius.

**Tagline:** Stopping your agents from shipping slop.

## Start here

| Artifact | Role |
|----------|------|
| [`CHARTER.md`](CHARTER.md) | Living charter (rules, agent loop, systems model, checklists) |
| [`theory/history/og-interview-draft.md`](theory/history/og-interview-draft.md) | OG interview draft (historical; do not edit) |
| [`DESCRIBE.md`](DESCRIBE.md) | Repo memory for agents |
| [`TODO`](TODO) | Work queue |
| [`agents/`](agents/) | Agent loop roles + agent nouns (standards-steward, adversarial-auditor) |

## Layout

```text
.
├─ CHARTER.md          # authoritative practice charter (§4 software, §16 systems)
├─ theory/             # essays, rationale, history
├─ agents/             # loop roles + agent nouns
│   ├─ proposer.md, reviewer.md, …     # loop roles
│   ├─ standards-steward/              # agent noun
│   └─ adversarial-auditor/            # agent noun
├─ tools/              # fitness checks, scaffolding, generators
├─ examples/           # sample systems that adopt the charter
├─ adrs/               # decisions that later work must not quietly undo
├─ integrity/          # checklist + fitness-check home for this meta-repo
└─ .agents/            # portable skills / instructions (cross-harness)
```

This repo is the **practice hub**, not an application domain tree. Application repos that adopt BBP should follow the shape in charter §8 (`domain/`, `goals/`, `workflows/`, …).

## Status

Working charter from a design conversation. Not yet a ratified organizational standard. Adoption "done" criteria are in charter §14. Systems extension (§16) ratified by ADR 0003.
