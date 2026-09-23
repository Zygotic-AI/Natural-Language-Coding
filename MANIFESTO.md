# Manifesto

> Hub belief SSOT. Same body as [`docs/nlc/compiler/MANIFESTO.md`](docs/nlc/compiler/MANIFESTO.md) (canonical under `docs/nlc/compiler/`). Do not fork prose between the two.

Software failures are usually not missing `if` statements. They are two truths about the same thing, each locally green.

**Code is not the product.** The product humans steward is **intent**: goals, requirements, and [knowledge domains](docs/TERMS.md#knowledge-domain). Code is what the [compiler](docs/TERMS.md#compiler) emits—an object file. Tests, PRs, and user-visible behavior are **symptoms** of whether the process was sound.

The [compiler](docs/TERMS.md#compiler) is AI. That does not mean autocomplete in a file. It means: humans keep intent; the compiler emits a boundary-shaped system; a [gate](docs/TERMS.md#gate) fails a quiet fork.

**[NLC](docs/TERMS.md#nlc) — Natural Language Coding — is the product and the factory.** Everything else in this repo exists so that factory can compile or refuse. [BBA](docs/TERMS.md#bba) and [BBP](docs/TERMS.md#bbp) are subcomponents: the architecture and the emit practice the factory is allowed to produce. They are not peer products and not the public name.

## Thesis

1. Agents can write locally perfect code that is system-false. Perfect-looking files are the failure mode, not the goal.
2. The only honest product is the process that makes a false fork *refuse* — at emit, not at PR, QA, or production.
3. Humans own three surfaces: goals, requirements (until adopted as ADRs/rules), and knowledge domains. They approve adoption, ratification, release, certified RCA, and accepted audit findings.
4. The compiler owns emit: nouns, verbs, adjective implementations, goal bodies, tests, and tag markings required by adopted rules.
5. A red gate is a success. A green file that no longer matches intent is the defect.
6. When something is wrong, climb the value stream. Patching generated code without changing intent hides the process defect. The symptom returns later, more expensive.

That is the whole claim. The rest of this page is how we refuse to forget it.

## Belief

Agents can write perfect code. Perfect is not a talent claim. It is what happens when the process is suitable and the environment makes the unsuitable path refuse.

The product of this repository is that process. Compiled systems are the factory output. They are inevitable when the factory is honest.

### No blame

A defect is not an agent mistake. It is not a human mistake. It is evidence that a process was not suitable for the agents or humans who ran it.

[RCA](docs/TERMS.md#rca) does not ask who. RCA asks which process, if it had been different, would have made the original defect impossible. Then it asks what process produced *that* process. Climb until the disconnect is visible.

### Climb upstream

A local environment fix that would have changed this one incident is not root. Root is the condition that produced the environment.

If a later process (an interview skill, a rule pack, a compiler step) ships incomplete, the first finding is that process. The next question is what in *this* factory allowed that process to ship incomplete. Keep climbing.

### Buck stops here

This repo is the end of the climb. When the factory makes defects, they are disconnects between the belief on this page and an implementation that does not carry it.

This page is the belief. NLC is the factory that has to carry it.

## Principles (six)

1. **No blame.** Defects are process unsuitability, never agent or human failure. We never say the agent made a mistake or the human made a mistake — we say the process was not suitable for them.

2. **Root cause upstream.** Climb past the environment condition to the process that produced it, all the way to the belief. The one thing is always the furthest upstream process change that would have made the defect impossible.

3. **The buck stops here.** This repo is where the RCA chain terminates — at the belief-to-implementation disconnect. That is the deepest cause that exists, by design.

4. **Process is the product.** We are building a factory; the code is the inevitable output when the factory runs correctly. Even when the customer touches an application, the focus is the process that makes that product inevitable.

5. **Dogfood or don't preach.** The hub must pass its own gates — BBA/BBP at the foundation of *emit*, under the NLC roof — or the claim is unproven. Bootstrap is the only honest exception, and it must be explicit, time-boxed, and sunset.

6. **Audit immediately.** Catch the fork at emit, not at PR time. Every downstream patch costs more than fixing the process.

---

## The stack (NLC owns the name)

- **[NLC](docs/TERMS.md#nlc)** — Natural Language Coding. The product. Describe intent. Compile or [refuse](docs/TERMS.md#refuse).
- **[Compiler](docs/TERMS.md#compiler)** — `/interview` + `/planit` + gates. Turns bound intent into a [compiled system](docs/TERMS.md#compiled-system).
- **[BBP](docs/TERMS.md#bbp)** — Boundary-Based Programming. The emit *practice*: [nouns](docs/TERMS.md#noun) own [adjectives](docs/TERMS.md#adjective); verbs are the only mutation path; [goals](docs/TERMS.md#goal) orchestrate.
- **[BBA](docs/TERMS.md#bba)** — Boundary-Based Architecture. The emit *architecture* and hub [integrity](docs/TERMS.md#integrity) doctrine under NLC. Not the consumer name.

NLC without BBA/BBP underneath is surface compliance: a slogan with no refuse. BBA/BBP without NLC as the roof is a shape looking for a factory. The hub's own source is the first thing `./nlc verify` runs against.

Retired as product names: ACS-as-the-whole, AIMS, “governance.” Optional integrator acronyms only: ASC = compiler, ACS = compiled-system artifact.

---

## Value stream

Work flows from stated intent to the user. Defects cost far more the later they are found—design cheap, production expensive. [NLC](docs/TERMS.md#nlc) does not ask you to memorize the curve; it asks you to **believe the direction** and act on it.

```text
goals · requirements · knowledge domains
        → compile (generate code)
        → automated tests & gates
        → change review
        → QA
        → UAT
        → user
```

**Principle:** [audit](docs/TERMS.md#audit) every generated artifact **immediately after it is produced**, not only when a PR opens or QA starts. Pull discovery left; shrink what reaches the expensive stages.

Details and method names: [quality processes](docs/nlc/compiler/QUALITY-PROCESSES.md).

## System vs symptoms

| Focus on the **system** (process) | Do not treat as the product (**symptoms**) |
| ----------------------------------- | ------------------------------------------ |
| [Interview](docs/TERMS.md#interview), bind, adoption, gates, [RCA](docs/TERMS.md#rca) | Generated source as something to “fix by hand” |
| Goals, requirements, [knowledge domains](docs/TERMS.md#knowledge-domain) | One-off green CI without intent change |
| Adversarial [audit](docs/TERMS.md#audit) right after emit | Blaming the last agent session |

When something is wrong, **root-cause as high on the value stream as the evidence allows**—tighten a [requirement](docs/TERMS.md#requirement), adopt an [ADR](docs/TERMS.md#adr), fix a [rule](docs/TERMS.md#rule), close an [interview](docs/TERMS.md#interview) gap—**before** rewarding a patch to generated code. Patching emit without intent change hides a process [defect](docs/TERMS.md#defect); the symptom returns downstream at higher cost.

## The source language

Not TypeScript. Not a class diagram.

```text
Intent (goals, requirements, knowledge domains, ADRs, adopted rules)
  → AI compile (PLANIT)
  → boundary-shaped code, tests, ops
```

The source is intent. The code is the object file. Who touches what: [intent surface](docs/nlc/compiler/INTENT-SURFACE.md). How emit works: [how it codes](docs/nlc/compiler/HOW-IT-CODES.md).

## Why shape still matters (without making you learn it first)

If the object file has no [rule](docs/TERMS.md#rule) for where an [adjective](docs/TERMS.md#adjective) lives, two goals will each own `status`. Both goals can match the requirements. Users still find the expensive bug.

The [compiler](docs/TERMS.md#compiler) is not free to emit arbitrary structure. It emits a fixed architecture (BBA/BBP). That is **under the covers**—for auditors and gates—not the first thing a consumer learns.

Humans do not maintain [noun](docs/TERMS.md#noun) files. They hire the [compiler](docs/TERMS.md#compiler). If a human must edit generated code to keep adjectives consistent, the **architecture failed**. The loop is: [gate](docs/TERMS.md#gate) red → [RCA](docs/TERMS.md#rca) → tighter [goal](docs/TERMS.md#goal) / [requirement](docs/TERMS.md#requirement) / [ADR](docs/TERMS.md#adr) / [knowledge domain](docs/TERMS.md#knowledge-domain) → regenerate.

## Division of labor (summary)

**Humans focus on three things:** goals, requirements (standards and policies live here until adopted as ADRs/rules), and [knowledge domains](docs/TERMS.md#knowledge-domain).

**Humans approve:** adopted ADRs, adopted if/then rules (and tag/primitive extensions when the closed set must grow), ratification and release when class requires it, certified [RCA](docs/TERMS.md#rca), accepted [audit](docs/TERMS.md#audit) findings.

**[Compiler](docs/TERMS.md#compiler) creates:** nouns, verbs, [adjective](docs/TERMS.md#adjective) implementations, [goal](docs/TERMS.md#goal) bodies, tests, and [tag](docs/TERMS.md#tag) markings **as required by adopted rules**—not ad hoc labels at emit time.

Full table: [intent surface](docs/nlc/compiler/INTENT-SURFACE.md).

## Process is the product

The entire emphasis is on the **value stream** and the **process** that walks it: [default-closed](docs/TERMS.md#default-closed) gates, [zero variance](docs/TERMS.md#zero-variance) on prescribed actions, adversarial review separated from generation.

Defects live in the **system**—unbound statements, wrong adoption, skipped gates—not in “bad lines of code” as the primary diagnosis. The code is where the process failed **last**, not where the truth lives.

We pursue ever-better process through a non-negotiable commitment to industrial **[quality](docs/TERMS.md#quality) processes** (lean + Six Sigma family)—without requiring every reader to learn that vocabulary up front. Early setups will be imperfect; **[quality](docs/TERMS.md#quality) emerges** as [knowledge domains](docs/TERMS.md#knowledge-domain), rules, [gate](docs/TERMS.md#gate) history, and the [interview](docs/TERMS.md#interview) catalog compound. See [quality processes](docs/nlc/compiler/QUALITY-PROCESSES.md).

## Measure

A healthy system is not “more generated files.” It is: one home per [adjective](docs/TERMS.md#adjective), every [goal](docs/TERMS.md#goal) talking to that home through a [contract](docs/TERMS.md#contract), machine checks that fail when that is not true, and [RCA](docs/TERMS.md#rca) that moves upstream — not patch downstream.

A healthy *factory* is not a larger manifesto. It is: interview that refuses unbound claims, planit that emits one gated artifact at a time, verify that is not ship, and a hub that fails its own gates when the belief on this page is not in the code.
