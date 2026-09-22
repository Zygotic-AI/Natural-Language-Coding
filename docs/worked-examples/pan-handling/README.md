# Worked example: PAN handling (shape only)

Illustrates [ADR](../../TERMS.md#adr) 0007 path: **[ADR](../../TERMS.md#adr) → adopted rules → tags on adjectives → emit obligations**. Not a [hub](../../TERMS.md#hub) [requirement](../../TERMS.md#requirement), not PCI certification — adopters bring their own packs (ADR 0016).

## UC3 — Decision (ADR)

See [`adrs/0007-tags-primitives-reduced-adrs.md`](../../../adrs/0007-tags-primitives-reduced-adrs.md). The [ADR](../../TERMS.md#adr) is the *why*; rules are the *what the [compiler](../../TERMS.md#compiler) runs*.

## UC4 — Adopt rules

Machine file: [`integrity/examples/pan-rules-adopted.json`](../../../integrity/examples/pan-rules-adopted.json).

```bash
python3 tools/check-rule-adoption.py integrity/examples/pan-rules-adopted.json
# ADOPTION:MET
```

True conflict (same tier, forbid vs must on `pan|return`) — fails until human override:

```bash
python3 tools/check-rule-adoption.py integrity/examples/pan-rules-conflict.json
# ADOPTION:NOT_MET — record winner in integrity/precedence-overrides.json
```

Precedence tiers: [ADR](../../TERMS.md#adr) 0012, [`integrity/adr-precedence.json`](../../../integrity/adr-precedence.json).

**Not a conflict:** `must encrypt` on `write` and `forbid` on `return` — different match keys. **Not a conflict:** regulatory `forbid return` vs org `must encrypt` on `write` — different primitives.

## UC5 — Tags and emit

1. Mark adjectives with [tag](../../TERMS.md#tag) `pan` in [noun](../../TERMS.md#noun) IR (`examples/invoice-correct/domain/invoice/` — teaching [specimen](../../TERMS.md#specimen)).
2. Verbs declare primitives per [ADR](../../TERMS.md#adr) 0009; undeclared interior I/O fails gates.
3. v1 Python stand-in: `taint.txt` + [`tools/fitness-taint-lifetime.py`](../../../tools/fitness-taint-lifetime.py) enforces lifetime rules aligned with `pan-no-return` / `pan-no-log`.

## [Knowledge domain](../../TERMS.md#knowledge-domain) (UC18)

Facts: [`knowledge/facts.json`](../../../knowledge/facts.json) (`KF-pan-scope`). Validate:

```bash
python3 tools/validate-knowledge-facts.py .
```

## Change [blast radius](../../TERMS.md#blast-radius) (UC9)

After changing a verb [contract](../../TERMS.md#contract):

```bash
python3 tools/nlc-delta-regen.py examples/invoice-correct --change verb:Invoice.apply_payment
```

Use the JSON plan as the [PLANIT](../../TERMS.md#planit) regen checklist; [prove](../../TERMS.md#prove) the tree when done.
