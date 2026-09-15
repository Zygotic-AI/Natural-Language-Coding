# missing-contract

Known-fail fixture for R9 / R10 / C7 / C8 **v1**.

A goal and a noun exist. Schema files do not. The code can even call a verb;
that does not count as a contract.

```bash
python3 tools/fitness-contract-presence.py examples/missing-contract
```

Must print `missing-goal-input`, `missing-goal-output`, `missing-noun-verbs-schema`
and `RESULT:NOT_MET`.

Do not "fix" this tree.
