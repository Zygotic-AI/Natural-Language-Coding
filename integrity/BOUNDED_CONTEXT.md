# Bounded Context

SSOT for the Bounded Context [noun](../docs/TERMS.md#noun) in [Boundary-Based Architecture](../docs/TERMS.md#bba). A Bounded Context is living system-as-is knowledge inside a [Boundary](../docs/TERMS.md#boundary) — the retrieval key for "how does X work?"

Rationale: [charter](../docs/TERMS.md#charter) §4 (nouns own identity, private state, adjectives), §16 (systems model). Related: [`BOUNDARY.md`](BOUNDARY.md), [`GATE.md`](GATE.md).

---

## Definition

A **Bounded Context** is a documented body of living knowledge about the current state of a system (or subsystem) inside a [Boundary](../docs/TERMS.md#boundary). It answers the question: *how does this actually work right now?*

A Bounded Context contains:

1. **Mechanisms** — how the system accomplishes its purpose; the moving parts, data flows, and interactions
2. **Identity / Correlation Keys** — how entities are identified, how events correlate to entities, how work items trace through the system
3. **Adjectives** — what must always be true within this context; the adjectives that govern valid states and transitions

A Bounded Context is:

- **Living** — updated when the system changes; reflects as-is, not as-designed or as-decided
- **Queryable** — structured so agents and humans can retrieve specific knowledge ("what keys correlate an Invoice to its Payments?")
- **Boundary-scoped** — lives inside one [Boundary](../docs/TERMS.md#boundary); cross-boundary knowledge belongs to a higher-level context or an integration document

### Bounded Context ≠ Documentation

| Concept | Purpose | Updated when |
|---------|---------|--------------|
| **Bounded Context** | Answer "how does X work right now?" | System changes |
| Documentation | Explain usage, onboarding, reference | Docs need refresh |
| Code comments | Clarify non-obvious implementation | Code changes |

A Bounded Context is not prose documentation. It is structured knowledge with declared sections (mechanisms, identity keys, adjectives) that can be queried by role ("show me the adjectives") or by entity ("show me Invoice identity keys").

---

## Bounded Context ≠ [ADR](../docs/TERMS.md#adr)

A Bounded Context describes **what is**. An [ADR](../docs/TERMS.md#adr) records **what was decided**.

| Artifact | Tense | Content | Updates |
|----------|-------|---------|---------|
| **Bounded Context** | Present | Mechanisms, keys, adjectives — current as-is state | On every system change that affects the described knowledge |
| **[ADR](../docs/TERMS.md#adr)** | Past | Decision, context, consequences — why X was chosen over Y | Superseded by new [ADR](../docs/TERMS.md#adr) if decision reverses; original preserved |

**Example:** An [ADR](../docs/TERMS.md#adr) records "we chose eventual consistency for Invoice→Payment sync" and why. The Bounded Context documents *how* the sync mechanism works today, what keys correlate Invoice to Payment, and what adjectives the sync must preserve.

An agent changing the sync mechanism:
1. Reads the Bounded Context to understand current state
2. Reads the [ADR](../docs/TERMS.md#adr) to understand constraints and rejected alternatives
3. Updates the Bounded Context after the change lands
4. Writes a new [ADR](../docs/TERMS.md#adr) only if the *decision* changes (not just the implementation)

### ADRs are not obsoleted by Bounded Context

ADRs remain valuable: they explain *why* and record rejected alternatives. Bounded Contexts explain *how* and record current truth. Both are needed.

---

## Bounded Context ≠ DDD Evans "Bounded Context"

Domain-Driven Design (Evans, 2003) uses "Bounded Context" to mean a **semantic [boundary](../docs/TERMS.md#boundary)** around a domain model where terms have consistent meaning. The [BBA](../docs/TERMS.md#bba) use of the term is related but distinct.

| Aspect | DDD Evans | [BBA](../docs/TERMS.md#bba) |
|--------|-----------|-----|
| **Primary concern** | Ubiquitous language consistency | Living system-as-is knowledge |
| **What it bounds** | A domain model and its vocabulary | Mechanisms, identity keys, adjectives inside a [Boundary](../docs/TERMS.md#boundary) |
| **Purpose** | Prevent semantic drift across models | Enable retrieval of "how does X work?" |
| **Lives in** | Conceptual modeling; may span code and team boundaries | Inside a declared [BBA](../docs/TERMS.md#bba) [Boundary](../docs/TERMS.md#boundary) |
| **Relationship to [Boundary](../docs/TERMS.md#boundary)** | Not the same concept | Always inside a [Boundary](../docs/TERMS.md#boundary) |

**Why "Bounded Context" in [BBA](../docs/TERMS.md#bba)?** The term signals that the knowledge is *scoped* — it belongs to a specific [Boundary](../docs/TERMS.md#boundary) and does not claim authority outside it. A Bounded Context does not define the One True Model; it documents how *this* [Boundary](../docs/TERMS.md#boundary)'s system works right now.

[BBA](../docs/TERMS.md#bba) practitioners may also use DDD Bounded Contexts at the modeling layer. The two concepts coexist: a DDD Bounded Context defines semantic scope for a domain model; a [BBA](../docs/TERMS.md#bba) Bounded Context documents living as-is knowledge inside a [BBA](../docs/TERMS.md#bba) [Boundary](../docs/TERMS.md#boundary).

---

## Structure

A Bounded Context document declares:

| Section | Contents | Required? |
|---------|----------|-----------|
| **Identity** | Name of the context, the [Boundary](../docs/TERMS.md#boundary) it belongs to, one-line purpose | Yes |
| **Mechanisms** | How the system works: data flows, components, interactions, algorithms | Yes |
| **Identity Keys** | How entities are identified: primary keys, external references, correlation IDs | Yes |
| **Correlation Keys** | How work items / events trace through the system: trace IDs, request IDs, saga keys | When applicable |
| **Adjectives** | What must always be true: state constraints, transition rules, consistency guarantees | Yes |
| **Failure Modes** | How the system fails: error states, retry behavior, compensation paths | When applicable |
| **Dependencies** | Other Bounded Contexts or external systems this context depends on | When applicable |
| **Last verified** | Date the as-is content was confirmed accurate against the running system | Yes |

### Mechanisms section

Mechanisms answer: *what are the moving parts and how do they interact?*

Good mechanism documentation:
- Names components and their roles
- Describes data flow direction
- States synchrony (sync vs async, push vs pull)
- Notes timing characteristics when relevant (polling interval, event delay bounds)

Mechanisms do not explain *why* the design was chosen (that belongs in an ADR) or *how to use* the system (that belongs in usage docs).

### Identity / Correlation Keys section

Identity keys answer: *how do I find or reference this entity?*

- Primary identifiers (UUID, auto-increment, natural key)
- External references (foreign keys, external system IDs)
- Human-readable identifiers (invoice number, order reference)

Correlation keys answer: *how do I trace work through the system?*

- Request/trace IDs that span multiple components
- Saga/workflow IDs that span time
- Event correlation IDs that link cause to effect

### Adjectives section

Adjectives answer: *what must always be true?*

Adjectives are expressed as predicates:
- "Invoice.status cannot transition from PAID to DRAFT"
- "Payment.amount + Payment.refunds ≤ Payment.authorized"
- "Every OrderLine references exactly one Product that exists"

Adjectives are not aspirational. They describe what the system currently enforces. If an [adjective](../docs/TERMS.md#adjective) is not enforced, it is not an [adjective](../docs/TERMS.md#adjective) — it is a wish.

---

## Querying a Bounded Context

Agents and humans query Bounded Contexts to understand the system. Common queries:

| Query | Section to read |
|------------------------|
| "How does Invoice payment sync work?" | Mechanisms |
| "What identifies a Customer across systems?" | Identity Keys |
| "How do I trace a request through the pipeline?" | Correlation Keys |
| "What transitions are legal for Order status?" | Adjectives |
| "What happens if the payment gateway times out?" | Failure Modes |

A well-structured Bounded Context enables targeted retrieval. An agent does not need to read the entire context to answer a specific question.

---

## Maintaining a Bounded Context

A Bounded Context is **living** — it must reflect the current system.

### Update triggers

| Event | [Action](../docs/TERMS.md#action) |
|-------|--------|
| Mechanism changes (new component, altered flow) | Update Mechanisms section |
| New or changed identifier | Update Identity/Correlation Keys |
| [Adjective](../docs/TERMS.md#adjective) added, removed, or relaxed | Update Adjectives section |
| System change lands | [Verify](../docs/TERMS.md#verify) and update "Last verified" date |

### Staleness is a [defect](../docs/TERMS.md#defect)

A Bounded Context that does not match the running system is incorrect. Staleness is not "technical debt to address later" — it is a [defect](../docs/TERMS.md#defect) that degrades the retrieval key.

**Remediation:** When a system change lands without updating the Bounded Context, the change is incomplete. The [produce package](../docs/TERMS.md#produce-package) for a system change should include Bounded Context updates when the change affects mechanisms, keys, or adjectives.

---

## Confirmation Checklist (Bounded Context-specific)

For changes that add or modify Bounded Contexts:

- [ ] CBC1. Bounded Context declares identity (name, Boundary, purpose).
- [ ] CBC2. Mechanisms section documents how the system works (components, flows, interactions).
- [ ] CBC3. Identity Keys section documents entity identifiers.
- [ ] CBC4. Correlation Keys section documents trace/saga/event keys (or states N/A with reason).
- [ ] CBC5. Adjectives section documents enforced constraints (predicates, not aspirations).
- [ ] CBC6. Failure Modes section documents error handling (or states N/A with reason).
- [ ] CBC7. Dependencies section lists dependent contexts/systems (or states N/A).
- [ ] CBC8. "Last verified" date is present and accurate.
- [ ] CBC9. Content reflects as-is state, not as-designed or as-decided.
- [ ] CBC10. No ADR-style decision rationale in the Bounded Context (decisions belong in ADRs).
- [ ] CBC11. No usage documentation in the Bounded Context (usage belongs in docs).

---

## Cross-references

- [Charter](../docs/TERMS.md#charter) §4: Core model — nouns own identity, private state, adjectives
- [Charter](../docs/TERMS.md#charter) §4.1: [Noun](../docs/TERMS.md#noun) structure — the retrieval key for "how does X work?"
- [Charter](../docs/TERMS.md#charter) §16: Systems model — [agent nouns](../docs/TERMS.md#agent-noun), [boundary](../docs/TERMS.md#boundary) artifacts
- [`BOUNDARY.md`](BOUNDARY.md): [Boundary](../docs/TERMS.md#boundary) [noun](../docs/TERMS.md#noun) — stages that own adjectives
- [`GATE.md`](GATE.md): [Gate](../docs/TERMS.md#gate) [noun](../docs/TERMS.md#noun) — binary enforcement checkpoints
- [`PRINCIPLES.md`](PRINCIPLES.md): P4 — hard [boundary](../docs/TERMS.md#boundary) I/O declarations
- [`../DESCRIBE.md`](../DESCRIBE.md): Project memory file — durable facts for agents
- [`../adrs/`](../adrs/): Decision records — why X was chosen over Y
