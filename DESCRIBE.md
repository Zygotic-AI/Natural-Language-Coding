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
| `integrity/BOUNDARY.md` | Boundary + Handoff noun SSOT; role-bound SOP |
| `integrity/ACTIONS.md` | Action noun SSOT; gated action catalog; nesting rule |
| `integrity/binding-matrix.json` | Requirement → audit → binder (unbound fails) |
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

## Adoption bar

Charter §14: charter present, real noun + goal, fitness check 1 fails a deliberate violation in CI, agent loop written for class A/B, confirmer produces evidence. Plus §5.8: binding matrix audits green (no unbound in-force requirements).

## Conventions in this workspace

- Prefer promise chaining over `await`; `.catch()` instead of try/catch around chains; `async` on Promise-returning functions; JSDoc on methods (when JS/TS lands).
- Portable agent SSOT: `.agents/` + `AGENTS.md`, not `.cursor/skills` as sole copy.
