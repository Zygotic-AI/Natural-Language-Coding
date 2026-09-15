# Examples

Sample systems / fixtures for Boundary-Based Programming. These are small trees, not products.

| Tree | Role |
|------|------|
| [`invoice-violation/`](invoice-violation/) | Known-fail for R5/C4: goal assigns noun fields |
| [`invoice-correct/`](invoice-correct/) | Known-pass: goal calls `Invoice.apply_payment` |
| [`invoice-verb-path-violation/`](invoice-verb-path-violation/) | Known-fail for R6/C5 v1: goal persists without a verb, no field assign |

## Fitness check 1 (R5 / C4)

```bash
python3 tools/fitness-no-noun-field-writes.py examples/invoice-violation
```

→ `RESULT:NOT_MET`, exit 1

```bash
python3 tools/fitness-no-noun-field-writes.py examples/invoice-correct
python3 tools/fitness-no-noun-field-writes.py examples/invoice-verb-path-violation
```

→ `RESULT:MET`, exit 0 on both. The verb-path fixture has no field writes.

## Verb-path v1 (R6 / C5 subset)

```bash
python3 tools/assert-verb-path-violation-fails.py
python3 tools/fitness-verb-path.py examples/invoice-verb-path-violation
```

→ assert PASS; fitness `RESULT:NOT_MET`

```bash
python3 tools/fitness-verb-path.py examples/invoice-correct
python3 tools/fitness-verb-path.py examples/invoice-violation
```

→ `RESULT:MET` on both. Field writes are R5, not this tool.

## Noun tests (invoice-correct)

```bash
python3 -m unittest examples/invoice-correct/domain/invoice/tests/test_invoice.py -v
```

Do not “fix” the `*-violation/` trees.
