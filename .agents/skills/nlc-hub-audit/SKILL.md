# nlc-hub-audit

Formal review of this hub. Same path for every agent. Findings first; no blame.

Do not skip phases. If a phase cannot finish, record NOT_MET and stop that phase — do not invent coverage.

## Phase 0 — Recon

Read at HEAD: `CHARTER.md`, `adrs/README.md`, `docs/TERMS.md`, `FINDINGS.md`, `HOLES.md`, `TODO`, `docs/USE-CASES.md`, `integrity/uc-product-status.json`, `integrity/rule-corpus.json`, `docs/ADR-ENFORCEMENT.md`, `docs/ai-compiled-systems/MANIFESTO.md`, ADR 0024 and 0025.

Record SHA. Do not trust a prior agent report over the tree.

## Phase 1 — Belief vs implementation

For each belief in the manifesto (perfect code via process, no blame, climb upstream, buck stops here): name the ADR/rule/gate that binds it, or file a finding (unbound text).

## Phase 2 — Spine

Confirm the pipeline is the one in ADR 0024:

plan → atomic actions gated vs plan → bind ADRs to actions → reverse audit → emit+manifest → emit audit → bound-ADR gates (default-closed).

Emit must not select rules. NLC vs BBA only tags corpus.

## Phase 3 — Corpora

Every published R/C/P id is in `integrity/rule-corpus.json` as `nlc` or `bba`. One ADR list. Bind or remove.

## Phase 4 — Trackers

FINDINGS is the only live gap queue. HOLES historical. TODO is not a second queue. USE-CASES is narrative. Note contradictions as findings.

## Phase 5 — Dogfood

Hub process follows NLC. Hub *emit shape* (when it emits compiled-system code) follows BBA. Do not score the hub as a compiled system for product requirements (ADR 0016).

## Phase 6 — Report

List findings with: id, corpus, belief/principle disconnected, evidence path, suggested binder. No who.
