# card-taint-violation

Known-fail fixture for A5 **v1**.

The goal reads `card_number` from the card noun and **returns** it. That is the
value leaving the consuming unit. The goal does not assign card fields and does
not copy a status machine.

```bash
python3 tools/fitness-taint-lifetime.py examples/card-taint-violation
```

Must be `RESULT:NOT_MET` (`return-taint:card_number`).

```bash
python3 tools/fitness-no-noun-field-writes.py examples/card-taint-violation
python3 tools/fitness-verb-path.py examples/card-taint-violation
python3 tools/fitness-adjective-locality.py examples/card-taint-violation
```

Must be MET. A5 ≠ R5 ≠ R6 ≠ R24.

Do not "fix" this tree.
