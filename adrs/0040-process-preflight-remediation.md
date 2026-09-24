# ADR 0040 — Process preflight and remediation (exit early)

- Status: Accepted
- Date: 2026-09-23
- Deciders: Human manager
- Class: F (process)
- Corpus: nlc

## Context

[ADR 0013](0013-requirements-preflight.md) requires listing all missing requirements at entry. [ADR 0018](0018-human-cli-interview-on-gap.md) requires plain-language gap reporting for humans. [ADR 0022](0022-hub-release-fail-early.md) orders cheap gates before expensive work.

Processes still fail when the operator starts on the wrong branch, merges the wrong line, or hits a state the tool could have detected—because remediation was left to memory instead of embedded questions and fixes.

## Decision

1. **Default-closed entry.** Every human orchestrator (starting with **`./release`**) runs a **preflight** that checks all known blocking conditions for the current repo state before irreversible or expensive steps.

2. **Exit early with remediation, not mystery.** On `NOT_MET`, the tool prints:
   - **What’s wrong** (one line),
   - **Why it blocks** (which ADR / gate),
   - **Fix** (exact commands or choices),
   - **Not** “you should have remembered X.”

3. **Disambiguation is part of the process.** When context is ambiguous, the tool **asks**—examples for release:
   - started on `main` but `release/v*` branches exist → list candidates and ask which release line to continue (or offer to create a new one from current preflight),
   - target branch may lack merged features → offer to compare against `main` or named branches and show commits not in the release line,
   - version file vs last tag vs branch name disagree → show all three and refuse until resolved.

4. **Async waits are in-process.** Waiting for PR merge remains inside `./release` ([ADR 0039](0039-single-command-human-surfaces.md)); preflight re-runs after resume where state may have changed.

## Consequences

- Release script gains branch/candidate listing and merge-completeness prompts (see [`TODO`](../TODO)).
- Other human entrypoints (`./nlc`, `/interview` gap blocks) already align; new orchestrators copy this pattern.
- v1 binder: **expansion** — `fitness-human-surface-binder` or release-specific fitness cites ADR 0040 checklist in RELEASE.md (follow-up).

## Rejected

- Failing with a single opaque exit code and no fix path.
- Assuming the operator already knows which `release/v*` branch is canonical.
