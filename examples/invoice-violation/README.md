# invoice-violation

Tiny fixture, not a product. Proves charter §14 item 4: fitness check 1 **fails a deliberate violation**.

`goals/record-bank-payment/implementation.py` assigns `invoice.status` (and `invoice.balance`) instead of calling `Invoice.apply_payment`. That is the point.

From repo root:

```text
python3 tools/fitness-no-noun-field-writes.py
```

Expected: exit 1, `VIOLATION` lines for `examples/invoice-violation/goals/record-bank-payment/implementation.py`, then `RESULT:NOT_MET`. If the command exits 0, the checker is wrong.
