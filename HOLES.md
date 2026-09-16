# v1 holes — work next

Matrix is full (89 bound / 0 unbound). These are the places a v1 gate
**passes while the charter promise is still open**. Work in this order.
Each item: keep the designed-fail specimen, keep invoice-correct green,
document the new hole if any remains.

---

## 1. C17 — tests must cover failure, not just names — DONE

v2: name in tests **and** a test with assertRaises/pytest.raises.
invoice-correct now has preconditions + failure tests.
Still does not check adjective *preservation*.

---

## 2. C18 — no goal tests is not “use-case tested” — DONE

v2: goal with implementation.py must have tests; those tests must not
copy adjective tokens. invoice-correct has a use-case test (called
apply_payment). Still does not prove the test *runs* the goal.

---

## 3. R32 / C25 — taint across statements — DONE

v2: same-function aliases from `get_`/`read_`/`export_` (and from taint
tokens) fail on return/store/pass. Still does not follow helpers.

---

## 4. C15 — idempotency *key*, not only a flag — DONE

v2: retrying goal needs `"idempotent": true`, the key in the schema, and
`idempotency_key=` at the call. Nested parens not parsed. invoice-correct
has no retry marker → skip.

---

## 5. C22 — same change, actually — DONE

v2: N/A is illegal when the tree has CHARTER/adrs *and* goals/domain
source. PASS must cite existing paths. Still does not inspect git.

---

## 6. C7 / C8 / C11 — “changed”, not tree-wide — DONE

v2: `CHANGED:` in CONFIRM wins; else dirty git under the scan root; else
tree-wide. Unchanged goals with missing schemas / extra doors do not fail.
Still not `origin/main...HEAD` on a clean CI checkout of a PR (no list → tree-wide).

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

## 9. R20 — schema field vs code — DONE

v2: required fields named in the verb; annotated types must match JSON.
Charter-vs-matrix is still R27. Unannotated params skip the type check.

---

## 10. R4 — “mentions” vs “needs”

**Today.** Token from `fields.txt` / `adjectives.txt` anywhere in the
method.

**Tighten.** The verb must *read or write* `self.<field>` (or equivalent),
not merely mention the word in a string.

---

## 11. R32 locals leftover / R33 ORM

Taint still won’t follow `n = f(x); g(n)` through helpers. Escape hatch
still isn’t raw SQL / `.save(`. Only do these after 3.

---

## 12. C10 — breaking, not “version ≠ 1”

**Today.** Version 2 with no local `adrs/` fails. Version 1 → skip even if
the schema dropped a required field.

**Tighten.** After 5–6 (diff): a removed/renamed required field is breaking
and needs an ADR, regardless of the version number.

---

Work one item per pass. Don’t mint new matrix ids unless the charter
gained a new promise.
