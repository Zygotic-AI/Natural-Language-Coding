# ADR Index

Full history of every ADR. Nothing is ever deleted. This is the audit trail.

Each entry: number, created date, origin (source, page, line), status, successor, lineage id.

The binder does **not** read this file. It reads [ACTIVE.md](ACTIVE.md). This file exists for audit, traceability, and human investigation.

See [ADR 0029](0029-adr-lineage-active-set-and-bind-snapshot.md).

| ADR | Created | Origin | Status | Successor | Lineage |
|-----|---------|--------|--------|-----------|--------|
| 0001 | 2026-01-01 | charter | active | — | L-0001 |
| 0002 | 2026-01-01 | charter | active | — | L-0002 |
| 0003 | 2026-01-01 | charter | active | — | L-0003 |
| 0004 | 2026-01-01 | charter | active | — | L-0004 |
| 0005 | 2026-01-01 | charter | active | — | L-0005 |
| 0006 | 2026-01-01 | charter | active | — | L-0006 |
| 0007 | 2026-01-01 | charter | active | — | L-0007 |
| 0008 | 2026-01-01 | charter | active | — | L-0008 |
| 0009 | 2026-01-01 | charter | active | — | L-0009 |
| 0010 | 2026-01-01 | charter | active | — | L-0010 |
| 0011 | 2026-01-01 | charter | active | — | L-0011 |
| 0012 | 2026-01-01 | charter | active | — | L-0012 |
| 0013 | 2026-01-01 | charter | active | — | L-0013 |
| 0014 | 2026-01-01 | charter | active | — | L-0014 |
| 0015 | 2026-01-01 | charter | active | — | L-0015 |
| 0016 | 2026-01-01 | charter | active | — | L-0016 |
| 0017 | 2026-01-01 | charter | active | — | L-0017 |
| 0018 | 2026-01-01 | charter | active | — | L-0018 |
| 0019 | 2026-01-01 | charter | active | — | L-0019 |
| 0020 | 2026-01-01 | charter | active | — | L-0020 |
| 0021 | 2026-01-01 | charter | active | — | L-0021 |
| 0022 | 2026-01-01 | charter | active | — | L-0022 |
| 0023 | 2026-01-01 | charter | active | — | L-0023 |
| 0024 | 2026-09-22 | session | active | — | L-0024 |
| 0025 | 2026-09-22 | session | active | — | L-0025 |
| 0026 | 2026-09-22 | session | active | — | L-0026 |
| 0027 | 2026-09-22 | session | active | — | L-0027 |
| 0028 | 2026-09-22 | session | active | — | L-0028 |
| 0029 | 2026-09-22 | session | active | — | L-0029 |
| 0030 | 2026-09-22 | session | active | — | L-0030 |
| 0031 | 2026-09-23 | session | active | — | L-0031 |
| 0032 | 2026-09-23 | session | active | — | L-0032 |
| 0033 | 2026-09-23 | session | active | — | L-0033 |
| 0034 | 2026-09-23 | session | active | — | L-0034 |
| 0035 | 2026-09-23 | session | active | — | L-0035 |
| 0036 | 2026-09-23 | session | active | — | L-0036 |
| 0037 | 2026-09-23 | session | active | — | L-0037 |
| 0038 | 2026-09-23 | session | active | — | L-0038 |
| 0039 | 2026-09-23 | session | active | — | L-0039 |
| 0040 | 2026-09-23 | session | active | — | L-0040 |
| 0041 | 2026-09-23 | session | active | — | L-0041 |
| 0042 | 2026-09-23 | session | active | — | L-0042 |
| 0043 | 2026-09-23 | session | active | — | L-0043 |
| 0044 | 2026-09-25 | session | active | — | L-0044 |

## Lineage format

When an ADR is superseded, add a row or update status:

```
| 0142 | 2026-03-01 | policy §4.2 p.12 | superseded | 0198 | L-0142 |
| 0198 | 2026-09-01 | policy §4.2 p.14 | active | — | L-0142 |
```

Same lineage id. Old ADR stays. New ADR cites it. ACTIVE reflects only the tip.
