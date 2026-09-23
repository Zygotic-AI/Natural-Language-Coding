# DESCRIBE.md — [Natural Language Coding](docs/TERMS.md#nlc) hub (BBP/BBA under the covers)

## What this repo is

**[Natural Language Coding](docs/TERMS.md#nlc) (NLC)** [hub](docs/TERMS.md#hub): goals and requirements in; [compiler](docs/TERMS.md#compiler) out a BBP-shaped **[compiled system](docs/TERMS.md#compiled-system)** or [refuse](docs/TERMS.md#refuse). BBP/BBA remain the design SSOT under the covers (`CHARTER.md`, `integrity/`). Tagline (consumer): stopping agents from shipping slop by compiling intent, not patching emit. Stand-alone branding: no foreign brand packages in [integrity](docs/TERMS.md#integrity); copy and re/unbrand if a shape is useful. Naming: [ADR](docs/TERMS.md#adr) 0011, [`docs/ai-compiled-systems/GLOSSARY.md`](docs/ai-compiled-systems/GLOSSARY.md).

## Core model (short)

- **[Noun](docs/TERMS.md#noun)** — identity, private state, adjectives; retrieval key for "how does X work?"
- **[Verb (on noun)](docs/TERMS.md#verb-on-noun)** — only legal mutation; contracted I/O
- **[Goal](docs/TERMS.md#goal)** — use-case orchestration (I/O, other nouns, policy); calls verbs; never writes [noun](docs/TERMS.md#noun) fields
- **[Workflow](docs/TERMS.md#workflow)** — durable composition of goals when one in-process call is not enough
- **[Charter](docs/TERMS.md#charter) + ADRs** — decisions and confirmable rules; adversarial review against the [charter](docs/TERMS.md#charter)
- **[Integrity](docs/TERMS.md#integrity) (zero variance)** — every [requirement](docs/TERMS.md#requirement) has a binary [audit](docs/TERMS.md#audit); every [action](docs/TERMS.md#action) has a hard [gate](docs/TERMS.md#gate); every [boundary](docs/TERMS.md#boundary) has hard I/O + failure mode; unbound / in-force-unbindable entries fail and are listed

### Systems model (§16)

Same structural discipline applied to organizing **agent fleets** — durable roles that operate a system over time. Ratified by [ADR](docs/TERMS.md#adr) 0003.

- **[Agent noun](docs/TERMS.md#agent-noun)** — durable role with identity and adjectives
- **[Verb (on agent noun)](docs/TERMS.md#verb-on-agent-noun)** — legal function; contracted I/O with input, output, failure mode
- **Use-case** — orchestration across [agent nouns](docs/TERMS.md#agent-noun) or to the outside world
- **[Boundary artifact](docs/TERMS.md#boundary-artifact)** — handoff-in, completion artifact, success criteria (ops vs defects)
- **[Produce ≠ Audit ≠ Ship](docs/TERMS.md#produce-audit-ship)** — separate who creates, who reviews, who authorizes release
- **[Audit](docs/TERMS.md#audit) roles have no shipping authority** — they produce findings, not decisions

### [Integrity](docs/TERMS.md#integrity) note: [BBA](docs/TERMS.md#bba) vs Bindings

**[BBA](docs/TERMS.md#bba)** (Boundary-Based Architecture) is the roof doctrine — confirmable rules in this repo that define how boundaries, handoffs, and [integrity](docs/TERMS.md#integrity) work (`CHARTER.md`, `integrity/`). **Bindings** is the operating policy map consumed by agent processes — P-series policies (P-016…P-031 class) that wire [refuse](docs/TERMS.md#refuse) criteria and evidence requirements to executable gates. Bindings live in the companion repo (`richardpickett/BBA-Bindings`). See [`docs/OPERATING_BINDINGS.md`](docs/OPERATING_BINDINGS.md) for the policy index.

## Key paths

| Path | Role |
|------|------|
| `CHARTER.md` | Living, authoritative [charter](docs/TERMS.md#charter) (§5.8 integrity, §16 systems model) |
| `theory/history/og-interview-draft.md` | OG [interview](docs/TERMS.md#interview) draft (frozen) |
| `theory/` | Theory and history |
| `agents/` | Agent loops, roles, prompts, [agent nouns](docs/TERMS.md#agent-noun) |
| `agents/standards-steward/` | [Agent noun](docs/TERMS.md#agent-noun): charter/ADR steward (no ship authority); query verbs for Session applicability |
| `agents/adversarial-auditor/` | [Agent noun](docs/TERMS.md#agent-noun): adversarial review (no ship authority) |
| `agents/ship-role/` | [Agent noun](docs/TERMS.md#agent-noun): authorize release (ship authority with mandate) |
| `tools/` | Gates, scaffolding, matrix auditor |
| `examples/` | [Adopter](docs/TERMS.md#adopter) sample systems |
| `adrs/` | Decision records (`0001` = [zero-variance](docs/TERMS.md#zero-variance), `0003` = systems extension) |
| `integrity/` | Principles, [binding matrix](docs/TERMS.md#binding-matrix), [audit](docs/TERMS.md#audit) defs |
| `integrity/GATE.md` | [Gate](docs/TERMS.md#gate) [noun](docs/TERMS.md#noun) SSOT (G1--G4, incomplete-packet hunt) |
| `integrity/QUALITY_METRIC.md` | [Quality](docs/TERMS.md#quality) metric SSOT (ops vs defects; Q1--Q5) |
| `integrity/BOUNDARY.md` | [Boundary](docs/TERMS.md#boundary) + [Handoff](docs/TERMS.md#handoff) [noun](docs/TERMS.md#noun) SSOT; role-bound SOP |
| `integrity/BOUNDED_CONTEXT.md` | Bounded Context [noun](docs/TERMS.md#noun) SSOT; living system-as-is knowledge (mechanisms, keys, adjectives) |
| `integrity/CONTRIBUTION.md` | [Shared docs standard](docs/TERMS.md#shared-docs-standard) + [Contribution Gate](docs/TERMS.md#contribution-gate) (G1--G4 refuse) |
| `integrity/LEXICON.md` | Locked term definitions (Action, Content type, Type recipe, etc.) |
| `integrity/ACTIONS.md` | [Action](docs/TERMS.md#action) [noun](docs/TERMS.md#noun) SSOT; gated [action](docs/TERMS.md#action) catalog; nesting [rule](docs/TERMS.md#rule) |
| `integrity/binding-matrix.json` | [Requirement](docs/TERMS.md#requirement) → [audit](docs/TERMS.md#audit) → [gate](docs/TERMS.md#gate) (JSON key is still `binder` until the auditor is updated) |
| `docs/OPERATING_BINDINGS.md` | Operating policy index (P-016…P-031 class); links to [BBA-Bindings](docs/TERMS.md#bba-bindings) companion |
| `content-types/HOW-TO-ADD.md` | Type recipes for adding content (ADR, integrity doc, agent noun, etc.) |
| `TODO` | Task list (`☐` / `✔ @done(...)`) |
| `AGENTS.md` | Cross-harness standing instructions |
| `.agents/` | Portable skills / instructions |

## Naming to avoid

Do not brand the practice "governance" / "governed." Prefer [charter](docs/TERMS.md#charter), [integrity](docs/TERMS.md#integrity), adversarial review. "Boundary-Enforced Programming" describes CI, not the practice title.

Settled vocabulary: **[adjective](docs/TERMS.md#adjective)** (not invariant/law), **[gate](docs/TERMS.md#gate)** (not binder-as-noun), **[binding](docs/TERMS.md#binding)** (the planning act).

## Terminology clarification (gate ≠ audit)

- **[Gate](docs/TERMS.md#gate)** = automated enforcement (fitness tools, CI rules); binary PASS/FAIL; blocks automatically; [default-closed](docs/TERMS.md#default-closed). See [`integrity/GATE.md`](integrity/GATE.md) for formal definition and all-required PASS fitness bar.
- **[Audit](docs/TERMS.md#audit)** = role-based adversarial review (adversarial-auditor agent noun); produces findings for [ship](docs/TERMS.md#ship) decision
- **[Produce ≠ Audit ≠ Ship](docs/TERMS.md#produce-audit-ship)** = separate [agent nouns](docs/TERMS.md#agent-noun) for creating artifacts, reviewing them, and authorizing release

Gates and audits both yield binary outcomes (ops vs defects), but differ in mechanism and authority. Gates block the build; audits produce findings for a ship-role or human to decide.

**All-required PASS bar (G1--G4):** A [gate](docs/TERMS.md#gate) is good only if incomplete work cannot PASS, every check is machine-checkable or [refuse-wired](docs/TERMS.md#default-closed), the last incomplete packet would FAIL it, and PASS does not require human redo. Design [rule](docs/TERMS.md#rule): write [refuse](docs/TERMS.md#refuse) + incomplete-packet fixture in the same tip. See [`integrity/GATE.md`](integrity/GATE.md).

## Terminology clarification (boundary ≠ handoff)

- **[Boundary](docs/TERMS.md#boundary)** = named stage in a work pipeline that owns adjectives, is [default-closed](docs/TERMS.md#default-closed), and produces binary advance. See [`integrity/BOUNDARY.md`](integrity/BOUNDARY.md).
- **[Handoff](docs/TERMS.md#handoff)** = [refuse-wired](docs/TERMS.md#default-closed) [gate](docs/TERMS.md#gate) between Boundaries; must meet G1--G4; `handoff_refused` ≠ fitness FAIL (produce-incomplete signal, not content defect).

Boundaries include: Plan, Conduct-RCA, Raise-Readiness, Produce, Fitness, Adversarial [Audit](docs/TERMS.md#audit), [Ship](docs/TERMS.md#ship), UAT/Promote, System-Remediate Design, Instance Heal. Role-bound SOP maps boundaries to roles (Plan Steward, Quality Architect, Adversarial Auditor, Ship Role, etc.) -- no person names in SOP tables.

**Incomplete-packet fixture:** 15855 without §7/R3/R4 must FAIL any raise-readiness [handoff](docs/TERMS.md#handoff). Policy wire: [P-030](https://github.com/richardpickett/BBA-Bindings/pull/9) on [BBA-Bindings](docs/TERMS.md#bba-bindings) main.

## Terminology clarification (action)

- **[Action](docs/TERMS.md#action)** = named, gated unit of work within a [boundary](docs/TERMS.md#boundary); executes through a [Gate](docs/TERMS.md#gate) or [Handoff](docs/TERMS.md#handoff). See [`integrity/ACTIONS.md`](integrity/ACTIONS.md).
- **[Atomic action](docs/TERMS.md#atomic-action)** = indivisible unit; exactly one Gate/Handoff.
- **[Compound action](docs/TERMS.md#compound-action)** = composed of atomic actions; every sub-gate must execute.
- **Nesting [rule](docs/TERMS.md#rule)** = every [Gate](docs/TERMS.md#gate) in a [compound action](docs/TERMS.md#compound-action) executes; no paper-only compounds.

Actions connect the pipeline (Plan → Produce → Fitness → Audit → Ship) to specific enforcement points. [Charter](docs/TERMS.md#charter) R30: every prescribed step or [action](docs/TERMS.md#action) has a hard [gate](docs/TERMS.md#gate).

## [Quality](docs/TERMS.md#quality) metric (ops vs defects)

- **[Quality](docs/TERMS.md#quality)** = `Ops / Opportunities` — rate of defect-free operations across agent processes
- **[Opportunity](docs/TERMS.md#opportunity)** = gate/verb execution with binary outcome (PASS/FAIL, MET/FAIL, ready/refused)
- **[Op](docs/TERMS.md#op)** = [opportunity](docs/TERMS.md#opportunity) completed as specified (PASS, MET, ready)
- **[Defect](docs/TERMS.md#defect)** = deviation from spec (FAIL, handoff_refused, error, not met)

DPMO-class without the academic theater. Binary classification only — no partial, weighted, or continuous scores. See [`integrity/QUALITY_METRIC.md`](integrity/QUALITY_METRIC.md) for formula, measurement surface, [refuse](docs/TERMS.md#refuse) rules (Q1--Q5).

**[Refuse](docs/TERMS.md#refuse) rules:** Fitness refuses [MET](docs/TERMS.md#met) without [quality evidence](docs/TERMS.md#quality-evidence) (Q1). Adversarial [audit](docs/TERMS.md#audit) refuses PASS without [quality snapshot](docs/TERMS.md#quality-snapshot) traceable to SSOT (Q2). [Boundary](docs/TERMS.md#boundary) exit refuses without [quality snapshot](docs/TERMS.md#quality-snapshot) recorded (Q3).

## Adoption bar

[Charter](docs/TERMS.md#charter) §14: [charter](docs/TERMS.md#charter) present, real [noun](docs/TERMS.md#noun) + [goal](docs/TERMS.md#goal), [gate](docs/TERMS.md#gate) 1 fails a deliberate violation in CI, agent loop written for class A/B, [confirmer](docs/TERMS.md#confirmer) produces evidence. Plus §5.8: [binding matrix](docs/TERMS.md#binding-matrix) audits green (no unbound in-force requirements).

## [Binding matrix](docs/TERMS.md#binding-matrix) status

**Current ratio: 40/78 bound (51.3%)**

Bound requirements have fail-capable gates under `tools/`. The 38 unbound reference requirements fall into two categories:

### Requirements needing future gates

These can gain automated gates with additional tooling work:

- **C5, R6**: Verb-path analysis (every state change through public verb) — needs call-graph tooling
- **R9, R10, C7, C8**: [Contract](docs/TERMS.md#contract) presence checks — needs schema validation tooling
- **R11, C9**: Field meaning uniqueness — needs semantic schema comparison
- **C19**: Duplicated [adjective](docs/TERMS.md#adjective) detection — needs AST-based predicate matching
- **R20**: Charter/ADR/code agreement — needs drift detection tooling

### Requirements staying reference (judgment required)

These require human review or are inherently design-time decisions:

- **R1-R4**: Ownership placement rules — requires understanding intent
- **R13, R15, R16, C11, C13**: Goal/noun design decisions — judgment calls
- **R17, R18, C14, C15**: [Workflow](docs/TERMS.md#workflow) composition rules — design review
- **C1-C3**: Change classification and home — proposal-time decisions
- **C16-C18, R25**: Test coverage and scope — review-time checks
- **C21-C24**: Proposal [integrity](docs/TERMS.md#integrity) — adversarial review items
- **P2**: [Zero variance](docs/TERMS.md#zero-variance) scope — meta-principle about the system itself

Run `python3 tools/audit-binding-matrix.py` to [verify](docs/TERMS.md#verify) matrix [integrity](docs/TERMS.md#integrity). All in-force requirements must be bound; reference requirements may remain unbound without failing the [audit](docs/TERMS.md#audit).

## Conventions in this workspace

- Prefer promise chaining over `await`; `.catch()` instead of try/catch around chains; `async` on Promise-returning functions; JSDoc on methods (when JS/TS lands).
- Portable agent SSOT: `.agents/` + `AGENTS.md`, not `.cursor/skills` as sole copy.
