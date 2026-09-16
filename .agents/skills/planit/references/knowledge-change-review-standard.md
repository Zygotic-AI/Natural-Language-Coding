# Knowledge Change Review (KCR) standard

Normative rules for **maintainer acceptance** before any **add**, **update**, or **remove** to durable knowledge layers in this vault.

**Related:** [`vault-intent-and-synthesis-standard.md` (vault-intent-and-synthesis-standard.md — not bundled in this skill), [`domain-first-authoring.md`](domain-first-authoring.md), [`audited-work-loop-standard.md`](audited-work-loop-standard.md) (Phase 5 sub-gate before durable writes), [`vault-pull-request-review-standard.md` (vault-pull-request-review-standard.md — not bundled in this skill), (vault authoring only — not applicable in installed skills), (vault authoring only — not applicable in installed skills).

---

## 1. Scope — layers requiring KCR

| Layer | Paths | Examples |
| ----- | ----- | -------- |
| **Standards** | `*.md` | New policy, extended checklist, deprecation |
| **Domain knowledge** | `vault metaprompt manifests (authoring only)/**`, `vault metaprompts (authoring only)/profiles/*.md` | Manifest fragments, profile overlays |
| **Goals / intent** | `vault metaprompts (authoring only)/vault-intents/*.json` | Mission, produces, audit conditions |

**Does not require KCR** (normal PR review): regenerable views — `prompts/` bounded regions (after intent accepted), `skills/` from materialize, `vault MSG packs (authoring only)/` from manifest.

---

## 2. KCR artifact

**Location:** `draft/knowledge-change-reviews/YYYY-MM-DD-<slug>.md`

**Template:** (vault authoring only — not applicable in installed skills)

**Required sections:** Summary; change table (`layer` | `operation` | `path` | `rationale`); before/after for updates; non-goals and tradeoffs; downstream impact; **Acceptance** block with explicit status.

---

## 3. Agent behavior (mandatory)

1. **Draft KCR first** — complete review Markdown; **stop**; do **not** write durable files in the same turn.
2. **Explicit acceptance only** — proceed when the maintainer clearly accepts (`accept`, `approved`, `lgtm` on the KCR, or **AskQuestion** Accept all). Unrelated assent does **not** count.
3. **Partial accept** — update KCR status and notes; write only accepted paths.
4. **Rejection** — no durable writes; revise or abandon.
5. **Batch changes** — one KCR may cover multiple layers; list every path.
6. **No bypass** — `/local-author-or-extend-knowledge`, `/local-msg-domain-pipeline`, `/local-induct-skill-or-prompt`, and standard-ripple must delegate to KCR before durable writes.

---

## 4. Anti-patterns

- Writing `vault standards (authoring only)`, manifest fragments, or `vault-intents/` without an accepted KCR.
- Treating interview JSON alone as acceptance (KCR is the human-readable acceptance surface).
- Auto-applying constituent expansion to committed intent without KCR listing proposed paths.

---

## 5. Registry linkage

After acceptance, reference the KCR path in the branch (vault authoring only — not applicable in installed skills) entry `## Changes` section for audit traceability.

---

## 6. Pull request merge

KCR acceptance is a **Critical** gate before merge when the PR touches durable layers (§1). Reviewers confirm:

1. KCR **Acceptance** block shows explicit approval (not unrelated assent).
2. Registry entry links the KCR path and lists every impacted durable path.
3. Registry **assertions** cover normative lines that must not silently drop after merge.

Full merge gate ordering, CI scripts, and AI/determinism expectations: [`vault-pull-request-review-standard.md` (vault-pull-request-review-standard.md — not bundled in this skill). Domain manifests: (vault authoring only — not applicable in installed skills). Runnable evaluation: **`/local-review-pr`** ((vault authoring only — not applicable in installed skills)).

---

## See also

- (vault authoring only — not applicable in installed skills)
- (vault authoring only — not applicable in installed skills)
- [`vault-pull-request-review-standard.md` (vault-pull-request-review-standard.md — not bundled in this skill)
