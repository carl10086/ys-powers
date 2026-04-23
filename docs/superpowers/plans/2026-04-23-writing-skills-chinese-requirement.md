# Writing-Skills 中文硬约束实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 `skills/writing-skills/SKILL.md` 中增加 Language Requirement 硬约束，要求所有新 skill 用中文编写。

**架构：** 仅在 Overview 节后插入一小节，零副作用，不改动其他逻辑。

**技术栈：** Markdown，Git

**必须遵守的规则：** 参见 `.claude/rules/code.md` —— 只做最小改动，不动相邻代码，保持现有风格。

---

### Task 1: 插入 Language Requirement 节

**文件：**
- 修改：`skills/writing-skills/SKILL.md:21-22`（在 `## Overview` 结束和 `## What is a Skill?` 之间插入）

- [ ] **Step 1: 定位插入点**

读取 `skills/writing-skills/SKILL.md`，确认 `## Overview` 结束于第21行，`## What is a Skill?` 始于第22行。

- [ ] **Step 2: 插入 Language Requirement**

在第21行后插入以下内容：

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

- [ ] **Step 3: 验证插入结果**

运行：
```bash
grep -n "Language Requirement" skills/writing-skills/SKILL.md
grep -n "<IMPORTANT>" skills/writing-skills/SKILL.md
```

预期输出包含 `Language Requirement` 和 `<IMPORTANT>` 的行号。

- [ ] **Step 4: 检查上下文完整性**

运行：
```bash
sed -n '18,45p' skills/writing-skills/SKILL.md
```

确认：
- `## Overview` 仍存在且未改动
- 新插入的 `## Language Requirement` 位于 `## Overview` 之后
- `## What is a Skill?` 紧随其后
- Markdown 标题层级正确（都是 `##`）

- [ ] **Step 5: Commit**

```bash
git add skills/writing-skills/SKILL.md
git commit -m "feat(skills): 增加 Language Requirement 硬约束，要求新 skill 用中文编写

在 writing-skills 的 SKILL.md Overview 后插入 <IMPORTANT> 块，
强制所有通过本 skill 创建的新 skill 使用简体中文。

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

---

## Self-Review 结果

**1. Spec 覆盖：** 设计文档中的唯一要求（插入 Language Requirement 节）由 Task 1 完全覆盖。

**2. Placeholder 扫描：** 无 TBD、无 TODO、所有代码块完整、有 exact 文件路径。

**3. 类型一致性：** 不涉及函数/类型，仅 Markdown 文本插入，无一致性风险。
