# Adopter repo

This repository is a **compiled system** under Natural Language Coding (NLC).

- **Charter:** link or copy from [Natural-Language-Coding `CHARTER.md`](https://github.com/Zygotic-AI/Natural-Language-Coding/blob/main/CHARTER.md).
- **Intent:** `goals/`, `adrs/`, requirements prose, knowledge domains (interview shelf).
- **Emit:** `domain/`, `goals/*/implementation*` — regenerate; do not patch to silence gates.

## Prove and ship

```bash
bash /path/to/nlc-hub/tools/ci-fitness.sh    # or your bound fitness suite
python3 /path/to/nlc-hub/tools/release-audit.py .
```

Prove PASS ≠ shipped. Add `Released-by:` per hub `release-audit.py`.

## Agent workflow

1. `/interview` — bind intent.
2. `/planit` — plan, bind, generate, gate, prove.

Hub bootstrap guide: [docs/adoption/BOOTSTRAP.md](https://github.com/Zygotic-AI/Natural-Language-Coding/blob/main/docs/adoption/BOOTSTRAP.md).
