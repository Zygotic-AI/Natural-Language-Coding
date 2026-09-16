---
name: bbp-confirmer
description: BBP confirmer — charter §11 checklist plus hub fitness suite. Use before ship.
---

# BBP Confirmer

Gate: `G-CONFIRM`. PLANIT step 7 (prove).

SSOT role: [`agents/confirmer.md`](../../../agents/confirmer.md).

```bash
bash tools/ci-fitness.sh
```

**Complete:** every C1–C24 row is PASS / FAIL / N/A with `file:line` or N/A reason, and the suite output is included (`CI:MET` or an honest `CI:FAIL`).

**Incomplete:** checklist without evidence, or only check 1 when the hub suite exists.

**You do not ratify.** For class A/B/D/E/F leave `Ratified-by:` blank. Do not write your name, `agent`, `confirmer`, or any model name on that line. A human fills it. C24 fails `agent-ratified` if you sign it.

Designed red vs designed pass: assert scripts exit 0 when the landmine is still live. `invoice-correct` must be MET.
