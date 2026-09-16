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

## 3. R32 / C25 — taint across statements

**Today.** `return card_number` fails; `n = card.get_number(); return n`
does not.

**Tighten.** Same-function assignment then return/store/pass of a tainted
name. Still not full dataflow.

---

## 4. C15 — idempotency *key*, not only a flag

**Today.** Retrying goal + `"idempotent": true` on the verb. A key argument
is not required or checked.

**Tighten.** Retrying goal must pass a named key (`idempotency_key` /
`idempotent_key`) that the verb schema declares.

---

## 5. C22 — same change, actually

**Today.** Confirmer contains `C22 — PASS|N/A`. No git.

**Tighten.** If the diff (or a named file list in the note) touches
`CHARTER.md` / `adrs/` / `*.schema.json` / `domain|goals`, the other
affected sides must appear in that same change. Needs git or an explicit
file list the confirmer cites that we stat.

---

## 6. C7 / C8 / C11 — “changed”, not tree-wide

**Today.** Cousins of R9 / R10 / R13 on the whole tree.

**Tighten.** Only entrypoints whose files are in the change (git, or a
`CHANGED:` list in CONFIRM). Unchanged goals with missing schemas must not
fail a product PR that didn’t touch them.

---

## 7. C23 — confirmer FAIL is a finding

**Today.** Only `FINDINGS.md` open checkboxes. invoice-correct `C17 — FAIL`
is invisible.

**Tighten.** Every `Cx — FAIL` in CONFIRM is an open finding unless the
same line contains `rebut` / `hole` / `accepted`. Patch invoice-correct
C17 to name the hole or add the missing tests (ties to item 1).

---

## 8. C1 / C21 / C24 — skip-if-no-note

**Today.** No `CONFIRM.md` → MET. An agent can skip the note and go green.

**Tighten.** If the scan root has `goals/` or `domain/` *and* this is a
product tree (not a designed-fail specimen), require CONFIRM.md. Specimens
stay exempt via README `Specimen.` marker already used.

---

## 9. R20 — schema field vs code

**Today.** Charter ids sit in the matrix. A schema `amount: integer` vs
code `amount: str` still passes.

**Tighten.** For each `verbs.schema.json` required field, the verb’s
signature or body must name that field. Complementary to R11 (type
identity across files).

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
