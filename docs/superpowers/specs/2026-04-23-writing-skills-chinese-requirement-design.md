# Writing-Skills 中文要求设计文档

## 背景

`writing-skills` 是指导 Claude 创建新 skill 的元技能。当前所有由该 skill 生成的新 skill 默认使用英文编写，不符合项目对中文技能库的要求。

## 目标

在 `writing-skills` 中增加一条硬性规则：**所有通过本 skill 创建的新 skill，内容必须用简体中文编写**。

## 设计

### 改动范围

仅修改 `skills/writing-skills/SKILL.md`，不改动其他文件。

### 具体改动

在 `## Overview` 后新增一节 `## Language Requirement`：

```markdown
## Language Requirement

<IMPORTANT>
ALL new skills created through this skill MUST be written in **Chinese (简体中文)**.

This includes:
- Overview, usage conditions, core patterns, all explanations
- Code comments and example descriptions
- Flowchart labels and diagram text
- Error examples and correct examples

What MAY remain in English:
- Technical terms (API names, library names, CLI commands)
- File paths and directory names
- Code identifiers (variable names, function names)

A skill that violates this rule is considered incomplete.
</IMPORTANT>
```

### 不做改动的部分

- `~/.claude/skills` 路径引用：保持现状，用户自行 move 到项目目录
- `anthropic-best-practices.md`、`testing-skills-with-subagents.md` 等配套文件
- 现有测试场景和流程图

## 验收标准

- [ ] `SKILL.md` 中新增 Language Requirement 节
- [ ] 位置在 Overview 之后，When to Use 之前
- [ ] 使用 `<IMPORTANT>` 标签包裹，形成硬约束
- [ ] 明确区分"必须中文"和"可保留英文"的内容边界

## 影响评估

- **风险**：极低。仅增加一条约束声明，不改动现有流程。
- **向后兼容**：不影响已有 skill 的使用。
- **token 开销**：增加约 80 tokens，可忽略。
