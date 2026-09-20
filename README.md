# Natural Language Coding

**Describe outcomes and rules in plain language—get a gated, boundary-shaped system, or a failed compile you can trust.**

Agents make one file green and fork the business rule next door. Natural Language Coding (NLC) stops that at the compile gate: you state **what** the software must do (goals) and **how** it must behave (requirements, ADRs, adopted rules, knowledge domains). The **compiler** emits and proves a **compiled system** in your repo—or refuses with evidence.

## How you work

1. **Install** the hub skills and tools (macOS, Linux, or WSL):

   ```bash
   curl -fsSL https://raw.githubusercontent.com/Zygotic-AI/Natural-Language-Coding/main/scripts/install.sh | bash
   ```

   Or clone this repo and run `bash scripts/install.sh` from the root.

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
| [`docs/spine/README.md`](docs/spine/README.md) | UC9 / UC14 / UC18 / UC19 tools |
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

**P / R / C** on rule ids: **P**rinciple, **R**equirement, **C**onfirmation. Hyphenated `P-020` is operating policy in the bindings companion repo.
