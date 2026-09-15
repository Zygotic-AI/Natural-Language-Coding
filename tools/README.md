# Tools

Enforcement and scaffolding that make the charter real.

## Boundary contracts (P4 / R31 documentation)

| Tool | Input | Output | Failure mode |
|------|-------|--------|--------------|
| [`audit-binding-matrix.py`](audit-binding-matrix.py) | No argv. Reads `integrity/binding-matrix.json`, `CHARTER.md`, `integrity/PRINCIPLES.md`. | `A-BINDING-*:MET\|NOT_MET`, lists, `RESULT:MET\|NOT_MET`. | Exit **0** = MET; exit **1** = NOT_MET. |
| [`fitness-no-noun-field-writes.py`](fitness-no-noun-field-writes.py) | Optional argv roots; no args → hub ROOT. | `VIOLATION <path>:<line> <field>`; `RESULT:MET\|NOT_MET`. | Exit **0** = MET; exit **1** = NOT_MET. |
| [`fitness-verb-path.py`](fitness-verb-path.py) | Optional argv roots; no args → hub ROOT outside trees. | `VIOLATION <path>:<line> <kind>`; `RESULT:MET\|NOT_MET`. | Exit **0** = MET; exit **1** = NOT_MET. |
| [`assert-invoice-violation-fails.py`](assert-invoice-violation-fails.py) | Fixed tree `examples/invoice-violation/`. | `ASSERT:PASS` or `ASSERT:FAIL`. | Exit **0** = PASS; exit **1** = FAIL. |
| [`assert-verb-path-violation-fails.py`](assert-verb-path-violation-fails.py) | Fixed tree `examples/invoice-verb-path-violation/`. | `ASSERT:PASS` or `ASSERT:FAIL`. | Exit **0** = PASS; exit **1** = FAIL. |
| [`ci-fitness-check1.sh`](ci-fitness-check1.sh) | Repo root; check 1 only. | `CI:FAIL` or `CI:MET`. | Exit **0** = CI:MET; exit **1** = CI:FAIL. |
| [`fitness-quality-metric.py`](fitness-quality-metric.py) | `tools/fixtures/quality-metric/`. | `CHECK …`; `RESULT:MET\|NOT_MET`. | Exit **0** = MET; exit **1** = NOT_MET. |

## Fitness check 1 (R5 / C4)

**Gate for:** R5, C4 only. **Not a gate for:** R6, C5.

```bash
python3 tools/assert-invoice-violation-fails.py
python3 tools/fitness-no-noun-field-writes.py examples/invoice-correct
```

Do **not** “fix” `examples/invoice-violation/`.

## Verb-path v1 (R6 / C5 subset — not a matrix bind)

Fails persistence escapes in `goals/`, `adapters/`, and optional `workflows/` packaging: `.save(`, `.update(`, `.execute(`, `UPDATE <table>`, `INSERT INTO`, `DELETE FROM`, `setattr(`.

Does **not** fail `invoice.status =`. That is check 1.

```bash
python3 tools/assert-verb-path-violation-fails.py
python3 tools/fitness-verb-path.py examples/invoice-verb-path-violation   # NOT_MET
python3 tools/fitness-verb-path.py examples/invoice-correct               # MET
python3 tools/fitness-no-noun-field-writes.py examples/invoice-verb-path-violation  # MET
```

R6 and C5 stay **unbound**. This tool is a cousin of the statement, not the statement.

## Agent noun package validation

Required `AGENT.md` heading is `## Adjectives`. Legacy `## Invariants` still passes the structure checker.

```bash
python3 tools/validate-agent-noun-packages.py
python3 tools/fitness-agent-noun-structure.py
```

## Other planned tools

- Adjective locality (R24) — not field writes
- One-boundary / taint lifetime (A5)
- Broader escape hatches (A7) — this is how R6 grows past v1
- Contract presence / schema identity (R9–R11)
- Generated impact graphs (R21)
