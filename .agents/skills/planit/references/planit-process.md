# PLANIT process (SSOT)

Normative source: [`docs/ai-compiled-systems/PROCESS.md`](../../../../docs/ai-compiled-systems/PROCESS.md).

Vocabulary and roles: [`docs/ai-compiled-systems/MERGE.md`](../../../../docs/ai-compiled-systems/MERGE.md).

AWL overlay (intake, applicability, `GATE-STD`, tiers): [`docs/ai-compiled-systems/PLANIT-ORCHESTRATION.md`](../../../../docs/ai-compiled-systems/PLANIT-ORCHESTRATION.md) and [`audited-work-loop-standard.md`](audited-work-loop-standard.md).

## Loop

**Load → interview → plan → product statements → bind → close gaps → generate → prove.**

BBP is bound on every statement by default (`CHARTER.md` is always on).

**Fail at prove** → RCA into **interview** or **bind**, then **regenerate**. Humans do not patch generated files to silence an audit.

## Steps (summary)

| Step | Name | Stop if |
|------|------|---------|
| 0 | Load | Facts already bound are re-interviewed instead of loaded |
| 1 | Interview | Goals/constraints cannot be named; incomplete → no plan |
| 2 | Plan | Items are not goal / boundary / requirement / ADR / **rule** work |

| 3 | Product statements | A step needs more than one boundary |
| 4 | Bind | Any statement lacks requirement ids, ADR ids, rule ids when 0007 applies, or explicit unbound handling |

| 5 | Close gaps | Any statement still unbound or ambiguous |
| 6 | Generate | Scope exceeds one artifact; no metrics in the plan; humans edit output to “help” |
| 6.5 | Gate that artifact | Gate not run, evidence missing, or FAIL — do not start the next statement |
| 7 | Prove | Machine gate non-zero or adversarial audit not PASS |


## Prove (both required — compile, not ship)

1. **Machine gate** — hub: `bash tools/ci-fitness.sh`. Adopter: that tree’s bound fitness suite. Non-zero exit = fail.
2. **Adversarial audit** — separate from the generator: statements done, bindings held, no second copy of an adjective inside a goal.

Fail → step **1** or **5**, then step **6** again.

**Ship** is `python3 tools/release-audit.py <tree>` after a human `Released-by:`. Prove PASS is not a release.


## Knowledge shelf (step 1)

Before generate: knowledge-steward `load-shelf` / `flag-gap`; new facts via `propose-fact` (human manager accepts). See [`agents/knowledge-steward/AGENT.md`](../../../../agents/knowledge-steward/AGENT.md).
