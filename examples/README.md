# Examples — specimens, not products

These trees exist so a gate has something to scan. They are not an invoice app.
The rules apply to any noun. Invoice and card are just the teaching objects.

| Tree | Designed red on | Must be green on the other gates |
|------|-----------------|----------------------------------|
| [`invoice-correct/`](invoice-correct/) | none | all |
| [`invoice-violation/`](invoice-violation/) | R5 field-writes | R24, R6, R9, A5, A7 |
| [`invoice-verb-path-violation/`](invoice-verb-path-violation/) | R6 verb-path | the others |
| [`invoice-locality-violation/`](invoice-locality-violation/) | R24 locality | the others |
| [`card-taint-violation/`](card-taint-violation/) | A5 taint | the others |
| [`invoice-escape-hatch-violation/`](invoice-escape-hatch-violation/) | A7 escape | the others |
| [`missing-contract/`](missing-contract/) | R9/R10 contracts | the others |
