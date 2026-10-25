# RCA: Unregistered Planit skill edit landed on `release/v0.4.0` with no PR

**Date:** 2026-10-25  
**Context:** Natural-Language-Coding hub — 0.4.0 prepare line  
**Status:** open (RCA only; no remediation in this record)

**Scope (user words):**

- “RCA ONLY. Do NOT change any code, skills, registries, manifests, or branches.”
- “Incident: commit d4b4648 … was pushed directly to release/v0.4.0 with no PR.”
- “It edited `.agents/skills/planit/SKILL.md` … but `integrity/planit-skill-registry.json` still says 85a11ef6….”
- “`python3 tools/fitness-planit-identity.py --skill-only --loaded .agents/skills/planit/SKILL.md` gives `PLANIT_IDENTITY:NOT_MET`, and the owner's local hook now denies work.”
- “Next, da90b90 regenerated the gate-set manifest, which is now unsigned.”
- “first name the defective product, then the process that produced it, and climb until you reach a root that, if fixed, would have prevented this whole class.”
- “How could this condition be created where we made a mandate for a signature and still allowed the skill edits to treat it as optional? What created that condition?”
- “Climb one level above the current root: find what CREATED the condition that signature/identity pins are optional later steps for skill produce.”
- “RCA ONLY, no remediation changes.”
- “What causes will be left in place after this RCA remediation that can cause this again? It seems if something intentionally edits /planit we won't ever be able to sign it - because it will come to me waiting for the signature, ending its turn. Then I sign and give it to the agent, which uses /planit to handle the signature I gave it and fails because /planit is not signed.”
- “I think we'll need to have a 'staging' area for new skills - so it can build a new /planit there, I can sign it, and after I sign it, the new version and the signature are put in place all at the same time.”
- “We're still remediating this error mode. I'm wanting to know what failed to realize this error mode was possible when this signing was set up.”
- “This is about the DESIGN process, not the mechanism.”
- “Add a 'Climb 4' section” reconstructing how signing was designed and which process step failed to surface the error mode.

---

## 1. Error condition

**Observed (bounded, reproducible):**

- `origin/release/v0.4.0` tip is `da90b909cb6470d8b2ff97b85778016985a63efc` (parent `d4b46487fe7319d209c9366d829f81ca3716d73c`). Neither commit is a merge. GitHub `GET /commits/{sha}/pulls` returns `[]` for both.
- `d4b4648` (Cursor Agent, 2026-10-25 00:50:16 UTC): “Repair published skills so the live author check is MET.” Touches 30 files, including `.agents/skills/planit/SKILL.md` and ten other published `SKILL.md` files. Does **not** touch `integrity/planit-skill-registry.json` or `integrity/nlc-install-hashes.json`.
- Current Planit bytes: `sha256 0e0493b4c0c95e56c53501d1a4d794ed7b699cc9cc5ad715c92709626f845d9f` (`.agents/skills/planit/SKILL.md`). Parent `ae6dcb6` of the repair still hashed `85a11ef6ce5037d3a4e0c54d074679598a19e347f4e1f80778d4f2f1ad15085e`.
- Registry still records that parent hash (`integrity/planit-skill-registry.json` line 4).
- Reproduction (this tree): `python3 tools/fitness-planit-identity.py --skill-only --loaded .agents/skills/planit/SKILL.md` → `VIOLATION loaded Planit skill hash does not match the registry` / `PLANIT_IDENTITY:NOT_MET` (exit 1).
- Cursor hook `.cursor/hooks/nlc-planit-identity.sh` (wired on `beforeSubmitPrompt` in `.cursor/hooks.json`) denies the prompt when that command is non-zero. That is the owner-local deny.
- `da90b90` (00:50:51 UTC): “Regenerate the unsigned gate-set manifest after the skill repair.” Only `integrity/gate-set-baseline.manifest.sha256` changes. `python3 tools/fitness-gate-set-manifest.py` → `VIOLATION … Content-SHA256 mismatch (statement 8ffa1481… vs file 1f3a82e5…)` / `RESULT:NOT_MET`.

**Not the error condition:** the YAML `name:` / in-skill-link repair itself. `python3 tools/nlc-skill-author-check.py --root .agents/skills` is `SKILL_AUTHOR:MET` after `d4b4648`. That is the gate the produce ran.

---

## 2. Defective product, then the process (climb)

| Layer | What it is | Evidence |
| ----- | ---------- | -------- |
| **(symptom) product** | Planit skill bytes on `release/v0.4.0` no longer match the identity pin; install fingerprints for nine published skills are stale; gate-set sidecar is unsigned | `PLANIT_IDENTITY:NOT_MET`; `INSTALL_VERIFY:NOT_MET` (nine paths); `fitness-gate-set-manifest` Content-SHA256 mismatch |
| **5. Landing** | Those commits updated `origin/release/v0.4.0` with no PR | `git cat-file -p d4b4648` has one parent; GitHub pulls API `[]`; branch `protected: false` |
| **4. Produce session** | Cloud run `bc-298e948a-5bf8-520b-84f0-5adf8e09ff99` executed walkthrough step 5, proved `SKILL_AUTHOR:MET`, pushed the release line, then regenerated an unsigned manifest | Transcript (00:50 UTC); commit messages; handoff: “did not bump identity” |
| **3. Walkthrough / type recipe** | Step 5’s machine finish line is the author checklist only. Skill type recipe has no identity or install-hash pin. “Refresh Planit identity if `planit/SKILL.md` bytes change” was unbound prose | Transcript step list; `content-types/HOW-TO-ADD.md` Skill section; ADR 0054 |
| **2. Pin design** | Identity registry is a hand-kept pin (ADR 0046) with no generator. Install hashes and gate-set manifests **are** generated, but Skill produce does not require those generators. Identity hook fires on local prompt-submit, not on commit/push | `integrity/planit-skill-registry.json`; `tools/nlc-install-hash-update.py`; `tools/generate-gate-set-baseline-manifest.py`; `.cursor/hooks.json` |
| **1. Host + brief** | `release/v*` is the working ship line (ADR 0044). GitHub has no ruleset and no protection on that branch. `RELEASE.md` recommends PR+CI only for `main`. Cloud briefing says “create a feature branch + PR”; `/release` and the walkthrough say commit on `release/v*` and defer the one PR to `./release` | Branch API; `docs/adoption/RELEASE.md`; `.agents/skills/release/SKILL.md`; transcript 256229 |

**Furthest controllable upstream point:** published-skill **produce** is not an atomic pin update, and the release line will accept a partial produce. Fixing only the current `SKILL.md` hash, or only the hook message, recreates the class the next time a walkthrough names one checklist as done.

---

## 3. Impact / scope

- Owner-local Planit intake is denied (`beforeSubmitPrompt` fail-closed) on any checkout of this tip.
- Hub `verify` profile is red: `planit-skill-identity` failed on both `d4b4648` and `da90b90` (GitHub Actions fitness runs `40148249783` and `40148286806`).
- Piped install on the same runs is `INSTALL_VERIFY:NOT_MET` (fingerprint list) / skill-author import failure on Windows (missing `yaml`) — separate contributing failure.
- Gate-set member bytes were regenerated without owner ratification. The produce named that as expected until a later sign step.
- `release/v0.4.0` is the 0.4.0 prepare line. These commits are on the line that `./release` would offer as the ship PR to `main`.

---

## 4. Timeline (brief)

| Time (UTC) | Event |
| ---------- | ----- |
| 2026-09-16 | ADR 0010 accepted: never pass generated output downstream before its gate |
| 2026-10-08 | ADR 0046: `integrity/planit-skill-registry.json` pins Planit path + SHA-256; Cursor hook on prompt-submit |
| 2026-10-11 | Registry last content change in history: `5bd6113` (O6). No generator exists |
| 2026-10-20 | RCA: skill YAML load errors. Repair of live skills is a later tracked row |
| 2026-10-20 | PR #26 (draft, base `main`): “Does **not** rewrite current hub skills (repair is a tracked TODO)” |
| 2026-10-24 19:38–00:46 | Direct pushes to `release/v0.4.0` (no PR from `ca001b9` onward). Fitness already failing on this line |
| 2026-10-24 ~session | Operator: “List the steps…”; agent emits 10-step 0.4.0 walkthrough. Step 5 = repair + “Refresh Planit identity if `planit/SKILL.md` bytes change.” Step 8 = owner sidecar last. Step 10 = one PR via `./release` |
| 2026-10-24 | Operator: “Let's walk through each one… Let's start now” |
| 2026-10-25 00:49 | Operator: “ok, what's next, go ahead and do it.” Agent maps that to step 5 |
| 2026-10-25 00:50:16 | `d4b4648` on `release/v0.4.0`; push `git push -u origin release/v0.4.0` (no PR). TODO row `@done(26-10-24 19:49)` |
| 2026-10-25 00:50:21 | Fitness workflow `40148249783` starts **after** the push; `FAILED planit-skill-identity` / `PLANIT_IDENTITY:NOT_MET` |
| 2026-10-25 00:50:51 | `da90b90` unsigned manifest regenerate; second push |
| 2026-10-25 00:50:54 | Fitness `40148286806`: same identity fail + pipeline-blockers (before-generate stamp) |

---

## 5. Mechanism on reproduction

**Confirmed (product):** parent Planit hash `85a11ef6…` equals the registry; tip Planit hash `0e0493b4…` does not. `prove()` in `tools/nouns/planit_identity/planit_identity.py` compares loaded bytes to `content_sha256` and returns the violation used by the hook and by `planit-skill-identity`.

**Confirmed (CI after land):** fitness.yml `on: push` ran `bash tools/ci-fitness.sh` → `ci_fitness.py` `main()` with `include_releasable_verify=True`. Verify profile includes `planit-skill-identity`. Both incident SHAs failed that gate in <10s. The job cannot refuse a push that already succeeded.

**Confirmed (process):** transcript of `bc-298e948a` at 00:50 UTC: agent notes no PR exists, walkthrough defers the ship PR to `./release`, cloud briefing wants a PR, walkthrough wins; `git push origin release/v0.4.0`. Handoff: “did not bump identity… Regenerated the unsigned gate-set… owner ratification stays the later sign step.” Verified list is `SKILL_AUTHOR:MET` plus author-checklist fitness; identity is absent.

**Confirmed (host):** `GET /repos/Zygotic-AI/Natural-Language-Coding/branches/release/v0.4.0` → `"protected": false`, `"protection": {"enabled": false, "required_status_checks": {"enforcement_level": "off", "contexts": [], "checks": []}}`. `GET …/rulesets` → `[]`. Detailed `…/protection` and org rulesets return 403 to this integration; the branch object is enough to show this ref is not protected.

---

## 6. The five questions

### Q1. Why could an agent push straight to `release/v0.4.0` with no PR?

**Host:** GitHub does not protect that ref. Repo rulesets are empty. Required status checks are off. A fast-forward `git push origin release/v0.4.0` is accepted. Contrast: `docs/adoption/RELEASE.md` lines 71–74 recommend PR + required CI **for `main` only**, and do not require a PR to update `release/v*`.

**Brief (hub):** ADR 0044 decision 1: unreleased work lives on `release/v*`. `/release` skill lines 64 and 74: prepare commits go on the release line branch, never `main`; the one PR is `release/v*` → `main` via `./release`. The 0.4.0 walkthrough step 2 restated that: “Feature branches aimed at `main` are not the ship.”

**Brief (cloud harness):** this class of run is also told to create a feature branch and open a PR per branch. The producing session recorded the conflict and chose the hub walkthrough (`transcript.json` thinking at the first push: “Cloud instructions suggest creating a PR instead. The user's locked walkthrough takes priority.”).

**Pattern:** from `ca001b9` through `da90b90`, GitHub `commits/{sha}/pulls` is `0`. Direct push to the release line is the in-force landing path, not a one-off.

### Q2. Why did no check run **before** that push catch the registry mismatch?

| Check | When it runs | Did it catch this? |
| ----- | ------------- | ------------------ |
| `.cursor/hooks/nlc-planit-identity.sh` | Cursor `beforeSubmitPrompt` on a local checkout | After the fact, on the owner's machine. Not installed as a git hook. Cloud commit/push does not run it |
| Repo git hooks | `pre-commit` / `pre-push` | Only `*.sample` files under `.git/hooks`. `core.hooksPath` is the cloud agent-hooks dir, not a repo fitness path. No pre-push identity check ran |
| `planit-skill-identity` in releasable verify | First block of `python3 tools/ci_fitness.py` (`include_releasable_verify=True`, `integrity/releasable-gates.json` lines 6–8 and 80–92) | **Yes, after the push.** Run `40148249783` job `fitness` at 00:50:26 UTC: `FAILED planit-skill-identity` / `PLANIT_IDENTITY:NOT_MET` / `CI:FAIL releasable verify profile`. Same on `da90b90` |
| `fitness.yml` `on: push` | After GitHub accepts the ref update | Ran; failed; could not un-land the commits because the branch does not require the check |
| Skill author check | What the produce actually ran | `SKILL_AUTHOR:MET` — different pin |

The check that should have caught the mismatch is `planit-skill-identity` (ADR 0046 binder in `integrity/adr-gates.json` line 185). It ran in CI and is the same command as the owner hook. It is not a pre-push gate. Fitness on this line was already failing before `d4b4648` (runs on `ca001b9`, `bcb2f95`, `4f3caf2`, `15c9bb0`, `ae6dcb6`), so a red status check was not treated as a stop.

### Q3. Why does editing a skill not require or produce a registry update? Derived or hand-kept?

**Three pins, three update stories:**

| Pin | Kind | Updater | Bound to Skill type? |
| --- | ---- | ------- | -------------------- |
| `integrity/planit-skill-registry.json` | Hand-kept identity pin (path + `content_sha256`) | **None.** Last history change `5bd6113`. ADR 0046 stores the hash; nothing regenerates it | No. Skill recipe gate is only `frontmatter-yaml` + `in-skill-links` (`content-types/HOW-TO-ADD.md` lines 296–328; ADR 0054 decisions 1–3) |
| `integrity/nlc-install-hashes.json` | Derived install fingerprint list (includes every `.agents/skills/**/SKILL.md`) | `python3 tools/nlc-install-hash-update.py` (`tools/nouns/install_hash_update/install_hash_update.py` lines 55–57 walk `SKILL.md`) | No. Repair did not run it |
| `integrity/gate-set-baseline.manifest.sha256` | Derived member digest list; ratification is the OpenPGP sidecar | `python3 tools/generate-gate-set-baseline-manifest.py` (header: “no ratification”) | Partial: the session **did** regenerate members (`da90b90`) and **explicitly** left the sidecar unsigned until walkthrough step 8 |

The identity registry is **hand-kept**. It is not a derived artifact today. The install-hash file **is** derived and should have been regenerated in the same change; the Skill type does not say so. Editing a skill to pass `SKILL_AUTHOR` is a complete Skill-type produce. ADR 0046 identity is a **load-time** refuse for Planit intake, not a **produce-time** refuse on `SKILL.md` writes.

### Q4. Who asked for the repair, and was it under an owner-approved plan?

**Asked by the operator**, inside a locked 0.4.0 walkthrough, not by a new `/planit` at repair time.

| Layer | Wording | Where |
| ----- | ------- | ----- |
| Program | Bind the checklist as law; use Planit for the plan; repair is a tracked TODO, not prompt-only law | Transcript `bc-298e948a` (user, earlier in the same run); PR #26 body: “Does **not** rewrite current hub skills (repair is a tracked TODO)” |
| Plan | Walkthrough step 5: repair so `SKILL_AUTHOR:MET`; also “Refresh Planit identity if `planit/SKILL.md` bytes change” | Transcript assistant text listing steps 1–10 |
| Lock | “Let's walk through each one. You guide. … Let's start now” | Transcript user |
| Execute | “ok, what's next, go ahead and do it” | Transcript user, immediately before step 5 |
| Record | TODO: “Repair current published skills so … `SKILL_AUTHOR:MET`” `@done(26-10-24 19:49)` | `TODO` line 678, committed in `d4b4648` |
| RCA follow-up | 2026-10-20 record updated in the same commit to say live skills were repaired | `docs/rca/2026-10-20-skill-yaml-terms-link-load-error.md` in `d4b4648` |

**Owner-approved:** executing the repair so the live author check is MET, on the 0.4.0 line, yes — that is the TODO + walkthrough step 5 + “go ahead.”  
**Not approved as a complete produce:** landing unregistered bytes. Step 5’s own prose required a Planit identity refresh when those bytes changed. The session treated `SKILL_AUTHOR:MET` as sufficient and wrote “did not bump identity.” No GitHub issue asked for a no-PR push. No PR on this branch reviewed `d4b4648`.

ADR 0025: this is not “the agent skipped a sentence.” The Skill type and ADR 0054 make `SKILL_AUTHOR` the only bound gate for that edit, so unbound prose (“refresh identity”) cannot refuse the handoff.

### Q5. Full list of files whose registered hash no longer matches

Derived with repo tools on this tip (`da90b90`), not guessed.

**A. Identity pin** — `python3 tools/fitness-planit-identity.py --skill-only --loaded .agents/skills/planit/SKILL.md`

| File | Registered (`planit-skill-registry.json`) | Actual |
| ---- | ----------------------------------------- | ------ |
| `.agents/skills/planit/SKILL.md` | `85a11ef6ce5037d3a4e0c54d074679598a19e347f4e1f80778d4f2f1ad15085e` | `0e0493b4c0c95e56c53501d1a4d794ed7b699cc9cc5ad715c92709626f845d9f` |

`.cursor/skills` is a symlink to `../.agents/skills` (same bytes, not a second registered path).

**B. Install fingerprints** — `python3 tools/nlc-install-verify.py` → `INSTALL_VERIFY:NOT_MET` (nine mismatches). Registered values from `integrity/nlc-install-hashes.json`:

| File | Registered | Actual |
| ---- | ---------- | ------ |
| `.agents/skills/bbp-confirmer/SKILL.md` | `4cf9a5009d5a92e9425ac9e4e987c243e85625e728e8419efd3005224a179ef4` | `6ed5bc11a3e3475d6d626f35259331251ad199152afdb8d598c66c3c9a1c8554` |
| `.agents/skills/bbp-proposer/SKILL.md` | `f3f9d588e7801fab70987c4b3afcbba19f52ea91efb6e173b5ffd2edee333352` | `4c2d40a2cbc33365c75680630920beb3d1afea321e6b13c6e408514e7539d029` |
| `.agents/skills/bbp-recorder/SKILL.md` | `7ee8659d50003bfe3f421ec1bd77b85f34cf2d3cae48a0ae5d753a5d27c79bb4` | `87f5ea131682e03eee71f706111ad24521cfab0db6946b0920a40d782b0330e1` |
| `.agents/skills/bbp-reviewer/SKILL.md` | `7c0c3e265bc52d28e3fea9a8fb02a735bf75cf17fb58ba42fcc414b47225ea5a` | `24ed5101dfdec2080d6a789aa533af17eaca1937e8066e24ad05725ac7db1655` |
| `.agents/skills/full-nlc-audit/SKILL.md` | `ad3f63966d69e7b4609a5370f62ac28210f6b8881ac3c444d2c04b23f63fcefc` | `5dcd8e90f2e08eec8493a705e5ccf02cd4f1a1a528c411f2a5d89c4c45a03866` |
| `.agents/skills/interview/SKILL.md` | `1d7a8861e476d1220bcb1144985a77266a7b914d6688a7c9ade59f97e0496e58` | `73ea432dc2492048e9df5835aab98ca5785a6cd961cb96d61765695df492c403` |
| `.agents/skills/planit/SKILL.md` | `85a11ef6ce5037d3a4e0c54d074679598a19e347f4e1f80778d4f2f1ad15085e` | `0e0493b4c0c95e56c53501d1a4d794ed7b699cc9cc5ad715c92709626f845d9f` |
| `.agents/skills/release/SKILL.md` | `a83161f30b2d6e37f21e7a8ac02f25fde8ec349b491e98621d415b5e2db03331` | `da71736d62912baee10bf3d068e0b26c494435d2418fffa83e55e2708fe72662` |
| `.agents/skills/verify/SKILL.md` | `70b0604fef757f4194892288cec4acdf00b91cd30ffc2b4f048388c7b1a73831` | `4164ff20b6966bb08a5d0f5385092d90abdc36e5498d77b92001a58cf4a52fee` |

Still matching in that manifest (not edited in `d4b4648`): `.agents/skills/nlc-hub-audit/SKILL.md`, `.agents/skills/requirement-pack-ingest/SKILL.md`.

**C. Gate-set sidecar (not a skill-file hash):** member lines were rewritten to the current tree in `da90b90`. The **signed statement** still names Content-SHA256 `8ffa1481…` vs file `1f3a82e5…`. That is an unsigned regenerate, not a ninth skill mismatch.

---

## 7. Candidate roots (at most three)

| Candidate | §3 bar | Verdict |
| --------- | ------ | ------- |
| Update `planit-skill-registry.json` (and install hashes) to `0e0493b4…` | Output-only; next skill repair repeats | Reject |
| Add a pre-push script | Detection; cloud/agent-hooks can skip repo hooks; unsigned gate-set and no-PR landing remain | Too low |
| Published-skill produce is one checklist; other pins and PR landing are later optional steps; `release/v*` accepts the partial produce | One process; deterministic; earliest controllable; in-repo (Skill type / ADR 0010 bind + host ruleset as the landing half of the same produce contract) | **Survives** |

---

## 8. The one thing

> What **one** deterministic, actionable thing, if it were different, would have **prevented this error condition from arising**?

**Answer:** Published-skill produce must be default-closed on every pin that names those bytes, and that produce must not be able to update `origin/release/v*` until those pins are consistent. A skill edit is incomplete unless the identity registry (when the path is registered), the install-hash list (derived), and gate-set ratification (when the path is a member) are updated or the change is refused in the same produce — and the host refuses a direct push of a partial produce onto the release line.

That is the process that produced an unregistered Planit skill, nine stale install fingerprints, an unsigned gate-set, and a no-PR release-line land as one class.

---

## 9. Prevention test

> If **Skill produce had refused MET unless every hash pin that names the edited `SKILL.md` bytes was updated in the same change, and `release/v*` had refused non-PR pushes unless fitness (already including `planit-skill-identity`) was green,** had been in place **before** walkthrough step 5, **`d4b4648` updating `origin/release/v0.4.0` with Planit bytes `0e0493b4…` while the registry still said `85a11ef6…`** could not have occurred because **the Skill-type gate would refuse the produce without the pin updates, and GitHub would refuse the ref update without a PR whose required fitness job already fails `PLANIT_IDENTITY`.**

**Completed:** yes (mechanism: produce-time pin coupling + host landing refuse; the owner hook is how the same identity command is seen locally after the land).

---

## 10. Contributing factors (optional)

- Walkthrough step 5 mentioned “Refresh Planit identity” as prose; ADR 0054 / Skill recipe do not bind that sentence, so `SKILL_AUTHOR:MET` closed the step.
- Walkthrough step 8 **intends** an unsigned gate-set until the owner signs last — so `da90b90` is consistent with that split, and is part of the same class (partial produce on the release line).
- ADR 0046 hook is `beforeSubmitPrompt`, not `pre-commit` / `pre-push`.
- Cloud “open a PR” briefing conflicts with ADR 0044 / `/release` “commit on `release/v*`”; the session resolved toward the hub brief.
- Fitness on `release/v0.4.0` was already red, so a new red identity fail was not a novel stop signal.
- `.nlc/planit-change-evidence.json` still records `85a11ef6…` (stale evidence; not the registry).

---

## 11. Preventive action (not done in this record)

RCA only. No remediation commit.

| Field | Value |
| ----- | ----- |
| Action | Track one produce-contract change: Skill type + handoff refuse unless all pins that name the edited skill bytes are updated in the same change; add a GitHub ruleset that forbids direct pushes to `release/*` and requires the fitness job |
| Owner | hub (human manager) |
| Path / artifact | `content-types/HOW-TO-ADD.md` Skill gate table; `integrity/skill-author-checklist.json` (or a bound identity/install-hash check id); GitHub ruleset on `release/v*`; ADR 0010 / 0046 / 0054 binders |
| Verification | A landmine that edits `.agents/skills/planit/SKILL.md` without touching `planit-skill-registry.json` is `PLANIT_IDENTITY:NOT_MET` **and** Contribution Gate refuse; `git push` to `release/v*` without a PR is rejected by GitHub |
| Belief / gate touch (ADR 0025) | Unsuitable process: generate-then-one-checklist. Touches ADR 0010 (gate after every generate), ADR 0046 (identity pin), ADR 0054 (Skill author contract), Skill type recipe, `planit-skill-identity` / install-verify / gate-set-manifest, and the `release/v*` landing rule in `RELEASE.md` |

---

## 12. Follow-up (candidates only — do not implement here)

**Class this root covers:** any produce that mutates a pinned published artifact (skill, install fingerprint, gate-set member) can satisfy one named gate, skip the other pins, and update `origin/release/v*` without a PR.

| # | Candidate | Prevents | Does not prevent |
| - | --------- | -------- | ---------------- |
| 1 | Bind Skill produce: refuse MET unless every pin that names those `SKILL.md` bytes is updated in the same change (identity registry when registered; run `nlc-install-hash-update.py` for published skills; do not land an unsigned gate-set regenerate as “done”) | Unregistered skill edits; stale install fingerprints; treating `SKILL_AUTHOR` as a complete produce | A determined direct push of a *complete* pin update onto `release/v*` with no PR |
| 2 | GitHub ruleset: no direct push to `release/*`; required check = `fitness` (already fails `planit-skill-identity`) | Unreviewed landing; this exact no-PR push | Local unregistered edits until someone opens a PR; walkthroughs that still split pins across commits |
| 3 | Repo `pre-push` running identity + install-verify + gate-set-manifest | A hook-respecting push of mismatched pins | Cloud/agent-hooks that are not this script; hook bypass; host still accepts the ref if hooks are absent |

**Recommend (1), with (2) as the landing half of the same produce contract.** (1) is the earliest controllable refuse (ADR 0010 / Skill type). (2) is what makes the already-failing CI job actually stop `origin/release/v*` from moving. (3) is detection-only and is how the owner hook already behaves — after the land.

---

## 13. The root (one sentence) — Climb 1 (superseded)

Published-skill produce is allowed to treat a single author checklist as the finish line and land those bytes on an unprotected release line, while identity pins, install fingerprints, and owner-signed gate-set remain optional later steps.

Climb 1 names the **condition**. Climb 2 asks what **created** that condition (owner, 2026-10-25): “How could this condition be created where we made a mandate for a signature and still allowed the skill edits to treat it as optional? What created that condition?”

---

## 14. Climb 2 — what created “pins are optional later steps”

**Scope (user words):** “RCA ONLY, no remediation changes.” “Climb one level above the current root: find what CREATED the condition that signature/identity pins are optional later steps for skill produce.” Four evidence questions as numbered in the request.

**Climb 1 root (too low):** the Skill produce finish line is one author checklist; identity, install fingerprints, and owner-signed gate-set are later optional steps; `release/v*` accepts the partial produce.

**This climb’s error condition:** a signature/identity **mandate** exists, and Skill produce is still allowed to treat that mandate as optional.

---

### Q1. How were the owner-signature mandates expressed?

**After-the-fact checks that report red on the result tree.** Policy text sometimes says “before merge” / “handoff REFUSE,” but the compiled form is a fitness/verify detector. None of these mandates is a precondition on Skill produce or on landing to `release/v*`.

| Mandate | Date / SHA | What the text says | What was wired |
| ------- | ---------- | ------------------ | -------------- |
| **ADR 0051** SG2 (hub-own produce — gate-set bytes need owner receipt) | 2026-10-11 `f0a0216` | **P-GATE-SET-RATIFY:** “content hash change requires human manager receipt **before merge**.” **R-GATE-SET-NO-SILENT-WEAKEN:** a produce package that changes member bytes without a receipt is “incomplete (**handoff REFUSE**).” Same row’s **codified constraint** is already a detector: “(to implement) `fitness-gate-change-receipt` … **NOT_MET** when diff touches gate-set paths.” **Decision 5:** “Implementation of codified constraints is follow-on work; this Proposed record **does not wire CI**.” | Follow-on wiring `d79e03b` (2026-10-13) + **ADR 0053** (text retrofit, Proposed 2026-10-13): in-force check is `fitness-gate-set-manifest` on the tree. **ADR 0053** item 2: the receipt filename is stale; SSOT is `integrity/gate-set-baseline.manifest.sha256` plus its OpenPGP sidecar |
| **ADR 0052** (owner OpenPGP ratification — amends 0051) | 2026-10-11 `cd384ea` (signed `#15`) | Context: “Agents commit pasted armor **unchanged**; they **never create ratification**.” Decision 4: “**Stamp / fitness (completion confirmation only)** … Unsigned, wrong key, hash mismatch, tampered manifest, or **pending** → **NOT_MET**. **No tool may write a ratified entry.**” Consequences: “Until step 2 lands, **no CI check enforces this**; the PM holds the merge.” | Same wiring: `fitness-adr-owner-sidecar` (C6) and `fitness-gate-set-manifest`. C6 in `.nlc/produce-package.json` at `d79e03b` is already **`exit_status`: `REFUSE`**, and `ssot_exit_status` is “owner ratification of legacy ADR sidecars and the **unsigned** gate-set manifest is **outstanding**.” Produce is allowed to finish with signing unfinished |
| **Gate-set sidecar** | Generator `1bce2eb` (2026-10-12) | `tools/generate-gate-set-baseline-manifest.py` header: “Regenerate … from gate-set paths **(no ratification)**.” | A legal produce step writes an unsigned member list. The sidecar check then paints the tree red. Regenerating unsigned is a named ship step (`1ee783d` 2026-10-21 “Regenerate **unsigned** gate-set manifest…”) |
| **ADR 0046** Planit identity registry | 2026-10-08; still **Proposed** / “Pending a redraft” (`9e3e442` 2026-10-13) | Decision 3: “**Intake fails** when the loaded path or the loaded bytes do not match the registry.” Decision 5: Cursor `beforeSubmitPrompt` hook; other harnesses run `fitness-planit-identity.py --skill-only`. | `integrity/adr-gates.json` binder **0046** → `tools/fitness-planit-identity.py`. `integrity/releasable-gates.json` puts `planit-skill-identity` on the **verify** profile (runs after the tree exists). Not a produce-time refuse on `SKILL.md` writes |

**Quoted design of “red, not refuse produce”:**

- **ADR 0051** Decision 5 (line 105): “this Proposed record does not wire CI.”
- **ADR 0052** Decision 4 (line 50): “Stamp / fitness (completion confirmation only).”
- **ADR 0052** line 40: “Until step 2 lands, no CI check enforces this.”
- Hub produce package (`d79e03b`, unchanged at this tip): C6 **REFUSE** + “unsigned gate-set manifest is outstanding.”
- C8 (`tools/nouns/fitness_no_tool_writes_ratification/fitness_no_tool_writes_ratification.py` line 1): “no tracked tool writes `*.approval.asc`.” A producer **cannot** complete the signature.

Published `SKILL.md` files **are** gate-set members today (`integrity/gate-set-baseline.manifest.sha256` lines 11–20 include `.agents/skills/planit/SKILL.md` and the other published skills). **ADR 0053** item 1: membership is **derived** by `derive_gate_set_paths` from CI workflow seeds — not a hand-kept Skill-type list. So the signature mandate covers skill bytes as members, but only through the same after-the-fact manifest+sidecar detector. `d4b4648` already rewrote the **unsigned** manifest in the skill-repair commit; `da90b90` did it again. That is the mandate’s designed produce path, not a miss.

---

### Q2. Were the Skill recipe, the skill-author checklist, and `/release` derived from those mandates?

**Authored separately.** No import, no derived list, no reference to **ADR 0051**, **ADR 0052**, the gate-set sidecar, or the Planit identity registry. Each produce recipe must restate those mandates by hand — and none of them did.

| Produce surface | When / SHA | What it binds | Mentions 0051 / 0052 / 0046 / sidecar / identity registry? |
| --------------- | ---------- | ------------- | ---------------------------------------------------------- |
| `integrity/skill-author-checklist.json` | 2026-10-21 `11a904c` | `frontmatter-yaml`, `in-skill-links` only. Commit body: “Same checklist SSOT (**frontmatter YAML plus in-skill links**).” | No |
| **ADR 0054** (published-skill author contract) | 2026-10-24 `bcb2f95`; Accepted `15c9bb0` | “**Checks now (discovered problems):** `frontmatter-yaml` … `in-skill-links`.” Context: “This record does **not** add Skill as a content type. … This record does **not** repair current hub skills.” Rejected: adding Skill as a type; repairing live skills | No. Rationale is **RCA 2026-10-20** (YAML `name:` / dead install links), not hub-own produce or identity |
| Skill type recipe (`content-types/HOW-TO-ADD.md`) | 2026-10-25 `4f3caf2` “Add Skill as a content type **pointed at the author checklist**” | Gate table = that checklist. Steps 1–6 end at `nlc-skill-author-check.py` + Contribution Gate CG-R2/CG-R3 | No. `git grep` of `approval.asc`, `sidecar`, `0052`, `gate-set` in `HOW-TO-ADD.md` is empty. The **ADR** type recipe (same file, lines 69–78) also has no sidecar row |
| `fitness-skill-content-type.py` | same `4f3caf2` | Module docstring: “recipe gate is the published-skill author checklist.” The binder **requires** the recipe to name `nlc-skill-author-check.py` and `skill-author-checklist.json` | Locks the separate checklist. Does not require identity or signing |
| `/release` skill | last material identity work `605cd17` (2026-10-10, **ADR 0050**) before the 0051/0052 wave; later edits are current-ship prose and the `d4b4648` YAML repair | Closeout = `ci_fitness.py` CI:MET, FINDINGS tree hash, inference record. Ship prove is a later phase | `git grep` of `0051`, `0052`, `0046`, `planit-skill-registry`, `gate-set-baseline`, `approval.asc` in `.agents/skills/release/SKILL.md` is empty |

**Contrast — what *is* derived from 0051/0052:** `integrity/adr-0051-0052-rules.json` must equal `tools/derive-adr-0051-0052-rules.py`; `integrity/adr-gates.json` maps those ADRs to **fitness** tools. That derivation feeds **detectors**, not type recipes.

**ADR 0010** (2026-09-16, gate immediately after every generate) says skills “inherit this rule.” Inheritance here means “run **that artifact’s** gate.” The Skill artifact’s gate was later defined as the two-item author checklist. **PLANIT-ORCHESTRATION** X6 is “gates of ADRs **bound to this action**” (per-action), not “gates of every mandate that names a touched path.” **GATE-STD** is “every touched path has a default-closed gate or N/A” — and the Skill path’s named gate is `SKILL_AUTHOR`.

The 0.4.0 TODO repair row restates the split in operator words: “Repair current published skills so … is `SKILL_AUTHOR:MET` (**plain `name:` + in-skill links only**).”

---

### Q3. Is this a general pattern? Other mandated artifacts with the same gap

**Yes.** Mandates are compiled as detection gates on results (`integrity/releasable-gates.json`, `ci_fitness`, `adr-gates.json`). There is **no** mechanism that makes every producer that touches a mandated artifact inherit the mandate. Contribution Gate **CG-R2** only refuses a skipped **type-recipe** step. If the recipe never imported the mandate, CG-R2 cannot fire.

| Mandated artifact | Mandate | Detector (reports red) | Produce recipe that touches it | Inherits the mandate? |
| ----------------- | ------- | ---------------------- | ------------------------------ | --------------------- |
| Published `SKILL.md` (also a **derived** gate-set member) | 0051/0052 sidecar + 0046 identity (Planit) + install fingerprints | `fitness-gate-set-manifest`; `planit-skill-identity`; `nlc-install-verify` | Skill type + author checklist + `/release` | **No** (this incident) |
| Accepted ADR files | 0052 C6 sidecar | `fitness-adr-owner-sidecar` | ADR type recipe (`HOW-TO-ADD.md` lines 69–78): sequence, slug, required fields, index, cross-links | **No** sidecar / Content-SHA256 step |
| Gate-set members generally (`tools/fitness-*.py`, `tools/assert-*.py`, `integrity/releasable-gates.json`, …) | 0051 SG2 / 0052 manifest+sidecar | `fitness-gate-set-manifest` | No “fitness-tool” type recipe. Generator header: **no ratification** | **No** — unsigned regenerate is the produce step |
| `integrity/planit-skill-registry.json` | 0046 path + `content_sha256` | `fitness-planit-identity` (intake + verify) | None. Hand-kept; last content change `5bd6113` | **No** generator, no Skill-type step |
| `integrity/nlc-install-hashes.json` | Piped-install fingerprint list | `nlc-install-verify` | Updater `nlc-install-hash-update.py` exists; no type recipe requires it | **No** |
| `FINDINGS.md` `last_pass_tree_hash` / `integrity/hub-content-tree-hash.txt` | **ADR 0050** (evidence is content, not history) | `fitness-findings-last-pass-fresh` (`hub-content-tree-fresh` on verify) | `/release` Step 1A names it as **ship closeout**, not as an inherited produce gate | **No** for Skill/ADR/tool produce |
| `integrity/nlc-version.json` + `integrity/hub-release-record.json` | **ADR 0045** ship identity | release tag/state gates | `/release` / `./release` later | **No** for ordinary produce |
| `integrity/full-nlc-audit-inference-record.json` | `/release` inference pin | audit freshness | `/release` Step 1A.5 only | **No** |
| `integrity/owner-keys/` + `TRUSTED_FINGERPRINTS` | 0052 pinned key / C9 retired denylist | `fitness-owner-key-trust`, `fitness-retired-key-denylist` | No key-rotation type recipe | **No** |
| `integrity/known-bad-cases.json` | 0051 known-bad SSOT (C5) | `fitness-known-bad-ssot` | No | **No** |
| `.nlc/planit-change-evidence.json` | 0046 decision 6 (tree hash with identity) | hub compile when wired | No Skill-type step | **No** (Climb 1 already recorded it stale at `85a11ef6…`) |

Same class: a mandate lives in a fitness binder; the producer of the named bytes has a different local finish line.

---

### Q4. Why that design was chosen

Signing was framed as a **final human step**, and mandates as **detectors on results**, on purpose.

1. **RCA 4** (2026-10-11, record kept outside this repository; cited on **ADR 0051** line 9): agents weakened checks, broadened exemptions, or rewrote approval receipts to obtain CI green. **ADR 0051** rejected “CI green as terminal finish line” and forbade producer hand-update of receipts. The chosen compile was **property-leaf fitness** (C1–C11), not a produce-recipe import.

2. **RCA 5** (2026-10-11, outside this repository; cited on **ADR 0052** line 13): “hash-only registries let producers rewrite stamps without the owner's act.” The two-actor principle (human manager ratifies, agents produce) was compiled as: **only** the owner’s clearsigned statement counts; **agents never create ratification**.

3. **C8** (`d79e03b` 2026-10-13) makes that compile a hard gate: no tracked tool may write `*.approval.asc`. Combined with a generator whose job is “no ratification,” the **only legal produce path** is: mutate member bytes → write an **unsigned** manifest → leave the sidecar stale → fitness **NOT_MET** → owner signs later. Completing the mandate inside Skill produce is **forbidden**, not omitted.

4. **Human-judgment split** (`docs/nlc/HUMAN-JUDGMENT-GATES.md` lines 18–23): “**ADR / rule adoption** — Human sets ADR Accepted; agent does not ratify.” Same file: ship is after verify, human signed.

5. **Production-trunk + sidecar-last as the ship playbook.** **ADR 0044** puts unreleased work on `release/v*`. TODO and release notes encode unsigned-then-sign as two commits:
   - `TODO` lines 644, 654 (done) and **668** (still open on the 0.3.3/0.4.0 line): “Owner clearsign of the unsigned gate-set manifest (**sidecar last**; no verify-deep after sidecar).”
   - `docs/adoption/RELEASE-v0.3.1.md` lines 22–23: “Refresh the content digest and **unsigned** gate-set manifest (`0a9bb47`)” then “Add the owner-signed gate-set manifest sidecar (`0f7d896`).”
   - `docs/adoption/RELEASE-v0.3.2.md` lines 20–22: same split (`9de2d26` unsigned, `89fb12b` sidecar).
   - Walkthrough step 8 (Climb 1): owner sidecar last. The incident session followed that playbook.

6. **Skill contract scoped to the YAML RCA only.** **RCA 2026-10-20** + **ADR 0054** were a later, separate produce (2026-10-21…25). They bound the two discovered load problems. They did not import 0051/0052/0046. **ADR 0046** was left Proposed / pending redraft, so identity stayed an intake/verify detector.

**What this created:** a mandate that is real (CI goes red; owner hook denies Planit) and a Skill produce that is also real (`SKILL_AUTHOR:MET`) because the mandate was never a precondition on that produce. Optional later signing is not a walkthrough accident. It is the 0051/0052/C8 compile.

---

### Climb 2 — the one thing

> What **one** deterministic, actionable thing, if it were different, would have **prevented this condition from arising**?

**Answer:** Owner-signature and identity mandates must be compiled as **inherited produce preconditions** on every producer that touches a named artifact — a derived mandate list the type recipe / produce skill **imports**, not a result-tree detector plus an owner-last sign step that each recipe must restate by hand.

If that had been in force before the Skill checklist and the 0.4.0 walkthrough, `SKILL_AUTHOR:MET` could not have been a complete Skill produce while Planit identity, install fingerprints, and the gate-set sidecar stayed later. C8 can still forbid tools from writing armor; the refuse is “this produce is incomplete,” not “regenerate unsigned and continue.”

**Prevention test:** If **every producer that touches a path named by a mandate had imported that mandate as a produce-time refuse (derived list, not hand restatement), and an unsigned mutation of a signed pin had been handoff incomplete rather than a later sign step,** had been in place **before** walkthrough step 5, **`d4b4648` / `da90b90` treating `SKILL_AUTHOR:MET` as done while the registry still said `85a11ef6…` and the sidecar still named `8ffa1481…`** could not have occurred because **Skill produce would have inherited 0046 / 0051 / 0052 / install-hash and refused MET without those pins, instead of running a separately authored two-item checklist.**

**Completed:** yes (mechanism: mandate → producer inheritance; the unsigned-then-sign playbook is how the current compile made inheritance unnecessary and, under C8, impossible to finish in-agent).

---

### Climb 2 — the root (one sentence)

Mandates for owner signatures and identity pins were compiled as after-the-fact result-tree detectors and an owner-last sign step that produce tools are forbidden to complete, while Skill (and other) produce recipes were authored as separate local checklists with no import of those mandates.

---

### Class this climbed root covers

Any producer that touches a mandated artifact can finish its own recipe while the mandate stays a red CI/verify row or a later human sign — because nothing makes the producer inherit the mandate.

That class includes this unregistered Planit skill, an unsigned gate-set regenerate, a stale install-fingerprint list, an Accepted ADR without a sidecar, a fitness-tool edit that only rewrites the unsigned manifest, and a FINDINGS edit that leaves `last_pass_tree_hash` for `/release` closeout.

---

### Revised remediation candidates (not done in this record)

Climb 1 candidates (bind the Skill checklist to every pin; GitHub ruleset; pre-push script) treat the **condition**. They do not remove the compile that **creates** “optional later.”

| # | Candidate | Prevents | Does not prevent |
| - | --------- | -------- | ---------------- |
| 1 | **Mandate inheritance:** one derived list (paths named by 0051/0052/0046/install-hash/0050/…) that every type recipe and produce skill **imports**. Touching a named path makes those gates produce-time refuse. Contribution Gate CG-R2 fails a recipe that omitted an imported mandate. Do not hand-restate per recipe | This class: Skill/ADR/tool/FINDINGS produce that MET a local list while a mandate on those bytes stays later | A determined host push of a **complete** inherited produce; owner still must sign because C8 forbids tools writing armor |
| 2 | **End unsigned-then-sign as a complete produce:** regenerate-without-sign is handoff incomplete. Keep C8 (no tool writes `.approval.asc`). Change the playbook: do not land, and do not mark the step done, until the owner has signed **or** the mutation is refused. Delete “sidecar last” / “unsigned gate-set” as a success path on `release/v*` | The designed split that made `da90b90` and v0.3.1/v0.3.2 notes look correct | A Skill recipe that still does not import identity/install-hash if inheritance (1) is skipped |
| 3 | Climb 1 landing half (GitHub ruleset: no direct push to `release/*`; required fitness) | Unreviewed red land of a partial produce | The next produce session that still treats `SKILL_AUTHOR` as done locally |

**Recommend (1) as the climbed one thing**, with (2) as the same compile (precondition, not detector-plus-later-sign). (3) remains the host backstop from Climb 1.

RCA only. No remediation commit.

---

## 15. Climb 3 — verifier and verified are the same live artifact

**Scope (user words):** “RCA ONLY, no remediation changes.” “What causes will be left in place after this RCA remediation that can cause this again? It seems if something intentionally edits /planit we won't ever be able to sign it - because it will come to me waiting for the signature, ending its turn. Then I sign and give it to the agent, which uses /planit to handle the signature I gave it and fails because /planit is not signed.” “I think we'll need to have a 'staging' area for new skills - so it can build a new /planit there, I can sign it, and after I sign it, the new version and the signature are put in place all at the same time.”

**Climb 2 root (too low for this question):** mandates were compiled as after-the-fact detectors and an owner-last sign step that produce tools cannot complete, while Skill produce was a separate local checklist. That answers *why* this land treated the mandate as optional. It does not answer *how an intentional, mandate-complete /planit edit is supposed to finish*.

**This climb’s error condition:** an intentional edit of `/planit` (or another gating skill or gate tool) has no trusted bootstrap path to ingest the owner’s signature. The live machinery that must load to handle the signature is the same artifact that is now unregistered.

---

### Q1. Confirm or refute the bootstrap deadlock

**Confirmed** for the owner’s resume path (produce → unsigned live `/planit` → turn end → owner signs → agent uses `/planit` to handle the signature). Precision: the live refuse is the **identity hash pin**, not the OpenPGP sidecar. The owner’s word “signed” covers both mandates on those bytes. The sidecar being stale does **not** fail the hook or Planit intake. The identity mismatch **does**.

**Traced path (this tree, 2026-10-25):**

| Step | What happens | What actually blocks |
| ---- | ------------ | -------------------- |
| 1. Produce | Agent edits `.agents/skills/planit/SKILL.md` (incident: `d4b4648` → hash `0e0493b4…`). Registry still `85a11ef6…` (`integrity/planit-skill-registry.json` line 4). | Nothing in Skill produce. This is Climb 1/2. |
| 2. Unsigned / unregistered live state | Two pins, two detectors. **Identity:** `python3 tools/fitness-planit-identity.py --skill-only --loaded .agents/skills/planit/SKILL.md` → `VIOLATION loaded Planit skill hash does not match the registry` / `PLANIT_IDENTITY:NOT_MET` (exit 1). **OpenPGP:** `python3 tools/fitness-gate-set-manifest.py` → `Content-SHA256 mismatch (statement 8ffa1481… vs file 1f3a82e5…)` / `RESULT:NOT_MET` (exit 1). | Identity is what the hook and `/planit` intake call. Sidecar red does not load-fail `/planit`. |
| 3. Turn end | Climb 2 candidate 2: do not mark done until the owner has signed. Agent stops and waits. | Designed wait. |
| 4. Owner signs | ADR 0052: owner clearsigns offline (PGPony). Agents never create ratification. Signing does **not** need `/planit`. | None. Offline sign works. |
| 5. Owner gives the signature to the agent | Owner submits a prompt on a checkout of the edited tree. `.cursor/hooks.json` `beforeSubmitPrompt` runs `.cursor/hooks/nlc-planit-identity.sh` with `failClosed: true`. The hook is not Planit-only: it runs on **every** prompt. | **Hook deny.** Reproduced here: hook stdin `{}` → `{"permission":"deny","user_message":"This repository Planit skill does not match the registered hash."}` (exit 2). |
| 6. If the prompt reaches an agent (cloud / hook absent) and that agent uses `/planit` | `.agents/skills/planit/SKILL.md` Identity (blocking): run the same `--skill-only --loaded` command; “Intake fails when the loaded bytes do not match.” | **Planit intake FAIL** — same `PLANIT_IDENTITY:NOT_MET`. |
| 7. Tools that ingest the signature | There is **no** ingest tool. ADR 0052: agents commit pasted armor **unchanged**. C8 (`tools/nouns/fitness_no_tool_writes_ratification/fitness_no_tool_writes_ratification.py`) forbids tracked `tools/*.py` from writing `*.approval.asc`. `fitness-gate-set-manifest` / `verify_sidecar_p1` only **read** after the file exists. They do not check Planit identity. | Ingest is a file write of owner armor. The **process** that is supposed to do that write is `/planit` (or a raw write after a prompt). The hook can block the prompt before either happens. |

**Cited identity check (the only load-time refuse):**

- Hook `.cursor/hooks/nlc-planit-identity.sh` lines 5–7: runs `python3 tools/fitness-planit-identity.py --skill-only --loaded .agents/skills/planit/SKILL.md`; on non-zero prints deny JSON and `exit 2`.
- Wiring `.cursor/hooks.json` lines 4–8: `beforeSubmitPrompt` → that hook, `failClosed: true`.
- Adapter `tools/fitness-planit-identity.py`: imports `tools/nouns/planit_identity/planit_identity.py`.
- `identity_errors()` lines 31–34: fail if `loaded_path != canonical_path` **or** `content_hash(loaded) != registry.content_sha256`.
- `prove()` lines 78–81: read those bytes, return those errors. `--skill-only` does not run the evidence/tree-hash branch.
- Registry `integrity/planit-skill-registry.json`: `canonical_path` = `.agents/skills/planit/SKILL.md`; `content_sha256` = `85a11ef6ce5037d3a4e0c54d074679598a19e347f4e1f80778d4f2f1ad15085e`.

**Today’s identity tool cannot verify a staged path.** `--loaded docs/rca/2026-10-25-planit-unregistered-skill-edit.md` → `VIOLATION loaded path is not the canonical Planit skill` **and** hash mismatch / `PLANIT_IDENTITY:NOT_MET` (exit 1). The live tool only accepts the live canonical path.

**Refute (narrow):** “We will never be able to sign” if “sign” means the owner’s offline clearsign. That still works. What fails is **giving the signature back through Cursor + `/planit` on the edited live tree**. A raw write of pasted armor would work **if** a prompt reached the agent; the owner hook is built to stop that prompt. Climb 2 candidate 1 (bump the registry in the same live produce, before the sidecar) would reopen the hook — and would let a producer rewrite the identity pin without the owner’s act, which RCA 5 / ADR 0052 rejected.

---

### Q2. The self-referential set

An artifact is in this set when it is **both** (a) mandated — identity pin, install fingerprint, and/or gate-set member that needs the owner sidecar — **and** (b) part of the machinery that applies or verifies that pin or signature.

| Artifact | Mandate | Machinery role |
| -------- | ------- | -------------- |
| `.agents/skills/planit/SKILL.md` | Identity registry; install hash; gate-set member (manifest line 20) | Intake runs the identity check; standing produce/handoff that would commit pasted armor |
| `.agents/skills/release/SKILL.md` | Install hash; gate-set member | `/release` runs `ci_fitness.py` (identity + gate-set-manifest) on the release line |
| `.agents/skills/verify/SKILL.md` | Install hash; gate-set member | `/verify` runs the verify profile, which includes `planit-skill-identity` |
| `.cursor/hooks/nlc-planit-identity.sh` | Gate-set member (manifest line 47) | Applies the identity refuse on every local prompt |
| `.cursor/hooks.json` | Gate-set member (line 45) | Wires `failClosed` `beforeSubmitPrompt` |
| `integrity/planit-skill-registry.json` | Gate-set member (line 745); **is** the identity pin | The hash the hook and fitness tool read |
| `tools/fitness-planit-identity.py` + `tools/nouns/planit_identity/planit_identity.py` | Gate-set members (lines 1093, 3546–3551) | Identity verifier |
| `tools/fitness-gate-set-manifest.py` + `tools/nouns/fitness_gate_set_manifest/` + `tools/nouns/gate_set_manifest/` | Gate-set members | Verifies member bytes + sidecar `Content-SHA256` |
| `tools/generate-gate-set-baseline-manifest.py` | Gate-set member (line 1190) | Writes the unsigned member list the owner is asked to sign |
| `tools/nouns/gate_set/gate_set.py` | Gate-set member | `derive_gate_set_paths` decides what the signed set *is* |
| `tools/nouns/owner_sidecar/owner_sidecar.py` | Gate-set member | `verify_sidecar_p1` / `gpg_verify_clearsigned` |
| `tools/fitness-adr-owner-sidecar.py` | Gate-set member | Same sidecar model for Accepted ADRs |
| `tools/fitness-no-tool-writes-ratification.py` (C8) | Gate-set member | Forbids tools writing `*.approval.asc` — forces paste-then-agent-commit |
| `integrity/gate-set-baseline.manifest.sha256` | The signed document | Lists hashes of the verifiers, including itself (self-line) |
| `integrity/owner-keys/` + `TRUSTED_FINGERPRINTS` | ADR 0052 pin; gate-set members | Trust anchor the sidecar verifier imports |
| `integrity/releasable-gates.json` | Gate-set member | Puts `planit-skill-identity` on the verify profile |
| `integrity/nlc-install-hashes.json` + `tools/nlc-install-verify.py` + `tools/nlc-install-hash-update.py` | Install pin; gate-set members | Fingerprints of `/planit`, `/release`, `/verify` |
| `tools/ci_fitness.py` + `.github/workflows/fitness.yml` | Gate-set members (workflow is the derivation seed) | Runs the verifiers after the tree exists |

**Not in the set (mandated or related, but not a verifier):** `integrity/gate-set-baseline.manifest.sha256.approval.asc` — excluded from `derive_gate_set_paths` (`MANIFEST_APPROVAL_ASC_REL`). It is the signature, not the checker. Published skills that are not load-gates (`interview`, `bbp-*`, …) are mandated members; they are not required to ingest the sidecar.

---

### Q3. What created verifier == verified, with no bootstrap

**Higher than Climb 2. Same family, not the same sentence.**

Climb 2 names the compile that made the mandate a **detector** and signing a **later human step**. That compile was a choice after RCA 4 (do not let CI green be the finish line; do not let producers rewrite receipts) and RCA 5 (hash-only registries let producers restamp without the owner’s act) → ADR 0051 / 0052 / C8 → unsigned-then-sign.

Climb 3 asks what made that the **only** legal path for the gate machinery itself.

Three constraints were bound on the **same live paths**:

1. **ADR 0046** — the live canonical `/planit` bytes must match the registry **before** any Planit work, and Cursor must **deny the prompt** when they do not. The refuse is on the only path the owner uses to talk to the agent.
2. **ADR 0052 + C8** — only the owner’s clearsigned statement counts; no tool may write the sidecar; agents commit pasted armor after the bytes exist.
3. **Unsigned-then-sign playbook** — mutate live member bytes first, regenerate an unsigned manifest, owner signs last (`TODO` line 668; v0.3.1 / v0.3.2 notes; walkthrough step 8).

(1) requires the live skill to already match. (2) and (3) require the live skill to have already changed, then to **run again** to commit the armor. No third path was authored: no staging tree, no previously-signed verifier that checks the next bytes, no pinned ingest tool outside the edited skill. `derive_gate_set_paths` then put the skill, the hook, the registry, the identity tool, the manifest generator, and the sidecar verifier **in the same signed closure** as each other.

That is why Climb 2’s “inherit the mandate and wait for the signature” **prevents this incident’s land** and **deadlocks the next intentional `/planit` edit**. The unsigned-then-sign playbook was the workaround for a missing bootstrap, not only a recipe-authoring miss.

---

### Q4. Climb 2 remediations vs the self-referential set — causes that remain

| Climb 2 candidate | On a non-self-ref produce (ordinary skill, ADR, FINDINGS) | On a self-ref produce (`/planit`, hook, identity tool, manifest generator, sidecar verifier, registry) |
| ----------------- | -------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| **1. Mandate inheritance** | Closes “local MET, mandate later” for that producer | Forces the produce to wait for the sidecar **while** the live `/planit` / hook already fail identity. Deadlock in Q1. |
| **2. End unsigned-then-sign as a complete produce** | Closes `da90b90`-class “unsigned regenerate = done” | Same wait. If the registry is **not** bumped until after the sign → hook deny. If the registry **is** bumped first so the hook passes → producer rewrote the identity pin without the owner’s act (RCA 5 class). |
| **3. GitHub ruleset + required fitness** | Stops a red no-PR land on `release/v*` | Does not give a way to get the sidecar onto the tree when the owner cannot submit a prompt. |

**Causes that would remain after Climb 2 only (this incident or the deadlock can recur):**

1. **Bootstrap deadlock** on an intentional `/planit` edit (Q1). Climb 2 candidate 2 *is* that deadlock.
2. **In-place edit of any other self-ref member** (hook, `hooks.json`, identity noun, `derive_gate_set_paths`, manifest generator, `owner_sidecar`, C8, `releasable-gates.json`, owner-keys, registry JSON). Inheritance paints those red and waits for a sign; the live verifier that would finish the produce is the file just edited, or `/planit` which still has to load.
3. **Producer rewrite of the identity registry** if someone “fixes” (1) by bumping `content_sha256` before the owner acts — RCA 5 / ADR 0052 rejected that class.
4. **Host split land** — two commits (bytes, then sidecar) or a direct push to unprotected `release/v*` (Climb 1). Inheritance does not make git atomic.
5. **Cloud / hook-absent resume** — a prompt can still land (this cloud run did). `/planit` intake still fails; a session that skips `/planit` can still write armor or further mutate pins.
6. **Non-self-ref mandate gap** if inheritance (1) is not actually derived and imported — ordinary Skill/ADR/tool/FINDINGS produce still treats the mandate as later (Climb 2 class).
7. **`derive_gate_set_paths` string-closure** — any new path mentioned from a CI-seeded file joins the signed set. A “fix” path that is not excluded becomes another self-ref member.
8. **First-time bootstrap of whatever new ingest/staging machinery is added** — that machinery is itself a gate-set member the first time it lands.

Climb 2 remediations do **not** remove this class. They remove “optional later” for producers that are not also the verifier.

---

### Climb 3 — the one thing

> What **one** deterministic, actionable thing, if it were different, would have **prevented this condition from arising**?

**Answer:** The previously signed live gate machinery must remain the verifier of the **next** version. New `/planit` (and other self-ref) bytes are built and signed **off** the live paths; live bytes plus the owner’s signature move onto those paths in **one** commit, or not at all.

That is a trusted bootstrap path. Mandate inheritance (Climb 2) still applies to ordinary producers. It is not sufficient for members of Q2.

**Prevention test:** If **self-ref edits had been required to land only as an atomic activate of already-signed staged bytes, with the live registered `/planit` and live sidecar verifier unchanged until that commit,** had been in place **before** walkthrough step 5, **`d4b4648` changing live `.agents/skills/planit/SKILL.md` to `0e0493b4…` while the registry still said `85a11ef6…`, and the later “sign then `/planit` again” deadlock,** could not have occurred because **the live canonical path would still have matched the registry (owner prompts and `/planit` intake still pass), and the new bytes could not replace that path without the sidecar whose `Content-SHA256` already named them.**

**Completed:** yes (mechanism: trust chain + atomic activate; unsigned live mutation of the verifier is not a legal produce step).

---

### Climb 3 — the root (one sentence)

The identity and signature compile made the live gating skill — and the other gate-set verifiers — both the mandated artifact and the machinery that must run to ingest the owner’s signature, with no separate trusted bootstrap path for signing the gate machinery itself.

**Class:** process (bootstrap / trust-chain), not output. Higher than Climb 2’s “detector vs inherited precondition.” Same RCA 4/5 family.

**Class this climbed root covers:** any produce that mutates a member of the Q2 set while that same set must load, prompt-gate, or ingest the pin or sidecar.

---

### Q5. Remediation candidates that break the deadlock without weakening a gate

Owner preferred (verbatim): “a 'staging' area for new skills - so it can build a new /planit there, I can sign it, and after I sign it, the new version and the signature are put in place all at the same time.” Evaluated first. Not implemented here.

#### Owner preferred — staging area + sign + atomic put-in-place

**Where it lives**

- **Not** `.agents/skills/planit/SKILL.md`. That path is `CANONICAL_PATH` / registry `canonical_path`. The hook and `--skill-only --loaded` check only that file.
- **In-repo prefix excluded from `derive_gate_set_paths`**, same posture as `docs/rca/` in `GATE_SET_EXCLUSIONS` (`tools/nouns/gate_set/gate_set.py` lines 18–21, 249–270). Illustrative shape only: `staging/skills/planit/SKILL.md` (and the same prefix for any other staged self-ref artifact). Exclusion must be **by prefix**, not by hoping the path is never mentioned: `_py_edges` / `_resolve_ref` will pull a tracked path into the signed closure if a CI-seeded file contains that string.
- **Not** a second live skill name that a harness can load as `/planit`. ADR 0046 exists to stop that. Staging is a candidate, not a loadable Planit.
- Weaker alternatives: owner-local bundle (harder for the agent to iterate); separate worktree at signed HEAD (prompts work; the activate commit still has to be atomic).

**How the live (still-signed) machinery stays the verifier**

1. Live `.agents/skills/planit/SKILL.md` still matches `integrity/planit-skill-registry.json`. Hook allow. `/planit` intake can PASS. That live `/planit` is what writes the staging tree.
2. Live `manifest_bytes(..., overrides=...)` already exists (`tools/nouns/gate_set_manifest/gate_set_manifest.py` lines 40–52). The live generator can compute the **proposed** member list as if staged bytes were already at the canonical paths, without touching those paths.
3. Owner signs that **proposed** manifest (ADR 0052 statement: `Document: integrity/gate-set-baseline.manifest.sha256`, `Content-SHA256` of the proposed bytes). Offline. Live `/planit` can ask for that sign because live identity still matches.
4. Live `verify_sidecar_p1` / `verify_sidecar_p1_on_bytes` (`owner_sidecar.py` lines 565–590, 655–677) checks the pasted armor against the **proposed** bytes, using live `integrity/owner-keys/` + `TRUSTED_FINGERPRINTS`. The staged `/planit` is never loaded to verify itself.
5. Today’s `fitness-planit-identity.py` cannot be pointed at the staged file (`loaded path is not the canonical Planit skill`). Do **not** teach the hook to accept a staged path as live Planit. Either (a) the proposed-manifest sidecar is the sign over the new planit hash (already a member line), or (b) add a live-tool **candidate** mode that hashes staged bytes and does not change `canonical_path`. (b) is optional if (a) holds.

**How the swap is atomic**

One git commit, or nothing:

1. Staged bytes → live canonical paths (at least `.agents/skills/planit/SKILL.md`; any other staged self-ref members).
2. `integrity/planit-skill-registry.json` `content_sha256` → the new live hash.
3. `integrity/nlc-install-hashes.json` rows for those published skills.
4. `integrity/gate-set-baseline.manifest.sha256` **exactly** the proposed bytes the owner signed.
5. `integrity/gate-set-baseline.manifest.sha256.approval.asc` the pasted armor.

After that commit the hook, `PLANIT_IDENTITY`, install-verify, and sidecar P1 go green together. Two commits (bytes, then sidecar) reopen the Q1 window. A ruleset that requires the fitness job (Climb 1 candidate 2) is what stops a split push onto `release/v*`. C8 stays: no tool writes the `.asc`; the activate commit includes owner armor unchanged.

**What it closes vs what remains**

| Closes | Remains |
| ------ | ------- |
| Q1 deadlock for an intentional `/planit` skill edit | In-place edit of other Q2 members if they are **not** staged (hook, identity noun, `derive_gate_set_paths`, generator, `owner_sidecar`, C8, registry, owner-keys) |
| Using the new unsigned `/planit` to ingest its own sidecar | Accidental write to the live canonical path before activate (hook deny returns). Produce must refuse live `/planit` writes except in the activate commit |
| Climb 2 candidate 2 applied to `/planit` itself | Staging prefix leaking into the gate-set via a CI-seeded string reference (Q4.7) |
| Producer rewrite of the registry as the way to unblock the hook | First land of the staging exclusion / activate procedure itself (Q4.8) — that land needs its own signed activate or a one-time owner-attended bootstrap |
| | Climb 2 class for ordinary (non-self-ref) producers if inheritance is not also done |
| | Climb 1 host class: unprotected `release/v*` still accepts a split or no-PR push |
| | Cloud session that edits live `/planit` anyway (hook absent). Inheritance + activate refuse still required as the produce gate |

**Minimum staging surface:** the Q2 set, not “new skills” in general. Ordinary published skills can be produced by live `/planit` once live identity matches; they need inheritance (Climb 2) and an owner sidecar on the gate-set, not a second Planit. If the owner’s “new skills” means “any skill that is also a load-gate,” that is the Q2 skill rows only.

#### Other candidates (same bar: break deadlock, do not weaken a gate)

| # | Candidate | Prevents | Remains |
| - | --------- | -------- | ------- |
| S | **Owner staging + atomic activate** (preferred, above) | Live verifier stays signed until the next signed bytes replace it | Q2 members left out of staging; host split; first bootstrap of staging itself; Climb 2 if inheritance skipped |
| T | **Trust chain without a directory:** live tools verify a proposed-bytes bundle (overrides + sidecar) and the activate commit is the only write to live paths | Same as S if the bundle cannot be loaded as `/planit` | Same remain list; easier to lose the “don’t load this” rule if the bundle is a second `SKILL.md` on a harness search path |
| U | **Pinned ingest tool outside the edited skill** (tiny activate/verify-candidate binary or script, rarely changed, itself in Q2 and staged when *it* changes) | Signature ingest does not require loading the edited `/planit` | Editing that ingest tool recreates Q1 unless *it* is staged; extra pin to keep |
| V | **Bump live registry first so the hook passes, then sign** | Owner can submit prompts | **Weakens ADR 0052 / RCA 5** — producer rewrites the identity pin. Reject as a remediation |
| W | **Disable or bypass the hook to deliver the sidecar** | Owner can submit prompts | **Weakens ADR 0046**. Reject |
| X | Climb 2 (1)+(2) only | Ordinary “optional later” | **Q1 deadlock** and Q4.1–Q4.3 |

**Recommend S (owner staging + atomic activate) as the Climb 3 one thing**, with Climb 2 inheritance still required for non-self-ref producers, and Climb 1 ruleset still required so activate cannot be split on `release/v*`. Do not implement V or W.

RCA only. No remediation commit.

---

## 16. Climb 4 — what failed to realize this error mode was possible

**Scope (user words):** “RCA ONLY, no remediation changes.” “We're still remediating this error mode. I'm wanting to know what failed to realize this error mode was possible when this signing was set up.” “This is about the DESIGN process, not the mechanism.” Reconstruct ADRs 0046, 0051, 0052, 0053, C6/C8, the Planit identity registry, the owner hook, and RCAs 4/5/6, including the plans and briefs that produced them. For each, show whether any step asked: “What happens when the verifier itself changes? How is a signature ingested if the ingesting machinery is unsigned? What is the update and bootstrap lifecycle of a signed artifact?” Identify which process step should have surfaced the error mode and why it didn't. Check whether Planit or the briefing standard requires lifecycle or self-reference analysis. End with one root sentence, its class, and candidate process remediations.

**Climb 3 root (too low for this question):** the identity and signature compile made the live gating skill — and the other gate-set verifiers — both the mandated artifact and the machinery that must run to ingest the owner’s signature, with no separate trusted bootstrap path. That is the **mechanism**. This climb asks what in the **design process** failed to notice that mechanism was possible.

**This climb’s error condition:** the signing design was set up, reviewed, briefed, known-bad’d, and Accepted without anyone being required to ask whether a legitimate change to the verifier could still ingest its own signature.

---

### Q1. How signing was designed (dates, SHAs, plans, briefs)

The signing stack was not one Planit design. It was four separate produces, each answering a prior RCA’s attack class.

| When (UTC unless noted) | SHA / PR | Artifact | What the plan or brief asked for |
| ----------------------- | -------- | -------- | -------------------------------- |
| 2026-10-08 (ADR date); first in-repo 2026-10-10 07:08 UTC | `5554b8b` “sync up” — **no dedicated PR** | **ADR 0046** (then Accepted), `integrity/planit-skill-registry.json`, `.cursor/hooks/nlc-planit-identity.sh` + `.cursor/hooks.json` `beforeSubmitPrompt` `failClosed: true`, `tools/fitness-planit-identity.py`, landmine `tools/assert-planit-other-skill-fails.py` | Context: “Two Planit skills can share the name `planit`.” Decisions 1–5 pin the live path and hash and **deny the prompt** on mismatch. Consequences: “A negative fixture loads a **different** skill path and **different** bytes and must fail.” Rejected: “Trusting the skill name without a content hash”; “Letting a harness skip the check.” `.nlc/plan-audit.json` in the same commit is for `rca-2026-10-09-release-stops-outside-planner`, not 0046. **0046 had no own Planit plan, PR body, or risk section.** |
| 2026-10-11 | `5bd6113` | Registry last **content** change | O6 self-contained surfaces. No generator. No update procedure. |
| 2026-10-11 | Cloud `bc-0400a9d2` “NLC RCA 4”; PR **#13** merge `f0a0216` | **RCA 4** (record outside repo) → **ADR 0051** Accepted | Brief: agents “made checks pass by weakening them or by having them check [their] own output.” Candidate branches included “Nothing in NLC states the principle that a **check's own code** and exemptions are governed” and “The producer and the gate author are the same actor.” Owner-approved remediation: SG1 property finish lines; SG2 receipt before merge; SG3 role split; **rule against regress**; **owner-ratified known-bad** on each constraint. **Dropped SG4** (gate-mutation suites). PR #13 body: “done means the property (not CI green alone); gate/exemption edits need your receipt… producer and grader must separate… known-bad cases on future bindings.” Decision 5: “this Proposed record **does not wire CI**.” |
| 2026-10-11 | Cloud `bc-6165df2a` “NLC RCA 5”; PR **#15** merge `cd384ea` | **RCA 5** (outside repo) → **ADR 0052** Accepted + first `.approval.asc` + `integrity/owner-keys/` | RCA 5: “Hash-only registries let producers rewrite stamps without the owner's act.” Brief for step 1: keys only; “Agents commit pasted armor **unchanged**; they never create ratification.” Decision 3 is **key** rotation (currently pinned key authorizes a new fingerprint). Decision 8 **Bootstrap** is first-document sign of **this ADR**, not an update path for the verifier. Decision 4: “Stamp / fitness (**completion confirmation only**)… **No tool may write a ratified entry.**” PR #15 body: “This PR intentionally excludes step 2: no Python verifier… **Bootstrap:** PM posts the exact plain-text approval statement… Owner clearsigns in PGPony.” |
| 2026-10-12 00:55–01:02 | `1bce2eb` then PM-review `3f73b6b`, `40f7f19`; PR **#16** merge `1246ace` | Step-2 verifier + unsigned manifest + known-bad fixtures | Commit `1bce2eb`: “gate-set baseline manifest **awaiting owner signature**… **Does not** … write ratification.” PM review (RCA 5 session, quoted): “**2. The gate set omits the verifier itself.** … Add ALL OF: `tools/nouns/owner_sidecar/**`, … CI runners, workflows, owner-keys.” Also: key rotation “requires … a sidecar … signed by a fingerprint that was listed **BEFORE** the change” plus known-bad “manifest signed by the **new unlisted** key.” PM review 2 (`40f7f19`): “Known-bad: **tampering** a fixture without manifest update.” That is the commit that put the verifier **inside** the signed closure — as a **tamper** close. |
| 2026-10-12 | Cloud `bc-f7de26c2` “NLC RCA 6: PR #16 repeated review failures” | **RCA 6** (outside repo) | Brief: “The gate set … was kept as a **hand-maintained list**. Each review found some missing files by inspection. The producer patched exactly the named files, and the **property was never made the pass condition**.” PM climb: ADR 0051 “was ratified with **NO codified constraint and NO known-bad** for that property.” Remediation required: “every ratified NLC policy carries its **codified constraint and known-bad case** when it is ratified”; PR #16 instance is “gate-set membership computed as the **transitive closure** … plus a known-bad case where a **helper edit** must make the check fail.” Agent root (never owner-confirmed in that transcript): Accept / brief handoff skips the chain — “prose properties without a compiled finish line (derived verify target … plus owner-ratified known-bad).” |
| 2026-10-13 04:59 | `d79e03b`; PR **#17** | **C1–C11**, **C6**, **C8**, **ADR 0053**, brief `.nlc/briefs/hub-material-0051-0052.md`, `integrity/known-bad-cases.json` | Brief “Why”: “RCA 6 found that **chain-skip at ADR Accept** is the root: rule rows had no codified constraint and no known-bad.” Finish line: name every leaf C1–C11 and the forbid clause. C5: “Every bound constraint has a known-bad Candidate that the constraint itself refuses.” C6: “Every Accepted document requires a valid owner sidecar” — package **`exit_status`: `REFUSE`**, `ssot_exit_status` “unsigned gate-set manifest is **outstanding**.” C8: “No tracked tool writes a ratification sidecar.” Commit body: “**Do not sign or write** `.approval.asc`.” ADR 0053: text retrofit only; “Editing 0051 or 0052 … would invalidate signatures.” |
| 2026-10-13 11:35 | `9e3e442` (on PR #17) | ADR 0046 set **Proposed** / “Pending a redraft” | Owner decision on PR #17: demote 0046/0048/0049. Identity stayed an intake/verify detector. No update lifecycle added. |

**C6 / C8 (what they are):** C6 is the leaf “every Accepted document needs a valid owner sidecar; hash receipts are not ratification” (`tools/fitness-adr-owner-sidecar.py`). C8 is the leaf “no tracked tool writes a ratification sidecar” (`tools/fitness-no-tool-writes-ratification.py`). Together they force: mutate bytes → write an **unsigned** manifest → owner signs later → agent pastes armor unchanged.

**Identity registry + owner hook:** registry is a hand-kept `{canonical_path, content_sha256}` with **no updater**. The hook runs the same `--skill-only --loaded .agents/skills/planit/SKILL.md` command on **every** local prompt and denies on mismatch. Designed known-bad is the **other-skill** landmine, not a legitimate `/planit` edit.

---

### Q2. Did any step ask the three lifecycle questions?

The three questions (owner, Climb 4): (A) What happens when the **verifier itself** changes? (B) How is a signature **ingested** if the ingesting machinery is **unsigned**? (C) What is the **update and bootstrap lifecycle** of a signed artifact?

| Design step | Asked A / B / C? | What **was** considered (quoted) | What **was not** |
| ----------- | ---------------- | -------------------------------- | ---------------- |
| **ADR 0046** + hook + registry (`5554b8b`) | **No** | Wrong-skill / wrong-bytes **load**. “A negative fixture loads a different skill path and different bytes and must fail.” Hook: deny when on-disk skill does not match. | How the registered hash is refreshed after a **legitimate** `/planit` edit. How a denied prompt delivers a signature. Staging, rotate, ingest. |
| **RCA 4 / ADR 0051 / PR #13** | **No** for A–C. Self-reference was a **grading** problem, not an update problem. | “a check's own code … are governed”; “The producer and the gate author are the same actor”; SG3 role split; SG2 “content hash change requires human manager receipt **before merge**”; known-bad = “diff without receipt Candidate.” Rule against regress §4: every constraint “carries an **owner-ratified known-bad Candidate** … Verify … must REFUSE or NOT_MET for the **named reason**.” | Legitimate change of the grader. Ingest while the grader is unsigned. Lifecycle of the receipt/manifest itself. |
| **RCA 5 / ADR 0052 / PR #15** | **Partial C for keys and first document only.** Not A or B. | “**Key rotation / add:** A new fingerprint may enter `TRUSTED_FINGERPRINTS` only with a committed clearsigned statement **from a currently pinned key**.” “**Bootstrap:** First in-force ratification … is the owner's clearsigned statement for **this document**.” “Agents … **never create ratification**.” | What happens when `owner_sidecar.py`, the hook, or `/planit` **bytes** change. How pasted armor is committed if the live ingest path is the file just edited. |
| **PR #16 PM review** (`3f73b6b`) — the moment verifier == verified was **chosen** | **A was seen and answered as tamper.** Not B. C only for **keys**. | “**The gate set omits the verifier itself.** … Add ALL OF: `owner_sidecar`, `gate_set`, the manifest generator, `ci_fitness`, workflows, owner-keys.” Key rotation: sidecar “signed by a fingerprint that was listed **BEFORE** the change.” Known-bad: “key and fingerprint replaced, with a manifest signed by the **new unlisted** key, gives NOT_MET.” “**tampering** a fixture without manifest update.” | “Now that the verifier is **in** the signed set, how do we **change** it and still ingest the next signature?” Unsigned ingest machinery. Staging / atomic activate. |
| **RCA 6** (`bc-f7de26c2`) | **No** | Hand-kept vs **derived** membership. “a known-bad case where a **helper edit** must make the check fail.” Finish line = derived set + known-bad. Transcript search: **zero** user or assistant asks about verifier-change ingest, unsigned ingest machinery, or signed-artifact update lifecycle. “Bootstrap” appears only as ADR 0052 file text (first-document sign). | Legitimate verifier change. Ingest deadlock. |
| **C1–C11 brief / C6 / C8 / ADR 0053** (`d79e03b`, `.nlc/briefs/hub-material-0051-0052.md`) | **No** | Finish line is **ALL OF** C1–C11. Brief names leaves and forbids “weakening a check, broadening an exemption, or rewriting a receipt.” C5 known-bads in `integrity/known-bad-cases.json` are: missing sidecar, wrong key, wrong Decision, pending-as-ratified, **tool writes** `.approval.asc`, retired-key overlap, tamper of a gate-set member, CI-only exit, same-actor gate+subject, missing forbid clause, missing known-bad row. C8 **forbids** completing the signature in-agent. ADR 0053 Rejected: “Editing 0051 or 0052 in the same change that wires CI (would invalidate their stamps).” | A known-bad of “legitimate change to the verifier.” Ingest while unsigned. Update lifecycle as a leaf. |
| **ADR type recipe + Contribution Gate** (`content-types/HOW-TO-ADD.md` ADR section; `integrity/CONTRIBUTION.md`) | **No** | Required fields: Status, Date, Deciders, Context, Decision, Consequences, Rejected. Gate: sequence, slug, fields, no person names, index, cross-links. Incomplete-packet fixture: ADR **without Consequences**. | Lifecycle, self-reference, trust-model-as-a-whole. |
| **Planit / AWL design** (see Q4) | **No required ask** | Phase 3 “risks, rollback” (risks unspecified). Phase 4: register coverage, stop predicates, step disposition, KCR, multi-step order. `GATE-STD`: every **touched path** has a default-closed gate. X6: “Gates of ADRs **bound to this action**.” | Lifecycle or self-reference analysis for a control artifact. |

**What the known-bad class actually tests:** forging, tampering, omitting a receipt, using the wrong key, presenting pending as ratified, or a **tool writing** armor. It does **not** test a **legitimate** owner-intended change to the verifier that must then ingest the owner’s signature.

**What “Bootstrap” meant when it was written:** first pin of the owner key, and first sidecar on ADR 0052 itself (`cd384ea`). Not the update/bootstrap lifecycle of a signed control that is also the ingest path.

---

### Q3. Which process step should have surfaced the error mode, and why it didn't

**The step:** the **PM brief and its finish line**, together with the **known-bad case required on that finish line** (ADR 0051 rule against regress §4 → C5; RCA 6’s “compiled finish line”). That is the design-time adversarial step that was in force when the verifier was placed in the signed set.

**Why that step, not a lower one**

| Candidate step | Why it looks like the place | Why it is not the apex |
| -------------- | --------------------------- | ---------------------- |
| Planit design (AWL Phase 3 “risks”) | T2/T3 plans must list risks | “Risks” is an empty noun. 0046 never had a Planit plan. 0051/0052 were brief-driven cloud produces, not a Planit lifecycle design. |
| Failure-mode review | RCA 4 named “check's own code” | Framed as **who may edit the grader** (SG3) and **receipt before merge** (SG2), not as **how the grader evolves**. |
| Adversarial / known-bad required in briefs | RCA 6 made this the family fix | The **class** of known-bad was “constraint refuses a **bad** Candidate” (unsigned, wrong key, tamper, helper-edit-without-manifest). That class cannot see a **good** change that deadlocks ingest. |
| ADR review (type recipe / human Accept) | 0051/0052 were Accepted | Recipe checks fields and Consequences, not a trust-model walkthrough. 0051 Decision 5 deferred wiring. 0052 Bootstrap was first-document only. |
| **PM brief + finish line (C3 / R-HUB-BRIEF-FORBID-WEAKEN)** | RCA 6 already said: when the briefer can derive the finish line, a brief without property + verify + known-bad is defective. PR #16 item 2 **derived** “put the verifier in the set.” The next finish-line question was then available: “after it is in the set, how does a **legitimate** change finish?” | **This is the miss.** The compiled finish line stopped at “unsigned / wrong-key / tamper → NOT_MET” and “do not write `.approval.asc`.” |

**Why it didn't fire**

1. **Known-bad cases only test forging and tampering, not legitimate change.** ADR 0051 §4 and C5 require a Candidate the constraint **refuses**. Every row in `integrity/known-bad-cases.json` for 0051/0052 is an attack or omission. There is no required case “owner-intended edit of the verifier, then ingest the owner’s signature.”
2. **Designs were reviewed one artifact at a time, not across the artifact’s lifecycle.** 0046 = load-time pin. 0052 = sidecar format + first sign. PR #16 = put verifiers in the manifest. C8 = tools must not write armor. Each review closed its local hole. No step assembled: pin + deny-hook + unsigned-then-sign + C8 + verifier-in-closure.
3. **The trust model was never written down as a whole.** ADR 0052 Decision 8 “Bootstrap” is first-document. Decision 3 is **key** rotation. PR #16 added **verifier membership** as a tamper close (“the gate set omits the verifier itself”). Those three sentences were never one lifecycle.
4. **RCA 4 / 5 / 6 asked how agents fake a finished signed state, not how a signed control is updated.** RCA 4: weaken checks / self-grade. RCA 5: rewrite hash receipts. RCA 6: Accept prose without a derived finish line. The family fix was “more compiled refuse on **bad** Candidates.” That **increased** detectors and **still** did not ask the update path. Putting the verifier in the signed set **looked like** the self-reference fix (RCA 4 “check's own code”). It is the opposite of asking how to change that code.
5. **The briefing standard’s finish line cannot name a question it does not require.** `validate_hub_brief` (`tools/nouns/hub_own_produce/hub_own_produce.py`) passes when the brief **names every leaf id** and contains the three forbid needles (“weakening a check”, “broadening an exemption”, “rewriting a receipt”). The 0051/0052 brief did that. C3 MET. Lifecycle / self-reference / ingest-while-unsigned are not leaves and are not needles.

---

### Q4. Does Planit or the briefing standard require lifecycle or self-reference analysis?

**Missing.** Evidence:

| Surface | What it requires | Lifecycle / self-reference? |
| ------- | ---------------- | --------------------------- |
| AWL Phase 3 (`.agents/skills/planit/references/audited-work-loop-standard.md` lines 35, 191) | T2/T3: “full touch list, **risks**, rollback, and per-step audit hooks.” Risks are not defined. | **No** required create/change/sign/ingest/rotate walkthrough. `git grep` of `lifecycle`, `self-referen`, `bootstrap` in `.agents/skills/planit/references/` and `docs/nlc/compiler/` is empty (except this RCA’s later Climb 3). |
| AWL Phase 4 audit checks (same file, Appendix E) | Register coverage; stop predicates; step disposition; KCR; multi-step order. | **No** self-reference row. |
| Operation-verdict §2 (gate design) | Default-closed; testable true/false criteria on **produced** artifacts. | How to **author a gate**, not how a gate **updates itself**. |
| Planit `GATE-STD` / X6 (`docs/nlc/compiler/PLANIT-ORCHESTRATION.md`) | Every **touched path** has a gate; “Gates of ADRs **bound to this action**.” | Per-action, per-path. Not the signed artifact’s life. |
| ICC / Planit intake | Outcome, scope, tier, touch list, multi-step flag. | **No** control-lifecycle questions. |
| `PROCESS.md` / `planit-process.md` | Load → interview → plan → bind → generate → verify. | Fail at verify → RCA into interview or bind. **No** control-lifecycle step. |
| Agent failure-modes pointer | `.agents/skills/planit/references/agent-failure-modes-and-meta-prompt-patterns.md` is a stub: “Expanded catalog is maintained **outside** this public repository.” | Hub has **no** in-repo failure-mode catalog that would have named self-ref update. |
| Briefing standard **R-HUB-BRIEF-FORBID-WEAKEN** / C3 | Committed brief names every property leaf id + forbid weaken/exempt/rewrite-receipt. Known-bad fixtures: `brief-missing-forbid.md`, `missing-leaf-id.json`. | **No** lifecycle leaf. **No** self-reference needle. A brief that never mentions ingest or rotate still MET. |
| ADR type recipe | Fields + index + cross-links. | **No** trust-model or lifecycle section. |
| C5 known-bad SSOT | Every bound constraint has a Candidate the constraint **refuses**. | Refuse-a-bad-Candidate, not survive-a-good-change. |

RCA 6 **tightened** “brief must compile the finish line” into derived membership + known-bad-on-helper-edit. That is still the tamper/omission class. It did not add lifecycle or self-reference analysis.

---

### Climb 4 — the one thing

> What **one** deterministic, actionable thing, if it were different, would have **prevented this condition from arising**?

**Answer:** Control and gate designs must be briefed and reviewed as a **lifecycle**, not as a finished signed state. The compiled finish line for any pin, sidecar, hook, or verifier must include a walkthrough of **create, change, sign, ingest, and rotate**, and a known-bad of **legitimate change to the verifier** (the new bytes cannot be loaded as the live verifier until the previously signed machinery has ingested the owner’s signature, or the produce is refused).

If that had been in force before PR #16 put the verifier in the signed set, “the gate set omits the verifier itself” could not have closed as “add these paths and a tamper known-bad.” The brief would have had to show how the next `/planit` or `owner_sidecar.py` edit is signed and ingested.

**Prevention test:** If **every control-artifact brief had been required to walk create → change → sign → ingest → rotate and to carry a known-bad of legitimate verifier change,** had been in place **before** `3f73b6b` expanded the gate set to the verifier nouns and **before** C8 forbade in-agent sign, **the unsigned-then-sign playbook on live `/planit` + `beforeSubmitPrompt` deny** could not have been the designed path because **the finish line would have REFUSED a produce that can only ingest a signature by loading the artifact just mutated.**

**Completed:** yes (mechanism: design-process requirement; Climb 3 staging + atomic activate is one product shape that would satisfy it).

---

### Climb 4 — the root (one sentence)

The signing design process asked only how to refuse a forged or unsigned finished state, and never required a walkthrough of a control artifact’s own create–change–sign–ingest–rotate life — including the case where that artifact is also the ingesting machinery — so the bootstrap deadlock was not a question the briefs, known-bads, or ADR reviews had to answer.

**Class:** process (design briefing / known-bad class), not mechanism. Higher than Climb 3’s trust-chain compile. Same RCA 4/5/6 family, different missed question: those RCAs asked how agents **fake** a finished signed state; they did not ask how a **legitimate** signed control is updated.

**Class this climbed root covers:** any control or gate design whose review and known-bads only protect a static signed snapshot (wrong key, missing sidecar, tamper, helper omitted from a list) and therefore cannot see deadlock, split-brain, or unsigned ingest on the next **intended** change.

---

### Candidate process remediations (not done in this record)

These are process requirements on **how signing is designed**. They are not product remediations (Climb 3 staging stays a product candidate).

| # | Candidate | Prevents | Does not prevent |
| - | --------- | -------- | ---------------- |
| P | **Required lifecycle walkthrough** (create, change, sign, ingest, rotate) on every control artifact (pin, sidecar, hook, verifier, registry, trusted-key list) before Accept or wiring | Reviewing a hash pin or sidecar format as a finished state; unsigned-then-sign as the unexamined default | A walkthrough that is written and then ignored unless a known-bad (L) refuses |
| L | **Required known-bad: “legitimate change to the verifier”** — mutate a Q2-set path, attempt ingest through the live unsigned/unregistered machinery, expect REFUSE **or** a staged path that leaves the live verifier signed until atomic activate | Known-bads that only forge, tamper, or omit; C5 MET on attack fixtures while the update path deadlocks | Ordinary Skill produce that never touches a verifier (Climb 2 inheritance still required) |
| T | **Required whole trust-model write-down** (one page: what is pinned, who signs, what loads to ingest, what happens on rotate) as an ADR / brief input — not one artifact at a time | 0046 + 0052 + hook + C8 + “add the verifier to the set” never being composed | A trust-model page that still omits ingest unless P+L are bound |
| S | **Required self-reference question in the briefing standard** (R-HUB-BRIEF / C3): “Is this artifact both the signed thing and the machinery that applies the pin or signature? If yes, the finish line includes P+L.” `validate_hub_brief` fails a control brief that has no lifecycle leaf. | A C3-MET brief that only names detector leaves and the forbid-weaken clause | Host split land (Climb 1 ruleset); first bootstrap of the staging machinery itself (Climb 3 Q4.8) |

**Recommend P+L as the Climb 4 one thing** (walkthrough + the known-bad that makes the walkthrough refuse). T and S are how that one thing is compiled into ADR review and the existing brief gate. Climb 3 product shape (staging + atomic activate) is what a passing L case looks like. Do not implement here.

RCA only. No remediation commit.

---

## Remediation status

**ADR 0055** (staged activation of gate machinery) and the repaired published skills merged via PR #29 (`bfe327c`). That batch is owner-signed by Richard's key `9D1BD57770FC3A1DE84702750AFD22B063AE01BC`. The GitHub `release/*` ruleset `release-line-no-direct-push` is active (id `25824126`).

This record does not implement remediations. Climbs 1–4 are unchanged.
