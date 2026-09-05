# Examples

Sample systems / fixtures for Boundary-Based Programming. These are small trees, not products.

| Tree | Role |
|------|------|
| [`invoice-violation/`](invoice-violation/) | Known-fail fixture: goal assigns noun fields |
| [`invoice-correct/`](invoice-correct/) | Known-pass fixture: goal calls `Invoice.apply_payment` |

## Fitness check 1

```bash
python3 tools/fitness-no-noun-field-writes.py examples/invoice-violation
```

→ `RESULT:NOT_MET`, exit 1

```bash
python3 tools/fitness-no-noun-field-writes.py examples/invoice-correct
```

→ `RESULT:MET`, exit 0

## Noun tests (invoice-correct)

```bash
python3 -m unittest examples/invoice-correct/domain/invoice/tests/test_invoice.py -v
```

Do not “fix” `examples/invoice-violation/`. That tree stays a deliberate violation.
