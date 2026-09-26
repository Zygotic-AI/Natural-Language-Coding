# Smoke: production-trunk release (ADR 0044)

Run from a clean clone when validating orchestrator changes.

```bash
python3 tools/nlc_release_main_purity.py --check
python3 tools/nlc_release_infer.py --emit json
python3 tools/nlc_release_resume.py --emit json
```

New release from a work branch (zero-parameter):

```bash
git checkout my-feature-branch
./release --dry-run
```

Continue on release line:

```bash
git checkout release/vX.Y.Z
./release --dry-run
```

Resume tag leg (after merge):

```bash
./release --dry-run
```

Expected: `RELEASE:INFER` banner; no interactive quizzes; `RELEASE:NOT_MET` or phase-appropriate dry-run log lines only.
