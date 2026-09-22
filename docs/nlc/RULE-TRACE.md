# Rule instance trace (ADR 0023)

Adopted [rules](../../docs/TERMS.md#rule) must appear as compiler-style receipts in code: `# nlc:rule=<rule_id>` (or `//` for JS/TS).

## Emit (generate)

- `./nlc maintainer rule-marker --id <rule_id> [--lang python|js|ts]`
- `./nlc maintainer goal-scaffold --goal <id>` — seeds markers for adopted rules
- `./nlc maintainer rule-emit --goal <id>` — compiler-owned sync after generate (inserts missing markers)
- [Planit](../../.agents/skills/planit/SKILL.md) step 6 + [bbp-proposer](../../.agents/skills/bbp-proposer/SKILL.md)

## Audit

- `./nlc maintainer rule-coverage [--adr <id>] [--tag <t>] [--check]`
- **`./nlc verify`** (fast) calls `rule_coverage_blockers` when `rules/adopted.json` and `goals/` or `domain/` exist

## Gate

Files with `nlc:rule=` markers require a PASS [gate record](GATE-RECORD-BINDER.md) after generate. See [`HARNESS.md`](HARNESS.md).

## Brownfield (UC15)

After `./nlc maintainer brownfield-inventory` (or `python3 tools/nlc-brownfield-inventory.py <root>`), add goals with `./nlc maintainer goal-scaffold --goal <id>` before bulk legacy migration.

Specimens:

- [`rule-coverage-minimal/`](../../examples/rule-coverage-minimal/) — markers present
- [`rule-coverage-missing/`](../../examples/rule-coverage-missing/) — verify blocks on missing markers
- [`adopter-verify-fast-green/`](../../examples/adopter-verify-fast-green/) — **`verify_fast`** green (stamp + gate + markers + `.nlc/verified.json`)
