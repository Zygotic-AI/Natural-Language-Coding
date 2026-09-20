# Operation verdict standard

Normative rules for **gates and pass/fail at the end of every operation**: every produced artifact has a **[default-closed](../../../../docs/TERMS.md#default-closed)** [gate](../../../../docs/TERMS.md#gate) whose criteria are **individually testable**; each operation must have **objective, measurable** success criteria; when a verdict is recorded or displayed, it must be **unmistakable** — even when warnings, conditionals, or incidentals appear in the same output.

**Related:** [`report-pyramid-structure.md`](report-pyramid-structure.md) (apex verdict first), [`audited-work-loop-standard.md`](audited-work-loop-standard.md) (Phase 4/6 PASS|FAIL), [`information-completion-contract.md`](information-completion-contract.md) (intake gate profile), [`lean-operating-principles.md`](lean-operating-principles.md) (jidoka — do not pass failing gates downstream), [`agent-failure-modes-and-meta-prompt-patterns.md`](agent-failure-modes-and-meta-prompt-patterns.md) §7 (verification), [`local-dsi-converge-audit-template.md`](local-dsi-converge-audit-template.md) (100% PASS / FAIL labels).

---

## 1. Scope

An **operation** is any bounded unit of work with a defined outcome, including:

- A skill **[Gate](../../../../docs/TERMS.md#gate)** or **Procedure** step
- A shell command or script invocation
- An [AWL](../../../../docs/TERMS.md#awl) **phase** (especially adversarial plan audit and execution audit)
- A machine [gate](../../../../docs/TERMS.md#gate) (`stop_check.py`, validator, preflight)
- A maintainer **[handoff](../../../../docs/TERMS.md#handoff)** or **[audit](../../../../docs/TERMS.md#audit)** section

Every operation in a skill, prompt, pipeline, or runbook **must** declare how PASS and FAIL are measured **before** the operation runs.

---

## 2. [Gate](../../../../docs/TERMS.md#gate) design (produced artifacts)

Every **produced** runnable artifact — published prompt, skilletted skill, repo-local `.cursor/prompts/` or `.cursor/skills/` pack, pipeline stage, [AWL](../../../../docs/TERMS.md#awl) phase with a stop, or machine preflight — **must** include at least one **[Gate](../../../../docs/TERMS.md#gate)** (or equivalent gate subsection) that controls whether downstream work may proceed.

### 2.1 [Default-closed](../../../../docs/TERMS.md#default-closed) posture

| [Rule](../../../../docs/TERMS.md#rule) | [Requirement](../../../../docs/TERMS.md#requirement) |
| ---- | ----------- |
| **[Default-closed](../../../../docs/TERMS.md#default-closed)** | Until the [gate](../../../../docs/TERMS.md#gate) **PASS**es, the agent **must not** run deliverable writes, destructive commands, or dependent procedure steps. Unmet, waived-without-authority, or ambiguous criteria ⇒ **FAIL** or **BLOCKED** — not proceed-with-caveats. |
| **No soft open** | Forbidden: “mostly ready,” “good enough,” “continue unless blocked,” or implied PASS from partial satisfaction. |
| **Machine authoritative** | When a machine [gate](../../../../docs/TERMS.md#gate) exists for a criterion, its result overrides chat self-attestation ([§3](#3-objective-success-criteria)). |
| **[Jidoka](../../../../docs/TERMS.md#jidoka)** | A failing [gate](../../../../docs/TERMS.md#gate) **stops** the [workflow](../../../../docs/TERMS.md#workflow) at source ([`lean-operating-principles.md`](lean-operating-principles.md) §1). |

### 2.2 Testable criteria (true/false)

Each **blocking** [gate](../../../../docs/TERMS.md#gate) criterion must be **individually decidable** as **true** or **false** from cited evidence before the [gate](../../../../docs/TERMS.md#gate) may PASS.

| [Requirement](../../../../docs/TERMS.md#requirement) | [Rule](../../../../docs/TERMS.md#rule) |
| ----------- | ---- |
| **One criterion, one test** | Split compound checks into separate rows. Forbidden: “inputs look fine” or “repo seems healthy.” |
| **Evidence type named** | Each row states *how* to test: exit code, file path exists, JSON field value, grep/count threshold, explicit human acceptance on record, validator id + exit code. |
| **Blocking vs optional** | Mark each row **blocking** or **optional**. Optional rows do not block PASS; blocking rows must all be **true**. |
| **Declared before run** | Criteria appear in **[Gate](../../../../docs/TERMS.md#gate)**, **Validation**, or an cited standard **before** execution — not invented after the fact. |

**Authoring shape (skills and prompts):** use a numbered [gate](../../../../docs/TERMS.md#gate) list or a table:

| Criterion | Blocking? | Pass when (true if…) | Evidence |
| --------- | --------- | -------------------- | -------- |
| … | yes / no | objective condition | command, path, or acceptance record |

**[Gate](../../../../docs/TERMS.md#gate) PASS:** every **blocking** row is **true**. Then emit the §4 verdict block with **`Result: PASS`**.

**[Gate](../../../../docs/TERMS.md#gate) FAIL:** any **blocking** row is **false** ⇒ **`Result: FAIL`**; do not proceed.

**[Gate](../../../../docs/TERMS.md#gate) BLOCKED:** a required test could not run (missing input, tool, or environment) ⇒ **`Result: BLOCKED`**.

### 2.3 [Gate](../../../../docs/TERMS.md#gate) profiles (specializations)

These are **profiles** of §2 — do not redefine [default-closed](../../../../docs/TERMS.md#default-closed) or testable criteria:

| Profile | Standard | When |
| ------- | -------- | ---- |
| **Intake / deliverable-write** | [`information-completion-contract.md`](information-completion-contract.md) | Phase 1 resolution table; no primary deliverables until information-complete |
| **Plan / execution [audit](../../../../docs/TERMS.md#audit)** | [`audited-work-loop-standard.md`](audited-work-loop-standard.md) §4 | Phases 4 and 6 adversarial audits |
| **Skilletted skill [Gate](../../../../docs/TERMS.md#gate) section** | [`skillet-export.md`](skillet-export.md) §4 | Compiled `SKILL.md` body; [compiler](../../../../docs/TERMS.md#compiler) `GATE_SNIPPET` is the **intake** profile |
| **Machine [gate](../../../../docs/TERMS.md#gate)** | Domain scripts (`stop_check.py`, `validate-skills.mjs`, …) | Exit code + structured output (`ok: true`) |

New profiles must cite this section and add only **domain-specific criteria rows**, not a weaker posture.

### 2.4 Anti-patterns

- [Gate](../../../../docs/TERMS.md#gate) with no blocking criteria (everything de facto optional).
- Criteria that require subjective judgment without a recorded acceptance path.
- PASS declared while a blocking row is false or untested.
- Separate “validation” section that contradicts or bypasses **[Gate](../../../../docs/TERMS.md#gate)**.

---

## 3. Objective success criteria

| [Requirement](../../../../docs/TERMS.md#requirement) | [Rule](../../../../docs/TERMS.md#rule) |
| ----------- | ---- |
| **Measurable** | PASS/FAIL must be decidable from cited evidence — exit code, validator name + exit code, file path + hash/count, JSON field (`ok: true`), threshold comparison — not mood or narrative confidence. |
| **Declared upfront** | Skills and prompts state criteria in [Gate](../../../../docs/TERMS.md#gate), Procedure, or **Done signals** before execution. Ad-hoc operations in chat must state criteria immediately before running. |
| **[Fail-closed](../../../../docs/TERMS.md#default-closed)** | If evidence is missing or ambiguous, verdict is **FAIL** or **BLOCKED** — not PASS with caveats. **INCONCLUSIVE** (could not tell whether the criterion holds) is **BLOCKED**, never PASS. |
| **Machine first** | When a machine [gate](../../../../docs/TERMS.md#gate) exists, its result is authoritative over chat self-attestation. |
| **Real artifact** | Evidence must be the **artifact under test**: command + exit code of the check that proves the outcome, validator JSON, file contents, or runtime output of the failing path re-run. |

**Forbidden as sole evidence:** compile- or lint-only when the claimed [defect](../../../../docs/TERMS.md#defect) was runtime; cached or derived freshness; a **delegate or subagent summary** without inspecting the produced files, diff, or machine output.

**Examples:**

| Operation | PASS (objective) | FAIL (objective) |
| --------- | ---------------- | ---------------- |
| Script | Exit code **0** | Exit code **≠ 0** |
| `stop_check.py` | JSON `ok: true`, exit **0** | `ok: false` or exit **≠ 0** |
| Unit tests | All tests pass, exit **0** | Any failure or exit **≠ 0** |
| Upload preflight | Indexes exist; `az account show` exit **0** | Missing index or az exit **≠ 0** |
| KCR | Reviewer **accepted** path recorded | Open blocking items |

---

## 4. Required verdict emission

At the **end** of each operation (before starting the next dependent operation), emit:

```markdown
## Verdict — <operation id or name>

**Result:** PASS | FAIL | BLOCKED

**Evidence:** <one line — command + exit code, validator id, or metric>

**Next:** <immediate next action, or `none` if PASS and no follow-up>
```

Rules:

1. **`Result`** must be exactly one of **PASS**, **FAIL**, or **BLOCKED** (blocked = could not run; missing input or environment).
2. **`Evidence`** must cite the objective measure from §3 and, for gates, show which blocking criteria evaluated **true**.
3. Do **not** substitute soft labels (`OK`, `success`, `clean`, `mostly passed`, `PASS with caveats`) for **`Result`**.
4. Follow [`report-pyramid-structure.md`](report-pyramid-structure.md): when the verdict is part of a longer report, this block is the **apex** (first readable block after the title).

---

## 5. Verdict vs conditionals and incidentals

When output includes warnings, advisories, assumptions, or optional notes **in the same turn or file** as a verdict:

| [Rule](../../../../docs/TERMS.md#rule) | [Requirement](../../../../docs/TERMS.md#requirement) |
| ---- | ----------- |
| **Separation** | Put **`Result: PASS | FAIL | BLOCKED`** in the verdict block (§4). Put conditionals under a **distinct** heading — e.g. `### Incidentals (verdict unchanged)` or `### Advisories (non-blocking)`. |
| **No verdict drift** | Incidentals **must not** alter the stated **`Result`**. If an incidental should change the outcome, open a new operation with its own criteria and verdict. |
| **Process verdict** | When multiple operations compose a process, add a **process-level** verdict after all required operations: **`Process result: PASS`** only if every **required** operation is **PASS**; otherwise **`Process result: FAIL`** and name the failing operation id(s). |
| **Display** | In CLI or JSON logs, include an explicit field (e.g. `"verdict": "PASS"`) or a final line `VERDICT: PASS` so parsers and humans cannot miss it among stderr warnings. |

**Forbidden:** A closing paragraph that says "everything looks good" without **`Result: PASS`**; a PASS verdict followed only by "but note…" with no incidental section header; implying PASS because most steps succeeded while a required [gate](../../../../docs/TERMS.md#gate) failed.

---

## 6. Skills and prompts (authoring)

When creating or **first editing** a skill or published prompt:

1. **[Gate](../../../../docs/TERMS.md#gate)** — per [§2](#2-gate-design-produced-artifacts): [default-closed](../../../../docs/TERMS.md#default-closed); blocking criteria individually testable true/false.
2. **Done signals** — list objective PASS conditions (and what FAIL looks like).
3. **Per-step verdict** — multi-step procedures require a §4 verdict block after each step (or after each machine gate); [handoff](../../../../docs/TERMS.md#handoff) may summarize process verdict.
4. **`uses_standards`** — include `standards/operation-verdict-standard.md` when the skill produces gated or audited output.
5. **Scripts** — prefer exit codes; stdout may include `VERDICT: PASS | FAIL | BLOCKED`. Do **not** print PASS if the check did not run. Parsers treat a missing verdict the same as BLOCKED when the script is the machine [gate](../../../../docs/TERMS.md#gate).

[AWL](../../../../docs/TERMS.md#awl) alignment: Phase 4 and Phase 6 [audit](../../../../docs/TERMS.md#audit) memos satisfy this standard when they use **`Verdict: PASS | FAIL`** and per-register evidence ([`audited-work-loop-standard.md`](audited-work-loop-standard.md) §4).

---

## 7. Agent behavior

1. Before running an operation, state (or cite) its PASS/FAIL criteria in one line if not already in the skill.
2. Evaluate each **blocking** [gate](../../../../docs/TERMS.md#gate) criterion true/false; do not proceed on any **false**, **untested**, or **INCONCLUSIVE** blocking row.
3. After running, emit the §4 verdict block before proceeding. Cite the artifact inspected — not a delegate's claim that it passed.
4. If stderr contains warnings but exit code is **0**, verdict is **PASS** with incidentals listed separately — unless the skill defines additional hard criteria beyond exit code.
5. Do not declare a process **done** while any required operation is **FAIL** or **BLOCKED** ([`lean-operating-principles.md`](lean-operating-principles.md) §1).

---

## 8. See also

- [`report-pyramid-structure.md`](report-pyramid-structure.md)
- [`audited-work-loop-standard.md`](audited-work-loop-standard.md)
- [`information-completion-contract.md`](information-completion-contract.md) — intake [gate](../../../../docs/TERMS.md#gate) profile
- [`dsi-converge-deliverable-contract.md`](dsi-converge-deliverable-contract.md) — Lens A **100% PASS** / **FAIL**
- [`vault-pull-request-review-standard.md`](vault-pull-request-review-standard.md) — merge [gate](../../../../docs/TERMS.md#gate) verdicts
- [`skillet-export.md`](skillet-export.md) — skilletted skill [Gate](../../../../docs/TERMS.md#gate) section
