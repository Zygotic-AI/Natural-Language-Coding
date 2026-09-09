# DESCRIBE.md — Boundary-Based Programming (central repo)

## What this repo is

Single source of truth for **Boundary-Based Programming** (BBP): theory → agentic application → tools. Tagline: stopping agents from shipping slop. Stand-alone branding: no foreign brand packages in integrity; copy and re/unbrand if a shape is useful.

## Core model (short)

- **Noun** — identity, private state, invariants; retrieval key for "how does X work?"
- **Verb (on noun)** — only legal mutation; contracted I/O
- **Goal** — use-case orchestration (I/O, other nouns, policy); calls verbs; never writes noun fields
- **Workflow** — durable composition of goals when one in-process call is not enough
- **Charter + ADRs** — decisions and confirmable rules; adversarial review against the charter
- **Integrity (zero variance)** — every requirement has a binary audit; every action has a hard gate; every boundary has hard I/O + failure mode; unbound / in-force-unbindable entries fail and are listed

### Systems model (§16)

Same structural discipline applied to organizing **agent fleets** — durable roles that operate a system over time. Ratified by ADR 0003.

- **Agent noun** — durable role with identity and invariants
- **Verb (on agent noun)** — legal function; contracted I/O with input, output, failure mode
- **Use-case** — orchestration across agent nouns or to the outside world
- **Boundary artifact** — handoff-in, completion artifact, success criteria (ops vs defects)
- **Produce ≠ Audit ≠ Ship** — separate who creates, who reviews, who authorizes release
- **Audit roles have no shipping authority** — they produce findings, not decisions

### Integrity note: BBA vs Bindings

**BBA** (Boundary-Based Architecture) is the roof doctrine — confirmable rules in this repo that define how boundaries, handoffs, and integrity work (`CHARTER.md`, `integrity/`). **Bindings** is the operating policy map consumed by agent processes — P-series policies (P-016…P-031 class) that wire refuse criteria and evidence requirements to executable gates. Bindings live in the companion repo (`richardpickett/BBA-Bindings`). See [`docs/OPERATING_BINDINGS.md`](docs/OPERATING_BINDINGS.md) for the policy index.

## Key paths

| Path | Role |
|------|------|
| `CHARTER.md` | Living, authoritative charter (§5.8 integrity, §16 systems model) |
| `theory/history/og-interview-draft.md` | OG interview draft (frozen) |
| `theory/` | Theory and history |
| `agents/` | Agent loops, roles, prompts, agent nouns |
| `agents/standards-steward/` | Agent noun: charter/ADR steward (no ship authority); query verbs for Session applicability |
| `agents/adversarial-auditor/` | Agent noun: adversarial review (no ship authority) |
| `agents/ship-role/` | Agent noun: authorize release (ship authority with mandate) |
| `tools/` | Fitness checks, scaffolding, matrix auditor |
| `examples/` | Adopter sample systems |
| `adrs/` | Decision records (`0001` = zero-variance, `0003` = systems extension) |
| `integrity/` | Principles, binding matrix, audit defs |
| `integrity/GATE.md` | Gate noun SSOT (G1--G4, incomplete-packet hunt) |
| `integrity/QUALITY_METRIC.md` | Quality metric SSOT (ops vs defects; Q1--Q5) |
| `integrity/BOUNDARY.md` | Boundary + Handoff noun SSOT; role-bound SOP |
| `integrity/BOUNDED_CONTEXT.md` | Bounded Context noun SSOT; living system-as-is knowledge (mechanisms, keys, invariants) |
| `integrity/CONTRIBUTION.md` | Shared docs standard + Contribution Gate (G1--G4 refuse) |
| `integrity/LEXICON.md` | Locked term definitions (Action, Content type, Type recipe, etc.) |
| `integrity/ACTIONS.md` | Action noun SSOT; gated action catalog; nesting rule |
| `integrity/binding-matrix.json` | Requirement → audit → binder (unbound fails) |
| `docs/OPERATING_BINDINGS.md` | Operating policy index (P-016…P-031 class); links to BBA-Bindings companion |
| `content-types/HOW-TO-ADD.md` | Type recipes for adding content (ADR, integrity doc, agent noun, etc.) |
| `TODO` | Task list (`☐` / `✔ @done(...)`) |
| `AGENTS.md` | Cross-harness standing instructions |
| `.agents/` | Portable skills / instructions |

## Naming to avoid

Do not brand the practice "governance" / "governed." Prefer charter, integrity, adversarial review. "Boundary-Enforced Programming" describes CI, not the practice title.

## Terminology clarification (gate ≠ audit)

- **Gate** = automated enforcement (fitness checks, CI rules); binary PASS/FAIL; blocks automatically; default-closed. See [`integrity/GATE.md`](integrity/GATE.md) for formal definition and all-required PASS fitness bar.
- **Audit** = role-based adversarial review (adversarial-auditor agent noun); produces findings for ship decision
- **Produce ≠ Audit ≠ Ship** = separate agent nouns for creating artifacts, reviewing them, and authorizing release

Gates and audits both yield binary outcomes (ops vs defects), but differ in mechanism and authority. Gates block the build; audits produce findings for a ship-role or human to decide.

**All-required PASS bar (G1--G4):** A gate is good only if incomplete work cannot PASS, every check is machine-checkable or refuse-wired, the last incomplete packet would FAIL it, and PASS does not require human redo. Design rule: write refuse + incomplete-packet fixture in the same tip. See [`integrity/GATE.md`](integrity/GATE.md).

## Terminology clarification (boundary ≠ handoff)

- **Boundary** = named stage in a work pipeline that owns laws, is default-closed, and produces binary advance. See [`integrity/BOUNDARY.md`](integrity/BOUNDARY.md).
- **Handoff** = refuse-wired gate between Boundaries; must meet G1--G4; `handoff_refused` ≠ fitness FAIL (produce-incomplete signal, not content defect).

Boundaries include: Plan, Conduct-RCA, Raise-Readiness, Produce, Fitness, Adversarial Audit, Ship, UAT/Promote, System-Remediate Design, Instance Heal. Role-bound SOP maps boundaries to roles (Plan Steward, Quality Architect, Adversarial Auditor, Ship Role, etc.) -- no person names in SOP tables.

**Incomplete-packet fixture:** 15855 without §7/R3/R4 must FAIL any raise-readiness handoff. Binder: [P-030](https://github.com/richardpickett/BBA-Bindings/pull/9) on BBA-Bindings main.

## Terminology clarification (action)

- **Action** = named, gated unit of work within a boundary; executes through a Gate or Handoff. See [`integrity/ACTIONS.md`](integrity/ACTIONS.md).
- **Atomic action** = indivisible unit; exactly one Gate/Handoff.
- **Compound action** = composed of atomic actions; every sub-gate must execute.
- **Nesting rule** = every Gate in a compound action executes; no paper-only compounds.

Actions connect the pipeline (Plan → Produce → Fitness → Audit → Ship) to specific enforcement points. Charter R30: every prescribed step or action has a hard gate.

## Quality metric (ops vs defects)

- **Quality** = `Ops / Opportunities` — rate of defect-free operations across agent processes
- **Opportunity** = gate/verb execution with binary outcome (PASS/FAIL, MET/FAIL, ready/refused)
- **Op** = opportunity completed as specified (PASS, MET, ready)
- **Defect** = deviation from spec (FAIL, handoff_refused, error, not met)

DPMO-class without the academic theater. Binary classification only — no partial, weighted, or continuous scores. See [`integrity/QUALITY_METRIC.md`](integrity/QUALITY_METRIC.md) for formula, measurement surface, refuse rules (Q1--Q5).

**Refuse rules:** Fitness refuses MET without quality evidence (Q1). Adversarial audit refuses PASS without quality snapshot traceable to SSOT (Q2). Boundary exit refuses without quality snapshot recorded (Q3).

## Adoption bar

Charter §14: charter present, real noun + goal, fitness check 1 fails a deliberate violation in CI, agent loop written for class A/B, confirmer produces evidence. Plus §5.8: binding matrix audits green (no unbound in-force requirements).

## Binding matrix status

**Current ratio: 40/78 bound (51.3%)**

Bound requirements have fail-capable binders under `tools/`. The 38 unbound reference requirements fall into two categories:

### Requirements needing future binders

These can gain automated binders with additional tooling work:

- **C5, R6**: Verb-path analysis (every state change through public verb) — needs call-graph tooling
- **R9, R10, C7, C8**: Contract presence checks — needs schema validation tooling
- **R11, C9**: Field meaning uniqueness — needs semantic schema comparison
- **C19**: Duplicated law detection — needs AST-based predicate matching
- **R20**: Charter/ADR/code agreement — needs drift detection tooling

### Requirements staying reference (judgment required)

These require human review or are inherently design-time decisions:

- **R1-R4**: Ownership placement rules — requires understanding intent
- **R13, R15, R16, C11, C13**: Goal/noun design decisions — judgment calls
- **R17, R18, C14, C15**: Workflow composition rules — design review
- **C1-C3**: Change classification and home — proposal-time decisions
- **C16-C18, R25**: Test coverage and scope — review-time checks
- **C21-C24**: Proposal integrity — adversarial review items
- **P2**: Zero variance scope — meta-principle about the system itself

Run `python3 tools/audit-binding-matrix.py` to verify matrix integrity. All in-force requirements must be bound; reference requirements may remain unbound without failing the audit.

## Conventions in this workspace

- Prefer promise chaining over `await`; `.catch()` instead of try/catch around chains; `async` on Promise-returning functions; JSDoc on methods (when JS/TS lands).
- Portable agent SSOT: `.agents/` + `AGENTS.md`, not `.cursor/skills` as sole copy.
