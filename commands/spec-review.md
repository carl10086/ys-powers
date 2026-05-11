---
description: 评审 spec 文档：AI 提炼关键点 + 列 issues，人勾选哪些是 blocker 拍板
---

# /spec-review

帮人审 spec 长文档：AI 提炼关键点、列 issues，由人勾选哪些是 blocker 拍板。**核心原则：AI 列，人选。** 把"哪条 issue 重要"的判断权留给人——LLM 在分级判断上飘，人 1 秒能判。

## 1. 定位 spec（三段式，同 `/plan`）

1. 当前 session 中刚生成的 spec → 用其路径
2. 否则取 `docs/ys-powers/specs/` 下最新的 `*-design.md`
3. 都没有 → 友好提示并问用户

`/spec-review` **不接受参数**。

## 2. 通读 spec + 必要的对照

- 读 spec 全文
- 如果 spec 引用了其它文件 / commit / 路径，**实际去读对照**（grep / git show / Read）。Naive review 容易"凭 spec 文字判断"；动手对照能发现真问题（路径错、版本错、引用漂移）。

## 3. 输出报告——固定四段标题，不自创章节

```
## Spec Review: <spec 标题>

【关键点提炼】
（4~7 条 bullet，回答"这份 spec 在干什么"）

【Issues】
（≤ 7 条；不分级；按你直觉的严重度排序）
1. [维度] @§N
   > <spec 原文引用 ≤3 行；缺失类填 "(原文未提及)">
   问题: <issue>
   建议: <建议>
2. ...

**为什么内联引用？** 让人勾选 blocker 时不必翻回 spec 来回对照——AI 把判断所需的原文摆到你眼前。

【Advisories】
（溢出的小建议、锦上添花的措辞改进；不进后续多选）
- ...
```

**严格禁止**：

- 自动把 issues 分成 Blocker / Should / Nit / 严重 / 一般 等任何分级标签
- 用自创章节名（"总体判断"、"可放行判断"、"修改建议"、"优先级"等）
- 在报告里下"可以进 plan / 建议实施" 之类的盖棺定论
- 修改原 spec 文件
- Issues 超过 7 条（多余的归到 Advisories）

## 4. 五维分类（用于 [维度] 标签）

| 维度 | 该看什么 |
|---|---|
| **Completeness** | 六大核心区是否齐全（Objective / Commands / Project Structure / Code Style / Testing / Boundaries）；Success Criteria / Open Questions 是否显式 |
| **Consistency** | 章节互相不矛盾；Tech Stack 与 Commands 自洽 |
| **Clarity** | 需求会被两种合理理解；Boundaries 三层是否具体 |
| **Scope** | 是单一可计划单元，没偷渡多个独立子系统 |
| **YAGNI** | 无 spec 没要求的功能、推测性抽象 |

**Calibration**：只挂会让 plan 阶段做错事的 issue。不为凑数升级。措辞瑕疵 / 章节详尽程度参差 → Advisories，不进 Issues。**优先指出"漏了什么"而不是复述"写了什么"** —— 自审场景下作者已经知道写了什么，"缺失"才是真价值。

## 5. 让人勾 blocker

报告呈完后，**调一次 AskUserQuestion**：

- `question`: "这 N 个 issues 里，哪些你想现在拍板？不勾的留作 advisory。"
- `multiSelect`: true
- `options`: 把 Issues 段每条做成一个 option（label = 简短标题 ≤12 字；description = 原文引用 + 问题，≤120 字 —— 让人不必翻回 spec 就能拍板）

**人勾的每条** → 再调一次 AskUserQuestion **单选**给出 2-3 个解法选项让人选。

人一条都没勾 → 跳过追问，直接进 §6。

## 6. 直接修改原文

根据人的决策，直接修改 spec 原文：
- 人勾的 issues + 选的解法 → 体现到对应章节
- 未勾的 issues → 忽略

修改完成后，简要汇总改动。

## Common Mistakes（来自 baseline 观测）

| 错误 | 修正 |
|---|---|
| 把 issues 分 Blocker / Should / Nit | 永不分级；分级是人勾选的事 |
| 自创章节名（"总体判断"等） | 严格用【关键点提炼】【Issues】【Advisories】 |
| 直接写"可以进入实施阶段" | 不下结论，决议来自人勾选 |
| Issues 数量超过 7 | 排序取头部 7 条，剩下落 Advisories |
| 跳过 AskUserQuestion 直接出结论 | 必须 multiSelect 让人勾 |

## Red Flags — STOP

如果你正在写：

- "分级标准是..."
- "## 总体判断" 或 "## Blocker" 或任何非约定章节名
- "这份 spec 可以进 / 不可以进 plan"
- 跳过 AskUserQuestion 直接给最终决议

→ 全部意味着：**停下，回到 §3 / §5 重做**。

<IMPORTANT>
- 报告全部用中文。技术术语 / 文件路径 / 命令名保留英文。
- 章节名严格用【关键点提炼】【Issues】【Advisories】，不自创章节。
- AI 永不给 issues 分级，分级靠人勾选。
- 根据人的决策直接修改 spec 原文。
</IMPORTANT>
