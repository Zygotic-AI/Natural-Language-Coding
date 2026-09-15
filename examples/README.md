# Examples

Sample systems / fixtures for Boundary-Based Programming. These are small trees, not products.

| Tree | Role |
|------|------|
| [`invoice-violation/`](invoice-violation/) | Known-fail for R5/C4: goal assigns noun fields |
| [`invoice-correct/`](invoice-correct/) | Known-pass: goal calls `Invoice.apply_payment` |
| [`invoice-verb-path-violation/`](invoice-verb-path-violation/) | Known-fail for R6/C5 v1: persist without a verb |
| [`invoice-locality-violation/`](invoice-locality-violation/) | Known-fail for R24: copies void/money-math, still calls the verb |

R5 ≠ R6 ≠ R24. Each fail fixture is MET on the other two tools.

```bash
python3 tools/assert-invoice-violation-fails.py
python3 tools/assert-verb-path-violation-fails.py
python3 tools/assert-adjective-locality-violation-fails.py
```

Do not “fix” the `*-violation/` trees.
