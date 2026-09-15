# Tools

```bash
python3 tools/assert-invoice-violation-fails.py
python3 tools/assert-verb-path-violation-fails.py
python3 tools/assert-adjective-locality-violation-fails.py
python3 tools/assert-taint-violation-fails.py
python3 tools/assert-escape-hatch-violation-fails.py
```

| Tool | Proves | Leaves |
|------|--------|--------|
| field-writes | R5 assignment | hatches, taint return |
| verb-path | R6 v1 `.save(` / SQL / setattr | `__dict__` |
| adjective-locality | R24 tokens + field math | C19 spelling forks |
| taint-lifetime | A5 v1 return/store of taint | gateway dataflow |
| escape-hatch | A7 v1 `__dict__` / vars / exec / eval | ORM dialects |

A5 and A7 have no matrix id. R6 stays unbound. Flip `R24.binder` to locality.
