# [Gate record](../TERMS.md#gate-record) binder (R27 / ADR 0010)

**[Requirement](../TERMS.md#requirement):** [ADR](../TERMS.md#adr) 0010 — no new **R** id until a binder can show metrics were named and the [gate](../TERMS.md#gate) ran after generate.

## Binder surface

| Piece | Role |
| ----- | ---- |
| [`tools/nlc_gate_record.py`](../../tools/nlc_gate_record.py) | Appends PASS receipts to `.nlc/gate-records.json` |
| [`tools/nlc_compliance.py`](../../tools/nlc_compliance.py) `gate_record_blockers` | `verify` fails when `goals/**/implementation.py` is newer than last PASS for that path |
| [Planit](../TERMS.md#planit) step 6.5 | Names `gate_id` + fitness command **before** generate; records PASS after |
| [`tools/assert-verify-gate-record-fails.py`](../../tools/assert-verify-gate-record-fails.py) | CI landmine on `examples/goal-untested` |

## [Gate](../TERMS.md#gate) ids (examples)

Use stable ids that match the plan row / fitness script name:

- `ci_fitness` — [hub](../TERMS.md#hub) tree [prove](../TERMS.md#prove)
- `fitness-<name>` — per-specimen or per-goal metric (e.g. `fitness-r4`)
- `skill-gate` — leaf skill [Gate](../TERMS.md#gate) table row id when emitting skills

`gate_id` is opaque to [verify](../TERMS.md#verify) except for storage; **artifact path** is what compliance compares to `implementation.py` mtime.

## CLI

```bash
./nlc maintainer gate-record --artifact goals/foo/implementation.py --gate-id fitness-r4 --command "python3 tools/fitness-r4.py ..."
python3 tools/nlc_gate_record.py --describe   # print this binding summary
```

## Matrix

[ADR](../TERMS.md#adr) 0010 consequence references R27. When a new **R** row is added for per-generate gating, point `binder` at `tools/nlc_gate_record.py` and [audit](../TERMS.md#audit) `gate_record_blockers` in `nlc_compliance.py`.
