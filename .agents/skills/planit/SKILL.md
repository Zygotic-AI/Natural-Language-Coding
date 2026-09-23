---
name: [planit](../../../docs/TERMS.md#planit)
description: [PLANIT](../../../docs/TERMS.md#planit) + [AWL](../../../docs/TERMS.md#awl) orchestrator — [ACS](../../../docs/TERMS.md#acs) load through [prove](../../../docs/TERMS.md#prove) with [default-closed](../../../docs/TERMS.md#default-closed) gates, GATE-STD, and [BBP](../../../docs/TERMS.md#bbp) leaf skills. Use for [/planit](../../../docs/TERMS.md#planit) or end-to-end BBP-shaped work in this repo.
disable-model-invocation: true
---

# [PLANIT](../../../docs/TERMS.md#planit) — load → [prove](../../../docs/TERMS.md#prove) (AWL overlay)

Read **`references/operation-verdict-standard.md`** (gate design §2, verdicts §4), **`references/audited-work-loop-standard.md`**, **`references/information-completion-contract.md`**, **`references/planit-process.md`**, and **`references/hub-charter-loop.md`** when this [hub](../../../docs/TERMS.md#hub) is in scope — before execution.

Map: [`docs/ai-compiled-systems/PLANIT-ORCHESTRATION.md`](../../../docs/ai-compiled-systems/PLANIT-ORCHESTRATION.md). [PLANIT](../../../docs/TERMS.md#planit) SSOT: [`docs/ai-compiled-systems/PROCESS.md`](../../../docs/ai-compiled-systems/PROCESS.md).

## Outcome

Orchestrate **[AWL](../../../docs/TERMS.md#awl) Phases 0–7** and **[PLANIT](../../../docs/TERMS.md#planit) steps 0–7** together: adversarial plan and execution audits; route to leaf skills; **enforce** [`operation-verdict-standard.md`](references/operation-verdict-standard.md) §2 on **every artifact [Planit](../../../docs/TERMS.md#planit) produces or approves**.

[PLANIT](../../../docs/TERMS.md#planit) is the compile process; [BBP](../../../docs/TERMS.md#bbp) is the shape ([`docs/ai-compiled-systems/MERGE.md`](../../../docs/ai-compiled-systems/MERGE.md)). This skill orchestrates — it does not replace knowledge-steward, [RCA](../../../docs/TERMS.md#rca), or leaf [gate](../../../docs/TERMS.md#gate) skills.

**Not the ai vault maintainer loop:** for durable ai-vault layers only (normative docs, manifests, intents, published prompts), route to **`~/.agents/skills/planit`** and its `local-*` leaf skills. Stay here for [ACS](../../../docs/TERMS.md#acs) + [BBP](../../../docs/TERMS.md#bbp) hub/adopter work.

## Required inputs

| Input | Blocking? | Notes |
| ----- | --------- | ----- |
| Outcome + scope | yes | [AWL](../../../docs/TERMS.md#awl) Phase 0 / [PLANIT](../../../docs/TERMS.md#planit) [interview](../../../docs/TERMS.md#interview) |
| [AWL](../../../docs/TERMS.md#awl) Appendix C rows | yes (T2+); compressed for T0/T1 | Tier per [AWL](../../../docs/TERMS.md#awl) §5 |
| Multi-step flag | yes (T2+) | Staged plan vs single pass |
| [Hub](../../../docs/TERMS.md#hub) vs [adopter](../../../docs/TERMS.md#adopter) | yes when [hub](../../../docs/TERMS.md#hub) touched | `references/hub-charter-loop.md` |

## [Gate](../../../docs/TERMS.md#gate) — [Planit](../../../docs/TERMS.md#planit) intake (default-closed)

**[Default-closed](../../../docs/TERMS.md#default-closed)** ([`operation-verdict-standard.md`](references/operation-verdict-standard.md) §2). Do **not** start [AWL](../../../docs/TERMS.md#awl) Phase 2 (applicability), [PLANIT](../../../docs/TERMS.md#planit) step **2** (plan), durable writes, or destructive commands until this [gate](../../../docs/TERMS.md#gate) **PASS**es. Phase 1 intake implements the resolution table ([`information-completion-contract.md`](references/information-completion-contract.md)).

| Criterion | Blocking? | Pass when (true if…) | Evidence |
| --------- | --------- | -------------------- | -------- |
| Outcome one-line | yes | Problem, user, and success shape stated | Resolution table row |
| In/out scope | yes | Boundaries explicit (what is excluded counts) | Resolution table row |
| Workspace root / subpath | yes | Root proposed; monorepo subpath when not whole repo | Resolution table row |
| Resolution table | yes | Every blocking Appendix C / ICC input → value, `Waived`, or `Assumption:` | Table in chat |
| [PLANIT](../../../docs/TERMS.md#planit) step 0 load | yes | `CHARTER.md`, in-scope ADRs/requirements/boundaries/contracts named or N/A with reason | Load list row |
| Tier (T2+) | yes when T2+ | T0–T3 named with rationale | Resolution table row |
| Multi-step flag (T2+) | yes when T2+ | Staged plan vs single pass recorded | Resolution table row |
| Blocking gaps | yes | No unresolved blocking ambiguity; numbered questions asked and **stopped** if still open | Chat turn state |
| Secrets | yes | No real credentials solicited in chat | Procedure compliance |

After all **blocking** rows are **true**, emit **`## Verdict — Planit intake gate`** per [`operation-verdict-standard.md`](references/operation-verdict-standard.md) §4, then proceed to [AWL](../../../docs/TERMS.md#awl) Phase 2.

## Procedure

**[PLANIT](../../../docs/TERMS.md#planit)** runs [AWL](../../../docs/TERMS.md#awl) **0–7** with [PLANIT](../../../docs/TERMS.md#planit) **0–7** embedded per [`PLANIT-ORCHESTRATION.md`](../../../docs/ai-compiled-systems/PLANIT-ORCHESTRATION.md). The name is [PLANIT](../../../docs/TERMS.md#planit) (`/planit`). Use [AWL](../../../docs/TERMS.md#awl) **Appendices A–F** for intake, plan, [audit](../../../docs/TERMS.md#audit) memos, handoffs, and Phase 7 record — do not duplicate those templates here.


This skill **orchestrates** existing norms and leaf skills — it does not replace KCR (ai vault), [RCA](../../../docs/TERMS.md#rca), DSI stop checks, or VPR gates.

### Produced-artifact [gate](../../../docs/TERMS.md#gate) enforcement (mandatory)

Any **runnable or durable output** [Planit](../../../docs/TERMS.md#planit) creates, edits, or accepts from a leaf skill **must** satisfy [`operation-verdict-standard.md`](references/operation-verdict-standard.md) §2:

| Output kind | [Gate](../../../docs/TERMS.md#gate) [requirement](../../../docs/TERMS.md#requirement) |
| ----------- | ---------------- |
| Skill (`SKILL.md`) | **[Gate](../../../docs/TERMS.md#gate)** section: [default-closed](../../../docs/TERMS.md#default-closed); each **blocking** criterion testable true/false; **Done signals** objective |
| Prompt (`.cursor/prompts/`, `prompts/`) | Intake [gate](../../../docs/TERMS.md#gate) profile + blocking **Validation** criteria testable before **Execution** |
| Standard / manifest / intent | KCR acceptance criterion testable on record |
| Plan (AWL Phase 3) | Each step: **stop predicate** decidable PASS/FAIL with cited evidence |
| [Plan audit](../../../docs/TERMS.md#plan-audit) / execution [audit](../../../docs/TERMS.md#audit) (Phases 4, 6) | **Verdict: PASS \| FAIL** apex; register rows PASS/FAIL/waived |
| [Handoff](../../../docs/TERMS.md#handoff) (Phase 7) | Lists produced paths; **gate-standard** spot-check row per artifact |
| Chat-only deliverable (report, review) | Lead with verdict; blocking claims cite evidence |

**Before each durable write (AWL Phase 5 / PLANIT 6):** confirm the target artifact already includes or will include a compliant **[Gate](../../../docs/TERMS.md#gate)** (or profile in §2.3). **Stop** rather than [ship](../../../docs/TERMS.md#ship) gateless output.

**Phase 6 register row (required):** `GATE-STD` — every produced artifact has [default-closed](../../../docs/TERMS.md#default-closed) [gate](../../../docs/TERMS.md#gate) with testable blocking criteria → **PASS** / **FAIL** / **N/A** with path list.

---

### [AWL](../../../docs/TERMS.md#awl) Phase 0 — Authorize and bound

1. Record **one-line outcome** and **in/out scope** from the user message or skill invocation.
2. **Authorized invocation** (`/planit`, “roll it”, “fix the issues”, attached plan) satisfies Phase 0 — **do not** re-confirm ([`references/lean-operating-principles.md`](references/lean-operating-principles.md) §2).
3. If scope is unbounded, ask **one** clarifying question on outcome only; then proceed.

---

### [AWL](../../../docs/TERMS.md#awl) Phase 1 — Intake (+ PLANIT 0–1)

Follow [AWL](../../../docs/TERMS.md#awl) **Appendix C** and [`references/information-completion-contract.md`](references/information-completion-contract.md). Emit the **resolution table** and satisfy the **[Gate](../../../docs/TERMS.md#gate)** table above.

**T0/T1 compression (write it, or agents run T3 on class C):** skip Appendix B; skip multi-step flag; one plan table; still **intake + bind + [prove](../../../docs/TERMS.md#prove)**. T2+ keeps full [AWL](../../../docs/TERMS.md#awl) §5 ceremony.


**[PLANIT](../../../docs/TERMS.md#planit) step 0 — Load** (evidence in intake gate):

1. Load [BBP](../../../docs/TERMS.md#bbp) standard (`CHARTER.md`), ADRs, requirements, known boundaries, verb contracts in scope.
2. Do **not** [interview](../../../docs/TERMS.md#interview) for facts already bound.

**[PLANIT](../../../docs/TERMS.md#planit) step 1 — [Interview](../../../docs/TERMS.md#interview)** (start; may continue into Phase 3):

1. Outcome, not feature list. Stop when goals and constraints can be named. Incomplete [interview](../../../docs/TERMS.md#interview) → **no plan**.
2. knowledge-steward **`load-knowledge-domain`** / **`flag-gap`** before generate; new facts via **`propose-fact`**. SSOT: [`agents/knowledge-steward/AGENT.md`](../../../agents/knowledge-steward/AGENT.md).

---

### [AWL](../../../docs/TERMS.md#awl) Phase 2 — Applicability register

Copy and complete [AWL](../../../docs/TERMS.md#awl) **Appendix A** minimum rows when applicable. Add domain-specific rows: `CHARTER.md`, [`PROCESS.md`](../../../docs/ai-compiled-systems/PROCESS.md), in-scope ADRs and **R***, [hub](../../../docs/TERMS.md#hub) `tools/ci-fitness.sh` when [hub](../../../docs/TERMS.md#hub) touched, produce-package / [SSOT exit evidence](../../../docs/TERMS.md#ssot-exit-evidence) when [hub](../../../docs/TERMS.md#hub) [handoff](../../../docs/TERMS.md#handoff) applies ([`AGENTS.md`](../../../AGENTS.md)), **`operation-verdict-standard.md` §2** for produced artifacts.

**Stop predicate:** Every plausible norm is listed or excluded — closed world.

---

### [AWL](../../../docs/TERMS.md#awl) Phase 3 — Plan (+ PLANIT 2–3)

Use [AWL](../../../docs/TERMS.md#awl) **Appendix D** plan template. Add **Leaf skill / procedure** column when routing:

| # | Step | Leaf skill / procedure | Stop predicate | [Audit](../../../docs/TERMS.md#audit) hook |
| - | ---- | ---------------------- | -------------- | ---------- |

**[PLANIT](../../../docs/TERMS.md#planit) step 2 — Plan:** work items only — each item is new/changed **[goal](../../../docs/TERMS.md#goal)**, **[boundary](../../../docs/TERMS.md#boundary)** (noun + verbs), **[requirement](../../../docs/TERMS.md#requirement)**, **[ADR](../../../docs/TERMS.md#adr)**, or **[rule](../../../docs/TERMS.md#rule)** (tags / primitives / if-then; ADR 0007). A standard that never becomes a [rule](../../../docs/TERMS.md#rule) is not done. If the plan cannot say which, it is not a plan. **[Hub](../../../docs/TERMS.md#hub):** classify change **A–F** (charter §6 step 1) in the plan header.


**[PLANIT](../../../docs/TERMS.md#planit) step 3 — Product statements:** single-step statements one [boundary](../../../docs/TERMS.md#boundary) can finish (see [`PROCESS.md`](../../../docs/ai-compiled-systems/PROCESS.md)).

**Orchestration rules:**

- **Multi-step:** each row is one stage; carry [AWL](../../../docs/TERMS.md#awl) Appendix D **step [handoff](../../../docs/TERMS.md#handoff)** blocks between steps internally.
- Name **leaf skill** when one exists (see **Routing** below). Read that skill’s `SKILL.md` at execute time.
- Follow [AWL](../../../docs/TERMS.md#awl) Appendix D **tier rules** (T0/T1 compression; scope creep → Phase 3 + re-run Phase 4).
- **[Gate](../../../docs/TERMS.md#gate) on deliverables:** plan **touch list** must name [gate](../../../docs/TERMS.md#gate) shape for each file to be written.
- **Step disposition:** every named step stays on the list until **PASS**, **FAIL**, or **`skip: <reason>`**. Silent omission fails Phase 4.

---

### [AWL](../../../docs/TERMS.md#awl) Phase 4 — Adversarial [plan audit](../../../docs/TERMS.md#plan-audit) (separate execution)

**Do not** implement or generate in the same prose block as Phase 3. Use a **fresh section or subagent pass**. Use [AWL](../../../docs/TERMS.md#awl) **Appendix E** [plan audit](../../../docs/TERMS.md#plan-audit) memo and checklist. **[Fail-closed](../../../docs/TERMS.md#default-closed)** per [AWL](../../../docs/TERMS.md#awl) §4.

Attack plan and statements: unbound items, [god-noun](../../../docs/TERMS.md#god-noun), split adjectives, **[noun inheritance](../../../docs/TERMS.md#noun-inheritance)** (ADR 0008), missing impact, wrong [charter](../../../docs/TERMS.md#charter) class, raw I/O that is not a [primitive](../../../docs/TERMS.md#primitive) function (ADR 0009). **[Hub](../../../docs/TERMS.md#hub):** **`bbp-reviewer`** on the proposal package; findings cite `R*` / `C*` / `P*`.


**Register rows must include:** `GATE-STD` (planned artifacts will ship with §2-compliant gates).

Emit **`## Verdict — Planit plan audit`** per [`operation-verdict-standard.md`](references/operation-verdict-standard.md) §4 before bind close-out and before [AWL](../../../docs/TERMS.md#awl) Phase 5.

**Machine receipt (required while planit is active):** export **[bbp-reviewer](../../../docs/TERMS.md#bbp-reviewer)** Q2 JSON (same shape as adversarial snapshot) and run `./nlc maintainer plan-audit --from <export.json>`. **`./nlc verify` fails** without `.nlc/plan-audit.json` when `.nlc/planit-in-progress.json` is active — prose-only “[audit](../../../docs/TERMS.md#audit) done” is not sufficient.

---

### [PLANIT](../../../docs/TERMS.md#planit) steps 4–5 — Bind and close gaps

**Step 4 — Bind:** every statement points at [requirement](../../../docs/TERMS.md#requirement) ids, [ADR](../../../docs/TERMS.md#adr) ids, **[rule](../../../docs/TERMS.md#rule)** ids when [ADR](../../../docs/TERMS.md#adr) 0007 applies, and **[BBP](../../../docs/TERMS.md#bbp) standard** (always on). No pointer → unbound.


**Step 5 — Close gaps:** loop until every statement is bound. **Do not generate yet.**

Emit **`## Verdict — Planit bind gate`** per §4 before [PLANIT](../../../docs/TERMS.md#planit) step 6. On **FAIL**, stay in step 5.

---

### [AWL](../../../docs/TERMS.md#awl) Phase 5 — Execute (+ PLANIT 6)

Run approved plan steps **in order**. Bind [gate](../../../docs/TERMS.md#gate) must already **PASS**. This phase is generate only — not bind, not [prove](../../../docs/TERMS.md#prove).

1. **Before each step** — confirm prior stop predicate [met](../../../docs/TERMS.md#met); emit §4 verdict when the step blocks downstream work.
2. **Leaf skill step** — read **`.agents/skills/<name>/SKILL.md`** (or `.cursor/skills/`); run [Gate](../../../docs/TERMS.md#gate) → Procedure; [verify](../../../docs/TERMS.md#verify) leaf output meets §2. Inspect files, diffs, and machine exit codes — do not accept a subagent summary as PASS.
3. **Before [PLANIT](../../../docs/TERMS.md#planit) step 6 — [Knowledge domain](../../../docs/TERMS.md#knowledge-domain) (UC18):** run `./nlc maintainer guide before-generate --scope <topic>` (repeat scopes as needed). **FAIL** → [PLANIT](../../../docs/TERMS.md#planit) 1 or 5. See [`references/nlc-before-generate.md`](references/nlc-before-generate.md). Harness doc: [`docs/nlc/HARNESS.md`](../../../docs/nlc/HARNESS.md) (documented; optional hooks in `.nlc/hooks.example.json` only).
4. **[Requirement](../../../docs/TERMS.md#requirement) / [contract](../../../docs/TERMS.md#contract) change (UC9):** if this step is regen after an ADR/rule/verb change, run `python3 tools/nlc-delta-regen.py` first and execute its `steps` in order.
5. **[PLANIT](../../../docs/TERMS.md#planit) steps 2–3 — Plan + atomic actions (ADR 0024 / 0030):** decompose the plan into atomic actions. Each action carries `id`, `plan_step_id`, and `description`. **Before any emit**, run the pipeline wire:
   ```bash
   python3 tools/nlc-pipeline-wire.py --plan <plan.json> --audit <audit.json> \
       --manifest <emit-manifest.json> --action-gates <gates.json>
   ```
   This runs **X1** (action↔plan) then **X2** (reverse audit: every applicable ADR bound to an action). **FAIL → do not emit.** See [`docs/nlc/PIPELINE-WIRING.md`](../../../docs/nlc/PIPELINE-WIRING.md).
5b. **[PLANIT](../../../docs/TERMS.md#planit) step 6 — Generate:** [hub](../../../docs/TERMS.md#hub) implementation only after [charter](../../../docs/TERMS.md#charter) **ratification** (§6 steps 4–5) unless ADR-exempt. Route **`bbp-proposer`**. **One artifact.** Metrics for that artifact must already be in the plan ([ADR 0010](../../../adrs/0010-gate-after-every-generate.md)). Before writing a new path (skill, doc, code), run `./nlc maintainer gate-scope --add <repo-relative-path>` (or rely on `gate-record`, which appends scope). New goal code may start from `./nlc maintainer goal-scaffold --goal <id>` (ADR 0023 markers). [Primitive](../../../docs/TERMS.md#primitive) I/O only via [`integrity/primitives.md`](../../../integrity/primitives.md) names ([ADR 0009](../../../adrs/0009-primitive-interior-functions.md)). At each adopted [rule](../../../docs/TERMS.md#rule) enforcement site emit a machine line `# nlc:rule=<rule_id>` ([ADR 0023](../../../adrs/0023-rule-instance-trace-and-instant-audit-scope.md)) — use `./nlc maintainer rule-marker --id <rule_id>` for the canonical line; after goal `implementation.py` edits run `./nlc maintainer rule-emit --goal <id>` so the [compiler](../../../docs/TERMS.md#compiler) owns receipts (do not hand-paste markers to pass audits). Humans do not edit output to help audits pass. After `domain/` edits run `python3 tools/fitness-no-noun-inheritance.py <adopter-root>` ([ADR 0008](../../../adrs/0008-no-noun-inheritance.md)). **Version class:** when the change is material, confirm patch / minor / major per [`.agents/instructions/change-version-class.md`](../../../.agents/instructions/change-version-class.md).
5c. **After emit — audit + manifest + bound gates (ADR 0030):** the emit must also write `emit-manifest.json` beside the artifact (schema: [`docs/nlc/emit-manifest.schema.json`](../../../docs/nlc/emit-manifest.schema.json)). Re-run the same wire; it now executes **X5** (every emit has an audit), **X3** (manifest schema, `unused=na`, gate closed), and **X6** (gates of ADRs bound to this action, default-closed). **FAIL → stop; do not start the next row.** PASS → `./nlc maintainer gate-record --artifact <path> --gate-id <id> --command "<fitness cmd>"` then next statement only.
6. **[PLANIT](../../../docs/TERMS.md#planit) step 6.5 — [Gate](../../../docs/TERMS.md#gate) that artifact:** run the named metrics immediately. Default fail. FAIL → stop; do not start the next row. PASS → `./nlc maintainer gate-record --artifact <path> --gate-id <id> --command "<fitness cmd>"` then next statement only.

7. **Inline step** — cite commands and exit codes of the **artifact under test**. INCONCLUSIVE is BLOCKED.
8. **KCR sub-gate** — if step touches durable **ai vault** layers, **stop** until KCR accepted ([`references/knowledge-change-review-standard.md`](references/knowledge-change-review-standard.md)); prefer routing to **`~/.agents/skills/planit`**.
9. **Failure** — [jidoka](../../../docs/TERMS.md#jidoka): stop; [RCA](../../../docs/TERMS.md#rca) if non-trivial ([`references/root-cause-analysis-standard.md`](references/root-cause-analysis-standard.md) or `/conduct-root-cause-analysis`); then [PLANIT](../../../docs/TERMS.md#planit) **1** or **5**, then **6** again. Do not patch generated files to silence audits.
10. **[Handoff](../../../docs/TERMS.md#handoff) between steps** — [AWL](../../../docs/TERMS.md#awl) Appendix D step [handoff](../../../docs/TERMS.md#handoff) template.
11. **Pre-write check** — no durable file write until target artifact’s **[Gate](../../../docs/TERMS.md#gate)** (§2) is defined in plan or draft.
12. **UC21 gate-scope** — after each durable generate under `.agents/`, `goals/`, or `domain/`, run `./nlc maintainer gate-scope --add <repo-relative-path>`; record `gate-record` when PLANIT 6.5 PASS applies.

---

### [PLANIT](../../../docs/TERMS.md#planit) step 7 — [Prove](../../../docs/TERMS.md#prove) (compile, not ship)

**Both** required:

1. **Machine [gate](../../../docs/TERMS.md#gate)** — [hub](../../../docs/TERMS.md#hub): **`bbp-confirmer`** (`python3 tools/ci_fitness.py` + [charter](../../../docs/TERMS.md#charter) §11 with evidence). [Adopter](../../../docs/TERMS.md#adopter): the fitness suite that tree bound. Exit non-zero = fail.
2. **Adversarial [audit](../../../docs/TERMS.md#audit)** — separate from the generator: statements done, bindings held, no second copy of an [adjective](../../../docs/TERMS.md#adjective) inside a [goal](../../../docs/TERMS.md#goal).

Compile-green is not released. **[Ship](../../../docs/TERMS.md#ship)** is later: `python3 tools/release-audit.py <tree>` after a human writes `Released-by:` (and `Ratified-by:` when class A/B/D/E/F). Do not treat [prove](../../../docs/TERMS.md#prove) PASS as [ship](../../../docs/TERMS.md#ship). Do not write those lines as the [confirmer](../../../docs/TERMS.md#confirmer).

Emit **`## Verdict — Planit prove`** per §4 when step 7 completes.


---

### [AWL](../../../docs/TERMS.md#awl) Phase 6 — Adversarial execution [audit](../../../docs/TERMS.md#audit) (separate execution)

Separate from Phase 5 prose — **fresh section or subagent pass**. Use [AWL](../../../docs/TERMS.md#awl) **Appendix E** execution [audit](../../../docs/TERMS.md#audit) memo and **Appendix B** meta-audit checklist (T2+). **[Fail-closed](../../../docs/TERMS.md#default-closed)** per [AWL](../../../docs/TERMS.md#awl) §4.

Re-check bindings vs diff; [prove](../../../docs/TERMS.md#prove) evidence is the **artifact under test**. **[Hub](../../../docs/TERMS.md#hub):** [charter](../../../docs/TERMS.md#charter) §11 rows and fitness output present.

**Domain instances** (orchestration hooks — use global Planit when primary):

- **DSI converge** — [`references/local-dsi-converge-audit-template.md`](references/local-dsi-converge-audit-template.md)
- **Vault PR (ai vault)** — `/local-review-pr` via **`~/.agents/skills/planit`**

**Required:** `GATE-STD` row **PASS** for every produced artifact path, or **FAIL** with fix list.

**Hub compile-system SSOT:** when the diff touches **`TODO` → Build a compiled system** or **`docs/USE-CASES.md`** spine, Phase 6 must cite `python3 tools/fitness-todo-use-cases-ssot.py` → `RESULT:MET` and any updates to [`integrity/uc-product-status.json`](../../../integrity/uc-product-status.json).

Emit **`## Verdict — Planit execution audit`** per §4 before Phase 7.

**Machine receipt:** app repos with compiled `goals/**/implementation*` need `.nlc/change-adversarial.json` (Q2) and `.nlc/produce-package.json` (Q1 + SSOT + Q2) on **`./nlc verify-deep`**. Set `producer_role` and `adversarial_auditor_role` to different loop roles (e.g. `bbp-proposer` vs `bbp-reviewer`) — same value fails verify ([ADR 0003](../../../adrs/0003-systems-extension-agent-nouns.md)). [Hub](../../../docs/TERMS.md#hub) material changes refresh `.nlc/produce-package.json` after **[bbp-reviewer](../../../docs/TERMS.md#bbp-reviewer)**.

---

### [AWL](../../../docs/TERMS.md#awl) Phase 7 — Record and propagate (+ hub §6 step 8)

Follow [AWL](../../../docs/TERMS.md#awl) **Appendix F** ([`references/domain-first-authoring.md`](references/domain-first-authoring.md) for back-propagation). **[Hub](../../../docs/TERMS.md#hub):** **`bbp-recorder`** (ADR or “no ADR, reason”).

Emit user-facing **[Handoff](../../../docs/TERMS.md#handoff)** for T2+ multi-step work. [Handoff](../../../docs/TERMS.md#handoff) must include:

- Produced artifact paths
- **Gate-standard compliance:** per-path **PASS** / **FAIL** / **N/A** for §2
- Open fix list when any path is **FAIL**

Emit **`## Verdict — Planit process`** (process-level §5 rollup). **PASS** only when intake, [plan audit](../../../docs/TERMS.md#plan-audit), bind [gate](../../../docs/TERMS.md#gate), [prove](../../../docs/TERMS.md#prove), and execution [audit](../../../docs/TERMS.md#audit) verdicts are **PASS**.

---

## Routing quick reference

| Outcome slice | Leaf skill / route |
| ------------- | ------------------ |
| Proposal / implement (hub) | `bbp-proposer` |
| Adversarial review | `bbp-reviewer` |
| [Prove](../../../docs/TERMS.md#prove) + [hub](../../../docs/TERMS.md#hub) fitness | `bbp-confirmer` |
| [ADR](../../../docs/TERMS.md#adr) / record | `bbp-recorder` |
| [Knowledge domain](../../../docs/TERMS.md#knowledge-domain) facts / gaps | `agents/knowledge-steward` |
| Root cause | `/conduct-root-cause-analysis` or `references/root-cause-analysis-standard.md` |
| DSI, [greenfield](../../../docs/TERMS.md#greenfield) WO, make-a-skill, ai vault `local-*` | **`~/.agents/skills/planit`** |

When no leaf skill fits, execute inline under this procedure with full [AWL](../../../docs/TERMS.md#awl) audits and §2 on all outputs.

---

## Reference files

| File | Use |
| ---- | --- |
| [`references/README.md`](references/README.md) | Vendored [AWL](../../../docs/TERMS.md#awl) norms + sync policy |
| [`references/planit-process.md`](references/planit-process.md) | [PLANIT](../../../docs/TERMS.md#planit) steps summary |
| [`references/hub-charter-loop.md`](references/hub-charter-loop.md) | [Charter](../../../docs/TERMS.md#charter) §6 [hub](../../../docs/TERMS.md#hub) mapping |
| [`docs/ai-compiled-systems/PLANIT-ORCHESTRATION.md`](../../../docs/ai-compiled-systems/PLANIT-ORCHESTRATION.md) | Combined spine |
| [`.agents/bbp-short-form.md`](../../bbp-short-form.md) | [Charter](../../../docs/TERMS.md#charter) §15 |

---

## [NLC](../../../docs/TERMS.md#nlc) shell (agent-invoked — ADR 0020)

From the [adopter](../../../docs/TERMS.md#adopter) [app repo](../../../docs/TERMS.md#adopter) root, **you** run machine steps; do not ask the human to run these between chat turns:

- `./nlc` — refresh queue after durable writes
- `./nlc maintainer requirements` after requirements ratified
- `./nlc verify-deep` then `./nlc verify` at [PLANIT](../../../docs/TERMS.md#planit) step 7
- `./nlc maintainer guide planit-start --label "…"` while a build session is open; `./nlc maintainer guide planit-end` when done
- **[UC9](../../../docs/TERMS.md#uc9) regen queue:** `./nlc maintainer regen-continue` → one [goal](../../../docs/TERMS.md#goal) via [PLANIT](../../../docs/TERMS.md#planit) → `./nlc maintainer regen-advance`

---

## Done signals

- Intake **[Gate](../../../docs/TERMS.md#gate)** **PASS** with §4 verdict emitted
- Applicability register closed (AWL Phase 2)
- [Plan audit](../../../docs/TERMS.md#plan-audit) **PASS** with `GATE-STD` planned — every named step PASS, FAIL, or `skip: <reason>` — §4 verdict before execute
- Bind [gate](../../../docs/TERMS.md#gate) **PASS** before generate
- Each generate has metrics in the plan; each artifact is gated **before** the next statement (ADR 0010)
- [Prove](../../../docs/TERMS.md#prove) **PASS** (machine + adversarial); [hub](../../../docs/TERMS.md#hub) [confirmer](../../../docs/TERMS.md#confirmer) output when [hub](../../../docs/TERMS.md#hub) touched. [Prove](../../../docs/TERMS.md#prove) is compile, not [ship](../../../docs/TERMS.md#ship).

- [Ship](../../../docs/TERMS.md#ship) is optional in this skill: `python3 tools/release-audit.py <tree>` after a human `Released-by:` — not part of process PASS

- Execution [audit](../../../docs/TERMS.md#audit) **PASS** with `GATE-STD` on delivered artifacts; evidence is the artifact under test, not a delegate summary — §4 verdict before record
- Appendix B meta-audit **PASS** when T2+
- Phase 7 [handoff](../../../docs/TERMS.md#handoff) includes per-artifact gate-standard compliance
- **Process result: PASS** only when every required phase verdict is **PASS**
