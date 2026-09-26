# Jidoka: defective machine output (do not counsel “ignore”)

When **tooling output** (CLI JSON, resume fields, gate messages) **contradicts** documented SSOT, landmines, or **operator-stated repo facts**, treat that as a **hub defect** — not something the operator should work around in their head.

## Gate (default-closed)

Before telling the operator what a field “really means” or what to do next:

| Criterion | Blocking? | Pass when |
| --------- | --------- | --------- |
| SSOT match | yes | Field meaning matches docs/RCA/skill for that key |
| Operator challenge | yes | If they say the data or advice is wrong, you **stop** operational guidance until reconciled |
| No ignore counseling | yes | You do **not** tell them to ignore, reinterpret, or “mentally remap” defective output |
| Fix or RCA | yes | Same session: **fix** the contract (code/docs) or **write RCA** with a verification command — then give steps |

## Fail patterns (do not ship in chat)

- “That name means X, not Y” **without** a merged fix to the emitter/docs
- “Just ignore `stale_*` / it’s not garbage” while SSOT still says **delete** those names
- Defending a patch you just landed instead of jidoka at the schema/skill layer

## Pass pattern

- “Resume JSON overloaded `stale_release_branches`; SSOT says delete stale. **Fix:** split `closed_release_branches` — verify: `python3 tools/nlc_release_resume.py --emit json`.”

## Harness

Linked from [`AGENTS.md`](../../AGENTS.md). Aligns with charter integrity (zero variance) and long-term quality (root cause in process, not output).
