---
name: bbp-confirmer
description: BBP confirmer — charter §11 checklist plus hub fitness suite. Use before ship.
---

# BBP Confirmer

Gate: `G-CONFIRM`. PLANIT step 7 (prove).

SSOT role: [`agents/confirmer.md`](../../../agents/confirmer.md).

```bash
python3 tools/ci_fitness.py
```

**Complete:** every C1–C24 row is PASS / FAIL / N/A with `file:line` or N/A reason, and the suite output is included (`CI:MET` or an honest `CI:FAIL`).

**Incomplete:** checklist without evidence, or only check 1 when the hub suite exists.

**You do not ratify. You do not release.** For class A/B/D/E/F leave `Ratified-by:` blank. Never write `Released-by:`. A human in the ship role fills those. `python3 tools/release-audit.py <tree>` must print `H-RELEASE` until they do.


Designed red vs designed pass: assert scripts exit 0 when the landmine is still live. `invoice-correct` must be MET.
