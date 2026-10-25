# Root cause analysis (RCA) standard

Normative rules for finding **one preventive change** after a failure — in **this vault**, in **consumer repositories**, and in **agent sessions** compiled from vault prompts and skills.

**Core question (required output):**

> What **one** deterministic, actionable thing, if it were different, would have **prevented this error condition from arising**?

**Related:** [`lean-operating-principles.md`](lean-operating-principles.md) (jidoka — stop and fix at source), [`agent-failure-modes-and-meta-prompt-patterns.md`](agent-failure-modes-and-meta-prompt-patterns.md) §7 (verification failures), [`domain-first-authoring.md`](domain-first-authoring.md) (where preventive fixes belong), [`knowledge-change-review-standard.md`](knowledge-change-review-standard.md) (vault durable writes after RCA).

---

## 1. When to run RCA

Run RCA **before** declaring a failure handled, **before** passing work downstream, and **before** treating a workaround as done.

| Trigger | Examples |
| ------- | -------- |
| **Failed gate** | CI red, validator non-zero exit, link check failure, pre-commit hook failure |
| **Recurring defect** | Same class of failure twice in a sprint or branch |
| **Incident** | Production or customer-impacting error, security event, data integrity issue |
| **Regression** | Behavior that worked on a prior commit or release |
| **Agent/session stall** | Repeated fix attempts without passing verification |

**Skip RCA** only when the failure is **trivial and fully understood** (typo in an uncommitted local edit you just fixed) — still state the one preventive change in chat in one sentence.

---

## 2. Terms

| Term | Meaning |
| ---- | ------- |
| **Error condition** | A **bounded**, **reproducible** description of what went wrong: observable signal, failing command, exit code, log excerpt, or incident symptom. Not a judgment ("bad code"). |
| **Symptom** | What you noticed first (red CI, exception, user report). May differ from the earliest preventable point. |
| **Contributing factor** | Something that made the failure more likely or worse; **not** sufficient alone to answer the core question. |
| **Root (the one thing)** | The **single** change that would have made this **exact error condition** impossible under the same inputs and environment, per §3. |
| **Output defect** | The failing artifact you see first: code, YAML, config, test result, deployed state. A **symptom** until upstream process is ruled out. |
| **Process defect** | A flaw in **how** work is produced: standard, prompt, skill, validator, playbook, template, gate, or handoff. Often the true root when agents or pipelines generated the output. |
| **Upstream chain** | Ordered producers from symptom to origin — e.g. defective code ← skill B ← skill A ← prompt. RCA walks this chain **away from the symptom**. |

---

## 2.1 Process before output (normative)

**The root cause of a defect is not found in the output. It is found in the process that produced it.**

When work was generated, scaffolded, or guided by prompts, skills, standards, validators, or playbooks:

1. **Bound the output defect** with evidence (file, command, log).
2. **Identify the producing chain** — what skill, prompt, standard, validator, or script produced or approved this output?
3. **Walk upstream** to the **furthest controllable** step where one preventive change would have blocked the defect.
4. **Select the one thing** at that upstream layer — not the nearest convenient patch to the symptom.

### Example (skill chain)

| Step | Artifact | Role |
| ---- | -------- | ---- |
| 1 | Prompt | Creates skill A |
| 2 | Skill A | Creates skill B |
| 3 | Skill B | Creates code |
| 4 | Code | Defect observed |

The defective **code** is evidence. The likely **root** is in **skill A** (or the prompt), because that is where B was shaped to produce defective code. Fixing only the code without fixing A recreates the defect on the next run.

### Reject output-only roots when process is controllable

Do **not** accept "fix this file" as the final answer when an upstream standard, skill, prompt, or validator could have prevented the class of error — unless you document why upstream prevention is infeasible.

---

## 3. The "one thing" bar

A valid answer must satisfy **all** of:

| Criterion | Test |
| --------- | ---- |
| **One** | Exactly one change — not a list, not "and also." If several changes seem necessary, pick the **earliest controllable** point in the causal chain (§5). |
| **Deterministic** | Under the same preconditions, this change makes the error condition **impossible**, not merely less likely. |
| **Actionable** | A specific artifact or behavior someone can implement: add a check, fix a script, change a standard, add a test, correct a config key, update a validator. |
| **Preventive** | Stops the condition **before** it arises — not only faster detection, logging, or cleanup after the fact. |
| **In scope** | Within team control — not "if the user had not asked for X" or "if the vendor had not shipped a bug" unless the preventive action is a **documented guard** (pin, contract test, feature flag). |

### 3.1 Reject these as final answers

Do **not** stop RCA on vague or non-preventive labels unless rewritten to a concrete change:

- "Human error" / "miscommunication" / "lack of attention"
- "Need more testing" (without naming **which** test or gate)
- "Misconfiguration" (without **which** key, file, or default)
- "Didn't read the docs" (without **which** doc should be linked, generated, or enforced)
- "Race condition" (without **which** ordering or synchronization change)
- "Legacy code" (without **which** boundary or removal step)
- "Fix the output file" / "patch the generated YAML" (when an upstream standard, skill, prompt, or validator is controllable — see §2.1)
- "Grandfather the violation" / "add an allowlist exception" for a fixable gap at standard-creation time (encodes debt as policy)
- Nil-check, optional unwrap, or comment-justified guard that **silences a crash or empty case** without removing the condition that made the guard necessary (symptom patch)

Detection-only mitigations (alert, retry, manual checklist) are **contributing follow-ups**, not the root, unless prevention is genuinely impossible — then state why and name the **earliest** detectable gate instead.

### 3.2 Prevention test (mandatory)

Before accepting an answer, complete this sentence:

> If **`{the one change}`** had been in place **before** the failure, **`{error condition}`** could not have occurred because **`{mechanism}`**.

If you cannot complete it with evidence, keep investigating.

---

## 4. Procedure

Execute in order. Do not skip to fixes before step 6 (the one thing).

1. **Bound the error condition** — Quote evidence: command, exit code, log lines, file paths, timestamps, reproduction steps. Separate **observed** from **inferred**.
2. **Stabilize reproduction** — Confirm the failure is reproducible or document why not (flaky, environmental).
3. **Walk backward through process and product** — From the error condition, ask "what had to be true for this to happen?" Include the **upstream chain** (§2.1): which prompt, skill, standard, validator, or playbook produced or permitted this output? Continue until you reach the **furthest controllable** preventive point — often process, not the symptom file.
4. **State candidate roots** — List at most three candidates; apply §3 to each.
5. **Confirm the surviving mechanism on the reproduction** — Observed evidence, not inference. Do **not** select the one thing until this holds, or document why the failure is unreproducible. The prevention test (§3.2) names that mechanism.
6. **Select the one thing** — Earliest controllable preventive change that passes the prevention test (§3.2).
7. **Place the fix** — See §6 (vault) or §7 (consumer repo).
8. **Record** — Write the RCA artifact (§8).
9. **Track one action** — Single owner-visible item; re-run the failing gate or reproduction to verify prevention.

---

## 5. Multiple apparent causes

When several changes seem required:

1. Prefer the **earliest** point where a **single gate** would have blocked the chain.
2. If failures are **independent** (two unrelated defects surfaced at once), run **two RCAs** — do not blend into one vague root.
3. If prevention truly requires a **compound** change (e.g. code + CI), the "one thing" is the **highest-leverage gate** that would have caught it before impact — usually an automated check over manual process.

---

## 6. Vault maintainer placement (this repository)

After RCA, place preventive work in the **durable** layer first ([`domain-first-authoring.md`](domain-first-authoring.md)):

| If the one thing is… | Update first |
| -------------------- | ------------ |
| Org-wide rule or convention | `standards/*.md` → **standard-ripple** |
| Validator/compiler gap | `metaprompts/scripts/` or relevant tooling → re-run validators |
| Domain/product fact | MSG manifest (`/local-msg-domain-pipeline`) |
| Prompt wording only (standard already correct) | `prompts/` bounded region |
| Maintainer procedure | `.cursor/prompts/` or `.cursor/skills/` |

**Durable writes** to `standards/`, manifests, or `vault-intents/` require an accepted **KCR** per [`knowledge-change-review-standard.md`](knowledge-change-review-standard.md). Reference the RCA path in the KCR **rationale**.

**Artifact location:** `draft/rca/YYYY-MM-DD-<slug>.md` (use [`metaprompts/templates/rca-record-TEMPLATE.md`](../metaprompts/templates/rca-record-TEMPLATE.md)).

---

## 7. Consumer repository placement

| If the one thing is… | Typical placement |
| -------------------- | ----------------- |
| Missing or wrong test/CI gate | Test file + pipeline job |
| Config/secrets contract | Env docs, sample config, validation script |
| Operational gap | `docs/runbooks/` or `RUNBOOK.md` |
| Code defect | Fix + regression test |
| Architecture fork | `docs/adr/` |

**Artifact location:** `docs/rca/YYYY-MM-DD-<slug>.md` (create directory if needed). For severe incidents, also link from `CHANGELOG.md` or the team's incident system — do not duplicate full postmortems unless the user requests.

---

## 8. RCA record (required sections)

Use the template at [`metaprompts/templates/rca-record-TEMPLATE.md`](../metaprompts/templates/rca-record-TEMPLATE.md). Minimum sections:

1. **Error condition** (evidence)
2. **Upstream chain** (symptom → producers; per §2.1)
3. **Impact / scope**
4. **Timeline** (brief)
5. **Mechanism on reproduction** (confirmed / unreproducible + evidence)
6. **The one thing** (single sentence)
7. **Prevention test** (§3.2 sentence completed)
8. **Contributing factors** (optional, non-actionable list)
9. **Preventive action** (one tracked item: owner, path, verification command)
10. **Follow-up** (detection improvements only if prevention is insufficient)

---

## 9. Agent behavior

1. On **non-zero verification** or **repeated fix failure**, run §4 through **confirm mechanism** (step 5) before claiming the one thing.
2. Present the **one thing** and **prevention test** in chat even when not writing a file.
3. Do **not** substitute RCA with symptom patches (retries, broader try/catch, weakened assertions, nil-guards that silence crashes) without naming why prevention was infeasible.
4. After preventive change, **re-run the original failing command** or reproduction.

**Building block** (for prompts and skills):

```markdown
## Root cause (required on failure)

When a gate fails or the same defect appears twice:

1. Bound the **error condition** with evidence (command, exit code, log excerpt).
2. Trace the **upstream chain** (§2.1) when output was produced by prompts, skills, or automation.
3. Answer: **What one deterministic, actionable thing, if it were different, would have prevented this error condition from arising?** Prefer the **furthest upstream controllable** fix.
4. Complete the **prevention test**: "If {change} had been in place before the failure, {condition} could not have occurred because {mechanism}."
5. Implement or track **that one preventive action**; re-run verification.
6. Write `docs/rca/YYYY-MM-DD-<slug>.md` (consumer repo) or `draft/rca/YYYY-MM-DD-<slug>.md` (vault) when the failure is non-trivial.

Reject vague roots (see root-cause-analysis-standard §3.1).
```

---

## 10. See also

- [`lean-operating-principles.md`](lean-operating-principles.md) — Jidoka
- [`repository-governance-standard.md`](repository-governance-standard.md) §10 — Incident readiness
- [`prompts/review/conduct-root-cause-analysis.md`](../prompts/review/conduct-root-cause-analysis.md) — Consumer runnable prompt
- [`.cursor/prompts/local-conduct-root-cause-analysis.md`](../.cursor/prompts/local-conduct-root-cause-analysis.md) — Vault maintainer runnable prompt
