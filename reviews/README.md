# Reviews

Bot-auditable review packages for PRs. Each PR directory contains artifacts required for automated audit per P-015 (no human review).

## Package structure

Each `pr-NNN/` directory contains:

| File | Purpose |
|------|---------|
| `PLAN.md` | Goal, success criteria, out of scope |
| `APPLICABILITY.md` | Standards that apply; ADRs in scope; matrix rows affected |
| `BOUNDARY-IO.md` | Each noun/verb boundary crossed with input → output pointers |
| `ADVERSARIAL.md` | Self-review notes: what could cheat, what was checked |
| `VERIFY.md` | Machine-checkable verification checklist |
| `verify.sh` | Executable verification script (exit 0 = pass) |

## Usage

Run all checks for a PR:

```bash
bash reviews/pr-003/verify.sh
```

## Constraint

**P-015 / KD-010:** Richard does NOT review PRs. All PR packages must be fully bot-auditable.
