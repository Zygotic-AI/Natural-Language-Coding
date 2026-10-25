# RCA: CI wall-clock explosion after per-file ADR signatures; local fitness and rewrite drill fail for separate reasons

**Date:** 2026-10-25  
**Context:** Natural-Language-Coding hub — PR #31 head `c9e8934` on `cursor/per-file-adr-sigs-54bd`  
**Status:** open (analysis only; no remediation in this record; no signatures — C8)

**Scope (user words):**

- “RCA only, no fix, no signatures (C8).”
- “Find: (1) the exact step/command where time goes (reproduce locally; time each step; check for per-ADR gpg verification cost, gpg-agent/keyring/pinentry blocking in non-interactive CI, the history-rewrite drill rerunning full fitness or re-verifying all signatures per rewritten commit, quadratic work over 56 sigs, etc.). (2) Root cause per conduct-rca: which produced artifact is defective and what process let it through (e.g. PR #31's finish line didn't time CI or run the drill with real owner sigs present). (3) Remediation options, each with expected run time; include moving the drill to a release-time step on a self-hosted box (vhost11) as one option.”
- “Richard's local run on c9e8934: `bash tools/ci-fitness.sh` fails FAST (3.6s) at '=== ADR 0050 evidence identity ===': `VIOLATION FINDINGS.md pins commits: d83c64a, a5287e2`. Yet GitHub fitness passed on this head in 18-22 min. Explain the discrepancy.”
- “`python3 tools/assert-history-rewrite-invariant-passes.py` fails in 0.4s: `git clone --local <repo> /tmp/nlc-rewrite-drill-*/baseline` exit 128 (stderr not captured). Determine why … and whether the same thing makes the CI drill hang instead of fail. Note the drill doesn't surface git stderr.”
- “Richard principle: anything that must deterministically pass must be produced by a deterministic script. The release-prepare edits (hub-release-record.json, DESCRIBE/FINDINGS 'last tagged ship') were hand-edited by an agent, which is how commit ids landed in FINDINGS.md. Evaluate whether a deterministic prepare script exists (`./release prepare?`) and why it wasn't used/required; include 'prepare edits come only from a script, checks verify its output' as a remediation.”
- “Richard's clone stderr: `fatal: failed to create link '/tmp/drilltest/.git/objects/1a/27b7...': Invalid cross-device link` — the drill's `git clone --local` hardlinks objects and his /tmp is a different filesystem. Record as a portability defect (fix: `--no-hardlinks` or scratch dir on the repo's filesystem, plus surface git stderr). Treat the GitHub hang as a separate cause unless evidence links them.”

**Resolution table (this record):**

| Criterion | This record |
| --------- | ----------- |
| Scope (user words) | Quoted above; outcome is this RCA + draft PR only |
| No narrowing | Time sink, gpg/pinentry/56-sig hypotheses, process that let it through, vhost11 option, local FINDINGS fail vs CI pass, local clone 128, prepare-script principle, cross-device hardlink — all present |
| Question vs implement | Analysis only; no product, CI, or signature change |
| Their vocabulary | Exact step/command, hang, per-file ADR sigs, finish line, real owner sigs, vhost11, pins commits, clone --local, Invalid cross-device link, deterministic script, prepare edits |
| Version class | Patch (instance record only) |

Three **independent** error conditions. They share a tree (`c9e8934`) and a finish line (PR #31). They do **not** share one mechanism. Conduct-rca (the hub root-cause standard: one preventive change per condition, process before output) forbids blending them.

| Id | Error condition | Mechanism |
| -- | --------------- | --------- |
| A | GitHub `fitness` 18–22 min and `rewrite-invariant` 37–54+ min after the owner sidecar lands | Full passing hub-ci-fitness, twice paying 311× full gate-set derive; the drill runs that profile three times |
| B | Richard’s `ci-fitness.sh` dies in 3.6s on `FINDINGS.md pins commits: d83c64a, a5287e2`; GitHub fitness on the same head is MET | History-ids grades the **local object database**, not the tree. Those SHAs are not on GitHub. FINDINGS is an agent-edited surface |
| C | Richard’s rewrite drill dies in 0.4s at `git clone --local` (exit 128); GitHub’s drill proceeds | `--local` hardlinks into `/tmp` across filesystems. The drill swallows git stderr. **Not** the GitHub wall-clock |

---

## 1. Error condition A — GitHub wall-clock

**Observed (bounded, reproducible) at `c9e8934`:**

| Run | Event | Job / step | Wall |
| --- | ----- | ---------- | ---- |
| 40219156431 (push `d35f8e3`, unsigned manifest, no owner sidecar) | rewrite-invariant SUCCESS | step `ADR 0050 history rewrite drill` | 4 min 21 s |
| 40219161859 (PR, same SHA) | rewrite-invariant SUCCESS | same step | 5 min 58 s |
| 40228783969 (PR `5c377a3`, 56 ADR `.md.asc` present, unsigned manifest) | fitness FAILURE | Hub fitness suite | 2 min 15 s |
| 40228783998 | rewrite-invariant SUCCESS (release profile **exit 1** == exit 1) | same step | 6 min 35 s |
| 40230451638 (push `c9e8934`, sidecar present) | fitness SUCCESS | Hub fitness suite 20:22:24Z–20:44:49Z | **22 min 25 s** |
| 40230455421 (PR `c9e8934`) | fitness SUCCESS | Hub fitness suite | **18 min 5 s** |
| 40230451697 job 121280825140 | rewrite-invariant **cancelled** | step `ADR 0050 history rewrite drill` 20:22:28Z–21:16:26Z | **54.1 min** then cancelled |
| 40230451697 rerun job 121294265385 | rewrite-invariant **SUCCESS** | same step | **37.0 min** (21:18:51Z–21:55:54Z) |
| 40230455447 job 121294648287 | rewrite-invariant still in progress when this record was written | same step | 30+ min observed |

The cancelled 54-minute job and the 37-minute success are **not a deadlock**. They are the same command finishing slowly enough to look hung. `nlc.py verify` after the fitness suite is ~0.3 s (`PLANIT_IDENTITY:MET` at 20:44:46Z). Piped-install jobs stay ~20 s.

**Exact command on the rewrite job:**

```text
python3 tools/assert-history-rewrite-invariant-passes.py
```

That script (`tools/nouns/assert_history_rewrite_invariant_passes/assert_history_rewrite_invariant_passes.py`) does, in order:

1. `git clone --local` of the hub into a temp `baseline`
2. `python3 tools/nlc_gate.py --profile release` (full **release** profile)
3. another `--local` clone, then `git filter-branch --env-filter … -- --all`
4. release profile again
5. `git clone --depth 1 --local` and release profile a third time

Release profile (`integrity/releasable-gates.json`) is `pipeline-blockers`, `planit-skill-identity`, `hub-content-tree-fresh`, **`hub-ci-fitness`**. `hub-ci-fitness` is the entire `run_ci_fitness_suite()` (fail-fast, no `CI_FITNESS_CONTINUE`).

`ci_fitness.py` `fail()` exits on the first red check. On `5c377a3` that is `fitness-gate-set-manifest` (unsigned sidecar / Content-SHA256 mismatch) after ~2 min. The drill then compares exit 1 to exit 1 and prints `ASSERT:PASS … (release profile exit 1)` — CI log 40219156431 at 18:04:36Z. On `c9e8934` the sidecar verifies, the suite runs to `CI:MET`, and the drill pays that cost **three times**.

---

## 2. Where the time goes (hypotheses, timed)

Local machine: this checkout at `c9e8934`, Python 3.12, GnuPG 2.4.4. Commands timed with `time.perf_counter`. Logs under `/tmp/rca-timings/` (copy at `/opt/cursor/artifacts/rca-timings/`).

### 2.1 Ruled out as the 8–22 minute sink

| Hypothesis | Local evidence | CI evidence |
| ---------- | -------------- | ----------- |
| Per-ADR `gpg --verify` of 50 Accepted ADRs | `verify_adr_detached_signature` 0.014–0.022 s each; `fitness-adr-owner-sidecar` **0.734 s** MET | Not a 520 s gap |
| Fresh `GNUPGHOME` + import per verify | 5 sequential verifies 0.070 s; reused home 0.024 s | Same API in CI |
| gpg-agent / pinentry block in non-interactive CI | Isolated env (no `DISPLAY`, `TERM=dumb`, stdin `/dev/null`, `setsid`): import 0.009 s, verify 0.003 s. `--pinentry-mode error` 0.003 s. pinentry is `pinentry-gnome3` 1.2.1; `--batch` does not hang here | CI log has `gpg decrypt failed` only on **placeholder** occupancy landmines (~10 s), then continues |
| Quadratic work over 56 `.md.asc` files | `assert-adr-approval-mismatch-fails` 0.654 s for 48 ACTIVE.md numbers | No 56×56 loop in the verifier |
| `filter-branch` of 534 commits | clone 0.114 s + filter-branch **14.163 s** | Fast rewrite runs (4–6 min) already included this |
| Re-verifying all signatures **per rewritten commit** | The drill rewrites author metadata, then runs the **release profile** (content gates), not `git log` × gpg | Same |

### 2.2 The two ~8.7 minute silences on GitHub fitness `40230451638`

Parent `---` labels are block-buffered. Child `RESULT:` / `ASSERT:` lines timestamp when they flush.

| From | To | Δ | What ran |
| ---- | -- | - | -------- |
| 20:24:50.052Z `RESULT:MET` | 20:33:30.501Z `RESULT:MET` | **520.4 s** | `fitness-hub-scope-derived` (after `fitness-gate-set-manifest`, so **unsigned trees never reach it**) |
| 20:36:11.382Z `ASSERT:PASS hub_only_fitness…` | 20:44:46.599Z `handoff_preflight:MET` / `CI:MET` | **515.2 s** | `preflight_handoff` → `validate_hub_material_package` (in-process; no stdout until done) |

Unsigned fitness `40228783969` fails at 20:03:32Z with `VIOLATION integrity/gate-set-baseline.manifest.sha256: Content-SHA256 mismatch` and **never** shows those gaps.

### 2.3 Mechanism (confirmed on this checkout)

`derived_changed_paths` is `git diff --name-only <merge-base v0.3.0>..HEAD` → **311 paths** at `c9e8934`.

`validate_hub_material_package` (`tools/nouns/hub_own_produce/hub_own_produce.py`) **overwrites** the produce package’s `changed_paths` with that list, then calls `validate_hub_gate_diff_role_separation`:

```python
gate_hits = [p for p in changed if is_gate_set_path(root, p)]
```

`is_gate_set_path` calls `derive_gate_set_paths` **every time** (3882-path AST/text closure; **1.004 s** here).

| Call | Local time | derive behavior |
| ---- | ---------- | --------------- |
| `derive_gate_set_paths` once | 1.004 s (3882 paths) | baseline |
| `manifest_bytes` / `fitness-gate-set-manifest` | 2.190 s / 3.169 s MET | one derive + rehash |
| `fitness-hub-scope-derived` | **291.354 s** MET | ~311 derives |
| `preflight_handoff` | same function as above | second ~291 s on the success path |
| `fitness-known-bad-ssot` | 37.707 s | 9× `gate_set_tamper` (~3 s) + 5× role_separation on **fixture** paths (~1.9 s), not the 311-list |

291 s / 1.00 s ≈ 291 derives. CI ~520 s / 311 ≈ 1.67 s per derive (same shape, slower runner).

Two success-path calls: **~10 min local, ~17 min on GitHub**, plus the rest of the suite (~2 min on the unsigned fail-fast path, plus post-manifest landmines). That is the 18–22 min fitness job.

The rewrite drill: 3 × (that suite) + ~14 s filter-branch. Expected **54–66 min** if each suite is 18–22 min; measured **37 min** on the successful rerun (cache / quieter runner) and **54 min cancelled** on the first attempt. Matches “hang.”

**Not linked to error condition C.** GitHub `ubuntu-latest` `/tmp` and the workspace are the same device class; `clone --local` in CI succeeds (checkout + Python setup finish in ~3 s, then the drill step runs for tens of minutes).

---

## 3. Defective product (A)

The produced artifact that is too slow when **green** is the conjunction of:

| Piece | Path | What it does |
| ----- | ---- | ------------ |
| Per-call derive | `is_gate_set_path` → `derive_gate_set_paths` | Full CI-load closure, no cache |
| 311-path list-comp | `validate_hub_gate_diff_role_separation` after `validate_hub_material_package` replaces `changed_paths` | 311 × derive |
| Fail-fast suite | `ci_fitness.fail` | Unsigned sidecar exits before the 311-loop; **valid sidecar is the trigger**, not the CPU |
| Drill ×3 | `assert-history-rewrite-invariant-passes` + `history-rewrite-invariant.yml` on every push/PR | Three full release profiles |

The 56 ADR `.md.asc` files and the signed manifest sidecar are **not** the inner loop. They are what lets `fitness-gate-set-manifest` pass so the expensive checks run. Earlier commits on this PR already had the 56 sigs (`1d34e86`) and still finished rewrite in 2–6 min because the **manifest sidecar** was missing or stale.

---

## 4. Error condition B — local history-ids vs GitHub MET

**Richard (Linux, miniconda Python 3.11, `c9e8934`):** `bash tools/ci-fitness.sh` → 3.6 s → `CI:FAIL fitness-no-history-ids-in-evidence` → `VIOLATION FINDINGS.md pins commits: d83c64a, a5287e2`.

**GitHub fitness `40230451638` / `40230455421`:** same head, **SUCCESS** 18–22 min. The check **is not skipped** on the hub tree. CI log 20:22:33Z: `--- fitness-no-history-ids-in-evidence ---`. The invoice-correct loop **skips** that file (`hub_only_fitness`); that skip is adopter-tree only.

### 4.1 The check

`commit_pins_in_text` (`tools/nouns/evidence_ref/evidence_ref.py`) keeps a 7–40 hex token only when `git rev-parse --verify <token>^{commit}` succeeds **in that clone’s object database**. Same `FINDINGS.md` bytes, different objects → different verdict.

This checkout and `git fetch origin main` (259 commits on `origin/main` tip `b3e6622`):

```text
d83c64a: fatal: Not a valid object name
a5287e2: fatal: Not a valid object name
```

GitHub API: **HTTP 422** `No commit found for SHA` for both. `python3 tools/fitness-no-history-ids-in-evidence.py` here → `RESULT:MET`.

Those tokens are prose in FINDINGS (wave-1 / wave-2):

- Line 93: `**Audit SHA:** \`d83c64a\` (\`origin/main\`)`
- Line 118: `**Base:** \`main\` after #38 (\`a5287e2\`)`

`git log -S` first introduction: `b5444e0` (2026-09-22, wave-2 residuals), plus earlier wave-1 commits `ce00c17` / `aea1512`. **Not** `5c377a3` (no FINDINGS hunk). **Not** `cfe39da` (only `v0.3.3` → `v0.4.0` on the last-pass / last-tagged-ship line).

Richard’s laptop has those objects (older local history, another remote, reflog). GitHub Actions `actions/checkout@v4` `fetch-depth: 0` fetches **this ref’s ancestry**, not every object that ever existed on a developer machine, and not SHAs the GitHub repo does not have.

**Different checkout state: yes (object DB). Check skipped in CI: no (hub path). FINDINGS edited by `5c377a3`: no.** `cfe39da` did hand-edit FINDINGS last-tagged-ship; it did not add these two tokens. The **class** of edit is still the process defect in §6.

---

## 5. Error condition C — `git clone --local` exit 128

**Richard:** `python3 tools/assert-history-rewrite-invariant-passes.py` → 0.4 s → `CalledProcessError` exit 128 on

```text
git clone --local <repo> /tmp/nlc-rewrite-drill-*/baseline
```

Stderr (Richard): `fatal: failed to create link '/tmp/drilltest/.git/objects/1a/27b7...': Invalid cross-device link`.

`--local` **hardlinks** object files. `nlink=2` on pack files after a `--local` clone on this VM. If `/tmp` and the repo are different filesystems, `link(2)` returns `EXDEV`. Git 2.43 then fails the clone (exit 128) unless `--no-hardlinks` or a scratch dir on the **repo’s** filesystem is used.

This VM: `/workspace` and `/tmp` are the same device (`10494320`); `--local` succeeds. Worktree source and shallow source also succeeded here. `protocol.file.allow=never` also yields 128 (`fatal: transport 'file' not allowed`) — a second portability footgun, **not** Richard’s stderr.

The drill uses `capture_output=True, check=True` and **prints none of git’s stderr**. That is why the first report was only “exit 128.”

**Does this make the GitHub drill hang?** No. CI checkout + `clone --local` finish in seconds; the drill step then spends 37–54 minutes inside `nlc_gate --profile release`. Separate cause.

---

## 6. Prepare edits and the deterministic-script principle

**Principle (Richard, 2026-10-25):** anything that must deterministically pass must be produced by a deterministic script.

### 6.1 What exists

| Surface | Writer script | Checker |
| ------- | ------------- | ------- |
| `integrity/hub-release-record.json` | **Yes:** `python3 tools/nlc_release_record.py --version --branch` (`WRITE_RECORD` in `goals/hub_release/execute.sh`). Schema 2: version, `release_branch`, `content_tree_hash_ref`. | `validate_record` / tag gate |
| FINDINGS / DESCRIBE **Last tagged ship** / **Shipped git tag** | **No writer.** `fitness_findings_shipped_tag_sync` and `nlc_release_tag_gate.check_findings_describe_identity` only **read** phrases | Phrase vs shipped/file version |
| FINDINGS `Last pass: \`<sha>\`` (old line shape) | `goals/hub_release_prep/execute.sh` `sed` inserts `git rev-parse --short HEAD` — a **commit id**, the ADR 0050 (evidence is content, not history) forbidden class | `fitness-no-history-ids-in-evidence` (object-DB relative) |
| Current FINDINGS last-pass line | `Last pass (26-10-18): … Shipped git tag **v0.4.0**` — the prep `sed` **does not match**, so official prep is a no-op on that line | F1 phrase check |

Human docs say **`./release` only** (ADR 0039 — one human command surface). `./release prepare` is an internal/deprecated alias. Internally, prepare is `PREP` (`scripts/nlc-release-prep.sh` → `goals/hub_release_prep/execute.sh`: full `ci_fitness`, install-hash, smoke, stale FINDINGS sed) then `WRITE_RECORD` then `COMMIT`.

### 6.2 Why PR #31 did not use it

`cfe39da` (Cursor Agent, 2026-10-25): hand-edited `integrity/hub-release-record.json` 0.3.3→0.4.0, DESCRIBE and FINDINGS last-tagged-ship 0.3.3→0.4.0. Commit message: so the tag gate does not rewrite them **after** the owner signs. PR #31 body: if `./release` prepare wrote those at tag time, the manifest would change and need a **second** signature.

They chose agent edit + remanifest (`5c377a3`) + owner sidecar (`c9e8934`) over `WRITE_RECORD` / prep, because the signed-set + whole-tree digest (RCA 2026-10-25 signed-whole-tree-digest) makes a post-sign prepare write a new owner event.

`/release` skill step 1A also tells the agent to **hand-set** FINDINGS `last_pass_tree_hash` and commit. That is an authorized agent-edit path, not a script-in/script-out close.

### 6.3 How commit ids relate

The two tokens Richard’s history-ids check resolved (`d83c64a`, `a5287e2`) were **already in FINDINGS** from September wave narrative. `cfe39da` did not add them. The principle still applies: FINDINGS is a free-edit surface; nothing produces “the FINDINGS bytes the history-ids check must accept on every clone.” A developer clone with extra objects fails; GitHub without those objects passes. That is not a deterministic pass.

The official prep `sed`, if the old `Last pass: \`sha\`` line were still present, would **inject** a resolvable commit pin on every machine — a script that produces an ADR 0050 violation. Stale, but it shows prepare was never bound to “script output ⊆ allowed evidence.”

---

## 7. Upstream chain (process before output)

| Step | Artifact / layer | What it did |
| ---- | ---------------- | ----------- |
| (symptom A) | GitHub rewrite-invariant 37–54 min; fitness 18–22 min | Valid sidecar; 3× / 1× full suite including 311× derive |
| (symptom B) | Richard ci-fitness 3.6 s | History-ids resolves local-only SHAs in FINDINGS |
| (symptom C) | Richard drill 0.4 s | `--local` hardlink `EXDEV`; stderr swallowed |
| 6 | PR #31 finish line | Declared fitness / history-rewrite “still pass” at `5c377a3` (unsigned, exit 1, 4–6 min). Did not time CI or run the drill **with real owner sigs present**. Did not run `./release` `WRITE_RECORD` |
| 5 | ADR 0056 (per-file detached ADR signatures) + sidecar land | Required 56 live sigs + one manifest clearsign. No finish-line row: “CI wall-clock with those bytes present” |
| 4 | `is_gate_set_path` / hub-scope derive | Correct on a small `changed_paths` fixture; quadratic in “diff since v0.3.0” once the produce package is valid |
| 3 | History-rewrite job on every push/PR | Cheap while hub-ci-fitness fail-fasts; unbounded when the suite is green |
| 2 | History-ids = resolvable-in-this-clone | Same tree, two verdicts. No “pins must be unresolvable on a GitHub-empty object DB” fixture |
| 1 | Prepare / FINDINGS authorship | Record writer exists; last-tagged-ship has no writer; FINDINGS remains agent-edited; prep `sed` would write a commit id |
| 0 | Principle gap | A control that must **deterministically** pass (CI on every clone, rewrite drill on every laptop) was allowed to depend on object DB, `/tmp` filesystem, and agent-edited prose. Finish lines that do not **time** the green path cannot refuse a produce that is only cheap while red |

**Furthest controllable upstream point for A:** the finish line / control-design process (time the green path with live owner sigs; refuse a drill that is 3× the untimed suite).  
**For B:** the principle — prepare and FINDINGS bytes that CI must accept come only from a script; checks verify that output (and must not depend on extra local objects).  
**For C:** the drill’s clone flags and stderr (portability), independent of A.

---

## 8. Candidate roots (at most three per condition)

### A (wall-clock)

| Candidate | §3 bar | Verdict |
| --------- | ------ | ------- |
| “gpg / 56 sigs / pinentry” | Contradicted by timings | Reject |
| Cache `derive_gate_set_paths` / stop 311× `is_gate_set_path` | Fixes the inner loop; next finish line can still ship an untimed 3× suite | Product follow-up |
| Finish line must **time** fitness + run the drill with **real owner sigs present** before calling the line green | One process change; deterministic; earliest controllable | **Survives for A** |

### B (FINDINGS pins)

| Candidate | §3 bar | Verdict |
| --------- | ------ | ------- |
| Delete two SHAs from FINDINGS | Output-only; next agent edit reintroduces pins | Reject |
| History-ids should scan GitHub, not the clone | Detection tweak; still allows free-edit FINDINGS | Contributing |
| Prepare + FINDINGS bytes that must pass come only from a script; checks verify that output | Matches the stated principle; deterministic across clones | **Survives for B** |

### C (cross-device clone)

| Candidate | §3 bar | Verdict |
| --------- | ------ | ------- |
| Same as A | No evidence link | Reject |
| `--no-hardlinks` or scratch on the repo filesystem, and print git stderr | Deterministic; actionable; matches Richard’s stderr | **Survives for C** |

---

## 9. The one thing

**A:** The produce finish line for a signing / CI-gate change must include a **timed** `fitness` run and a **rewrite-invariant** run on a tree that already has the **live owner signatures**. Declaring the drill green on an unsigned tree (exit 1 == exit 1 in 4–6 min) is an incomplete finish line.

**Prevention test (A):** If **“time CI and run the drill with real owner sigs present”** had been a blocking finish-line row **before** `c9e8934` was called complete, **the 18–22 min fitness / 37–54 min rewrite** could not have been a surprise because **the produce would have been REFUSED until those measured runs existed.**

**B:** Anything that must deterministically pass (history-ids, tag-gate FINDINGS phrases, hub-release-record) must be **produced by a deterministic script**; checks verify that output. Agent hand-edit of prepare identity is not that script.

**Prevention test (B):** If **prepare edits came only from a script and history-ids/F1 verified that output** had been in force **before** FINDINGS became a free-edit ship surface, **Richard’s 3.6 s fail vs GitHub MET** could not have occurred because **the script would not emit resolvable commit pins and both clones would grade the same bytes the same way.**

**C:** The drill must not `clone --local` (hardlink) into `/tmp` across devices, and must surface git stderr.

**Prevention test (C):** If **`--no-hardlinks` or a same-filesystem scratch, plus un-captured stderr printed on failure** had been in the drill **before** Richard ran it, **exit 128 in 0.4 s with no reason** could not have occurred because **clone would copy instead of `link(2)`, or the `EXDEV` line would be on stdout.**

**Class:** A and B are process (finish line / prepare authorship). C is a product portability gap in the drill. A and C are **not** the same cause.

---

## 10. Contributing factors

- `run_profile` does not fail-fast; the **suite** does. Unsigned rewrite still runs three suites but each dies at gate-set-manifest (~2 min × 3 + filter-branch ≈ 4–6 min).
- Merge-base default is **v0.3.0**, so `changed_paths` grows with the line (311 today; more later) unless `is_gate_set_path` is cached.
- Parent CI logs buffer `---` labels; the 515 s handoff looks like a hang.
- `/release` step 1A authorizes agent FINDINGS edits.
- Official prep `sed` is stale against `Last pass (26-10-18):` and would write a commit SHA if the old line returned.
- C8 (no tracked tool writes `*.approval.asc`) is not the time sink. It forced the sidecar to arrive as a last human commit, which is when the suite turned green and expensive.

---

## 11. Remediation options (not done)

Expected times use: this VM’s 291 s × 2 ≈ 10 min extra; GitHub ~520 s × 2 ≈ 17 min extra; rest of suite ~2–5 min; filter-branch ~14 s; 3× for the drill.

### A1 — Cache `derive_gate_set_paths` per process / make `is_gate_set_path` a set lookup

**Expected:** fitness ~2–5 min (unsigned-path plus cheap landmines); rewrite ~6–15 min (3× suite + 14 s).  
**Tradeoff:** Correctness depends on not mutating the tree mid-derive. Small change.

### A2 — `validate_hub_material_package` must not run the 311-list through per-path derive

One `set(derive_gate_set_paths(root))`, then membership. Same expected times as A1.

### A3 — Drill runs only evidence-identity gates, not `hub-ci-fitness`

**Expected:** rewrite ~1–2 min (clone + filter-branch + cheap gates). Fitness job unchanged (~18–22 min until A1/A2).  
**Tradeoff:** Loses “full release profile invariant.” ADR 0050 (content, not history) only needs the gates that would flip on a rewrite.

### A4 — Move the drill to release-time on a self-hosted box (vhost11)

**Expected:** GitHub `rewrite-invariant` job **gone** (0 min on `ubuntu-latest`). Fitness stays 18–22 min until A1/A2. vhost11 drill: **37–54 min** if unfixed, **~6–15 min** after A1/A2, **~1–2 min** after A3. Put the scratch dir on the **repo filesystem** (see C1) so Richard’s `EXDEV` does not recur there.  
**Tradeoff:** PR CI no longer proves the invariant; a broken drill is found at ship. Matches “release-time step.”

### A5 — Timeout / schedule only (nightly or `release/v*` only)

**Expected:** PR wall-clock drops the 37–54 min job; defect remains on the scheduled run. Detection, not prevention.

### A6 — Status quo (wait 37–54 min)

The successful rerun shows it can finish. **Rejected** as remediation; recorded so “just wait” is not mistaken for a fix.

### B1 — Prepare edits come only from a script; checks verify its output *(required by the principle)*

**Product:** `WRITE_RECORD` is the only writer of `hub-release-record.json`. Add a writer for DESCRIBE/FINDINGS last-tagged-ship / shipped-tag phrases (or stop requiring those phrases). Fitness/tag-gate: **bytes equal script(`version`)**, not “agent edited until the regex matches.” History-ids: script output contains **no** resolvable commit tokens (delete wave-1/2 SHAs as part of the scripted surface, or move them under `docs/history/` which the scanner already skips). Remove or rewrite the prep `sed` that inserts `git rev-parse --short HEAD`.

**Expected:** Richard and GitHub get the **same** history-ids verdict. Prepare no longer needs a second owner sign **if** the script is the last writer before remanifest (the signed-whole-tree-digest RCA still applies).

**Why it was not used on PR #31:** last-tagged-ship has no writer; running `./release` `WRITE_RECORD` at tag time was believed to force a second sidecar; the agent wrote `cfe39da` instead.

### B2 — History-ids uses a throwaway object DB (or `--bare` empty) so only pins that are **blobs in the tree** cannot “become” commits

**Expected:** both clones MET on today’s FINDINGS (tokens do not exist as commits in an empty DB). Does not implement the principle; papers over free-edit FINDINGS.

### C1 — `--no-hardlinks` or scratch on the repo filesystem; print git stderr

**Expected:** Richard’s drill **starts** (then hits condition A’s 37–54 min, or A1–A3’s shorter time). GitHub unchanged.  
**Not** a fix for the hang.

### Shared process row

CONTROL-LIFECYCLE / briefing / PR finish line: **time the green path** with live owner sigs; **prepare identity is script-out**. Without that row, A1–A4 and B1 can be skipped the next time a sidecar turns a cheap fail-fast into a 20-minute suite.

---

## 12. Preventive action (single tracked item — not done)

| Field | Value |
| ----- | ----- |
| Action | Bind the finish-line row (time fitness + rewrite drill with live owner sigs) and the prepare-script row (writers for record + last-tagged-ship; checks verify output; no commit pins). Then pick A1 or A2 for the 311× derive, C1 for `--local`/`EXDEV`, and optionally A4 (vhost11) so GHA does not run the 3× suite. |
| Owner | hub |
| Path / artifact | `tools/nouns/gate_set/gate_set.py`, `hub_own_produce.py`, `assert_history_rewrite_invariant_passes.py`, `goals/hub_release/execute.sh`, `goals/hub_release_prep/execute.sh`, FINDINGS/DESCRIBE writers, CONTROL-LIFECYCLE / `/release` 1A |
| Verification | On a tree with the live sidecar: `fitness-hub-scope-derived` and `preflight_handoff` each < 5 s; `ci-fitness.sh` MET on a clone **without** `d83c64a`/`a5287e2` **and** on a clone that has extra objects; drill clone into a `/tmp` on another filesystem exits 0 or prints `EXDEV`; unsigned tree still fail-fasts at gate-set-manifest |
| Belief / gate touch (ADR 0025) | Unsuitable process: finish line that treats fail-fast-red as “rewrite passed”; prepare identity by agent edit. Touches hub-scope derive, drill clone, prepare writers |

---

## 13. Follow-up (detection only)

- Job 121294648287 (PR rewrite rerun) may still be running; treat 37 min SUCCESS on 40230451697 as the completed specimen, 54 min cancel as the “hang” specimen.
- Do not “fix” FINDINGS by deleting two SHAs in this PR. That is condition B’s output-only reject.
- Do not sign anything in this produce (C8).

RCA only. No remediation commit.
