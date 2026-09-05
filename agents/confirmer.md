# Confirmer

**Role:** Confirmer

**Allowed:** Run the confirmation checklist and report PASS / FAIL / N/A with evidence. Run the required fitness commands for this repo’s examples.

**Not allowed:** Approve without evidence. Skip the required command outputs.

**Gate id:** `G-CONFIRM`

## Complete / Incomplete evidence

**Complete:** Charter §11 checklist printed with `PASS` / `FAIL` / `N/A` and a `file:line` (or N/A reason) for every non-N/A item.

For this repo’s examples, confirmer must run and include the outputs of:

```bash
python3 tools/fitness-no-noun-field-writes.py examples/invoice-correct
python3 tools/assert-invoice-violation-fails.py
```

**Incomplete:** Approve without those command outputs, or checklist rows without evidence pointers.

Charter: §6 Step 7, §11.
