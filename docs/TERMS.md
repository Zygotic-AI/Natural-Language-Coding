# Terms dictionary

SSOT for vocabulary in this repository (NLC product, BBP emit shape, BBA integrity, and tooling). Other docs link here as `[term](TERMS.md#anchor)` (path relative to each file).

Charter-shaped **R** / **C** / **P** rules stay in [`CHARTER.md`](../CHARTER.md). Locked integrity nouns also appear in [`integrity/LEXICON.md`](../integrity/LEXICON.md).

After adding terms here, re-run `python3 tools/link-terms-dictionary.py` to refresh links in markdown across the repo.

---

## A

### ACS

Optional acronym for a **compiled system** artifact only—not the whole product. See [NAMES.md](ai-compiled-systems/NAMES.md).

### Action

Named unit of work with contracted I/O and a completion **gate**. See [ACTIONS.md](../integrity/ACTIONS.md).

### ADR

Architecture Decision Record—dated **why** for a choice; may reduce to **rules** when adopted.

### Adopter

Team repo running a **compiled system** (not the hub). See [BOOTSTRAP.md](adoption/BOOTSTRAP.md).

### Adjective

Descriptor owned by a **noun** (charter term—not “invariant”). One home per adjective; duplicates fail gates.

### Agent noun

Durable agent **role** with identity, adjectives, and contracted **verbs** (charter §16). See ADR 0003.

### AIMS

Retired name; folded into **NLC** + **PLANIT**. Do not use for the product.

### ASC

Optional acronym for the **compiler** (integrator docs only).

### Atomic action

**Action** that cannot split further without losing a binary **gate**.

### Audit

Role-based adversarial review producing findings; does not automatically block (**gate** blocks). See [GATE.md](../integrity/GATE.md).

### Audit receipt

Evidence that an **audit** ran; may satisfy a downstream **gate**.

### AWL

Agent workflow layering referenced inside the **planit** skill (phases, tier rules).

---

## B

### BBA

**Boundary-Based Architecture**—hub charter and **integrity** roof (`CHARTER.md`, `integrity/`).

### BBA-Bindings

Companion repo for **P-0xx** operating policies; index in [OPERATING_BINDINGS.md](OPERATING_BINDINGS.md).

### BBP

**Boundary-Based Programming**—emit shape: **noun**, **verb**, **adjective**, **goal**.

### Binding

Act of pointing plan statements at **R** / **C** / **ADR** / **rule** ids (not “binder” as a gate noun).

### Binding matrix

Requirement → audit → gate tooling map (`integrity/binding-matrix.json`).

### Blast radius

Set of **goals** / nouns / verbs that must **regenerate** when a requirement changes (**UC9**).

### Boundary

Pipeline stage that owns adjectives, is default-closed, and advances binarily. See [BOUNDARY.md](../integrity/BOUNDARY.md).

### Boundary artifact

Handoff-in, completion artifact, and success criteria for agent **use-cases** (§16).

### Brownfield

Adopting **NLC** in a repo that already has product code (**UC15** beta).

### bbp-confirmer

Hub skill: charter §11 + **fitness** evidence before ship-class work.

### bbp-proposer

Hub skill: spec-first implementation proposals.

### bbp-recorder

Hub skill: **ADR** or “no ADR, reason.”

### bbp-reviewer

Hub skill: adversarial review citing **R** / **C** / **P**.

---

## C

### C (confirmation id)

Checklist line on one change (e.g. C24 release). See [NAMES.md](ai-compiled-systems/NAMES.md).

### Call-tree pack

**UC20**—inventory verb → interior **primitives**; parked.

### Change adversarial

App `.nlc/change-adversarial.json`—**Q2** execution audit snapshot for **verify-deep**.

### Change class

Charter classes A–F for what kind of change is proposed (**UC6**).

### Charter

Living BBP spec—[`CHARTER.md`](../CHARTER.md).

### Code pack

**UC16**—swap a **noun** interior (e.g. Python → Rust) with unchanged contracts; see [LANGUAGE-SCANNER.md](LANGUAGE-SCANNER.md).

### Compiled system

Runnable **BBP**-shaped tree in an **adopter** repo—not `examples/` **specimens**.

### Compiler

**AI system compiler**—interview → plan → bind → generate → gate → **prove**.

### Compound action

**Action** composed of other actions, each gated, plus an outer **gate**.

### Confirmer

Path that runs **fitness** + charter §11 evidence (often **bbp-confirmer**).

### Content type

First-class artifact class (ADR, integrity doc, **agent noun**, …) with a **type recipe**.

### Contribution Gate

Refuse-wired gate for **add-X** contributions. See [CONTRIBUTION.md](../integrity/CONTRIBUTION.md).

### Contract

**Noun-verb** payload contract vs **goal** envelope (charter §4.5). **Published verb contract** is the edge others depend on (**ADR 0006**).

---

## D

### Default-closed

Work does not advance until a **gate** or **handoff** explicitly opens.

### Defect

Quality metric: outcome that deviated from spec (FAIL, **handoff_refused**, error).

### Delta-regen queue

`.nlc/delta-regen-queue.json`—ordered **UC9** rebuild steps; open queue blocks **verify**.

### Durability

Runtime property of a **goal** (wait/retry/human)—not a fourth design primitive.

---

## G

### G1–G4

All-required PASS bar for **gates** and **handoffs**. See [GATE.md](../integrity/GATE.md).

### Gate

Binary PASS/FAIL enforcement; automated and default-closed. ≠ **audit**, ≠ human review.

### Gate record

`.nlc/gate-records.json` receipt after **PLANIT** 6.5 (**ADR 0010**). See [GATE-RECORD-BINDER.md](nlc/GATE-RECORD-BINDER.md).

### Goal

Use-case orchestration boundary; calls **verbs** and other goals; never writes **noun** fields.

### God-noun

Plan audit finding: one noun carrying adjectives that belong elsewhere.

### Greenfield

New app via `nlc-init` / **UC15**.

---

## H

### Handoff

Refuse-wired **gate** between **boundaries**; `handoff_refused` ≠ fitness FAIL.

### handoff_refused

Produce/handoff incomplete signal—not a content defect score.

### Hub

This repo—compiler, tools, skills; ships no product requirements (**ADR 0016**).

### Human interview

ADR **0018** shape: problem, gaps, ask, choices, examples on human CLI failures.

---

## I

### Integrity

Principles, matrix, audits, zero-variance practice (`integrity/`).

### Intent surface

What humans touch vs what the **compiler** emits—[INTENT-SURFACE.md](ai-compiled-systems/INTENT-SURFACE.md).

### Interview

**UC1** / `/interview`—bind **goals**, **requirements**, **knowledge domains**.

---

## J

### Jidoka

Stop on gate FAIL; **RCA** upstream—do not patch emit to green.

---

## K

### Knowledge domain

Standing facts and references for interview/bind—not a fourth code citizen (**UC18**).

### Knowledge fact

Row in `knowledge/facts.json` rules can bind; unbound → interview continues.

---

## L

### Lock file

`.nlc/lock.json` pins hub semver for an **adopter** (**ADR 0015**).

---

## M

### MET

Machine apex line: check passed (CI/agents). Not the first line humans should read (**ADR 0018**).

### Migration unit

`migrations/X_to_Y/` step for hub upgrade (**ADR 0014**): noop | script | interview.

---

## N

### NLC

**Natural Language Coding**—the product.

### NOT_MET

Machine apex line: check failed.

### Noun

Domain identity, state, and **adjectives**; no **noun inheritance** (ADR 0008).

### Noun inheritance

Rejected pattern—reuse via **verbs** / composition, not subclassing nouns.

---

## O

### Op

Quality metric: opportunity completed as specified (PASS, **MET**, ready).

### Opportunity

Single **gate** / verb / **handoff** execution with a binary outcome.

---

## P

### P (principle id)

Hub integrity principle P1–P7—not **P-0xx** operating policies.

### P-0xx

Operating policy in **BBA-Bindings** (handoff default-closed, SSOT exit, …).

### Plan audit

`.nlc/plan-audit.json`—**bbp-reviewer** **Q2** while **planit** is active.

### PLANIT

Orchestrated loop: load → interview → plan → bind → generate → gate → **prove** (`/planit`).

### Primitive

Closed interior function name **verbs** call ([`integrity/primitives.md`](../integrity/primitives.md), ADR 0009).

### Produce package

JSON with **quality evidence**, **SSOT exit** fields, optional **quality snapshot** (ADR 0004/0005).

### Produce ≠ Audit ≠ Ship

Separate roles: create artifact, review artifact, authorize release.

### Prove

Machine **fitness** + adversarial audit = compile green—not **ship**.

### Published verb contract

Contract edge dependents use; breaking change stays red until requirement accepted (**ADR 0006**).

---

## Q

### Q (quality metric id)

Quality evidence rules Q1–Q5. See [QUALITY_METRIC.md](../integrity/QUALITY_METRIC.md).

### Q1–Q5

Refuse rules for quality evidence at fitness, audit, and boundary exit.

### Quality

`Ops / Opportunities`—defect-free rate, not a vibe score.

### Quality snapshot

**Q2** adversarial JSON shape (`opportunities`, `ops`, `defects`, `quality`).

### Quality evidence

**Q1** produce-side evidence array for **produce package** / fitness handoff.

---

## R

### R (requirement id)

Charter rule the shape/code must keep.

### Ratified-by

Human sign-off line when change class requires ratification.

### RCA

Root cause analysis upstream of emit defects (**UC10**).

### REFUSE

Gate/handoff outcome when checks cannot run or packet is incomplete.

### Released-by

Human sign-off for release liability (**C24** / ship).

### Requirement

Constraint or policy in prose until **ADR** / **rule** adoption.

### Requirement pack

Versioned ADR/rule bundle export/install (hub v0.2). See [REQUIREMENT-PACKS.md](nlc/REQUIREMENT-PACKS.md).

### Rule

Adopted if/then over **tags**, **primitives**, and **facts** (ADR 0007).

### Rule IR

Executable rule runner—parked; v1 uses tags + fitness stand-ins.

### Rule precedence tier

**UC14** / ADR 0012—wins on conflicting effects at adopt time.

---

## S

### S / CS

Agent-noun structure / confirmation-systems id prefixes.

### Shared docs standard

Structure and refuse rules for SSOT docs—[CONTRIBUTION.md](../integrity/CONTRIBUTION.md).

### Ship

Human **Released-by** (and **Ratified-by** when required) after **prove**.

### ship-check

`./nlc ship-check`—promotion + human release gates.

### Specimen

`examples/` tree for gates to go red/green—not a **compiled system**.

### SSOT exit evidence

`ssot_leaf_ids` + `ssot_exit_status` on **produce package** (P-020).

### Standing requirements

Requirements that apply across **goals** (retention, engine, …).

---

## T

### Tag

Classification on nouns/adjectives (`pan`, `runtime=temporal`, …) feeding **rules**.

### Type recipe

Steps and **gate** criteria for adding a **content type** instance.

---

## U

### UC1–UC21

Numbered use-case stories—[USE-CASES.md](USE-CASES.md).

### UC9

Requirement change → impact graph → **delta-regen** queue.

### UC14

**Rule** conflict detection at adoption.

### UC15

**Greenfield** / **brownfield** adopt.

### UC16

**Code pack** interior swap.

### UC18

**Knowledge domain** / facts before generate.

### UC19

Retired—hub does not ship product requirements (**ADR 0016**).

### UC20

**Call-tree pack**.

### UC21

**Gate** immediately after every generate (**ADR 0010**).

### Use-case (systems)

Orchestration across **agent nouns** (§16)—distinct from **goal** in product code.

---

## V

### Verb (on noun)

Only legal **noun** mutation; contracted I/O and **primitives**.

### Verb (on agent noun)

Contracted agent function with I/O and failure mode.

### verify

Fast fingerprints (`.nlc/verified.json`) + policy blockers.

### verify-deep

Full **fitness** / release-audit path + refresh fingerprints (**ADR 0021**).

### Version store

Hub semver trees under install root (**ADR 0015**).

---

## W

### Waived

Explicit waiver line in handoff/ADR; empty `Waived:` fails **verify**.

### Work queue

`.nlc/work-queue.json`—dashboard scan of next human/agent steps.

### Workflow

Durable composition of **goals** when one process is not enough.

---

## Z

### Zero variance

Charter §5.8—prescribed actions only; hard **gates**; complete/incomplete.
