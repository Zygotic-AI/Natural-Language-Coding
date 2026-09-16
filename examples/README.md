# Examples — specimens, not products

These trees exist so a gate has something to scan. They are not an invoice app.

| Tree | Designed red on |
|------|-----------------|
| [`invoice-correct/`](invoice-correct/) | none (also the generated-graph pass tree) |
| [`invoice-violation/`](invoice-violation/) | R5 field-writes |
| [`invoice-verb-path-violation/`](invoice-verb-path-violation/) | R6 verb-path |
| [`invoice-locality-violation/`](invoice-locality-violation/) | R24 locality |
| [`card-taint-violation/`](card-taint-violation/) | R32 / C25 taint |
| [`invoice-escape-hatch-violation/`](invoice-escape-hatch-violation/) | R33 / C26 escape |

| [`missing-contract/`](missing-contract/) | R9/R10 contracts |
| [`schema-identity-violation/`](schema-identity-violation/) | R11/C9 identity |
| [`duplicated-adjective-violation/`](duplicated-adjective-violation/) | C19 duplicated adjective |
| [`extra-goal-entrypoint/`](extra-goal-entrypoint/) | R13 two entrypoints |
| [`impact-list-mismatch/`](impact-list-mismatch/) | C21 missing generated caller |
| [`noun-without-tests/`](noun-without-tests/) | R25 no tests next to noun |
| [`adjective-untested/`](adjective-untested/) | C16 adjective never named in tests |
| [`verb-untested/`](verb-untested/) | C17 verb never named in tests |
| [`goal-tests-copy-adjectives/`](goal-tests-copy-adjectives/) | C18 goal tests copy noun adjectives |
| [`missing-failure-mode/`](missing-failure-mode/) | P4/R31 failure mode |
| [`unversioned-contract/`](unversioned-contract/) | R12 schema has no version |
| [`missing-change-class/`](missing-change-class/) | C1 no change class A–F |
| [`copied-goal-helper/`](copied-goal-helper/) | R15 helper copied into two goals |
| [`workflow-as-goal/`](workflow-as-goal/) | R17 workflows/ clones a goal |
| [`noun-retries/`](noun-retries/) | R18 retry loop on the noun |
| [`retrying-goal/`](retrying-goal/) | C15 retrying goal, verb not idempotent |
| [`adjectives-in-goal/`](adjectives-in-goal/) | C2 adjectives.txt under a goal |
| [`unsigned-class-a/`](unsigned-class-a/) | C24 class A, no ratification |
| [`orchestration-on-noun/`](orchestration-on-noun/) | C3/R3 Customer calls Invoice verb |














Hub suite (every landmine still red; invoice-correct still green):

```bash
bash tools/ci-fitness.sh
```

```bash
python3 tools/generate-impact-graph.py examples/invoice-correct
python3 tools/assert-impact-graph-generated.py
```


Do not commit the JSON that command prints.
