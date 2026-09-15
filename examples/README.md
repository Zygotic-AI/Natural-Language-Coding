# Examples

| Tree | Role |
|------|------|
| [`invoice-violation/`](invoice-violation/) | R5 field assign |
| [`invoice-correct/`](invoice-correct/) | known-pass + contract files |
| [`invoice-verb-path-violation/`](invoice-verb-path-violation/) | R6 persist without verb |
| [`invoice-locality-violation/`](invoice-locality-violation/) | R24 copied adjective |
| [`card-taint-violation/`](card-taint-violation/) | A5 taint return |
| [`invoice-escape-hatch-violation/`](invoice-escape-hatch-violation/) | A7 `__dict__` |
| [`missing-contract/`](missing-contract/) | R9/R10 v1 no schema files |

```bash
python3 tools/assert-contract-presence-fails.py
python3 tools/fitness-contract-presence.py examples/invoice-correct
```

Do not “fix” the `*-violation/` or `missing-contract/` trees.
