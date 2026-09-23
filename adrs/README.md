# ADRs

Architecture Decision Records for this practice and for example systems that need recorded decisions.

Naming: `NNNN-short-slug.md`. Superseded ADRs are marked superseded, not deleted (charter R22).

Deciders are role names (CG-R4). Person-to-role mapping lives outside SSOT.

| [ADR](../docs/TERMS.md#adr) | Title | Status |
|-----|-------|--------|
| [`0001-zero-variance-integrity.md`](0001-zero-variance-integrity.md) | [Zero-variance](../docs/TERMS.md#zero-variance) [integrity](../docs/TERMS.md#integrity), [binding matrix](../docs/TERMS.md#binding-matrix), binary audits | Accepted |
| [`0002-p2-scope.md`](0002-p2-scope.md) | Scope of P2 | Accepted |
| [`0003-systems-extension-agent-nouns.md`](0003-systems-extension-agent-nouns.md) | Systems extension: [agent nouns](../docs/TERMS.md#agent-noun) | Accepted |
| [`0004-produce-fitness-handoff.md`](0004-produce-fitness-handoff.md) | Produce→fitness [handoff](../docs/TERMS.md#handoff) [default-closed](../docs/TERMS.md#default-closed) | Accepted |
| [`0005-ssot-exit-evidence.md`](0005-ssot-exit-evidence.md) | [SSOT exit evidence](../docs/TERMS.md#ssot-exit-evidence) in produce packages | Accepted |
| [`0006-contract-change-notice.md`](0006-contract-change-notice.md) | How loud a published-contract change is | Accepted |
| [`0007-tags-primitives-reduced-adrs.md`](0007-tags-primitives-reduced-adrs.md) | Tags, primitives, reduced ADRs | Accepted |
| [`0008-no-noun-inheritance.md`](0008-no-noun-inheritance.md) | Nouns do not inherit nouns | Accepted |
| [`0009-primitive-interior-functions.md`](0009-primitive-interior-functions.md) | Primitives are interior functions | Accepted |
| [`0010-gate-after-every-generate.md`](0010-gate-after-every-generate.md) | [Gate](../docs/TERMS.md#gate) immediately after every generate | Accepted |
| [`0011-natural-language-coding-naming.md`](0011-natural-language-coding-naming.md) | [NLC](../docs/TERMS.md#nlc) product naming (compiler vs compiled system) | Accepted |
| [`0012-adr-precedence-and-rule-conflicts.md`](0012-adr-precedence-and-rule-conflicts.md) | [ADR](../docs/TERMS.md#adr) precedence tiers and adopt-time [rule](../docs/TERMS.md#rule) conflicts | Accepted |
| [`0013-requirements-preflight.md`](0013-requirements-preflight.md) | Requirements checked at entry; list all missing | Accepted |
| [`0014-semver-upgrade-steps-and-noop-migrations.md`](0014-semver-upgrade-steps-and-noop-migrations.md) | Semver upgrade chain; explicit noop migrations and UPGRADE:* logs | Accepted |
| [`0015-distribution-lock-and-version-store.md`](0015-distribution-lock-and-version-store.md) | [Version store](../docs/TERMS.md#version-store), `.nlc/lock.json`, tarball install, two layouts | Accepted |
| [`0016-hub-carries-no-product-requirements.md`](0016-hub-carries-no-product-requirements.md) | [Hub](../docs/TERMS.md#hub) has no built-in compliance; [UC19](../docs/TERMS.md#uc19) retired; packs v0.2 | Accepted |
| [`0017-human-command-surface.md`](0017-human-command-surface.md) | Human surface: jargon-free UX, menu/order, agent bridge (all adopters paths) | Accepted |
| [`0018-human-cli-interview-on-gap.md`](0018-human-cli-interview-on-gap.md) | [Interview](../docs/TERMS.md#interview) on gap/failure for all human surfaces (scripts, tools, prompts) | Accepted |
| [`0019-guided-orchestration.md`](0019-guided-orchestration.md) | Guided flow: queue, resume unfinished work | Accepted |
| [`0020-human-vs-agent-commands.md`](0020-human-vs-agent-commands.md) | Human shell vs agent-invoked tools (requirements/build) | Accepted |
| [`0021-verify-fast-and-deep.md`](0021-verify-fast-and-deep.md) | `./nlc verify` fingerprints; `verify-deep`; `/verify` skill | Accepted |
| [`0022-hub-release-fail-early.md`](0022-hub-release-fail-early.md) | `./release` preflight, notes [gate](../docs/TERMS.md#gate) before [verify](../docs/TERMS.md#verify), [tag](../docs/TERMS.md#tag) baseline | Accepted |
| [`0023-rule-instance-trace-and-instant-audit-scope.md`](0023-rule-instance-trace-and-instant-audit-scope.md) | [Compiler](../docs/TERMS.md#compiler) [rule](../docs/TERMS.md#rule) receipts, instant [audit](../docs/TERMS.md#audit) scope (prescribed path only) | Accepted |
| [`0024-nlc-factory-spine.md`](0024-nlc-factory-spine.md) | [NLC](../docs/TERMS.md#nlc) factory spine: corpora, bind-or-remove, action bind, emit audit | Accepted |
| [`0025-belief-no-blame-climb.md`](0025-belief-no-blame-climb.md) | Belief: no blame, climb upstream, buck stops here | Accepted |
| [`0026-promote-x1-x3-runners.md`](0026-promote-x1-x3-runners.md) | Promote X1–X3 expansion runners to law | Accepted |
| [`0030-pipeline-wiring.md`](0030-pipeline-wiring.md) | Sequence X1/X2/X3/X5/X6 around every emit via `nlc-pipeline-wire.py` | Accepted |
