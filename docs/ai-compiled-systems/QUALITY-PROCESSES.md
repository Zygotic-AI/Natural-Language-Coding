# Quality processes

How Natural Language Coding uses [lean](https://en.wikipedia.org/wiki/Lean_manufacturing) and [Six Sigma](https://en.wikipedia.org/wiki/Six_Sigma) ideas **in this repo**. The [manifesto](MANIFESTO.md) states principles in plain language; this page names the methods and maps them to PLANIT, gates, and the intent surface.

Public reference metrics (example): [Zygotic.ai](https://zygotic.ai) — illustrative of automatic quality display; not a charter requirement.

## Value stream and defect cost

Defect cost rises sharply the later a mistake is found. Classic teaching uses orders of magnitude from design through production (often summarized as “$1 in design → $10 in code → … → $100k in the field”). NLC does not treat those numbers as literal invoices; they justify **where** to spend attention.

```text
Intent (goals, requirements, knowledge domains)
    → compile / generate (developer-equivalent)
    → automated tests & machine gates
    → change review (PR / adversarial audit)
    → broader QA
    → UAT
    → production user
```

**Design move:** adversarial audit **immediately after** each generated artifact (PLANIT step 6.5), not only at PR or release. That pulls discovery left on the stream and compounds savings on every later stage.

## System vs symptoms

| | System (process) | Symptoms (outputs) |
| - | ---------------- | -------------------- |
| **What** | Interview, bind, adoption, gates, RCA, catalog of misses | Generated source, failing test output, red CI, user-reported bug |
| **Where defects belong** | Wrong requirement, unbound statement, bad adoption, skipped gate | Visible in code only **after** process failed |
| **Fix order** | RCA as **high** on the stream as evidence allows; tighten intent or process | Patch generated code to green **without** intent change — refused (UC10) |

Symptoms are signals. Treating the symptom as the product turns every fix into a downstream $10^n event.

## Methods we align to (glossary)

Use these names here and in internal runbooks—not in the short manifesto.

| Term | Meaning here | NLC hook |
| ---- | ------------ | -------- |
| **DFSS** (Design for Six Sigma) | Design quality in before scale; voice of customer → measurable requirements | Interview + bind; requirements and ADRs before emit |
| **DMADV** | Define, Measure, Analyze, Design, Verify — new product / new flow | PLANIT 0–7 on a new goal or boundary; prove = Verify |
| **DMAIC** | Define, Measure, Analyze, Improve, Control — improve existing flow | RCA after gate FAIL; catalog interview misses; tighten gates |
| **Value stream** | End-to-end flow from intent to user value; waste = rework downstream | Goals → compile → ship; [`INTENT-SURFACE.md`](INTENT-SURFACE.md) |
| **Jidoka** | Stop the line on defect; do not pass bad work downstream | Gate FAIL stops next statement; [`lean-operating-principles`](../../.agents/skills/planit/references/lean-operating-principles.md) in Planit |
| **Andon** | Visible signal that work stopped | Red fitness, `handoff_refused`, audit FAIL verdicts |
| **Inherent / automatic quality** | Measure quality in the process, not only inspect at the end | Per-artifact gate (ADR 0010), binding matrix, `ci-fitness.sh` |
| **Voice of the customer** | Stated outcomes and constraints | Goals, requirements, and knowledge domains |

## Non-negotiable commitment (operational)

Perfection is not a release criterion. **Direction** is: every cycle that runs through NLC should leave the **process** measurably tighter—better requirements, fewer unbound statements, faster RCA to intent, richer interview catalog ([`docs/RISKS-AND-CONCERNS.md`](../RISKS-AND-CONCERNS.md) §1.7).

Early deployments are expected to be uneven. **Emergent quality:** as knowledge domains, rules, and gate history grow, the same compiler inputs produce fewer downstream surprises. Quality is a property of the **system in use**, not a one-time certification.

## Related pages

- [MANIFESTO.md](MANIFESTO.md) — principles without acronym soup
- [PROCESS.md](PROCESS.md) — PLANIT steps and prove vs ship
- [INTENT-SURFACE.md](INTENT-SURFACE.md) — human focus at stream start
- [`integrity/QUALITY_METRIC.md`](../../integrity/QUALITY_METRIC.md) — ops vs defects (Q1–Q5)
