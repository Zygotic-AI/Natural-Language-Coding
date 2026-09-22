# Before generate (UC18)

Mandatory immediately **before [PLANIT](../../../../docs/TERMS.md#planit) step 6** on any repo with a [knowledge domain](../../../../docs/TERMS.md#knowledge-domain).

```bash
./nlc maintainer guide before-generate --scope <noun-or-topic> ...
```

- Validates `knowledge/facts.json`.
- Runs steward **`load-knowledge-domain`** per scope (same as `tools/load-knowledge-domain.py`).
- **FAIL** (`BEFORE_GENERATE:NOT_MET`) → bind or [interview](../../../../docs/TERMS.md#interview); do not generate.

Name scopes from the plan (nouns, `pii`, `invoice`, etc.). [Hub](../../../../docs/TERMS.md#hub) work on this repo: at least `--scope invoice` when invoice-shaped.

# After [requirement](../../../../docs/TERMS.md#requirement) / [contract](../../../../docs/TERMS.md#contract) change (UC9)

```bash
python3 tools/nlc-delta-regen.py . --change verb:Noun.verb --orchestrate --write-queue
```

Execute each `DELTA_REGEN:STEP` via [Planit](../../../../docs/TERMS.md#planit); [gate](../../../../docs/TERMS.md#gate) after every generate (ADR 0010).

# Before generate (UC18)

When an [ADR](../../../../docs/TERMS.md#adr), [rule](../../../../docs/TERMS.md#rule), or [published verb contract](../../../../docs/TERMS.md#published-verb-contract) changed, produce a regen checklist **before** editing emit:

```bash
python3 tools/nlc-delta-regen.py <repo-root> --change verb:Invoice.apply_payment
# or goal:… | noun:… | rule:…
```

Execute each row via `./nlc maintainer regen-continue`, [PLANIT](../../../../docs/TERMS.md#planit) 6 → 6.5, `./nlc maintainer regen-advance`, then `./nlc verify-deep`.
