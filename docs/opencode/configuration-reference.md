# OpenCode 配置参考

> 信息来源：[opencode.ai/docs/zh-cn](https://opencode.ai/docs/zh-cn)
> 适用版本：截至 2026/05/16 的文档版本
> 目标读者：已熟悉 Claude Code 配置、希望了解 OpenCode 对应机制的开发者

---

## 1. 概述

OpenCode 是一款 AI 编码助手，其配置机制与 Claude Code 有较高的相似度，同时提供了多层级合并和 Claude Code 兼容模式。

**核心特点：**

- 使用 JSON 作为统一配置格式
- 支持多层级配置合并（远程 → 全局 → 项目 → 环境变量）
- 原生兼容 Claude Code 的 `.claude/` 目录结构
- 支持 skills、commands、rules、agents 四类扩展能力

---

## 2. 配置系统

### 2.1 配置文件格式

OpenCode 使用 JSON 配置文件，Schema 地址为：

```json
{
  "$schema": "https://opencode.ai/config.json"
}
```

### 2.2 配置加载优先级（从低到高）

后面的配置会覆盖前面配置的冲突键，非冲突键则会合并保留：

| 优先级 | 配置源 | 说明 |
|--------|--------|------|
| 1 | `.well-known/opencode` | 远程组织默认配置（通过身份验证提供商自动获取） |
| 2 | `~/.config/opencode/opencode.json` | 全局用户配置 |
| 3 | `OPENCODE_CONFIG_CONTENT` | 环境变量，直接内联 JSON 内容 |
| 4 | 项目配置 | 当前目录或向上遍历到最近的 Git 工作树根目录 |
| 5 | 自定义配置 | 通过 `OPENCODE_CONFIG_DIR` 指定的额外目录 |

**关键行为：** 配置是**合并**而非替换。例如组织配置默认禁用了某个 MCP 服务器，用户仍可在全局配置中显式启用它。

### 2.3 项目配置位置

OpenCode 启动时会在以下位置查找项目级配置：

- 当前工作目录
- 向上遍历目录树，直到到达 Git 工作树根目录

项目配置文件可安全提交到 Git，与全局配置使用相同的 Schema。

### 2.4 常用配置项示例

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-sonnet-4-5",
  "title_model": "anthropic/claude-haiku-4-5",
  "timeout": 300000,
  "scroll_acceleration": {
    "enabled": true
  },
  "agents": {
    "build": {
      "model": "anthropic/claude-sonnet-4-20250514",
      "temperature": 0
    }
  }
}
```

---

## 3. Skills（技能）

### 3.1 文件格式

每个 skill 是一个目录，内含 `SKILL.md` 文件：

```
<skill-name>/
└── SKILL.md
```

`SKILL.md` 必须以 YAML frontmatter 开头，正文为 Markdown：

```markdown
---
name: git-release
description: Create consistent releases and changelogs
---

# Git Release

Use this when you are preparing a tagged release.

## Steps

1. Draft release notes from merged PRs
2. Propose a version bump
3. Provide a copy-pasteable git tag command
```

**命名规则：** 仅包含小写字母和数字，可用单个连字符分隔。正则表达式为 `^[a-z0-9]+(-[a-z0-9]+)*$`。

### 3.2 搜索路径

OpenCode 按以下顺序查找 skills：

**项目本地路径：**

1. `.claude/skills/<name>/SKILL.md`
2. `.agents/skills/<name>/SKILL.md`
3. `.opencode/skills/<name>/SKILL.md`

**全局路径：**

4. `~/.config/opencode/skills/<name>/SKILL.md`
5. `~/.claude/skills/<name>/SKILL.md`
6. `~/.agents/skills/<name>/SKILL.md`

项目本地优先于全局。OpenCode 会从当前工作目录向上遍历到 Git 工作树根目录。

### 3.3 权限控制

可在代理配置中通过 `available_skills` 限制可访问的 skills：

```json
{
  "agents": {
    "plan": {
      "available_skills": ["explore", "debug"]
    }
  }
}
```

为不需要使用 skills 的代理完全禁用：

```json
{
  "agents": {
    "review": {
      "available_skills": []
    }
  }
}
```

---

## 4. Commands（命令）

### 4.1 文件格式

Commands 使用 Markdown 文件定义，文件名即为命令名：

```
.opencode/commands/
├── test.md
├── create-component.md
└── review-changes.md
```

**文件结构：**

```markdown
---
model: anthropic/claude-3-5-sonnet-20241022
description: Run tests with coverage
---

Run the full test suite with coverage report and show any failures.
Focus on the failing tests and suggest fixes.
```

Frontmatter 定义命令属性，正文内容成为发送给 LLM 的提示词模板。

### 4.2 搜索路径

- 项目本地：`.opencode/commands/<name>.md`
- 全局：`~/.config/opencode/commands/<name>.md`、`~/.opencode/commands/<name>.md`

**与 Claude Code 的兼容性：**

OpenCode **不读取** `.claude/commands/`。若已有 Claude Code 的 commands，可通过以下方式复用：

```bash
# 方案 1：软连接（推荐，保持单份源码）
ln -s ~/.claude/commands ~/.opencode/commands

# 方案 2：复制（独立管理）
cp -r ~/.claude/commands/* ~/.opencode/commands/
```

### 4.3 占位符语法

Commands 支持在提示词中使用占位符：

| 占位符 | 说明 |
|--------|------|
| `$ARGUMENTS` | 用户输入的所有参数 |
| `$1`, `$2`, `$3` | 第 N 个参数 |

**示例：**

```markdown
---
description: Create a new component
---

Create a new React component named $ARGUMENTS with TypeScript support.
Include proper typing and basic structure.
```

```markdown
---
description: Create a new file with content
---

Create a file named $1 in the directory $2 with the following content: $3
```

### 4.4 系统命令集成

Command 内容中可嵌入 shell 命令，其输出会成为提示词的一部分：

```markdown
---
description: Review recent changes
---

Review these changes and suggest any improvements:

`git log --oneline -10`
```

命令在项目根目录运行，输出结果自动注入上下文。

### 4.5 覆盖内置命令

自定义命令与内置命令同名时会覆盖内置命令。例如定义 `.opencode/commands/test.md` 会覆盖默认的 `test` 命令。

---

## 5. Rules（规则）

### 5.1 核心文件

OpenCode 使用 `AGENTS.md` 提供自定义指令，类似于 Cursor 的 Rules 功能。文件内容会被纳入 LLM 上下文，用于针对特定项目定制行为。

### 5.2 搜索顺序

OpenCode 按以下顺序查找规则文件，**第一个匹配的文件生效**：

**项目级（仅在项目目录及其子目录工作时生效）：**

1. `AGENTS.md`（项目根目录）
2. `.opencode/AGENTS.md`
3. `CLAUDE.md`（项目根目录，源码 `defaultContextPaths` 确认）
4. `CLAUDE.local.md`（项目根目录）
5. `.claude/CLAUDE.md`（官方文档提及）
6. `.claude/AGENTS.md`（官方文档提及）

**全局级（应用于所有会话）：**

7. `~/.config/opencode/AGENTS.md`
8. `~/.claude/CLAUDE.md`
9. `~/.claude/AGENTS.md`

**注意：** 源码（归档版本）中的 `defaultContextPaths` 只包含项目根目录的 `CLAUDE.md`，不含 `.claude/CLAUDE.md`。官方文档描述的路径可能对应更新的闭源版本。

### 5.3 Claude Code 兼容性

OpenCode 原生支持 Claude Code 的 `CLAUDE.md` 和 `.claude/` 目录约定：

- `.claude/AGENTS.md`
- `.claude/CLAUDE.md`
- `.claude/skills/*/SKILL.md`

可通过环境变量禁用兼容性：

| 环境变量 | 作用 |
|----------|------|
| `OPENCODE_DISABLE_CLAUDE_CODE` | 完全禁用所有 `.claude` 支持 |
| `OPENCODE_DISABLE_CLAUDE_CODE_PROMPT` | 仅禁用 `~/.claude/CLAUDE.md` |
| `OPENCODE_DISABLE_CLAUDE_CODE_SKILLS` | 仅禁用 `.claude/skills` |

### 5.4 自动生成规则

运行以下命令可自动扫描项目并生成 `AGENTS.md`：

```bash
$ opencode rules
```

该命令会分析项目结构和内容，生成初始规则文件。如果已存在规则文件，则会在其基础上补充。

### 5.5 外部文件引用

OpenCode 支持在 `AGENTS.md` 中引用外部文件，但**不直接支持文件路径引用**。可通过以下方式实现：

**方式一：配置中指定指令文件**

```json
{
  "agents": {
    "instructions": [
      "docs/guidelines.md",
      ".cursor/rules/*.md"
    ]
  }
}
```

支持 glob 模式和远程 URL：

```json
{
  "agents": {
    "instructions": [
      "https://raw.githubusercontent.com/my-org/shared-rules/main/style.md"
    ]
  }
}
```

**方式二：在 AGENTS.md 中指示代理懒加载**

```markdown
# TypeScript Project Rules

## External File Loading

CRITICAL: When you encounter a file reference (e.g., @rules/general.md), use your Read tool to load it on a need-to-know basis.

## Development Guidelines

For TypeScript code style: @docs/typescript-guidelines.md
For React patterns: @docs/react-patterns.md
```

---

## 6. Agents（代理）

### 6.1 内置代理

OpenCode 内置两类代理：

**主代理（用户直接交互）：**

| 代理 | 用途 | 工具权限 |
|------|------|----------|
| Build | 标准开发工作 | 完整工具访问 |
| Plan | 规划和分析，防止意外修改 | 受限权限 |

**子代理（主代理调用或用户直接调用）：**

| 代理 | 用途 | 特点 |
|------|------|------|
| General | 研究复杂问题、执行多步骤任务 | 完整工具访问（除 todo 外） |
| Explore | 快速只读代码库探索 | 无法修改文件 |
| External | 外部文档和依赖研究 | 只读，可克隆依赖仓库 |
| Context Compaction | 长上下文压缩 | 自动运行，不可选择 |
| Title Generation | 生成会话标题 | 自动运行，不可选择 |
| Summary | 创建会话摘要 | 自动运行，不可选择 |

**会话导航快捷键：**

- `session_child_cycle_forward`：向前循环会话（父 → 子1 → 子2 → ... → 父）
- `session_child_cycle_reverse`：向后循环会话

### 6.2 自定义代理

可通过两种方式自定义代理：JSON 配置或 Markdown 文件。

**JSON 配置方式：**

```json
{
  "agents": {
    "review": {
      "name": "Code Review",
      "description": "Reviews code for best practices and potential issues",
      "model": "anthropic/claude-sonnet-4-20250514",
      "temperature": 0,
      "system_prompt": "You are a code reviewer. Focus on security, performance, and maintainability.",
      "max_iterations": 10,
      "tools": {
        "Read": false,
        "Write": false
      }
    }
  }
}
```

**Markdown 文件方式：**

在 `~/.config/opencode/agents/` 目录下创建 Markdown 文件：

> **Claude Code 兼容性提示：** 官方文档和开源源码均未明确记载 `.claude/agents/` 的兼容性，但有用户实测将 agents 文件置于 `~/.claude/agents/` 亦可生效。如需确保稳定可用，建议使用 `~/.config/opencode/agents/`。

```markdown
---
name: Code Review
description: Reviews code for quality and best practices
model: anthropic/claude-sonnet-4-20250514
temperature: 0
max_iterations: 10
---

You are in code review mode. Focus on:

- Code quality and best practices
- Potential bugs and edge cases
- Performance implications
- Security considerations

Provide constructive feedback without making direct changes.
```

文件名即为代理名称，如 `review.md`。

### 6.3 代理配置项说明

| 配置项 | 类型 | 说明 |
|--------|------|------|
| `name` | string | 代理显示名称 |
| `description` | string | 功能描述，在 TUI 中展示 |
| `model` | string | 模型 ID，格式为 `provider/model-name` |
| `temperature` | number | 控制随机性，0 为确定性，1 为创造性 |
| `system_prompt` | string | 系统提示词，可使用 `{file:./prompts.txt}` 引用外部文件 |
| `max_iterations` | number | 最大代理迭代次数，达到限制后代理会返回摘要 |
| `tools` | object | 工具访问权限，可单独禁用特定工具 |
| `hide` | boolean | 在自动补全菜单中隐藏，仅通过 Task 工具由其他代理调用 |
| `tasks` | array | 控制该代理可通过 Task 工具调用哪些子代理，支持 glob 模式 |
| `orchestrator` | boolean | 允许从自动补全菜单直接调用任何子代理 |

**模型 ID 格式：** 使用 `provider/model-name`，例如：

- `anthropic/claude-sonnet-4-5`
- `anthropic/claude-haiku-4-5`
- `opencode/gpt-5.1-codex`

**工具权限控制示例：**

```json
{
  "agents": {
    "plan": {
      "tools": {
        "Write": false,
        "Bash": false
      }
    }
  }
}
```

使用通配符控制 MCP 工具：

```json
{
  "agents": {
    "review": {
      "tools": {
        "mcp_*": false
      }
    }
  }
}
```

### 6.4 使用方式

**主代理切换：**

在 TUI 中使用快捷键循环切换主代理（Build / Plan）。主代理处理你的主要对话，工具访问通过权限配置。

**子代理调用：**

子代理有两种调用方式：

1. **主代理自动调用**：主代理在执行任务时，根据需要调用子代理完成特定工作
2. **用户直接调用**：在消息输入框中使用 `@agent名称` 提及代理名称，例如：

```
@general help me search for this function
```

**会话导航：**

当子代理创建自己的子会话时，使用以下快捷键在父会话和所有子会话之间导航：

- `session_child_cycle_forward`：向前循环（父 → 子1 → 子2 → ... → 父）
- `session_child_cycle_reverse`：向后循环（父 ← 子1 ← 子2 ← ... ← 父）

**子代理权限控制：**

通过 `tasks` 字段控制代理可调用哪些子代理：

```json
{
  "agents": {
    "build": {
      "tasks": ["explore", "general", "debug-*"]
    }
  }
}
```

当 `tasks` 为空数组时，该代理无法调用任何子代理。使用 `orchestrator: true` 可允许代理绕过 `tasks` 限制，直接从自动补全菜单调用子代理。

## 7. Hooks（钩子）

OpenCode **目前没有** Claude Code 式的 hooks 机制。

经核查：

- 官方文档中无 hooks 相关页面
- 开源源码（已归档）中无 hooks 系统实现
- 配置文件中无类似 `settings.json` 中的 `hooks` 字段

**这意味着：**

- Claude Code 的 `UserPromptSubmit`、`SessionStart` 等 hooks **无法在 OpenCode 中直接复用**
- 若需实现类似功能（如会话开始时自动加载上下文），需借助 OpenCode 的 `agents` 配置或外部脚本间接实现

---

## 8. 与 Claude Code 的兼容性对照

| 能力 | Claude Code | OpenCode | 兼容性说明 |
|------|-------------|----------|------------|
| 配置文件 | `settings.json` / `settings.local.json` | `opencode.json` | 格式不同，需手动迁移 |
| Skills 目录 | `.claude/skills/<name>/SKILL.md` | `.opencode/skills/<name>/SKILL.md` | **原生兼容**，OpenCode 主动读取 `.claude/skills` |
| Commands 目录 | `.claude/commands/<name>.md` | `.opencode/commands/<name>.md` | **不兼容**，需软连接或复制 |
| Rules 文件 | `.claude/CLAUDE.md` | `.opencode/AGENTS.md` | **部分兼容**，项目根目录 `CLAUDE.md` 可直接读取；`.claude/CLAUDE.md` 兼容性视版本而定 |
| Agents 目录 | 无内置 agents 配置 | `~/.config/opencode/agents/` | **部分兼容**，`.claude/agents/` 未在文档/源码中证实，但有用户实测生效 |
| Hooks | `settings.json` 中的 hooks 字段 | 无 | **不兼容**，OpenCode 目前无 hooks 机制 |
| 全局配置目录 | `~/.claude/` | `~/.config/opencode/` | 路径不同 |

**关键结论：**

- **零改动复用：** Skills（`.claude/skills/`）
- **软连接解决：** Commands（`ln -s ~/.claude/commands ~/.opencode/commands`）
- **直接生效：** Rules（项目根目录 `CLAUDE.md`）
- **OpenCode 特有：** Agents、Hooks（Claude Code 无对应机制，Hooks 目前不存在）

---

## 9. 快速迁移检查清单

将 ys-powers 能力迁移到 OpenCode 项目：

- [ ] **Skills**（零改动）：确认 `.claude/skills/` 下的 `SKILL.md` 符合命名规范（小写+数字+连字符），OpenCode 会自动读取
- [ ] **Commands**（需软连接）：`ln -s ~/.claude/commands ~/.opencode/commands`
- [ ] **Rules**（直接生效）：项目根目录的 `CLAUDE.md` 会自动读取；全局规则放 `~/.config/opencode/AGENTS.md`
- [ ] **Agents**（建议放标准路径）：在 `~/.config/opencode/agents/` 中创建 Markdown 文件；如放 `~/.claude/agents/` 请自行验证可用性
- [ ] **Hooks**（无法迁移）：OpenCode 目前无 hooks 机制，相关功能需通过 agents 或外部脚本间接实现
- [ ] **配置**：创建 `~/.config/opencode/opencode.json` 设置模型、超时等偏好
- [ ] **权限**：如需限制代理工具访问，在配置中设置 `agents.*.tools` 字段

---

## 10. 参考链接

- [OpenCode 官方文档](https://opencode.ai/docs/zh-cn)
- [配置 Schema](https://opencode.ai/config.json)
- [Skills 文档](https://opencode.ai/docs/zh-cn/skills)
- [Commands 文档](https://opencode.ai/docs/zh-cn/commands)
- [Rules 文档](https://opencode.ai/docs/zh-cn/rules)
- [Agents 文档](https://opencode.ai/docs/zh-cn/agents)
