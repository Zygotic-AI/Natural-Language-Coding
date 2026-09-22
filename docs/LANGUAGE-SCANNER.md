# [Code packs](TERMS.md#code-pack) — language scanner spec

**[Code packs](TERMS.md#code-pack) (UC16):** per-stack source adapters for the same [charter](TERMS.md#charter) gates. **v1 product:** `./nlc maintainer language-scan` inventories languages; ACS source enforcement stays **Python-only** until step 2 below ships.

The **runner** may stay Python (`python3 tools/…`). That is a toolchain [rule](TERMS.md#rule).
The **[charter](TERMS.md#charter) sentences** (field writes, taint, verb signatures, helpers) are not
Python. v1 gates mostly match Python-shaped source. A second language without
a spec will fork the [charter](TERMS.md#charter): one scanner will have the bug, another will not.

## Order (mandatory)

1. Write the **spec** (this file, expanded). Language-agnostic.
2. From that spec, write the **adapter** for the new language.
3. Do **not** copy `tools/fitness-*.py` and regex-port them.

Contracts, CONFIRM.md, schemas, matrix, `release-audit.py` human gates stay
one suite. They already do not care about language.

## What the spec must contain before any adapter ships

- Split: **contract/IR checks** (one suite) vs **source-matches-IR** (thin adapter).
- For each source-level promise (today: R4, R5/field-writes, R15, R20, R32, C15,
  R33/escape, C3/noun-calls-noun, R18): the designed-fail [specimen](TERMS.md#specimen) *shape*
  (not Python), the designed-pass shape, exit codes, `RESULT:MET|NOT_MET`.
- A shared invoice-shaped product tree in the new language that must [MET](TERMS.md#met) the
  same ids `examples/invoice-correct/` mets.
- Landmine assert: `assert-*-fails` equivalent, exit 0 while the landmine is live.
- Explicit non-goals: do not re-specify C1/C22/C23/C24/C10/H-RELEASE here.

## Adapter fitness (when someone does step 2)

The adapter is done when:

1. Every source-level id in the spec has a red [specimen](TERMS.md#specimen) and a green [specimen](TERMS.md#specimen).
2. [Hub](TERMS.md#hub) `ci-fitness.sh` (or a sibling job) runs those landmines.
3. `release-audit.py` still runs the same human gates on CONFIRM.md.

Until then, [ACS](TERMS.md#acs) source enforcement is **Python-only**. Say that. Do not claim
language-agnostic *gates*.
