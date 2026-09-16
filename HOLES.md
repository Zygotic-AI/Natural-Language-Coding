# v1 holes — work next

Matrix is full (89 bound / 0 unbound). These are the places a v1 gate
**passes while the charter promise is still open**. Work in this order.
Each item: keep the designed-fail specimen, keep invoice-correct green,
document the new hole if any remains.

---

## 1. C17 — tests must cover failure, not just names — CLOSED

Success + `assertRaises` + a non-raises test that names an adjective and
asserts. Execution is CI, not this scanner.

## 2. C18 — no goal tests is not “use-case tested” — CLOSED

Goal tests must call a public impl function (`name(`). Copied adjectives
still fail. Execution is CI.

---

## 3. R32 / C25 — taint across statements — DONE

v2: same-function aliases from `get_`/`read_`/`export_` (and from taint
tokens) fail on return/store/pass. Still does not follow helpers.

---

## 4. C15 — idempotency *key*, not only a flag — CLOSED

Nested parens parsed. Call must pass the key; the verb body must use it.
No retry → skip.

---

## 5. C22 — same change, actually — CLOSED

N/A is illegal when the change set (CHANGED: / dirty git /
`origin/main...HEAD`) includes charter and code. Tree shape alone is not
the test.

## 6. C7 / C8 / C11 — “changed”, not tree-wide — CLOSED

Same change set as C22. Clean main checkout with no list still tree-wide
(nothing changed). A PR diff against `origin/main` scopes the check.

---

## 7. C23 — confirmer FAIL is a finding — DONE

v2: `- C12 — FAIL` in CONFIRM is an open finding unless the line has
rebut/accepted/hole. invoice-correct has no FAIL lines (C17 is PASS).
Still not a human signature.

---

## 8. C1 / C21 / C24 — skip-if-no-note — DONE

v2: product trees (goals/ or domain/, README not Specimen/Designed red/
Known-fail) require CONFIRM.md. Specimens still skip. Class still not
checked for *correctness*.

---

## 9. R20 — schema field vs code — CLOSED

Required fields must be named *and annotated*. JSON type must match when present.

## 11. R32 helpers / R33 ORM — CLOSED

Same-file helpers that return taint taint their callers.
Escape hatch includes setattr / .save( / SQL execute.
Out of reach: taint across files.

## 12. C10 — breaking, not “version ≠ 1” — CLOSED

Dropped required fields vs `*.previous.json` need an ADR even at version 1.

---

## 10. R4 — “mentions” vs “needs” — DONE

Public verbs must read/write `self.<field>` (or getattr/setattr). String
mention is not use. Out of reach: whether a *using* verb belongs on this
noun rather than another.

---

## 11. R32 locals leftover / R33 ORM — CLOSED

Same-file helpers that return taint taint their callers.
Escape hatch includes setattr / .save( / SQL execute.
Out of reach: taint across files.

## 12. C10 — breaking, not “version ≠ 1” — CLOSED

Dropped required fields vs `*.previous.json` need an ADR even at version 1.

---

Work one item per pass. Don’t mint new matrix ids unless the charter
gained a new promise.
