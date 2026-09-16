---
name: planit
description: PLANIT + AWL orchestrator — ACS load through prove with default-closed gates, GATE-STD, and BBP leaf skills. Use for /planit or end-to-end BBP-shaped work in this repo.
disable-model-invocation: true
---

# PLANIT — load → prove (AWL overlay)

Read **`references/operation-verdict-standard.md`** (gate design §2, verdicts §4), **`references/audited-work-loop-standard.md`**, **`references/information-completion-contract.md`**, **`references/planit-process.md`**, and **`references/hub-charter-loop.md`** when this hub is in scope — before execution.

Map: [`docs/ai-compiled-systems/PLANIT-ORCHESTRATION.md`](../../../docs/ai-compiled-systems/PLANIT-ORCHESTRATION.md). PLANIT SSOT: [`docs/ai-compiled-systems/PROCESS.md`](../../../docs/ai-compiled-systems/PROCESS.md).

## Outcome

Orchestrate **AWL Phases 0–7** and **PLANIT steps 0–7** together: adversarial plan and execution audits; route to leaf skills; **enforce** [`operation-verdict-standard.md`](references/operation-verdict-standard.md) §2 on **every artifact Planit produces or approves**.

PLANIT is the compile process; BBP is the shape ([`docs/ai-compiled-systems/MERGE.md`](../../../docs/ai-compiled-systems/MERGE.md)). This skill orchestrates — it does not replace knowledge-steward, RCA, or leaf gate skills.

**Not the ai vault maintainer loop:** for durable ai-vault layers only (normative docs, manifests, intents, published prompts), route to **`~/.agents/skills/planit`** and its `local-*` leaf skills. Stay here for ACS + BBP hub/adopter work.

## Required inputs

| Input | Blocking? | Notes |
| ----- | --------- | ----- |
| Outcome + scope | yes | AWL Phase 0 / PLANIT interview |
| AWL Appendix C rows | yes (T2+); compressed for T0/T1 | Tier per AWL §5 |
| Multi-step flag | yes (T2+) | Staged plan vs single pass |
| Hub vs adopter | yes when hub touched | `references/hub-charter-loop.md` |

## Gate — Planit intake (default-closed)

**Default-closed** ([`operation-verdict-standard.md`](references/operation-verdict-standard.md) §2). Do **not** start AWL Phase 2 (applicability), PLANIT step **2** (plan), durable writes, or destructive commands until this gate **PASS**es. Phase 1 intake implements the resolution table ([`information-completion-contract.md`](references/information-completion-contract.md)).

| Criterion | Blocking? | Pass when (true if…) | Evidence |
| --------- | --------- | -------------------- | -------- |
| Outcome one-line | yes | Problem, user, and success shape stated | Resolution table row |
| In/out scope | yes | Boundaries explicit (what is excluded counts) | Resolution table row |
| Workspace root / subpath | yes | Root proposed; monorepo subpath when not whole repo | Resolution table row |
| Resolution table | yes | Every blocking Appendix C / ICC input → value, `Waived`, or `Assumption:` | Table in chat |
| PLANIT step 0 load | yes | `CHARTER.md`, in-scope ADRs/requirements/boundaries/contracts named or N/A with reason | Load list row |
| Tier (T2+) | yes when T2+ | T0–T3 named with rationale | Resolution table row |
| Multi-step flag (T2+) | yes when T2+ | Staged plan vs single pass recorded | Resolution table row |
| Blocking gaps | yes | No unresolved blocking ambiguity; numbered questions asked and **stopped** if still open | Chat turn state |
| Secrets | yes | No real credentials solicited in chat | Procedure compliance |

After all **blocking** rows are **true**, emit **`## Verdict — Planit intake gate`** per [`operation-verdict-standard.md`](references/operation-verdict-standard.md) §4, then proceed to AWL Phase 2.

## Procedure

**PLANIT** runs AWL **0–7** with PLANIT **0–7** embedded per [`PLANIT-ORCHESTRATION.md`](../../../docs/ai-compiled-systems/PLANIT-ORCHESTRATION.md). The name is PLANIT (`/planit`). Use AWL **Appendices A–F** for intake, plan, audit memos, handoffs, and Phase 7 record — do not duplicate those templates here.


This skill **orchestrates** existing norms and leaf skills — it does not replace KCR (ai vault), RCA, DSI stop checks, or VPR gates.

### Produced-artifact gate enforcement (mandatory)

Any **runnable or durable output** Planit creates, edits, or accepts from a leaf skill **must** satisfy [`operation-verdict-standard.md`](references/operation-verdict-standard.md) §2:

| Output kind | Gate requirement |
| ----------- | ---------------- |
| Skill (`SKILL.md`) | **Gate** section: default-closed; each **blocking** criterion testable true/false; **Done signals** objective |
| Prompt (`.cursor/prompts/`, `prompts/`) | Intake gate profile + blocking **Validation** criteria testable before **Execution** |
| Standard / manifest / intent | KCR acceptance criterion testable on record |
| Plan (AWL Phase 3) | Each step: **stop predicate** decidable PASS/FAIL with cited evidence |
| Plan audit / execution audit (Phases 4, 6) | **Verdict: PASS \| FAIL** apex; register rows PASS/FAIL/waived |
| Handoff (Phase 7) | Lists produced paths; **gate-standard** spot-check row per artifact |
| Chat-only deliverable (report, review) | Lead with verdict; blocking claims cite evidence |

**Before each durable write (AWL Phase 5 / PLANIT 6):** confirm the target artifact already includes or will include a compliant **Gate** (or profile in §2.3). **Stop** rather than ship gateless output.

**Phase 6 register row (required):** `GATE-STD` — every produced artifact has default-closed gate with testable blocking criteria → **PASS** / **FAIL** / **N/A** with path list.

---

### AWL Phase 0 — Authorize and bound

1. Record **one-line outcome** and **in/out scope** from the user message or skill invocation.
2. **Authorized invocation** (`/planit`, “roll it”, “fix the issues”, attached plan) satisfies Phase 0 — **do not** re-confirm ([`references/lean-operating-principles.md`](references/lean-operating-principles.md) §2).
3. If scope is unbounded, ask **one** clarifying question on outcome only; then proceed.

---

### AWL Phase 1 — Intake (+ PLANIT 0–1)

Follow AWL **Appendix C** and [`references/information-completion-contract.md`](references/information-completion-contract.md). Emit the **resolution table** and satisfy the **Gate** table above.

**T0/T1 compression (write it, or agents run T3 on class C):** skip Appendix B; skip multi-step flag; one plan table; still **intake + bind + prove**. T2+ keeps full AWL §5 ceremony.


**PLANIT step 0 — Load** (evidence in intake gate):

1. Load BBP standard (`CHARTER.md`), ADRs, requirements, known boundaries, verb contracts in scope.
2. Do **not** interview for facts already bound.

**PLANIT step 1 — Interview** (start; may continue into Phase 3):

1. Outcome, not feature list. Stop when goals and constraints can be named. Incomplete interview → **no plan**.
2. knowledge-steward **`load-shelf`** / **`flag-gap`** before generate; new facts via **`propose-fact`**. SSOT: [`agents/knowledge-steward/AGENT.md`](../../../agents/knowledge-steward/AGENT.md).

---

### AWL Phase 2 — Applicability register

Copy and complete AWL **Appendix A** minimum rows when applicable. Add domain-specific rows: `CHARTER.md`, [`PROCESS.md`](../../../docs/ai-compiled-systems/PROCESS.md), in-scope ADRs and **R***, hub `tools/ci-fitness.sh` when hub touched, produce-package / SSOT exit evidence when hub handoff applies ([`AGENTS.md`](../../../AGENTS.md)), **`operation-verdict-standard.md` §2** for produced artifacts.

**Stop predicate:** Every plausible norm is listed or excluded — closed world.

---

### AWL Phase 3 — Plan (+ PLANIT 2–3)

Use AWL **Appendix D** plan template. Add **Leaf skill / procedure** column when routing:

| # | Step | Leaf skill / procedure | Stop predicate | Audit hook |
| - | ---- | ---------------------- | -------------- | ---------- |

**PLANIT step 2 — Plan:** work items only — each item is new/changed **goal**, **boundary** (noun + verbs), **requirement**, **ADR**, or **rule** (tags / primitives / if-then; ADR 0007). A standard that never becomes a rule is not done. If the plan cannot say which, it is not a plan. **Hub:** classify change **A–F** (charter §6 step 1) in the plan header.


**PLANIT step 3 — Product statements:** single-step statements one boundary can finish (see [`PROCESS.md`](../../../docs/ai-compiled-systems/PROCESS.md)).

**Orchestration rules:**

- **Multi-step:** each row is one stage; carry AWL Appendix D **step handoff** blocks between steps internally.
- Name **leaf skill** when one exists (see **Routing** below). Read that skill’s `SKILL.md` at execute time.
- Follow AWL Appendix D **tier rules** (T0/T1 compression; scope creep → Phase 3 + re-run Phase 4).
- **Gate on deliverables:** plan **touch list** must name gate shape for each file to be written.
- **Step disposition:** every named step stays on the list until **PASS**, **FAIL**, or **`skip: <reason>`**. Silent omission fails Phase 4.

---

### AWL Phase 4 — Adversarial plan audit (separate execution)

**Do not** implement or generate in the same prose block as Phase 3. Use a **fresh section or subagent pass**. Use AWL **Appendix E** plan audit memo and checklist. **Fail-closed** per AWL §4.

Attack plan and statements: unbound items, god-noun, split adjectives, missing impact, wrong charter class. **Hub:** **`bbp-reviewer`** on the proposal package; findings cite `R*` / `C*` / `P*`.

**Register rows must include:** `GATE-STD` (planned artifacts will ship with §2-compliant gates).

Emit **`## Verdict — Planit plan audit`** per [`operation-verdict-standard.md`](references/operation-verdict-standard.md) §4 before bind close-out and before AWL Phase 5.

---

### PLANIT steps 4–5 — Bind and close gaps

**Step 4 — Bind:** every statement points at requirement ids, ADR ids, **rule** ids when ADR 0007 applies, and **BBP standard** (always on). No pointer → unbound.


**Step 5 — Close gaps:** loop until every statement is bound. **Do not generate yet.**

Emit **`## Verdict — Planit bind gate`** per §4 before PLANIT step 6. On **FAIL**, stay in step 5.

---

### AWL Phase 5 — Execute (+ PLANIT 6)

Run approved plan steps **in order**. Bind gate must already **PASS**. This phase is generate only — not bind, not prove.

1. **Before each step** — confirm prior stop predicate met; emit §4 verdict when the step blocks downstream work.
2. **Leaf skill step** — read **`.agents/skills/<name>/SKILL.md`** (or `.cursor/skills/`); run Gate → Procedure; verify leaf output meets §2. Inspect files, diffs, and machine exit codes — do not accept a subagent summary as PASS.
3. **PLANIT step 6 — Generate:** hub implementation only after charter **ratification** (§6 steps 4–5) unless ADR-exempt. Route **`bbp-proposer`**. BBP-shaped code for bound statements only; humans do not edit output to help audits pass.
4. **Inline step** — cite commands and exit codes of the **artifact under test**. INCONCLUSIVE is BLOCKED.
5. **KCR sub-gate** — if step touches durable **ai vault** layers, **stop** until KCR accepted ([`references/knowledge-change-review-standard.md`](references/knowledge-change-review-standard.md)); prefer routing to **`~/.agents/skills/planit`**.
6. **Failure** — jidoka: stop; RCA if non-trivial ([`references/root-cause-analysis-standard.md`](references/root-cause-analysis-standard.md) or `/conduct-root-cause-analysis`); then PLANIT **1** or **5**, then **6** again. Do not patch generated files to silence audits.
7. **Handoff between steps** — AWL Appendix D step handoff template.
8. **Pre-write check** — no durable file write until target artifact’s **Gate** (§2) is defined in plan or draft.

---

### PLANIT step 7 — Prove (compile, not ship)

**Both** required:

1. **Machine gate** — hub: **`bbp-confirmer`** (`bash tools/ci-fitness.sh` + charter §11 with evidence). Adopter: the fitness suite that tree bound. Exit non-zero = fail.
2. **Adversarial audit** — separate from the generator: statements done, bindings held, no second copy of an adjective inside a goal.

Compile-green is not released. **Ship** is later: `python3 tools/release-audit.py <tree>` after a human writes `Released-by:` (and `Ratified-by:` when class A/B/D/E/F). Do not treat prove PASS as ship. Do not write those lines as the confirmer.

Emit **`## Verdict — Planit prove`** per §4 when step 7 completes.


---

### AWL Phase 6 — Adversarial execution audit (separate execution)

Separate from Phase 5 prose — **fresh section or subagent pass**. Use AWL **Appendix E** execution audit memo and **Appendix B** meta-audit checklist (T2+). **Fail-closed** per AWL §4.

Re-check bindings vs diff; prove evidence is the **artifact under test**. **Hub:** charter §11 rows and fitness output present.

**Domain instances** (orchestration hooks — use global Planit when primary):

- **DSI converge** — [`references/local-dsi-converge-audit-template.md`](references/local-dsi-converge-audit-template.md)
- **Vault PR (ai vault)** — `/local-review-pr` via **`~/.agents/skills/planit`**

**Required:** `GATE-STD` row **PASS** for every produced artifact path, or **FAIL** with fix list.

Emit **`## Verdict — Planit execution audit`** per §4 before Phase 7.

---

### AWL Phase 7 — Record and propagate (+ hub §6 step 8)

Follow AWL **Appendix F** ([`references/domain-first-authoring.md`](references/domain-first-authoring.md) for back-propagation). **Hub:** **`bbp-recorder`** (ADR or “no ADR, reason”).

Emit user-facing **Handoff** for T2+ multi-step work. Handoff must include:

- Produced artifact paths
- **Gate-standard compliance:** per-path **PASS** / **FAIL** / **N/A** for §2
- Open fix list when any path is **FAIL**

Emit **`## Verdict — Planit process`** (process-level §5 rollup). **PASS** only when intake, plan audit, bind gate, prove, and execution audit verdicts are **PASS**.

---

## Routing quick reference

| Outcome slice | Leaf skill / route |
| ------------- | ------------------ |
| Proposal / implement (hub) | `bbp-proposer` |
| Adversarial review | `bbp-reviewer` |
| Prove + hub fitness | `bbp-confirmer` |
| ADR / record | `bbp-recorder` |
| Shelf facts / gaps | `agents/knowledge-steward` |
| Root cause | `/conduct-root-cause-analysis` or `references/root-cause-analysis-standard.md` |
| DSI, greenfield WO, make-a-skill, ai vault `local-*` | **`~/.agents/skills/planit`** |

When no leaf skill fits, execute inline under this procedure with full AWL audits and §2 on all outputs.

---

## Reference files

| File | Use |
| ---- | --- |
| [`references/README.md`](references/README.md) | Vendored AWL norms + sync policy |
| [`references/planit-process.md`](references/planit-process.md) | PLANIT steps summary |
| [`references/hub-charter-loop.md`](references/hub-charter-loop.md) | Charter §6 hub mapping |
| [`docs/ai-compiled-systems/PLANIT-ORCHESTRATION.md`](../../../docs/ai-compiled-systems/PLANIT-ORCHESTRATION.md) | Combined spine |
| [`.agents/bbp-short-form.md`](../../bbp-short-form.md) | Charter §15 |

---

## Done signals

- Intake **Gate** **PASS** with §4 verdict emitted
- Applicability register closed (AWL Phase 2)
- Plan audit **PASS** with `GATE-STD` planned — every named step PASS, FAIL, or `skip: <reason>` — §4 verdict before execute
- Bind gate **PASS** before generate
- Prove **PASS** (machine + adversarial); hub confirmer output when hub touched. Prove is compile, not ship.
- Ship is optional in this skill: `python3 tools/release-audit.py <tree>` after a human `Released-by:` — not part of process PASS

- Execution audit **PASS** with `GATE-STD` on delivered artifacts; evidence is the artifact under test, not a delegate summary — §4 verdict before record
- Appendix B meta-audit **PASS** when T2+
- Phase 7 handoff includes per-artifact gate-standard compliance
- **Process result: PASS** only when every required phase verdict is **PASS**
