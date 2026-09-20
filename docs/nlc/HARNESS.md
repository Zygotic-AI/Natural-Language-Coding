# Harness wire-up (UC18)

Knowledge domains must load **before generate**, not discovered during a late ship audit.

## Required calls

| When | Command / skill |
| ---- | ---------------- |
| Interview | knowledge-steward `load-knowledge-domain` / `flag-gap` ([`/interview`](../../.agents/skills/interview/SKILL.md)) |
| Planit step 6 (before emit) | `python3 tools/nlc-before-generate.py` ([`nlc-before-generate.md`](../../.agents/skills/planit/references/nlc-before-generate.md)) |
| Session start (hub work) | `bash tools/session-preflight.sh` |

## Default-closed

If `nlc-before-generate.py` exits non-zero, **do not generate**. Fix facts, waive with explicit `Assumption:`, or continue interview.

## CI (app repo)

On every PR, run the adopter fitness suite. Optional workflow template: `.github/workflows/nlc-prove.yml` from `nlc-init`.

Ship promotion semantics: [`PROVE-AND-SHIP.md`](PROVE-AND-SHIP.md).
