# Information-completion contract

Normative rules for eliciting inputs until an agent can run a prompt or skill safely: resolution table, blocking vs optional facts, fast path, deliverable-write gate, and multi-stage Handoff validation.

**Related:** [`operation-verdict-standard.md`](operation-verdict-standard.md) (default-closed gates, testable criteria, PASS/FAIL verdicts), [`agent-failure-modes-and-meta-prompt-patterns.md` (agent-failure-modes-and-meta-prompt-patterns.md — not bundled in this skill) §13 (secrets), [`audited-work-loop-standard.md`](audited-work-loop-standard.md) (Phase 1 intake), [`prompts/README.md`](information-completion-contract.md) (vault placeholder table and frontmatter).

**Profile:** This contract is the **intake / deliverable-write gate profile** ([`operation-verdict-standard.md`](operation-verdict-standard.md) §2.3). It inherits **default-closed** posture and **testable true/false** criteria; do not weaken them here.

---

Published prompts and skilletted skills are **Markdown only**—agents follow this contract by instruction; there is no runtime validator. Users may prepend answers or edit the paste block; the agent must still behave safely and avoid redundant questioning when the first message is already complete.

## Two layers of inputs

1. **Layer A — Declared parameters** — Placeholders from the placeholder convention (`{{PROJECT_NAME}}`, `{{REPO_ROOT}}`, `{{TEAM}}`, `{{PRIMARY_LANGUAGE}}`, etc.), plus any **prompt-specific** placeholders documented in that file (e.g. design-pack slots in stage prompts—mark whether they are **user-resolved** or **filled from a prior stage Handoff**). Vault catalog: [`prompts/README.md`](information-completion-contract.md).
2. **Layer B — Task facts** — Blocking facts that are not necessarily placeholders (e.g. risk tier, runtime model, monorepo **subpath scope**, merge vs replace for `TODO.md`). Authors should make **blocking** vs **optional** items obvious in **Questions** or a short list under **Validation**.

**Completion rule:** The agent treats the task as **information-complete** when Layer A is resolved **and** every **blocking** Layer B item is answered, explicitly **waived** only where the prompt allows, or recorded as a labeled **`Assumption:`** (or equivalent) in the deliverable when the prompt permits assumptions instead of facts.

## Step 0 — Resolution table (before Execution)

**AWL Phase 1:** This step satisfies **intake** in [`audited-work-loop-standard.md`](audited-work-loop-standard.md). For **T2+** work, use the extended intake table and blocking questions in AWL **Appendix C** (tier compression for T0/T1 per AWL §5).

After parsing the user message and workspace context, emit a short **resolution table** in chat: each placeholder and blocking fact → **resolved value**, **`Waived`** (if allowed), or **`Assumption: …`** (if allowed). Include **subpath scope** when the task is not the whole repo (`{{REPO_ROOT}}` only, or `{{REPO_ROOT}}/path`).

Do **not** leave literal `{{…}}` in generated files or primary chat deliverables except when teaching the convention or when the prompt is explicitly a **template generator** whose output is another prompt (see stage-4 style prompts).

## Blocking rule: deliverable writes

Do **not** create or overwrite the prompt’s **primary deliverables** (files, mandated report sections, etc.) until **information-complete** per the completion rule.

**Read-only discovery** is allowed before completion when **Validation** requires it (e.g. locate `Dockerfile*`, confirm layout). Order steps so **invasive edits** never precede the gate; if a prompt’s Validation lists reads, perform those reads before claiming completion is impossible.

## Fast path

If the user’s first message (plus obvious workspace facts) already supplies all blocking inputs **unambiguously**, skip re-asking: emit the resolution table once for **transparency**, then **immediately** proceed to **Validation** → **Execution**. Do **not** wait for an acknowledgment or ask “Should I proceed?” — that is premature andon when work is already authorized ([`lean-operating-principles.md`](lean-operating-principles.md) §2).

## Waiver and defaults

Where the prompt says a question may be **waived** or a **default** applies, document the default in the resolution table and in the deliverable as an **`Assumption:`** when the prompt requires it. Do **not** invent unsafe defaults for compliance tier, scope, or security-sensitive choices unless the prompt explicitly allows assumption.

## Ambiguity and contradiction

If two user statements conflict, **surface the conflict** and ask which value to use. If an answer is vague, ask **one** focused follow-up rather than guessing material behavior.

## Secrets and credentials

**Never** loop to collect secrets, API keys, or session tokens in chat. Point to Key Vault, environment injection, or org process; use placeholders in examples only. Align with [`agent-failure-modes-and-meta-prompt-patterns.md` (agent-failure-modes-and-meta-prompt-patterns.md — not bundled in this skill) §13.

## Multi-turn behavior

If inputs are missing, end the turn with a **short numbered question list**. The **ask → user reply → re-evaluate** loop spans **chat turns**; do not pretend to recurse indefinitely in one turn.

## Operation completion (verdict)

After each **Gate**, **Procedure** step, or machine command that blocks downstream work, emit a verdict per [`operation-verdict-standard.md` (operation-verdict-standard.md — not bundled in this skill): **`Result: PASS | FAIL | BLOCKED`**, objective **Evidence**, and **Next**. Warnings and advisories go under **Incidentals (verdict unchanged)** — they do not replace or soften the verdict line.

## Multi-stage pipelines and Handoff

- **Orchestration maps** (`paste_contract.kind: orchestration_map` — see vault-published-prompt-contract (not bundled in this skill)) are for **humans**: use **pre-flight checklists** (workspace open, placeholders resolved, prior stage **Handoff** pasted) before opening each stage prompt. Do not paste the map file alone as the runnable instruction.
- **Stage prompts** that consume only prior output must **validate** required **Handoff** sections/headings. If missing or malformed, ask the user to paste the missing sections or **re-run** the prior stage—do **not** invent prior-stage content.
