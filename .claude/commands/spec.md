---
description: Start spec-driven development — explore context, clarify requirements, prepare workspace, then write spec
---

## Phase 1: Explore and Clarify

Begin by understanding what the user wants to build.

Invoke the **explore-then-ask** skill to ask clarifying questions one at a time (in Chinese) about:

1. The objective and target users
2. Core features and acceptance criteria
3. Tech stack preferences and constraints
4. Known boundaries (what to always do, ask first about, and never do)

Continue through explore-then-ask's full dialogue flow: surface assumptions, propose 2-3 approaches with trade-offs, present design sections, and get user approval.

## Phase 2: Prepare Workspace

Ask the user to choose a workspace strategy:

> 这个需求需要隔离开发环境吗？
> 1. 创建 git worktree（适合较大改动，完全隔离目录）
> 2. 创建 feature branch（适合常规改动，轻量分支）
> 3. 直接基于当前分支（适合极小改动，如配置调整、单函数修改）

根据选择执行：

- **worktree**: derive kebab-case `topic`, then `git worktree add .claude/worktrees/${topic}`
- **feature branch**: derive kebab-case `topic`, then `git checkout -b feat/${topic}`
- **current branch**: no action

## Phase 3: Structured Spec

Invoke the **spec-driven-development** skill to generate a structured spec covering all six core areas: objective, commands, project structure, code style, testing strategy, and boundaries.

<IMPORTANT>
- Write the spec content in Chinese. Keep technical terms, code identifiers, file paths, and command names in English.
- Save the spec to `docs/ys-powers/specs/YYYY-MM-DD-<feature-name>-design.md` where `<feature-name>` is a kebab-case short name derived from the spec title.
- If the directory does not exist, create it first.
- Confirm the file path with the user before saving.
</IMPORTANT>

## Phase 4: HTML Preview

After the spec is saved, automatically convert it to an HTML page for easier reading and sharing.

Spawn the `html-generator` subagent using the Agent tool:

```
Agent tool:
  subagent_type: "html-generator"
  description: "Convert spec to HTML preview"
  prompt: |
    Input: <spec-file-path>
    Input type: file
    Working directory: <current-directory>
    Generate HTML following skills/html-anything/SKILL.md.
    Apply the Output Path Rule and return the result in the specified output format.
```

Wait for the subagent to complete and return its output.

### Browser Open

After receiving the file path from the subagent:

1. Convert the absolute path to a `file://` URL
2. Use the Chrome DevTools MCP to navigate to that URL
3. The page opens for the user to review visually

### Response to User

Present the result in Chinese:

```markdown
**Spec 已完成**

- Spec 路径：`<spec-file-path>`
- HTML 预览：`<html-file-path>`

已在浏览器中打开 HTML 预览版。
如需调整 spec 内容，直接描述修改需求。
```

### Rules

1. Skip HTML preview only if the user explicitly says "不需要 HTML 预览" or "no preview".
2. Always delegate HTML generation to the `html-generator` subagent. Do not build HTML directly in the primary agent.
3. Pass the exact spec file path to the subagent without modification.
