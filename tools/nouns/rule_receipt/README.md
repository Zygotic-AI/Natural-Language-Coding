# RuleReceipt (hub X4 pilot)

BBA noun for compiler-owned `nlc:rule=` receipts and rule-IR snapshot materialization (ADR 0023).

Hub CLI adapters (thin boundaries):

- `tools/nlc_rule_marker.py`
- `tools/nlc_rule_coverage.py`
- `tools/nlc_rule_runner.py`
- `tools/nlc_rule_emit.py`

Mutation of receipt text / IR snapshot goes through public verbs on `RuleReceipt` only.
