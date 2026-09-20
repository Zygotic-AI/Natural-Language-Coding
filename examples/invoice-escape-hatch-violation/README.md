# invoice-escape-hatch-violation

Known-fail fixture for A7 **v1**.

The [goal](../../docs/TERMS.md#goal) reaches through `invoice.__dict__` instead of calling a verb.
It does not assign `invoice.status` and does not call `.save(` / `setattr(`.

```bash
python3 tools/fitness-escape-hatch.py examples/invoice-escape-hatch-violation
```

Must be `RESULT:NOT_MET` (`dict-hatch`).

Do not "fix" this tree.
