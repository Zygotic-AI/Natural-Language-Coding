# [Adopter repo](../../docs/TERMS.md#adopter)

This repository is a **[compiled system](../../docs/TERMS.md#compiled-system)** under [Natural Language Coding](../../docs/TERMS.md#nlc) (NLC).

- **[Charter](../../docs/TERMS.md#charter):** link or copy from [Natural-Language-Coding `CHARTER.md`](https://github.com/Zygotic-AI/Natural-Language-Coding/blob/main/CHARTER.md).
- **Intent:** `goals/`, `adrs/`, requirements prose, [knowledge domains](../../docs/TERMS.md#knowledge-domain).
- **Emit:** `domain/`, `goals/*/implementation*` — regenerate; do not patch to silence gates.

## [Verify](../../docs/TERMS.md#verify) and [ship](../../docs/TERMS.md#ship)

```bash
./nlc verify          # PR / fast gate — fingerprints in .nlc/verified.json
./nlc verify-deep     # main / after material compile — full gates + refresh fingerprints
./nlc ship-check      # human Released-by: when required
```

Commit **`.nlc/verified.json`** when `verify-deep` [MET](../../docs/TERMS.md#met) on main (or your release branch) so PR `verify` can compare fingerprints. CI template: `templates/adopter/github-workflows-nlc-verify.yml` (PR = `verify`; push to `main` = `verify-deep`).

[Prove](../../docs/TERMS.md#prove) PASS ≠ shipped. Add `Released-by:` per [hub](../../docs/TERMS.md#hub) `release-audit.py` / `CONFIRM.md`.

## Agent [workflow](../../docs/TERMS.md#workflow)

1. `/interview` — bind intent.
2. `/planit` — plan, bind, generate, [gate](../../docs/TERMS.md#gate), [prove](../../docs/TERMS.md#prove).

[Hub](../../docs/TERMS.md#hub) bootstrap guide: [docs/adoption/BOOTSTRAP.md](https://github.com/Zygotic-AI/Natural-Language-Coding/blob/main/docs/adoption/BOOTSTRAP.md).
