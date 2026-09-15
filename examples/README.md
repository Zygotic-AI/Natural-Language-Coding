# Examples

Small trees, not products.

| Tree | Role |
|------|------|
| [`invoice-violation/`](invoice-violation/) | R5/C4 field assign |
| [`invoice-correct/`](invoice-correct/) | known-pass verb call |
| [`invoice-verb-path-violation/`](invoice-verb-path-violation/) | R6/C5 v1 persist without verb |
| [`invoice-locality-violation/`](invoice-locality-violation/) | R24 copied adjective |
| [`card-taint-violation/`](card-taint-violation/) | A5 v1 taint return |
| [`invoice-escape-hatch-violation/`](invoice-escape-hatch-violation/) | A7 v1 `.__dict__` |

```bash
python3 tools/assert-invoice-violation-fails.py
python3 tools/assert-verb-path-violation-fails.py
python3 tools/assert-adjective-locality-violation-fails.py
python3 tools/assert-taint-violation-fails.py
python3 tools/assert-escape-hatch-violation-fails.py
```

Do not “fix” the `*-violation/` trees.
