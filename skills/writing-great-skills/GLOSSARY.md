# 术语表 — 编写优质 Skills / Commands

本术语表是 [`SKILL.md`](SKILL.md) 的 disclosed reference。粗体术语在 SKILL.md 中同样加粗。

## Predictability（可预测性）

Skill 或 command 使 agent 在每次运行时采取相同过程的程度。不是输出一致，而是行为过程一致。所有其他术语都服务于它。

## Model-Invoked

保留 `description` 的 skill/command，agent 可以看见并自动触发，人也可以手动调用。可被其他 skill 调用。代价是 **context load**。

## User-Invoked

设置 `disable-model-invocation: true` 的 skill/command，对 agent 不可见，只能由人手动调用。零 context load，但增加人的 **cognitive load**。

## Description

Skill/command 的 machine-readable trigger，也是 model-invoked 必须保持加载的 **context pointer**。

## Context Pointer

指向外部材料的引用。其 wording 决定 agent 何时、多可靠地访问目标。

## Context Load

Model-invoked skill/command 对上下文的持续占用成本，来源是 `description`。

## Cognitive Load

User-invoked skill/command 对人的记忆成本：需要记得它存在以及何时调用。

## Information Hierarchy

内容按 agent 需要的紧迫程度分层：in-skill steps → in-skill reference → disclosed reference。

## Progressive Disclosure

把 **reference** 移出 `SKILL.md`，通过 **context pointer** 引用，保持顶部可读。

## Steps

Skill/command 中的有序动作。有 steps 时占据主层级，每个 step 以 **completion criterion** 结束。

## Completion Criterion

告诉 agent 工作完成的条件。最强的标准同时满足 **checkable**（能判断完成）和 **exhaustive**（要求彻底）。

## Post-Completion Steps

当前 step 之后的 steps。可见时会诱使 agent **premature completion**。

## Legwork

Agent 在单个 step 内做的幕后工作，由 leading word 或 demanding completion criterion 驱动。

## Reference

Agent 按需查阅的材料：定义、规则、事实、示例。没有 steps 时，reference 可以是 skill 的全部内容。

## Branch

Skill/command 的不同调用路径或处理场景。

## Leading Word

预训练中的 compact concept，用于锚定行为。

## Single Source of Truth

每个意思只在一个权威位置存在。

## Relevance

某行内容是否仍与 skill/command 的职责相关。

## No-Op

不改行为的指令。测试：删掉这句话会改变 agent 行为吗？

## Failure Modes

- **Premature completion**：step 提前结束
- **Duplication**：意思重复
- **Sediment**：陈旧内容堆积
- **Sprawl**：skill/command 过长
- **No-op**：不改行为的指令
