# CONFIRM — examples/invoice-correct

**Role:** Confirmer (`G-CONFIRM`)  
**Change under review:** `examples/invoice-correct/` — goal `record_bank_payment` calls `Invoice.apply_payment`; does not assign `invoice.status` or `invoice.balance`.  
**Change class:** C (use-case / goal orchestration around existing verbs).  
**Date:** 2026-09-04

This file is a recorded confirmer template for the next agent. Charter §11.

---

## Required command outputs

### `python3 tools/fitness-no-noun-field-writes.py examples/invoice-correct`

```text
RESULT:MET
```

(exit 0)

### `python3 tools/assert-invoice-violation-fails.py`

```text
VIOLATION examples/invoice-violation/goals/record-bank-payment/implementation.py:5 balance
VIOLATION examples/invoice-violation/goals/record-bank-payment/implementation.py:6 status
RESULT:NOT_MET
ASSERT:PASS fixture still fails check 1 with required citation
```

(exit 0)

---

## Charter §11 checklist

Format: `Cx — PASS|FAIL|N/A — reason — file:line` (file:line omitted only for N/A).

### Classification and home

- C1 — PASS — Change class C stated in this confirmer note — examples/invoice-correct/CONFIRM.md:6
- C2 — PASS — Status/balance laws live on `Invoice` verbs, not in the goal — examples/invoice-correct/domain/invoice/invoice.py:10
- C3 — PASS — Orchestration is the goal entrypoint `record_bank_payment`, not a method glued onto an unrelated noun — examples/invoice-correct/goals/record-bank-payment/implementation.py:4

### Mutation path

- C4 — PASS — Fitness check 1 reports RESULT:MET; goal does not assign noun fields — examples/invoice-correct/goals/record-bank-payment/implementation.py:5
- C5 — PASS — Goal mutates only via public verb `apply_payment` — examples/invoice-correct/goals/record-bank-payment/implementation.py:5
- C6 — PASS — Noun module has no imports of goals/workflows — examples/invoice-correct/domain/invoice/invoice.py:1

### Contracts

- C7 — N/A — Tiny fixture has no goal contract JSON / schema files
- C8 — N/A — Tiny fixture has no verb contract JSON / schema files
- C9 — N/A — No dual contract layers in this tree to fork `balance` / `status`
- C10 — N/A — No schema version or breaking contract change in this fixture

### Goal and workflow shape

- C11 — PASS — One public entrypoint `record_bank_payment` — examples/invoice-correct/goals/record-bank-payment/implementation.py:4
- C12 — PASS — Single goal; does not import another goal’s internals — examples/invoice-correct/goals/record-bank-payment/implementation.py:1
- C13 — N/A — Teaching fixture demonstrating verb-only calls vs field writes; not a product goal-inventory change (pass-through acknowledged in charter §4.3)
- C14 — N/A — No workflows/ tree in this fixture
- C15 — N/A — No retrying workflow invokes these verbs in this fixture

### Invariants and tests

- C16 — PASS — Verb outcomes covered by noun tests (open/balance, paid-at-zero, void) — examples/invoice-correct/domain/invoice/tests/test_invoice.py:14
- C17 — FAIL — Success paths tested; no precondition-failure cases for the three verbs — examples/invoice-correct/domain/invoice/tests/test_invoice.py:13
- C18 — N/A — No separate goal-level test suite in this tiny fixture
- C19 — PASS — Status/balance transitions appear only under the noun, not reimplemented in the goal — examples/invoice-correct/goals/record-bank-payment/implementation.py:5

### Integrity of the change

- C20 — PASS — Fitness check 1 (R23 field-write surface) RESULT:MET for this tree; R24 law-locality linter not installed in hub (N/A portion noted) — tools/fitness-no-noun-field-writes.py (run above)
- C21 — N/A — No proposal impact list or generated caller graph for this fixture
- C22 — N/A — Fixture-only tree; no charter/ADR/contract edits in scope of this confirmer pass
- C23 — N/A — No adversarial review findings file for this fixture template
- C24 — N/A — No ratification log required for this teaching fixture (not a class A/B/D/E/F product change)

---

## Confirmer verdict

Template recorded. **C4 = PASS.** Fitness on `invoice-correct` = **RESULT:MET**. Blocking gaps for a *product* change would include C17 (precondition tests) and missing contracts (C7/C8) if those were in scope — they are noted, not papered over.

Gate `G-CONFIRM`: complete for this recorded template (checklist + required command outputs present).
