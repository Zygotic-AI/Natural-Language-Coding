# ADR enforcement

Every **Accepted** [ADR](../adrs/README.md) must map to **runnable** binders (tools, `./nlc verify` blockers, CI landmines, or prescribed skills)—not prose alone.

**Status SSOT:** checklist in repo [`TODO`](../TODO) (ADR enforcement section). This file holds the per-ADR table; **bound** means hub compile CI proves the binder set (meta-fitness + landmines), not that every adopter runtime path is complete.

| ADR | Must be enforced by (target) | Status |
| --- | --- | --- |
| 0001 | `fitness-adr-0001-binder.py` + `assert-binding-matrix-met.py` | bound |
| 0002 | `fitness-p2-hub-scope.py` + `assert-p2-hub-scope-passes.py` | bound |
| 0003 | `fitness-agent-noun-structure` + landmines | bound |
| 0004 | `fitness-adr-0004-0005-binder.py` + produce/verify-deep landmines | bound |
| 0005 | (with 0004) SSOT + `fitness-produce-ssot-binder.py` + quality fixtures | bound |
| 0006 | contract_change on non-specimen adopters + diff-scoped C10/C21 + `fitness-verify-pipeline-wired` + landmines | bound |
| 0007 | compiler applies rule IR on generate (full runner) | **gap** (v1: [`nlc_rule_runner.py`](../tools/nlc_rule_runner.py) + `rule-emit`; landmine `assert-rule-runner-fails.py`; semantic apply = expansion) |
| 0008 | `fitness-adr-0008-binder.py` + specimen + invoice-correct MET landmine | bound |
| 0009 | verb → primitive inventory gate | **gap** (v1: [`nlc_call_tree.py`](../tools/nlc_call_tree.py) + verify; multi-language packs = expansion) |
| 0010 | `fitness-adr-0010-binder.py` + gate landmines | bound |
| 0011 | `fitness-nlc-naming.py` + landmine | bound |
| 0012 | `check-rule-adoption.py` + conflict landmine | bound |
| 0013 | `hub_tool` fitness + landmine | bound |
| 0014 | migration + `assert-release-preflight-passes.py` | bound |
| 0015 | `fitness-distribution-binder.py` + install landmines | bound |
| 0016 | `fitness-hub-no-product-requirements.py` + landmine | bound |
| 0017–0018 | `fitness-human-surface-binder.py` + interview landmines | bound |
| 0019 | `fitness-guide-orchestration.py` + landmine | bound |
| 0020 | (with 0017–0018) MENU/HARNESS + dashboard fitness | bound |
| 0021 | `nlc verify` / `verify-deep` | bound |
| 0022 | `./release`, release workflow, preflight | bound |
| 0023 | `rule_coverage_blockers` + `nlc_rule_emit.py` + binder fitness + landmines | bound |
| 0024 | `fitness-adr-0024-binder.py` + `nlc-action-plan-gate.py` + `nlc-reverse-audit.py` + `nlc-emit-manifest-enforce.py` (ADR 0026) | bound |
| 0025 | `rules/nlc-0025.json` + binder (v1: existence + fields) | bound |
| 0026 | `nlc-action-plan-gate.py` + `nlc-reverse-audit.py` + `nlc-emit-manifest-enforce.py` + specimens + fitness wrappers | bound |

**0007/0009 gap:** full semantic rule runners and per-language call-tree packs are not MET; v1 binders are `rule-runner`, `rule-emit`, and `call-tree`. ADR 0023 marker emit is bound via `rule-emit` / `goal-scaffold` / verify audit.

**Specimens:** `product_tree.is_specimen` skips `CONFIRM` requirements and **ADR 0006** `contract_change_blockers` unless the README includes `contract-change applies` (see `product_tree.contract_change_applies`).

Update this table when hub binder coverage changes.
