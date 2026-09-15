# Risks and Concerns

This document qualifies the architecture upfront: the problems it solves, the problems it introduces, and the mitigating steps for each. Read it before adopting. It is not a second charter — the BBA standard in `CHARTER.md` remains the design SSOT. This is the honest ledger of trade-offs.

---

## Part 1 — Problems this architecture solves

### 1.1 Locally green, globally wrong

**Problem.** Agents ship code that passes every local test and still forks a business rule across two goals. Two goals each invent `status`. Both look correct. The user finds the bug at $100,000.

**Solved by.** Nouns own adjectives (the descriptors that must stay true). Verbs are the only mutation path. Goals call verbs; they never write noun fields or re-decide an adjective. A machine binder fails any goal-side write.

### 1.2 Anemic domain model

**Problem.** Thin nouns with verbs scattered across goals are procedural code wearing a class costume. The logic lives wherever the last developer put it. Nobody can find it. Nobody can audit it.

**Solved by.** Fat nouns. Every verb that reads or writes a noun's adjectives lives on that noun. The noun is the single place that knows how to charge a card, mask a PAN, or void an invoice.

### 1.3 Software decay under fast technology change

**Problem.** New technology arrives faster every year. Each swap is a rewrite because the concern is scattered across the codebase. Decay rate accelerates.

**Solved by.** Swappable concerns are adjectives on nouns. Changing "log to a file" into "log to Logstash" is one requirement change. The AI figures out the delta and rebuilds only the affected noun. Same codebase, new technology.

### 1.4 Sensitive data leakage (PII, PCI)

**Problem.** A card number or a person's name gets passed around as a bare value through DTOs and intermediate objects. It leaks into logs, caches, and places that should never see it.

**Solved by.** An adjective's value never traverses more than one boundary as data. It is consumed inside the boundary that calls the verb. No intermediate noun ever holds the raw value.

### 1.5 Context-window explosion

**Problem.** An agent editing a large codebase needs the whole repo in context. Cost and error rate scale with size.

**Solved by.** Discrete atomic boundaries. The agent works on one boundary at a time, plus the published contracts of the nouns it calls. The repo can be huge; the window never is.

### 1.6 Defect cost compounds down the value stream

**Problem.** A defect found in design costs $1. In code, $10. In QA, $1,000. In UAT, $10,000. In production, $100,000. The further down the stream, the more expensive.

**Solved by.** PLANIT spends the extra minutes up front — interview, bind, audit — because the codebase lives five to ten years. The two-minute audit is cheap against a decade of operation.

---

## Part 2 — Problems this architecture introduces

### 2.1 God noun

**Problem.** Once fat is rewarded, every new behavior wants to live on the nearest noun. `Invoice` ends up owning tax calculation, email, PDF rendering, and fraud scoring. One class that knows everything — the anemic model in reverse.

**Mitigation.** A noun may only own an adjective or verb that is about that noun's own state. Tax calculation belongs on a `Tax` noun, not `Invoice`. `Invoice` calls `Tax.calculate` — one hop, allowed. The test: does this behavior read or write this noun's adjectives? If no, it does not belong here.

### 2.2 Leaky verbs

**Problem.** A verb returns a raw sensitive value instead of doing the work — `getCardNumber()` instead of `charge()`. That is the escape hatch the binder is supposed to catch.

**Mitigation.** The audit treats *returning* a sensitive adjective the same as *assigning* one. A verb that returns PCI data to a caller that is not the declared consumer fails. The audit checks return values, not just field writes.

### 2.3 Boundary thrash / chatty call chains

**Problem.** If every interaction is one hop and nouns cannot carry data, you get chatty chains — `Order` calls `Payment`, `Payment` calls `Card`, `Card` calls `Bank`. Fine for auditability, expensive at runtime.

**Mitigation.** Batching verbs: `chargeAndSettle()` instead of `charge()` then `settle()`. The cost is fat verbs, which is the same gravity as the god noun, just at the verb level. Keep batches intentional and declared, not accidental.

### 2.4 Capability explosion (rejected path)

**Problem.** Solving data residency with opaque handles instead of the binding rule drowns the system in handle types — one handle per sensitive adjective per noun.

**Mitigation.** Do not use handles. Use binding-at-plan-time: the plan declares the call site as the consumer; the audit verifies the value is consumed in place. No second object type.

### 2.5 Adjective value outlives the consuming verb (supersedes 2.5)

**Problem.** Even with a correct binding, the fetched value can be stored in another piece of data or returned from the verb that used it. The leak is not about intent — it is about lifetime. `charge(card.getNumber())` is fine; `let n = card.getNumber(); stash(n)` is not.

**Mitigation.** The adversarial audit tracks the adjective's **taint lifetime**, not the plan's declared consumer. Rule: a sensitive adjective fetched inside a verb may not be assigned to a field, passed as an argument to another boundary, or returned from that verb. It must be consumed inside the same verb and dropped. The audit is mechanical taint tracking — no trust in the binding declaration. This removes the silent-hole risk entirely: the binder does not need to know whether the site is a consumer; it only needs to know the value never escapes.

### 2.6 Per-step audit cost

**Problem.** If each atomic step spawns a heavy review, PLANIT becomes slower than writing code directly. The cycle eats its own value.

**Mitigation.** Keep per-step audits mechanical: does this code touch only what it was bound to, and does no sensitive adjective outlive its verb? Save deep adversarial review for work-package completion. Two tiers — cheap gate per step, thorough review per package.

### 2.7 Regeneration only stays cheap if adjectives actually moved

**Problem.** If "log to a file" was a goal's private habit instead of an adjective on a `Logging` noun, changing the requirement regenerates nothing. You still have scattered file writes to find.

**Mitigation.** Every swappable concern must be an adjective the binder can see. The manifesto's "same codebase, new tech" promise holds only when this is true. Audit the adjectives, not just the nouns.

### 2.8 Sensitive data relocated, not closed

**Problem.** "Invoice calls Customer directly" still moves the name across a boundary. The PDF generator now holds PII in its own memory. The leak is relocated, not closed.

**Mitigation.** The adjective's value never becomes data that crosses a boundary. It is consumed inside the calling statement. No intermediate noun holds the raw value. Combined with 2.5, the audit enforces this mechanically.

### 2.9 Non-OO escape hatches (residual risk of the existential flaw)

**Problem.** Private fields and methods make adjectives unreachable from outside in OO languages. But the language's protection dies the moment a goal reaches the noun through serialization, a raw SQL update, or an ORM that bypasses the object entirely. The noun's adjective is never consulted, so nothing fails, but the rule now lives in two places. This is the residual of the original binder gap — narrowed, not eliminated.

**Mitigation.** A7 on the audit checklist: scan for direct storage access — raw SQL, ORM bypasses, deserialization into noun state, reflection — that mutates or reads a noun's adjectives without going through a published verb. This is a narrow, known hole with a specific check, not an open one. The OO privacy handles the common case; A7 handles the paths the language cannot see.

---

## Part 3 — Adversarial audit checklist

Every artifact creation or change runs an adversarial audit. The audit family grows with the artifact type. None of these trust the generator.

| # | When | What it checks |
|---|------|----------------|
| A1 | Noun created | The new noun reaches no other boundary except through that boundary's published verbs. Both directions: it does not read another noun's state, and it does not call into a goal. |
| A2 | Verb / adjective added or changed | Every caller of a changed contract still satisfies it, or callers were updated in the same change. |
| A3 | Goal completed | The code actually delivers the stated outcome — not just compiles, not just passes local tests. |
| A4 | Requirement bound | The bound code path enforces the requirement, not merely references it. |
| A5 | Any sensitive adjective fetched | **Taint lifetime:** the value is not assigned to a field, passed to another boundary, or returned from the consuming verb. Consumed in place or dropped. (Replaces any "declared consumer" check.) |
| A6 | Work package completed | Deep review: statements done, all bound ADRs/requirements held, no second copy of an adjective inside a goal, no god-noun growth. |
| A7 | Any noun mutation or read | **Non-OO escape hatches:** no raw SQL, ORM bypass, deserialization, or reflection mutates or reads a noun's adjectives without going through a published verb. Catches the residual of the existential flaw — the paths OO privacy cannot see. |

**Rule:** A5 is mechanical and cheap — it runs at every per-step gate. A6 is the thorough pass at package completion. A7 runs wherever a noun's storage is touched. Do not merge A5 into A6; the cheap taint check is what keeps PLANIT fast. Do not skip A7 because "we use OO" — the escape hatches are exactly where the existential flaw survives.

---

## Part 4 — The ledger, one line each

| # | Problem solved | Problem introduced | Mitigation |
|---|----------------|--------------------|------------|
| 1 | Locally green, globally wrong | — | Nouns own adjectives; binder fails goal-side writes |
| 2 | Anemic domain model | God noun | Noun owns only its own state; else call another noun |
| 3 | Decay under fast tech change | Regeneration only cheap if adjectives moved | Every swappable concern is a visible adjective |
| 4 | Sensitive data leakage | Relocated leak if not closed properly | Value never crosses as data; taint lifetime enforced (A5) |
| 5 | Context-window explosion | — | One boundary + its contracts per window |
| 6 | Defect cost compounds | Per-step audit cost | Mechanical per-step (incl. A5), deep per-package (A6) |
| 7 | — | Leaky verbs | A5 treats returns and assignments the same |
| 8 | — | Boundary thrash | Batching verbs, declared not accidental |
| 9 | — | Adjective outlives verb | A5 taint tracking — no trust in binding declaration |
| 10 | — | Capability explosion | Reject handles; bind at plan time, enforce by taint |
| 11 | — | Non-OO escape hatches (residual existential flaw) | A7 scans for raw SQL / ORM / deserialization bypasses |

---

## Standing rule

This document is updated whenever a new risk is found in practice. A risk without a mitigation is a defect in the architecture, not a footnote. If you adopt this and hit a problem not listed here, add it — with the mitigation, or with an honest "unmitigated, do not adopt until solved."
