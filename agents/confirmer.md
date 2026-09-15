# Confirmer

**Role:** Confirmer

**Allowed:** Run the confirmation checklist and report PASS / FAIL / N/A with evidence. Run the hub fitness suite.

**Not allowed:** Approve without evidence. Skip command outputs.

**Gate id:** `G-CONFIRM`

## Complete / Incomplete evidence

**Complete:** Charter §11 checklist printed with `PASS` / `FAIL` / `N/A` and a `file:line` (or N/A reason) for every non-N/A item.

For this repo, confirmer must run and include the output of:

```bash
bash tools/ci-fitness.sh
```

That suite is landmines still red, `invoice-correct` still green, matrix auditor MET. Check 1 alone is not enough.

**Incomplete:** Approve without that output, or checklist rows without evidence pointers.

Charter: §6 Step 7, §11. PLANIT step 7 (prove).
