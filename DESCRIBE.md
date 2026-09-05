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
| `integrity/binding-matrix.json` | Requirement → audit → binder (unbound fails) |
| `TODO` | Task list (`☐` / `✔ @done(...)`) |
| `AGENTS.md` | Cross-harness standing instructions |
| `.agents/` | Portable skills / instructions |

## Naming to avoid

Do not brand the practice "governance" / "governed." Prefer charter, integrity, adversarial review. "Boundary-Enforced Programming" describes CI, not the practice title.

## Terminology clarification (gate ≠ audit)

- **Gate** = automated enforcement (fitness checks, CI rules); binary pass/fail; blocks automatically
- **Audit** = role-based adversarial review (adversarial-auditor agent noun); produces findings for ship decision
- **Produce ≠ Audit ≠ Ship** = separate agent nouns for creating artifacts, reviewing them, and authorizing release

Gates and audits both yield binary outcomes (ops vs defects), but differ in mechanism and authority. Gates block the build; audits produce findings for a ship-role or human to decide.

## Adoption bar

Charter §14: charter present, real noun + goal, fitness check 1 fails a deliberate violation in CI, agent loop written for class A/B, confirmer produces evidence. Plus §5.8: binding matrix audits green (no unbound in-force requirements).

## Conventions in this workspace

- Prefer promise chaining over `await`; `.catch()` instead of try/catch around chains; `async` on Promise-returning functions; JSDoc on methods (when JS/TS lands).
- Portable agent SSOT: `.agents/` + `AGENTS.md`, not `.cursor/skills` as sole copy.
