# using-superpowers

**定位**：会话启动时的元 skill，强制 agent 在行动前先查找并调用相关 skill。

**触发条件**：任何对话开始时；只要某个 skill 有 1% 可能适用，就必须先调用它。

---

## 指令优先级

1. **用户显式指令**（CLAUDE.md、GEMINI.md、AGENTS.md、直接请求）— 最高。
2. **Superpowers skills** — 覆盖默认系统行为。
3. **默认系统 prompt** — 最低。

## 核心规则

> **If you think there is even a 1% chance a skill might apply, you ABSOLUTELY MUST invoke the skill.**

Skill 必须在任何回应或行动**之前**调用，包括澄清问题、探索代码库、读文件。

## 如何加载 skill

- **Claude Code**：用 `Skill` 工具。
- **Codex**：原生加载。
- **Copilot CLI**：用 `skill` 工具。
- **Gemini CLI**：用 `activate_skill`。
- 其他平台参见 `using-superpowers/references/` 下对应工具文档。

**不要直接用文件工具读 SKILL.md**；要用平台机制激活 skill。

## Skill 优先级

多个 skill 可能适用时：

1. **Process skills 优先**（如 `brainstorming`、`systematic-debugging`）— 决定怎么做。
2. **Implementation skills 其次**（如具体技术 skill）— 指导执行。

例如：
- “Let's build X” → 先 `brainstorming`，再实现 skill。
- “Fix this bug” → 先 `systematic-debugging`，再领域 skill。

## Skill 类型

- **Rigid**（如 TDD、systematic-debugging）：严格遵循，不允许因地制宜。
- **Flexible**（如模式）：根据上下文调整原则。

Skill 自身会说明属于哪一类。

## 对 ys-powers 的启示

这是 Superpowers 的“启动器”：它把 skill 从可选参考变成强制工作流。如果在 ys-powers 里想让某些 skill 自动触发，需要类似的 bootstrap 机制（会话启动 hook 或 command 入口），而不是指望 agent 自己记得调用。
