# Interview pattern catalog (UC1)

Empirical prompts for **PLANIT step 1** ([`PROCESS.md`](PROCESS.md)). Patterns compound: when prove fails or ship forks, replay the interview and add a **miss** row below.

SSOT procedure: [`.agents/skills/interview/SKILL.md`](../../.agents/skills/interview/SKILL.md). Knowledge domains: [`knowledge/facts.json`](../../knowledge/facts.json) + steward `load-knowledge-domain`.

## When to use this page

| Situation | Action |
| --------- | ------ |
| Starting `/interview` | Run **P-LOAD** then **P-OUTCOME**; consult **P-KD** before policy guesses |
| User lists features first | **P-OUTCOME**, then **P-GOAL** |
| Compliance / PCI / HIPAA named | **P-KD**, **P-COMPLIANCE-SCOPE** |
| Two teams want different behavior | **P-FORK**, **P-REQ-ADR** |
| Interview feels “done” | **P-HANDOFF** gate table |

## Patterns

### P-LOAD — Load before you ask

**Trigger:** Any fact might already be bound (charter, ADRs, requirements, prior interview).

**Ask:** What is already ratified in this repo or hub that answers this?

**Pass:** Step 0 complete; no duplicate questions for bound ids.

---

### P-OUTCOME — Outcome one-liner

**Trigger:** Feature list, tech stack, or “build X module” without user or success shape.

**Ask:** Who is blocked today? What changes for them when this works? How do we know in one sentence?

**Pass:** One line: problem + actor + observable success (not implementation).

---

### P-GOAL — Name goals, not tasks

**Trigger:** Plan items sound like Jira tickets (“add API”, “write tests”).

**Ask:** What **goal** does the user accomplish? Which **nouns** and **verbs** are in play?

**Pass:** At least one goal id or explicit “no new goals” with reason; goals call verbs only (charter).

---

### P-KD — Knowledge domain before policy

**Trigger:** Security, privacy, payments, retention, or “we must comply with …”.

**Ask:** Which **knowledge domain** applies? Run `load-knowledge-domain` (or `nlc-before-generate.py` before generate). What facts are missing?

**Pass:** Facts in scope cited, or `flag-gap` + `propose-fact` path named; gaps closed or `Assumption:` logged.

---

### P-COMPLIANCE-SCOPE — Standard → requirement → ADR

**Trigger:** External standard cited without adoption record.

**Ask:** Is this a **requirement** we must meet, or a **decision** we still need (ADR)? What is in force in *this* repo today?

**Pass:** Requirement refs or `Waived:`; no silent “industry best practice” without bind.

---

### P-REQ-ADR — Constraint vs decision

**Trigger:** “Should we encrypt?” vs “We cannot store PAN.”

**Ask:** Is this fixed input (requirement / fact) or a choice we must record (ADR)?

**Pass:** Requirements state constraints; conflicts go to ADR precedence ([ADR 0012](../../adrs/0012-adr-precedence-and-rule-conflicts.md)), not interview debate.

---

### P-BOUNDARY — Nouns and verbs early

**Trigger:** Ambiguous ownership (“the system sends email”).

**Ask:** Which **noun** owns the verb? What crosses the boundary (input, output, failure mode)?

**Pass:** Candidate noun list or explicit “boundary TBD” blocker for plan step.

---

### P-FORK — One adjective, one goal

**Trigger:** Same quality word on two outcomes (“secure checkout” and “secure admin” with different rules).

**Ask:** Are these the same requirement id on both goals, or a fork that needs two bindings?

**Pass:** No duplicate adjective across goals without shared requirement/ADR pointer (R1 / C3).

---

### P-WAIVE — Explicit waive

**Trigger:** User wants to skip constraints, knowledge load, or goals “for now”.

**Ask:** What is waived, why, and what prove step will catch a mistake?

**Pass:** `Waived: <item> — <reason>` in handoff; blocking gate rows updated.

---

### P-HANDOFF — Resolution table for `/planit`

**Trigger:** User asks to “start coding” or interview gate rows are green.

**Emit:**

| Goals | Requirements / ADRs | Knowledge domains | Assumptions / waivers |
| ----- | ------------------- | ----------------- | --------------------- |
| … | … | … | … |

**Pass:** User directed to `/planit`, not ship; no generate in interview skill.

## Miss log (add rows from RCA)

When compile or adversarial audit fails because the interview skipped something, append a row. Do not delete old rows.

| Date | Symptom (prove / ship) | Missed pattern | Question we should have asked | Follow-up (fact, req, ADR) |
| ---- | ---------------------- | -------------- | ----------------------------- | -------------------------- |
| 2026-09-20 | (seed) | P-KD | Which knowledge domain covers card data before naming storage? | See [`docs/worked-examples/pan-handling/`](../worked-examples/pan-handling/README.md) |

## Related

- [INTENT-SURFACE.md](INTENT-SURFACE.md) — what interview may touch
- [QUALITY-PROCESSES.md](QUALITY-PROCESSES.md) — auditable interview, catalog compounding
- [docs/RISKS-AND-CONCERNS.md](../RISKS-AND-CONCERNS.md) — replay and measurable “good”
