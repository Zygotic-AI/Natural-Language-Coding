# [PLANIT](../../../../docs/TERMS.md#planit) process (SSOT)

Normative source: [`docs/ai-compiled-systems/PROCESS.md`](../../../../docs/ai-compiled-systems/PROCESS.md).

Vocabulary and roles: [`docs/ai-compiled-systems/MERGE.md`](../../../../docs/ai-compiled-systems/MERGE.md).

[AWL](../../../../docs/TERMS.md#awl) overlay (intake, applicability, `GATE-STD`, tiers): [`docs/ai-compiled-systems/PLANIT-ORCHESTRATION.md`](../../../../docs/ai-compiled-systems/PLANIT-ORCHESTRATION.md) and [`audited-work-loop-standard.md`](audited-work-loop-standard.md).

## Loop

**Load → [interview](../../../../docs/TERMS.md#interview) → plan → product statements → bind → close gaps → generate → [verify](../../../../docs/TERMS.md#verify).**

[BBP](../../../../docs/TERMS.md#bbp) is bound on every statement by default (`CHARTER.md` is always on).

**Fail at [verify](../../../../docs/TERMS.md#verify)** → [RCA](../../../../docs/TERMS.md#rca) into **[interview](../../../../docs/TERMS.md#interview)** or **bind**, then **regenerate**. Humans do not patch generated files to silence an [audit](../../../../docs/TERMS.md#audit).

## Steps (summary)

| Step | Name | Stop if |
|------|------|---------|
| 0 | Load | Facts already bound are re-interviewed instead of loaded |
| 1 | [Interview](../../../../docs/TERMS.md#interview) | Goals/constraints cannot be named; incomplete → no plan |
| 2 | Plan | Items are not [goal](../../../../docs/TERMS.md#goal) / [boundary](../../../../docs/TERMS.md#boundary) / [requirement](../../../../docs/TERMS.md#requirement) / [ADR](../../../../docs/TERMS.md#adr) / **[rule](../../../../docs/TERMS.md#rule)** work |

| 3 | Product statements | A step needs more than one [boundary](../../../../docs/TERMS.md#boundary) |
| 4 | Bind | Any statement lacks [requirement](../../../../docs/TERMS.md#requirement) ids, [ADR](../../../../docs/TERMS.md#adr) ids, [rule](../../../../docs/TERMS.md#rule) ids when 0007 applies, or explicit unbound handling |

| 5 | Close gaps | Any statement still unbound or ambiguous |
| 6 | Generate | Scope exceeds one artifact; no metrics in the plan; humans edit output to “help” |
| 6.5 | [Gate](../../../../docs/TERMS.md#gate) that artifact | [Gate](../../../../docs/TERMS.md#gate) not run, evidence missing, or FAIL — do not start the next statement |
| 7 | [Prove](../../../../docs/TERMS.md#prove) | Machine [gate](../../../../docs/TERMS.md#gate) non-zero or adversarial [audit](../../../../docs/TERMS.md#audit) not PASS |


## [Prove](../../../../docs/TERMS.md#prove) (both required — compile, not ship)

1. **Machine [gate](../../../../docs/TERMS.md#gate)** — [hub](../../../../docs/TERMS.md#hub): `python3 tools/ci_fitness.py`. [Adopter](../../../../docs/TERMS.md#adopter): that tree’s bound fitness suite. Non-zero exit = fail.
2. **Adversarial [audit](../../../../docs/TERMS.md#audit)** — separate from the generator: statements done, bindings held, no second copy of an [adjective](../../../../docs/TERMS.md#adjective) inside a [goal](../../../../docs/TERMS.md#goal).

Fail → step **1** or **5**, then step **6** again.

**[Ship](../../../../docs/TERMS.md#ship)** is `python3 tools/release-audit.py <tree>` after a human `Released-by:`. [Prove](../../../../docs/TERMS.md#prove) PASS is not a release.


## [Knowledge domain](../../../../docs/TERMS.md#knowledge-domain) (step 1)

Before generate (machine gate): `python3 tools/nlc-before-generate.py --repo <tree> --scope …`. Steward verbs: `load-knowledge-domain` / `flag-gap`; new facts via `propose-fact`. See [`nlc-before-generate.md`](nlc-before-generate.md) and [`agents/knowledge-steward/AGENT.md`](../../../../agents/knowledge-steward/AGENT.md).

After [requirement](../../../../docs/TERMS.md#requirement) / verb / [rule](../../../../docs/TERMS.md#rule) change: `python3 tools/nlc-delta-regen.py` → execute JSON `steps` before emit.
