# AI-Compiled Systems

**Instead of giving code to a compiler, you give goals and requirements. The AI builds the rest.**

The source is intent. The code is the object file. What the compiler emits must be **BBA-shaped**, or the build fails.

Locally green, globally wrong — stopped.

This folder is the process + naming layer. The design standard remains [`CHARTER.md`](../../CHARTER.md) (Boundary-Based Architecture). Do not treat these pages as a second charter.

| Page | Role |
|------|------|
| [MERGE.md](MERGE.md) | Settled split: AIMS = process, BBA = shape |
| [PROCESS.md](PROCESS.md) | Interview → bind → generate → prove (steps 0–7) |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Two layers, two citizen lists, compile gate |
| [MANIFESTO.md](MANIFESTO.md) | Why intent is the source |
| [COMPILER.md](COMPILER.md) | What “AI compiled” means and when generation is incomplete |
| [AIMS-FILE-MAP.md](AIMS-FILE-MAP.md) | What happened to the old 34-file AIMS suite |

Infographic in one line: goals + requirements → discrete boundaries → write/audit/graph one object at a time, neighbors only through hard contracts.
