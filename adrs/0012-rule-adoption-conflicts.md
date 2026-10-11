# [ADR](../docs/TERMS.md#adr) 0012 — [ADR](../docs/TERMS.md#adr) precedence and [rule](../docs/TERMS.md#rule) adoption conflicts

- Status: Accepted
- Date: 2026-09-20
- Deciders: Human manager
- Class: F (process)

## Context

Adopted rules (if/thens) can overlap on the same tagged [primitive](../docs/TERMS.md#primitive). Not every overlap is a conflict: `must encrypt` and `must not store plaintext` often compose. **[UC14](../docs/TERMS.md#uc14)** is not “encrypt vs cannot store.”

Real conflicts appear when two adopted obligations on the **same match** cannot both hold—for example `pan ∧ return → forbid` and `pan ∧ return → must` (export to processor).

Not all ADRs are equal. Regulatory and charter-grade decisions outrank local product ADRs unless a human records an explicit override.

## Decision

1. **Precedence tiers** (high to low): `charter` → `regulatory` → `org` → `project` → `local`. Config SSOT: [`integrity/adr-precedence.json`](../integrity/adr-precedence.json).

2. Each adopted [rule](../docs/TERMS.md#rule) cites an **[ADR](../docs/TERMS.md#adr) id** and **precedence_tier** (and optional **precedence_rank** within tier).

3. **Automatic resolution:** when rules share the same match key (`tags` + `primitive`) and effects conflict, the higher tier wins; within tier, higher `precedence_rank` wins.

4. **Human resolution:** when tier and rank tie and effects still conflict, adoption **fails closed** until [`integrity/precedence-overrides.json`](../integrity/precedence-overrides.json) names the winning `rule_id` with `decided_by` and `date`.

5. **Adopt-time [gate](../docs/TERMS.md#gate):** `python3 tools/check-rule-adoption.py <rules-file>` runs before rules are marked in force. Emit-time application is unchanged (ADR 0007).

## Consequences

- [`docs/USE-CASES.md`](../docs/USE-CASES.md) [UC14](../docs/TERMS.md#uc14) row uses a true conflict example, not encryption vs storage policy.
- [`tools/check-rule-adoption.py`](../tools/check-rule-adoption.py) enforces tiers and overrides.

## Rejected

- **Prompt negotiation** at emit time for conflicting adopted rules.
- **All ADRs equal** — org policy cannot silently trump regulatory tier.
