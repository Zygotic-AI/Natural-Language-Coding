# ACTIVE ADRs

This is the **only** file the binding process reads.

Rule: if an ADR is not listed here, it does not apply. No superseded-check logic in the binder. Lineage resolution happens at retirement time, not at bind time.

A plan snapshots this set at bind time. A freshness check fails the plan if ACTIVE changes between bind and emit.

See [ADR 0029](0029-adr-lineage-active-set-and-bind-snapshot.md).

---

| ADR | Lineage | Origin | Effective |
|-----|---------|--------|----------|
| 0001 | L-0001 | charter | 2026-01-01 |
| 0002 | L-0002 | charter | 2026-01-01 |
| 0003 | L-0003 | charter | 2026-01-01 |
| 0004 | L-0004 | charter | 2026-01-01 |
| 0005 | L-0005 | charter | 2026-01-01 |
| 0006 | L-0006 | charter | 2026-01-01 |
| 0007 | L-0007 | charter | 2026-01-01 |
| 0008 | L-0008 | charter | 2026-01-01 |
| 0009 | L-0009 | charter | 2026-01-01 |
| 0010 | L-0010 | charter | 2026-01-01 |
| 0011 | L-0011 | charter | 2026-01-01 |
| 0012 | L-0012 | charter | 2026-01-01 |
| 0013 | L-0013 | charter | 2026-01-01 |
| 0014 | L-0014 | charter | 2026-01-01 |
| 0015 | L-0015 | charter | 2026-01-01 |
| 0016 | L-0016 | charter | 2026-01-01 |
| 0017 | L-0017 | charter | 2026-01-01 |
| 0018 | L-0018 | charter | 2026-01-01 |
| 0019 | L-0019 | charter | 2026-01-01 |
| 0020 | L-0020 | charter | 2026-01-01 |
| 0021 | L-0021 | charter | 2026-01-01 |
| 0022 | L-0022 | charter | 2026-01-01 |
| 0023 | L-0023 | charter | 2026-01-01 |
| 0024 | L-0024 | session | 2026-09-22 |
| 0025 | L-0025 | session | 2026-09-22 |
| 0026 | L-0026 | session | 2026-09-22 |
| 0027 | L-0027 | session | 2026-09-22 |
| 0028 | L-0028 | session | 2026-09-22 |
| 0029 | L-0029 | session | 2026-09-22 |
| 0030 | L-0030 | session | 2026-09-22 |
| 0031 | L-0031 | session | 2026-09-23 |
| 0032 | L-0032 | session | 2026-09-23 |
| 0033 | L-0033 | session | 2026-09-23 |
| 0034 | L-0034 | session | 2026-09-23 |
| 0035 | L-0035 | session | 2026-09-23 |

When an ADR is superseded, remove it from this table and add its successor. Update INDEX status in the same change.
