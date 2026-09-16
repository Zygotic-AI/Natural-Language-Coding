# Lean operating principles (maintainers)

Normative **maintainer and agent** behavior for this vault and for workflows compiled from it. Complements [`agent-failure-modes-and-meta-prompt-patterns.md` (agent-failure-modes-and-meta-prompt-patterns.md — not bundled in this skill) (consumer-repo agents) and [`skillet-export.md` (skillet-export.md — not bundled in this skill) (product principles).

---

## 1. Jidoka — do not pass problems downstream

**Principle:** When you detect a defect, abnormality, or failed gate, **stop and address it** (or escalate with a clear blocker). Do not leave the problem for the next person, the next pipeline stage, or the next session.

| In manufacturing | In this vault |
| ---------------- | ------------- |
| Stop the line when quality fails | Do not declare a task complete while CI, validators, or link checks fail |
| Fix at source | Fix the **compiler/script/standard** that caused drift, not only symptoms |
| Andon — visible stop | Report failing command, path, and exit code; do not hand-wave as "pre-existing" without a tracked follow-up. See §2 before escalating that stop to a human. |

**Related Toyota phrases:** *No problem is a problem* (if you never see issues, you are not looking). *See a problem, fix a problem* (when in scope).

**Agent behavior**

1. Run relevant validators before claiming done (`validate-vault-intents`, `check-vault-intent-parity`, `validate-skills`, `verify-build-clean`, `./vault metaprompt scripts (authoring only)/rebuild-all-packs.sh` for link check when touching skills).
2. If a gate fails, **fix or file** — do not defer with "user should commit" unless the only remaining step is an explicit human acceptance (e.g. KCR). Prefer **autonomous recovery** per §2 before asking a human.
3. Do not describe a known failure as out of scope when the current task introduced or exposed it.

**RCA before workaround:** When a gate fails or the same defect appears twice, run [`root-cause-analysis-standard.md`](root-cause-analysis-standard.md) before declaring done. Answer the core question — *what one deterministic, actionable thing would have prevented this error condition?* — and record non-trivial failures under `draft/rca/`. Invoke **`/local-conduct-root-cause-analysis`** (vault) or fix at the durable layer (standard, script, prompt) per standard §6.

---

## 2. Premature andon — autonomous recovery first

**Name:** **Premature andon** (also: **false escalation**; **manual gate for automatable recovery**; **re-confirmation of authorized work**).

**Principle:** Andon is a visible stop so the system can clear the abnormality. When an existing **autonomous recovery** can clear it (owned script, skill, prompt, pack install, or equivalent), agents and compiled workflows **must invoke that path** and **re-enter the check**. Do **not** ask the human to run or approve that path by default.

**Also premature andon — do not re-ask for work already authorized:**

When the user’s message (this turn or earlier in the same task thread) already ordered an action — including by clear implication — the agent **must execute** that action. It is a **complete failure** to stop and ask whether to proceed with that same work.

| Already authorized (examples) | Forbidden agent response |
| ----------------------------- | ------------------------ |
| “RCA and remediate” | “Want me to fix those now?” |
| “Did you fix them?” after an RCA with open remediation | “Should I finish remediating?” |
| “Guess what I want” after “No” to “fixed and ready” | Asking to confirm the guessed next step instead of doing it |
| `/local-dsi-converge <repo>` | Stopping mid-loop to ask whether to continue Stage C |

**Test:** If removing the question would leave a clear imperative the user already gave, **do not ask** — continue.

| Failure | Correct behavior |
| ------- | ---------------- |
| Premature andon | Prompting y/n or “please run X” when the current skill/workflow can run X and re-check |
| Premature andon | “Want me to do that?” / “Should I proceed?” when the user already ordered that work |
| Correct andon | Stop after autonomous recovery is missing, unsafe, or already failed; or when standards reserve a human gate; or when a **new** blocking input is truly missing (information-completion) |

**Legitimate human stops (not premature andon)**

- Knowledge Change Review (KCR) and other explicit acceptance gates
- Irreversible or production-destructive actions already marked manual in vault prompts (authoring only)
- Recovery path missing, not locatable, or failed after an autonomous attempt
- Secrets/credentials the agent must not invent
- **Genuinely new** blocking facts never supplied (resolution table) — not re-asking for authorization of work already in the thread

**Agent / prompt author behavior**

1. When designing a gate: if recovery is a known vault command (e.g. `bash tools/tree-sitter/install.sh`), **wire it to run autonomously**, then loop back to the same check.
2. Escalate to the human only with the **blocker that remains after** autonomous recovery (exit code, path, what was tried).
3. Opt-out env flags (e.g. `DSI_TREESITTER_INSTALL=n`) are for sandboxes that must not mutate the environment — not the default product path.
4. After RCA with a preventive action, or after answering “no, not fixed yet,” **implement the remaining fixes in the same turn** — do not ask permission to continue authorized remediation.
5. Never end a turn with only “Want me to …?” when the user’s last clear intent was to have that work done.

**Anti-pattern (historical):** DSI Stage B asking the human y/n to install Tree-sitter when the skill could run `install.sh` and re-check. Asking “want me to remediate?” after the user ordered RCA + remediate and then asked if fixes were done.

**Related:** [`agent-failure-modes-and-meta-prompt-patterns.md` (agent-failure-modes-and-meta-prompt-patterns.md — not bundled in this skill) §7.2; KCR `draft/knowledge-change-reviews/2026-07-24-premature-andon-autonomous-recovery.md`; KCR `draft/knowledge-change-reviews/2026-07-24-no-reconfirm-authorized-work.md`.

---

## 3. See also

- [`root-cause-analysis-standard.md`](root-cause-analysis-standard.md) — One preventive change; prevention test; RCA record
- [`agent-failure-modes-and-meta-prompt-patterns.md` (agent-failure-modes-and-meta-prompt-patterns.md — not bundled in this skill) — Verification, scope, completeness; premature andon §7.2
- [`knowledge-change-review-standard.md`](knowledge-change-review-standard.md) — Human acceptance before durable writes (legitimate andon)
- [`audited-work-loop-standard.md`](audited-work-loop-standard.md) — Seven-phase work loop; audit failure behavior; authorized-work exceptions
