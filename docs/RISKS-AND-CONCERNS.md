# Risks and Concerns

This document qualifies the architecture upfront: the problems it solves, the problems it introduces, and the mitigating steps for each. Read it before adopting. It is not a second [charter](TERMS.md#charter) — the [BBA](TERMS.md#bba) standard in `CHARTER.md` remains the design SSOT. This is the honest ledger of trade-offs.

---

## Part 1 — Problems this architecture solves

### 1.1 Locally green, globally wrong

**Problem.** Agents [ship](TERMS.md#ship) code that passes every local test and still forks a business [rule](TERMS.md#rule) across two goals. Two goals each invent `status`. Both look correct. The user finds the bug at $100,000.

**Solved by.** Nouns own adjectives (the descriptors that must stay true). Verbs are the only mutation path. Goals call verbs; they never write [noun](TERMS.md#noun) fields or re-decide an [adjective](TERMS.md#adjective). A [gate](TERMS.md#gate) fails any goal-side write.

### 1.2 Anemic domain model

**Problem.** Thin nouns with verbs scattered across goals are procedural code wearing a class costume. The logic lives wherever the last developer put it. Nobody can find it. Nobody can [audit](TERMS.md#audit) it.

**Solved by.** Fat nouns. Every verb that reads or writes a [noun](TERMS.md#noun)'s adjectives lives on that [noun](TERMS.md#noun). The [noun](TERMS.md#noun) is the single place that knows how to charge a card, mask a PAN, or void an invoice.

### 1.3 Software decay under fast technology change

**Problem.** New technology arrives faster every year. Each swap is a rewrite because the concern is scattered across the codebase. Decay rate accelerates.

**Solved by.** Swappable concerns are adjectives on nouns. Changing "log to a file" into "log to Logstash" is one [requirement](TERMS.md#requirement) change. The AI figures out the delta and rebuilds only the affected [noun](TERMS.md#noun). Same codebase, new technology.

### 1.4 Sensitive data leakage (PII, PCI)

**Problem.** A card number or a person's name gets passed around as a bare value through DTOs and intermediate objects. It leaks into logs, caches, and places that should never see it.

**Solved by.** An [adjective](TERMS.md#adjective)'s value never traverses more than one [boundary](TERMS.md#boundary) as data. It is consumed inside the [boundary](TERMS.md#boundary) that calls the verb. No intermediate [noun](TERMS.md#noun) ever holds the raw value.

### 1.5 Context-window explosion

**Problem.** An agent editing a large codebase needs the whole repo in context. Cost and error rate scale with size.

**Solved by.** Discrete atomic boundaries. The agent works on one [boundary](TERMS.md#boundary) at a time, plus the published contracts of the nouns it calls. The repo can be huge; the window never is.

### 1.6 [Defect](TERMS.md#defect) cost compounds down the value stream

**Problem.** A [defect](TERMS.md#defect) found in design costs $1. In code, $10. In QA, $1,000. In UAT, $10,000. In production, $100,000. The further down the stream, the more expensive.

**Solved by.** [PLANIT](TERMS.md#planit) spends the extra minutes up front — [interview](TERMS.md#interview), bind, [audit](TERMS.md#audit) — because the codebase lives five to ten years. The two-minute [audit](TERMS.md#audit) is cheap against a decade of operation.

### 1.7 [Interview](TERMS.md#interview) [quality](TERMS.md#quality) (resolved as design; empirical in practice)

**Problem.** Everything downstream compounds from the [interview](TERMS.md#interview). A weak [interview](TERMS.md#interview) produces excellent-looking goals that still fork an [adjective](TERMS.md#adjective), and [RCA](TERMS.md#rca) only catches it after the fact. The $1-to-$100k curve only holds if the [interview](TERMS.md#interview) is genuinely good, and genuinely good is the hardest thing to automate.

**Solved by (design).** The [interview](TERMS.md#interview) does not need to be perfect on day one — it needs to be **auditable**. Every question asked, every gap closed, every [ADR](TERMS.md#adr) or [requirement](TERMS.md#requirement) produced gets recorded. When a fork surfaces months later, the [interview](TERMS.md#interview) can be replayed to find exactly which question was missed. That miss becomes a new entry in the pattern catalog. Over time the log compounds into what a good [interview](TERMS.md#interview) actually asks — "good" becomes measurable, not assumed.

**Status.** Resolved as an architectural problem. What remains is operational: running interviews, finding the misses, tightening the catalog. That is empirical work, not a flaw in the framework.

### 1.8 [Contract](TERMS.md#contract) churn (resolved)

**Problem.** When a verb's meaning changes, every caller has to accept it. In a real codebase with dozens of goals, a changed `applyPayment` is a migration event, not a footnote. The binder can flag the break; it cannot decide whether the callers are ready.

**Solved by.** Two stacked moves.

*[Audit](TERMS.md#audit) readiness.* The binder already knows every caller of a verb — that is the [binding](TERMS.md#binding) graph. When the [contract](TERMS.md#contract) changes, it diffs each call site against the new signature and emits a blast-radius report: here is who breaks. That is detection, not a judgment call. The human decides when callers are ready; the binder tells them who is affected.

*Versioned verbs.* [Ship](TERMS.md#ship) `applyPaymentV2` alongside `applyPayment`. Old callers keep working. New code binds to V2. When the last caller migrates, V1 is deprecated, then removed. No forced migration, no big-bang rewrite.

**The hard [rule](TERMS.md#rule) that makes versioning safe.** Adjectives belong to the [noun](TERMS.md#noun), never to the verb. A verb can only honor an [adjective](TERMS.md#adjective) or break it — it can never redefine it. So V2 cannot fork an [adjective](TERMS.md#adjective) at all. It either respects every [adjective](TERMS.md#adjective) on the [noun](TERMS.md#noun) or it is invalid on arrival. Versioning is therefore a pure API-shape question: same adjectives, different parameters or return shape. That is a much smaller migration surface than a [rule](TERMS.md#rule) change. If a verb change *did* need a different [adjective](TERMS.md#adjective), that is not a versioning problem — it is a [noun](TERMS.md#noun) redesign, and it goes through the normal [PLANIT](TERMS.md#planit) cycle with a new [adjective](TERMS.md#adjective) on the [noun](TERMS.md#noun).

**Status.** Resolved. The binder does the detection; versioning does the safety; the adjective-ownership [rule](TERMS.md#rule) keeps the two from colliding.

---

## Part 2 — Problems this architecture introduces

### 2.1 God [noun](TERMS.md#noun)

**Problem.** Once fat is rewarded, every new behavior wants to live on the nearest [noun](TERMS.md#noun). `Invoice` ends up owning tax calculation, email, PDF rendering, and fraud scoring. One class that knows everything — the anemic model in reverse.

**Mitigation.** A [noun](TERMS.md#noun) may only own an [adjective](TERMS.md#adjective) or verb that is about that [noun](TERMS.md#noun)'s own state. Tax calculation belongs on a `Tax` [noun](TERMS.md#noun), not `Invoice`. `Invoice` calls `Tax.calculate` — one hop, allowed. The test: does this behavior read or write this [noun](TERMS.md#noun)'s adjectives? If no, it does not belong here.

### 2.2 Leaky verbs

**Problem.** A verb returns a raw sensitive value instead of doing the work — `getCardNumber()` instead of `charge()`. That is the escape hatch the binder is supposed to catch.

**Mitigation.** The [audit](TERMS.md#audit) treats *returning* a sensitive [adjective](TERMS.md#adjective) the same as *assigning* one. A verb that returns PCI data to a caller that is not the declared consumer fails. The [audit](TERMS.md#audit) checks return values, not just field writes.

### 2.3 [Boundary](TERMS.md#boundary) thrash / chatty call chains

**Problem.** If every interaction is one hop and nouns cannot carry data, you get chatty chains — `Order` calls `Payment`, `Payment` calls `Card`, `Card` calls `Bank`. Fine for auditability, expensive at runtime.

**Mitigation.** Batching verbs: `chargeAndSettle()` instead of `charge()` then `settle()`. The cost is fat verbs, which is the same gravity as the god [noun](TERMS.md#noun), just at the verb level. Keep batches intentional and declared, not accidental.

### 2.4 Capability explosion (rejected path)

**Problem.** Solving data residency with opaque handles instead of the [binding](TERMS.md#binding) [rule](TERMS.md#rule) drowns the system in handle types — one handle per sensitive [adjective](TERMS.md#adjective) per [noun](TERMS.md#noun).

**Mitigation.** Do not use handles. Use binding-at-plan-time: the plan declares the call site as the consumer; the [audit](TERMS.md#audit) verifies the value is consumed in place. No second object type.

### 2.5 [Adjective](TERMS.md#adjective) value outlives the consuming verb (supersedes 2.5)

**Problem.** Even with a correct [binding](TERMS.md#binding), the fetched value can be stored in another piece of data or returned from the verb that used it. The leak is not about intent — it is about lifetime. `charge(card.getNumber())` is fine; `let n = card.getNumber(); stash(n)` is not.

**Mitigation.** The adversarial [audit](TERMS.md#audit) tracks the [adjective](TERMS.md#adjective)'s **taint lifetime**, not the plan's declared consumer. [Rule](TERMS.md#rule): a sensitive [adjective](TERMS.md#adjective) fetched inside a verb may not be assigned to a field, passed as an argument to another [boundary](TERMS.md#boundary), or returned from that verb. It must be consumed inside the same verb and dropped. The [audit](TERMS.md#audit) is mechanical taint tracking — no trust in the [binding](TERMS.md#binding) declaration. This removes the silent-hole risk entirely: the binder does not need to know whether the site is a consumer; it only needs to know the value never escapes.

### 2.6 Per-step [audit](TERMS.md#audit) cost

**Problem.** If each atomic step spawns a heavy review, [PLANIT](TERMS.md#planit) becomes slower than writing code directly. The cycle eats its own value.

**Mitigation.** Keep per-step audits mechanical: does this code touch only what it was bound to, and does no sensitive [adjective](TERMS.md#adjective) outlive its verb? Save deep adversarial review for work-package completion. Two tiers — cheap [gate](TERMS.md#gate) per step, thorough review per package.

### 2.7 Regeneration only stays cheap if adjectives actually moved

**Problem.** If "log to a file" was a [goal](TERMS.md#goal)'s private habit instead of an [adjective](TERMS.md#adjective) on a `Logging` [noun](TERMS.md#noun), changing the [requirement](TERMS.md#requirement) regenerates nothing. You still have scattered file writes to find.

**Mitigation.** Every swappable concern must be an [adjective](TERMS.md#adjective) the binder can see. The manifesto's "same codebase, new tech" promise holds only when this is true. [Audit](TERMS.md#audit) the adjectives, not just the nouns.

### 2.8 Sensitive data relocated, not closed

**Problem.** "Invoice calls Customer directly" still moves the name across a [boundary](TERMS.md#boundary). The PDF generator now holds PII in its own memory. The leak is relocated, not closed.

**Mitigation.** The [adjective](TERMS.md#adjective)'s value never becomes data that crosses a [boundary](TERMS.md#boundary). It is consumed inside the calling statement. No intermediate [noun](TERMS.md#noun) holds the raw value. Combined with 2.5, the [audit](TERMS.md#audit) enforces this mechanically.

### 2.9 Non-OO escape hatches (residual risk of the existential flaw)

**Problem.** Private fields and methods make adjectives unreachable from outside in OO languages. But the language's protection dies the moment a [goal](TERMS.md#goal) reaches the [noun](TERMS.md#noun) through serialization, a raw SQL update, or an ORM that bypasses the object entirely. The [noun](TERMS.md#noun)'s [adjective](TERMS.md#adjective) is never consulted, so nothing fails, but the [rule](TERMS.md#rule) now lives in two places. This is the residual of the original binder gap — narrowed, not eliminated.

**Mitigation.** A7 on the [audit](TERMS.md#audit) checklist: scan for direct storage access — raw SQL, ORM bypasses, deserialization into [noun](TERMS.md#noun) state, reflection — that mutates or reads a [noun](TERMS.md#noun)'s adjectives without going through a published verb. This is a narrow, known hole with a specific check, not an open one. The OO privacy handles the common case; A7 handles the paths the language cannot see.

### 2.10 Versioned verbs that silently drop an [adjective](TERMS.md#adjective) (closed by 1.8)

**Problem.** A new verb version could quietly carry a weaker set of adjectives than the one it replaces — `applyPaymentV2` honors balance-never-negative but drops void-after-pay. Callers migrate to V2 and the [adjective](TERMS.md#adjective) is forked under a new name. This is the original existential flaw wearing a costume.

**Mitigation.** Closed by the [rule](TERMS.md#rule) in 1.8: adjectives belong to the [noun](TERMS.md#noun), and a verb can only honor or break them, never redefine them. V2 is validated against the [noun](TERMS.md#noun)'s full [adjective](TERMS.md#adjective) set at creation (A1/A2). If it drops one, it fails before any caller touches it. Versioning is safe precisely because the [adjective](TERMS.md#adjective) surface is noun-owned and checked independently of the verb's API shape.

---

## Part 3 — Adversarial [audit](TERMS.md#audit) checklist

Every artifact creation or change runs an adversarial [audit](TERMS.md#audit). The [audit](TERMS.md#audit) family grows with the artifact type. None of these trust the generator.

| # | When | What it checks |
|---|------|----------------|
| A1 | [Noun](TERMS.md#noun) created | The new [noun](TERMS.md#noun) reaches no other [boundary](TERMS.md#boundary) except through that [boundary](TERMS.md#boundary)'s published verbs. Both directions: it does not read another [noun](TERMS.md#noun)'s state, and it does not call into a [goal](TERMS.md#goal). |
| A2 | Verb / [adjective](TERMS.md#adjective) added or changed | Every caller of a changed [contract](TERMS.md#contract) still satisfies it, or callers were updated in the same change. For a *new verb version*, [verify](TERMS.md#verify) it honors the [noun](TERMS.md#noun)'s **full** [adjective](TERMS.md#adjective) set — no silent drop. |
| A3 | [Goal](TERMS.md#goal) completed | The code actually delivers the stated outcome — not just compiles, not just passes local tests. |
| A4 | [Requirement](TERMS.md#requirement) bound | The bound code path enforces the [requirement](TERMS.md#requirement), not merely references it. |
| A5 | Any sensitive [adjective](TERMS.md#adjective) fetched | **Taint lifetime:** the value is not assigned to a field, passed to another [boundary](TERMS.md#boundary), or returned from the consuming verb. Consumed in place or dropped. (Replaces any "declared consumer" check.) |
| A6 | Work package completed | Deep review: statements done, all bound ADRs/requirements held, no second copy of an [adjective](TERMS.md#adjective) inside a [goal](TERMS.md#goal), no [god-noun](TERMS.md#god-noun) growth. |
| A7 | Any [noun](TERMS.md#noun) mutation or read | **Non-OO escape hatches:** no raw SQL, ORM bypass, deserialization, or reflection mutates or reads a [noun](TERMS.md#noun)'s adjectives without going through a published verb. Catches the residual of the existential flaw — the paths OO privacy cannot see. |

**[Rule](TERMS.md#rule):** A5 is mechanical and cheap — it runs at every per-step [gate](TERMS.md#gate). A6 is the thorough pass at package completion. A7 runs wherever a [noun](TERMS.md#noun)'s storage is touched. Do not merge A5 into A6; the cheap taint check is what keeps [PLANIT](TERMS.md#planit) fast. Do not skip A7 because "we use OO" — the escape hatches are exactly where the existential flaw survives.

---

## Part 4 — Architectural decisions captured

These are the standing decisions from the existential-flaw discussion. They are not risks; they are rules the architecture depends on. They are recorded here so the migration and the [audit](TERMS.md#audit) checklist have one source of truth for them.

1. **[Adjective](TERMS.md#adjective) crosses at most one [boundary](TERMS.md#boundary).** An [adjective](TERMS.md#adjective)'s value never traverses more than one [boundary](TERMS.md#boundary) as data. It is consumed inside the [boundary](TERMS.md#boundary) that calls the verb. No intermediate [noun](TERMS.md#noun) holds the raw value. (See 1.4, 2.5, 2.8.)
2. **Private fields and methods are the default enforcement.** In OO languages the [adjective](TERMS.md#adjective) is unreachable from outside except through published verbs. The language does the common case; the [gate](TERMS.md#gate) does the rest.
3. **Taint lifetime, not declared consumer.** The [gate](TERMS.md#gate) does not trust the plan's label of a call site as a consumer. It tracks the value's lifetime: assigned to a field, passed to another [boundary](TERMS.md#boundary), or returned from the consuming verb → violation. Consumed in place or dropped → fine. (See 2.5, A5.)
4. **Adjectives are noun-owned.** A verb honors them or breaks them; it never redefines them. A new verb version cannot fork an [adjective](TERMS.md#adjective) — it is validated against the [noun](TERMS.md#noun)'s full [adjective](TERMS.md#adjective) set at creation. (See 1.8, 2.10, A2.)
5. **Versioned verbs for [contract](TERMS.md#contract) churn.** [Ship](TERMS.md#ship) V2 alongside V1; migrate at each caller's pace; retire V1 when the [binding](TERMS.md#binding) graph shows zero callers. Versioning is API-shape only because adjectives cannot move with it. (See 1.8.)
6. **Gates are default closed.** A [gate](TERMS.md#gate) with no binder registered is marked unbound, never passed. (See vocabulary rules in `MIGRATION.md`.)
7. **Explicit empty [binding](TERMS.md#binding).** If a plan step finds no applicable ADRs or requirements, the [binding](TERMS.md#binding) step must declare "no bindings applicable, reason" — that declaration is itself a [binding](TERMS.md#binding) the [gate](TERMS.md#gate) can [verify](TERMS.md#verify).
8. **Fat nouns, own-state test.** A [noun](TERMS.md#noun) owns only adjectives and verbs about its own state. Behavior that does not read or write this [noun](TERMS.md#noun)'s adjectives belongs on another [noun](TERMS.md#noun). (See 2.1.)
9. **Batching verbs are declared, not accidental.** `chargeAndSettle()` is allowed to avoid chatty chains, but batches must be intentional. (See 2.3.)
10. **No handles.** Data residency is solved by binding-at-plan-time plus taint tracking, not by opaque capability types. (See 2.4.)
11. **Non-OO escape hatches are a known residual, not an open flaw.** A7 scans for raw SQL, ORM bypass, deserialization, and reflection. (See 2.9, A7.)
12. **Value-stream cost curve is the rationale for up-front cost.** A [defect](TERMS.md#defect) costs $1 in design, $10 in code, $1,000 in QA, $10,000 in UAT, $100,000 in production. [PLANIT](TERMS.md#planit) spends the extra minutes because the codebase lives five to ten years, and because swapping technology is one [requirement](TERMS.md#requirement) change when every swappable concern is a visible [adjective](TERMS.md#adjective). (See 1.6, 2.7.)

---

## Part 5 — The ledger, one line each

| # | Problem solved | Problem introduced | Mitigation |
|---|----------------|--------------------|------------|
| 1 | Locally green, globally wrong | — | Nouns own adjectives; [gate](TERMS.md#gate) fails goal-side writes |
| 2 | Anemic domain model | God [noun](TERMS.md#noun) | [Noun](TERMS.md#noun) owns only its own state; else call another [noun](TERMS.md#noun) |
| 3 | Decay under fast tech change | Regeneration only cheap if adjectives moved | Every swappable concern is a visible [adjective](TERMS.md#adjective) |
| 4 | Sensitive data leakage | Relocated leak if not closed properly | Value never crosses as data; taint lifetime enforced (A5) |
| 5 | Context-window explosion | — | One [boundary](TERMS.md#boundary) + its contracts per window |
| 6 | [Defect](TERMS.md#defect) cost compounds | Per-step [audit](TERMS.md#audit) cost | Mechanical per-step (incl. A5), deep per-package (A6) |
| 7 | [Interview](TERMS.md#interview) [quality](TERMS.md#quality) (design-resolved) | Empirical: catalog must be built in practice | Auditable [interview](TERMS.md#interview) log; misses become catalog entries |
| 8 | [Contract](TERMS.md#contract) churn | Versioned verb silently drops an [adjective](TERMS.md#adjective) | Adjectives are noun-owned; V2 validated against full [adjective](TERMS.md#adjective) set (A2); versioning is API-shape only |
| 9 | — | Leaky verbs | A5 treats returns and assignments the same |
| 10 | — | [Boundary](TERMS.md#boundary) thrash | Batching verbs, declared not accidental |
| 11 | — | [Adjective](TERMS.md#adjective) outlives verb | A5 taint tracking — no trust in [binding](TERMS.md#binding) declaration |
| 12 | — | Capability explosion | Reject handles; bind at plan time, enforce by taint |
| 13 | — | Non-OO escape hatches (residual existential flaw) | A7 scans for raw SQL / ORM / deserialization bypasses |

---

## Standing [rule](TERMS.md#rule)

This document is updated whenever a new risk is found in practice. A risk without a mitigation is a [defect](TERMS.md#defect) in the architecture, not a footnote. If you adopt this and hit a problem not listed here, add it — with the mitigation, or with an honest "unmitigated, do not adopt until solved."
