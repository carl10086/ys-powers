---
name: why
description: 调查代码或设计为什么会变成现在这样，从历史记录给出有引用的原因与取舍；只想知道当前如何运行时不使用。
disable-model-invocation: true
---

# Why

从记录回答“为什么”，不要根据当前代码猜测动机。

1. 明确要调查的设计、规则或代码。
2. 找到引入它的 commit、PR 和作者讨论。
3. 检查每一次后续修改；证据不足时，继续查 issue、ADR、postmortem 等一手记录。
4. 引用作者实际写下的原因和取舍。
5. 分开写明记录确认的事实、自己的推断，以及记录无法回答的问题。

改编自 Cursor pstack 的 [`why`](../../../refer/cursor-plugins/pstack/skills/why/SKILL.md)，上游采用 MIT License，Copyright (c) 2026 Lauren Tan。
