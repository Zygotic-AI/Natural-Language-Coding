# ADR 0058 — No harness hooks; NLC is harness- and model-agnostic

- Status: Proposed
- Date: 2026-11-07
- Deciders: Human manager
- Class: F (process)
- Corpus: nlc
- Related: [ADR 0010](0010-gate-after-every-generate.md), [ADR 0021](0021-verify-fast-and-deep.md)
- Product story and reasons: [`docs/nlc/FEATURES.md`](../docs/nlc/FEATURES.md)
- Version class of this change: **minor** (new policy; not a published-contract break)

## Context

NLC must work with commodity models and with commonly used agent setups (Cursor, Claude Code, Codex, Copilot, and others). It does not guarantee identical output from every model. It does guarantee the same compile rules.

Today this hub registers Cursor-only hooks (Write/Delete on generated files, and a prompt-submit identity check). Those hooks do not see shell redirects, other tool connections, or helper-agent writes. Other setups have no such hooks at all. Keeping them as the way NLC “notices” generated files marries NLC to one editor.

A soft rule of the form “you may use editor hooks, and if you do not, remember to run verify” is not a rule. People forget. The law has to be a single sentence.

## Decision

1. **No harness hooks.** NLC does not ship, require, or rely on editor/harness hooks (Cursor `preToolUse`, `beforeSubmitPrompt`, or the equivalent in any other tool). Compile correctness is enforced on the files in the repo (`./nlc verify` / `./nlc verify-deep` and the generate stamps and gate receipts those commands already check).

2. **No required model or agent provider.** NLC does not name a required model, agent host, or harness. If a commonly used model or harness cannot meet a reasonable compile expectation, the first move is to change NLC. A “not recommended” label is allowed only after that analysis shows the expectation is reasonable and that setup still will not meet it.

3. **Enabling a harness later is explicit.** A future milestone may add a named harness. That work lands as accepted decisions for that harness, including a check that the harness in use is the one named, and a fail if it is not. Until that milestone, the rule is no hooks.

4. **In-tree Cursor wiring is removed after this record is accepted.** Removal includes `.cursor/hooks.json` and `.cursor/hooks/*`, the fitness that currently requires the Write/Delete hook, and adopter examples that tell people to copy Cursor hooks. That removal is follow-on work, not this record’s first landing.

## Consequences

- Verify on the tree is the only notice path for generated files.
- Adopters are not told to install editor-specific traps.
- Future harness support cannot sneak in as “optional convenience.” It is an accepted decision that names the harness.
- Identity of the Planit skill (this repo’s copy) must be enforced by repo gates, not by a Cursor prompt-submit hook.

## Rejected

- **Keep Cursor Write/Delete hooks and hope other harnesses run verify.** That is two rules, one of them hope.
- **Require a specific model or harness for NLC to be “supported.”** Commodity models are the point.
- **Implement hook removal in the same change as first proposing this record.** Spec first; remove after accept.

## Proposal (G-PROPOSE)

- **Change class:** F
- **Nouns / verbs / goals touched:** none in this landing (docs + this record). After accept: hook scripts and the fitness that requires them.
- **Adjectives that must hold:** default-closed compile; verify remains the merge gate.
- **Non-goals:** shipping a Cursor (or any) harness integration; inventing the majority-key pack-signing scheme; changing generate stamps.
- **Tests when implementing removal:** a check that fails if `.cursor/hooks.json` registers `preToolUse` / `beforeSubmitPrompt` (or any harness hook) as NLC enforcement; existing verify still fails a generated file that skipped the stamp.
- **Impact:** anyone using the current Cursor Write/Delete deny loses that early pop-up; they keep verify.
