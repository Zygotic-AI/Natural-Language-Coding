# Manifesto

Software failures are usually not missing `if` statements. They are two truths about the same thing, each locally green.

**Code is not the product.** The product humans steward is **intent**: goals, requirements, and knowledge domains. Code is what the compiler emits—an object file. Tests, PRs, and user-visible behavior are **symptoms** of whether the process was sound.

The compiler is AI. That does not mean autocomplete in a file. It means: humans keep intent; the compiler emits a boundary-shaped system; a gate fails a quiet fork.

## Value stream

Work flows from stated intent to the user. Defects cost far more the later they are found—design cheap, production expensive. NLC does not ask you to memorize the curve; it asks you to **believe the direction** and act on it.

```text
goals · requirements · knowledge domains
        → compile (generate code)
        → automated tests & gates
        → change review
        → QA
        → UAT
        → user
```

**Principle:** audit every generated artifact **immediately after it is produced**, not only when a PR opens or QA starts. Pull discovery left; shrink what reaches the expensive stages.

Details and method names: [quality processes](QUALITY-PROCESSES.md).

## System vs symptoms

| Focus on the **system** (process) | Do not treat as the product (**symptoms**) |
| ----------------------------------- | ------------------------------------------ |
| Interview, bind, adoption, gates, RCA | Generated source as something to “fix by hand” |
| Goals, requirements, knowledge domains | One-off green CI without intent change |
| Adversarial audit right after emit | Blaming the last agent session |

When something is wrong, **root-cause as high on the value stream as the evidence allows**—tighten a requirement, adopt an ADR, fix a rule, close an interview gap—**before** rewarding a patch to generated code. Patching emit without intent change hides a process defect; the symptom returns downstream at higher cost.

## The source language

Not TypeScript. Not a class diagram.

```text
Intent (goals, requirements, knowledge domains, ADRs, adopted rules)
  → AI compile (PLANIT)
  → boundary-shaped code, tests, ops
```

The source is intent. The code is the object file. Who touches what: [intent surface](INTENT-SURFACE.md). How emit works: [how it codes](HOW-IT-CODES.md).

## Why shape still matters (without making you learn it first)

If the object file has no rule for where an adjective lives, two goals will each own `status`. Both goals can match the requirements. Users still find the expensive bug.

The compiler is not free to emit arbitrary structure. It emits a fixed architecture (BBA/BBP). That is **under the covers**—for auditors and gates—not the first thing a consumer learns.

Humans do not maintain noun files. They hire the compiler. If a human must edit generated code to keep adjectives consistent, the **architecture failed**. The loop is: gate red → RCA → tighter goal / requirement / ADR / knowledge domain → regenerate.

## Division of labor (summary)

**Humans focus on three things:** goals, requirements (standards and policies live here until adopted as ADRs/rules), and knowledge domains.

**Humans approve:** adopted ADRs, adopted if/then rules (and tag/primitive extensions when the closed set must grow), ratification and release when class requires it, certified RCA, accepted audit findings.

**Compiler creates:** nouns, verbs, adjective implementations, goal bodies, tests, and tag markings **as required by adopted rules**—not ad hoc labels at emit time.

Full table: [intent surface](INTENT-SURFACE.md).

## Process is the product

The entire emphasis is on the **value stream** and the **process** that walks it: default-closed gates, zero variance on prescribed actions, adversarial review separated from generation.

Defects live in the **system**—unbound statements, wrong adoption, skipped gates—not in “bad lines of code” as the primary diagnosis. The code is where the process failed **last**, not where the truth lives.

We pursue ever-better process through a non-negotiable commitment to industrial **quality processes** (lean + Six Sigma family)—without requiring every reader to learn that vocabulary up front. Early setups will be imperfect; **quality emerges** as knowledge domains, rules, gate history, and the interview catalog compound. See [quality processes](QUALITY-PROCESSES.md).

## Measure

A healthy system is not “more generated files.” It is: one home per adjective, every goal talking to that home through a contract, machine checks that fail when that is not true, and RCA that moves upstream—not patch downstream.
