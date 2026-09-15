# Tools

```bash
python3 tools/assert-invoice-violation-fails.py
python3 tools/assert-verb-path-violation-fails.py
python3 tools/assert-adjective-locality-violation-fails.py
python3 tools/assert-taint-violation-fails.py
```

| Tool | Proves | Does not prove |
|------|--------|----------------|
| field-writes | R5 / C4 assignment | verb path, copied adjectives, taint return |
| verb-path | R6/C5 v1 `.save(` / SQL | every mutation is a verb |
| adjective-locality | R24 named tokens + field math | C19 different spelling |
| taint-lifetime | A5 v1 `return` / store of taint tokens | value never reaches a gateway |

R6/C5 and A5 stay unbound (A5 has no matrix row).
R24 should use `fitness-adjective-locality.py` as its binder.
