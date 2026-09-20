# Natural Language Coding

**Describe outcomes and rules in plain language—get a gated, boundary-shaped system, or a failed compile you can trust.**

Agents make one file green and fork the business rule next door. Natural Language Coding (NLC) stops that at the compile gate: you state **what** the software must do (goals) and **how** it must behave (requirements, ADRs, adopted rules, knowledge domains). The **compiler** emits and proves a **compiled system** in your repo—or refuses with evidence.

## How you work

1. **Install** the hub skills and tools:

   **macOS, Linux, or WSL:**

   ```bash
   curl -fsSL https://raw.githubusercontent.com/Zygotic-AI/Natural-Language-Coding/main/scripts/install.sh | bash
   ```

   **Windows (PowerShell):**

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
   irm https://raw.githubusercontent.com/Zygotic-AI/Natural-Language-Coding/main/scripts/install.ps1 | iex
   ```

   Or clone this repo and run `bash scripts/install.sh` or `powershell -File scripts/install.ps1` from the root. Hub lands under `%USERPROFILE%\.local\share\nlc\` (versioned store + `hub` pointer; same layout on Unix). Remote install pulls the latest **semver release** (override with `NLC_VERSION`); verify uses [`integrity/nlc-install-hashes.json`](integrity/nlc-install-hashes.json) unless `NLC_SKIP_VERIFY=1`. App repos pin hub via [`.nlc/lock.json`](integrity/schemas/nlc-lock.schema.json); upgrade with `tools/nlc-update.py` (ADR 0014–0015).

   **Prove (compile)** from the hub root:

   ```bash
   python3 tools/ci_fitness.py
   ```

   Windows: `python tools\ci_fitness.py` or `powershell -File tools\ci-fitness.ps1`.

2. **Greenfield app repo** (preferred):

   ```bash
   python3 ~/.local/share/nlc/hub/tools/nlc-init.py ~/projects/my-app --name MyApp
   ```

   Brownfield existing code: [beta guide](docs/adoption/BROWNFIELD.md).

3. **Open the app repo** in [Cursor](https://cursor.com) (Agent chat).

4. Run **`/interview`** until goals, requirements, and knowledge domains are bound.

5. Run **`/planit`** to plan, bind, generate one artifact at a time, gate, and prove.

Compile green is not release. Ship requires human `Released-by:` per [`tools/release-audit.py`](tools/release-audit.py).

## Three layers

| Layer | You say | What it is |
| ----- | ------- | ---------- |
| **NLC** | Natural Language Coding | The product: intent in, compile or refuse. |
| **Compiler** | AI system compiler | PLANIT + agent harness + [`tools/`](tools/) gates. |
| **Compiled system** | Your app tree | BBP-shaped code in *your* repo—not [`examples/`](examples/) (those are gate specimens). |

Under the covers: boundary-based architecture ([`CHARTER.md`](CHARTER.md)). Glossary: [`docs/ai-compiled-systems/GLOSSARY.md`](docs/ai-compiled-systems/GLOSSARY.md).

## Start here

| Artifact | Role |
| -------- | ---- |
| [`docs/ai-compiled-systems/GETTING-STARTED.md`](docs/ai-compiled-systems/GETTING-STARTED.md) | Install, `/interview`, `/planit`, fitness |
| [`docs/ai-compiled-systems/MANIFESTO.md`](docs/ai-compiled-systems/MANIFESTO.md) | Why intent is the product |
| [`docs/adoption/BOOTSTRAP.md`](docs/adoption/BOOTSTRAP.md) | Adopt NLC in a new app repo (UC15) |
| [`docs/nlc/README.md`](docs/nlc/README.md) | Doc map (start here for navigation) |
| [`docs/spine/README.md`](docs/spine/README.md) | UC9 / UC14 / UC18 tools |
| [`CHARTER.md`](CHARTER.md) | Design rules (adopters) |
| [`docs/USE-CASES.md`](docs/USE-CASES.md) | What the practice does |
| [`FINDINGS.md`](FINDINGS.md) | Open product gaps |
| [`TODO`](TODO) | Hub task queue |

## Not for you if

- You want to hand-edit generated noun code to stay green without changing intent.
- You need a finished low-code UI today—several compile-spine use-cases are still open ([`FINDINGS.md`](FINDINGS.md)).
- You only want CI lint rules without goals, requirements, and prove/ship separation.

## Status

Working charter and hub gates. Not a ratified organizational standard. Adoption “done” is charter §14.

**v0.1.0 (first release)** — greenfield adopt, install, lock, `/interview` + `/planit`, impact graph + delta-regen orchestration, UC14/UC18 spine. Hub ships **no** product requirements (ADR 0016). **v0.2** — requirement packs. See [`FINDINGS.md`](FINDINGS.md). Pre-tag: `bash scripts/nlc-release-prep.sh`.

**P / R / C** on rule ids: **P**rinciple, **R**equirement, **C**onfirmation. Hyphenated `P-020` is operating policy in the bindings companion repo.
