# Claude Code Subagent 使用指南

## 概述

在 Claude Code 中，Subagent（子代理）是一种将复杂任务派发给独立上下文的机制。每个 subagent 拥有独立的会话历史（context window），执行完毕后只将结果回传给主会话（primary agent），从而避免大量工具调用和文件读取污染主上下文。

本指南基于 Claude Code 官方文档和 agent-skills 项目的编排实践，涵盖 subagent 的定义方式、触发机制、隔离选项以及常见编排模式。

---

## 定义方式

Claude Code 支持两种创建 subagent 的方式：

| 方式 | 需要预定义文件 | 适用场景 |
|:---|:---|:---|
| 预定义 Agent | 需要 `agents/<name>.md` | 复用性高的专用 persona（角色模板） |
| 动态 Task 启动 | **不需要任何文件** | 一次性、临时任务 |

### 方式一：预定义 Agent

在 `agents/` 目录下创建 Markdown 文件，通过 YAML frontmatter（前置元数据）定义 persona。

**文件位置优先级**（由高到低）：

1. `.claude/agents/` —— 项目级自定义
2. `~/.claude/agents/` —— 用户级全局自定义
3. 插件 `agents/` —— 插件内置（如 `refer/agent-skills/agents/`）

**示例**：`agents/code-reviewer.md`

```markdown
---
name: code-reviewer
description: Senior code reviewer that evaluates changes across five dimensions...
model: sonnet
tools: ["Read", "Bash", "WebFetch"]
---

You are a senior code reviewer...
```

**调用方式**：

```markdown
Agent tool + subagent_type: "code-reviewer"
```

### 方式二：动态 Task 启动

通过 Task 工具直接创建临时 subagent，无需预先准备文件。

**调用方式**：

```markdown
Task tool:
  subagent_type: "general-purpose"
  description: "Analyze conversation for unwanted behaviors"
  prompt: |
    You are analyzing a Claude Code conversation...
    Return findings as a structured list...
```

这种方式适合快速实验或调用次数不多的场景。

---

## Agent Frontmatter 字段

预定义 Agent 支持以下 frontmatter 字段：

| 字段 | 类型 | 说明 |
|:---|:---|:---|
| `name` | string | **必填**。Agent 标识符，用于 `subagent_type` 匹配 |
| `description` | string | **必填**。触发条件描述，支持 `<example>` 标签 |
| `model` | string | 继承父级或指定模型（`sonnet` / `opus` / `haiku`） |
| `tools` | array | 允许使用的工具白名单 |
| `disallowedTools` | array | 禁止使用的工具黑名单 |
| `maxTurns` | number | 最大对话轮数限制 |
| `skills` | array | 自动加载的 skill 列表 |
| `memory` | boolean | 是否继承会话记忆 |
| `isolation` | string | 隔离级别：`worktree` 提供 git 工作区隔离 |
| `color` | string | UI 标识颜色 |
| `initialPrompt` | string | 初始系统提示词 |

**插件 Agent 不支持的字段**（会被静默忽略）：

- `hooks`
- `mcpServers`
- `permissionMode`

如需使用这些字段，请将 Agent 文件复制到 `.claude/agents/` 或 `~/.claude/agents/`。

---

## 内置 Subagent 类型

在定义自定义 Agent 之前，先检查内置类型是否满足需求：

| 内置类型 | 用途 | 推荐场景 |
|:---|:---|:---|
| `Explore` | 只读代码库搜索与分析 | 大量文件检索、代码定位 |
| `Plan` | Plan 模式下的只读研究 | 规划阶段的上下文调研 |
| `general-purpose` | 多步骤探索与修改任务 | 一般性的独立工作单元 |

**建议**：不要重复定义这些内置类型的功能。将自定义 Agent 作为专业层（如 `code-reviewer`、`security-auditor`）叠加在它们之上。

---

## 隔离选项

Subagent 的隔离级别通过 frontmatter 控制：

| 隔离级别 | 配置方式 | 效果 |
|:---|:---|:---|
| 无隔离 | 不设置 `isolation` | Subagent 与 primary agent 共享文件系统 |
| 工作区隔离 | `isolation: worktree` | Subagent 获得独立的 git worktree（工作区），文件修改不影响主工作区 |

**使用 `isolation: worktree` 的场景**：

- 需要并行开发多个功能分支
- 担心 subagent 的文件操作污染主会话状态
- 执行有风险的操作（如批量重命名、格式转换）

**注意**：worktree 隔离仅影响文件系统，不影响 git 仓库本身。subagent 的提交仍会进入同一仓库。

---

## 编排模式

基于 agent-skills 项目的实践，推荐以下 5 种编排模式：

### 模式 1：直接调用（Direct Invocation）

单 persona、单视角、单产物。成本最低，是评估其他模式的基准。

```text
user → code-reviewer → report → user
```

**适用**：单一视角的审查任务，如代码审查、安全扫描。

### 模式 2：单 Persona 命令封装（Single-Persona Slash Command）

用 Command 封装常用的单 persona 调用，避免用户每次重复描述工作流。

```text
/review → code-reviewer (with skill) → report
```

**适用**：同一 persona 被反复调用且配置相同的场景。

**示例**：`/review`、`/test`、`/code-simplify`。

### 模式 3：并行 Fan-out 合并（Parallel Fan-out with Merge）

多个 persona 同时处理同一输入，各自产出独立报告，主 agent 合并为统一决策。

```text
              ┌→ code-reviewer    ┐
/ship → fan ──┼→ security-auditor ┤→ merge → go/no-go
              └→ test-engineer    ┘
```

**关键要求**：

- 所有 subagent 必须在**单次 assistant turn**（助手回合）内同时启动，才能实现并行
- 子任务必须真正独立（无顺序依赖、无共享可变状态）
- 合并步骤必须能在主 agent 剩余上下文中完成

**适用**：多维度审查后合并决策，如发布前的质量门禁。

### 模式 4：顺序管道（Sequential Pipeline）

用户按顺序运行 Command，每个步骤的产出作为下一步的输入。用户本身就是编排器。

```text
user: /spec → /plan → /build → /test → /review → /ship
```

**适用**：有依赖关系的流程，且人工判断能增加价值。

**为何不用自动化编排器**：LLM 编排器会在步骤间丢失细节、跳过人工检查点、双倍消耗 token。

### 模式 5：研究隔离（Research Isolation）

当任务需要读取大量材料但不应污染主上下文时，启动研究 subagent，仅返回摘要。

```text
main agent → research subagent (reads 50 files) → digest → main agent continues
```

**推荐**：使用内置 `Explore` subagent，它基于 Haiku 模型运行，无写入权限，专为只读搜索设计。

---

## 平台限制

Claude Code 强制执行的规则：

1. **Subagent 不能嵌套**：subagent 无法再启动其他 subagent
2. **Teammate 不能嵌套**：Agent Teams 模式下的 teammate 无法再创建自己的 team
3. **并行必须单 turn**：多个 subagent 并行需要在单次 assistant turn 内发出所有 Agent tool 调用

---

## 决策流程

```text
工作是单一视角、单一产物？
├── 是 → 直接调用。停止。
└── 否 → 相同组合会重复出现？
         ├── 否 → 直接调用，按需使用。停止。
         └── 是 → 子任务是否独立？
                  ├── 否 → 用户驱动顺序 Command（模式 4）。停止。
                  └── 是 → 并行 Fan-out（模式 3）。
                       对照检查清单验证。
                       任一检查不通过 → 回退到单 Persona Command（模式 2）。
```

---

## 示例：HTML 生成场景

以 `html-anything` skill 为例，展示如何选择编排模式：

**场景**：用户要求将 `data.csv` 转换为 HTML dashboard。

**分析**：

- 不是单一视角任务（涉及文件读取、prompt 选择、HTML 生成、验证）
- 但同一时刻只有一个文档需要处理，无并行需求
- 生成过程会读取 90+ 个 prompt 文件，严重污染主上下文

**选择**：**模式 5（研究隔离）的变体** —— 用 Task 工具启动临时 subagent 执行完整 workflow，仅返回生成的文件路径。

```markdown
Task tool:
  subagent_type: "general-purpose"
  description: "Generate HTML dashboard from CSV"
  prompt: |
    Read skills/html-anything/SKILL.md and follow its workflow.
    Input file: data.csv
    Output: generate output.html and return the file path.
    Do not explain the internal pipeline unless asked.
```

---

## 审校清单

- [ ] 是否需要复用？是 → 创建预定义 Agent；否 → 使用动态 Task
- [ ] 是否涉及文件系统风险？是 → 考虑 `isolation: worktree`
- [ ] 是否需要读取大量文件？是 → 考虑内置 `Explore` subagent
- [ ] 是否需要多个 persona 同时工作？是 → 确保单 turn 内并行启动
- [ ] 子任务是否真正独立？否 → 回退到顺序管道或单 persona
