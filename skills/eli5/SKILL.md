---
name: eli5
description: Explain a topic like I'm a 5 year old. Use when the user types /eli5 <topic> or asks for a dead-simple picture explainer of how something works.
argument-hint: "[topic]"
disable-model-invocation: true
---

# eli5

Explain like I'm someone who knows nothing about this topic, using a self-contained HTML artifact with big pictures and few words.

Write the HTML file to the system temporary directory's `.eli5/` subdirectory (`$TMPDIR/.eli5/` on macOS/Linux, or `/tmp/.eli5/` when `TMPDIR` is unset). Return the real file path; do not write only to an `out://` artifact.

Topic: $ARGUMENTS
