# RCA: PR #38 reached the owner signature with a hidden executable-shape NOT_MET

**Date:** 2026-10-27  
**Context:** Natural-Language-Coding hub — PR #38 (`cursor/v041-hash-out-of-gate-set-8ecd`) at `2b760cb`; measurements taken there, this record lands off `release/v0.4.1`  
**Status:** open (analysis only; no remediation in this record)

**Scope (user words):**

- “Do not fix anything yet.”
- “Run an RCA (conduct-rca-2 style: defective product first, then the process that produced it, climb until the root is a process/principle) on why PR #38 reached Richard's signature with a hidden NOT_MET: the two new assert scripts are UNCLASSIFIED in fitness-executable-shape, and that row was masked because ci_fitness stops at the first failing check (fitness-gate-set-manifest).”
- “Questions: why was the shape failure not seen before the signing ask (by you, and by my finish line, which only required 'red only on the signature check')? Is fail-fast masking in ci_fitness itself a fail-open defect class (later checks unknown counts as pass)? Also determine, without changing files: would classifying the two scripts change integrity/gate-set-baseline.manifest.sha256 (i.e. require a new signature)?”
- “Write the RCA as docs/rca/2026-10-27-pr38-masked-shape-failure.md on a new branch off release/v0.4.1, open a draft PR to release/v0.4.1, and report root, proposed remediation, and the re-sign answer.”

**Resolution table (this record):**

| Criterion | This record |
| --------- | ----------- |
| Scope (user words) | Quoted above; outcome is this RCA + draft PR only |
| No narrowing | Product, process climb, both named questions, remanifest/re-sign answer — all present |
| Question vs implement | Analysis only; no product, process, or signature change |
| Their vocabulary | Hidden NOT_MET, UNCLASSIFIED, fail-fast masking, fail-open, later checks unknown counts as pass, classifying, re-sign |
| Version class | Patch (instance record only) |

---

## 1. Error condition

**Observed (bounded, reproducible) on PR #38 at `2b760cb`:**

1. Two new executables exist and are wired into the hub fitness suite:
   - `tools/assert-content-only-change-does-not-trip-gate-set-signature-passes.py` (4102 chars)
   - `tools/assert-gate-set-member-change-fails-closed.py` (2531 chars)
2. `python3 tools/fitness-executable-shape.py` prints:

   ```text
   UNCLASSIFIED:2
   UNCLASSIFIED tools/assert-content-only-change-does-not-trip-gate-set-signature-passes.py
   UNCLASSIFIED tools/assert-gate-set-member-change-fails-closed.py
   RESULT:NOT_MET
   ```

   Those are the only two unclassified executables on that tree. 441 other `tools/*.py` files (not under `tools/nouns/`) classify as `primitive adapter`.
3. Before the owner sidecar landed, CI `fitness` failed at `CI:FAIL fitness-gate-set-manifest` and stopped. `fitness-executable-shape` never ran on that job.
4. The produce asked the owner to sign Content-SHA256 `bbdc6a411031be65b523884c5c77e4fa44768a3b8474c73c1676da919fa7ca52` and stated that CI may be red only on the signature check.
5. After the owner-pasted armor landed unchanged (`2b760cb`), the signature check is `RESULT:MET`. The same `fitness` job then fails on `fitness-executable-shape`.

**This climb’s error condition:** a signature-pending produce reached the owner signing ask with a later check already NOT_MET, and that later result was unknown at ask time.

**Not the error condition:** the Option A exclusion of `integrity/hub-content-tree-hash.txt` from the signed set (PR #38 product). That work is a separate produce. This record is the masking of a second NOT_MET behind the expected signature row.

---

## 2. Defective product

Two product facts composed.

### 2.1 The two scripts are UNCLASSIFIED

`classify()` in `tools/nouns/executable_shape/executable_shape.py`:

```python
if rel.startswith("tools/") and rel.endswith(".py"):
    if "from nouns." in text and len(text) < 2500:
        return "primitive adapter"
    return None
```

Both scripts contain `from nouns.` Both are at or over 2500 characters (4102 and 2531). The classifier returns `None`. Kind is `python`; class is missing; the file is UNCLASSIFIED.

The in-tree convention is a thin `tools/assert-*.py` adapter (import + `main`) with the body under `tools/nouns/…`. That shape is how the other 441 `tools/*.py` files pass. There is no type recipe for “add an assert script” in `content-types/HOW-TO-ADD.md`, so the convention is implicit.

### 2.2 `ci_fitness` stops at the first failing check

`fail()` in `tools/nouns/ci_fitness/ci_fitness.py`:

```python
def fail(msg: str) -> None:
    print(f"CI:FAIL {msg}")
    if os.environ.get("CI_FITNESS_CONTINUE") == "1":
        _CI_FAILURES.append(msg)
        return
    sys.exit(1)
```

Default: `CI_FITNESS_CONTINUE` is unset. GitHub `fitness.yml` runs `bash tools/ci-fitness.sh` → `python3 tools/ci_fitness.py` with no continue flag.

On PR #38 the suite order is:

| Label | Position |
| ----- | -------- |
| `fitness-gate-set-manifest` | first of the ratification block (`run(` at line 721) |
| `assert-content-only-change-does-not-trip-gate-set-signature` | later; those scripts execute as tests |
| `assert-gate-set-member-change-fails-closed` | later |
| `fitness-executable-shape` | later (`run(` at line 824 on PR #38; line 813 on `release/v0.4.1`) |

On the unsigned tree, the first of those to fail is the signature check. Forty later `run(` calls never execute. The shape check is one of them.

**Mechanism:** fat `tools/*.py` → UNCLASSIFIED → `fitness-executable-shape` is NOT_MET, **and** fail-fast means that NOT_MET is not printed while the sidecar is missing.

The scripts themselves can PASS as tests (they did, locally and as later suite rows once continue/order allowed). The hidden row is the **shape** check on those files, not the asserts’ own verdicts.

---

## 3. Upstream chain (process before output)

| Step | Artifact / layer | What it did |
| ---- | ---------------- | ----------- |
| (symptom) | Owner signing ask + first CI:FAIL | Sidecar requested; only visible red row was `fitness-gate-set-manifest` |
| 7 | Agent produce for PR #38 | Added two fat assert scripts; remanifested; offered the six-field statement; said CI may be red only on the signature check |
| 6 | Local verification the agent actually ran | Derived lists; the two named asserts; remanifest; `fitness-gate-set-manifest` (expected NOT_MET). Did **not** run `fitness-executable-shape` or `CI_FITNESS_CONTINUE=1` |
| 5 | Finish line in the produce brief | Required (a) derived lists (b) content-only test (c) fail-closed member test (d) remanifest + statement (e) checklist rule. Allowed “CI may be red only on the signature check pending [the owner] signature; say so explicitly.” Did **not** require a remaining-suite inventory |
| 4 | Confirmer skill | `python3 tools/ci_fitness.py` (fail-fast). Complete if the suite output is `CI:MET` or an “honest `CI:FAIL`.” A first-check fail satisfies that sentence |
| 3 | Implicit add-executable convention | Thin adapter + noun body. No blocking recipe. A finish line that says “a test proving…” can be met by a fat `tools/*.py` |
| 2 | Prior signature-pending produces (PR #29, PR #36) | Same allowed sentence: green except the owner-signature rows. Trained the next brief to treat the first signature `CI:FAIL` as the remaining-suite proof |
| 1 | Principle gap | A finish line that claims “red only on X” under a fail-fast runner treats every unrun later check as pass. Unknown result counts as pass. That is fail-open |

**Furthest controllable upstream point:** the briefing / finish-line / confirmer rule for a signature-pending produce. The two unclassified files and the fail-fast runner are outputs of that rule (the brief did not require remaining-check evidence; the runner does not emit it by default).

---

## 4. Checks the user named

### 4.1 Why was the shape failure not seen before the signing ask (by the agent)?

**Because the agent verified the finish-line rows and stopped.**

What ran before the statement was offered:

- `python3 tools/derive-gate-set-closure-reference.py .` (row a)
- the two new assert scripts (rows b and c)
- remanifest + Content-SHA256 (row d)
- checklist text (row e)
- `fitness-gate-set-manifest` as the expected red signature row

What did not run:

- `python3 tools/fitness-executable-shape.py`
- `CI_FITNESS_CONTINUE=1 python3 tools/ci_fitness.py`

GitHub then showed `CI:FAIL fitness-gate-set-manifest` and nothing after it. The agent read that truncated log as confirmation of “red only on the signature check.”

That is an agent-session miss **and** a brief miss. The session followed the written finish line.

### 4.2 Why did the finish line not see it?

**The finish line pre-authorized the claim and did not require evidence for it.**

The produce brief listed five proofs and then said CI may be red only on the signature check. “Red only on X” is a claim about **every other check**. Under fail-fast, the only observed result is X. The brief treated that observation as the proof.

It also named the two new tests as (b) and (c). It did not name `fitness-executable-shape`. Adding a new executable is exactly when that check is live. The finish line tested the **behavior** of the new scripts and not the **shape** of the new scripts.

The same sentence appeared on earlier signature-pending produces (“all PR checks green except the owner-signature rows”). Those produces used it for bootstrap/sidecar occupancy. Copying it onto a produce that **adds new executables** made the hidden shape row possible.

### 4.3 Is fail-fast masking in `ci_fitness` itself a fail-open defect class (later checks unknown counts as pass)?

**Yes, for the remaining-check inventory. No, for the suite-as-a-whole.**

| Claim | Fail-closed? | Why |
| ----- | ------------ | --- |
| “The hub fitness suite is MET” | Yes | First failure exits 1. The job is red. Missing later results do not make the suite pass. |
| “The only NOT_MET is the signature check” / “CI may be red only on the signature check” | **No** | Later checks were not run. They have no result. The allowed finish-line sentence fills that absence with pass. |

Fail-open, as used on the v0.4.1 fail-closed work and in the two new asserts themselves, is: missing tool, empty result, or **unknown result counts as false (not a pass)**.

Fail-fast masking is that class when anyone consumes the truncated log as a complete inventory:

- Later check result = unknown.
- “Red only on the signature check” = those unknowns counted as pass.

`CI_FITNESS_CONTINUE=1` already exists and would have printed both `CI:FAIL fitness-gate-set-manifest` and `CI:FAIL fitness-executable-shape`. Default off means the inventory is not produced. The defect is not that the job goes green. The defect is that **the only consumer-visible per-check signal is the first failure**, and the finish line is allowed to treat that as “everything else is MET.”

So: fail-fast in `ci_fitness` is fail-closed for “suite MET” and fail-open for “which checks are MET,” which is the claim a signature-pending finish line makes.

### 4.4 Would classifying the two scripts change `integrity/gate-set-baseline.manifest.sha256` (require a new signature)?

**Yes. Determined without writing any file.**

On PR #38 at `2b760cb`:

- Both scripts are members of `derive_gate_set_paths` (`is_gate_set_path` True).
- The signed manifest Content-SHA256 is `bbdc6a411031be65b523884c5c77e4fa44768a3b8474c73c1676da919fa7ca52`.
- `manifest_bytes(root, overrides=…)` rebuilds the manifest in memory. Every classification path that edits a member changes that digest:

| In-memory override (no disk write) | New Content-SHA256 | Changed? |
| ---------------------------------- | ------------------ | -------- |
| Shrink the content-only script to 2400 bytes (then `classify` → `primitive adapter`) | `f14a3b785b657c16b3122a09ac273a0496d7daa5b3e2c08c3a7454dfa35a0015` | yes |
| Append a comment to the member-change script (does not even classify; still a member-byte edit) | `2ed727678ecc4d1c5f6d53612fcddc8828c4bce925e5f47dfa1fa9dd60ca85c0` | yes |
| Change the 2500 cap to 9999 in `executable_shape.py` (also a member) | `8f4c4f30f0196cfa269dfcf9f61e6a479b2920ae087ea6562323cdb838192374` | yes |

Moving the bodies under `tools/nouns/` and leaving thin adapters would add new gate-set members and change existing member bytes. Same result: remanifest + new owner sidecar.

**Re-sign answer:** classifying the two scripts requires a new owner signature. Do not classify on this analysis branch.

---

## 5. Impact / scope

- The owner signed a statement for a tree that was already NOT_MET on `fitness-executable-shape`.
- After ingest, CI is still red. The sidecar did not finish the produce.
- Any later signature-pending produce that adds an executable can hide the same row, or any other check after `fitness-gate-set-manifest` (owner-key trust, mandate inheritance, live self-ref, produce preflight, …).
- The two named asserts’ fail-closed helpers are not in doubt. Their **files** are the landmine for the shape check.

---

## 6. Timeline (brief)

| Time | Event |
| ---- | ----- |
| Produce brief for PR #38 | Finish line (a)–(e) plus “CI may be red only on the signature check” |
| `7853eae` | Hash exclusion + two fat assert scripts + remanifest; statement offered |
| First CI on that head | `CI:FAIL fitness-gate-set-manifest`; suite exits; shape check unrun |
| Owner signs the six-field statement (VALIDSIG on the named key) | Armor ingested at `2b760cb` |
| CI on `2b760cb` | Signature MET; `fitness-executable-shape` NOT_MET (`UNCLASSIFIED` × 2) |
| This record | Analysis only; no classify, no remanifest, no second statement |

---

## 7. Mechanism on reproduction

**Confirmed (product), at `2b760cb`:**

```text
len(content-only script) == 4102
len(member-change script) == 2531
"from nouns." in both == True
classify(each) == None
is_gate_set_path(each) == True
fitness-executable-shape == NOT_MET (exactly those two paths)
CI_FITNESS_CONTINUE unset => fail() sys.exit(1)
fitness-gate-set-manifest runs before fitness-executable-shape
```

**Confirmed (process):** the produce brief’s finish line allowed “red only on the signature check” without a remaining-suite command. The confirmer skill accepts an honest first `CI:FAIL`. The agent session ran (a)–(e) and not `fitness-executable-shape`.

**Confirmed (re-sign), in memory only:** `manifest_bytes(..., overrides=)` changes Content-SHA256 under every classification edit listed in §4.4.

---

## 8. Candidate roots (at most three)

| Candidate | §3 bar | Verdict |
| --------- | ------ | ------- |
| Classify the two scripts / raise the 2500 cap | Output-only; next fat `tools/*.py` + signature-pending finish line repeats the hide | Reject as the one thing (product follow-up) |
| Default `CI_FITNESS_CONTINUE=1` | Detection; would have printed the second CI:FAIL on this instance. Next brief can still claim “red only on X” from a partial local run | Too low (runner follow-up) |
| Signature-pending finish line / confirmer must refuse the signing ask unless remaining checks are **observed** MET; unknown counts as false | One process change; deterministic; earliest controllable; matches the fail-open class the user named | **Survives** |

---

## 9. The one thing

> What **one** deterministic, actionable thing, if it were different, would have **prevented this error condition from arising**?

**Answer:** A signature-pending produce (brief, confirmer, finish line) must **refuse the signing ask** unless the remaining suite is an **observed inventory**: every check after the expected signature NOT_MET has a printed MET (from `CI_FITNESS_CONTINUE=1` or from running those checks). Unknown later results count as false. “CI may be red only on the signature check” is incomplete without that inventory.

**Prevention test:** If **that refuse** had been in force **before** the PR #38 statement was offered, **“reached the owner signature with a hidden NOT_MET”** could not have occurred because **the signing ask would have been refused until `fitness-executable-shape` (and the other later rows) printed MET or were themselves listed as known NOT_MET.**

**Completed:** yes (mechanism: finish-line / confirmer refuse). Classifying the two scripts is what would then make the remaining inventory MET. That is a product follow-up and needs a new signature (§4.4). Do not implement here.

**Class:** process / principle (unknown remaining-check result counts as pass). Same family as fail-open: empty or unknown counts as false, inverted by the finish line.

---

## 10. Contributing factors

- The 2500-character cap is working as written. The scripts are over it.
- No type recipe for adding `tools/assert-*.py`, so “a test proving…” can land as a fat file.
- Confirmer “honest `CI:FAIL`” does not distinguish first-check fail from remaining-suite fail.
- Prior “green except sidecar” produces made the sentence feel sufficient.
- Fail-fast is a reasonable default for wall-clock CI. It is the wrong default for a claim about later checks.
- C8 (no tool-written armor) is correct. It made the hidden row expensive; it did not create it.

---

## 11. Remediation options (not done)

Every option is required to pass the same **known-bad:** a signature-pending produce that adds an unclassified executable must **refuse the signing ask**. A produce whose remaining inventory is observed MET may ask. After classify, a new sidecar is expected.

### Option A — Finish-line / confirmer refuse (the one thing)

**Process:** standing instruction + confirmer complete-row: before offering a statement, run `CI_FITNESS_CONTINUE=1 python3 tools/ci_fitness.py` (or an equivalent remaining-check list) and attach the inventory. If any later label is missing or NOT_MET, refuse. Unknown = refuse.

**Tradeoffs:** Prevents this class. Does not classify the current two scripts. Next agent still has to classify to get a green remaining inventory.

### Option B — Runner emits a remaining inventory on fail-fast

**Product:** on first failure, `ci_fitness` prints `CI:UNKNOWN <label>` for every later `run(` it will not execute, then exits 1. Finish lines cannot say “red only on X” when `CI:UNKNOWN` lines exist.

**Tradeoffs:** Makes the fail-open visible in default CI. Still needs Option A so agents do not ignore `CI:UNKNOWN`. Detection, not prevention of unclassified files.

### Option C — Classify the two scripts (thin adapters + nouns)

**Product:** move bodies under `tools/nouns/`; leave `<2500` adapters that contain `from nouns.`. Remanifest. New owner sidecar.

**Tradeoffs:** Fixes this instance’s shape row. Does not stop the next fat script plus “red only on signature.” Requires re-sign (§4.4).

### Option D — Raise or drop the 2500 cap

**Product:** edit `executable_shape.py` so these two files classify as `primitive adapter`.

**Tradeoffs:** Weakens the thin-adapter convention. Still a member edit; still re-sign. Next signature-pending produce can hide a different later check.

### Option E — Default `CI_FITNESS_CONTINUE=1` in CI

**Product:** GitHub `fitness` always prints every `CI:FAIL`.

**Tradeoffs:** This instance would have shown both reds before the owner signed **if** the agent had waited for a continue run. The first unsigned CI would have been double-red; the brief could still have offered the statement from local (b)(c) only. Pair with A.

**Rejected as the only fix:** “just classify now” (C or D alone) and “just sign again.” Those clear the current red without closing the class.

---

## 12. Preventive action (single tracked item — not done)

| Field | Value |
| ----- | ----- |
| Action | Add a refuse to the signature-pending finish line / confirmer: remaining-check inventory required; unknown = false. Then classify the two scripts and remanifest (new sidecar). |
| Owner | hub |
| Path / artifact | `.agents/skills/bbp-confirmer/SKILL.md`, produce-brief / finish-line standing instruction; follow-up on the two assert paths + `ci_fitness.py` inventory |
| Verification | A fixture produce that adds an unclassified `tools/*.py` and has a missing sidecar **refuses** the signing ask; `CI_FITNESS_CONTINUE=1` lists `fitness-executable-shape` NOT_MET. After classify + remanifest + sidecar, remaining inventory is MET. |
| Belief / gate touch | Unsuitable process: “red only on the signature check” under fail-fast. Touches confirmer / briefing; product follow-up touches the two scripts and needs a new signature |

---

## 13. Follow-up (detection only)

- Do not classify, remanifest, or ask for a second signature from this analysis PR.
- PR #38 stays red on `fitness-executable-shape` until a later produce does Option C (and re-signs).
- PR #37 stays untouched here.

RCA only. No remediation commit.
