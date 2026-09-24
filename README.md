# [Natural Language Coding](docs/TERMS.md#nlc)

**Describe outcomes and rules in plain language. Get a gated, boundary-shaped system, or a failed compile you can trust.**

- The AI [compiler](docs/TERMS.md#compiler) generates and audits your entire app, one increment at a time, from your natural language functionality descriptions, requirements, policies, and standards.
- Trace every [requirement](docs/TERMS.md#requirement) to where it is enforced—**when shipped**; see [jobs to be done](docs/JOBS-TO-BE-DONE.md) for what is available today vs not yet.
- [Ship](docs/TERMS.md#ship) only what you intended—multiple internal [audit](docs/TERMS.md#audit) points confirm what's intended is what's built, with final audits to certify the entire build.
- Easily update or add policies, standards, or even major technology—just update and recompile. (Swap AES-256 for AES-512, or GCP for AWS.)
- Stop silent drift - problems surface at compile time with evidence—or the build stops.
- The AI [compiler](docs/TERMS.md#compiler) eliminates costly models and hallucinations by producing tightly-scoped code.
- Code is interchangeable. Build Dev/QA rapidly in Python; deploy UAT and Prod in Rust.
- **Soft-green:** hub fitness / source-level gates are **Python-first** today; other languages are adapter-parked (`docs/LANGUAGE-SCANNER.md`), not complete.

## Quick start (app repo)

1. **Install** (macOS, Linux, WSL):

   ```bash
   curl -fsSL https://raw.githubusercontent.com/Zygotic-AI/Natural-Language-Coding/main/scripts/install.sh | bash
   ```

   Windows (PowerShell): [Getting started](docs/nlc/compiler/GETTING-STARTED.md) (install block).

   Then check the install: `nlc doctor` (or `./nlc doctor` if you only use a repo-local launcher).

2. **Create or open your [app repo](docs/TERMS.md#adopter)**

   - **New app:** `nlc new ~/projects/my-app --name MyApp` — scaffolds `./nlc`, [lock file](docs/TERMS.md#lock-file), and CI template.
   - **Existing code:** [Brownfield (beta)](docs/adoption/BROWNFIELD.md).
   - Open the repo in [Cursor](https://cursor.com) (Agent chat).

3. **Run `./nlc`** at the repo root. Read **YOUR QUEUE** and the short command map ([menu](docs/nlc/MENU.md)).

4. **`/interview`** — say what you are building; ratify goals, requirements, and knowledge. No product codegen in this step.

5. **`/planit`** — plan, bind, generate one piece at a time, [gate](docs/TERMS.md#gate), then **`./nlc verify-deep`** and **`./nlc verify`**.

6. **[Ship](docs/TERMS.md#ship)** is separate: human `Released-by:` on `CONFIRM.md`, then **`./nlc ship-check`**. Compile green is not release ([verify vs ship](docs/nlc/VERIFY-AND-SHIP.md)).

Stuck on [verify](docs/TERMS.md#verify)? Use **`/verify`** in the agent—not hand-edits to generated files.

## Human vs agent (one screen)

| You run | Agent runs |
| ------- | ---------- |
| `./nlc`, `./nlc verify`, `./nlc verify-deep`, `./nlc new`, `./nlc doctor`, `./nlc ship-check` | `/interview`, `/planit`, `/verify` |

Agents also run `./nlc maintainer …` (requirements sync, regen queue, before-generate). You do not need to memorize those—see [HARNESS.md](docs/nlc/HARNESS.md).

## Three layers

| Layer | You say | What it is |
| ----- | ------- | ---------- |
| **[NLC](docs/TERMS.md#nlc)** | [Natural Language Coding](docs/TERMS.md#nlc) | Intent in, compile or [refuse](docs/TERMS.md#refuse). |
| **[ASC](docs/TERMS.md#asc)** | [AI System Compiler](docs/TERMS.md#compiler) | `/interview` + `/planit` + gates in [`tools/`](tools/). |
| **[Compiled system](docs/TERMS.md#compiled-system)** | Your app tree | BBP-shaped code in *your* repo—not [`examples/`](examples/) (gate specimens only). |

Design SSOT: [`CHARTER.md`](CHARTER.md). Words: [`GLOSSARY.md`](docs/nlc/compiler/GLOSSARY.md).

## Go deeper

| If you want… | Read |
| ------------ | ---- |
| Five-minute walkthrough | [`GETTING-STARTED.md`](docs/nlc/compiler/GETTING-STARTED.md) |
| Why intent is the product | [`MANIFESTO.md`](MANIFESTO.md) → SSOT [`docs/nlc/compiler/MANIFESTO.md`](docs/nlc/compiler/MANIFESTO.md) |
| Adopt step-by-step | [`BOOTSTRAP.md`](docs/adoption/BOOTSTRAP.md) |
| Full doc map | [`docs/nlc/README.md`](docs/nlc/README.md) |

## Working on this [hub](docs/TERMS.md#hub) repo

Clone and `bash scripts/install.sh` (or `install.ps1`). [Hub](docs/TERMS.md#hub) compile [gate](docs/TERMS.md#gate):

```bash
python3 tools/ci_fitness.py
```

Windows: `powershell -File tools/ci-fitness.ps1`.

**[Ship](docs/TERMS.md#hub) version:** **`./release`** (one session; or **`./release prepare`** then **`./release finish`**) — [release guide](docs/adoption/RELEASE.md).

Install layout, version pins, and checksums: [`docs/nlc/README.md`](docs/nlc/README.md) (distribution section).

## Not for you if

- You want to hand-edit generated [noun](docs/TERMS.md#noun) code to stay green without changing intent.
- You need a finished low-code UI today—open gaps are in [`FINDINGS.md`](FINDINGS.md).
- You only want CI lint rules without goals, requirements, and verify/ship separation.

## Status

Working [charter](docs/TERMS.md#charter) and [hub](docs/TERMS.md#hub) gates. Not a ratified organizational standard. Adoption “done” is [charter](docs/TERMS.md#charter) §14.

**v0.1.0** — install, lock, [greenfield](docs/TERMS.md#greenfield) adopt, `/interview` + `/planit`, [verify](docs/TERMS.md#verify) path, impact graph + [delta-regen](docs/TERMS.md#delta-regen-queue). [Hub](docs/TERMS.md#hub) ships **no** product requirements (ADR 0016). **v0.2** — [requirement packs](docs/TERMS.md#requirement-pack). Gaps: [`FINDINGS.md`](FINDINGS.md).

**P / R / C** on [rule](docs/TERMS.md#rule) ids: **P**rinciple, **R**equirement, **C**onfirmation. Hyphenated `P-020` is operating policy in the companion bindings repo.
