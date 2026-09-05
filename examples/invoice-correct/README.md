# invoice-correct

Tiny fixture, not a product. Goal calls `Invoice.apply_payment`; it does **not** assign `invoice.status` or `invoice.balance`.

This tree must pass:

```bash
python3 tools/fitness-no-noun-field-writes.py examples/invoice-correct
```

Expected: `RESULT:MET`, exit 0.

Contrast: [`examples/invoice-violation/`](../invoice-violation/) must fail the same tool (pointed at that tree, or with no extra args that still scan it):

```bash
python3 tools/fitness-no-noun-field-writes.py examples/invoice-violation
```

Expected: `RESULT:NOT_MET`, exit 1. Do not “fix” the violation tree.
