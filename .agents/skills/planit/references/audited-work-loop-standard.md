# Audited work loop (AWL)

Normative **org-wide** process for work that produces output in the metaprompt system and in workflows compiled from it. **Canonical for fiqit/metaprompts** when exported from this vault; not specific to one repository layout.

**Related:** [`operation-verdict-standard.md`](operation-verdict-standard.md) (objective PASS/FAIL per operation and process), [`information-completion-contract.md`](information-completion-contract.md), [`domain-first-authoring.md`](domain-first-authoring.md), [`knowledge-change-review-standard.md`](knowledge-change-review-standard.md), [`lean-operating-principles.md`](lean-operating-principles.md), [`report-pyramid-structure.md`](report-pyramid-structure.md), [`root-cause-analysis-standard.md`](root-cause-analysis-standard.md), [`agent-failure-modes-and-meta-prompt-patterns.md`](agent-failure-modes-and-meta-prompt-patterns.md), [`local-dsi-converge-audit-template.md`](local-dsi-converge-audit-template.md).

---

## 1. Purpose

Deliver **high-quality, already audited** outputs — plans, standards, prompts, skills, code, consumer artifacts — by executing **seven distinct phases**. Each phase has a stop predicate; do not start the next phase until the prior phase passes.

**Self-reflexive:** Authoring or amending this standard, and all **future** metaprompt artifacts, must follow [AWL](../../../../docs/TERMS.md#awl). Phase 6 **meta-audit** confirms Phases 0–7 were followed.

---

## 2. Enforcement policy

| Scope | [Rule](../../../../docs/TERMS.md#rule) |
| ----- | ---- |
| **Future create** | New prompts under `prompts/`, new `metaprompts/vault-intents/`, new materialized skills, and new `.cursor/skills/` / `.cursor/prompts/` maintainer packs **must** embed [AWL](../../../../docs/TERMS.md#awl) in Gate/Procedure (phase map + stop predicates). **Non-compliant artifacts do not belong in the metaprompt system.** |
| **Existing catalog** | **Grandfathered** until a maintainer **edits** the artifact. From the first edit forward, [AWL](../../../../docs/TERMS.md#awl) applies; no mass rewrite required in the same PR unless scope demands it. |
| **DSI** | [`local-dsi-converge-audit-template.md`](local-dsi-converge-audit-template.md) is a **Phase 6 execution-audit instance** for converge — not a separate process. |
| **Export** | When [AWL](../../../../docs/TERMS.md#awl) is extracted to **fiqit/metaprompts**, this file remains the normative source until sync rules say otherwise (tracked on export branch). |

---

## 3. Seven phases (distinctly executed)

| Phase | Name | Primary output | Stop predicate |
| ----- | ---- | -------------- | -------------- |
| **0** | Authorize and bound | One-line outcome; in/out scope | User order or skill invocation satisfies authorization ([`lean-operating-principles.md`](lean-operating-principles.md) §2 — no re-confirm) |
| **1** | Intake | Resolution table | Blocking inputs resolved, [waived](../../../../docs/TERMS.md#waived), or `Assumption:` ([`information-completion-contract.md`](information-completion-contract.md)); **tier** proposed or confirmed for T2+ (Appendix C) |
| **2** | Applicability register | Register table (Appendix A) | Every norm that could apply is listed or excluded with reason |
| **3** | Plan | Plan: steps, touch list, stop predicates, risks, rollback | Plan reviewable without reading implementation |
| **4** | Adversarial [plan audit](../../../../docs/TERMS.md#plan-audit) | [Audit](../../../../docs/TERMS.md#audit) memo: **PASS/FAIL** apex + per-register rows | **[Fail-closed](../../../../docs/TERMS.md#default-closed)** — see §4 |
| **5** | Execute | Delivered artifacts | Only approved plan steps; scope creep → Phase 3 |
| **6** | Adversarial execution [audit](../../../../docs/TERMS.md#audit) | [Audit](../../../../docs/TERMS.md#audit) memo + cited evidence | **[Fail-closed](../../../../docs/TERMS.md#default-closed)** — same register as Phase 4, checked on **delivered** artifacts |
| **7** | Record and propagate | KCR/registry/handoff/RCA as applicable | [`domain-first-authoring.md`](domain-first-authoring.md) §2 step 6; no "done" with failing gates |

Phases **4** and **6** are **separate executions** from Phases **3** and **5** (different section, turn, or agent pass — not the same prose block as "and then I checked").

---

## 4. Adversarial [audit](../../../../docs/TERMS.md#audit) (definition)

**Adversarial [audit](../../../../docs/TERMS.md#audit)** — independent verification with a **[fail-closed](../../../../docs/TERMS.md#default-closed)** posture:

1. **Assume the artifact will cheat** — no "I verified" without evidence (command + exit code, file path, validator name, grep/spot check).
2. **Closed world over the applicability register** — every Phase 2 row is **PASS**, **FAIL**, or **[waived](../../../../docs/TERMS.md#waived)** (human acceptance recorded).
3. **[Fail-closed](../../../../docs/TERMS.md#default-closed)** — FAIL blocks Phase 5 (after plan audit) or completion (after execution audit); fix and re-audit — do not hand off downstream ([`lean-operating-principles.md`](lean-operating-principles.md) §1 [jidoka](../../../../docs/TERMS.md#jidoka)).
4. **Report pyramid** — [audit](../../../../docs/TERMS.md#audit) memos lead with verdict ([`report-pyramid-structure.md`](report-pyramid-structure.md)).
5. **Operation verdict** — each phase and machine [gate](../../../../docs/TERMS.md#gate) ends with an explicit **PASS | FAIL | BLOCKED** and objective evidence ([`operation-verdict-standard.md`](operation-verdict-standard.md)).
6. **Meta-audit** — for vault/metaprompt work, Phase 6 includes: "Did this work follow Phases 0–7?" including [plan audit](../../../../docs/TERMS.md#plan-audit) before durable writes.

**Subtypes:** **[Plan audit](../../../../docs/TERMS.md#plan-audit)** (Phase 4) and **execution [audit](../../../../docs/TERMS.md#audit)** (Phase 6). Same rules; different evidence (plan text vs delivered files and machine gates).

**Not adversarial:** self-attestation only, advisory notes without PASS/FAIL, or re-running the same generative pass that produced the artifact with no independent checks.

---

## 5. Tier table (ceremony vs risk)

| Tier | When | Phases 3–4 | Phase 6 |
| ---- | ---- | ---------- | ------- |
| **T0** | Trivial fix (typo, one-line) | Compressed plan in chat + mental checklist | Minimal spot check |
| **T1** | Single-file vault edit | Short plan + register subset | Validator/link check cited |
| **T2** | New standard, skill, intent, or pack | Full plan + full register | Full adversarial [audit](../../../../docs/TERMS.md#audit) + evidence |
| **T3** | Cross-cutting org policy | KCR + registry + ripple plan | VPR author_preflight + [audit](../../../../docs/TERMS.md#audit) memo |

Authoring or amending **this standard** is **T2 minimum**.

**Authorized skill runs:** Phase 0 may be satisfied by invocation (`/planit` — [PLANIT](../../../../docs/TERMS.md#planit) / [AWL](../../../../docs/TERMS.md#awl) orchestrator), `/local-author-or-extend-knowledge` (vault durable authoring), `/local-dsi-converge`, etc.). Do **not** re-confirm authorized work ([`lean-operating-principles.md`](lean-operating-principles.md) §2). Phase 3 may compress; Phases 4 and 6 still run (may be lightweight for T0/T1).


**General orchestrator:** For arbitrary multi-step work (vault or consumer), invoke **`skills/planit/SKILL.md`** (`/planit`). It runs the full loop, routes steps to leaf skills, and keeps plan/execution audits distinct. Vault-only durable-knowledge authoring may use `/local-author-or-extend-knowledge` directly or as a routed step inside [Planit](../../../../docs/TERMS.md#planit).

---

## 6. Sub-gates (orchestrated, not replaced)

| [Gate](../../../../docs/TERMS.md#gate) | [AWL](../../../../docs/TERMS.md#awl) phase | Standard |
| ---- | --------- | -------- |
| Resolution table before deliverable writes | 1 | [`information-completion-contract.md`](information-completion-contract.md) |
| KCR before durable standards/manifests/intents | 5 (before write) | [`knowledge-change-review-standard.md`](knowledge-change-review-standard.md) |
| [RCA](../../../../docs/TERMS.md#rca) before workaround | 5–6 on failure | [`root-cause-analysis-standard.md`](root-cause-analysis-standard.md) |
| DSI machine stop + converge [audit](../../../../docs/TERMS.md#audit) template | 6 instance | [`local-dsi-converge-audit-template.md`](local-dsi-converge-audit-template.md) |

---

## 7. Future prompts and skills (required shape)

Every **new** or **first edited** prompt/skill/intent **must** include:

1. **`uses_standards`** listing `standards/audited-work-loop-standard.md` (plus others).
2. **[Gate](../../../../docs/TERMS.md#gate)** — maps to Phases 0–1 (inputs, resolution table); **[default-closed](../../../../docs/TERMS.md#default-closed)** with **testable true/false** blocking criteria per [`operation-verdict-standard.md`](operation-verdict-standard.md) §2.
3. **Procedure** — maps steps to Phases 2–7 or cites a pipeline that does.
4. **Stop predicates** — explicit PASS/FAIL for [plan audit](../../../../docs/TERMS.md#plan-audit) and execution [audit](../../../../docs/TERMS.md#audit) where the skill produces durable output.

Prompts that only compose existing stages must reference [AWL](../../../../docs/TERMS.md#awl) in the orchestration map or parent skill.

---

## 8. Compliance review (v1)

- **Author:** Run Phase 4/6 checklists (Appendix E); cite evidence in [handoff](../../../../docs/TERMS.md#handoff) (Appendix F).
- **Reviewer:** [`vault-pull-request-review-standard.md`](vault-pull-request-review-standard.md) + **`/local-review-pr`** author_preflight for new/touched consumer prompts.
- **Automated [gate](../../../../docs/TERMS.md#gate):** deferred (human checklist v1); optional scripted VPR [gate](../../../../docs/TERMS.md#gate) in a follow-on change.

---

## Appendix A — Applicability register (Phase 2 artifact)

Copy this table for each work item; add rows until closed world is satisfied.

| Id | Source path | Applies because | Gates phase(s) | [Audit](../../../../docs/TERMS.md#audit) evidence |
| -- | ----------- | --------------- | -------------- | -------------- |
| AWL-1 | `standards/audited-work-loop-standard.md` | All metaprompt output | 4, 6 | Phase checklist PASS; meta-audit |
| ICC-1 | `standards/information-completion-contract.md` | Produces deliverables | 1, 5 | Resolution table present |
| KCR-1 | `standards/knowledge-change-review-standard.md` | Touches durable layers | 5 | Accepted KCR path |
| RCA-1 | `standards/root-cause-analysis-standard.md` | Failure or workaround risk | 5–6 | [RCA](../../../../docs/TERMS.md#rca) path if triggered |
| DFA-1 | `standards/domain-first-authoring.md` | Net-new policy/domain facts | 3, 5, 7 | Standards before prompts |
| VPR-1 | `standards/vault-pull-request-review-standard.md` | Vault PR planned | 6–7 | author_preflight report |
| GATE-STD | `standards/operation-verdict-standard.md` §2 | Produces runnable or durable artifacts | 3–7 | Per-path [gate](../../../../docs/TERMS.md#gate) compliance PASS/FAIL |

Add domain-specific rows until closed world is satisfied. **Excluded row (required when skipping a norm):** path · reason not applicable.

---

## Appendix B — Meta-audit checklist (Phase 6, vault work)

- [ ] Phase 0 authorization recorded (user order or skill)
- [ ] Phase 1 resolution table emitted before durable writes
- [ ] Phase 2 applicability register complete
- [ ] Phase 4 [plan audit](../../../../docs/TERMS.md#plan-audit) **PASS** (or waived with acceptance) **before** Phase 5 durable writes
- [ ] Phase 6 execution [audit](../../../../docs/TERMS.md#audit) **PASS** with cited evidence
- [ ] Phase 7 registry/KCR/handoff updated as applicable

---

## Appendix C — Intake inputs (Phase 1)

Emit a **resolution table** before plan or durable writes ([`information-completion-contract.md`](information-completion-contract.md)).

**Tier compression:** For **T0** and **T1** ([§5](#5-tier-table-ceremony-vs-risk)), a compressed resolution table is sufficient — outcome, scope, and proposed tier with rationale. For **T2** and **T3**, include every **blocking** row below (or record `Waived` / `Assumption:` where allowed).

| Input | Blocking? | Notes |
| ----- | --------- | ----- |
| `{{REPO_ROOT}}` | yes | Propose from workspace |
| Monorepo subpath | when nested | Whole repo vs subfolder |
| Outcome (one paragraph) | yes | Problem, user, success shape |
| Tier (T0–T3) | yes (T2+) | Propose from scope; user may override |
| Touch surfaces | yes (T2+) | Files, skills, repos, environments |
| Multi-step? | yes (T2+) | Single pass vs staged plan |
| Durable vault layers? | when yes | Triggers KCR sub-gate in Phase 5 |
| Consumer smoke required? | when behavior changes | VPR / smoke-check routing |

**Blocking questions** — numbered list; **stop** the turn if any blocking row is missing (max one round unless contradiction):

1. What is the **success shape** (artifact, command exit, observable behavior)?
2. **In scope / out of scope** for this session?
3. **Tier** proposal (T0 typo … T3 cross-cutting) with one-line rationale?
4. If multi-step: rough **stage count** and whether stages run **sequentially in this session** or hand off?

---

## Appendix D — Plan artifact (Phase 3) and step [handoff](../../../../docs/TERMS.md#handoff) (Phase 5)

Produce a plan **reviewable without reading implementation**:

```markdown
## Plan

**Outcome:**
**Tier:**
**Touch list:**
**Rollback:**

### Steps

| # | Step | Procedure | Stop predicate | Audit hook |
| - | ---- | --------- | -------------- | ---------- |
| 1 | … | inline or delegated workflow | … | Phase 6 spot / gate |
```

**Procedure** column may name a leaf skill, script, or inline agent work. Orchestrators may add a **Leaf skill** column when routing to repo-local or org skills.

**Tier rules:**

- **T0/T1:** compressed plan (≤5 steps) allowed.
- **T2/T3:** full touch list, risks, rollback, and per-step [audit](../../../../docs/TERMS.md#audit) hooks.
- **Scope creep** during Phase 5 → return to Phase 3, re-run Phase 4.

**Multi-step [handoff](../../../../docs/TERMS.md#handoff)** (internal, between Phase 5 steps):

```markdown
### Step N handoff

- Done:
- Evidence:
- Next step:
```

**T2/T3 multi-step:** after each major step, optional **step verification** (command + exit code or spot check) before continuing.

**Step disposition:** every named plan step remains on the list until **PASS**, **FAIL**, or **`skip: <reason>`**. Dropping a named step without an explicit skip is a Phase 4 **FAIL**. Stop predicates that cannot be decided are **BLOCKED** ([`operation-verdict-standard.md`](operation-verdict-standard.md) §3), not implied PASS.

---

## Appendix E — [Audit](../../../../docs/TERMS.md#audit) memos and checklists (Phases 4 and 6)

Phases **4** and **6** are **separate executions** from Phases **3** and **5** — use a fresh section, turn, or subagent pass.

### Phase 4 — [Plan audit](../../../../docs/TERMS.md#plan-audit) memo

Shape per [`report-pyramid-structure.md`](report-pyramid-structure.md):

```markdown
## Plan audit — PASS | FAIL

**Verdict:** …
**Next action if FAIL:** …

| Register Id | Result | Evidence |
| ----------- | ------ | -------- |
| AWL-1 | PASS/FAIL/waived | … |
```

**[Fail-closed](../../../../docs/TERMS.md#default-closed):** **FAIL** blocks Phase 5 (no durable writes, no destructive commands) until plan fixed and Phase 4 re-run **PASS**.

**Checks:**

- Plan covers every register row or justified exclusion.
- Steps have stop predicates and [audit](../../../../docs/TERMS.md#audit) hooks appropriate to tier.
- Every named step has disposition PASS, FAIL, or `skip: <reason>` — no silent omission.
- KCR listed before any durable vault write step.
- Multi-step order is coherent; no missing [handoff](../../../../docs/TERMS.md#handoff) between stages.

### Phase 6 — Execution [audit](../../../../docs/TERMS.md#audit) memo

```markdown
## Execution audit — PASS | FAIL

**Verdict:** …
**Evidence summary:** …

| Register Id | Result | Evidence (path, command, exit) |
| ----------- | ------ | ------------------------------ |
```

Include **meta-audit** (Appendix B): Phase 4 **PASS** before durable writes; Phases 0–7 followed.

**FAIL** → remediate and re-audit; no “done” [handoff](../../../../docs/TERMS.md#handoff).

Domain-specific execution-audit instances (for example DSI converge, vault PR author_preflight) are **orchestration hooks** — cite the applicable standard or skill; do not duplicate their full checklists here.

---

## Appendix F — Record and user [handoff](../../../../docs/TERMS.md#handoff) (Phase 7)

As applicable ([`domain-first-authoring.md`](domain-first-authoring.md)):

- KCR path + status
- `registry/` entry for durable vault changes
- [RCA](../../../../docs/TERMS.md#rca) under `draft/rca/` if failure occurred
- Consumer smoke record if behavior changed
- Materialize/parity when vault skills touched

**User-facing [handoff](../../../../docs/TERMS.md#handoff)** (optional; recommended for T2+ multi-step work):

```markdown
## Handoff

- **Outcome:**
- **Tier:**
- **Plan audit:** PASS (date/turn)
- **Execution audit:** PASS (date/turn)
- **Deliverables:**
- **Evidence:**
- **Registry / KCR / RCA:**
- **Next:**
```
