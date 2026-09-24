---
name: release
description: Hub ship entrypoint — agent closes continuity (commit, SSOT, stale branches), readiness, then ./release. Use when the user wants to release, ship, promote, tag, or run ./release.
disable-model-invocation: true
---

# Release (`/release`)

**You remember one thing:** invoke **`/release`** in chat.

**Your job:** run the **full pre-ship pipeline** — not a checklist for the human. **`/release` authorizes** the agent to commit the hub continuity/product batch, fix SSOT headers, remove stale `release/v*` branches, prove gates, run inference, then start **`./release`**. The human stays on **interactive** `./release` prompts only (release class, release notes text, “PR merged” wait, tag-move confirm) — not on git hygene the agent can do.

**Terminal orchestrator:** [`./release`](../../../docs/adoption/RELEASE.md) — ADR 0039. Start it after **Ship: GO** (or confirmed **GO with residuals**).

**Do not** instruct the user to “commit and merge”, “update FINDINGS`, “delete stale branch”, or run `full-nlc-audit` by hand — **do it** (or fix failures and retry). **Do not** write `Released-by:`.

## Gate (default-closed)

Do **not** run `./release` until every **blocking** row is true.

| Criterion | Blocking? | Pass when | Evidence |
| --------- | --------- | --------- | -------- |
| Repo root | yes | NLC hub workspace | Path |
| Agent closeout (Step 1A) | yes | Clean tree at ship HEAD **or** resume leg with no ship-intent dirty edits | `git status --porcelain` |
| Resume probe | yes | Step 0 complete | `nlc_release_resume.py` |
| Machine continuity | yes | **prepare:** `release-prep` MET on ship HEAD. **await_merge / tag_ready:** waived | Command output |
| Hub compile | yes | `python3 tools/ci_fitness.py` → CI:MET on ship HEAD | Exit 0 |
| P0/P1 inference | yes | None from Step 4 | Inference apex |
| Product residuals | yes when P2/P3 | User confirms **once** if open product gaps remain | Chat |
| `./release` started | yes on GO | Orchestrator invoked from repo root | Terminal |

**Done signals:** Closeout done; **Ship** verdict; `./release` running or honest NOT_MET with agent fix loop.

## Procedure

### 0 — Resume probe (always first)

```bash
python3 tools/nlc_release_context.py --list-branches
python3 tools/nlc_release_resume.py --emit json
git tag -l
git ls-remote --tags origin 'v*' 2>/dev/null | tail -5
```

- **`tag` / `planned_tag` in JSON** = name `./release` would create — **not** an existing ref unless **`git_tag_on_merge`** is true.
- **`stale_release_branches`:** agent **deletes** those refs in Step 1A (local + `origin` when permitted).

| Phase | Agent path |
| ----- | ---------- |
| **prepare** | Steps 1 → 1A → 2–6 |
| **await_merge** / **tag_ready** | Skip 1A commit burst if tree clean; skip Step 3 `release-prep`; **GO** → `./release` |
| **complete** | Report shipped; new ship needs fresh prepare on `main` |

Never tell the user to run `./release finish` or `prepare` — **`./release`** only.

### 1 — Bound ship state

Record branch, short SHA, dirty file count. On **`main`** for **prepare**.

### 1A — Agent continuity closeout (mandatory on **prepare**)

**When the user invokes `/release`, treat uncommitted hub work as ship intent** unless they say *resume only*, *audit only*, or *no commit*.

Execute **in order** (fix and retry on NOT_MET; do not dump steps on the user):

1. **Prove working tree** — `python3 tools/ci_fitness.py` → **CI:MET**. If FAIL, fix until MET (jidoka).
2. **Stale `release/v*`** — for each name in **`stale_release_branches`**: `git branch -D <branch>`; `git push origin --delete <branch>` when remote exists (no force-push to `main`).
3. **Stage and commit** all ship-intent changes on `main` (one or two commits: feature batch, then SSOT header if needed). Use repo commit message style; never `--no-verify`.
4. **FINDINGS header** — set `` `last_pass_sha:` `` and **Last pass** line to `git rev-parse --short HEAD`; run `python3 tools/fitness-findings-last-pass-fresh.py` → MET. Commit if not in step 3.
5. **Inference record** — update [`integrity/full-nlc-audit-inference-record.json`](../../../integrity/full-nlc-audit-inference-record.json): `audit_sha`, `machine_verdict`, `continuity_verdict`, `phases_summary`, empty `p0_p1_product_blockers` when true. Commit if needed.
6. **TODO continuity** — mark completed closeout rows `@done` when predicates MET (same commit or follow-up).
7. **Re-prove** — `python3 tools/ci_fitness.py` → CI:MET on final HEAD.
8. **Clean tree** — `git status --porcelain` empty.

**Stop / NO-GO only if:** CI cannot MET after fix attempts; git push rejected; P0/P1 inference; user refused product residuals.

**Waived:** optional `--profile full` on clean tree (not required for `./release`).

### 2 — Outstanding scan (inform verdict)

Scan [`TODO`](../../../TODO), [`FINDINGS.md`](../../../FINDINGS.md), [`integrity/uc-product-status.json`](../../../integrity/uc-product-status.json). Tag **continuity** vs **product** ([`references/release-vs-product.md`](references/release-vs-product.md)). **Product** open items → **GO with residuals** after one confirmation; do not block on UC14/16/20 expansion by default.

### 3 — Machine (`release-prep` on **prepare** only)

```bash
python3 tools/full-nlc-audit.py --check --profile release-prep
```

Skip when **await_merge** / **tag_ready** / **complete**. NOT_MET → agent fixes (Step 1A loop), not user homework.

**tag_ready:** optional `python3 tools/nlc_release_tag_gate.py --check --commit … --tag …`

### 4 — Inference

```bash
python3 tools/full-nlc-audit.py --emit-inference-checklist
```

Compressed phases; apex **Continuity: PASS | FAIL | PASS with residuals**.

### 5 — Ship verdict

| Verdict | When | Agent next |
| ------- | ---- | ---------- |
| **Ship: NO-GO** | Unfixable gate / P0/P1 | Keep fixing; no `./release` |
| **Ship: GO with residuals** | Product gaps only | One-line impact + **yes** → Step 6 |
| **Ship: GO** | Closeout + machine + inference | Step 6 |

### 6 — Run `./release`

```bash
./release
```

Use `./release --yes` only if the user asked for routine auto-confirm. Report **NOT_MET** verbatim; agent fixes what is fixable outside interactive prompts, then re-run.

**Human-only at terminal:** release class, release notes content, merge wait, retag confirm.

## Routing

| Need | Skill |
| ---- | ----- |
| Machine/inference detail | [`full-nlc-audit`](../full-nlc-audit/SKILL.md) |
| Compile proof | [`bbp-confirmer`](../bbp-confirmer/SKILL.md) |
| Large hub change plan | [`planit`](../planit/SKILL.md) |

## Reference

- [`docs/adoption/RELEASE.md`](../../../docs/adoption/RELEASE.md)
- [`references/release-vs-product.md`](references/release-vs-product.md)
