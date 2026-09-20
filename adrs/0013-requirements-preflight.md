# [ADR](../docs/TERMS.md#adr) 0013 — Requirements preflight (fail fast, list all)

- Status: Accepted
- Date: 2026-09-20
- Deciders: Human manager
- Class: F (process / tooling)

## Context

Install and [prove](../docs/TERMS.md#prove) scripts assumed `python3`, `git`, or other tools were present. Failures surfaced mid-run after partial work. Operators need one clear signal listing **every** missing prerequisite.

## Decision

1. **Earliest point:** Before any mutating or expensive work, run a **requirements preflight**.

2. **Collect all gaps:** Do not exit on the first missing binary; build the full list, then fail once.

3. **Output shape (normative):**
   - First line: `REQUIREMENTS:NOT_MET`
   - Following lines: `  missing: <what>` (one per gap)
   - Optional: `  hint: <how to fix>`
   - Exit code non-zero.

4. **Python SSOT:** [`tools/nlc_requirements.py`](../tools/nlc_requirements.py) — profiles (`hub_prove`, `hub_tool`, `install_remote`, `install_local`).

5. **Shell installers:** [`scripts/install.sh`](../scripts/install.sh) and [`scripts/install.ps1`](../scripts/install.ps1) use the same message shape before clone/copy.

6. **Pass line (optional):** `REQUIREMENTS:MET` when a script chooses to log success (install may skip).

## Consequences

- [Hub](../docs/TERMS.md#hub) [prove](../docs/TERMS.md#prove) entrypoints call `hub_prove` preflight (`ci_fitness.py`, `ci-fitness.ps1`).
- Consumer-facing CLIs under `tools/nlc-*.py` call `hub_tool` preflight.
- New scripts with external dependencies must preflight per this [ADR](../docs/TERMS.md#adr).

## Rejected

- **Lazy failure** halfway through a fitness suite or install copy.
- **Different error formats** per script without documenting an exception [ADR](../docs/TERMS.md#adr).
