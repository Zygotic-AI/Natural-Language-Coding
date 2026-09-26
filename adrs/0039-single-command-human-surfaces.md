# ADR 0039 — Single-command human surfaces

- Status: Accepted
- Date: 2026-09-23
- Deciders: Human manager
- Class: F (process)
- Corpus: nlc

## Context

[ADR 0017](0017-human-command-surface.md) requires a jargon-free human menu. [ADR 0022](0022-hub-release-fail-early.md) orders release gates but today exposes multiple operator entry points (`./release`, `./release prepare`, `./release finish`) that imply the human must know which phase they are in and what was already done.

Async work (PR review, merge, CI) is normal; the human surface must still be **one command** that resumes from durable state—not a checklist of separate verbs for verify, merge, push, tag, and test.

## Decision

1. **One primary command per human process.** For hub version [ship](../docs/TERMS.md#ship), the public entry is **`./release`** at repo root. Subcommands may exist for automation or recovery, but they are not the documented human path and must not be required for a correct end-to-end run.

2. **The orchestrator is stateful and resumable.** `./release` must:
   - detect what phase the repo is in (e.g. no release branch, branch pushed awaiting merge, merged awaiting tag, tag pushed awaiting CI),
   - continue through waits (merge, Enter, or polling where implemented) without the operator running a different command for each phase,
   - persist or infer progress from **git and committed artifacts** (branches, release notes, release record), not from chat or operator memory.

3. **Decompose internally, not in the menu.** Verify, notes, bump, prep, PR, merge wait, tag, and push are **steps inside** `./release`, not separate human products—aligned with [ADR 0020](0020-human-vs-agent-commands.md) (humans run `./release`; agents run maintainer tools).

4. **Zero-parameter public surface (2026-09-25).** The documented human path is **`./release` with no required flags**. Version and `release/v*` branch are inferred ([`nlc_release_infer.py`](../tools/nlc_release_infer.py)); CLI flags remain for automation overrides only ([`RELEASE.md`](../docs/adoption/RELEASE.md) appendix).

## Consequences

- [`docs/adoption/RELEASE.md`](../docs/adoption/RELEASE.md) documents **`./release` only** as the human path; `prepare` / `finish` become implementation details or deprecated aliases that forward into the state machine.
- [`scripts/nlc-release.sh`](../scripts/nlc-release.sh) uses `nlc_release_resume.py` and tag gate (`nlc_release_tag_gate.py`).
- v1 binder: [`tools/fitness-adr-0039-release-binder.py`](../tools/fitness-adr-0039-release-binder.py) + [`tools/assert-release-tag-gate-fails.py`](../tools/assert-release-tag-gate-fails.py).
- Tag push remains the moment GitHub Actions builds release artifacts ([`.github/workflows/release.yml`](../.github/workflows/release.yml)).

## Rejected

- Documenting a multi-command release ritual as the norm (“run prepare, then merge, then finish”).
- Expecting humans to track release phase in a spreadsheet or chat.
