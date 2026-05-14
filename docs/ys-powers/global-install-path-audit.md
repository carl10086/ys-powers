# Global Install 路径兼容性审计报告

**审计日期**: 2026-05-14
**审计范围**: `skills/`, `commands/`, `agents/`, `hooks/` 全部文件
**审计目标**: 排查 global install（`~/.claude/`）后，因相对路径或硬编码路径导致的能力失效问题

---

## 执行摘要

Global install 将 ys-powers 的内容复制到用户主目录的 `~/.claude/` 下。当 Claude Code 加载这些能力时，**当前工作目录（CWD）是用户的项目目录**，而非 ys-powers 仓库根目录。因此：

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
| **修复建议** | 改为 `./scripts/idea-refine.sh`（如果 Claude Code 执行 skill 时 CWD 是 skill 目录）或移除该引用，让 skill 直接执行初始化逻辑 |

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
| **修复建议** | 验证 Claude Code 行为。如果按 CWD 解析，需要改为使用环境变量（如 `${CLAUDE_PLUGIN_ROOT}`）或绝对路径 |

### 3. `skills/html-anything/SKILL.md` — Skill 内引用 Prompts

| 属性 | 值 |
|------|-----|
| **文件** | `skills/html-anything/SKILL.md` |
| **行号** | 369, 426, 451 |
| **问题代码** | `Read ./prompts/styles/_design.md`<br>`prompts/sources/`<br>`prompts/styles/` |
| **影响** | Skill 的 instructions 包含相对路径引用。如果 Claude Code 按 CWD 解析，找不到 prompts 目录 |
| **风险场景** | HTML 生成时缺少 Clockless 设计 token 和 source-specific 分析 guidance |
| **修复建议** | 同上。注意：如果 global install 后整个 `skills/html-anything/`（含 `prompts/` 子目录）被复制到 `~/.claude/skills/html-anything/`，且 Claude Code 从 skill 文件目录解析，则路径正确 |

---

## 三、设计意图（非 Bug，在用户项目 CWD 下操作）

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

**注意**：这些设计意图的路径在 global install 后仍然正确工作，因为它们本来就打算在用户项目 CWD 下操作。

---

## 四、已验证安全（Global Install 后正确工作）

| 文件 | 机制 | 说明 |
|------|------|------|
| `hooks/session-start.sh` | `$0` + `dirname` 自定位 | `~/.claude/hooks/` → `~/.claude/skills/using-agent-skills/SKILL.md`。Global install 后 skills 也在 `~/.claude/skills/`，路径正确 |
| `hooks/simplify-ignore.sh` | `${CLAUDE_PROJECT_DIR}` | Claude Code 执行 hooks 时会设置此变量 |
| `hooks/sdd-cache-pre.sh` | `${CLAUDE_PROJECT_DIR:-$PWD}` | 同上，且 fallback 到 `$PWD` 在 hooks 场景下可接受 |
| `hooks/sdd-cache-post.sh` | `${CLAUDE_PROJECT_DIR:-$PWD}` | 同上 |
| `skills/brainstorming/scripts/server.cjs` | `__dirname` | Node.js 的 `__dirname` 是绝对路径，始终正确 |
| `skills/brainstorming/scripts/start-server.sh` | `cd "$SCRIPT_DIR"` | 切换工作目录到脚本所在目录后执行，安全 |

---

## 五、低风险项（通常不影响生产使用）

| 文件 | 问题 | 说明 |
|------|------|------|
| `hooks/simplify-ignore-test.sh` | 相对路径 `hooks/simplify-ignore.sh` | 测试脚本，通常不会被用户直接执行。Global install 后即使被复制到 `~/.claude/hooks/`，误执行的概率极低 |
| `skills/html-anything/prompts/styles/catalog.json` | 17 个 `docs/example-previews/` 路径 | JSON 数据文件，不会自动被读取。只有当 skill 显式解析该 JSON 并加载预览图时才会涉及。需验证 html-anything skill 是否真的会加载这些预览图 |
| `agents/README.md` | `../references/orchestration-patterns.md` | Markdown 文档链接，不影响功能 |
| `agents/code-reviewer.md` | `[agents/README.md](README.md)` | 同上 |

---

## 六、修复建议汇总

### 优先级 P0（必须修复）

**`skills/idea-refine/SKILL.md:22`**
```markdown
# 修改前
bash /mnt/skills/user/idea-refine/scripts/idea-refine.sh

# 修改后（方案 A：相对路径，假设 CWD 是 skill 目录）
bash ./scripts/idea-refine.sh

# 修改后（方案 B：移除引用，让 skill 自身执行初始化）
# 删除该行，skill instructions 中直接包含目录初始化逻辑
```

### 优先级 P1（需要验证后决定）

**`agents/html-generator.md:34-35`** 和 **`skills/html-anything/SKILL.md:369,426,451`**

**验证方法**：
1. 在一个非 ys-powers 的测试项目中 global install ys-powers
2. 运行 `/html` 命令，观察 Claude Code 是否能成功读取 `skills/html-anything/SKILL.md` 和 `prompts/styles/_design.md`
3. 检查 Claude Code 的日志或输出，看是否有 "file not found" 错误

**如果验证失败**，修复方案：
- 方案 A：使用环境变量（如果 Claude Code 支持）
- 方案 B：使用绝对路径（不推荐，因用户主目录不同）
- 方案 C：将 prompts 内容内联到 skill/agent 文件中（消除外部依赖）
- 方案 D：如果确认 Claude Code 从 skill/agent 文件目录解析相对路径，则无需修改

---

## 七、审计方法论

本次审计采用以下方法：

1. **自动化扫描**：4 个 subagent 并行扫描 `skills/`, `commands/`, `agents/`, `hooks/` 全部文件
2. **模式匹配**：查找 `__file__`, `Path(__file__)`, `../`, `./`, `Path.cwd()`, `os.getcwd()`, `subprocess.run` 等模式
3. **人工复核**：对扫描结果中的关键文件进行人工读取和上下文分析
4. **运行时行为推断**：基于 global install 后的目录结构（`~/.claude/skills/`, `~/.claude/agents/` 等）推断路径解析结果

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
