# [ADR](../docs/TERMS.md#adr) 0023 — [Rule](../docs/TERMS.md#rule) instance trace (emit shape) and instant [audit](../docs/TERMS.md#audit) scope

- Status: Accepted
- Date: 2026-09-20
- Deciders: Human manager
- Class: F (process / enforcement trace)

## Context

Teams want **instant [audit](../docs/TERMS.md#audit)**: given an [ADR](../docs/TERMS.md#adr) range or a sensitivity [tag](../docs/TERMS.md#tag) (e.g. PCI `pan`), list where it is enforced (`{rule_id, goal, file, span, gate_id}`). Proposals included hand-maintained comments on every enforcement site and Hungarian `adr_pan_*` locals. Those improve readability only when humans maintain them; they do not survive [generate](../docs/TERMS.md#generate) unless the [compiler](../docs/TERMS.md#compiler) owns them and [fitness](../docs/TERMS.md#fitness) forbids drift.

[BBP](../docs/TERMS.md#bbp) already models sensitivity on **nouns/adjectives** in [IR](../docs/TERMS.md#rule-ir), not by renaming every local in every verb. [ADR 0007](0007-tags-primitives-reduced-adrs.md) binds tags and primitives; adopted rules SSOT maps [rule](../docs/TERMS.md#rule) rows to [ADR](../docs/TERMS.md#adr) ids.

**Instant [audit](../docs/TERMS.md#audit)** is a product promise. It must state what world it assumes.

## Decision

### 1. What instant [audit](../docs/TERMS.md#audit) assumes (normative)

Instant audit answers: *“Under the prescribed change path, is this ADR/tag enforced everywhere the [binding matrix](../docs/TERMS.md#binding-matrix) and adopted rules require?”*

**In scope:** Repositories where material changes to enforced surfaces run only through **prescribed** paths—[interview](../docs/TERMS.md#interview), [plan](../docs/TERMS.md#plan), [generate](../docs/TERMS.md#generate), regen, `./nlc` [verify](../docs/TERMS.md#verify), and bound skills/scripts/prompts. That is the same world [zero variance](../docs/TERMS.md#zero-variance) already describes for practice work.

**Out of scope (not a failure of instant audit):** Ad hoc hand edits outside that path. Consumer copy must not imply “audit still holds if someone patches generated files by hand.” That is outside the compile contract—caught by [verify](../docs/TERMS.md#verify) / regen refusal when the workflow is used, not by treating hand edits as a supported mode.

### 2. Traceability mechanics (not comments-as-SSOT)

| Mechanism | Use for | Do not use for |
| --------- | ------- | -------------- |
| [Tag](../docs/TERMS.md#tag) id (e.g. `pan`) in rules + adopted rules SSOT | [Rule](../docs/TERMS.md#rule) matching, ADR pointers, audit queries | Renaming every language local by hand |
| Schema / field names that encode sensitivity (`pan_last4`, `card_number_enc`) | API and goals | Replacing noun [adjectives](../docs/TERMS.md#adjective) |
| **Compiler-emitted** one-line [rule](../docs/TERMS.md#rule) receipt per enforcement block (machine-parseable, e.g. `nlc:rule=<id>`) | Enforcement inventory scan | Human-maintained comment essays |
| [Impact graph](../docs/TERMS.md#impact-graph) + goal-bindings | “These goals touch PCI-tagged nouns” | Line-perfect ADR map without regen |

**Rejected as primary enforcement:** comment-only markers; mandatory Hungarian `adr_pan_*` on every local unless the [compiler](../docs/TERMS.md#compiler) owns naming. Tags stay in [IR](../docs/TERMS.md#rule-ir) and adoption metadata; optional codegen style may align names when generation owns the file.

### 3. SSOT chain for “[ADR](../docs/TERMS.md#adr) set → everywhere”

1. [ADR](../docs/TERMS.md#adr) → [rule](../docs/TERMS.md#rule) ids in adopted rules (each row cites ADR id).
2. Nouns/adjectives carry tags in [IR](../docs/TERMS.md#rule-ir); lexicon locks tag names ([`integrity/LEXICON.md`](../integrity/LEXICON.md) / [`docs/TERMS.md`](../docs/TERMS.md)).
3. **On generate:** verb (or primitive) surface declares matched rules + tags; emit stable parseable marker per enforcement block where a binder exists.
4. **[Audit](../docs/TERMS.md#audit) tool:** `tools/nlc-rule-coverage.py` (name reserved)—input `adr:0012..0018` or `tag:pan` → output enforcement rows by scanning markers, schemas, tag/taint [fitness](../docs/TERMS.md#fitness), and impact graph—not grep for “PCI” in prose.

Hand-editing emitted markers or bodies without a matching plan receipt fails [gate](../docs/TERMS.md#gate) / [verify](../docs/TERMS.md#verify) when the prescribed path is used.

### 4. Fitness

Where markers are required, fitness **forbids** hand-edited receipts in generated surfaces (same class as “regen or refuse”). Until binders exist, [ADR](../docs/TERMS.md#adr) 0023 does not invent new **R** ids; reviewers use this [ADR](../docs/TERMS.md#adr) + [plan audit](../docs/TERMS.md#plan-audit) for PCI-range questions.

## Consequences

- Product language for “instant [audit](../docs/TERMS.md#audit)” cites this [ADR](../docs/TERMS.md#adr)’s assumption [boundary](../docs/TERMS.md#boundary).
- Implementation queue: emit shape in compiler/skills, then `nlc-rule-coverage.py`, then matrix binders as needed.
- PCI-range “show me every enforcement site” becomes one command **in the prescribed-change world**, not a comment-discipline exercise.

## Rejected

- **Comments as authoritative SSOT** for [rule](../docs/TERMS.md#rule) instances.
- **Hungarian locals as the retrieval key** instead of tagged nouns/schemas.
- **Instant [audit](../docs/TERMS.md#audit) that promises correctness after unscoped hand edits**—misleading; state the assumption instead.
