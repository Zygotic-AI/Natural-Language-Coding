# [ADR](../docs/TERMS.md#adr) 0003 — Systems extension: [agent nouns](../docs/TERMS.md#agent-noun) and contracted verbs

- Status: Accepted
- Date: 2026-09-05
- Deciders: Richard Pickett
- Class: F (charter extension)

## Context

[BBP](../docs/TERMS.md#bbp) originated as a software practice: nouns own state and adjectives, verbs are the only legal mutation, goals orchestrate I/O, workflows compose goals. This model shrinks the search space for agents editing code.

The same structural discipline applies to organizing agent fleets and durable roles in a system. Without boundaries, agent responsibilities blur. Handoffs become implicit. Completion is vibes. [Audit](../docs/TERMS.md#audit) trails scatter.

Decision KD-005 (Koan): Start with [BBP](../docs/TERMS.md#bbp) as systems model. Nouns = durable agents/roles; verbs = legal functions; goals/workflows = use-cases; [boundary](../docs/TERMS.md#boundary) artifacts = [handoff](../docs/TERMS.md#handoff), completion definition, auditable success (ops vs defects).

[Quality](../docs/TERMS.md#quality) north star: highest [quality](../docs/TERMS.md#quality); effectiveness before efficiency; [default-closed](../docs/TERMS.md#default-closed) (deny until evidence); DFSS; measure ops vs defects.

## Decision

### 1. Vocabulary mapping

| Software [BBP](../docs/TERMS.md#bbp) | Systems [BBP](../docs/TERMS.md#bbp) |
|--------------|-------------|
| [Noun](../docs/TERMS.md#noun) | [Agent noun](../docs/TERMS.md#agent-noun) (durable role with identity and adjectives) |
| [Verb (on noun)](../docs/TERMS.md#verb-on-noun) | Verb (legal function an agent may perform; contracted I/O) |
| [Goal](../docs/TERMS.md#goal) | Use-case (orchestration across agent nouns or to the outside world) |
| [Workflow](../docs/TERMS.md#workflow) | [Workflow](../docs/TERMS.md#workflow) (durable composition of use-cases) |
| [Contract](../docs/TERMS.md#contract) | [Boundary artifact](../docs/TERMS.md#boundary-artifact) (input, output, failure mode, handoff, completion) |
| [Adjective](../docs/TERMS.md#adjective) | Role [adjective](../docs/TERMS.md#adjective) (what the agent must never violate) |
| [Gate](../docs/TERMS.md#gate) | [Gate](../docs/TERMS.md#gate) (automated enforcement; binary pass/fail; CI-bound) |
| Adversarial review | [Audit](../docs/TERMS.md#audit) (role-based review against charter; produces findings) |

### 2. [Agent noun](../docs/TERMS.md#agent-noun) structure

Every [agent noun](../docs/TERMS.md#agent-noun) package declares:

- **Identity:** Role name, purpose (one line)
- **Adjectives:** What the agent must never violate
- **Verb list:** Each verb has input [contract](../docs/TERMS.md#contract), output [contract](../docs/TERMS.md#contract), failure mode
- **Handoff-in:** What must be true before this agent receives work
- **Completion artifact:** What the agent produces to mark work complete
- **Success criteria:** Ops vs defects; binary auditable outcomes

### 3. Produce ≠ [Audit](../docs/TERMS.md#audit) (charter §7 extension)

An agent that produces an artifact may not be the final auditor of that artifact. The agent that ships (ratifies, merges, releases) may not be the agent that grades itself. Separate produce, [audit](../docs/TERMS.md#audit), and [ship](../docs/TERMS.md#ship).

### 4. No shipping authority for [audit](../docs/TERMS.md#audit) roles

[Agent nouns](../docs/TERMS.md#agent-noun) whose purpose is adversarial review, [audit](../docs/TERMS.md#audit), or standards enforcement do **not** have shipping authority (no `ratify`, `merge`, `release` verbs). They produce findings. Another role (or human) decides whether findings block the [ship](../docs/TERMS.md#ship).

### 5. [Charter](../docs/TERMS.md#charter) section

A new [charter](../docs/TERMS.md#charter) section (§16 or similar) documents the systems model without altering the software rules in §§4–5.

## Consequences

- [Charter](../docs/TERMS.md#charter) gains a "Systems / [agent nouns](../docs/TERMS.md#agent-noun)" section with vocabulary mapping and produce≠[audit](../docs/TERMS.md#audit)≠[ship](../docs/TERMS.md#ship) constraint.
- `agents/` gains structured [agent noun](../docs/TERMS.md#agent-noun) packages (not just role prompts) with declared boundaries.
- Existing software [BBP](../docs/TERMS.md#bbp) rules unchanged in meaning; systems layer is additive.
- Three [agent nouns](../docs/TERMS.md#agent-noun) implement [Produce ≠ Audit ≠ Ship](../docs/TERMS.md#produce-audit-ship): standards-steward (produce standards), adversarial-auditor (audit), ship-role (authorize release).

## Rejected

- Branding the systems model as "governance" (charter §3 naming).
- Conflating [agent nouns](../docs/TERMS.md#agent-noun) with existing role packs (proposer/reviewer/confirmer/recorder are loop roles; agent nouns are durable organizational positions).
- Granting [audit](../docs/TERMS.md#audit) roles any [ship](../docs/TERMS.md#ship) authority.

## Related

- [Charter](../docs/TERMS.md#charter) §§3–7 (naming, core model, rules, agent loop, agent roles)
- [`integrity/PRINCIPLES.md`](../integrity/PRINCIPLES.md) — produce≠[audit](../docs/TERMS.md#audit) aligns with P2/P3 (zero variance, hard gates)
- KD-005 (Koan decision: BBP as systems model)
