# Prove and ship

NLC separates **compile** (machine gates on intent-bound artifacts) from **ship** (human acceptance of release liability). Both matter early; neither replaces the other.

## Default order (fix upstream first)

1. **Generate one artifact** (PLANIT 6).
2. **Gate that artifact immediately** (PLANIT 6.5, ADR 0010) — metrics named in the plan; default fail.
3. **Prove the tree** — adopter fitness suite (and hub `ci_fitness.py` when touching the hub).
4. **Promotion gates** — run the same suites on every merge to main / QA branch; do not save all checking for “release week.”

Deferring audits until production guarantees larger blast radius: the same defect costs more to fix downstream and violates gate-after-generate.

## Tools

| When | Tool | Pass means |
| ---- | ---- | ---------- |
| After each generate | Plan gate + artifact metrics | That artifact is allowed to exist |
| CI on app repo (PR / QA) | Adopter-bound `fitness-*.py` / `ci_fitness.py` | Tree still matches bound reqs/ADRs/rules |
| Promotion / release candidate | [`tools/release-audit.py`](../../tools/release-audit.py) | Compile checks + human `Released-by:` where class requires it |

`release-audit.py` is **not** a substitute for per-artifact gates. It is a **bundle check** before a human promotes a build (QA sign-off, staging, or production). Run it when a candidate is “complete enough to test as a unit,” not only minutes before customers.

## QA vs production “ship”

| Stage | Typical gate |
| ----- | ------------- |
| Dev / PR | Fitness on changed tree; PLANIT 6.5 per generated file |
| QA / integration | Full adopter fitness + `release-audit.py` **without** treating missing `Released-by:` as optional if your class requires it for QA promotion |
| Production | `Released-by:` on `CONFIRM.md` (human, not agent — C24) |

An audit that “checks everything except release-worthiness” only has value if **earlier** gates already ran. Otherwise findings pile up and fixes violate upstream-first RCA.

## Hub vs app repo

- **This hub repo** — `python3 tools/ci_fitness.py` proves the practice specimens and gates.
- **Your compiled system** — `nlc-init` scaffolds `CONFIRM.md`; wire fitness + `release-audit.py` in **your** CI (see [`BOOTSTRAP.md`](../adoption/BOOTSTRAP.md)).

Compile-green in an app repo means “safe to keep building.” Ship-ready means “human accepted liability” for the promotion you defined.
