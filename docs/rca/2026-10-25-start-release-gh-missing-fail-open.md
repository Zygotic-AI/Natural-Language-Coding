# RCA: start-release shipped a `gh` dependency the target runner lacks; existence guards fail open

**Date:** 2026-10-26  
**Context:** Natural-Language-Coding hub — `main` at `5e7147be` (PR #34 merge); first `start-release` dispatch for `v0.4.1`  
**Status:** open (RCA only; no remediation in this record)

**Scope (user words):**

- “RCA only, no fixes.”
- “Use the conduct-rca approach: identify the defective product first, then the process that produced it, climbing until the root is a process/principle gap, not a symptom.”
- “PR #34 (start-release.yml, merged as 5e7147be) ran for v0.4.1 on self-hosted runner vhost11-zygotic-2 … ‘Create release branch’ failed with `gh: command not found` (exit 127).”
- “Infra had stated the runner has git, gpg, python3, sha256sum, not gh.”
- “The PR body said ‘gh on PATH’ as a runner requirement, but nothing verified it before merge, and the workflow was never executed on the real runner before merge.”
- “Separately, the branch/tag-exists refusal guards are written `if gh api …; then refuse`, so any error (missing tool, auth, network) is treated as ‘does not exist’ and the guard passes: fail-open.”
- “(1) Why did a workflow ship that depends on a tool the target runner lacks, with no proof-on-target before merge? Consider the brief I (Helix, PM) wrote, which listed finish-line cases tested only locally.”
- “(2) Why do refusal guards fail open, and is this pattern elsewhere in the repo's checks? List every instance.”
- “(3) What is the highest root, and what single process change prevents the class?”
- “Deliver docs/rca/2026-10-25-start-release-gh-missing-fail-open.md in a draft PR to main.”
- “Report the root in 3 sentences, the fail-open instance list, and the proposed remediation (not implemented).”

**Resolution table (this record):**

| Criterion | This record |
| --------- | ----------- |
| Scope (user words) | Quoted above; outcome is this RCA + draft PR only |
| No narrowing | Q1 (why ship without proof-on-target, including Helix’s local-only finish line), Q2 (why fail-open + every instance), Q3 (highest root + one process change) — all present |
| Question vs implement | RCA only; no product, process, workflow, or runner change |
| Their vocabulary | Defective product, climb, proof-on-target, Helix (PM) brief, finish-line cases tested only locally, fail-open, refusal guards, class |
| Version class | Patch (instance record only) |

---

## 1. Error condition

**Observed (bounded, reproducible):**

1. PR #34 (`cursor/start-release-workflow-1e55` → `main`) merged as `5e7147be1465cdb1c2557d9feb6c36b97a22321e` at 2026-10-26 02:13:49 UTC. Title: “Create release branches via one-click start-release workflow.” Reviews: none. Issue comments: none.
2. Produce session: cloud agent `bc-dbf9d54a-e3a2-5b93-b03d-61b57bc21e55`. First user message is the Helix (PM) brief. Later user messages set `runs-on: [self-hosted, Linux, X64]`, concurrency, App ID `5473379`, and owner sidecar ingest.
3. First live dispatch: GitHub Actions run [40258097353](https://github.com/Zygotic-AI/Natural-Language-Coding/actions/runs/40258097353) at 2026-10-26 02:14:16 UTC on runner `vhost11-zygotic-2` (`/home/gha-runner/zygotic-2/…`), event `workflow_dispatch`, input `VERSION=v0.4.1`, head `5e7147be`.
4. Step “Reject version that is not vX.Y.Z” succeeded. Step “Mint start-release GitHub App token” succeeded (`actions/create-github-app-token@v3`).
5. Step “Create release branch from main HEAD” failed:

```text
/home/gha-runner/zygotic-2/_work/_temp/c90a3759-8c57-4733-953f-ac04f3ac2e13.sh: line 3: gh: command not found
/home/gha-runner/zygotic-2/_work/_temp/c90a3759-8c57-4733-953f-ac04f3ac2e13.sh: line 7: gh: command not found
/home/gha-runner/zygotic-2/_work/_temp/c90a3759-8c57-4733-953f-ac04f3ac2e13.sh: line 11: gh: command not found
##[error]Process completed with exit code 127.
```

Lines 3 and 7 are the branch-exists and tag-exists `if gh api …; then refuse` guards. Line 11 is `SHA="$(gh api "repos/…/git/ref/heads/main" …)"` under `set -euo pipefail`. The job died on the third `gh` (fail-closed create path), after both refusal guards had already treated `command not found` as “does not exist.”

6. Operator-stated infra inventory (not in the produce transcript; treated as a stated repo fact): the runner has `git`, `gpg`, `python3`, `sha256sum`, **not** `gh`.
7. PR #34 body listed “`gh` CLI on the runner PATH” as a runner-side requirement. Nothing in that produce executed `start-release` on vhost11 before merge. PR checks that went green (`fitness`, `piped-install-*`, `rewrite-invariant`) run on GitHub-hosted images and never dispatch `workflow_dispatch`.

**Not the error condition:** App token mint (that step succeeded). Version regex (that step accepted `v0.4.1`). Ruleset bypass actor research. Owner sidecar ingest for the regenerated gate-set manifest.

**Two products of one produce:**

| Product | Observable |
| ------- | ---------- |
| A. Undeclared/unverified tool | Job needs `gh`; target inventory does not have it |
| B. Fail-open refusal | `if gh api; then refuse` collapses missing-tool / auth / network / 5xx / 404 into “absent → proceed” |

---

## 2. Defective product

`.github/workflows/start-release.yml` at `5e7147be` (job `create-release-branch`, `runs-on: [self-hosted, Linux, X64]`):

```yaml
if gh api --silent "repos/${REPO}/git/ref/heads/${BRANCH}"; then
  echo "ERROR: branch ${BRANCH} already exists"
  exit 1
fi
if gh api --silent "repos/${REPO}/git/ref/tags/${VERSION}"; then
  echo "ERROR: tag ${VERSION} already exists"
  exit 1
fi
SHA="$(gh api "repos/${REPO}/git/ref/heads/main" --jq .object.sha)"
```

**What it is:** a `workflow_dispatch` control that creates `release/<version>` from `main` HEAD. The only GitHub API client it uses is `gh`. The only “already exists” refuse is “`gh api` exited 0.”

**What it is not:** a runner-inventory contract. “`gh` on PATH” is PR-body prose. No step runs `command -v gh`. No step distinguishes HTTP 404 from other `gh` failures. No CI job on the PR executes this workflow.

---

## 3. Upstream chain (process before output)

| Layer | What it is | Evidence |
| ----- | ---------- | -------- |
| **(symptom)** | First dispatch on vhost11-zygotic-2: `gh: command not found`, exit 127 | Run 40258097353 job log |
| **6. Product** | Workflow depends on `gh`; existence refuse is `if gh api; then exit 1` | `start-release.yml` lines 48–61 |
| **5. Produce session** | Agent implemented `gh` because the producer VM has `gh`; verified regex / actionlint / PyYAML / `gh api` **from that VM**; wrote “`gh` on PATH” as a runner requirement; did not dispatch on vhost11 | Transcript `bc-dbf9d54a` tools 216/220/223; thinking 214 (“A local test will validate…”); message 246; thinking 197 (401/403 “let the script proceed to creation”) |
| **4. Helix (PM) brief** | Finish line (a)(b)(c) is local/static: reject `v0.4` / `release/v1` / existing version; accept `v0.4.1`; show actionlint/YAML; ruleset JSON diff; PR body lists manual steps. No proof-on-target. No runner inventory. No fail-closed known-bad for the existence refuse | Transcript message 0 |
| **3. Brief amendments** | `runs-on` must be vhost11 self-hosted; labels `[self-hosted, Linux, X64]`; `workflow_dispatch` only; concurrency; gpg/GNUPGHOME if used. Still no “dispatch on vhost11 and show the job” row; still no tool inventory | Transcript messages 117, 161 |
| **2. Merge gate** | PR CI green on GitHub-hosted `ubuntu-latest` / macos / windows. `start-release.yml` is `on: workflow_dispatch` only, so those checks cannot execute it. No review | `gh pr checks 34`; `gh pr view 34` reviews `[]` |
| **1. Finish-line / briefing process** | CONTROL-LIFECYCLE and `validate_hub_brief` require create/change/sign/ingest/rotate, first bootstrap, and “legitimate change to the verifier” **only** when a committed hub brief is marked control-or-gate-design. They have no needle for proof-on-target, declared inventory, or fail-closed probes. The standing produce package is still the 0051/0052 retrofit brief, not this produce. Workflow is not a content type, so Contribution Gate has no type recipe for it | `hub_own_produce.py` `CONTROL_LIFECYCLE_NEEDLES`; `fitness_control_lifecycle.py`; `.nlc/produce-package.json`; `content-types/HOW-TO-ADD.md` |

**Furthest controllable upstream point:** the produce **finish-line / briefing** process. It accepted a brief whose “I will verify” rows are all locally testable, and it has no blocking row that an environment-bound control was executed on the declared target with the declared inventory, with refusal probes fail-closed.

Fixing only `gh` on vhost11, or only the two `if` guards, recreates the class the next time a brief names local/static cases as done.

---

## 4. Question 1 — why this shipped with no proof-on-target

**Because the Helix (PM) brief’s finish line listed only locally-testable cases, and the in-force briefing / CONTROL-LIFECYCLE process treats that as complete.**

### 4.1 The brief (Helix, PM)

First user message of `bc-dbf9d54a` (not labeled “Helix” in the transcript; this record treats it as the brief the PM named):

> Finish line (I will verify): (a) workflow rejects 'v0.4', 'release/v1', and an existing version (known-bad cases), accepts 'v0.4.1'; show actionlint/YAML validation output; (b) ruleset JSON diff keeps pull_request on updates and non_fast_forward, and adds exactly one bypass actor limited in scope; (c) PR body lists the exact manual step(s) Richard or an admin must do, minimized.

| Finish-line row | Where it can be proven | Proven before merge? |
| --------------- | ---------------------- | -------------------- |
| (a) regex reject `v0.4`, `release/v1` | Producer VM | Yes (Python/bash on the cloud agent) |
| (a) existing version refuse | Producer VM + `gh api` from that VM | Yes (`release/v0.4.0` exists; `v0.4.1` absent) — **not** on vhost11, and the probe used the producer’s `gh` |
| (a) accept `v0.4.1` format | Producer VM | Yes (regex only; no branch created) |
| (a) actionlint / YAML | Producer VM (downloaded actionlint 1.7.7) | Yes |
| (b) ruleset JSON diff | Diff in the PR | Yes |
| (c) manual steps in PR body | PR body text | Yes (includes the unverified “`gh` on PATH” sentence) |
| Dispatch `start-release` on vhost11 | Target runner | **No — not a finish-line row** |
| Required tools ⊂ runner inventory | Target runner / infra statement | **No — not a finish-line row** |
| Existence refuse is fail-closed | Known-bad: missing `gh` / 401 / 5xx must REFUSE, not “absent” | **No — not a finish-line row** |

Later amendments (messages 117, 161) changed **YAML targeting** (`runs-on`, labels, concurrency, public-repo trigger). They did not add a proof-on-target row. Infra’s inventory (`git`, `gpg`, `python3`, `sha256sum`, not `gh`) is not in that transcript; the brief never bound it.

### 4.2 What the producer did with that finish line

The agent’s plan (thinking 214): “A **local test** will validate the version regex and file existence… I will run the **existence check against the real API** using the known-bad version tag v0.4.0.” That is exactly finish-line (a). It is also exactly “tested only locally” (plus API calls from a machine that has `gh`).

The agent then **invented** the runner requirement that made those local proofs look portable: PR body, “`gh` CLI on the runner PATH.” That sentence is not a check. PR CI cannot falsify it.

### 4.3 Why merge did not catch it

- `fitness.yml` / `release.yml` / `history-rewrite-invariant.yml` run on GitHub-hosted runners. They never execute `workflow_dispatch`.
- A new workflow that is `on: workflow_dispatch` only has **no PR check** that is that workflow.
- CONTROL-LIFECYCLE greps Planit / AWL / the briefing validator for verifier-lifecycle needles. It cannot fail a chat brief that never commits `control_or_gate_design` and never mentions proof-on-target.
- The standing `.nlc/produce-package.json` still points at `.nlc/briefs/hub-material-0051-0052.md` (C1–C11). Fitness can be MET for a later produce that never wrote a brief for *this* control.
- Contribution Gate has no type recipe for “GitHub workflow” (`content-types/HOW-TO-ADD.md` index: ADR, integrity doc, agent noun, audit, example, Skill). CG-R2/CG-R3 do not apply.
- No human review on PR #34.

The brief is not a side note. It **is** the process input that named “done.” A producer that takes Helix literally will stop at local regex / actionlint / YAML / API-from-elsewhere. That is what shipped.

---

## 5. Question 2 — why the refusal guards fail open, and every instance

### 5.1 Mechanism (this product)

Bash `if cmd; then refuse; fi` is true only when `cmd` exits 0. GitHub’s git-ref API uses **404 + non-zero** for “no such ref.” The same non-zero class includes:

| Probe result | Intended meaning | What the guard does |
| ------------ | ---------------- | ------------------- |
| HTTP 200 | ref exists | Refuse (correct) |
| HTTP 404 | ref does not exist | Proceed (correct **only** for this one error) |
| `gh: command not found` (127) | tool missing | Proceed — **fail-open** |
| HTTP 401 / 403 | auth | Proceed — **fail-open** |
| HTTP 5xx / network | probe failed | Proceed — **fail-open** |
| empty `GH_TOKEN` / wrong repo | probe failed | Proceed — **fail-open** |

The producer recorded this (thinking 197): “Other API failures like 401 or 403 will **let the script proceed to creation and fail later**.” That is fail-open by construction. The Helix finish line asked for “Fails if the branch or tag already exists” and did not ask for “Fails closed if the existence probe is not a clean 404.”

In run 40258097353 the create path later died under `set -e` on the third `gh` (line 11). The two guards had already passed. A future edit that used a different create client, or a run where `gh` exists but auth/network fails on the probe only, would skip the refuse and continue.

**Why this shape was written:** the brief specified existence-refuse; the producer encoded “exists” as “`gh api` succeeded,” which is the natural bash/API idiom and the same idiom the local proof used. There is no in-force known-bad that a refusal probe failing for the **wrong** reason must itself REFUSE.

### 5.2 Exact pattern in checks: `if <probe>; then refuse`

These are the only shell refusal guards of the form `if <probe>; then echo ERROR; exit 1; fi` where probe failure proceeds.

| # | Location | Probe | Intends | Fail-open collapse |
| - | -------- | ----- | ------- | ------------------ |
| 1 | `.github/workflows/start-release.yml` branch guard (lines 48–51) | `gh api --silent repos/…/git/ref/heads/${BRANCH}` | Refuse if `release/<version>` exists | Missing `gh`, 401/403, 5xx, network, wrong repo → “does not exist” |
| 2 | `.github/workflows/start-release.yml` tag guard (lines 52–55) | `gh api --silent repos/…/git/ref/tags/${VERSION}` | Refuse if tag exists | Same |

No other `.github/workflows/*` file on `origin/main` (`fitness.yml`, `history-rewrite-invariant.yml`, `release.yml`) uses this pattern. Those workflows are fail-closed on command failure (`set -e` / `test -f` / Python gates).

### 5.3 Same class in other repo checks (probe error = absent = proceed)

Same collapse: `returncode == 0` (or non-empty stdout) means “exists / known / published”; any other result means the negative case, without distinguishing missing binary, auth, network, or genuine absence. Listed from code, not a hand wave.

| # | Location | Probe | Intends | Fail-open effect |
| - | -------- | ----- | ------- | ---------------- |
| 3 | `tools/nouns/release_tags/release_tags.py` `tag_exists` | `git rev-parse -q --verify ${tag}^{commit}` | Tag present? | Missing `git` / bad repo / any git error → `False` |
| 4 | `tools/nouns/release_tags/release_tags.py` `list_version_tags` | `git tag -l v*.*.*` | List shipped tags | Git error → `[]` (“no tags”) |
| 5 | `tools/nouns/release_tags/release_tags.py` `tag_is_ancestor` | `git merge-base --is-ancestor` | Ancestry | Git error → `False` (not ancestor) |
| 6 | `tools/nouns/release_tags/release_tags.py` `remote_tag_commit_only` | `git ls-remote` | Remote tag peel | Any failure → `""` |
| 7 | `tools/nouns/release_tags/release_tags.py` `align_local_tag_to_remote` | `git fetch` | Align local tag | Fetch failure → `None` |
| 8 | `tools/nouns/release_notes/release_notes.py` (~196) | `tag_exists(from_tag)` | Changelog base | Probe error → clear `from_tag`, continue |
| 9 | `tools/nouns/release_infer/release_infer.py` `branch_exists` | `git show-ref --verify --quiet refs/heads/…` | Local branch present? | Probe error → create path |
| 10 | `tools/nouns/nlc_release_resume/nlc_release_resume.py` `remote_branch_exists` | `git ls-remote --heads` | Remote branch present? | Network/auth/git error → no remote branch |
| 11 | `tools/nouns/nlc_release_resume/nlc_release_resume.py` `resolve_ref_sha` | `git rev-parse` | Resolve tip | Error → `""` → skip branch |
| 12 | `tools/nouns/nlc_release_resume/nlc_release_resume.py` `tag_on_commit` / closed-line detect | `tag_exists` | Line already shipped? | Probe error → not closed (may re-orchestrate) |
| 13 | `tools/nouns/evidence_ref/evidence_ref.py` `is_resolvable_commit` | `git rev-parse --verify` | Pin resolvable commits | Probe error → token omitted |
| 14 | `tools/nouns/nlc_release_state/nlc_release_state.py` `_out` | any git subprocess | Fact string | Non-zero → `""` (“missing SHA/tag”) |
| 15 | `tools/nouns/nlc_release_state/nlc_release_state.py` `_remote_branch_sha` | `git ls-remote` (stdout only) | Remote SHA | Failed ls-remote → `""` → relation `"absent"` |
| 16 | `tools/nouns/nlc_release_state/nlc_release_state.py` `remote_known` | `git fetch` | Remote state known? | Fetch failure → `False` (unknown, not refuse) |
| 17 | `tools/nouns/nlc_release_state/nlc_release_state.py` `_pull_requests` | `gh pr list --json …` | PR facts | `gh` missing / auth / network / bad JSON → `(False, [])` |
| 18 | `tools/nouns/nlc_release_state/nlc_release_state.py` `_publish_status` | `gh release view` | GitHub Release published? | Any non-success → `"missing"` (same bucket as unpublished) |
| 19 | `tools/nouns/release_state/release_state.py` `_publish_decision` | local/remote tag peel | Plan CREATE_LOCAL_TAG / PUSH_TAG | Empty peel from probe error → plan as if tag absent |
| 20 | `tools/nouns/release_main_purity/release_main_purity.py` `check_main_purity` | empty `tag` / `tag_at` | Purity MET when no shipped tag | Failed tag enumeration/peel → **purity passes** |
| 21 | `tools/nouns/mandated_paths/mandated_paths.py` `git_changed_paths` | `git merge-base` / `git diff` | Changed-path set | merge-base fail → diff `HEAD`; failed diff → skip (under-report) |
| 22 | `tools/nouns/nlc_distribution/nlc_distribution.py` `_github_latest_tag` | HTTP then `ls-remote` | Latest published tag | Any `HTTPError` (404/401/5xx) → fallback; ls-remote fail → `[]` |
| 23 | `goals/hub_release/execute.sh` `CREATE_RELEASE_LINE` | `git show-ref --verify --quiet` | Checkout vs create | Any show-ref failure → `checkout -b` |
| 24 | `goals/sign_adrs/execute.sh` `sig_ok` | `gpg --verify … \|\| true` | Valid sidecar? | Missing/broken gpg → no `VALIDSIG` → treat as unsigned (proceed to sign) |

**Call-site notes (not extra patterns):** `tag_exists` / `branch_exists` / `remote_branch_exists` / `is_resolvable_commit` are the primitives behind rows 8–13. `reachable_tags` filters through `tag_exists` + `tag_is_ancestor` (same collapse).

### 5.4 Fail-closed counterparts (not instances)

Listed so “every instance” is not inflated:

| Location | Why fail-closed |
| -------- | --------------- |
| `start-release.yml` version regex `if [[ ! =~ ]]; then exit 1` | Invalid input refuses |
| `start-release.yml` lines 56–61 (`SHA="$(gh api …)"`, `test -n`, POST) | Under `set -e`; this is what killed run 40258097353 |
| `.cursor/hooks/nlc-goal-write-gate.sh` | Missing `jq` **and** `python3` → deny |
| `.cursor/hooks/nlc-planit-identity.sh` | Identity check non-zero → deny |
| `scripts/install.sh` | `if ! command -v git` → exit 1 |
| `goals/sign_adrs/execute.sh` secret-key preflight | `if ! gpg --list-secret-keys` → die |
| `tools/nouns/nlc_release_context/nlc_release_context.py` | Git failure must not return `contained` (ADR 0049 context closure) |
| `tools/nouns/evidence_ref` + tag/shipped gates `resolve_commit` | Resolution failure → `*:REFUSE` |
| `goals/hub_release_prep/execute.sh` | `if ! git diff --quiet` → NOT_MET (git error is non-quiet) |
| `assert_release_resume_invariant_passes.py` | `await_merge` without remote branch → ASSERT:FAIL |

ADR 0049 §10 already forbids release-planner **context** that can fail open to `contained`. That gate does **not** cover workflow refusal probes or `gh`/`git` existence helpers in §5.3.

---

## 6. Question 3 — highest root and the one process change

### 6.1 Candidate roots (at most three)

| Candidate | §3 bar | Verdict |
| --------- | ------ | ------- |
| Install `gh` on vhost11, or rewrite the job to `curl` + `GITHUB_TOKEN` | Output-only; next environment-bound workflow can still ship on a local finish line | Reject (symptom) |
| Rewrite the two `if gh api` guards to fail closed (404 ≠ 401 ≠ missing binary) | Fixes product B; product A and the class remain | Too low |
| Finish-line / briefing process must refuse an environment-bound produce whose “done” rows are only local/static, and must carry a fail-closed known-bad for every refusal probe | One process change; deterministic; earliest controllable; matches Helix’s brief as the process input | **Survives** |

### 6.2 The one thing

> What **one** deterministic, actionable thing, if it were different, would have **prevented this error condition from arising**?

**Answer:** The produce finish-line / briefing process (Helix-style “I will verify” rows, CONTROL-LIFECYCLE, `validate_hub_brief`, Contribution Gate for environment-bound controls) must treat a brief that lists **only locally-testable cases** as incomplete when the artifact declares a target environment. The blocking rows are: **proof-on-target** (the control executed on that environment using only the declared inventory) and a **fail-closed known-bad** (missing required tool, and any probe error other than the intended condition, is REFUSE — not “absent”).

That is one process change. It sits above “add `gh`” and above “fix the two `if`s.” It is the same family as RCA 6 / Climb 4 / the signed-whole-tree climb: a compiled finish line that never named the known-bad that would have refused the produce.

### 6.3 Prevention test

If **proof-on-target + fail-closed-probe known-bad** had been a blocking finish-line row **before** the Helix brief was accepted and **before** PR #34 merged, **`gh: command not found` on vhost11-zygotic-2 and fail-open existence guards** could not have been the shipped path because **the brief’s local-only (a)(b)(c) would have been incomplete, and a required vhost11 dispatch would have failed on the missing tool / the missing-tool known-bad before merge.**

**Completed:** yes (mechanism: design-process requirement). Product shapes that would then pass are options below. Do not implement here.

**Class:** process (briefing / finish-line / known-bad class). Not output. Not “the runner is missing a package.”

### 6.4 Root in three sentences

The defective product is `start-release.yml`: it calls `gh` on a runner whose stated inventory does not include `gh`, and it encodes “already exists” as `if gh api; then refuse`, so missing-tool / auth / network are treated as “does not exist.” That product is the output of a Helix (PM) brief whose finish line named only local regex / actionlint / YAML / API-from-elsewhere cases, plus a produce session that treated those cases as done and wrote “`gh` on PATH” as unverified prose. The highest root is the finish-line process itself: it has no blocking row that an environment-bound control was proven on the declared target with the declared inventory, and no fail-closed known-bad for refusal probes, so a local-only brief is accepted as complete.

---

## 7. Impact / scope

- `release/v0.4.1` was not created. The documented “release branches are created only via start-release” path is red on first use.
- The two existence guards did not refuse; they passed. The job failed later on the third `gh`. A retry after installing `gh` without rewriting the guards leaves fail-open intact.
- PR CI cannot detect this class for any `workflow_dispatch`-only, self-hosted workflow.
- Release-planner checks in §5.3 can still treat `gh`/`git` probe errors as “no tag / no branch / unpublished” (ADR 0049 closed context to `contained` only).
- This record is docs-only under `docs/rca/` (provenance; not a gate-set member). Syncing `integrity/hub-content-tree-hash.txt` would be a signed-member edit; this produce does not do that.

---

## 8. Timeline (brief)

| Time (UTC) | Event |
| ---------- | ----- |
| 2026-10-25 | Owner approved replacing manual ruleset toggling with a one-click workflow (Helix brief states this) |
| 2026-10-26 00:40 | Produce `bc-dbf9d54a` starts; Helix finish line (a)(b)(c) |
| 00:43–00:44 | Amendments: vhost11 self-hosted; labels `[self-hosted, Linux, X64]`; concurrency; gpg note |
| 00:46 | Local regex / `gh api` from producer VM / actionlint 1.7.7 / PyYAML |
| 00:47 | PR #34 opened; body requires “`gh` on PATH” |
| 00:59–01:05 | App ID 5473379; remanifest; owner sidecar; mark ready; wait on CI |
| ~02:13 | PR #34 merged (`5e7147be`); no reviews |
| 02:14 | Dispatch `v0.4.1` on vhost11-zygotic-2; `gh: command not found`; exit 127 |

---

## 9. Mechanism on reproduction

**Confirmed (product), at `5e7147be` + run 40258097353:**

- Workflow file uses `gh` four times in the create step; runner log prints `gh: command not found` on the first three invocations that executed (two `if` probes + SHA fetch). POST never ran.
- `if gh api; then … exit 1; fi` did not enter the refuse body (no “already exists” lines in the log).
- PR checks on #34 are GitHub-hosted and do not include a `start-release` job.

**Confirmed (process):**

- Helix brief message 0 finish line has no vhost11 dispatch and no inventory row.
- Transcript has no statement that the runner lacks `gh`. Agent message 246 requires `gh` on PATH. Infra inventory is operator-stated, outside that transcript.
- `CONTROL_LIFECYCLE_NEEDLES` = `create, change, sign, ingest, rotate` / `first bootstrap` / `legitimate change to the verifier`. No proof-on-target. No fail-closed probe.
- `.nlc/produce-package.json` `brief_ref` remains `.nlc/briefs/hub-material-0051-0052.md`.

---

## 10. Contributing factors

- Producer VM has `gh`; target runner does not. Local proof of the existence idiom is not transferable.
- `workflow_dispatch` + self-hosted means PR CI is a different machine class than the job.
- Agent noted 401/403 fail-open in thinking and still shipped the idiom; the finish line did not forbid it.
- ADR 0055 was applied as a **gate-set pin move** (remanifest + owner sidecar), not as a control-lifecycle walk of “run this job on vhost11.”
- Workflow is not a content type; no type recipe can refuse a missing proof-on-target step.
- No review on PR #34.
- ADR 0049 fail-open forbid is scoped to planner context `contained`, so it did not see these guards.

---

## 11. Remediation (not implemented)

The process row in §6.2 is a prerequisite for all product options. Without it, the next brief can again list only local cases.

### Process (the one change)

Extend the finish-line / briefing / CONTROL-LIFECYCLE / Contribution-Gate path so that when a produce declares a target environment (self-hosted runner labels, hook host, named inventory):

1. A brief whose verify rows are only local/static (regex, actionlint, YAML, API from the producer VM) is **incomplete**.
2. Blocking row: **proof-on-target** — the control ran on that environment; required tools were observed on that environment; happy path and refusal cases used only the declared inventory.
3. Blocking known-bad: **missing required tool REFUSE**; **probe error other than the intended condition REFUSE** (404 ≠ 401 ≠ 127). Success-means-exists refusal is incomplete.

Verification of the process row (after a later produce, not this one): a fixture brief that names only actionlint + regex is refused; a fixture workflow whose existence guard is `if probe; then refuse` fails the known-bad; a fixture that dispatches on a runner missing a required binary is NOT_MET before merge.

### Product options (after the process row)

Every option must pass: dispatch `start-release` on the stated vhost11 inventory; missing `gh` (or whatever the job actually needs) is a hard refuse with a distinct error; branch-exists / tag-exists refuse only on a confirmed 200; 401/403/5xx/network refuse; a clean 404 proceeds to create.

| Option | Shape | Tradeoff |
| ------ | ----- | -------- |
| **A. Keep `gh`; bind inventory** | Install `gh` on vhost11; add a first-step `command -v gh` refuse; rewrite existence checks to inspect HTTP status | Fastest restore of the current YAML. Still depends on a tool infra did not list. Process row still required or the next job can add `jq` the same way |
| **B. Drop `gh`; use `curl` + the minted App token** | Same API, tools already implied by the runner image / `create-github-app-token` | Matches stated inventory better (`curl` is not in the stated list either — must be proven on target). Rewrites the job |
| **C. Fail-closed probes + inventory preflight, either A or B** | Preflight: each required binary `command -v` or REFUSE. Existence: parse status; only 404 means absent; anything else REFUSE | Closes product B regardless of client. This is the product half of the known-bad |
| **D. Status quo (install `gh` quietly, leave `if gh api` as-is)** | Symptom patch | Missing-tool may go away; fail-open remains. **Rejected** as a remediation |

Do not implement A–C in this record.

---

## 12. Preventive action (single tracked item — not done)

| Field | Value |
| ----- | ----- |
| Action | Make proof-on-target + fail-closed-probe known-bad a blocking finish-line row for environment-bound produce; refuse local-only briefs. Then pick a product option that passes that known-bad (A+C or B+C). |
| Owner | hub |
| Path / artifact | Briefing validator (`tools/nouns/hub_own_produce/hub_own_produce.py`), CONTROL-LIFECYCLE (`tools/nouns/fitness_control_lifecycle/`, Planit / AWL needles), Contribution Gate / type recipe if workflow becomes a type; product follow-up on `.github/workflows/start-release.yml` and vhost11 inventory |
| Verification | A brief that only lists regex/actionlint/YAML is incomplete. A workflow whose refuse is `if probe; then exit 1` fails the known-bad. A required-binary-missing fixture REFUSE. After product fix: dispatch `v0.4.1` on vhost11-zygotic-* creates `release/v0.4.1` or refuses for a named, intended reason |
| Belief / gate touch (ADR 0025) | Unsuitable process: finish line that accepts local substitutes for target execution, and refusal probes that fail open. Touches briefing / CONTROL-LIFECYCLE; after Accept, the workflow and runner inventory |

---

## 13. Follow-up (detection only)

- Run 40258097353 is the live specimen of both products. Do not treat “install `gh` and re-run” as the RCA close.
- If a written infra inventory exists outside this repo, attach it to the remediation produce so “declared inventory” is a file, not chat.

RCA only. No remediation commit.
