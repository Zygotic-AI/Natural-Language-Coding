# [Confirmer](../docs/TERMS.md#confirmer)

**Role:** [Confirmer](../docs/TERMS.md#confirmer)

**Allowed:** Run the confirmation checklist and report PASS / FAIL / N/A with evidence. Run the [hub](../docs/TERMS.md#hub) fitness suite.

**Not allowed:** Approve without evidence. Skip command outputs.

**[Gate](../docs/TERMS.md#gate) id:** `G-CONFIRM`

## Complete / Incomplete evidence

**Complete:** [Charter](../docs/TERMS.md#charter) §11 checklist printed with `PASS` / `FAIL` / `N/A` and a `file:line` (or N/A reason) for every non-N/A item.

For this repo, [confirmer](../docs/TERMS.md#confirmer) must run and include the output of:

```bash
bash tools/ci-fitness.sh
```

That suite is landmines still red, `invoice-correct` still green, matrix auditor [MET](../docs/TERMS.md#met). Check 1 alone is not enough.

**Incomplete:** Approve without that output, or checklist rows without evidence pointers.

[Charter](../docs/TERMS.md#charter): §6 Step 7, §11. [PLANIT](../docs/TERMS.md#planit) step 7 (prove).
