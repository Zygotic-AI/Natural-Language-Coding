# [Interview](../TERMS.md#interview) pattern catalog (UC1)

Empirical prompts for **[PLANIT](../TERMS.md#planit) step 1** ([`PROCESS.md`](PROCESS.md)). Patterns compound: when [prove](../TERMS.md#prove) fails or [ship](../TERMS.md#ship) forks, replay the [interview](../TERMS.md#interview) and add a **miss** row below.

SSOT procedure: [`.agents/skills/interview/SKILL.md`](../../.agents/skills/interview/SKILL.md). [Knowledge domains](../TERMS.md#knowledge-domain): [`knowledge/facts.json`](../../knowledge/facts.json) + steward `load-knowledge-domain`.

## When to use this page

| Situation | [Action](../TERMS.md#action) |
| --------- | ------ |
| Starting `/interview` | Run **P-LOAD** then **P-OUTCOME**; consult **P-KD** before policy guesses |
| User lists features first | **P-OUTCOME**, then **P-GOAL** |
| Compliance / PCI / HIPAA named | **P-KD**, **P-COMPLIANCE-SCOPE** |
| Two teams want different behavior | **P-FORK**, **P-REQ-ADR** |
| [Interview](../TERMS.md#interview) feels “done” | **P-HANDOFF** [gate](../TERMS.md#gate) table |

## Patterns

### P-LOAD — Load before you ask

**Trigger:** Any fact might already be bound (charter, ADRs, requirements, prior interview).

**Ask:** What is already ratified in this repo or [hub](../TERMS.md#hub) that answers this?

**Pass:** Step 0 complete; no duplicate questions for bound ids.

---

### P-OUTCOME — Outcome one-liner

**Trigger:** Feature list, tech stack, or “build X module” without user or success shape.

**Ask:** Who is blocked today? What changes for them when this works? How do we know in one sentence?

**Pass:** One line: problem + actor + observable success (not implementation).

---

### P-GOAL — Name goals, not tasks

**Trigger:** Plan items sound like Jira tickets (“add API”, “write tests”).

**Ask:** What **[goal](../TERMS.md#goal)** does the user accomplish? Which **nouns** and **verbs** are in play?

**Pass:** At least one [goal](../TERMS.md#goal) id or explicit “no new goals” with reason; goals call verbs only (charter).

---

### P-KD — [Knowledge domain](../TERMS.md#knowledge-domain) before policy

**Trigger:** Security, privacy, payments, retention, or “we must comply with …”.

**Ask:** Which **[knowledge domain](../TERMS.md#knowledge-domain)** applies? Run `load-knowledge-domain` (or `nlc-before-generate.py` before generate). What facts are missing?

**Pass:** Facts in scope cited, or `flag-gap` + `propose-fact` path named; gaps closed or `Assumption:` logged.

---

### P-COMPLIANCE-SCOPE — Standard → [requirement](../TERMS.md#requirement) → [ADR](../TERMS.md#adr)

**Trigger:** External standard cited without adoption record.

**Ask:** Is this a **[requirement](../TERMS.md#requirement)** we must meet, or a **decision** we still need (ADR)? What is in force in *this* repo today?

**Pass:** [Requirement](../TERMS.md#requirement) refs or `Waived:`; no silent “industry best practice” without bind.

---

### P-REQ-ADR — Constraint vs decision

**Trigger:** “Should we encrypt?” vs “We cannot store PAN.”

**Ask:** Is this fixed input (requirement / fact) or a choice we must record (ADR)?

**Pass:** Requirements state constraints; conflicts go to [ADR](../TERMS.md#adr) precedence ([ADR 0012](../../adrs/0012-adr-precedence-and-rule-conflicts.md)), not [interview](../TERMS.md#interview) debate.

---

### P-BOUNDARY — Nouns and verbs early

**Trigger:** Ambiguous ownership (“the system sends email”).

**Ask:** Which **[noun](../TERMS.md#noun)** owns the verb? What crosses the [boundary](../TERMS.md#boundary) (input, output, failure mode)?

**Pass:** Candidate [noun](../TERMS.md#noun) list or explicit “[boundary](../TERMS.md#boundary) TBD” blocker for plan step.

---

### P-FORK — One [adjective](../TERMS.md#adjective), one [goal](../TERMS.md#goal)

**Trigger:** Same [quality](../TERMS.md#quality) word on two outcomes (“secure checkout” and “secure admin” with different rules).

**Ask:** Are these the same [requirement](../TERMS.md#requirement) id on both goals, or a fork that needs two bindings?

**Pass:** No duplicate [adjective](../TERMS.md#adjective) across goals without shared requirement/ADR pointer (R1 / C3).

---

### P-WAIVE — Explicit waive

**Trigger:** User wants to skip constraints, knowledge load, or goals “for now”.

**Ask:** What is [waived](../TERMS.md#waived), why, and what [prove](../TERMS.md#prove) step will catch a mistake?

**Pass:** `Waived: <item> — <reason>` in [handoff](../TERMS.md#handoff); blocking [gate](../TERMS.md#gate) rows updated.

---

### P-HANDOFF — Resolution table for `/planit`

**Trigger:** User asks to “start coding” or [interview](../TERMS.md#interview) [gate](../TERMS.md#gate) rows are green.

**Emit:**

| Goals | Requirements / ADRs | [Knowledge domains](../TERMS.md#knowledge-domain) | Assumptions / waivers |
| ----- | ------------------- | ----------------- | --------------------- |
| … | … | … | … |

**Pass:** User directed to `/planit`, not [ship](../TERMS.md#ship); no generate in [interview](../TERMS.md#interview) skill.

## Miss log (add rows from RCA)

When compile or adversarial [audit](../TERMS.md#audit) fails because the [interview](../TERMS.md#interview) skipped something, append a row. Do not delete old rows.

| Date | Symptom (prove / ship) | Missed pattern | Question we should have asked | Follow-up (fact, req, ADR) |
| ---- | ---------------------- | -------------- | ----------------------------- | -------------------------- |
| 2026-09-20 | (seed) | P-KD | Which [knowledge domain](../TERMS.md#knowledge-domain) covers card data before naming storage? | See [`docs/worked-examples/pan-handling/`](../worked-examples/pan-handling/README.md) |

## Related

- [INTENT-SURFACE.md](INTENT-SURFACE.md) — what [interview](../TERMS.md#interview) may touch
- [QUALITY-PROCESSES.md](QUALITY-PROCESSES.md) — auditable [interview](../TERMS.md#interview), catalog compounding
- [docs/RISKS-AND-CONCERNS.md](../RISKS-AND-CONCERNS.md) — replay and measurable “good”
