# writing-skills

**定位**：把 TDD 的红/绿/重构循环应用到 agent skill 的创作与验证上。

**触发条件**：新建 skill、修改现有 skill、部署前验证 skill 是否按预期工作。

---

## 核心主张

> **Creating skills IS Test-Driven Development applied to process documentation.**

- 先让 agent 在没有 skill 的情况下失败（RED），观察它的真实行为与借口。
- 再写刚好解决这些失败的 skill（GREEN）。
- 继续找新借口并堵住（REFACTOR）。

## Skill 是什么

- **是**：可复用的技术、模式、工具、参考指南。
- **不是**：一次性解决某个问题的叙事。

## Skill 类型

| 类型 | 例子 | 测试重点 |
|---|---|---|
| **Technique** | TDD、条件等待 | 能在真实场景正确应用技术 |
| **Pattern** | 降低复杂度、信息隐藏 | 能识别何时适用/不适用 |
| **Reference** | API 文档、命令参考 | 能检索并正确应用信息 |

## SKILL.md 结构

```markdown
---
name: skill-name
description: Use when [具体触发条件与症状]
---

# Skill Name

## Overview
## When to Use
## Core Pattern
## Quick Reference
## Implementation
## Common Mistakes
```

## 关键规则

- **description 只写触发条件**，不写流程总结。agent 可能只看 description 就跳过正文。
- **名字用主动语态、动名词开头**，如 `creating-skills`、`condition-based-waiting`。
- **Token 效率**：getting-started <150 词，常用 <200 词，其他 <500 词。
- **交叉引用用技能名**，不要用 `@` 强制加载。

## Iron Law

```
NO SKILL WITHOUT A FAILING TEST FIRST
```

新建或修改 skill 都必须先测试，无例外。

## 防弹设计：对抗合理化

agent 在压力下会找借口绕过规则。对应手段：

- **显式关闭每个漏洞**：不只说规则，还要禁止具体 workaround。
- **精神即文字**：违反 letter 就是违反 spirit。
- **合理化表格**：记录常见借口与事实。
- **Red Flags 列表**：让 agent 自我识别正在找借口。

## RED-GREEN-REFACTOR

- **RED**：无 skill 跑压力场景，记录失败与借口。
- **GREEN**：写最小 skill，让同样场景通过。
- **REFACTOR**：发现新借口 → 加 counter → 重测。

## 压力测试

好场景同时叠加 3+ 种压力：时间、沉没成本、权威、经济、疲惫、社交、“务实”。用 A/B/C 强制选择，不给“我先问问”的逃避。

## 部署检查清单

每个 skill 部署前必须完成 RED/GREEN/REFACTOR 阶段的检查项，包括 frontmatter、关键词、overview、baseline 测试、pressure 测试、rationalization 表、red flags 等。

详见 `refer/superpowers/skills/writing-skills/testing-skills-with-subagents.md`。
