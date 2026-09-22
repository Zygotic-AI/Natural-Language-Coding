# [Quality](../TERMS.md#quality) processes

How [Natural Language Coding](../TERMS.md#nlc) uses [lean](https://en.wikipedia.org/wiki/Lean_manufacturing) and [Six Sigma](https://en.wikipedia.org/wiki/Six_Sigma) ideas **in this repo**. The [manifesto](MANIFESTO.md) states principles in plain language; this page names the methods and maps them to [PLANIT](../TERMS.md#planit), gates, and the [intent surface](../TERMS.md#intent-surface).

Public reference metrics (example): [Zygotic.ai](https://zygotic.ai) — illustrative of automatic [quality](../TERMS.md#quality) display; not a [charter](../TERMS.md#charter) [requirement](../TERMS.md#requirement).

## Value stream and [defect](../TERMS.md#defect) cost

[Defect](../TERMS.md#defect) cost rises sharply the later a mistake is found. Classic teaching uses orders of magnitude from design through production (often summarized as “$1 in design → $10 in code → … → $100k in the field”). [NLC](../TERMS.md#nlc) does not treat those numbers as literal invoices; they justify **where** to spend attention.

```text
Intent (goals, requirements, knowledge domains)
    → compile / generate (developer-equivalent)
    → automated tests & machine gates
    → change review (PR / adversarial audit)
    → broader QA
    → UAT
    → production user
```

**Design move:** adversarial [audit](../TERMS.md#audit) **immediately after** each generated artifact (PLANIT step 6.5), not only at PR or release. That pulls discovery left on the stream and compounds savings on every later stage.

## System vs symptoms

| | System (process) | Symptoms (outputs) |
| - | ---------------- | -------------------- |
| **What** | [Interview](../TERMS.md#interview), bind, adoption, gates, [RCA](../TERMS.md#rca), catalog of misses | Generated source, failing test output, red CI, user-reported bug |
| **Where defects belong** | Wrong [requirement](../TERMS.md#requirement), unbound statement, bad adoption, skipped [gate](../TERMS.md#gate) | Visible in code only **after** process failed |
| **Fix order** | [RCA](../TERMS.md#rca) as **high** on the stream as evidence allows; tighten intent or process | Patch generated code to green **without** intent change — refused (UC10) |

Symptoms are signals. Treating the symptom as the product turns every fix into a downstream $10^n event.

## Methods we align to (glossary)

Use these names here and in internal runbooks—not in the short manifesto.

| Term | Meaning here | [NLC](../TERMS.md#nlc) hook |
| ---- | ------------ | -------- |
| **DFSS** (Design for Six Sigma) | Design [quality](../TERMS.md#quality) in before scale; voice of customer → measurable requirements | [Interview](../TERMS.md#interview) + bind; requirements and ADRs before emit |
| **DMADV** | Define, Measure, Analyze, Design, [Verify](../TERMS.md#verify) — new product / new flow | [PLANIT](../TERMS.md#planit) 0–7 on a new [goal](../TERMS.md#goal) or [boundary](../TERMS.md#boundary); [prove](../TERMS.md#prove) = [Verify](../TERMS.md#verify) |
| **DMAIC** | Define, Measure, Analyze, Improve, Control — improve existing flow | [RCA](../TERMS.md#rca) after [gate](../TERMS.md#gate) FAIL; catalog [interview](../TERMS.md#interview) misses; tighten gates |
| **Value stream** | End-to-end flow from intent to user value; waste = rework downstream | Goals → compile → [ship](../TERMS.md#ship); [`INTENT-SURFACE.md`](INTENT-SURFACE.md) |
| **[Jidoka](../TERMS.md#jidoka)** | Stop the line on [defect](../TERMS.md#defect); do not pass bad work downstream | [Gate](../TERMS.md#gate) FAIL stops next statement; [`lean-operating-principles`](../../.agents/skills/planit/references/lean-operating-principles.md) in [Planit](../TERMS.md#planit) |
| **Andon** | Visible signal that work stopped | Red fitness, `handoff_refused`, [audit](../TERMS.md#audit) FAIL verdicts |
| **Inherent / automatic [quality](../TERMS.md#quality)** | Measure [quality](../TERMS.md#quality) in the process, not only inspect at the end | Per-artifact [gate](../TERMS.md#gate) (ADR 0010), [binding matrix](../TERMS.md#binding-matrix), `ci-fitness.sh` |
| **Voice of the customer** | Stated outcomes and constraints | Goals, requirements, and [knowledge domains](../TERMS.md#knowledge-domain) |

## Non-negotiable commitment (operational)

Perfection is not a release criterion. **Direction** is: every cycle that runs through [NLC](../TERMS.md#nlc) should leave the **process** measurably tighter—better requirements, fewer unbound statements, faster [RCA](../TERMS.md#rca) to intent, richer [interview](../TERMS.md#interview) catalog ([`docs/RISKS-AND-CONCERNS.md`](../RISKS-AND-CONCERNS.md) §1.7).

Early deployments are expected to be uneven. **Emergent [quality](../TERMS.md#quality):** as [knowledge domains](../TERMS.md#knowledge-domain), rules, and [gate](../TERMS.md#gate) history grow, the same [compiler](../TERMS.md#compiler) inputs produce fewer downstream surprises. [Quality](../TERMS.md#quality) is a property of the **system in use**, not a one-time certification.

## Related pages

- [MANIFESTO.md](MANIFESTO.md) — principles without acronym soup
- [PROCESS.md](PROCESS.md) — [PLANIT](../TERMS.md#planit) steps and [prove](../TERMS.md#prove) vs [ship](../TERMS.md#ship)
- [INTENT-SURFACE.md](INTENT-SURFACE.md) — human focus at stream start
- [`integrity/QUALITY_METRIC.md`](../../integrity/QUALITY_METRIC.md) — ops vs defects (Q1–Q5)
