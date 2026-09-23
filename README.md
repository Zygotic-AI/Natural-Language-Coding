# Natural Language Coding (NLC)

**NLC is the product.** You describe what the system must do and what it must never do, in plain language. The compiler either emits a gated system that traces back to that intent, or it refuses. A red compile is a success: the fork was caught before it shipped.

Code is the object file. Goals, requirements, and knowledge are the source.

**BBA** (Boundary-Based Architecture) and **BBP** (Boundary-Based Programming) are *inside* NLC — the shape and integrity rules the compiler must emit. They are not the product name.

## If you want the specifics later

| You want… | Read |
| --------- | ---- |
| The thesis | [`MANIFESTO.md`](MANIFESTO.md) |
| Confirmable rules | [`CHARTER.md`](CHARTER.md) |
| Word meanings | [`docs/TERMS.md`](docs/TERMS.md) |
| Honest “works today / not yet” | [`docs/JOBS-TO-BE-DONE.md`](docs/JOBS-TO-BE-DONE.md) |
| Numbered compiler stories | [`docs/USE-CASES.md`](docs/USE-CASES.md) |
| Human command menu | [`docs/nlc/MENU.md`](docs/nlc/MENU.md) |
| Full doc map | [`docs/nlc/README.md`](docs/nlc/README.md) |
| Adopt an existing repo | [`docs/adoption/BROWNFIELD.md`](docs/adoption/BROWNFIELD.md) |
| Verify vs ship | [`docs/nlc/VERIFY-AND-SHIP.md`](docs/nlc/VERIFY-AND-SHIP.md) |
| Open gaps | [`FINDINGS.md`](FINDINGS.md) |

You do not need those pages to start.

---

## Use it

### 1. Install

macOS / Linux / WSL:

```bash
curl -fsSL https://raw.githubusercontent.com/Zygotic-AI/Natural-Language-Coding/main/scripts/install.sh | bash
nlc doctor
```

Windows (PowerShell):

```powershell
Set-ExecutionPolicy -Scope Process Bypass -Force
irm https://raw.githubusercontent.com/Zygotic-AI/Natural-Language-Coding/main/scripts/install.ps1 | iex
nlc doctor
```

If you only have a repo-local launcher, use `./nlc doctor`.

### 2. Open an app repo

- **New:** `nlc new ~/projects/my-app --name MyApp` — lock file, `./nlc`, CI template.
- **Existing code:** [Brownfield (beta)](docs/adoption/BROWNFIELD.md).
- Open the repo in Cursor (Agent chat). Full adopt walkthrough: [BOOTSTRAP.md](docs/adoption/BOOTSTRAP.md).

### 3. See your queue

From the app repo root:

```bash
./nlc
```

Read **YOUR QUEUE** and the command map.

### 4. Bind intent — `/interview`

In the agent: **`/interview`**.

Say the outcome. Ratify goals, requirements, and knowledge. Do not generate product code in this step. Stop when gaps are closed or explicitly waived.

### 5. Compile one piece — `/planit`

In the agent: **`/planit`**.

Plan → bind → generate **one** artifact → gate. Then:

```bash
./nlc verify-deep
./nlc verify
```

If verify fails, use **`/verify`** in the agent. Do not hand-edit generated files to go green.

### 6. Ship (separate from compile)

Compile green is not release.

1. Human `Released-by:` on `CONFIRM.md`.
2. `./nlc ship-check`.

Details: [verify vs ship](docs/nlc/VERIFY-AND-SHIP.md).

---

## What you run vs what the agent runs

| You run | Agent runs |
| ------- | ---------- |
| `./nlc`, `nlc new`, `nlc doctor` | `/interview` |
| `./nlc verify`, `./nlc verify-deep` | `/planit` |
| `./nlc ship-check` | `/verify` |

Agents also run `./nlc maintainer …` (requirements sync, regen queue, before-generate). You do not need those commands. See [HARNESS.md](docs/nlc/HARNESS.md).

---

## What you use it for

These are the jobs NLC is built to do. Status is honest: **available** means you can run it on an adopter repo today.

| Job | You get | Status |
| --- | ------- | ------ |
| Policy into code | Standards → ADRs → rules → markers → gates | Available (v1) |
| Outcome in, spec out | Interview until goals and facts are bound; no silent scope | Available |
| Named goal you can audit | Behavior traces to a goal and a plan | Available |
| Change one rule, not the world | Delta-regen of the affected blast radius | Available (v1) |
| Catch rule fights before code | Conflicting adopted rules fail at adopt-time | Available |
| Prove before ship | `verify` green, then a human release step | Available |
| Fix upstream, not the object file | Red gate → interview / ADR / rule / regen | Available |
| Greenfield app quickly | Install, lock, scaffold, menu | Available |
| Upgrade the hub | Lock + migration chain | Available |
| Bring your own requirements | Requirement packs (install + ratify in *your* repo) | Available (v1) |
| Size a tech change | Who is hit before you swap a runtime or interior | Blocked (adapters still expanding) |

Full narrative + mechanism map: [JOBS-TO-BE-DONE.md](docs/JOBS-TO-BE-DONE.md). Compiler IDs (UC1–UC21): [USE-CASES.md](docs/USE-CASES.md).

---

## How the pieces fit (one screen)

| Name | Role |
| ---- | ---- |
| **NLC** | The product. Intent in; compile or refuse. |
| **Compiler** (`/interview` + `/planit` + `tools/`) | Turns bound intent into a compiled system. |
| **Compiled system** | Your app repo. Not `examples/` (those are gate specimens). |
| **BBP** | Emit *practice*: nouns own adjectives; verbs mutate; goals orchestrate. |
| **BBA** | Emit *architecture* + hub integrity under NLC. Not the public name. |

Design rules: [`CHARTER.md`](CHARTER.md). Short word list: [`GLOSSARY.md`](docs/nlc/compiler/GLOSSARY.md).

Soft-green today: hub fitness is **Python-first**. Other languages are inventoried, not fully adapted ([LANGUAGE-SCANNER.md](docs/LANGUAGE-SCANNER.md)).

---

## Not for you if

- You want to hand-edit generated noun code to stay green without changing intent.
- You need a finished low-code UI today — gaps live in [`FINDINGS.md`](FINDINGS.md).
- You only want CI lint, with no goals, requirements, or verify/ship split.

## Status

Working charter and hub gates. Not a ratified organizational standard. Adoption “done” is charter §14.

**v0.1.0** — install, lock, greenfield adopt, `/interview` + `/planit`, verify path, impact graph + delta-regen. This hub ships **no** product requirements (no PCI/HIPAA built-in; ADR 0016). **v0.2** — requirement packs. Gaps: [`FINDINGS.md`](FINDINGS.md).

**P / R / C** on rule ids: **P**rinciple, **R**equirement, **C**onfirmation. Hyphenated `P-020` is operating policy in the companion bindings repo.

---

## Working on this hub

Clone, then `bash scripts/install.sh` (or `install.ps1`). Hub compile gate:

```bash
python3 tools/ci_fitness.py
```

Windows: `powershell -File tools/ci-fitness.ps1`.

Ship a hub version with **`./release`** ([release guide](docs/adoption/RELEASE.md)). Install layout and pins: [docs/nlc/README.md](docs/nlc/README.md).
