# USE-CASE proof index (machine SSOT)

Binder functions and proof commands are authoritative in [`integrity/uc-product-status.json`](../integrity/uc-product-status.json). This table is a human navigation aid.

| UC | Verify blockers (hub) | Maintainer / landmine |
| -- | --------------------- | --------------------- |
| UC1 | `interview_packet_blockers` | `validate-interview-packet.py`; `assert-interview-packet-fails` |
| UC3 | `proposed_adr_blockers`, `adr_traceability_blockers`, `interview_requirements_sync_blockers` | `assert-requirements-sync-pending-fails` |
| UC4 | `rule_ir_blockers`, `rule_runner_blockers` | `./nlc maintainer rule-runner`; `assert-rule-runner-fails`; `assert-rule-semantic-pan-fails` / `passes` |
| UC5 | `rule_apply_blockers`, `rule_coverage_blockers` | `./nlc maintainer rule-emit`; `assert-adopter-verify-fast-green-passes` |
| UC9 | `goal_bindings_narrow_blockers` | `assert-goal-bindings-narrow-fails`, `assert-delta-regen-narrow-passes`, `assert-delta-regen-orchestrate-passes`, `assert-verify-regen-queue-fails` |
| UC10 | `upstream_hand_patch_blockers` | `assert-upstream-hand-patch-fails` |
| UC13 | `durable_engine_blockers`, `durable_rule_blockers`, `engine_runtime_tag_strict_blockers` | `assert-durable-engine-rule-fails`, `assert-durable-engine-tag-strict-fails`, `assert-durable-engine-tag-strict-passes` |
| UC16 | `non_python_adapter_blockers` | `./nlc maintainer language-scan`; `assert-non-python-adapter-fails` |
| UC18 | `before_generate_stamp_blockers` | `./nlc maintainer guide before-generate` |
| UC20 | `call_tree_blockers`, `primitive_inventory_blockers` | `./nlc maintainer call-tree` |
| UC21 | `gate_record_blockers` | `./nlc maintainer gate-scope`, `gate-record` |

Expansion-only work (semantic ADR 0007 runners, per-stack call-tree packs, etc.) is listed under **Needed (expansion)** in [`USE-CASES.md`](USE-CASES.md).
