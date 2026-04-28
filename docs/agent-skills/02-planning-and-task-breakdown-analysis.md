# Easy Analysis: planning-and-task-breakdown/SKILL.md

## 分析概要

### 文档定位
这是一个 Claude Code **技能定义文件**，规定了"计划与任务拆解"（planning-and-task-breakdown）这一工程流程的完整工作流。它是 `spec-driven-development` 的下游技能 —— 承接已确定的规格，将其转化为可执行的任务清单。

### 核心主张
**"好的任务拆解是可靠交付与一团糟之间的分水岭。"** 该 skill 强调将工作分解为"小、可验证、有明确验收标准"的任务，每个任务应能在一次专注会话内完成、测试和验证。其关键创新在于**垂直切片**（vertical slicing）和**任务尺寸管控**。

### 结构骨架

| 章节 | 内容 |
|------|------|
| 概述 + 使用时机 | 任务拆解的目的和触发条件 |
| 计划流程（5 步） | 进入计划模式 → 识别依赖图 → 垂直切片 → 编写任务 → 排序与检查点 |
| 任务尺寸指南 | XS/S/M/L/XL 五级尺寸表，及何时需要进一步拆分 |
| 计划文档模板 | 可直接使用的 Markdown 模板 |
| 并行化机会 | 哪些任务可以并行，哪些必须串行 |
| 常见借口 | 反驳"边做边想""计划是开销"等借口 |
| 危险信号 | 无任务清单直接编码、任务过大等 |
| 验证清单 | 进入实现前的确认项 |

### 关键洞察

1. **垂直切片 > 水平切片** — 不要先建完所有数据库再建所有 API 再建所有 UI，而是先完成一个端到端的用户场景（如注册），再完成下一个。这样每个切片都是可测试的。
2. **任务尺寸是质量门** — XL 任务必须拆分，S 和 M 是智能体的最佳工作范围。这不是建议，而是硬性约束。
3. **计划就是产出** — "Planning is the task. Implementation without a plan is just typing."（计划本身就是任务。没有计划的实现只是在打字。）

---

## Step 1: 逐段精读

### 段落 1: Frontmatter（元数据声明）

**原文:**
```yaml
---
name: planning-and-task-breakdown
description: Breaks work into ordered tasks. Use when you have a spec or clear requirements and need to break work into implementable tasks. Use when a task feels too large to start, when you need to estimate scope, or when parallel work is possible.
---
```

**翻译:**
```yaml
---
name: planning-and-task-breakdown
description: 将工作拆解为有序的任务。当你已有规格或清晰需求，需要将工作拆解为可执行的任务时使用。当任务感觉太大不知如何开始、需要估算范围、或可能存在并行工作时使用。
---
```

**要点:**
- **为什么重要**: Frontmatter 明确定义了触发条件。关键是"use when you have a spec" —— 这意味着该 skill 有一个前置依赖（`spec-driven-development`）。如果你还没有规格，应该先调用 `/spec`。
- **隐含意义**: "when a task feels too large to start" 捕捉到了开发者的一种常见心理状态 —— 面对一个大任务时的"启动困难"。任务拆解的心理价值不亚于工程价值。
- **可执行建议**: 当你觉得"这个任务好大，我不知道从哪里开始"时，这就是调用 `/plan` 的明确信号。

---

### 段落 2: 标题与概述

**原文:**
```markdown
# Planning and Task Breakdown

## Overview

Decompose work into small, verifiable tasks with explicit acceptance criteria. Good task breakdown is the difference between an agent that completes work reliably and one that produces a tangled mess. Every task should be small enough to implement, test, and verify in a single focused session.
```

**翻译:**
```markdown
# 计划与任务拆解

## 概述

将工作分解为小的、可验证的任务，并附带明确的验收标准。好的任务拆解是智能体能可靠完成工作与制造一团糟之间的分水岭。每个任务都应该足够小，能在一次专注的会话内实现、测试和验证。
```

**要点:**
- **为什么重要**: 开篇即建立了强烈的价值主张 —— 任务拆解不是"可有可无的组织工作"，而是决定 AI 交付质量的**关键因素**。"tangled mess"（一团糟）这个短语暗示了没有计划时 AI 代码的典型失败模式：纠缠不清、难以验证。
- **隐含意义**: "single focused session"（一次专注会话）是一个关键约束。它暗示了人类的注意力有限性，也暗示了 AI 的上下文窗口有限性 —— 如果一个任务需要跨多个会话完成，记忆和一致性就会衰减。
- **可执行建议**: 把"能否在单次会话内完成"作为任务大小的试金石。如果一个任务预计需要 3 小时，它应该被拆成两个 1.5 小时的任务。

---

### 段落 3: 使用时机

**原文:**
```markdown
## When to Use

- You have a spec and need to break it into implementable units
- A task feels too large or vague to start
- Work needs to be parallelized across multiple agents or sessions
- You need to communicate scope to a human
- The implementation order isn't obvious

**When NOT to use:** Single-file changes with obvious scope, or when the spec already contains well-defined tasks.
```

**翻译:**
```markdown
## 使用时机

- 你已有规格，需要将其拆解为可执行单元
- 任务感觉太大或太模糊，不知如何开始
- 工作需要在多个智能体会话间并行化
- 你需要向人类沟通范围
- 实现顺序不明显

**不要使用：**范围明显的单文件变更，或规格中已经包含定义良好的任务。
```

**要点:**
- **为什么重要**: 明确了 skill 的使用边界。特别注意"when the spec already contains well-defined tasks" —— 如果上游的 `spec-driven-development` 已经把任务定义得很好，就不需要再调用 `/plan`。避免过度流程化。
- **隐含意义**: "You need to communicate scope to a human" 揭示了任务拆解的一个社交功能。任务清单是人类和 AI 之间关于"这件事有多大"的共享语言。没有它，人类可能低估或高估所需时间。
- **可执行建议**: 面对一个新任务时，用 30 秒判断：它涉及几个文件？顺序是否明确？如果答案是不确定，就启用 `/plan`。

---

### 段落 4: The Planning Process — Step 1: Enter Plan Mode

**原文:**
```markdown
## The Planning Process

### Step 1: Enter Plan Mode

Before writing any code, operate in read-only mode:

- Read the spec and relevant codebase sections
- Identify existing patterns and conventions
- Map dependencies between components
- Note risks and unknowns

**Do NOT write code during planning.** The output is a plan document, not implementation.
```

**翻译:**
```markdown
## 计划流程

### 步骤 1：进入计划模式

在写任何代码之前，以只读模式操作：

- 读取规格和相关代码库部分
- 识别现有模式和约定
- 映射组件之间的依赖关系
- 记录风险和未知项

**计划在期间不要写代码。** 产出是一份计划文档，不是实现。
```

**要点:**
- **为什么重要**: 这是计划阶段的**纪律要求**。"Do NOT write code during planning" 用大写强调，因为它是最容易被违反的规则 —— 开发者（和 AI）倾向于"我先改一点，然后再计划"。
- **隐含意义**: "Read-only mode" 是一个心智模型。它要求你在动手之前先建立完整的心智地图。这就像拼图前先看看盒上的完整图案，而不是拿起一块就开始找位置。
- **可执行建议**: 启用 `/plan` 时，先花 5-10 分钟只读代码和规格，不要打开编辑器。产出应该是一份 Markdown 计划文档，而不是代码文件。

---

### 段落 5: Step 2: Identify the Dependency Graph

**原文:**
```markdown
### Step 2: Identify the Dependency Graph

Map what depends on what:

```
Database schema
    │
    ├── API models/types
    │       │
    │       ├── API endpoints
    │       │       │
    │       │       └── Frontend API client
    │       │               │
    │       │               └── UI components
    │       │
    │       └── Validation logic
    │
    └── Seed data / migrations
```

Implementation order follows the dependency graph bottom-up: build foundations first.
```

**翻译:**
```markdown
### 步骤 2：识别依赖图

映射什么依赖于什么：

```
数据库架构
    │
    ├── API 模型/类型
    │       │
    │       ├── API 端点
    │       │       │
    │       │       └── 前端 API 客户端
    │       │               │
    │       │               └── UI 组件
    │       │
    │       └── 验证逻辑
    │
    └── 种子数据 / 迁移
```

实现顺序遵循依赖图自底向上：先构建基础。
```

**要点:**
- **为什么重要**: 依赖图是技术实现的"地形图"。它强迫你在编码前思考"如果我改了这里，哪里会坏"。这个图不是装饰，而是决定实现顺序的核心输入。
- **隐含意义**: ASCII 图展示了一个典型的全栈依赖链：数据库 → 类型/模型 → 端点 → 客户端 → UI。这个模式可以套用到几乎所有 Web 项目上。"自底向上"（bottom-up）的顺序意味着你总是在稳固的基础上构建。
- **可执行建议**: 在写计划文档时，强制自己画一个依赖图。即使只是文本形式的缩进列表，也能暴露隐藏的依赖关系。

---

### 段落 6: Step 3: Slice Vertically

**原文:**
```markdown
### Step 3: Slice Vertically

Instead of building all the database, then all the API, then all the UI — build one complete feature path at a time:

**Bad (horizontal slicing):**
```
Task 1: Build entire database schema
Task 2: Build all API endpoints
Task 3: Build all UI components
Task 4: Connect everything
```

**Good (vertical slicing):**
```
Task 1: User can create an account (schema + API + UI for registration)
Task 2: User can log in (auth schema + API + UI for login)
Task 3: User can create a task (task schema + API + UI for creation)
Task 4: User can view task list (query + API + UI for list view)
```

Each vertical slice delivers working, testable functionality.
```

**翻译:**
```markdown
### 步骤 3：垂直切片

不要先构建所有数据库，然后所有 API，然后所有 UI —— 而是一次构建一条完整的功能路径：

**不好（水平切片）：**
```
任务 1：构建整个数据库架构
任务 2：构建所有 API 端点
任务 3：构建所有 UI 组件
任务 4：连接所有东西
```

**好（垂直切片）：**
```
任务 1：用户可以创建账户（注册所需的架构 + API + UI）
任务 2：用户可以登录（登录所需的认证架构 + API + UI）
任务 3：用户可以创建任务（创建所需的任务架构 + API + UI）
任务 4：用户可以查看任务列表（列表视图所需的查询 + API + UI）
```

每个垂直切片都交付可工作、可测试的功能。
```

**要点:**
- **为什么重要**: 这是本 skill 中**最重要的方法论创新**。水平切片的问题是：在前三个任务完成后，你没有任何可演示的功能，只有一堆互不连接的基础设施。垂直切片确保每一步都有"可工作的软件"。
- **隐含意义**: "Each vertical slice delivers working, testable functionality" 呼应了敏捷开发的核心理念。但它被重新表述为任务拆解的技术原则。垂直切片使得团队可以在第 1 个任务完成后就获得反馈，而不是等到第 4 个。
- **可执行建议**: 在写任务时，检查每个任务标题。如果它只涉及一个技术层（如"建表"、"写 API"），考虑把它与其他层的相关工作合并为一个用户场景任务。

---

### 段落 7: Step 4: Write Tasks

**原文:**
```markdown
### Step 4: Write Tasks

Each task follows this structure:

```markdown
## Task [N]: [Short descriptive title]

**Description:** One paragraph explaining what this task accomplishes.

**Acceptance criteria:**
- [ ] [Specific, testable condition]
- [ ] [Specific, testable condition]

**Verification:**
- [ ] Tests pass: `npm test -- --grep "feature-name"`
- [ ] Build succeeds: `npm run build`
- [ ] Manual check: [description of what to verify]

**Dependencies:** [Task numbers this depends on, or "None"]

**Files likely touched:**
- `src/path/to/file.ts`
- `tests/path/to/test.ts`

**Estimated scope:** [Small: 1-2 files | Medium: 3-5 files | Large: 5+ files]
```
```

**翻译:**
```markdown
### 步骤 4：编写任务

每个任务遵循以下结构：

```markdown
## 任务 [N]: [简短的描述性标题]

**描述：** 一段解释此任务完成什么的文字。

**验收标准：**
- [ ] [具体的、可测试的条件]
- [ ] [具体的、可测试的条件]

**验证：**
- [ ] 测试通过：`npm test -- --grep "feature-name"`
- [ ] 构建成功：`npm run build`
- [ ] 手动检查：[需要验证的内容描述]

**依赖：** [此任务依赖的任务编号，或"无"]

**可能触及的文件：**
- `src/path/to/file.ts`
- `tests/path/to/test.ts`

**估计范围：** [小: 1-2 文件 | 中: 3-5 文件 | 大: 5+ 文件]
```
```

**要点:**
- **为什么重要**: 这是任务的标准化模板。每个字段都有明确目的：**Description** 回答"做什么"，**Acceptance criteria** 回答"怎样算完成"，**Verification** 回答"如何验证"，**Dependencies** 回答"先做什么"。
- **隐含意义**: **Verification** 部分要求具体的命令（如 `npm test -- --grep "feature-name"`），而不是模糊的"测试一下"。这确保了验证是可重复、可自动化的。
- **可执行建议**: 不要省略任何一个字段。特别是 "Files likely touched" —— 即使只是预测，它也能帮助发现任务是否过大（如果列表超过 5 个文件，考虑拆分）。

---

### 段落 8: Step 5: Order and Checkpoint

**原文:**
```markdown
### Step 5: Order and Checkpoint

Arrange tasks so that:

1. Dependencies are satisfied (build foundation first)
2. Each task leaves the system in a working state
3. Verification checkpoints occur after every 2-3 tasks
4. High-risk tasks are early (fail fast)

Add explicit checkpoints:

```markdown
## Checkpoint: After Tasks 1-3
- [ ] All tests pass
- [ ] Application builds without errors
- [ ] Core user flow works end-to-end
- [ ] Review with human before proceeding
```
```

**翻译:**
```markdown
### 步骤 5：排序与设置检查点

安排任务，确保：

1. 依赖已满足（先构建基础）
2. 每个任务都让系统保持可工作状态
3. 每 2-3 个任务后设置验证检查点
4. 高风险任务放在前面（快速失败）

添加明确的检查点：

```markdown
## 检查点：任务 1-3 完成后
- [ ] 所有测试通过
- [ ] 应用构建无错误
- [ ] 核心用户流程端到端可用
- [ ] 继续前与人类审核
```
```

**要点:**
- **为什么重要**: 排序规则是计划阶段的"质量控制"。第 2 点"Each task leaves the system in a working state" 是一个强约束 —— 它要求每个任务都是原子的、不破坏现有功能的。
- **隐含意义**: "High-risk tasks are early (fail fast)" 是一个反直觉但至关重要的原则。人类倾向于把"难的"事情往后拖，但 skill 要求先做。原因是：如果高风险任务注定失败，越早发现，浪费越少。
- **可执行建议**: 检查点不是可选的。每 2-3 个任务后必须有一个检查点，强制停下来验证系统状态。这防止了"做了 10 个任务后发现第 1 个就错了"的灾难。

---

### 段落 9: Task Sizing Guidelines（任务尺寸指南）

**原文:**
```markdown
## Task Sizing Guidelines

| Size | Files | Scope | Example |
|------|-------|-------|---------|
| **XS** | 1 | Single function or config change | Add a validation rule |
| **S** | 1-2 | One component or endpoint | Add a new API endpoint |
| **M** | 3-5 | One feature slice | User registration flow |
| **L** | 5-8 | Multi-component feature | Search with filtering and pagination |
| **XL** | 8+ | **Too large — break it down further** | — |

If a task is L or larger, it should be broken into smaller tasks. An agent performs best on S and M tasks.
```

**翻译:**
```markdown
## 任务尺寸指南

| 尺寸 | 文件数 | 范围 | 示例 |
|------|--------|------|------|
| **XS** | 1 | 单个函数或配置变更 | 添加验证规则 |
| **S** | 1-2 | 一个组件或端点 | 添加新 API 端点 |
| **M** | 3-5 | 一个功能切片 | 用户注册流程 |
| **L** | 5-8 | 多组件功能 | 带过滤和分页的搜索 |
| **XL** | 8+ | **太大 —— 进一步拆分** | — |

如果任务是 L 或更大，它应该被拆分为更小的任务。智能体在 S 和 M 任务上表现最佳。
```

**要点:**
- **为什么重要**: 这是任务拆解的**量化标准**。它将主观感觉（"这个任务有点大"）转化为客观指标（文件数量）。XL 被标记为"必须拆分"，没有例外。
- **隐含意义**: "An agent performs best on S and M tasks" 是对 AI 能力的现实主义评估。AI 在处理 1-5 个文件的变更时，上下文管理最清晰；超过 5 个文件，遗漏和错误率会显著上升。
- **可执行建议**: 把这张表作为硬性规则。如果一个任务预计触及 6 个文件，自动把它拆成两个任务。不要跟 XL 任务妥协。

---

### 段落 10: When to break a task down further

**原文:**
```markdown
**When to break a task down further:**
- It would take more than one focused session (roughly 2+ hours of agent work)
- You cannot describe the acceptance criteria in 3 or fewer bullet points
- It touches two or more independent subsystems (e.g., auth and billing)
- You find yourself writing "and" in the task title (a sign it is two tasks)
```

**翻译:**
```markdown
**何时需要进一步拆分任务：**
- 它需要超过一次专注会话（大约 2 小时以上的智能体工作）
- 你无法在 3 个或更少的要点内描述验收标准
- 它触及两个或更多独立的子系统（如认证和账单）
- 你发现自己在任务标题中写了"和"（这是两个任务的信号）
```

**要点:**
- **为什么重要**: 这是拆分任务的**启发式规则**（heuristics）。它们比单纯的文件数更具操作性。特别是"验收标准不超过 3 个要点" —— 如果一个任务需要 8 个验收标准，说明它实际上包含多个子任务。
- **隐含意义**: "You find yourself writing 'and' in the task title" 是一个巧妙的语言学检测。"实现用户注册和登录" = 两个任务。"更新 auth 和 billing 的日志记录" = 两个任务。这个规则利用了人类的语言直觉。
- **可执行建议**: 写完任务标题后，检查是否包含"和"/"以及"/"同时"。如果是，把它拆成两个标题。

---

### 段落 11: Plan Document Template（计划文档模板）

**原文:**
```markdown
## Plan Document Template

```markdown
# Implementation Plan: [Feature/Project Name]

## Overview
[One paragraph summary of what we're building]

## Architecture Decisions
- [Key decision 1 and rationale]
- [Key decision 2 and rationale]

## Task List

### Phase 1: Foundation
- [ ] Task 1: ...
- [ ] Task 2: ...

### Checkpoint: Foundation
- [ ] Tests pass, builds clean

### Phase 2: Core Features
- [ ] Task 3: ...
- [ ] Task 4: ...

### Checkpoint: Core Features
- [ ] End-to-end flow works

### Phase 3: Polish
- [ ] Task 5: ...
- [ ] Task 6: ...

### Checkpoint: Complete
- [ ] All acceptance criteria met
- [ ] Ready for review

## Risks and Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk] | [High/Med/Low] | [Strategy] |

## Open Questions
- [Question needing human input]
```
```

**翻译:**
```markdown
## 计划文档模板

```markdown
# 实现计划：[功能/项目名称]

## 概述
[一段关于我们要构建什么的总结]

## 架构决策
- [关键决策 1 及其理由]
- [关键决策 2 及其理由]

## 任务清单

### 阶段 1：基础
- [ ] 任务 1：...
- [ ] 任务 2：...

### 检查点：基础
- [ ] 测试通过，构建干净

### 阶段 2：核心功能
- [ ] 任务 3：...
- [ ] 任务 4：...

### 检查点：核心功能
- [ ] 端到端流程可用

### 阶段 3：优化
- [ ] 任务 5：...
- [ ] 任务 6：...

### 检查点：完成
- [ ] 所有验收标准已满足
- [ ] 准备审核

## 风险与缓解
| 风险 | 影响 | 缓解策略 |
|------|------|----------|
| [风险] | [高/中/低] | [策略] |

## 开放问题
- [需要人工输入的问题]
```
```

**要点:**
- **为什么重要**: 这是一个完整的、可直接使用的计划文档模板。它强制要求思考架构决策、风险和开放问题 —— 这些通常被遗漏，但决定了项目的成败。
- **隐含意义**: 模板中嵌入了三个阶段（Foundation → Core Features → Polish），这是一种自然的优先级分层。它确保核心功能优先于优化，防止过早优化（premature optimization）。
- **可执行建议**: 将这个模板保存到项目目录中，每次启用 `/plan` 时直接复制使用。不要省略 "Risks and Mitigations" 和 "Open Questions" 部分 —— 即使它们的内容很短。

---

### 段落 12: Parallelization Opportunities

**原文:**
```markdown
## Parallelization Opportunities

When multiple agents or sessions are available:

- **Safe to parallelize:** Independent feature slices, tests for already-implemented features, documentation
- **Must be sequential:** Database migrations, shared state changes, dependency chains
- **Needs coordination:** Features that share an API contract (define the contract first, then parallelize)
```

**翻译:**
```markdown
## 并行化机会

当有多个智能体会话可用时：

- **可以安全并行：** 独立的功能切片、已实现功能的测试、文档
- **必须串行：** 数据库迁移、共享状态变更、依赖链
- **需要协调：** 共享 API 契约的功能（先定义契约，再并行）
```

**要点:**
- **为什么重要**: 在多智能体协作的场景下，错误的并行化会导致冲突和损坏。这一段提供了清晰的并行化规则，防止"为了并行而并行"。
- **隐含意义**: "Needs coordination" 类别特别重要。它识别了中间状态 —— 不是绝对安全，也不是绝对禁止，而是需要额外的协调机制（如先定义 API 契约）。
- **可执行建议**: 在计划文档中，为每个任务标注并行化类别。如果有两个任务都标记为"Needs coordination"，确保它们有一个"定义契约"的前置任务。

---

### 段落 13: Common Rationalizations

**原文:**
```markdown
## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll figure it out as I go" | That's how you end up with a tangled mess and rework. 10 minutes of planning saves hours. |
| "The tasks are obvious" | Write them down anyway. Explicit tasks surface hidden dependencies and forgotten edge cases. |
| "Planning is overhead" | Planning is the task. Implementation without a plan is just typing. |
| "I can hold it all in my head" | Context windows are finite. Written plans survive session boundaries and compaction. |
```

**翻译:**
```markdown
## 常见借口

| 借口 | 现实 |
|---|---|
| "我会边做边想" | 这就是你最终得到一团糟和返工的原因。10 分钟的计划节省数小时。 |
| "任务很明显" | 还是写下来。明确的任务能暴露隐藏的依赖和被遗忘的边界情况。 |
| "计划是开销" | 计划本身就是任务。没有计划的实现只是在打字。 |
| "我能在脑子里记住所有东西" | 上下文窗口是有限的。书面计划能跨越会话边界和压缩而存活。 |
```

**要点:**
- **为什么重要**: 与 `spec-driven-development` 中的 Common Rationalizations 类似，这一段是心理防御机制。它预见到开发者会找理由跳过计划，并提前准备好反驳。
- **隐含意义**: "Context windows are finite" 这句话特别针对 AI 场景。它提醒我们：即使 AI 能"记住"很多事情，它的上下文窗口是有限的，而且会话结束后记忆会丢失。书面计划是跨越这些限制的唯一方式。
- **可执行建议**: 当团队有人说"这个不需要计划"时，引用第四点："你能记住，但 AI 记不住。" 这不是侮辱，而是客观事实。

---

### 段落 14: Red Flags

**原文:**
```markdown
## Red Flags

- Starting implementation without a written task list
- Tasks that say "implement the feature" without acceptance criteria
- No verification steps in the plan
- All tasks are XL-sized
- No checkpoints between tasks
- Dependency order isn't considered
```

**翻译:**
```markdown
## 危险信号

- 在没有书面任务清单的情况下开始实现
- 任务只写"实现功能"而没有验收标准
- 计划中没有验证步骤
- 所有任务都是 XL 尺寸
- 任务之间没有检查点
- 没有考虑依赖顺序
```

**要点:**
- **为什么重要**: 这些是计划层面的预警信号。它们比代码 smells 更严重，因为它们位于流程的源头。如果这些信号出现，后续的代码质量几乎必然受损。
- **隐含意义**: "Tasks that say 'implement the feature' without acceptance criteria" 是最常见的反模式。它把任务当成了标题，而不是可执行的指令。验收标准的缺失意味着"完成"的定义是模糊的。
- **可执行建议**: 将这段作为代码审查的一部分。在审查 PR 时，检查其对应的任务是否有验收标准和验证步骤。

---

### 段落 15: Verification

**原文:**
```markdown
## Verification

Before starting implementation, confirm:

- [ ] Every task has acceptance criteria
- [ ] Every task has a verification step
- [ ] Task dependencies are identified and ordered correctly
- [ ] No task touches more than ~5 files
- [ ] Checkpoints exist between major phases
- [ ] The human has reviewed and approved the plan
```

**翻译:**
```markdown
## 验证

在开始实现之前，确认：

- [ ] 每个任务都有验收标准
- [ ] 每个任务都有验证步骤
- [ ] 任务依赖已识别并正确排序
- [ ] 没有任务触及超过约 5 个文件
- [ ] 主要阶段之间存在检查点
- [ ] 人工已审核并批准计划
```

**要点:**
- **为什么重要**: 这是计划阶段的最终检查点。它是一个强制性的 checklist，确保所有前置条件都已满足。最后一项再次强调了人类审核的必要性。
- **隐含意义**: "No task touches more than ~5 files" 是一个量化质量门。它与前面的任务尺寸指南形成闭环，确保计划在进入实现阶段前已经过"尺寸检查"。
- **可执行建议**: 在每次 `/plan` 完成后，物理地勾选这个清单。不要凭感觉认为"应该没问题"。

---

## Step 3: 整体总结

### 核心概念

| 概念 | 定义 |
|------|------|
| **Vertical Slicing**（垂直切片） | 按用户场景（如"注册"）而非技术层（如"数据库"）拆解任务，每个切片都交付端到端的可工作功能。 |
| **Dependency Graph**（依赖图） | 组件之间的依赖关系映射，决定实现顺序（自底向上）。 |
| **Checkpoint**（检查点） | 每 2-3 个任务后的强制停止点，用于验证系统状态并获得人类反馈。 |
| **Task Sizing**（任务尺寸） | XS/S/M/L/XL 五级分类，XL 必须拆分，S 和 M 是 AI 的最佳工作范围。 |
| **Plan Mode**（计划模式） | 只读、不编码的模式，产出是计划文档而非代码。 |
| **Fail Fast**（快速失败） | 高风险任务应该排在前面，以便尽早发现问题，减少浪费。 |

### 工作流程

```
开始
  │
  ▼
已有规格或清晰需求？
  │
  ├── 否 → 先调用 /spec（spec-driven-development）
  │
  └── 是 → 进入计划流程
            │
            ▼
      ┌─────────────────┐
      │ 1. Enter Plan   │ ← 只读模式：读规格、读代码、识别模式
      │    Mode         │
      └────────┬────────┘
               │
               ▼
      ┌─────────────────┐
      │ 2. Dependency   │ ← 绘制组件依赖图（数据库 → 模型 → API → UI）
      │    Graph        │
      └────────┬────────┘
               │
               ▼
      ┌─────────────────┐
      │ 3. Slice        │ ← 垂直切片：按用户场景而非技术层拆解
      │    Vertically   │
      └────────┬────────┘
               │
               ▼
      ┌─────────────────┐
      │ 4. Write Tasks  │ ← 使用标准模板编写任务（描述/验收/验证/依赖/文件/尺寸）
      └────────┬────────┘
               │
               ▼
      ┌─────────────────┐
      │ 5. Order &      │ ← 按依赖排序、设置检查点、高风险优先
      │    Checkpoint   │
      └─────────────────┘
```

### 关键文件

| 文件 | 作用 |
|------|------|
| `skills/planning-and-task-breakdown/SKILL.md` | 本 skill 的定义文件，包含 5 步计划流程和任务模板 |
| `docs/agent-skills/02-planning-and-task-breakdown-analysis.md` | 本分析文件，提供对 SKILL.md 的逐段精读和总结 |

### 与其他 Skill 的关系

- **前置**: `spec-driven-development`（必须先有规格，才能拆解任务）
- **后置/协同**: 
  - `incremental-implementation`（按任务逐个实现）
  - `test-driven-development`（每个任务都用 TDD 实现）
  - `context-engineering`（加载正确的上下文以执行任务）

### 使用建议

1. **垂直切片是核心原则** — 如果你只记住一件事，记住"按用户场景切片，而不是按技术层切片"。
2. **XL 任务零容忍** — 任何预计触及 8+ 文件或需要 2+ 小时的任务，自动拆分。
3. **检查点不是装饰** — 每 2-3 个任务后必须停下来验证。这是防止"做了半天发现方向错了"的唯一机制。
4. **计划期间绝不编码** — 即使你很确定某行代码怎么写，也等到计划被批准后再写。计划阶段的产出是文档，不是代码。
5. **把计划当作版本控制产物** — 计划文档属于仓库，应该在实现过程中持续更新，而不是一次性使用后丢弃。
