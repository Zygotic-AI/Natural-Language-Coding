# [Verify](../TERMS.md#verify) and [ship](../TERMS.md#ship)

[NLC](../TERMS.md#nlc) separates **[verify](../TERMS.md#verify)** (machine gates on intent-bound artifacts) from **[ship](../TERMS.md#ship)** (human acceptance of release liability).

## [Adopter](../TERMS.md#adopter) commands

| When | Command | Pass means |
| ---- | ------- | ---------- |
| CI / before release artifact | `./nlc verify` | Fingerprints match `.nlc/verified.json`; pipeline blockers clear |
| After material change | `./nlc verify-deep` | Full gates + refresh fingerprints |
| Promotion | `./nlc ship-check` | Bundle check + human `Released-by:` when required |

On [verify](../TERMS.md#verify) failure: **`/verify`** in your agent — not a ping-pong of scripts.

## Default order

1. Generate one artifact (`/planit`).
2. [Gate](../TERMS.md#gate) that artifact immediately (ADR 0010).
3. **`./nlc verify-deep`** then **`./nlc verify`** on the tree.
4. Promotion gates on merge to main / QA.

## [Hub](../TERMS.md#hub) vs [app repo](../TERMS.md#adopter)

- **[Hub](../TERMS.md#hub)** — `verify-deep` runs `ci_fitness.py`.
- **[App repo](../TERMS.md#adopter)** — `verify-deep` runs `release-audit.py` on your tree (wire `./nlc verify` in CI; template `templates/adopter/github-workflows-nlc-verify.yml`).

[Verify](../TERMS.md#verify) PASS is compile-ready. [Ship](../TERMS.md#ship) needs human `Released-by:` on `CONFIRM.md` when your class requires it.

## Layers (ADR cross-walk)

| Layer | What | Tool |
| ----- | ---- | ---- |
| Compile | Per-artifact [gate](../TERMS.md#gate) + tree fitness | [ADR](../TERMS.md#adr) 0010, `gate-record`, [planit](../TERMS.md#planit) 6.5 |
| [Verify](../TERMS.md#verify) | Fingerprints + policy blockers | `./nlc verify` |
| [Verify-deep](../TERMS.md#verify-deep) | Full suite + produce / [change adversarial](../TERMS.md#change-adversarial) | `./nlc verify-deep`, `.nlc/produce-package.json` (hub) or `change-adversarial.json` + produce (app) |
| [Ship](../TERMS.md#ship) | Human release liability | `./nlc ship-check`, `Released-by:` |

Compile [MET](../TERMS.md#met) does not imply [ship](../TERMS.md#ship). See [`HUMAN-JUDGMENT-GATES.md`](HUMAN-JUDGMENT-GATES.md).
