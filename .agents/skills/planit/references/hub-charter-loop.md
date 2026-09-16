# Hub charter agent loop (when this repo is in scope)

Normative source: [`CHARTER.md`](../../../../CHARTER.md) **§6** (steps 0–8).

AWL overlay: [`docs/ai-compiled-systems/PLANIT-ORCHESTRATION.md`](../../../../docs/ai-compiled-systems/PLANIT-ORCHESTRATION.md).

Use **in addition to** PLANIT when the outcome changes the practice hub (charter, integrity, agents, tools, ADRs, examples).

| Charter step | PLANIT alignment | Leaf skill |
|--------------|------------------|------------|
| 0 Load charter | PLANIT step 0 | — |
| 1 Classify A–F | Before ratified plan | — |
| 2 Propose (spec) | PLANIT 2–4 draft; no code | `bbp-proposer` (proposal only) |
| 2.5 Fitness preflight | Produce package complete | `tools/ci-fitness.sh` preflight rules in charter |
| 3 Adversarial review | Plan/bind audit + proposal review | `bbp-reviewer` |
| 4–5 Revise / ratify | Human or named gate | — |
| 6 Implement | PLANIT step 6 | `bbp-proposer` (implement) |
| 7 Confirm | PLANIT step 7 | `bbp-confirmer` |
| 8 Record | After prove PASS | `bbp-recorder` |

**Produce package (hub handoff):** classification, applicability, boundary I/O, self-adversarial notes, `ssot_leaf_ids` + `ssot_exit_status` per [`AGENTS.md`](../../../../AGENTS.md).

Short-form always-on rules: [`.agents/bbp-short-form.md`](../../../bbp-short-form.md).
