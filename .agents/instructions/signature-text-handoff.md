# Signature text handoff (always)

Anytime you need a signature, give the exact text to the human in that same message. Do not say a signature is required and leave them to reconstruct it.

## Gate (default-closed)

Before you finish a message that needs a signature, every blocking row must be true:

| Criterion | Blocking? | Pass when |
| --------- | --------- | --------- |
| Text present | yes | The message contains the exact bytes they will sign |
| Clearly indicated | yes | The message says **Sign this** and names the output path outside the signed text |
| One surface | yes | IDE or terminal, not both wrapping the same text |
| IDE copy | yes when the session is an IDE | One fenced block; the block body is only the signed text |
| Terminal markers | yes when the session is a terminal | The start marker is the line above the text and the end marker is the line below it |

An IDE session is a chat or editor where a fenced block copies as its body. A terminal session is a plain-text transcript with no fence copy. If you cannot tell, use the IDE fence.

## IDE

One fenced block. Nothing else inside it: no command, no path, no marker line. The human copies the block body.

## Terminal

Put these marker lines on their own, immediately above and below the signed text. The markers are not part of the signed text.

```
======== SIGNATURE TEXT START ========
======== SIGNATURE TEXT END ========
```

## Harness

Linked from [`AGENTS.md`](../../AGENTS.md). Cursor injects a thin pointer at [`.cursor/rules/signature-text-handoff.mdc`](../../.cursor/rules/signature-text-handoff.mdc). SSOT is this file.
