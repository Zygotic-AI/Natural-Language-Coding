# CONFIRM — examples/invoice-correct

**Role:** [Confirmer](../../docs/TERMS.md#confirmer) (`G-CONFIRM`)  
**Change under review:** `examples/invoice-correct/` — [goal](../../docs/TERMS.md#goal) `record_bank_payment` calls `Invoice.apply_payment`; does not assign `invoice.status` or `invoice.balance`.  
**[Change class](../../docs/TERMS.md#change-class):** C (use-case / goal orchestration around existing verbs).  
**Date:** 2026-09-04

This file is a recorded [confirmer](../../docs/TERMS.md#confirmer) template for the next agent. [Charter](../../docs/TERMS.md#charter) §11.

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

## [Charter](../../docs/TERMS.md#charter) §11 checklist

Format: `Cx — PASS|FAIL|N/A — reason — file:line` (file:line omitted only for N/A).

### Classification and home

- C1 — PASS — [Change class](../../docs/TERMS.md#change-class) C stated in this [confirmer](../../docs/TERMS.md#confirmer) note — examples/invoice-correct/CONFIRM.md:6
- C2 — PASS — Status/balance adjectives live on `Invoice` verbs, not in the [goal](../../docs/TERMS.md#goal) — examples/invoice-correct/domain/invoice/invoice.py:10
- C3 — PASS — Orchestration is the [goal](../../docs/TERMS.md#goal) entrypoint `record_bank_payment`, not a method glued onto an unrelated [noun](../../docs/TERMS.md#noun) — examples/invoice-correct/goals/record-bank-payment/implementation.py:4

### Mutation path

- C4 — PASS — [Gate](../../docs/TERMS.md#gate) 1 reports RESULT:[MET](../../docs/TERMS.md#met); [goal](../../docs/TERMS.md#goal) does not assign [noun](../../docs/TERMS.md#noun) fields — examples/invoice-correct/goals/record-bank-payment/implementation.py:5
- C5 — PASS — [Goal](../../docs/TERMS.md#goal) mutates only via public verb `apply_payment` — examples/invoice-correct/goals/record-bank-payment/implementation.py:5
- C6 — PASS — [Noun](../../docs/TERMS.md#noun) module has no imports of goals/workflows — examples/invoice-correct/domain/invoice/invoice.py:1

### Contracts

- C7 — N/A — Tiny fixture has no [goal](../../docs/TERMS.md#goal) [contract](../../docs/TERMS.md#contract) JSON / schema files
- C8 — N/A — Tiny fixture has no verb [contract](../../docs/TERMS.md#contract) JSON / schema files
- C9 — N/A — No dual [contract](../../docs/TERMS.md#contract) layers in this tree to fork `balance` / `status`
- C10 — N/A — No schema version or breaking [contract](../../docs/TERMS.md#contract) change in this fixture

### [Goal](../../docs/TERMS.md#goal) and [workflow](../../docs/TERMS.md#workflow) shape

- C11 — PASS — One public entrypoint `record_bank_payment` — examples/invoice-correct/goals/record-bank-payment/implementation.py:4
- C12 — PASS — Single [goal](../../docs/TERMS.md#goal); does not import another [goal](../../docs/TERMS.md#goal)’s internals — examples/invoice-correct/goals/record-bank-payment/implementation.py:1
- C13 — N/A — Teaching fixture demonstrating verb-only calls vs field writes; not a product goal-inventory change (pass-through acknowledged in charter §4.3)
- C14 — N/A — No workflows/ tree in this fixture
- C15 — N/A — No retrying [workflow](../../docs/TERMS.md#workflow) invokes these verbs in this fixture

### Adjectives and tests

- C16 — PASS — Verb outcomes covered by [noun](../../docs/TERMS.md#noun) tests (open/balance, paid-at-zero, void) — examples/invoice-correct/domain/invoice/tests/test_invoice.py:14
- C17 — PASS — Each verb has a success test and assertRaises precondition — examples/invoice-correct/domain/invoice/tests/test_invoice.py

- C18 — PASS — [Goal](../../docs/TERMS.md#goal) test checks the use-case (called apply_payment), not [noun](../../docs/TERMS.md#noun) adjectives — examples/invoice-correct/goals/record-bank-payment/tests/test_record_bank_payment.py

- C19 — PASS — Status/balance transitions appear only under the [noun](../../docs/TERMS.md#noun), not reimplemented in the [goal](../../docs/TERMS.md#goal) — examples/invoice-correct/goals/record-bank-payment/implementation.py:5

### [Integrity](../../docs/TERMS.md#integrity) of the change

- C20 — PASS — [Gate](../../docs/TERMS.md#gate) 1 (R23 field-write surface) RESULT:[MET](../../docs/TERMS.md#met) for this tree; R24 adjective-locality linter not installed in [hub](../../docs/TERMS.md#hub) (N/A portion noted) — tools/fitness-no-noun-field-writes.py (run above)
- C21 — PASS — Generated caller `invoice.apply_payment` is named in this note (header + this line) — examples/invoice-correct/goals/record-bank-payment/implementation.py:5

- C22 — N/A — Fixture-only tree; no charter/ADR/contract edits in scope of this [confirmer](../../docs/TERMS.md#confirmer) pass
- C23 — N/A — No adversarial review findings file for this fixture template
- C24 — N/A — No ratification log required for this teaching fixture (not a class A/B/D/E/F product change)

---

## [Confirmer](../../docs/TERMS.md#confirmer) verdict

Template recorded. **C4 = PASS.** Fitness on `invoice-correct` = **RESULT:[MET](../../docs/TERMS.md#met)**. Blocking gaps for a *product* change would include C17 (precondition tests) and missing contracts (C7/C8) if those were in scope — they are noted, not papered over.

[Gate](../../docs/TERMS.md#gate) `G-CONFIRM`: complete for this recorded template (checklist + required command outputs present).
