---
name: [bbp-confirmer](../../../docs/TERMS.md#bbp-confirmer)
description: [BBP](../../../docs/TERMS.md#bbp) [confirmer](../../../docs/TERMS.md#confirmer) — [charter](../../../docs/TERMS.md#charter) §11 checklist plus [hub](../../../docs/TERMS.md#hub) fitness suite. Use before [ship](../../../docs/TERMS.md#ship).
---

# [BBP](../../../docs/TERMS.md#bbp) [Confirmer](../../../docs/TERMS.md#confirmer)

[Gate](../../../docs/TERMS.md#gate): `G-CONFIRM`. [PLANIT](../../../docs/TERMS.md#planit) step 7 (prove).

SSOT role: [`agents/confirmer.md`](../../../agents/confirmer.md).

```bash
python3 tools/ci_fitness.py
```

**Complete:** every C1–C24 row is PASS / FAIL / N/A with `file:line` or N/A reason, and the suite output is included (`CI:MET` or an honest `CI:FAIL`).

**Incomplete:** checklist without evidence, or only check 1 when the [hub](../../../docs/TERMS.md#hub) suite exists.

**You do not ratify. You do not release.** For class A/B/D/E/F leave `Ratified-by:` blank. Never write `Released-by:`. A human in the [ship](../../../docs/TERMS.md#ship) role fills those. `python3 tools/release-audit.py <tree>` must print `H-RELEASE` until they do.


Designed red vs designed pass: assert scripts exit 0 when the landmine is still live. `invoice-correct` must be [MET](../../../docs/TERMS.md#met).
