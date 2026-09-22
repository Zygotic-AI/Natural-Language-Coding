# A-S7

- [Requirement](../../docs/TERMS.md#requirement): `S7`
- Outcome: **[met](../../docs/TERMS.md#met)** | **not [met](../../docs/TERMS.md#met)** only

## Statement

Produce→fitness [handoff](../../docs/TERMS.md#handoff) is [default-closed](../../docs/TERMS.md#default-closed). Produce completion requires change artifacts AND [produce package](../../docs/TERMS.md#produce-package). Without a complete package, fitness preflight returns `handoff_refused`; content scoring does not open.

## Binary criteria

[Met](../../docs/TERMS.md#met) iff:
1. [Charter](../../docs/TERMS.md#charter) §6 Step 2 states [produce package](../../docs/TERMS.md#produce-package) is required for [handoff](../../docs/TERMS.md#handoff)
2. [Charter](../../docs/TERMS.md#charter) §6 Step 2.5 defines fitness preflight that returns `handoff_refused` for incomplete packages
3. Fitness does not open content scoring on incomplete handoffs
4. `handoff_refused` is distinct from fitness FAIL

Not [met](../../docs/TERMS.md#met) if:
- Produce can claim ready without package
- Fitness soft-fails or discovers missing packages instead of refusing
- Content scoring opens without preflight pass

## Evidence

On [met](../../docs/TERMS.md#met) or not [met](../../docs/TERMS.md#met), cite:
- [Charter](../../docs/TERMS.md#charter) §6 Step 2 (produce package requirement)
- [Charter](../../docs/TERMS.md#charter) §6 Step 2.5 (fitness preflight)
- [Agent noun](../../docs/TERMS.md#agent-noun) `quality-architect` preflight-fitness-handoff verb output [contract](../../docs/TERMS.md#contract)
