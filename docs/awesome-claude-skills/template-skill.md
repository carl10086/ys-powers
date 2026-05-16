# template-skill

## 定位

Claude Skill 的标准模板，提供最小可运行的目录结构和文件骨架，作为创建新 Skill 的起点。

## 触发时机

- 从零开始创建新 Claude Skill 需要参考标准结构时
- 快速搭建 Skill 原型验证想法时
- 教学演示 Skill 的基本组成部分时
- **不适用**：已有成熟 Skill 需要修改，或使用 `skill-creator` / `skill-share` 自动生成时

## 核心能力

1. **最小结构**：提供标准目录布局和必需的 YAML frontmatter
2. **快速启动**：复制模板后即可开始编写 Skill 逻辑
3. **规范示例**：展示正确的 `name` 和 `description` 格式

## 目录结构

```
template-skill/
└── SKILL.md          # 必需：包含 YAML frontmatter + Markdown 指令
```

## 模板内容

```markdown
---
name: template-skill
description: Replace with description of the skill and when Claude should use it.
---

# Insert instructions below
```

## 与 ys-powers 的关联

- **与 skill-creator 的关系**：`template-skill` 是「最小模板」，`skill-creator` 是「完整开发指南」。前者适合快速启动，后者适合深度设计
- **借鉴价值**：无特别独特的设计，但其极简结构可作为 ys-powers 内部快速创建 Skill 的脚手架
- **搬运建议**：低价值。模板本身过于简单，建议直接使用 `skill-creator` 的能力

## 元信息

- 来源：`refer/awesome-claude-skills/template-skill/SKILL.md`
- 维护者：Composio / 社区
- 许可证：Apache 2.0
