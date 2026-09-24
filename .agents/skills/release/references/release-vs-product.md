# Release readiness — continuity vs product

**Continuity** = at this SHA, machine manifest + SSOT headers + inference agree. Blocks `./release` when step **0c** (`release-prep`) fails.

**Product** = expansion / parked work in FINDINGS and `uc-product-status.json`. Often **does not** block `./release` when v1 binders are MET and gaps are `expansion_only`.

| Signal | Usually blocks ship? | `./release` behavior |
| ------ | -------------------- | -------------------- |
| `full-nlc-audit` release-prep NOT_MET | **Yes** | Prepare refuses |
| `FINDINGS` `last_pass_sha` ≠ HEAD | **Yes** | Fails `findings-last-pass-fresh` stage |
| Open TODO **Continuity** rows (unmerged batch, stale inference SHA) | **Often yes** | Fix or waive explicitly |
| Open TODO **product** rows (UC16/UC20 expansion, composable IR) | **No** (default) | Ship with residuals |
| Dirty git (uncommitted ship intent) | **Yes** until agent closeout | **`/release` Step 1A** commits; user does not |
| `--profile full` not run | **No** | Optional; `./release` runs verify-deep separately |

**User question:** “Ship without X?” — only meaningful when X is **product**; continuity gaps need fix or honest **NO-GO**.

## Aborted or partial `./release`

Resume SSOT: `python3 tools/nlc_release_resume.py --emit json` (same detector as `./release`).

| Phase | `/release` skill | `./release` script |
| ----- | ---------------- | ------------------ |
| `await_merge` | Skip `release-prep`; **GO** to continue waiting for PR merge | No prepare 0c; `wait_for_merge` → tag |
| `tag_ready` | Skip `release-prep`; optional tag-gate check; **GO** | `cmd_finish` (tag gate + push) |
| `complete` | Report already shipped | Prints done; bump for next version |
| `prepare` | Full readiness then **GO** | `run_prepare_core` … |

Invoking **`/release`** after Ctrl-C at “Press Enter when merged…” is **continue**, not a new ship.
