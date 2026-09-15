# invoice-locality-violation

Known-fail fixture for R24 **v1**.

The goal calls `apply_payment`. It does not assign noun fields. Fitness check 1
must stay MET. The goal *reimplements* the void-invoice adjective by comparing
`status == "void"` and doing money math on `balance` before calling the verb.

```bash
python3 tools/fitness-adjective-locality.py examples/invoice-locality-violation
```

Must be `RESULT:NOT_MET`.

```bash
python3 tools/fitness-no-noun-field-writes.py examples/invoice-locality-violation
python3 tools/fitness-verb-path.py examples/invoice-locality-violation
```

Must both be `RESULT:MET`. R24 ≠ R5 ≠ R6.

Do not "fix" this tree.
