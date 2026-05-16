# Global Install 路径兼容性审计报告

**审计日期**: 2026-05-14
**审计范围**: `skills/`, `commands/`, `agents/`, `hooks/` 全部文件
**审计目标**: 排查 global install（`~/.claude/`）后，因相对路径或硬编码路径导致的能力失效问题
**状态**: ✅ 已修复（分支 `feat/global_install`，提交至 `b839cb4`）

---

## 执行摘要

Global install 将 ys-powers 的内容复制到用户主目录的 `~/.claude/` 下。当 Claude Code 加载这些能力时，**当前工作目录（CWD）是用户的项目目录**，而非 ys-powers 仓库根目录。

因此：
- 任何假设 CWD 是 ys-powers 项目根目录的相对路径都会失效或指向错误位置
- 任何硬编码的绝对路径（如容器路径）会完全失效
- 使用 `$0`/`__file__` 自定位的脚本在 global install 后通常能正确工作

---

## 一、明确 Bug（Global Install 后必定失败）

### 1. `skills/idea-refine/SKILL.md` — 硬编码容器绝对路径

| 属性 | 值 |
|------|-----|
| **文件** | `skills/idea-refine/SKILL.md` |
| **行号** | 22 |
| **问题代码** | `bash /mnt/skills/user/idea-refine/scripts/idea-refine.sh` |
| **影响** | 用户在任何项目运行该 skill 时，Claude Code 尝试执行此路径，文件不存在 |
| **根因** | 该路径是容器环境（`/mnt/skills/user/`）的硬编码绝对路径，global install 后 skill 位于 `~/.claude/skills/idea-refine/` |

**待决策修复方案**：
- **方案 A**：改为 `bash "$HOME/.claude/skills/idea-refine/scripts/idea-refine.sh"`（global install 后确定存在，但 local install 时可能不存在）
- **方案 B**：改为 `bash ./scripts/idea-refine.sh`（假设 Claude Code 执行 skill 时 CWD 是 skill 目录）
- **方案 C**：移除引用，改为内联 `mkdir -p docs/ys-powers/ideas`（不依赖外部脚本）
- **方案 D**：安装时替换（`install.py` 复制文件时将 `/mnt/skills/user/...` 替换为实际路径）

---

## 二、潜在风险（取决于 Claude Code 路径解析行为）

以下路径在 global install 后**可能**失效，取决于 Claude Code 的 skill/agent 加载器如何解析相对路径：

**假设 A**：Claude Code 从 skill/agent 文件所在目录解析相对路径 → 这些路径在 global install 后**正确**
**假设 B**：Claude Code 从用户项目 CWD 解析相对路径 → 这些路径在 global install 后**失效**

> **当前状态**：未验证 Claude Code 的具体行为，标记为待验证。

### 2. `agents/html-generator.md` — Agent 引用 Skill 和 Prompts

| 属性 | 值 |
|------|-----|
| **文件** | `agents/html-generator.md` |
| **行号** | 34-35 |
| **问题代码** | `Load skills/html-anything/SKILL.md`<br>`Read prompts/styles/_design.md, prompts/styles/catalog.json` |
| **影响** | Agent 被调用时，Claude Code 尝试读取这些文件。如果按 CWD 解析，在用户项目下找不到 `skills/` 和 `prompts/` 目录 |
| **风险场景** | 用户运行 `/html` 命令时，agent 无法加载 style guidance，导致 HTML 生成缺少设计系统约束 |

**待决策修复方案**：
- **方案 A**：信任 Claude Code 从 agent/skill 目录解析（与 `html-anything` 原项目保持一致，无需修改）
- **方案 B**：安装时替换路径（将 `skills/html-anything/SKILL.md` 替换为 `${CLAUDE_PLUGIN_ROOT}/skills/html-anything/SKILL.md` 或绝对路径）
- **方案 C**：重构为 skill 名称调用（参考 `agent-skills`，不直接引用文件路径，而是通过 Claude Code 机制调用 `skill: html-anything`）
- **方案 D**：内容内联（将引用的 skill/prompts 内容直接复制到 agent 文件中，消除外部依赖）

### 3. `skills/html-anything/SKILL.md` — Skill 内引用 Prompts

| 属性 | 值 |
|------|-----|
| **文件** | `skills/html-anything/SKILL.md` |
| **行号** | 369, 426, 451 |
| **问题代码** | `Read ./prompts/styles/_design.md`<br>`prompts/sources/`<br>`prompts/styles/` |
| **影响** | Skill 的 instructions 包含相对路径引用。如果 Claude Code 按 CWD 解析，找不到 prompts 目录 |

**待决策修复方案**：
- **方案 A**：信任 Claude Code 从 skill 目录解析（`html-anything` 原项目的设计方式）
- **方案 B**：安装时替换（将 `./prompts/` 替换为 `${CLAUDE_PLUGIN_ROOT}/skills/html-anything/prompts/`）
- **方案 C**：内容内联（将 prompts 内容合并到 SKILL.md 中）

---

## 三、参考项目策略对比

| 项目 | 核心策略 | 适用场景 |
|------|---------|---------|
| **superpowers** | `$0` 自定位 | Hooks、可执行脚本 |
| **agent-skills** | 环境变量 `${CLAUDE_PLUGIN_ROOT}` + skill 名称调用 | Hooks、skill 间调用 |
| **get-shit-done** | 安装时路径替换 + 泄漏检测 | 跨平台通用工具 |
| **html-anything**（原项目） | `__dirname` 运行时解析 + 相对路径 | 带可执行组件的 skill |

**关键洞察**：
- `superpowers` 和 `agent-skills` 都不在 skill/agent markdown 中硬编码文件路径
- `html-anything` 原项目使用 `./prompts/styles/...` 相对路径，说明作者预期 Claude Code 从 skill 目录解析
- `get-shit-done` 的安装时替换最全面，但复杂度最高，且对 markdown 文件的替换存在不可移植性问题

---

## 四、方案讨论记录

### 议题 1：安装时替换的可行性

**观点**：在 `install.py` 复制文件时，将相对路径替换为 `${CLAUDE_PLUGIN_ROOT}` 或绝对路径。

**反对理由**：
- 替换为绝对路径（如 `/Users/xxx/.claude/skills/...`）→ 不可移植到其他机器
- 替换为环境变量（如 `$HOME/.claude/skills/...`）→ Claude Code 解析 markdown 时不会展开 shell 变量
- 替换为 `${CLAUDE_PLUGIN_ROOT}` → Claude Code 只在 hooks 配置中保证识别此变量，skill/agent markdown 中不保证识别

**结论**：安装时替换对 hooks 可行（已在使用），对 skill/agent markdown **不可行**。

### 议题 2：保守策略 vs 主动修复

**保守策略（方案 C）**：
- 只修复 `/mnt/skills/user/...`（明确 bug）
- 其他路径引用保持现状（信任 `html-anything` 原项目的设计）
- 未来如发现问题，再系统性修复

**主动修复（方案 A/B）**：
- 对所有潜在风险点进行预防性修改
- 可能引入不必要的复杂度和维护负担

**待决策**：是否接受保守策略？

---

## 五、设计意图（非 Bug，在用户项目 CWD 下操作）

以下路径是 skill/command 的**预期行为**，它们故意在用户当前项目下创建或读取文件：

| 文件 | 路径 | 说明 |
|------|------|------|
| `skills/idea-refine/SKILL.md` | `docs/ideas/[idea-name].md` | 要求用户确认后保存 ideation 结果到用户项目 |
| `skills/idea-refine/SKILL.md` | `docs/ys-powers/ideas/[idea-name].md` | 同上，带组织前缀 |
| `skills/idea-refine/scripts/idea-refine.sh` | `docs/ys-powers/ideas` | 初始化脚本，在用户项目 CWD 下创建目录 |
| `skills/brainstorming/SKILL.md` | `docs/ys-powers/specs/...` | 保存 brainstorming 输出到用户项目 |
| `skills/documentation-and-adrs/SKILL.md` | `docs/decisions/` | 保存 ADR 到用户项目 |
| `commands/plan.md` | `docs/ys-powers/plans/...` | 保存计划到用户项目 |
| `commands/spec.md` | `docs/ys-powers/specs/...` | 保存 spec 到用户项目 |
| `commands/build-doc.md` | `docs/ys-powers/guidelines/...` | 保存文档规范到用户项目 |
| `commands/teach-code.md` | `docs/superpowers/specs/...` | 保存阅读笔记到用户项目 |
| `commands/easy-analysis.md` | `docs/<project-name>/...` | 保存分析结果到用户项目 |
| `commands/sop-add.md` | `sop/...` | 保存 SOP 到用户项目 |

---

## 六、已验证安全（Global Install 后正确工作）

| 文件 | 机制 | 说明 |
|------|------|------|
| `hooks/session-start.sh` | `$0` + `dirname` 自定位 | `~/.claude/hooks/` → `~/.claude/skills/using-agent-skills/SKILL.md`。Global install 后 skills 也在 `~/.claude/skills/`，路径正确 |
| `hooks/simplify-ignore.sh` | `${CLAUDE_PROJECT_DIR}` | Claude Code 执行 hooks 时会设置此变量 |
| `hooks/sdd-cache-pre.sh` | `${CLAUDE_PROJECT_DIR:-$PWD}` | 同上，且 fallback 到 `$PWD` 在 hooks 场景下可接受 |
| `hooks/sdd-cache-post.sh` | `${CLAUDE_PROJECT_DIR:-$PWD}` | 同上 |
| `skills/brainstorming/scripts/server.cjs` | `__dirname` | Node.js 的 `__dirname` 是绝对路径，始终正确 |
| `skills/brainstorming/scripts/start-server.sh` | `cd "$SCRIPT_DIR"` | 切换工作目录到脚本所在目录后执行，安全 |

---

## 七、修复决策与验证结果

| 问题 | 决策 | 验证结果 |
|------|------|----------|
| `skills/idea-refine/SKILL.md:22` | 方案 B：`./scripts/idea-refine.sh` | ✅ 已修复（`441630f`） |
| `agents/html-generator.md` | 改为 `skill: html-anything` 调用 | ✅ 已修复（`b839cb4`） |
| `skills/html-anything/SKILL.md` | 信任 Claude Code 从 skill 目录解析 `./prompts/...` | ✅ 已验证（`/html test` 成功生成 `teaching` 风格 HTML） |
| **统一策略** | 已制定，见 [spec](specs/2026-05-15-global-install-path-fix-design.md) | — |

### 验证详情（2026-05-15）

在 `ys-powers` 项目内执行 `/html test`：
- `/html` 命令正确触发
- `html-generator` subagent 正常启动
- 成功应用 `teaching` 风格（说明 `prompts/styles/` 被正确读取）
- 输出文件有效（含完整 HTML 结构、CSS 变量、字体加载）
- 无 "file not found" 或 "skill not found" 错误

---

## 附录：Global Install 后的目录结构

```
~/.claude/
├── skills/           # 从 ys-powers/skills/ 复制
│   ├── html-anything/
│   │   ├── SKILL.md
│   │   └── prompts/        # 随 skill 一起复制
│   ├── idea-refine/
│   │   ├── SKILL.md
│   │   └── scripts/
│   └── ...
├── agents/           # 从 ys-powers/agents/ 复制
│   ├── html-generator.md
│   └── ...
├── commands/         # 从 ys-powers/commands/ 复制
├── hooks/            # 从 ys-powers/hooks/ 复制
├── rules/
├── references/
└── settings.json     # hooks 注入目标
```

**关键约束**：Claude Code 运行时的 CWD = 用户的项目目录（如 `~/projects/foo/`），而非 `~/.claude/`。
