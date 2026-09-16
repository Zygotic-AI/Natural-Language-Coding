# PLANIT orchestration (agent skill)

How the **ACS compile loop** ([`PROCESS.md`](PROCESS.md)) and the **audited work loop (AWL)** run together when an agent invokes **`/planit`** in this repository.

| Layer | SSOT | Role |
|-------|------|------|
| **PLANIT** | [`PROCESS.md`](PROCESS.md) | What to produce: load → interview → plan → statements → bind → close gaps → generate → prove |
| **AWL** | [`.agents/skills/planit/references/audited-work-loop-standard.md`](../../.agents/skills/planit/references/audited-work-loop-standard.md) | How to run work safely: intake, applicability, audits, gates, record |
| **BBP** | [`CHARTER.md`](../../CHARTER.md) | Shape of generated code and hub change order (§6–7, §11) |

PLANIT does not replace BBP ([`MERGE.md`](MERGE.md)). AWL does not replace PLANIT — it adds **default-closed gates**, **tier ceremony**, and **operation verdicts** on every phase and durable artifact ([`operation-verdict-standard.md`](../../.agents/skills/planit/references/operation-verdict-standard.md)).

**Skill entrypoint:** [`.agents/skills/planit/SKILL.md`](../../.agents/skills/planit/SKILL.md) (Cursor: `.cursor/skills/planit`).

**Org-global Planit** (`~/.agents/skills/planit`) remains the orchestrator for ai-vault-only routes (DSI, `local-*` maintainer skills). This repo skill is authoritative **here** for ACS + BBP hub work.

---

## Combined spine (one run)

```text
AWL 0–1 (authorize, ICC intake + tier)     + PLANIT 0 (load) + PLANIT 1 (interview)
AWL 2 (applicability register)
PLANIT 2–3 (plan, product statements)      + AWL 3 (plan template: leaf, stop predicate)
AWL 4 (adversarial plan audit)             + GATE-STD on touch list
PLANIT 4–5 (bind, close gaps)              + bind gate verdict
AWL 5 (execute)                            + PLANIT 6 (generate) + hub ratify rules
PLANIT 7 (prove)                           + machine gate + adversarial prove
AWL 6 (execution audit)                    + GATE-STD on delivered paths + meta-audit when T2+
AWL 7 (record)                             + PLANIT record + charter §6 step 8 (hub)
```

Do not start **plan** (PLANIT 2), **applicability** durable writes, or **generate** until **intake** passes. Do not **generate** until **bind gate** passes. Do not hand off until **prove** and **execution audit** pass.

---

## Phase map

| AWL phase | PLANIT step(s) | Primary outputs |
|-----------|----------------|-----------------|
| 0 Authorize | — | Outcome, scope |
| 1 Intake | 0 Load (evidence row), 1 Interview (start) | Resolution table, tier (T2+), load list |
| 2 Applicability | 0 (norms in scope) | Register: charter, PROCESS, ADRs, R*, fitness, operation-verdict §2 for writes |
| 3 Plan | 2 Plan, 3 Product statements | Work items, atomic statements, leaf skill column |
| 4 Plan audit | (before bind complete) | PASS/FAIL + `GATE-STD` on planned artifacts |
| 5 Execute | 4–5 Bind/close gaps; 6 Generate; 7 Prove | Bound statements, code, gate outputs |
| 6 Execution audit | After prove | Evidence on artifacts under test; `GATE-STD` on paths |
| 7 Record | Hub §6 step 8 | ADR/recorder handoff, back-propagation when applicable |

---

## Gates and verdicts

| Gate | When | Standard |
|------|------|----------|
| Intake | Before PLANIT 2 / AWL 2 | ICC + skill intake table; verdict per operation-verdict §4 |
| Bind | Before PLANIT 6 | All statements bound |
| Prove | PLANIT 7 | Machine gate + adversarial audit; hub: `tools/ci-fitness.sh` + §11 |
| Produced artifact | Before each durable write | operation-verdict §2 (skills, prompts, plans, handoffs) |
| `GATE-STD` | Plan audit + execution audit | Every touched path has default-closed gate or N/A with reason |

Verdict headings: `## Verdict — Planit intake gate`, `plan audit`, `bind gate`, `prove`, `execution audit`, `process`.

---

## Failure and RCA

**Prove FAIL** → stop (jidoka). Non-trivial failure → [`root-cause-analysis-standard.md`](../../.agents/skills/planit/references/root-cause-analysis-standard.md) or `/conduct-root-cause-analysis`, then PLANIT **1** (interview) or **5** (bind), then **6** (regenerate). Humans do not patch generated files to silence audits ([`PROCESS.md`](PROCESS.md)).

---

## Leaf skills (this repo)

| Slice | Skill |
|-------|--------|
| Orchestrator | `planit` |
| Propose / implement | `bbp-proposer` |
| Adversarial review | `bbp-reviewer` |
| Prove / fitness | `bbp-confirmer` |
| Record | `bbp-recorder` |
| Knowledge shelf | `agents/knowledge-steward` |

Hub charter loop detail: [`.agents/skills/planit/references/hub-charter-loop.md`](../../.agents/skills/planit/references/hub-charter-loop.md).

---

## Reference bundle

Vendored under [`.agents/skills/planit/references/`](../../.agents/skills/planit/references/) (sync policy: [`references/README.md`](../../.agents/skills/planit/references/README.md)). BBP-specific summaries: `planit-process.md`, `hub-charter-loop.md`.
