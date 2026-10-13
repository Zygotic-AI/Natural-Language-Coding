# ADR 0047 — ADR approval receipts

- Status: Superseded
- Superseded-by: ADR 0052
- Date: 2026-10-08
- Deciders: Human manager
- Ratified-by: Human manager (practice-enforcement task list, 2026-10-08)
- Class: F (process)
- Corpus: nlc

## Context

Active records 0001–0045 say Accepted. Only 0044 and 0045 carried `Ratified-by:`. An edit to an accepted record could keep the Accepted line while the approved bytes changed. The enforcement table still left 0007, 0009, and 0028 as gaps.

## Decision

1. One registry, `integrity/adr-approval-receipts.json`, keys each active record number to the SHA-256 of that file.
2. Records 0001–0043 share one bulk receipt object that lists each hash. Later active records use the same object.
3. Any edit that changes the hash makes `receipt_holds` false until a new receipt is written.
4. The hub compile fails when any active record is missing a receipt, has a status cell that is not bound, or has a status cell marked as a gap.
5. Each active record has a gate path and a fixture path in `integrity/adr-gates.json`. The fixture must fail when that record's approved bytes change. Records 0007, 0009, and 0028 also have a fixture that fails when their decision is violated.

## Consequences

- `docs/ADR-ENFORCEMENT.md` has no gap status on an active record.
- Version class for this policy is minor.

## Rejected

- Treating the word Accepted as the approval.
- Leaving a gap row in force and still compiling the hub.
