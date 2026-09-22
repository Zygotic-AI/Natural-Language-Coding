# Change version class (hub + adopter repos)

When you change a repo that uses [NLC](../../docs/TERMS.md#nlc) (this hub or an adopter compiled system), **ask the human** which release class applies unless it is obvious:

| Class | When | [Hub](../../docs/TERMS.md#hub) semver | [Adopter](../../docs/TERMS.md#adopter) [ship](../../docs/TERMS.md#ship) |
| ----- | ---- | ---------- | ------------ |
| **Patch** | Fixes, docs-only, internal tooling, no new requirements | patch | same intent; refresh [verify](../../docs/TERMS.md#verify) fingerprints |
| **Minor** | New requirements, policy, or scope (e.g. PCI, HIPAA, new ADR/rule pack) | minor | ratify new ADRs/rules; [UC9](../../docs/TERMS.md#uc9) regen if bindings change |
| **Major** | Breaking [contract](../../docs/TERMS.md#contract), charter-level change, removed obligations | major | [ADR](../../docs/TERMS.md#adr) + plan with named callers; [prove](../../docs/TERMS.md#prove) stays red until accepted |

**Intuition examples**

- Adding PCI handling as a new [requirement pack](../../docs/TERMS.md#requirement-pack) → **minor** (not patch).
- Renaming or tightening a [published verb contract](../../docs/TERMS.md#published-verb-contract) → **major** ([ADR 0006](../../adrs/0006-contract-change-notice.md)).
- Fixing [gate](../../docs/TERMS.md#gate) tooling or [interview](../../docs/TERMS.md#interview) copy with no [requirement](../../docs/TERMS.md#requirement) change → **patch**.

[Hub](../../docs/TERMS.md#hub) releases: **`./release`** (default waits for PR merge, then tags) or **`./release prepare`** / **`./release finish`**. No [tag](../../docs/TERMS.md#tag) before merge. Commit **`docs/adoption/RELEASE-vX.Y.Z.md`** with a filled **Highlights** section; draft the **Changes since** block with `python3 tools/nlc_release_notes.py --write-draft --version X.Y.Z --to HEAD` (see [`RELEASE.md`](../../docs/adoption/RELEASE.md)).

[Adopter](../../docs/TERMS.md#adopter) repos: bump is usually “material compile change” vs doc-only; align with `CONFIRM.md` [change class](../../docs/TERMS.md#change-class) and `./nlc verify-deep` before [ship](../../docs/TERMS.md#ship).
