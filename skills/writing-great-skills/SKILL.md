---
name: Writing Great Skills
description: Reference for writing and editing skills and commands well — the vocabulary and principles that make a skill or command predictable. Use when creating, reviewing, or refactoring a skill/command.
disable-model-invocation: true
---

# 编写优质 Skills / Commands

Skill 与 command 的存在是为了**从随机系统里挤出确定性**。核心美德是 **predictability（可预测性）**——不是让每次输出相同，而是让每次执行的过程相同。

粗体术语的定义见 [`GLOSSARY.md`](GLOSSARY.md)。

## 调用方式

两种选择，trade-off 不同：

- **Model-invoked**：保留 `description`，agent 能自动触发，也能被其他 skill/command 调用。代价是 **context load**（description 每轮都占上下文）。
- **User-invoked**：设置 `disable-model-invocation: true`，只有人手动调用。零 context load，但增加人的 **cognitive load**（得记得它存在）。

选择原则：只有 agent 必须自动触发时才用 model-invoked。纯手动的 skill/command 做成 user-invoked。

当 user-invoked 数量过多时，用一个 **router skill** 做索引。

## 撰写 description

Model-invoked 的 `description` 做两件事：说明 skill 是什么，列出触发它的 **branches**。每个词都在增加 **context load**，所以要比 body 更严格地剪枝：

- **开头放 leading word**
- 一个分支一个 trigger，同义词不要重复
- 只写触发场景，body 里已有的内容不再重复

## 信息层级

Skill/command 内容由两类混合而成：**steps** 和 **reference**。核心决策是每层放什么。层级按 agent 需要的紧迫程度排列：

1. **In-skill step**：`SKILL.md` 内的有序动作，主层级。每个 step 以 **completion criterion** 结束——告诉 agent 什么情况下算做完。标准要 checkable（能判断完成）且尽量 exhaustive（彻底）。
2. **In-skill reference**：`SKILL.md` 内的定义、规则，按需查阅。可以是平铺的同级集合。
3. **Disclosed reference**：推到 `SKILL.md` 外部，通过 **context pointer** 引用，只在 pointer 触发时加载。

**Progressive disclosure**：把 reference 往下层移动，保持顶部可读。按 **branch** 判断：所有路径都需要的内容内联，只有部分路径需要的内容 disclosure。

## 何时拆分

拆分会花费两种 load 之一，只有值得时才拆：

- **By invocation**：有独立的 **leading word** 应该单独触发，或另一个 skill 必须调用它时，拆成 model-invoked skill。
- **By sequence**：后续 **post-completion steps** 诱使 agent 提前完成当前 step 时，拆出去隐藏后续步骤。

## 剪枝

- 每个意思保留 **single source of truth**
- 每行检查 **relevance**：它还跟 skill 做的事有关吗？
- 每句做 **no-op 测试**：删掉这句话会改变行为吗？不会就删

## Leading Words

Leading word 是模型预训练里已有的 compact concept，agent 在执行时用它思考。它在文中重复出现，以分布式定义锚定一大片行为，同时调用模型已有的 prior。

例如：

- "fast, deterministic, low-overhead" → **tight**
- "a loop you believe in" → **red**

好处：省 token，同时给 agent 一个清晰的行为钩子。优先使用已有词汇，少造新词。

## 失败模式

| 模式 | 含义 | 解法 |
|---|---|---|
| **Premature completion** | 当前 step 没做完就想跳到下一步 | 先 sharpen completion criterion；仍不行再拆分 |
| **Duplication** | 同一个意思出现在多处 | single source of truth |
| **Sediment** | 陈旧内容堆积，不敢删 | 定期 pruning |
| **Sprawl** | skill/command 太长 | 用信息层级下推 reference，按 branch/sequence 拆分 |
| **No-op** | 说的话 agent 本来就会做 | 逐句测试，删不改行为的句子 |
