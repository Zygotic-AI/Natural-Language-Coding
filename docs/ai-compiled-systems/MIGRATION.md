# Migration: BBA primitives into AIMS

Date: 2026-09-15

## Why this exists

The AIMS documents describe a world without nouns. Until they are rewritten, anyone reading the process spec will generate goal-only code and call it done. This is the fourth existential issue, and it is the action of the merge itself.

What we have done so far: placed the AIMS documents inside the BBA repo and added a hallway between them. That is not a merge. The AIMS terminology has not been rewritten to require BBA-shaped output.

This document is the plan to finish the merge methodically.

---

## The primitives (dependency order)

Each primitive assumes only the ones above it. Do not introduce a term before its dependencies exist.

1. **Noun** — the atomic object; owns state and behavior.
2. **Adjective** — a descriptor on a noun that no verb may violate.
3. **Verb** — the only legal mutation path; honors every adjective on its noun.
4. **Boundary** — the sealed edge; crossing it is only legal through a published verb.
5. **Goal** — an outcome that reaches the edge; calls verbs, never writes fields.
6. **Contract** — the published input, output, and failure mode of a verb.
7. **Requirement** — a constraint on behavior, bound to goals, verbs, or nouns.
8. **ADR** — a dated decision; treated as any rule in the system.
9. **Knowledge domain** — a shelf of standing ADRs and requirements the interview consults.
10. **PLANIT** — the process: interview, decompose into work packages, bind, generate, audit.
11. **Binding** — the planning act of linking each atomic step to the ADRs and requirements it must honor. An explicit "no bindings applicable" declaration is itself a binding.
12. **Gate** — the verification act. Runs after generation. Checks that the code held the bindings. Default closed: a gate with no binder registered is marked unbound, never passed.
13. **Audit** — the independent pass (adversarial) that verifies code against bindings and rules. Includes the taint-lifetime check (A5) and the non-OO escape-hatch check (A7).

**Dependency note:** 1 and 2 are the foundation. 5 (goal) cannot be defined until 3 (verb) exists. 11 (binding) and 12 (gate) are distinct acts — binding happens in planning, gate happens after generation. Do not conflate them.

---

## The method

Not a single rewrite pass. Section by section.

1. **List the primitives first** (done above). This is the checklist.
2. **Order them by dependency** (done above). Noun and adjective land before goal.
3. **Walk each AIMS document one section at a time.** For each section, ask: which of these primitives apply here? Rewrite that section so the applicable primitives are inside it, using the settled vocabulary.
4. **Do not introduce a term before its dependencies.** If a section needs "goal," noun and verb must already be defined in an earlier section or an earlier document.
5. **Compounded primitives may move together** when they are inseparable (e.g., noun + adjective + verb often land as one unit). Still list them; still respect order.
6. **After each document is rewritten, it must not reference an undefined term.** A reader going top to bottom never hits a forward reference to a primitive not yet introduced.
7. **CHARTER.md stays the design SSOT** until the migration is complete. These pages do not replace it.

---

## Document walk order

Walk in this order. Each pass introduces only the primitives that section needs.

| Pass | Document | Primitives introduced | Notes |
|------|----------|----------------------|-------|
| 1 | MANIFESTO.md | noun, adjective, verb (lightly) | Source is intent; shape is not optional. Introduce noun as where an adjective lives. |
| 2 | ARCHITECTURE.md | noun, adjective, verb, boundary, goal, contract | Two layers, two citizen lists. Replace "binder" with binding + gate. |
| 3 | COMPILER.md | noun, adjective, verb, boundary, contract, gate | Incomplete generation = gate fails. |
| 4 | PROCESS.md | PLANIT, binding, gate, audit, knowledge domain | The loop. Binding is step 4; gate is step 7. |
| 5 | MERGE.md | all (reconcile) | Vocabulary table updated; citizen lists updated. |
| 6 | AIMS-FILE-MAP.md | — | Update the "still to write" list to reflect landed pages. |
| 7 | README.md | — | Index update; link to this migration doc. |

Later authoring pages (goal authoring, requirement authoring, interview patterns, RCA record) land after this pass and inherit the vocabulary.

---

## Vocabulary rules for the rewrite

- **Binder** is retired as a noun. Use **gate** for the machine that fails a change. Use **binding** for the planning act.
- **Invariant** is retired. Use **adjective**.
- **Standing rules** is retired. Use **BBA standard**.
- A gate is **default closed**. A gate with no binder registered is **unbound**, never green.
- Binding a step to nothing applicable requires an explicit "no bindings applicable, reason" declaration.
- Adjectives belong to the noun. A verb honors them or breaks them; it never redefines them. A new verb version cannot fork an adjective.

---

## Definition of done

The migration is done when:

- Every AIMS document uses the settled vocabulary.
- No document describes generation without BBA shape as a valid output.
- No document references "binder" as a planning concept; binding and gate are distinct.
- A reader can go top to bottom through the folder and never encounter an undefined primitive.
- CHARTER.md is still the design SSOT; these pages point at it, not around it.
