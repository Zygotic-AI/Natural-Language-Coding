# Examples — specimens, not products

These trees exist so a gate has something to scan. They are not an invoice app.

| Tree | Designed red on |
|------|-----------------|
| [`invoice-correct/`](invoice-correct/) | none (also the generated-graph pass tree) |
| [`invoice-violation/`](invoice-violation/) | R5 field-writes |
| [`invoice-verb-path-violation/`](invoice-verb-path-violation/) | R6 verb-path |
| [`invoice-locality-violation/`](invoice-locality-violation/) | R24 locality |
| [`card-taint-violation/`](card-taint-violation/) | A5 taint |
| [`invoice-escape-hatch-violation/`](invoice-escape-hatch-violation/) | A7 escape |
| [`missing-contract/`](missing-contract/) | R9/R10 contracts |
| [`schema-identity-violation/`](schema-identity-violation/) | R11/C9 identity |
| [`duplicated-adjective-violation/`](duplicated-adjective-violation/) | C19 duplicated adjective |
| [`extra-goal-entrypoint/`](extra-goal-entrypoint/) | R13 two entrypoints |
| [`impact-list-mismatch/`](impact-list-mismatch/) | C21 missing generated caller |
| [`noun-without-tests/`](noun-without-tests/) | R25 no tests next to noun |
| [`missing-failure-mode/`](missing-failure-mode/) | P4/R31 failure mode |




Hub suite (every landmine still red; invoice-correct still green):

```bash
bash tools/ci-fitness.sh
```

```bash
python3 tools/generate-impact-graph.py examples/invoice-correct
python3 tools/assert-impact-graph-generated.py
```


Do not commit the JSON that command prints.
