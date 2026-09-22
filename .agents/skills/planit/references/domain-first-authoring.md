# Domain-first authoring

Normative rules for **maintainers** and **agents editing this vault**. Prompts and skilletted skills are **composed views** of durable knowledge. The vault compounds value when **standards**, **domain manifests**, and **reference** grow over time—not when individual prompt files accumulate one-off prose.

**Related:** vault-published-prompt-contract (not bundled in this skill) (`rebuild_from`, `uses_standards`), [`vault-pull-request-review-standard.md` (vault-pull-request-review-standard.md — not bundled in this skill), [`msg-vault-integration.md` (msg-vault-integration.md — not bundled in this skill), (vault authoring only — not applicable in installed skills), (vault authoring only — not applicable in installed skills), (vault authoring only — not applicable in installed skills), [`audited-work-loop-standard.md`](audited-work-loop-standard.md) (Phases 2 and 7).

---

## 1. Principle

| Asset | Location | Role | Lifespan |
| ----- | -------- | ---- | -------- |
| Background | (vault authoring only — not applicable in installed skills) | Policies, glossaries, industry practice | Durable |
| Cross-cutting norms | [`vault standards (authoring only)`](.) | How systems, repos, pipelines, and reviews **should** work | Durable — **highest leverage** |
| Domain model | (vault authoring only — not applicable in installed skills), [`vault MSG packs (authoring only)/` (vault path — not bundled in installed skills) | Product- and tech-specific facts (actors, artifacts, playbooks) | Durable |
| Runnable views | (vault authoring only — not applicable in installed skills) | Thin composition with `paste_contract`, `rebuild_from`, `uses_standards` | Regenerable |
| User entry | (vault authoring only — not applicable in installed skills) (skilletted) | Self-contained runtime compiled from prompts + domain | Output — not source |

**Do not treat `prompts/` as the primary knowledge store.** Treat it as the **published execution layer** built from constituents listed in `rebuild_from.constituents`.

---

## 2. Default maintainer loop

When a maintainer needs a prompt or skill for use in **another repository**:

1. **Discover** — Search `vault standards (authoring only)`, `vault metaprompt manifests (authoring only)/`, `vault metaprompts (authoring only)/vault-intents/`, and existing `prompts/` (`uses_standards`, `rebuild_from`, grep). Reuse before authoring.
2. **Extend knowledge** — Put net-new facts in the correct durable layer:
   - Org-wide convention → `<topic>-standard.md` (or extend an existing standard).
   - Domain/product [workflow](../../../../docs/TERMS.md#workflow) → MSG: **`/local-msg-domain-pipeline`** ((vault authoring only — not applicable in installed skills)), not a one-off paragraph in a prompt.
   - Background only → `reference/` when not yet normative.
3. **Compose** — Author a **thin** prompt under `prompts/<category>/` that cites constituents in `rebuild_from` and `uses_standards`; inline only **minimum operative** excerpts in bounded paste regions (vault-published-prompt-contract (not bundled in this skill) §11).
4. **Validate** — Run once in the target application repo (bounded paste or skilletted `/<id>`). This is a **test**, not where knowledge should live.
5. **Back-propagate** — If the run surfaced real learning, update **`vault standards (authoring only)` or the domain manifest**, then ripple or re-materialize—not prompt-only edits unless the underlying knowledge was already correct.
6. **Record** — Log the change in the (vault authoring only — not applicable in installed skills) with a short summary and CI-verified **assertions** (§7). This makes large AI-authored diffs reviewable and guards against silent drops.

---

## 3. Where learnings go after a consumer run

| Learning type | Update first | Then |
| ------------- | ------------ | ---- |
| Org-wide policy or repo convention | `*.md` | **standard-ripple** ((vault authoring only — not applicable in installed skills)) |
| Product/domain [workflow](../../../../docs/TERMS.md#workflow), actors, artifacts | Domain manifest (`/local-msg-domain-pipeline` refresh) | `finish-pack.sh` or `rebuild-all-packs.sh` |
| Prompt wording or pacing only | `prompts/` file | Bump `updated` / `version` |
| New multi-stage flow | Stage bodies under `prompts/<category>/` + map in `prompts/pipelines/` | Skillet to one outcome skill if org-wide |

---

## 4. Anti-patterns (agents must avoid)

- **Prompt-first authoring** — Drafting long runnable prose under `prompts/` before checking whether the fact belongs in `vault standards (authoring only)` or a domain manifest.
- **Knowledge trapped in prompts** — Embedding durable domain or policy facts only inside bounded paste regions with no `rebuild_from` path to a standard or manifest.
- **Paste-copy-tweak loops** — Iterating only on prompt text without back-propagating learnings to durable layers.
- **Consumer-repo shortcuts for vault work** — Suggesting ad-hoc `.cursor/prompts/` or `/make-a-prompt` in an application repo when the maintainer [goal](../../../../docs/TERMS.md#goal) is **org-wide, reviewed** knowledge in this vault (repo-local authoring is for **team-only** outcomes per [`repository-agent-local-artifacts.md` (repository-agent-local-artifacts.md — not bundled in this skill) §6).
- **Skipping ripple** — Changing a standard without running **standard-ripple** or checking dependents via `uses_standards` / `rebuild_from`.

---

## 5. Maintainer entry points (this vault as workspace)

**Front door for net-new or extend durable knowledge:** **`/local-author-or-extend-knowledge`**. Leaf skills marked **`sub_procedure: true`** are invoked by the orchestrator (or for prompt-only refresh) and are **hidden from `/local`**.

| Step | Invoke | Notes |
| ---- | ------ | ----- |
| **Unified durable authoring (preferred)** | **`/local-author-or-extend-knowledge`** | KCR + vault-intent + prompt + parity |
| Add or refresh domain knowledge | **`/local-msg-domain-pipeline`** | KCR before manifest promotion |
| Induct external prompt or skill | **`/local-induct-skill-or-prompt`** (sub-procedure; prefer **`/local-author-or-extend-knowledge`**) | Full KCR + intent when invoked directly |
| Post-change hygiene | **`/local-vault-maintainer-pipeline`** | Ripple, normalize, [audit](../../../../docs/TERMS.md#audit) — **not** net-new authoring |
| Standard changed → update dependents | **vault-maintainer-pipeline** _standard-ripple_ | KCR first if **editing** the standard file |
| Catalog / [contract](../../../../docs/TERMS.md#contract) [audit](../../../../docs/TERMS.md#audit) | **vault-maintainer-pipeline** _full-audit_ | Regenerable views; no KCR for prompt-only fixes |

**Sub-procedures** (do not use as front door for net-new consumer outcomes):

| Sub-procedure | Role |
| ------------- | ---- |
| **`/interview-author-published-prompt`** | Prompt file shape after KCR + intent |
| **`/author-or-refresh-meta-prompt`** | Composition-heavy meta after KCR + intent |
| **`/synthesize-prompt-from-intent`** | Author-time bounded-region synthesis |

Human runbook: (vault authoring only — not applicable in installed skills) §12 (domain-first iteration).

---

## 6. Dependency chain (authoring order)

1. (vault authoring only — not applicable in installed skills)
2. [`vault standards (authoring only)`](.)
3. (vault authoring only — not applicable in installed skills) → [`vault MSG packs (authoring only)/` (vault path — not bundled in installed skills)
4. (vault authoring only — not applicable in installed skills) — durable consumer outcome goals
5. Domain prompts under (vault authoring only — not applicable in installed skills)
6. (vault authoring only — not applicable in installed skills) and (vault authoring only — not applicable in installed skills)
7. Skilletted (vault authoring only — not applicable in installed skills) (compiled output)
8. (vault authoring only — not applicable in installed skills)

Promotion: (vault authoring only — not applicable in installed skills) → reviewed (vault authoring only — not applicable in installed skills) per (vault authoring only — not applicable in installed skills).

---

## 7. Change registry (audit + silent-drop guard)

Durable edits (standards, domain manifests/fragments, published prompts) are
**recorded** in (vault authoring only — not applicable in installed skills) — one immutable Markdown file per
change. The registry is the intent/audit layer that lets review scale when the
underlying diff is large (AI-authored prose), without trusting a full re-read.

The maintainer skills append to it automatically; the loop is:

1. **Resolve** this branch's entry — `node vault metaprompt scripts (authoring only)/registry-active.mjs` (0 → create from (vault authoring only — not applicable in installed skills); 1 → reuse; >1 → pick).
2. **Append** the change (what + why) under `## Changes`, and any **assertions** — machine-checkable claims (`contains` / `regex` / `absent`) about canonical files that must not silently disappear.
3. **Attribute** — set `domains` and `reviewers` from [`../domain-owners.yml` (vault path — not bundled in installed skills); reviewers are auto-assigned on the PR.
4. **[Verify](../../../../docs/TERMS.md#verify)** — CI runs `node vault metaprompt scripts (authoring only)/verify-registry-assertions.mjs`; a broken assertion fails the build, pinpointing when/where a regression entered.

Pull request merge gates (CI, KCR, consumer smoke, reviewer routing): [`vault-pull-request-review-standard.md` (vault-pull-request-review-standard.md — not bundled in this skill). Domain manifests: (vault authoring only — not applicable in installed skills). Before open PR: **`/local-review-pr`** ((vault authoring only — not applicable in installed skills)).

Entries are **immutable**: to reverse or supersede one, write a new entry and
move the old file to (vault authoring only — not applicable in installed skills) (never deleted;
its assertions retire automatically). Schema and rules: (vault authoring only — not applicable in installed skills).

---

## See also

- [`vault-pull-request-review-standard.md` (vault-pull-request-review-standard.md — not bundled in this skill) — Merge gates for PRs to `main`
- (vault authoring only — not applicable in installed skills) — Domain-first authoring (agent policy)
- (vault authoring only — not applicable in installed skills) — Authoritative vs composed surfaces
- [`prompts/README.md`](information-completion-contract.md) — Frontmatter and paste [contract](../../../../docs/TERMS.md#contract)
