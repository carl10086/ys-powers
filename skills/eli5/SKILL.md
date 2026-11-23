---
name: eli5
description: 用适合五岁孩子理解的简单语言解释主题，使用具体、友好的儿童熟悉类比和大图、少文字的 HTML artifact。仅手动调用：/eli5 [topic]。
argument-hint: "[topic]"
disable-model-invocation: true
---

# eli5

Explain like I'm someone who knows nothing about this topic, using a self-contained HTML artifact with big pictures and few words.

Write the HTML file to the system temporary directory's `.eli5/` subdirectory (`$TMPDIR/.eli5/` on macOS/Linux, or `/tmp/.eli5/` when `TMPDIR` is unset). Return the real file path; do not write only to an `out://` artifact.

Topic: $ARGUMENTS
