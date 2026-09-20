# Before generate (UC18)

Mandatory immediately **before PLANIT step 6** on any repo with a knowledge domain.

```bash
python3 tools/nlc-before-generate.py --repo <adopter-or-hub-root> --scope <noun-or-topic> ...
```

- Validates `knowledge/facts.json`.
- Runs steward **`load-knowledge-domain`** per scope (same as `tools/load-knowledge-domain.py`).
- **FAIL** (`BEFORE_GENERATE:NOT_MET`) → bind or interview; do not generate.

Name scopes from the plan (nouns, `pii`, `invoice`, etc.). Hub work on this repo: at least `--scope invoice` when invoice-shaped.

# After requirement / contract change (UC9 v2)

When an ADR, rule, or published verb contract changed, produce a regen checklist **before** editing emit:

```bash
python3 tools/nlc-delta-regen.py <repo-root> --change verb:Invoice.apply_payment
# or goal:… | noun:… | rule:…
```

Execute each row in the JSON `steps` via PLANIT 6 → 6.5, then prove.
