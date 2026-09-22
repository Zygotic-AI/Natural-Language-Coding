# Manifesto

Software failures are usually not missing `if` statements. They are two truths about the same thing, each locally green.

**Code is not the product.** The product humans steward is **intent**: goals, requirements, and [knowledge domains](../TERMS.md#knowledge-domain). Code is what the [compiler](../TERMS.md#compiler) emits—an object file. Tests, PRs, and user-visible behavior are **symptoms** of whether the process was sound.

The [compiler](../TERMS.md#compiler) is AI. That does not mean autocomplete in a file. It means: humans keep intent; the [compiler](../TERMS.md#compiler) emits a boundary-shaped system; a [gate](../TERMS.md#gate) fails a quiet fork.

## Value stream

Work flows from stated intent to the user. Defects cost far more the later they are found—design cheap, production expensive. [NLC](../TERMS.md#nlc) does not ask you to memorize the curve; it asks you to **believe the direction** and act on it.

```text
goals · requirements · knowledge domains
        → compile (generate code)
        → automated tests & gates
        → change review
        → QA
        → UAT
        → user
```

**Principle:** [audit](../TERMS.md#audit) every generated artifact **immediately after it is produced**, not only when a PR opens or QA starts. Pull discovery left; shrink what reaches the expensive stages.

Details and method names: [quality processes](QUALITY-PROCESSES.md).

## System vs symptoms

| Focus on the **system** (process) | Do not treat as the product (**symptoms**) |
| ----------------------------------- | ------------------------------------------ |
| [Interview](../TERMS.md#interview), bind, adoption, gates, [RCA](../TERMS.md#rca) | Generated source as something to “fix by hand” |
| Goals, requirements, [knowledge domains](../TERMS.md#knowledge-domain) | One-off green CI without intent change |
| Adversarial [audit](../TERMS.md#audit) right after emit | Blaming the last agent session |

When something is wrong, **root-cause as high on the value stream as the evidence allows**—tighten a [requirement](../TERMS.md#requirement), adopt an [ADR](../TERMS.md#adr), fix a [rule](../TERMS.md#rule), close an [interview](../TERMS.md#interview) gap—**before** rewarding a patch to generated code. Patching emit without intent change hides a process [defect](../TERMS.md#defect); the symptom returns downstream at higher cost.

## The source language

Not TypeScript. Not a class diagram.

```text
Intent (goals, requirements, knowledge domains, ADRs, adopted rules)
  → AI compile (PLANIT)
  → boundary-shaped code, tests, ops
```

The source is intent. The code is the object file. Who touches what: [intent surface](INTENT-SURFACE.md). How emit works: [how it codes](HOW-IT-CODES.md).

## Why shape still matters (without making you learn it first)

If the object file has no [rule](../TERMS.md#rule) for where an [adjective](../TERMS.md#adjective) lives, two goals will each own `status`. Both goals can match the requirements. Users still find the expensive bug.

The [compiler](../TERMS.md#compiler) is not free to emit arbitrary structure. It emits a fixed architecture (BBA/BBP). That is **under the covers**—for auditors and gates—not the first thing a consumer learns.

Humans do not maintain [noun](../TERMS.md#noun) files. They hire the [compiler](../TERMS.md#compiler). If a human must edit generated code to keep adjectives consistent, the **architecture failed**. The loop is: [gate](../TERMS.md#gate) red → [RCA](../TERMS.md#rca) → tighter [goal](../TERMS.md#goal) / [requirement](../TERMS.md#requirement) / [ADR](../TERMS.md#adr) / [knowledge domain](../TERMS.md#knowledge-domain) → regenerate.

## Division of labor (summary)

**Humans focus on three things:** goals, requirements (standards and policies live here until adopted as ADRs/rules), and [knowledge domains](../TERMS.md#knowledge-domain).

**Humans approve:** adopted ADRs, adopted if/then rules (and tag/primitive extensions when the closed set must grow), ratification and release when class requires it, certified [RCA](../TERMS.md#rca), accepted [audit](../TERMS.md#audit) findings.

**[Compiler](../TERMS.md#compiler) creates:** nouns, verbs, [adjective](../TERMS.md#adjective) implementations, [goal](../TERMS.md#goal) bodies, tests, and [tag](../TERMS.md#tag) markings **as required by adopted rules**—not ad hoc labels at emit time.

Full table: [intent surface](INTENT-SURFACE.md).

## Process is the product

The entire emphasis is on the **value stream** and the **process** that walks it: [default-closed](../TERMS.md#default-closed) gates, [zero variance](../TERMS.md#zero-variance) on prescribed actions, adversarial review separated from generation.

Defects live in the **system**—unbound statements, wrong adoption, skipped gates—not in “bad lines of code” as the primary diagnosis. The code is where the process failed **last**, not where the truth lives.

We pursue ever-better process through a non-negotiable commitment to industrial **[quality](../TERMS.md#quality) processes** (lean + Six Sigma family)—without requiring every reader to learn that vocabulary up front. Early setups will be imperfect; **[quality](../TERMS.md#quality) emerges** as [knowledge domains](../TERMS.md#knowledge-domain), rules, [gate](../TERMS.md#gate) history, and the [interview](../TERMS.md#interview) catalog compound. See [quality processes](QUALITY-PROCESSES.md).

## Measure

A healthy system is not “more generated files.” It is: one home per [adjective](../TERMS.md#adjective), every [goal](../TERMS.md#goal) talking to that home through a [contract](../TERMS.md#contract), machine checks that fail when that is not true, and [RCA](../TERMS.md#rca) that moves upstream—not patch downstream.
