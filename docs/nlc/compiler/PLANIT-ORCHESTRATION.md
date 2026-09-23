# [PLANIT](../../TERMS.md#planit) orchestration (agent skill)

How the **[ACS](../../TERMS.md#acs) compile loop** ([`PROCESS.md`](PROCESS.md)) and the **audited work loop (AWL)** run together when an agent invokes **`/planit`** in this repository.

| Layer | SSOT | Role |
|-------|------|------|
| **[PLANIT](../../TERMS.md#planit)** | [`PROCESS.md`](PROCESS.md) | What to produce: load → [interview](../../TERMS.md#interview) → plan → statements → bind → close gaps → generate → [verify](../../TERMS.md#verify) |
| **[AWL](../../TERMS.md#awl)** | [`.agents/skills/planit/references/audited-work-loop-standard.md`](../../../.agents/skills/planit/references/audited-work-loop-standard.md) | How to run work safely: intake, applicability, audits, gates, record |
| **[BBP](../../TERMS.md#bbp)** | [`CHARTER.md`](../../../CHARTER.md) | Shape of generated code and [hub](../../TERMS.md#hub) change order (§6–7, §11) |

[PLANIT](../../TERMS.md#planit) does not replace [BBP](../../TERMS.md#bbp) ([`MERGE.md`](MERGE.md)). [AWL](../../TERMS.md#awl) does not replace [PLANIT](../../TERMS.md#planit) — it adds **[default-closed](../../TERMS.md#default-closed) gates**, **tier ceremony**, and **operation verdicts** on every phase and durable artifact ([`operation-verdict-standard.md`](../../../.agents/skills/planit/references/operation-verdict-standard.md)).

**Skill entrypoint:** [`.agents/skills/planit/SKILL.md`](../../../.agents/skills/planit/SKILL.md) (Cursor: `.cursor/skills/planit`).

**Org-global [Planit](../../TERMS.md#planit)** (`~/.agents/skills/planit`) remains the orchestrator for ai-vault-only routes (DSI, `local-*` maintainer skills). This repo skill is authoritative **here** for [ACS](../../TERMS.md#acs) + [BBP](../../TERMS.md#bbp) [hub](../../TERMS.md#hub) work.

---

## Combined spine (one run)

```text
AWL 0–1 (authorize, ICC intake + tier)     + PLANIT 0 (load) + PLANIT 1 (interview)
AWL 2 (applicability register)
PLANIT 2–3 (plan, product statements)      + AWL 3 (plan template: leaf, stop predicate)
AWL 4 (adversarial plan audit)             + GATE-STD on touch list
PLANIT 4–5 (bind, close gaps)              + bind gate verdict
  → X1 action-plan gate + X2 reverse audit   (ADR 0024/0030; before any emit)
AWL 5 (execute)                            + PLANIT 6 (generate) + hub ratify rules
  → X5 emit audit + X3 manifest + X6 bound gates (ADR 0030; after emit)
PLANIT 7 (verify)                          + machine gate + adversarial audit
AWL 6 (execution audit)                    + GATE-STD on delivered paths + meta-audit when T2+
AWL 7 (record)                             + PLANIT record + charter §6 step 8 (hub)
```

Do not start **plan** (PLANIT 2), **applicability** durable writes, or **generate** until **intake** passes. Do not **generate** until **bind [gate](../../TERMS.md#gate)** passes. Do not **emit** until **X1 + X2** pass. Do not **proceed** after emit until **X5 + X3 + X6** pass. Do not hand off until **[verify](../../TERMS.md#verify)** and **execution [audit](../../TERMS.md#audit)** pass. [Verify](../../TERMS.md#verify) is compile. [Ship](../../TERMS.md#ship) is `./nlc ship-check` or `release-audit.py` after a human `Released-by:` — not the same [gate](../../TERMS.md#gate).

**T0/T1:** skip Appendix B, skip multi-step flag, one plan table, still intake + bind + [verify](../../TERMS.md#verify). If this is not followed, the run is T3.

---

## Phase map

| [AWL](../../TERMS.md#awl) phase | [PLANIT](../../TERMS.md#planit) step(s) | Primary outputs |
|-----------|----------------|-----------------|
| 0 Authorize | — | Outcome, scope |
| 1 Intake | 0 Load (evidence row), 1 [Interview](../../TERMS.md#interview) (start) | Resolution table, tier (T2+), load list |
| 2 Applicability | 0 (norms in scope) | Register: [charter](../../TERMS.md#charter), PROCESS, ADRs, R*, rules, fitness, operation-verdict §2 for writes |
| 3 Plan | 2 Plan, 3 Product statements | Work items (goal / boundary / requirement / ADR / **rule**), atomic statements, leaf skill column |
| 4 [Plan audit](../../TERMS.md#plan-audit) | (before bind) | PASS/FAIL + `GATE-STD` on planned artifacts |
| — Bind | **4–5 Bind / close gaps** | Bound statements; bind [gate](../../TERMS.md#gate) PASS. **Not execute.** |
| — Pipeline pre-emit | **X1 + X2** | action↔plan valid; every applicable ADR bound to an action |
| 5 Execute | **6 Generate one artifact** then **6.5 [gate](../../TERMS.md#gate) it** | Code/skill/doc; immediate [default-closed](../../TERMS.md#default-closed) [gate](../../TERMS.md#gate). FAIL stops the next row. |
| — Pipeline post-emit | **X5 + X3 + X6** | emit audited; manifest schema-valid (`unused=na`); bound ADR gates run |
| — [Verify](../../TERMS.md#verify) | **7 [Verify](../../TERMS.md#verify)** | `./nlc verify-deep` / fitness + adversarial [audit](../../TERMS.md#audit). Compile, not [ship](../../TERMS.md#ship). |
| 6 Execution [audit](../../TERMS.md#audit) | After [verify](../../TERMS.md#verify) | Evidence on artifacts under test; `GATE-STD` on paths |
| 7 Record | [Hub](../../TERMS.md#hub) §6 step 8 | ADR/recorder [handoff](../../TERMS.md#handoff), back-propagation when applicable |
| — [Ship](../../TERMS.md#ship) | After human sign | `release-audit.py` — `Released-by:` required |

---

## Gates and verdicts

| [Gate](../../TERMS.md#gate) | When | Standard |
|------|------|----------|
| Intake | Before [PLANIT](../../TERMS.md#planit) 2 / [AWL](../../TERMS.md#awl) 2 | ICC + skill intake table; verdict per operation-verdict §4 |
| Bind | Before [PLANIT](../../TERMS.md#planit) 6 | All statements bound (incl. rules when 0007 applies) |
| X1 action-plan | Before emit | Every action maps to a plan step; every step has an action |
| X2 reverse audit | Before emit | Every applicable ADR bound to ≥1 action |
| X5 emit audit | After emit | Every emit has an audit (non-pending) |
| X3 emit manifest | After emit | Manifest matches schema; `unused=na`; gate closed |
| X6 bound ADR gates | After emit | Gates of ADRs bound to this action, default-closed |
| [Verify](../../TERMS.md#verify) | [PLANIT](../../TERMS.md#planit) 7 | [Hub](../../TERMS.md#hub): `ci_fitness.py` + §11. [Adopter](../../TERMS.md#adopter): `./nlc verify` / `verify-deep` ([`APP-VERIFY.md`](../APP-VERIFY.md)). Adversarial [audit](../../TERMS.md#audit) separate from generate. |
| [Ship](../../TERMS.md#ship) | After [verify](../../TERMS.md#verify), human signed | `./nlc ship-check`. Compile-green is not released. |
| Produced artifact | Before each durable write | operation-verdict §2 (skills, prompts, plans, handoffs) |
| `GATE-STD` | [Plan audit](../../TERMS.md#plan-audit) + execution [audit](../../TERMS.md#audit) | Every touched path has [default-closed](../../TERMS.md#default-closed) [gate](../../TERMS.md#gate) or N/A with reason |

Verdict headings: `## Verdict — Planit intake gate`, `plan audit`, `bind gate`, `prove`, `execution audit`, `process`.


---

## Failure and [RCA](../../TERMS.md#rca)

**[Prove](../../TERMS.md#prove) FAIL** → stop (jidoka). Non-trivial failure → [`root-cause-analysis-standard.md`](../../../.agents/skills/planit/references/root-cause-analysis-standard.md) or `/conduct-root-cause-analysis`, then [PLANIT](../../TERMS.md#planit) **1** (interview) or **5** (bind), then **6** (regenerate). Humans do not patch generated files to silence audits ([`PROCESS.md`](PROCESS.md)).

---

## Leaf skills (this repo)

| Slice | Skill |
|-------|--------|
| Orchestrator | `planit` |
| Propose / implement | `bbp-proposer` |
| Adversarial review | `bbp-reviewer` |
| [Prove](../../TERMS.md#prove) / fitness | `bbp-confirmer` |
| Record | `bbp-recorder` |
| [Knowledge domains](../../TERMS.md#knowledge-domain) | `agents/knowledge-steward` |

[Hub](../../TERMS.md#hub) [charter](../../TERMS.md#charter) loop detail: [`.agents/skills/planit/references/hub-charter-loop.md`](../../../.agents/skills/planit/references/hub-charter-loop.md).

---

## Reference bundle

Vendored under [`.agents/skills/planit/references/`](../../../.agents/skills/planit/references/) (sync policy: [`references/README.md`](../../../.agents/skills/planit/references/README.md)). BBP-specific summaries: `planit-process.md`, `hub-charter-loop.md`.
