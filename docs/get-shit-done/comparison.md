# ys-powers 与 get-shit-done 对比分析

> 从命令覆盖、Skill 组织、Agent 系统、状态管理、质量门五个维度进行结构化对比。

---

## 一、命令覆盖对比

### 1.1 核心工作流命令

| 阶段 | get-shit-done | ys-powers | 差距分析 |
|------|---------------|-----------|----------|
| 项目初始化 | `/gsd-new-project` | 无 | GSD 有完整的项目脚手架，ys-powers 假设项目已存在 |
| 需求澄清 | `/gsd-discuss-phase`, `/gsd-spec-phase` | `/spec` | 两者都有 spec 驱动，但 GSD 多了 Socratic 问答 + 模糊度评分 |
| 规划 | `/gsd-plan-phase` | `/ys-plan` | GSD 有内置研究 Agent 和验证循环；ys-powers 更轻量 |
| 执行 | `/gsd-execute-phase` | `/build` | GSD 有 wave 并行；ys-powers 是单线程增量实现 |
| 验证 | `/gsd-verify-work` | `/test` | GSD 是对话式 UAT；ys-powers 是 TDD 技能调用 |
| 交付 | `/gsd-ship` | `/ship` | 两者都有 fan-out 评审，但 GSD 还管 PR 创建和合并追踪 |
| 自主模式 | `/gsd-autonomous` | 无 | GSD 可全自动跑完所有剩余阶段 |

### 1.2 GSD 独有的命令类别

**上下文工程**
- `/gsd-map-codebase` — 代码库映射
- `/gsd-graphify` — 知识图谱构建
- `/gsd-ingest-docs` — 文档摄取
- `/gsd-extract-learnings` — 经验提取

**质量门**
- `/gsd-code-review --fix` — 代码审查 + 自动修复
- `/gsd-eval-review` — AI 评估审查
- `/gsd-nyquist-auditor` — Nyquist 采样验证
- `/gsd-secure-phase` — 安全阶段审查

**管理**
- `/gsd-workspace` — 多仓库工作空间
- `/gsd-workstreams` — 工作流命名空间
- `/gsd-thread` — 持久化上下文线程
- `/gsd-inbox` — 待办捕获

**探索**
- `/gsd-spike` — 技术探针
- `/gsd-sketch` — 快速草图
- `/gsd-explore` — 代码库探索

### 1.3 ys-powers 独有的命令

- `/gc` — 智能 Git 工作流（分支→提交→推送→PR 一键完成）
- `/s2m` — worktree 回主分支清理
- `/scout` — 多渠道并行信息探索
- `/local-commit` — 极简本地提交
- `/alias` — zsh 别名管理
- `/html` — 转换为 HTML 页面
- `/doc-codebase` — 代码库文档化

---

## 二、Skill 组织对比

### 2.1 GSD 的 Skill 模式

GSD 的 `skills/` 不是传统意义上的 skill 目录，而是**运行时技能表面预算系统**：

- **安装时**：通过 profile（core/standard/full）决定写入多少技能
- **运行时**：通过 `/gsd:surface` 动态启用/禁用技能簇
- **技能格式**：与命令格式相同（YAML frontmatter + Markdown）
- **依赖解析**：`requires:` 字段定义依赖，安装器计算传递闭包

### 2.2 ys-powers 的 Skill 模式

ys-powers 采用**传统 skill 定义**：

- `skills/<name>/SKILL.md` — 主 skill 文件
- `skills/<name>/*.md` — 辅助文件（示例、框架、模板等）
- 安装时完整复制到目标项目的 `.claude/skills/`
- 无运行时动态开关机制

### 2.3 Skill 内容深度对比

以「规划」为例：

| 维度 | GSD plan-phase | ys-powers planning-and-task-breakdown |
|------|----------------|--------------------------------------|
| 前置研究 | 内置 `--research` 模式，自动 spawn researcher | 无内置研究，依赖外部 spec |
| 验证循环 | 内置 plan-checker，迭代到通过或最大次数 | 无内置验证，依赖 human review |
| 输出格式 | PLAN.md（含 wave 分组、依赖图） | plan markdown（任务列表） |
| 重规划 | `--reviews` 支持跨 AI 反馈重规划 | 无内置重规划机制 |
| 交互深度 | 多 flag 控制（--auto, --gaps, --skip-verify 等） | 单一流程 |

---

## 三、Agent 系统对比

### 3.1 Agent 数量与覆盖度

| 类别 | GSD Agents | ys-powers Agents |
|------|-----------|------------------|
| 规划 | gsd-planner, gsd-plan-checker, gsd-roadmapper | 无 |
| 执行 | gsd-executor, gsd-code-fixer | 无 |
| 验证 | gsd-verifier, gsd-eval-auditor, gsd-nyquist-auditor | 无 |
| 调试 | gsd-debugger, gsd-debug-session-manager | 无 |
| 代码审查 | gsd-code-reviewer | code-reviewer |
| 安全审计 | gsd-security-auditor | security-auditor |
| 测试 | 无专门测试 Agent | test-engineer |
| 研究 | gsd-phase-researcher, gsd-domain-researcher 等 6 个 | 无 |
| UI | gsd-ui-auditor, gsd-ui-checker, gsd-ui-researcher | 无 |
| 文档 | gsd-doc-writer, gsd-doc-synthesizer 等 4 个 | 无 |

### 3.2 Agent 设计差异

**GSD Agent 特点**：
- 每个 Agent 有明确的触发者和输入输出合约
- 支持 `tools:` 限制和 `hooks:`（如 PostToolUse 自动 eslint）
- 有颜色标记（`color: green/yellow`）用于 UI 区分
- 强制引用 `@~/.claude/get-shit-done/references/mandatory-initial-read.md`

**ys-powers Agent 特点**：
- 仅 3 个通用评审 Agent，用于 `/ship` 的 fan-out
- 无触发者概念，直接由命令调用
- 无工具限制（继承主会话的工具权限）
- 更轻量，无需额外配置

---

## 四、状态管理对比

### 4.1 GSD 的状态系统

GSD 是**有状态框架**，项目状态集中管理：

```
.planning/STATE.md          # 全局状态
.planning/ROADMAP.md        # 路线图（含阶段定义）
.planning/config.json       # 配置
{phase_dir}/SUMMARY.md      # 阶段总结
{phase_dir}/{phase}-UAT.md  # 验收结果
```

**状态机**：
- 阶段状态：`not_started` → `in_progress` → `completed`
- 里程碑管理：归档、审计、完成
- Workstream：多工作流隔离

### 4.2 ys-powers 的状态系统

ys-powers 是**无状态系统**：

- 不管理项目级状态文件
- Spec 和 Plan 保存在 `docs/superpowers/specs/` 和 `docs/superpowers/plans/`
- 状态由用户自行管理（git 提交、GitHub Issues 等）
- 无 `.planning/` 目录要求

### 4.3 利弊分析

| 维度 | GSD 有状态 | ys-powers 无状态 |
|------|-----------|-----------------|
| 上手成本 | 高（需要理解 .planning 体系） | 低（直接用命令） |
| 项目迁移 | 难（状态绑定目录） | 易（纯配置） |
| 自动化程度 | 高（可自主推进） | 低（依赖用户决策） |
| 上下文保持 | 强（STATE.md 持久化） | 弱（依赖会话记忆） |
| 适用场景 | 长期项目、团队协作 | 快速任务、个人工作流 |

---

## 五、质量门对比

### 5.1 GSD 的多层质量门

| 层级 | 机制 | 强制性 |
|------|------|--------|
| 规划 | Plan Checker + Nyquist Validation | 强制（可 --skip-verify 跳过） |
| 执行 | MVP+TDD Gate + Checkpoint Protocol | 条件强制（MVP+TDD 模式下） |
| 验证 | Conversational UAT + Gap Closure | 强制 |
| 交付 | Cross-AI Peer Review + Security Audit | 可选 |
| 合并 | Post-Merge Hunk Verification | 可选 |

### 5.2 ys-powers 的质量门

| 层级 | 机制 | 强制性 |
|------|------|--------|
| 规划 | Human Review（plan 文件确认） | 强制（需用户确认保存路径） |
| 执行 | Incremental Implementation + TDD | 推荐（技能引导） |
| 验证 | Test + Build + Browser Test | 推荐（技能引导） |
| 交付 | /ship fan-out（code-reviewer + security-auditor + test-engineer） | 强制（/ship 命令自动执行） |

### 5.3 关键差距

1. **GSD 有自动验证 Agent**，ys-powers 依赖 human review
2. **GSD 有 TDD 强制门**，ys-powers 只是推荐
3. **GSD 有 Cross-AI Review**，ys-powers 的 /ship 是单运行时内的 subagent
4. **GSD 有 Gap Closure Loop**，ys-powers 无内置的修复→重执行循环

---

## 六、交互设计对比

### 6.1 语言策略

| 维度 | GSD | ys-powers |
|------|-----|-----------|
| 主要语言 | 英文 | 中文 |
| 文档多语言 | 有（ja-JP, ko-KR, pt-BR, zh-CN） | 无 |
| 命令名 | 英文 | 英文缩写（/gc, /s2m 等） |

### 6.2 交互深度

**GSD**：
- 大量 `--auto` / `--interactive` 模式切换
- Socratic 问答（多轮对话）
- Batch 模式（批量回答问题）
- Power 模式（从文件批量导入答案）

**ys-powers**：
- 大多数命令直接执行
- 关键决策点询问用户（如 workspace 策略选择）
- Explore-then-ask skill 有结构化问答，但不是所有命令都用

---

## 七、架构复杂度对比

### 7.1 代码量与依赖

| 维度 | GSD | ys-powers |
|------|-----|-----------|
| 主要语言 | TypeScript + CommonJS | Python + Markdown |
| 依赖数量 | 大量（npm 包、synckit、Vitest 等） | 极少（标准库） |
| 测试覆盖 | 70%+ 行覆盖要求 | 无强制要求 |
| CI/CD | 完整（CodeRabbit、secret-scan、lint 等） | 简单 Makefile |
| ADR | 12+ 个架构决策记录 | 无 |

### 7.2 可维护性

**GSD**：
- 优点：工程化程度高，有完整测试和文档
- 缺点：架构复杂（CJS/SDK 双运行时、Sync Bridge、15 运行时兼容），变更成本高

**ys-powers**：
- 优点：极简（纯 Markdown + Python 脚本），变更成本低
- 缺点：无测试覆盖，缺乏自动化验证

---

## 八、总结矩阵

| 能力 | GSD 优势 | ys-powers 优势 |
|------|----------|----------------|
| 项目初始化 | 完整脚手架 + 深度上下文收集 | 更灵活，不绑架项目结构 |
| 规划深度 | 研究 + 规划 + 验证循环 | 轻量快速，不阻塞 |
| 执行自动化 | Wave 并行 + 子 Agent | 简单直接 |
| 质量保障 | 多层强制门 | /ship fan-out 足够实用 |
| 上下文管理 | STATE.md 持久化 | 无负担 |
| 多运行时 | 15 个运行时兼容 | 聚焦 Claude Code，体验更好 |
| 可维护性 | 工程化强但复杂 | 极简但缺乏验证 |
| 中文支持 | 有但非优先 | 原生中文体验 |

---

*对比分析完成时间：2026-06-01*
