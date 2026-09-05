# ADR 0003 — Systems extension: agent nouns and contracted verbs

- Status: Accepted
- Date: 2026-09-05
- Deciders: Richard Pickett
- Class: F (charter extension)

## Context

BBP originated as a software practice: nouns own state and invariants, verbs are the only legal mutation, goals orchestrate I/O, workflows compose goals. This model shrinks the search space for agents editing code.

The same structural discipline applies to organizing agent fleets and durable roles in a system. Without boundaries, agent responsibilities blur. Handoffs become implicit. Completion is vibes. Audit trails scatter.

Decision KD-005 (Koan): Start with BBP as systems model. Nouns = durable agents/roles; verbs = legal functions; goals/workflows = use-cases; boundary artifacts = handoff, completion definition, auditable success (ops vs defects).

Quality north star: highest quality; effectiveness before efficiency; default-closed (deny until evidence); DFSS; measure ops vs defects.

## Decision

### 1. Vocabulary mapping

| Software BBP | Systems BBP |
|--------------|-------------|
| Noun | Agent noun (durable role with identity and invariants) |
| Verb (on noun) | Verb (legal function an agent may perform; contracted I/O) |
| Goal | Use-case (orchestration across agent nouns or to the outside world) |
| Workflow | Workflow (durable composition of use-cases) |
| Contract | Boundary artifact (input, output, failure mode, handoff, completion) |
| Invariant | Role invariant (what the agent must never violate) |
| Fitness check | Audit (binary ops vs defects, success vs failure) |

### 2. Agent noun structure

Every agent noun package declares:

- **Identity:** Role name, purpose (one line)
- **Invariants:** What the agent must never violate
- **Verb list:** Each verb has input contract, output contract, failure mode
- **Handoff-in:** What must be true before this agent receives work
- **Completion artifact:** What the agent produces to mark work complete
- **Success criteria:** Ops vs defects; binary auditable outcomes

### 3. Produce ≠ Audit (charter §7 extension)

An agent that produces an artifact may not be the final auditor of that artifact. The agent that ships (ratifies, merges, releases) may not be the agent that grades itself. Separate produce, audit, and ship.

### 4. No shipping authority for audit roles

Agent nouns whose purpose is adversarial review, audit, or standards enforcement do **not** have shipping authority (no `ratify`, `merge`, `release` verbs). They produce findings. Another role (or human) decides whether findings block the ship.

### 5. Charter section

A new charter section (§16 or similar) documents the systems model without altering the software rules in §§4–5.

## Consequences

- Charter gains a "Systems / agent nouns" section with vocabulary mapping and produce≠audit constraint.
- `agents/` gains structured agent noun packages (not just role prompts) with declared boundaries.
- Existing software BBP rules unchanged in meaning; systems layer is additive.
- First two agent nouns: standards-steward and adversarial-auditor.

## Rejected

- Branding the systems model as "governance" (charter §3 naming).
- Conflating agent nouns with existing role packs (proposer/reviewer/confirmer/recorder are loop roles; agent nouns are durable organizational positions).
- Granting audit roles any ship authority.

## Related

- Charter §§3–7 (naming, core model, rules, agent loop, agent roles)
- [`integrity/PRINCIPLES.md`](../integrity/PRINCIPLES.md) — produce≠audit aligns with P2/P3 (zero variance, hard gates)
- KD-005 (Koan decision: BBP as systems model)
