# ADR 0037 — Charter non-R surfaces (§6 execution order, §16 systems model)

- Status: Accepted
- Date: 2026-09-23
- Deciders: Human manager
- Class: F (process)
- Corpus: nlc

## Context

[ADR 0031](0031-charter-ratification-program.md) closed the **R** id backlog via ADRs 0032–0035. [`integrity/charter-ratify-backlog.json`](../integrity/charter-ratify-backlog.json) still listed **non-R** residuals: charter §6 (order of agent execution) and §16 (systems model / ship roles) without a named decision trail.

## Decision

1. **§6 Order of agent execution** is ratified as operational law already enforced by:
   - [ADR 0010](0010-gate-after-every-generate.md) (gate after generate)
   - [ADR 0019](0019-guided-orchestration.md) (queue / resume)
   - [ADR 0024](0024-nlc-factory-spine.md) + [ADR 0030](0030-pipeline-wiring.md) (plan → bind → emit wire)
   - Planit / interview skills (AWL phases; no silent skip of audits)

2. **§16 Systems model** (agent nouns, produce handoff, ship vs compile) is ratified by:
   - [ADR 0003](0003-systems-extension-agent-nouns.md) (agent noun packages)
   - [ADR 0004](0004-produce-fitness-handoff.md) + [ADR 0005](0005-ssot-exit-evidence.md) (produce → fitness handoff)
   - [ADR 0020](0020-human-vs-agent-commands.md) + [ADR 0021](0021-verify-fast-and-deep.md) (human shell vs agent tools; verify paths)
   - [`docs/nlc/VERIFY-AND-SHIP.md`](../docs/nlc/VERIFY-AND-SHIP.md) (`Released-by:` vs compile green)

No new **R** ids. This ADR is the ratification pointer for non-R charter prose called out in Evaluate-NLC A1 residuals.

## Consequences

- `charter-ratify-backlog.json` `non_r_residuals` rows cite ADR 0037 as ratified.
- FINDINGS A1 non-R prose residual closes (soft-green → done for program scope).

## Related

- [ADR 0031](0031-charter-ratification-program.md)
