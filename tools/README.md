# Tools

Enforcement and scaffolding that make the charter real.

## Boundary contracts (P4 / R31 documentation)

| Tool | Input | Output | Failure mode |
|------|-------|--------|--------------|
| [`audit-binding-matrix.py`](audit-binding-matrix.py) | No argv. Reads `integrity/binding-matrix.json`, `CHARTER.md`, `integrity/PRINCIPLES.md`. | `A-BINDING-*:MET\|NOT_MET`, `MISSING_FROM_MATRIX`, `MISSING_AUDIT_ID`, `UNBOUND`, `IN_FORCE_UNBINDABLE`, `RESULT:MET\|NOT_MET`. | Exit **0** = MET/PASS; exit **1** = NOT_MET/FAIL. No silent exception swallow. |
| [`fitness-no-noun-field-writes.py`](fitness-no-noun-field-writes.py) | Optional argv roots; no args → hub `ROOT` (`domain/`, `goals/`, `workflows/`, `adapters/`, `examples/**`). | `VIOLATION <path>:<line> <field>`; `RESULT:MET\|NOT_MET`. | Exit **0** = MET/PASS; exit **1** = NOT_MET/FAIL. No silent exception swallow. |
| [`assert-invoice-violation-fails.py`](assert-invoice-violation-fails.py) | No argv. Fixed tree `examples/invoice-violation/`. | `VIOLATION …`, `RESULT:…`, `ASSERT:PASS` or `ASSERT:FAIL …`. | Exit **0** = ASSERT:PASS; exit **1** = ASSERT:FAIL. No silent exception swallow. |
| [`ci-fitness-check1.sh`](ci-fitness-check1.sh) | No argv. Repo root; assert gate + each `examples/*/` except `invoice-violation`. | Section banners; child stdout; `CI:FAIL …` or `CI:MET`. | Exit **0** = CI:MET/PASS; exit **1** = CI:FAIL. Child failures not swallowed. |

These docstring/header contracts are documentation for P4/R31. **P4/R31 stay unbound** until a fail-capable checker exists for the contract text itself.

| Tool | Role |
|------|------|
| [`audit-binding-matrix.py`](audit-binding-matrix.py) | Binary audits `A-BINDING-COVERAGE`, `A-BINDING-UNBOUND`, `A-BINDING-PROMOTE`; lists offenders; exit 1 on not met |
| [`fitness-no-noun-field-writes.py`](fitness-no-noun-field-writes.py) | Fitness check 1 (charter §12.1 / R5 / C4): fail if goals/workflows/adapters assign a noun field |
| [`assert-invoice-violation-fails.py`](assert-invoice-violation-fails.py) | Known-fail gate: exit 0 only if the invoice-violation fixture still fails check 1 |
| [`ci-fitness-check1.sh`](ci-fitness-check1.sh) | Hub CI wrapper: fixture gate + non-fixture trees must pass |

## Fitness check 1

**Binder for:** R5, C4 only. **Not a binder for:** R6, C5, contracts, workflows-as-law, P2, P4, R31.

Noun modules live under `domain/<noun>/` (and under an example root the same way). Goals, workflows, and adapters live under `goals/`, `workflows/`, `adapters/`. The tool fails if a file in those outside trees assigns to a field declared on a noun.

Field declaration v1: `fields.txt` in the noun dir, or inferred from assignments inside the noun’s own sources. Prints `VIOLATION <path>:<line> <field>` then `RESULT:NOT_MET` or `RESULT:MET`.

### Required hub commands

```bash
# 1) Known-fail fixture gate — must exit 0 (meaning the example still fails check 1)
python3 tools/assert-invoice-violation-fails.py

# 2) Fitness check on any other example tree — must be MET (exit 0)
python3 tools/fitness-no-noun-field-writes.py examples/<other-example>
```

| Command | Required outcome |
|---------|------------------|
| `assert-invoice-violation-fails.py` | Exit **0**: fixture is NOT_MET and at least one `VIOLATION` cites `goals/record-bank-payment/`. Exit **1** if the example is clean (checker dead or example “fixed”). |
| `fitness-no-noun-field-writes.py` on any other `examples/*/` tree | Exit **0** (`RESULT:MET`). Do not point this at `examples/invoice-violation/`. |

Do **not** “fix” `examples/invoice-violation/` to make check 1 green.

### Other invocations

```bash
# Whole hub (includes known-fail fixture → typically NOT_MET)
python3 tools/fitness-no-noun-field-writes.py

# Explicit fixture scan (expect NOT_MET; prefer assert-invoice-violation-fails.py in CI)
python3 tools/fitness-no-noun-field-writes.py examples/invoice-violation
```

Two-invocation wrapper (uses the assert gate + non-fixture MET scans):

```bash
bash tools/ci-fitness-check1.sh
```

## Agent noun package validation

Validates that agent noun packages under `agents/<name>/` have:
- `AGENT.md` with required sections (Identity, Invariants, Handoff-in, Completion artifact, Success criteria)
- `verbs.md` where every verb declares Input contract, Output contract, and Failure mode (per S2 / R31)

| Tool | Input | Output | Failure mode |
|------|-------|--------|--------------|
| [`validate-agent-noun-packages.py`](validate-agent-noun-packages.py) | Optional argv = specific agent names; no args → scans all `agents/*/` | `PACKAGE:<name>:VALID\|INVALID`, `AGENT_MISSING_SECTION`, `VERB_MISSING_*`, `RESULT:MET\|NOT_MET`. | Exit **0** = MET/PASS; exit **1** = NOT_MET/FAIL. No silent exception swallow. |

### Commands

```bash
# Validate all agent noun packages
python3 tools/validate-agent-noun-packages.py

# Validate specific agent nouns
python3 tools/validate-agent-noun-packages.py quality-architect adversarial-auditor
```

### Machine-readable verb schemas

Agent noun verb contracts may also have machine-readable JSON Schema definitions under `agents/<name>/schemas/`. See [`agents/quality-architect/schemas/verbs.schema.json`](../agents/quality-architect/schemas/verbs.schema.json) for example.

## Other planned tools

- Fitness checks for import boundaries and law locality
- A checker that fails when a listed public tool lacks Input/Output/Failure mode (would bind P4/R31)
- Generators for impact / dependency views from code (not hand-maintained JSON)
