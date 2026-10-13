# Hub material brief — ADR 0051 / 0052 retrofit (C1–C11)

This committed brief is the `brief_ref` for the hub produce package. It names every property leaf id and forbids obtaining MET by weakening a check, broadening an exemption, or rewriting a receipt.

## Property leaf ids

- `C1` — hub-scope-derived: hub material and changed paths come from git, never from the package.
- `C2` — handoff-hub-profile: produce handoff refuses a hub package with no property leaves.
- `C3` — brief-forbid-weaken: this brief names every leaf and carries the forbid clause.
- `C4` — no-check-on-check: no wired tool grades another fitness or assert tool's source or logic.
- `C5` — known-bad-ssot: every bound constraint has a known-bad Candidate that the constraint itself refuses.
- `C6` — sidecar-all-accepted: every Accepted document needs a valid owner sidecar.
- `C7` — pending-known-bad: Pending or Proposed presented as ratified is NOT_MET.
- `C8` — no-tool-writes-ratification: no tracked tool writes `*.approval.asc` or ratified registry state.
- `C9` — retired-key-denylist: retired fingerprint 1A86E89505A908766DFD7304F04AD1CEC768DB18 never enters TRUSTED_FINGERPRINTS.
- `C10` — adr-gates-rows: `integrity/adr-gates.json` maps each 0051/0052 constraint to a check and known-bad.
- `C11` — rules-ssot: `integrity/adr-0051-0052-rules.json` ids equal `derive-adr-0051-0052-rules.py`.

## Forbid clause

Stabilization and cloud-agent work on hub material must **forbid** weakening a check, broadening an exemption, or rewriting a receipt to obtain MET.
