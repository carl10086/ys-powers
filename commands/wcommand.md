---
description: Use when creating or materially editing a slash command with a focused workflow and predictable execution path
argument-hint: [command-name-or-idea]
disable-model-invocation: true
---

# /wcommand

写 command。Command 是 **entrypoint**：它应该把一个具体 workflow 拉直，而不是复制一整套方法论。

## Flow

1. 明确 command 类型：
   - **Workflow**：串起固定步骤，例如 `/gc`、`/ship`。
   - **Discipline**：防止 agent 绕过流程，例如 authoring gate。
   - **Utility**：包装工具或脚本，例如 HTML / docs 生成。
2. 读取 `writing-great-skills`，用它决定 description、steps、completion criterion、split、prune。
3. 查已有 `commands/*.md`：有重叠就扩展或替换，不新增同义 command。
4. 只在 trigger / scope / arguments 无法从 repo 判断时，按 `explore-then-ask` 一次问一个问题；否则直接写。
5. 保存到 `commands/<kebab-case-name>.md`。
6. Verify：frontmatter 合法；description 只写 trigger；body 中文；technical identifiers 保持英文；每个 step 可执行；最后有可检查完成条件；没有复制 skill/reference 正文。

## Frontmatter

Claude Code commands 常用字段：

- `description`：必填；写触发场景，不写流程总结。
- `argument-hint`：可选；展示参数形状。
- `allowed-tools`：可选；需要约束工具面时才写。
- `disable-model-invocation`：可选；纯手动 command 才设为 `true`。

## Trial run

新 command 至少做一次 lightweight trial：用一个 primary scenario 走完整流程，确认不会卡住、不会调用不存在的 skill/tool/path。Discipline command 再补一个 boundary scenario。
