# Examples — specimens, not products

These trees exist so a [gate](../docs/TERMS.md#gate) has something to scan. They are not an invoice app.

| Tree | Designed red on |
|------|-----------------|
| [`invoice-correct/`](invoice-correct/) | none (also the generated-graph pass tree) |
| [`invoice-violation/`](invoice-violation/) | R5 field-writes |
| [`invoice-verb-path-violation/`](invoice-verb-path-violation/) | R6 verb-path |
| [`invoice-locality-violation/`](invoice-locality-violation/) | R24 locality |
| [`noun-inheritance-violation/`](noun-inheritance-violation/) | ADR 0008 noun inherits noun |
| [`rule-adoption-conflict/`](rule-adoption-conflict/) | ADR 0012 conflicting adoptions |
| [`c10-changed-out-of-scope/`](c10-changed-out-of-scope/) | ADR 0006 diff-scoped C10 |
| [`c21-changed-out-of-scope/`](c21-changed-out-of-scope/) | ADR 0006 diff-scoped C21 |
| [`card-taint-violation/`](card-taint-violation/) | R32 / C25 taint by name |
| [`card-taint-alias/`](card-taint-alias/) | R32 `n = get_number(); return n` |

| [`invoice-escape-hatch-violation/`](invoice-escape-hatch-violation/) | R33 / C26 escape |

| [`missing-contract/`](missing-contract/) | R9/R10 contracts |
| [`schema-identity-violation/`](schema-identity-violation/) | R11/C9 identity |
| [`duplicated-adjective-violation/`](duplicated-adjective-violation/) | C19 duplicated [adjective](../docs/TERMS.md#adjective) |
| [`extra-goal-entrypoint/`](extra-goal-entrypoint/) | R13 two entrypoints |
| [`impact-list-mismatch/`](impact-list-mismatch/) | C21 missing generated caller |
| [`verify-impact-c21/`](verify-impact-c21/) | `./nlc verify` ADR 0006 / C21 landmine |
| [`verify-breaking-accept/`](verify-breaking-accept/) | `./nlc verify` ADR 0006 acceptance landmine |
| [`verify-no-before-stamp/`](verify-no-before-stamp/) | `./nlc verify` missing UC18 stamp |
| [`verify-stale-stamp/`](verify-stale-stamp/) | `./nlc verify` stale before-generate stamp |
| [`verify-skill-ungated/`](verify-skill-ungated/) | `./nlc verify` gate-scoped SKILL without receipt |
| [`verify-produce-handoff/`](verify-produce-handoff/) | verify-deep incomplete produce package (SSOT) |
| [`verify-produce-self-audit/`](verify-produce-self-audit/) | verify-deep produce package self-audit roles (CS5) |
| [`regen-queue-pending/`](regen-queue-pending/) | open delta-regen queue on verify |
| [`rule-coverage-minimal/`](rule-coverage-minimal/) | ADR 0023 rule-coverage MET |
| [`rule-coverage-missing/`](rule-coverage-missing/) | ADR 0023 verify `rule_coverage_blockers` |
| [`adopter-verify-fast-green/`](adopter-verify-fast-green/) | ADR 0021/0023 adopter `verify_fast` MET |
| [`interview-packet-missing/`](interview-packet-missing/) | UC1 `./nlc verify` blocks missing interview-packet |
| [`rule-marker-domain/`](rule-marker-domain/) | ADR 0023 marker without gate-record |
| [`noun-without-tests/`](noun-without-tests/) | R25 no tests next to [noun](../docs/TERMS.md#noun) |
| [`adjective-untested/`](adjective-untested/) | C16 [adjective](../docs/TERMS.md#adjective) never named in tests |
| [`verb-untested/`](verb-untested/) | C17 verb never named in tests |
| [`verb-success-only/`](verb-success-only/) | C17 named, no failure-path test |

| [`goal-tests-copy-adjectives/`](goal-tests-copy-adjectives/) | C18 [goal](../docs/TERMS.md#goal) tests copy [noun](../docs/TERMS.md#noun) adjectives |
| [`goal-untested/`](goal-untested/) | C18 [goal](../docs/TERMS.md#goal) has code, no tests |

| [`missing-failure-mode/`](missing-failure-mode/) | P4/R31 failure mode |
| [`unversioned-contract/`](unversioned-contract/) | R12 schema has no version |
| [`missing-change-class/`](missing-change-class/) | C1 no [change class](../docs/TERMS.md#change-class) A–F |
| [`copied-goal-helper/`](copied-goal-helper/) | R15 helper copied into two goals |
| [`workflow-as-goal/`](workflow-as-goal/) | R17 workflows/ clones a [goal](../docs/TERMS.md#goal) |
| [`noun-retries/`](noun-retries/) | R18 retry loop on the [noun](../docs/TERMS.md#noun) |
| [`retrying-goal/`](retrying-goal/) | C15 retrying, verb not idempotent |
| [`retrying-no-key/`](retrying-no-key/) | C15 retrying, flag set, no key |
| [`adjectives-in-goal/`](adjectives-in-goal/) | C2 adjectives.txt under a [goal](../docs/TERMS.md#goal) |
| [`unsigned-class-a/`](unsigned-class-a/) | C24 class A, no ratification |
| [`orchestration-on-noun/`](orchestration-on-noun/) | C3/R3 Customer calls Invoice verb |
| [`stray-verb/`](stray-verb/) | R4 verb never touches adjectives |
| [`wrapper-goal/`](wrapper-goal/) | C13/R16 one-verb [goal](../docs/TERMS.md#goal), no I/O schemas |
| [`version-bump-no-adr/`](version-bump-no-adr/) | C10 version 2, no [ADR](../docs/TERMS.md#adr) |
| [`missing-c22/`](missing-c22/) | C22 no same-change line |
| [`c22-na-with-both/`](c22-na-with-both/) | C22 N/A with [charter](../docs/TERMS.md#charter) and code |
| [`open-findings/`](open-findings/) | C23 open FINDINGS.md checkbox |
| [`confirmer-open-fail/`](confirmer-open-fail/) | C23 [confirmer](../docs/TERMS.md#confirmer) FAIL unrebutted |


















[Hub](../docs/TERMS.md#hub) suite (every landmine still red; invoice-correct still green):

```bash
bash tools/ci-fitness.sh
```

```bash
python3 tools/generate-impact-graph.py examples/invoice-correct
python3 tools/assert-impact-graph-generated.py
```


Do not commit the JSON that command prints.

| [`changed-only-ok/`](changed-only-ok/) | C7/C11 CHANGED lists good; bad is dirty but out of scope |
| [`changed-missing-schema/`](changed-missing-schema/) | C7 CHANGED lists a [goal](../docs/TERMS.md#goal) with no schemas |
| [`product-no-confirm/`](product-no-confirm/) | C1 product tree, no CONFIRM.md |
| [`schema-field-missing/`](schema-field-missing/) | R20 required field absent from verb |
| [`schema-type-mismatch/`](schema-type-mismatch/) | R20 integer vs str |
| [`mention-only-verb/`](mention-only-verb/) | R4 string mention is not use |
| [`verb-no-preserve/`](verb-no-preserve/) | C17 no [adjective](../docs/TERMS.md#adjective) preservation |
| [`goal-test-no-call/`](goal-test-no-call/) | C18 test exists, never calls the [goal](../docs/TERMS.md#goal) |
| [`retrying-nested-no-key/`](retrying-nested-no-key/) | C15 nested parens, no key |
| [`retrying-key-unused/`](retrying-key-unused/) | C15 key passed, verb ignores it |
| [`retrying-nested-ok/`](retrying-nested-ok/) | C15 nested parens, verb honors key |
| [`schema-unannotated/`](schema-unannotated/) | R20 required field unannotated |
| [`imported-goal-helper/`](imported-goal-helper/) | R15 two goals import the same helper |
| [`card-taint-helper/`](card-taint-helper/) | R32 taint through a helper |
| [`sql-escape-hatch/`](sql-escape-hatch/) | R33 SQL execute in a [goal](../docs/TERMS.md#goal) |
| [`breaking-no-adr/`](breaking-no-adr/) | C10 version 1 dropped a required field |
| [`card-taint-crossfile/`](card-taint-crossfile/) | R32 taint through a helper in another file |
| [`class-c-on-charter/`](class-c-on-charter/) | C1 class C while [CHARTER](../docs/TERMS.md#charter).md is in the change |
| [`agent-ratified/`](agent-ratified/) | C24 [confirmer](../docs/TERMS.md#confirmer) signed [Ratified-by](../docs/TERMS.md#ratified-by) |
