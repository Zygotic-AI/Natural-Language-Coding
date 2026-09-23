# [Hub](../../../../docs/TERMS.md#hub) [charter](../../../../docs/TERMS.md#charter) agent loop (when this repo is in scope)

Normative source: [`CHARTER.md`](../../../../CHARTER.md) **§6** (steps 0–8).

[AWL](../../../../docs/TERMS.md#awl) overlay: [`docs/nlc/compiler/PLANIT-ORCHESTRATION.md`](../../../../docs/nlc/compiler/PLANIT-ORCHESTRATION.md).

Use **in addition to** [PLANIT](../../../../docs/TERMS.md#planit) when the outcome changes the practice [hub](../../../../docs/TERMS.md#hub) (charter, integrity, agents, tools, ADRs, examples).

| [Charter](../../../../docs/TERMS.md#charter) step | [PLANIT](../../../../docs/TERMS.md#planit) alignment | Leaf skill |
|--------------|------------------|------------|
| 0 Load [charter](../../../../docs/TERMS.md#charter) | [PLANIT](../../../../docs/TERMS.md#planit) step 0 | — |
| 1 Classify A–F | Before ratified plan | — |
| 2 Propose (spec) | [PLANIT](../../../../docs/TERMS.md#planit) 2–4 draft; no code | `bbp-proposer` (proposal only) |
| 2.5 Fitness preflight | [Produce package](../../../../docs/TERMS.md#produce-package) complete | `tools/ci-fitness.sh` preflight rules in [charter](../../../../docs/TERMS.md#charter) |
| 3 Adversarial review | Plan/bind [audit](../../../../docs/TERMS.md#audit) + proposal review | `bbp-reviewer` |
| 4–5 Revise / ratify | Human or named [gate](../../../../docs/TERMS.md#gate) | — |
| 6 Implement | [PLANIT](../../../../docs/TERMS.md#planit) step 6 | `bbp-proposer` (implement) |
| 7 Confirm | [PLANIT](../../../../docs/TERMS.md#planit) step 7 (compile) | `bbp-confirmer` — `ci-fitness.sh` + §11. Not [ship](../../../../docs/TERMS.md#ship). |
| 8 Record | After [prove](../../../../docs/TERMS.md#prove) PASS | `bbp-recorder` |
| [Ship](../../../../docs/TERMS.md#ship) | After human `Released-by:` | `python3 tools/release-audit.py <tree>` |


**[Produce package](../../../../docs/TERMS.md#produce-package) (hub handoff):** classification, applicability, [boundary](../../../../docs/TERMS.md#boundary) I/O, self-adversarial notes, `ssot_leaf_ids` + `ssot_exit_status` per [`AGENTS.md`](../../../../AGENTS.md).

Short-form always-on rules: [`.agents/bbp-short-form.md`](../../../bbp-short-form.md).
