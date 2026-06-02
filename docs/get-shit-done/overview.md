# get-shit-done 架构与设计理念总览

> 对应 refer 项目：`refer/get-shit-done/`（已归档，后续开发迁移至 [open-gsd/gsd-core](https://github.com/open-gsd/gsd-core)）
>
> 本文档基于对 refer 目录内容的只读分析，记录其设计结构供 ys-powers 借鉴参考。

---

## 一、项目定位

get-shit-done（简称 GSD）是一套**完整的 AI 驱动软件开发工作流系统**，目标是为 Claude Code、Copilot、Gemini CLI、Codex、Cursor 等 15+ 个 AI 编码工具提供统一的工程化流程支持。

与 ys-powers 的「轻量增强」定位不同，GSD 是一个**重型框架**：
- 拥有完整的 Node.js CLI 和 TypeScript SDK
- 自带 `.planning/` 目录状态管理系统
- 86+ 个命令、30+ 个 Agent 角色
- 多运行时安装器与兼容层

---

## 二、核心生命周期

GSD 定义了从项目初始化到交付的完整流水线：

```
new-project
    │
    ▼
discuss-phase ──→ spec-phase ──→ ui-phase (可选)
    │
    ▼
plan-phase ──→ execute-phase ──→ verify-work
    │                              │
    └────── gaps-only loop ────────┘
    │
    ▼
ship
    │
    ▼
complete-milestone / audit-milestone
```

### 关键阶段说明

| 阶段 | 产出物 | 核心机制 |
|------|--------|----------|
| `new-project` | PROJECT.md, REQUIREMENTS.md, ROADMAP.md, STATE.md, config.json | 深度上下文收集 + 结构化初始化 |
| `discuss-phase` | {phase}-CONTEXT.md, {phase}-DISCUSSION-LOG.md | Socratic 问答 + 自适应追问 |
| `spec-phase` | {phase}-SPEC.md | 模糊度评分（4 维度，≤0.20 阈值） |
| `plan-phase` | RESEARCH.md, PLAN.md | 研究 → 规划 → 验证循环 |
| `execute-phase` | SUMMARY.md, 原子提交 | Wave 并行执行 + 子 Agent 调度 |
| `verify-work` | {phase}-UAT.md | 对话式 UAT + 自动诊断修复 |
| `ship` | PR + 审查 | 推分支 → 创建 PR → 追踪合并 |

---

## 三、文档系统

GSD 强制使用一套**结构化文档体系**来管理项目状态：

```
.planning/
├── PROJECT.md          # 项目背景、目标、约束
├── REQUIREMENTS.md     # 范围化的需求列表
├── ROADMAP.md          # 阶段结构（含 Mode: mvp 标记）
├── STATE.md            # 项目记忆（进度、状态、上下文）
├── config.json         # 工作流偏好配置
├── research/           # 领域研究（可选）
├── phases/             # 各阶段产物
│   ├── 01-{name}/
│   │   ├── 01-SPEC.md
│   │   ├── 01-CONTEXT.md
│   │   ├── 01-PLAN.md
│   │   ├── 01-SUMMARY.md
│   │   └── 01-UAT.md
│   └── ...
└── workstreams/        # 多工作流隔离（可选）
```

### STATE.md 设计

STATE.md 是 GSD 的「项目记忆」核心，采用 frontmatter + 进度表格的形式：

```yaml
---
project: MyApp
phase: 3
status: in_progress
---
```

后续跟着各阶段的完成状态表格，便于机器解析和人阅读。

---

## 四、命令系统

### 4.1 命令规模

GSD 拥有 **86+ 个稳定命令**，分布在多个命名空间下：

| 命名空间 | 命令示例 | 职责 |
|----------|----------|------|
| `gsd-workflow` | plan-phase, execute-phase, verify-work, phase, progress | 阶段流水线 |
| `gsd-project` | new-milestone, complete-milestone, audit-milestone, summary | 项目生命周期 |
| `gsd-quality` | code-review, debug, audit-fix, security, eval-review, ui-review | 质量门 |
| `gsd-context` | map-codebase, graphify, ingest-docs, extract-learnings | 代码库智能 |
| `gsd-manage` | config, workspace, workstreams, thread, update, ship, inbox | 管理操作 |
| `gsd-ideate` | explore, sketch, spike, spec, capture | 探索与捕获 |

### 4.2 Namespace Meta-Skills（两级路由）

GSD v1.40 引入了**命名空间元技能**来解决「技能列表 token 消耗」问题：

- 传统方式：86 个技能平铺列出 → 约 2,150 tokens
- 命名空间方式：6 个路由器 + 按需展开 → 约 120 tokens

每个命名空间是一个「一级路由」，模型先选命名空间，再选具体命令。所有具体命令仍然可以直接调用。

### 4.3 命令定义格式

GSD 的命令采用 YAML frontmatter + Markdown body 的标准格式：

```yaml
---
name: gsd:plan-phase
description: Create detailed phase plan (PLAN.md) with verification loop
argument-hint: "[phase] [--auto] [--research] ..."
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
  - Agent
  - AskUserQuestion
  - WebFetch
  - mcp__context7__*
requires: [discuss-phase, phase, review, update]
---
```

关键字段：
- `name`：命令名（含运行时前缀）
- `allowed-tools`：显式声明允许使用的工具
- `requires`：依赖的其他命令/技能（用于安装时计算传递闭包）
- `argument-hint`：参数提示

---

## 五、Agent 系统

GSD 定义了 **34 个专门化的 Agent 角色**，每个都有明确的职责边界和触发条件：

### 核心执行 Agent

| Agent | 触发者 | 职责 |
|-------|--------|------|
| `gsd-planner` | plan-phase | 创建可执行的 PLAN.md，含依赖分析和 wave 分组 |
| `gsd-executor` | execute-phase | 原子执行计划，每任务一个 commit，处理偏差 |
| `gsd-verifier` | verify-work | 验证执行结果，生成 UAT 报告 |
| `gsd-debugger` | debug | 调试会话管理，诊断问题 |
| `gsd-code-reviewer` | code-review | 代码审查 |

### 研究型 Agent

| Agent | 触发者 | 职责 |
|-------|--------|------|
| `gsd-phase-researcher` | plan-phase --research | 领域研究，生成 RESEARCH.md |
| `gsd-domain-researcher` | new-project | 项目领域研究 |
| `gsd-ai-researcher` | 自主模式 | AI 集成相关研究 |
| `gsd-assumptions-analyzer` | discuss-phase --assumptions | 分析实现假设 |

### 质量门 Agent

| Agent | 触发者 | 职责 |
|-------|--------|------|
| `gsd-plan-checker` | plan-phase | 验证 PLAN.md 的可执行性 |
| `gsd-security-auditor` | secure-phase | 安全审计 |
| `gsd-ui-auditor` | ui-review | UI 审查 |
| `gsd-eval-auditor` | eval-review | 评估审计 |
| `gsd-nyquist-auditor` | 验证流程 | Nyquist 采样验证 |

### Agent 设计模式

每个 Agent 文件都遵循统一结构：

```yaml
---
name: gsd-planner
description: Creates executable phase plans...
tools: Read, Write, Bash, Glob, Grep, WebFetch, mcp__context7__*
color: green
---

<role>
  角色定义、触发者列表、核心职责
</role>

<documentation_lookup>
  文档查询策略（Context7 MCP 优先）
</documentation_lookup>

<project_context>
  项目上下文发现规则（CLAUDE.md、rules/*.md）
</project_context>

<context_fidelity>
  用户决策保真度约束（locked decisions、deferred ideas）
</context_fidelity>

<execution_flow>
  具体执行步骤
</execution_flow>
```

---

## 六、质量门与验证机制

GSD 在多个环节嵌入了强制性的质量检查：

### 6.1 规划阶段

- **Plan Checker**：验证 PLAN.md 的可执行性（任务是否可分解、依赖是否可达）
- **Nyquist Validation**：确保计划采样足够密集，不会遗漏关键步骤
- **Stall Detection**：检测 plan-phase 是否卡死

### 6.2 执行阶段

- **MVP+TDD Gate**：当 `MVP_MODE=true` 且 `TDD_MODE=true` 时，行为添加任务必须先有 failing test commit
- **Wave Execution**：将任务按依赖分组为 wave，wave 内并行、wave 间串行
- **Checkpoint Protocol**：执行器在 checkpoint 处暂停等待用户确认

### 6.3 验证阶段

- **Conversational UAT**：对话式用户验收测试
- **Cross-Phase Regression Gate**：检查是否破坏其他阶段的功能
- **Requirements Coverage Gate**：验证需求覆盖度

### 6.4 交付阶段

- **Cross-AI Peer Review**：调用外部 AI CLI（Gemini、Claude、Codex 等）独立评审计划
- **Security Enforcement**：安全强制检查
- **Post-Merge Hunk Verification**：合并后逐块验证

---

## 七、MVP 模式与垂直切片

GSD 的 MVP 模式是其最具特色的设计之一：

### 核心概念

| 概念 | 定义 |
|------|------|
| **MVP Mode** | 以垂直切片（UI→API→DB）而非水平分层组织任务 |
| **Vertical Slice** | 单功能端到端交付（从用户视角的一个完整能力） |
| **Walking Skeleton** | 新项目 Phase 1 的最薄端到端栈，证明各层能协同工作 |
| **User Story** | 标准格式：`As a [role], I want to [capability], so that [outcome].` |
| **SPIDR Splitting** | 五轴分解法：Spike, Paths, Interfaces, Data, Rules |

### Walking Skeleton 触发条件

```
phase_number == "01"
  AND prior_summaries == 0
  AND MVP_MODE == true
```

产出 `SKELETON.md`，记录后续垂直切片继承的架构决策。

---

## 八、技术架构

### 8.1 双运行时架构

GSD 采用 **CJS 兼容层 + TypeScript SDK** 的双层设计：

```
CLI 入口 (bin/gsd-tools.cjs)
    │
    ├── CJS Command Router (兼容层，逐步迁移中)
    │      └── 调用 Sync Runtime Bridge
    │
    └── TypeScript SDK (sdk/src/)
            ├── Query Dispatch Pipeline
            ├── Phase Runner
            ├── Runtime Bridge (async)
            └── Runtime Bridge Sync (Worker + Atomics.wait)
```

- **Sync Runtime Bridge**：使用 `synckit` + `SharedArrayBuffer` + Worker 线程实现同步调用异步 SDK，首调用开销 ~80ms，稳态 ~0.1ms
- **Command Routing Hub**：纯结果合约（不抛异常、不退出、不打印），统一 6 值错误枚举

### 8.2 安装系统

GSD 支持 15 个运行时的安装：

```
claude, antigravity, augment, cline, codebuddy, codex, copilot,
cursor, gemini, hermes, kilo, opencode, qwen, trae, windsurf
```

安装时根据运行时类型转换命令格式（hyphen/colon/dollar 前缀）、Agent 格式、技能布局等。

### 8.3 Skill Surface Budget

GSD 通过 **Profile** 控制安装时写入的运行时技能数量：

- `core`：最小集
- `standard`：标准集
- `full`：完整集（默认）

运行时还可通过 `/gsd:surface` 命令动态启用/禁用技能簇，无需重新安装。

---

## 九、与 ys-powers 的本质差异

| 维度 | get-shit-done | ys-powers |
|------|---------------|-----------|
| **定位** | 重型框架，完整生命周期管理 | 轻量增强，聚焦 Claude Code |
| **运行时** | Node.js CLI + SDK，有实际可执行代码 | 纯配置（skills/rules/commands），无运行时 |
| **状态管理** | `.planning/` 目录体系，STATE.md 为核心 | 无状态，不管理项目级状态 |
| **命令数量** | 86+ | 20 |
| **Agent 数量** | 34 | 3（code-reviewer, security-auditor, test-engineer） |
| **多运行时** | 15 个运行时兼容 | 仅 Claude Code |
| **安装方式** | npm 包 + 运行时安装器 | Python 脚本安装到 `.claude/` |
| **交互语言** | 英文为主，多语言文档 | 中文优先 |
| **TDD 强制** | MVP+TDD Gate 可强制 failing test 先提交 | 推荐 TDD，不强制 |
| **Context Rot 缓解** | Context Window Monitoring、Prompt Thinning | 依赖 spec/plan 文档化 |

---

## 十、关键设计亮点（值得深入研究）

1. **Namespace Meta-Skills**：两级路由降低 token 消耗的创新方案
2. **Ambiguity Scoring**：spec-phase 的定量化模糊度评分机制
3. **User Decision Fidelity**：locked/deferred/discretion 三级决策保真度
4. **Wave Parallelization**：execute-phase 的依赖感知并行执行
5. **Cross-AI Peer Review**：多 AI 独立评审的工程质量实践
6. **Context Window Utilization Guard**：主动监控和压缩上下文
7. **Skill Surface Budget**：通过 profile 和 cluster 控制技能暴露面
8. **Sync Runtime Bridge**：CJS/ESM 互操作的工程化方案

---

*文档生成时间：2026-06-01*
*分析基于 refer/get-shit-done 归档版本*
