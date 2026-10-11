# Terms dictionary

SSOT for vocabulary in this repository (NLC product, BBP emit shape, BBA integrity, and tooling). Other docs link here as `[term](TERMS.md#anchor)` (path relative to each file). **Do not define terms elsewhere** — [`integrity/LEXICON.md`](../integrity/LEXICON.md), [`docs/nlc/compiler/GLOSSARY.md`](nlc/compiler/GLOSSARY.md), [`docs/nlc/compiler/NAMES.md`](nlc/compiler/NAMES.md), and [`docs/nlc/RULE-VOCAB.md`](nlc/RULE-VOCAB.md) are pointers only.

Charter-shaped **R** / **C** / **P** rules stay in [`CHARTER.md`](../CHARTER.md).

After adding terms here, re-run `python3 tools/link-terms-dictionary.py` to refresh links in markdown across the repo.

---

## A

### ACS

Optional acronym for a **compiled system** artifact only—not the whole product. See [NAMES.md](nlc/compiler/NAMES.md).

### Action

Named unit of work with contracted I/O. Every **action** has a completion **gate** (complete / incomplete). See [ACTIONS.md](../integrity/ACTIONS.md).

**Audit `A-LEXICON-ACTION`:** **Met** iff every artifact labeled “action” declares input, output, and **gate**. Not **met** if any action omits **gate**.

### Active set

The **tip** of every **lineage** — the only ADRs gates, overlay, audit, and RCA consult. Superseded links stay in history, not in the active set (ADR 0028).

### ADR

Architecture Decision Record—dated **why** for a choice; may reduce to **rules** when adopted. Policies compile into ADRs; ADRs form immutable **lineages** (ADR 0028).

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

An **action** that cannot decompose further without losing a meaningful **gate**.

**Audit `A-LEXICON-ATOMIC`:** **Met** iff no **atomic action** definition permits decomposition into gated sub-parts. Not **met** if an **atomic action** can be meaningfully split and each part still gated.

### Atomic verb

Member of the closed verb set — `create`, `read`, `write`, `update`, `delete`, `validate`, `emit`, `bind`. Compound verbs are sequences of these, never new primitives (ADR 0028). See [VERB-SET.md](bba/VERB-SET.md).

### Audit

Role-based adversarial review producing findings for a **ship** decision. Audits yield binary per-item outcomes (**met** / not **met**) but do not block automatically.

**Audit ≠ Gate.** Gates block the build; audits produce findings. See [`GATE.md`](../integrity/GATE.md).

### Audit receipt

Evidence artifact produced by an **audit**. An **audit receipt** is **gate evidence** when a **gate** requires proof an **audit** occurred (PASS / FAIL / REFUSE documented). **Audit receipt** is gate evidence; **audit** is not a **gate**.

### AWL

Agent workflow layering referenced inside the **planit** skill (phases, tier rules).

---

## B

### BBA

**Boundary-Based Architecture**—integrity and emit *architecture* under **NLC** (boundaries, contracts, hub integrity). Not the public product name. Distinct from **BBP** (the emit *practice*). Not NLC process law (ADR 0024).

**Conflict note (BBP vs BBA):** keep this split. Retired wording: RULE-VOCAB’s old “BBA = emit shape” line — **emit shape** belongs to **BBP** only; **BBA** is architecture/integrity under the covers.

### Operating bindings (P-0xx)

Hub-local index of **P-0xx** operating policies in [OPERATING_BINDINGS.md](OPERATING_BINDINGS.md) (handoff default-closed, SSOT exit evidence, raise-readiness refuse, …).

### BBP

**Boundary-Based Programming**—emit *practice* under **NLC**: **noun**, **verb**, **adjective**, **goal**. The compiler must emit this shape. Not the public product name.

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

Checklist line on one change (e.g. C24 release). See [NAMES.md](nlc/compiler/NAMES.md).

### Call-tree pack

**UC20**—inventory verb → interior **primitives**; parked.

### Change adversarial

App `.nlc/change-adversarial.json`—**Q2** execution audit snapshot for **verify-deep**.

### Change class

Charter classes A–F for what kind of change is proposed (**UC6**).

### Charter

BBP emit + integrity doctrine under the [NLC](#nlc) roof—[`CHARTER.md`](../CHARTER.md) ([ADR 0011](../adrs/0011-natural-language-coding-naming.md)).

### Code pack

**UC16**—swap a **noun** interior (e.g. Python → Rust) with unchanged contracts; see [LANGUAGE-SCANNER.md](LANGUAGE-SCANNER.md).

### Compiled system

Runnable **BBP**-shaped tree in an **adopter** repo—not `examples/` **specimens**.

### Compiler

**AI system compiler**—interview → plan → bind → generate → gate → **prove**.

### Compound action

An **action** composed of other **actions**, yet still possessing its own completion **gate**. Every inner **action** executes its own **gate**; the **compound action** also executes its outer **gate**.

**Audit `A-LEXICON-COMPOUND`:** **Met** iff every **compound action** definition (a) names its constituent actions, (b) each constituent has a **gate**, and (c) the compound has its own outer **gate**.

### Compound verb

Named **sequence** of **atomic verbs**, each gated, plus an outer gate. Not a primitive — composition, not a new verb (ADR 0028).

### Condition

The `if` of a **rule** — when the rule applies (ADR 0024).

### Confirmer

Path that runs **fitness** + charter §11 evidence (often **bbp-confirmer**).

### Content type

A first-class artifact class in the repository (ADR, integrity doc, **agent noun**, **audit** definition, example). Each **content type** has a **type recipe** prescribing how to add or amend instances.

**Audit `A-LEXICON-CONTENT-TYPE`:** **Met** iff each **content type** named in `content-types/` has a **type recipe**.

### Contribution Gate

The **refuse-wired** **gate** for contributions. Refuses when: **shared docs standard** not **met**; **type recipe** not followed; person names in SSOT surfaces; required fixture missing. See [`CONTRIBUTION.md`](../integrity/CONTRIBUTION.md) (CG-R1–CG-R7).

**Audit `A-LEXICON-CONTRIB-GATE`:** **Met** iff the **contribution gate** definition states **refuse** criteria and an incomplete-packet fixture. **Audit `A-LEXICON-CONTRIBUTION`:** **Met** iff every add-X instruction links to the **type recipe** and states the **contribution gate**.

### Contract

**Noun-verb** payload contract vs **goal** envelope (charter §4.5). **Published verb contract** is the edge others depend on (**ADR 0006**).

### Corpus

`nlc` = factory process. `bba` = emit shape. SSOT map: [`../integrity/rule-corpus.json`](../integrity/rule-corpus.json) (ADR 0024). Not a second ADR list.

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

Binary enforcement checkpoint: **PASS / FAIL / REFUSE** only—no partial, provisional, warn-only, or soft-pass. **Default-closed** and **refuse-wired** (if a check cannot run, the gate refuses). See [`GATE.md`](../integrity/GATE.md) (G1–G4 all-required PASS bar).

**Gate ≠ Audit.** Gates block automatically; audits produce findings for a decision-maker.

### Gate record

`.nlc/gate-records.json` receipt after **PLANIT** 6.5 (**ADR 0010**). See [GATE-RECORD-BINDER.md](nlc/GATE-RECORD-BINDER.md).

### Goal

**Compile-time intent only** (owner decision, RCA 3, approved 2026-10-10): a **goal** names what the compile must deliver. Runtime behavior lives in the **application** (the compiled system); NLC does not use the term **orchestrator**.

**Conflict note (Goal):** prior copy called goals an “orchestration boundary” — **retired**. Runtime-module rename is scheduled **v0.4**. Goals call **verbs** (and other goals) in emitted shape; they must not write **noun** fields directly.

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

What humans touch vs what the **compiler** emits—[INTENT-SURFACE.md](nlc/compiler/INTENT-SURFACE.md).

### Interview

**UC1** / `/interview`—bind **goals**, **requirements**, **knowledge domains**.

---

## J

### Jobs to be done

Adopter outcomes and **honest** mechanism status—[`JOBS-TO-BE-DONE.md`](JOBS-TO-BE-DONE.md) (not the UC id list in [USE-CASES.md](USE-CASES.md)).

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

### Lineage

Immutable chain of ADRs about one decision topic. Only the **tip** is in the **active set**; the chain is retained for audit (ADR 0028). See [POLICY-ADR-LINEAGE.md](bba/POLICY-ADR-LINEAGE.md).

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

### Obligation

The `then` of a **rule** — what must be true when the **condition** holds.

### Op

Quality metric: opportunity completed as specified (PASS, **MET**, ready).

### Opportunity

Single **gate** / verb / **handoff** execution with a binary outcome.

---

## P

### P (principle id)

Hub integrity principle P1–P7—not **P-0xx** operating policies.

### P-0xx

Operating policy indexed in [OPERATING_BINDINGS.md](OPERATING_BINDINGS.md) (handoff default-closed, SSOT exit, …).

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

Constraint, **standard**, or policy in prose until **ADR** / **rule** adoption.

### Requirement pack

Versioned ADR/rule bundle export/install (hub v0.2). See [REQUIREMENT-PACKS.md](nlc/REQUIREMENT-PACKS.md).

### Rule

Adopted if/then: **condition** (`if`) + **obligation** (`then`) + **gate**. May close over **tags**, **primitives**, and **facts** (ADR 0007). Each rule belongs to one **corpus** (`nlc` | `bba`) (ADR 0024).

### Rule IR

Executable rule runner—parked; v1 uses tags + fitness stand-ins.

### Rule precedence tier

**UC14** / ADR 0012—wins on conflicting effects at adopt time.

---

## S

### S / CS

Agent-noun structure / confirmation-systems id prefixes.

### Shared docs standard

Structure, naming, lexicon, evidence, role language, incomplete-packet **refuse**, and supersede rules for SSOT documents: (1) **Structure** — purpose, definition, refuse criteria, fixture, checklist, cross-refs; (2) **Naming** — predictable paths; (3) **Lexicon** — terms from **TERMS.md**; (4) **Evidence** — audits, binders, fixtures; (5) **Role language** — no person names in SSOT; (6) **Incomplete-packet refuse**; (7) **Supersede rules** (charter R22). See [`CONTRIBUTION.md`](../integrity/CONTRIBUTION.md).

**Audit `A-LEXICON-SHARED-DOCS`:** **Met** iff **shared docs standard** is documented and contribution gates enforce it.

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

Prescribed steps and **gate** criteria for adding or amending **content type** X: (1) **Inputs**; (2) **Steps**; (3) **Gate criteria**; (4) **Incomplete-packet fixture** (must FAIL). Index: [`content-types/HOW-TO-ADD.md`](../content-types/HOW-TO-ADD.md).

**Audit `A-LEXICON-TYPE-RECIPE`:** **Met** iff every **type recipe** documents inputs, steps, **gate** criteria, and incomplete-packet fixture.

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

Only legal **noun** mutation; contracted I/O and **primitives**. In BBA emit, verbs are **atomic** (ADR 0028).

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
