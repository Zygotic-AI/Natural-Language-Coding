# invoice-locality-violation

Known-fail fixture for R24 **v1**.

The [goal](../../docs/TERMS.md#goal) calls `apply_payment`. It does not assign [noun](../../docs/TERMS.md#noun) fields. Fitness check 1
must stay [MET](../../docs/TERMS.md#met). The [goal](../../docs/TERMS.md#goal) *reimplements* the void-invoice [adjective](../../docs/TERMS.md#adjective) by comparing
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
