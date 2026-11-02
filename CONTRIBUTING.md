# Contributing

The [README](README.md) is for people who **use** published [Natural Language Compiler](docs/TERMS.md#nlc) in their own app repos. This page is for changing **this** repository — the compiler, its gates, and its docs.

Fork, make a focused change, and open a pull request. That part is ordinary.

What is not ordinary is the bar. This tree is process engineering with AI: stated intent is compiled into gated work, or the compile **refuses**. A change that skips the process (silent patches, unbound new surfaces, “we’ll add the why later”) does not fit here, even if the code runs.

## What we look for

- **Intent first.** Say what must stay true. Then change the code. Do not edit generated output to quiet a gate.
- **A home for the change.** New lasting behavior belongs on a [goal](docs/TERMS.md#goal), a decision record ([ADR](docs/TERMS.md#adr)), a [rule](docs/TERMS.md#rule), or a [type recipe](docs/TERMS.md#type-recipe) — not a one-off script with no why.
- **Complete or refused.** Incomplete packets do not pass. There is no soft pass.
- **Role language** on lasting surfaces (no person names).

The machine and document gate is [`integrity/CONTRIBUTION.md`](integrity/CONTRIBUTION.md). How to add a content type: [`content-types/HOW-TO-ADD.md`](content-types/HOW-TO-ADD.md). Standing rules: [`CHARTER.md`](CHARTER.md). If an agent is doing the work: [`AGENTS.md`](AGENTS.md).

## Check the change

```bash
python3 tools/ci_fitness.py
```

Windows: `powershell -File tools/ci-fitness.ps1`.

Hub versions ship with **`./release`** ([release guide](docs/adoption/RELEASE.md)), not ad-hoc tags.

Install layout and checksums: [`docs/nlc/README.md`](docs/nlc/README.md) (distribution section).
