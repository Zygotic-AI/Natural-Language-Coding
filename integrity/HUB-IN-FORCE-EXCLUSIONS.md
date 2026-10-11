# Hub in-force surface exclusions (O6)

Gates **fitness-hub-public-self-contained** and **fitness-internal-links** treat every file under the repo as **in-force** unless its path matches an exclusion below. This is an exclusion list only; history and RCA instance records stay out of scope.

## Excluded prefixes

| Prefix | Reason |
|--------|--------|
| `docs/history/` | Archived prose; not operating law |
| `docs/rca/` | RCA instance records (may cite old paths and names) |
| `theory/history/` | Frozen theory drafts |
| `examples/` | Adopter fixtures and landmines |
| `node_modules/`, `.git/`, `.venv/`, `venv/`, `__pycache__/` | Tooling caches |

## Excluded top-level names

| Name | Reason |
|------|------|
| `uploads/` | Ephemeral agent uploads |

## Person-name gate (CG-R4) only

Accepted ADR ratification headers may still name deciders until a dedicated re-ratification PR lands (ADR 0047). **Person-name patterns** are not applied under `adrs/`; forbidden private-repo markers still apply there.

Implementation: `tools/nouns/hub_in_force_surfaces/hub_in_force_surfaces.py` (`EXCLUDED_PREFIXES`, `EXCLUDED_TOP_LEVEL`, `PERSON_NAME_EXCLUDED_PREFIXES`).
