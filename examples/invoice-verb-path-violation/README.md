# invoice-verb-path-violation

Known-fail fixture for R6/C5 **v1**.

The goal does not assign `invoice.status`. Fitness check 1 (field writes) must
stay MET on this tree. The goal persists through a repository `.save()` and a
raw `UPDATE` instead of calling `apply_payment`.

```bash
python3 tools/fitness-verb-path.py examples/invoice-verb-path-violation
```

Must print `VIOLATION` lines for `goals/record-bank-payment/implementation.py`
and `RESULT:NOT_MET` (exit 1).

```bash
python3 tools/fitness-no-noun-field-writes.py examples/invoice-verb-path-violation
```

Must print `RESULT:MET` (exit 0). That is the point: R5 ≠ R6.

Do not "fix" this tree.
