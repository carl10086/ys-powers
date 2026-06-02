# ys-powers 演进指南：基于 GSD 工程化思想的优化

> 本文档是 `specs/2026-06-01-gsd-inspired-optimization-design.md` 的配套参考手册，面向 ys-powers 用户和维护者。
>
> 阅读对象：已熟悉 ys-powers 基础使用的开发者，希望了解新增能力和使用方法。

---

## 目录

1. [概述](#概述)
2. [Commands 参考](#commands-参考)
3. [Skills 参考](#skills-参考)
4. [Agents 参考](#agents-参考)
5. [Rules 参考](#rules-参考)
6. [快速开始](#快速开始)
7. [迁移指南](#迁移指南)
8. [Roadmap](#roadmap)

---

## 概述

### 演进背景

ys-powers 是一套面向 Claude Code 的轻量工作流增强系统。在长期使用中，我们发现以下痛点：

- **执行走偏**：模型声称"完成"，但实际留下 stub 代码或未连接的死代码
- **计划不可执行**：生成的 plan 缺少验收标准，或任务粒度过大
- **上下文腐烂**：长会话中模型逐渐遗忘早期决策
- **质量无保障**：缺少系统化的验证和质量门机制

通过对 `refer/get-shit-done`（GSD）的深度分析，我们提取了其工程化思想中最适合 ys-powers「纯配置、无运行时、中文优先」定位的借鉴点，在不增加系统重量的前提下，提升准确性、能力和质量保障。

### 设计原则

| 原则 | 说明 |
|------|------|
| **吸收思想，不复制复杂度** | 学习 GSD 的验证机制、Agent 合约、质量门思想，但不引入其 SDK/CLI/状态系统 |
| **纯配置，无运行时** | 所有新增内容都是 Markdown + YAML frontmatter，不依赖任何运行时环境 |
| **中文优先** | 用户可见文本全中文，技术术语保留英文 |
| **渐进启用** | 新功能默认关闭或可选（`--flag`），不强制改变现有工作流 |
| **向后兼容** | 所有现有命令和技能保持不变 |

### 与 GSD 的关系

```
GSD（重型框架）
├── Node.js CLI + SDK
├── .planning/ 状态系统
├── 86+ 命令
├── 34 个 Agent
└── 15 运行时兼容

    ↓ 提取思想，去掉复杂度

ys-powers（轻量增强）
├── Markdown + YAML 配置
├── 无状态系统
├── 25+ 命令（+5 命名空间路由）
├── 7 个 Agent（+4 新增）
└── 仅 Claude Code
```

### 术语表

| 术语 | 英文 | 说明 |
|------|------|------|
| 验证模式 | Verification Patterns | 检查代码是否真实实现，而非 stub/占位符 |
| Agent 合约 | Agent Contracts | Subagent 间传递信息的标准格式和完成标记 |
| 修订循环 | Revision Loop | 发现问题 → 自动修订 → 最多 3 轮 → 升级用户 |
| 质量门 | Quality Gate | 在关键节点强制检查，防止问题漏出 |
| 命名空间路由 | Namespace Meta-Skills | 将命令按功能域分组，降低 token 消耗 |
| 四层验证 | Four-Level Verification | 存在 → 实质 → 连接 → 功能 |

---

## Commands 参考

### `/verify`

**定位**：通用验证命令，检测 stub/placeholder/TODO 等幻觉痕迹。

**用法**：
```bash
/verify <path> [--deep] [--strict]
```

**参数**：

| 参数 | 必填 | 说明 |
|------|------|------|
| `path` | 是 | 要验证的文件或目录路径 |
| `--deep` | 否 | 启用第四层「功能验证」（尝试运行测试或构建） |
| `--strict` | 否 | 将 WARNING 升级为 BLOCKER |

**执行流程**：
1. 扫描目标路径的所有代码文件
2. 应用 stub 检测规则集（grep 模式匹配）
3. 检查文件是否被引用/导入（连接层）
4. （`--deep` 时）尝试运行相关测试或构建
5. 输出验证报告，按 BLOCKER / WARNING / INFO 分级

**示例**：
```bash
/verify src/utils/auth.ts
/verify src/ --deep --strict
```

**输出示例**：
```markdown
## 验证报告: src/utils/auth.ts

| 层级 | 状态 | 发现 |
|------|------|------|
| 存在 | PASS | 文件存在 |
| 实质 | BLOCKER | 发现 3 处 TODO + 1 处 `return null` |
| 连接 | PASS | 被 4 个文件引用 |
| 功能 | WARNING | 测试覆盖率 45%，低于阈值 70% |

### Blockers
- [ ] L23: `// TODO: implement refresh token`
- [ ] L45: `return null; // placeholder`
```

**使用场景**：
- 提交前自检
- `/ship` 前强制验证（集成到 fan-out）
- 怀疑模型留下 stub 时主动检查

---

### `/build --tdd`

**定位**：TDD 强制模式，在标准 `/build` 流程中嵌入红绿循环。

**用法**：
```bash
/build [--tdd] [--task <n>]
```

**新增 Flag**：

| Flag | 说明 |
|------|------|
| `--tdd` | 启用 TDD 模式 |

**TDD 执行流程**：
1. **RED**：先写 failing test（禁止写任何实现代码）
2. 确认 test 失败
3. **GREEN**：写最小实现使 test 通过
4. **REFACTOR**：清理代码，保持测试通过
5. 提交：`test(task-N): add failing test for <criteria>`
6. 提交：`feat(task-N): implement <criteria>`

**中断条件**：
- 如果跳过 RED 步骤直接写实现，立即中断并提示用户
- 如果 failing test 无法写出（如纯 UI 调整），需用户确认豁免

**示例**：
```bash
/build --tdd              # 当前任务启用 TDD
/build --tdd --task 3     # 指定任务 3 启用 TDD
```

**使用场景**：
- 新功能开发时确保测试先行
- 代码质量要求高的项目
- 团队协作中统一测试规范

---

### `/health`

**定位**：项目健康检查 + 上下文利用率监控。

**用法**：
```bash
/health [--context]
```

**检查项**：

| 维度 | 检查内容 | 健康标准 |
|------|----------|----------|
| 配置完整 | `.claude/skills/`、`commands/`、`rules/` 是否存在 | 全部存在 |
| Skill 同步 | 本地 skills 与 ys-powers 最新版本差异 | 无重大差异 |
| 上下文利用率 | 当前会话 tokens used / context window | < 60% healthy, 60-70% warning, ≥70% critical |
| 未提交变更 | 工作区是否有未提交修改 | 无（或用户确认） |

**`--context` 输出示例**：
```markdown
## 上下文利用率

已用: 42,000 / 200,000 tokens (21%)
状态: healthy
建议: 无需操作

## 配置健康

✓ skills/ 目录存在 (12 skills)
✓ commands/ 目录存在 (20 commands)
⚠ rules/context7.md 落后于上游版本
  建议: 运行 `make install` 同步
```

**使用场景**：
- 会话开始时快速检查环境
- 感觉模型响应变慢时检查上下文利用率
- 发现 skills 行为异常时检查配置完整性

---

### `/spec --template`

**定位**：基于 spec 内容自动生成 CLAUDE.md 项目规范。

**用法**：
```bash
/spec [--template]
```

**新增 Flag**：

| Flag | 说明 |
|------|------|
| `--template` | 在 spec 完成后生成 CLAUDE.md |

**执行流程**：
```
Phase 3 完成 → 保存 spec 文件
    │
    ▼
询问: "需要基于本 spec 生成 CLAUDE.md 项目规范吗？"
    │
    ├── 是 → 生成 CLAUDE.md → 询问保存路径 → 保存
    └── 否 → 结束
```

**CLAUDE.md 模板内容**：
```markdown
# CLAUDE.md

## 项目概述
[从 spec Objective 提取]

## 目录结构
[从 spec Project Structure 提取]

## 代码风格
[从 spec Code Style 提取]

## 测试策略
[从 spec Testing Strategy 提取]

## 常用命令
[从 spec Commands 提取]

## 边界
[从 spec Boundaries 提取]
```

**使用场景**：
- 新项目初始化时快速生成项目规范
- 现有项目补充 CLAUDE.md
- 团队标准化项目文档

---

### `/spec --ambiguity-check`

**定位**：Spec 模糊度自检，定量化评估需求清晰度。

**用法**：
```bash
/spec [--ambiguity-check]
```

**评估维度**：

| 维度 | 说明 |
|------|------|
| 目标清晰度 | 用户想要什么是否明确 |
| 范围边界 | 做什么/不做什么是否清晰 |
| 验收标准 | 成功标准是否具体可测量 |
| 技术约束 | 框架/语言/依赖是否明确 |

**评分标准**：
- 综合模糊度 ≤ 0.20：直接生成 spec
- 综合模糊度 0.20 - 0.30：提示某些维度可优化
- 综合模糊度 > 0.30：建议继续澄清

**使用场景**：
- 需求复杂或模糊时，确保 spec 质量
- 团队协作中统一对需求的理解

---

### 命名空间路由命令

**定位**：将命令按功能域分组，降低技能列表 token 消耗。

**命令列表**：

| 命令 | 包含子命令 | 说明 |
|------|-----------|------|
| `/ys-workflow` | spec, plan, build, test, ship | 核心工作流 |
| `/ys-code` | ys-review, code-simplify, refactor, html | 代码质量 |
| `/ys-info` | scout, doc-codebase, easy-analysis, teach-code | 信息探索 |
| `/ys-git` | gc, local-commit, s2m | Git 工作流 |
| `/ys-manage` | alias, wskill, sop-add | 管理工具 |

**使用方式**：
```bash
/ys-workflow     # 显示 workflow 子命令列表
/spec            # 直接调用（不受影响）
```

**向后兼容**：所有原子命令保持不变，命名空间命令是 additive。

**使用场景**：
- 新用户快速了解命令体系
- 命令较多时减少 token 消耗

---

## Skills 参考

### `verification-patterns`

**定位**：通用验证框架，防止「存在≠实现」的幻觉。

**核心原则**：
```markdown
## 存在 ≠ 实现

验证必须检查四层：
1. **Exists** — 文件存在于预期路径
2. **Substantive** — 内容是真实实现，非占位符
3. **Wired** — 与系统其余部分有连接
4. **Functional** — 实际运行时可用
```

**Stub 检测规则集**：

| 类别 | 检测模式 | 示例 |
|------|----------|------|
| 注释类 stub | `TODO\|FIXME\|XXX\|HACK\|PLACEHOLDER` | `// TODO: implement` |
| 空实现 | `return null\|return undefined\|return {}` | `return null;` |
| 硬编码值 | 硬编码 ID、count、length | `id = "12345"` |
| UI 占位符 | `placeholder\|lorem ipsum\|coming soon` | `<div>Coming soon</div>` |

**使用方式**：
- 被 `/verify` 命令内部调用
- 被 `/ship` fan-out 评审时调用
- 手动调用：`Invoke the verification-patterns skill`

---

### `agent-contracts`

**定位**：Agent 完成标记与 handoff 合约规范，确保 subagent 间信息传递可靠。

**完成标记规范**：

| 标记 | 含义 | 使用场景 |
|------|------|----------|
| `## TASK COMPLETE` | 任务成功完成 | 所有正常完成的 subagent |
| `## CHECKPOINT REACHED` | 需要用户决策 | 遇到不确定性的 subagent |
| `## TASK BLOCKED` | 任务被阻塞 | 缺少信息或权限的 subagent |
| `## ESCALATE` | 需要升级处理 | 发现严重问题的 subagent |

**Handoff 合约**：

**Planner → Executor**：
- frontmatter（task, acceptance, verify）
- `<objective>`：任务目标
- `<tasks>`：有序任务列表
- `<verification>`：验证步骤

**Executor → Verifier**：
- frontmatter（task, files_modified, metrics）
- `<summary>`：执行摘要
- `<deviations>`：偏离计划的部分及原因

**使用方式**：
- 所有使用 `Agent` tool spawn subagent 的命令必须遵循
- `/ship` 的 fan-out 评审中强制执行

---

### `revision-loop`

**定位**：检查-修订-升级循环，自动修正问题，不自欺欺人。

**核心模式**：

```
prev_issue_count = Infinity
iteration = 0

LOOP:
  1. 运行 checker 评估当前输出
  2. 如果 PASSED 或只有 INFO：接受，退出
  3. 如果有 BLOCKER 或 WARNING：
     a. iteration += 1
     b. 如果 iteration > 3：升级给用户
     c. 如果 issue_count >= prev_issue_count：升级（修订停滞）
     d. prev_issue_count = issue_count
     e. 用 checker 反馈重新 spawn producer
     f. 回到 LOOP
```

**反馈格式**：
```yaml
checker_issues:
  - dimension: 完整性
    severity: BLOCKER
    finding: "缺少 acceptance criteria"
    suggested_fix: "补充：'Acceptance: API 返回 201 状态码'"
```

**使用方式**：
- `/plan` 后自动运行 plan-checker（可选）
- `/build` 失败后的自动修复尝试
- `/ship` 前 code-reviewer 发现问题后的自动修订

---

### `gate-prompts`

**定位**：结构化决策 gate 模式，减少歧义和决策疲劳。

**模式库**：

| 模式 | 选项 | 使用场景 |
|------|------|----------|
| approve-revise-abort | 批准 \| 请求修改 \| 中止 | plan 审批、gap closure |
| yes-no | 是 \| 否 | 重新规划、提交确认 |
| stale-continue | 刷新 \| 继续 | 过时警告、时间戳检查 |
| multi-option-failure | 重试 \| 跳过 \| 回滚 \| 中止 | 构建失败 |
| multi-option-gaps | 自动修复 \| 覆盖 \| 手动 \| 跳过 | 验证发现 gaps |

**约束**：
- header 最多 12 个字符
- 每 prompt 最多 4 个选项
- 必须处理 "Other"（用户输入自定义回复）

**使用方式**：
- 嵌入到所有需要用户决策的命令中
- `/spec` 的假设确认步骤
- `/build` 的 checkpoint 暂停

---

### `context-management`

**定位**：上下文窗口管理与 context rot 缓解。

**Context Rot 信号**：
- 会话超过 30 轮
- 模型开始重复之前的回答
- 模型忘记了会话早期的关键决策
- 响应质量明显下降

**应对措施**：

| 严重程度 | 措施 |
|----------|------|
| 轻度（20-30 轮） | 主动总结关键决策，要求用户确认 |
| 中度（30-50 轮） | 建议保存当前状态到文件，然后 `/clear` |
| 重度（>50 轮） | 强制建议开启新会话，加载 plan 文件恢复上下文 |

**预防性措施**：
- 每 10 轮主动做一次「决策回顾」
- 将关键决策写入文件（用户自行管理路径）
- 复杂任务拆分为多个会话

**使用方式**：
- `/health --context` 内部调用
- 手动调用：`Invoke the context-management skill`

---

### `context-engineering`（强化）

**定位**：优化上下文加载策略，减少 token 浪费。

**Right Context at Right Time 原则**：

| 阶段 | 加载内容 | 避免加载 |
|------|----------|----------|
| 探索 | 项目结构、README、最近提交 | 全部源码 |
| 规划 | Spec 相关章节、依赖模块接口 | 实现细节 |
| 实现 | 当前任务涉及的文件 + 直接依赖 | 无关模块 |
| 验证 | 测试文件 + 被测代码 | 未变更文件 |

**Context 预算分配**：
- Orchestrator（主会话）：~15% context budget
- Subagent（每次 spawn）：100% fresh context

**使用方式**：
- 大项目操作时自动建议
- 上下文利用率 ≥70% 时触发

---

## Agents 参考

### `plan-checker`

**定位**：验证 plan 的可执行性和完整性。

**触发方式**：
- `/plan` 完成后自动执行：`/plan --verify`
- 手动调用：作为 subagent spawn

**验证维度**：

| 维度 | 检查内容 | 标准 |
|------|----------|------|
| 完整性 | 每个任务是否有 acceptance criteria | 必须有 |
| 可达性 | 任务依赖是否形成循环 | 必须无循环 |
| 粒度 | 每个任务是否可在一个会话内完成 | 建议 ≤5 文件 |
| 验证 | 每个任务是否有 verify 步骤 | 必须有 |
| 一致性 | 任务是否与 spec 一致 | 必须一致 |

**输出格式**：
```yaml
## VERIFICATION PASSED
# 或
## ISSUES FOUND

issues:
  - dimension: 完整性
    severity: BLOCKER
    task: "Task 3"
    finding: "缺少 acceptance criteria"
    suggested_fix: "补充：'Acceptance: API 返回 201 状态码'"
```

**严重级别**：
- **BLOCKER**：必须修复，否则计划不可执行
- **WARNING**：建议修复，但不阻塞执行
- **INFO**：参考信息

---

### `debugger`

**定位**：系统化诊断和修复代码问题。

**触发方式**：
- `/build` 失败时自动调用
- 手动调用：`/debug <error-message>`

**调试流程**：
1. **信息收集**：错误消息、堆栈、相关代码、最近变更、环境信息
2. **假设生成**：列出 3-5 个可能的 root cause，按可能性排序
3. **假设验证**：对每个假设设计验证方法并运行
4. **修复方案**：针对确认的 root cause 提出修复方案，评估副作用
5. **输出**：root cause 分析、修复方案、预防建议

**输出标记**：
- `## DEBUG COMPLETE` — 调试完成
- `## ROOT CAUSE FOUND` — 找到 root cause
- `## CHECKPOINT REACHED` — 需要用户决策

---

### `spec-reviewer`

**定位**：评审 spec 的完整性和质量。

**触发方式**：
- `/spec` 完成后可选执行：`/spec --review`
- 手动调用评审现有 spec

**评审维度**：

| 维度 | 检查内容 |
|------|----------|
| 六域覆盖 | Objective、Commands、Structure、Style、Testing、Boundaries 是否齐全 |
| 可测试性 | Success Criteria 是否具体、可测量 |
| 无歧义 | 是否存在多个合理解读 |
| 边界清晰 | Always/Ask First/Never 是否明确 |
| 一致性 | 各章节之间是否矛盾 |

**输出格式**：
```yaml
## SPEC REVIEW COMPLETE

score: 85/100

strengths:
  - "Objective 清晰，用户场景明确"

gaps:
  - dimension: 可测试性
    severity: WARNING
    finding: "Success Criteria 中 '提升准确性' 不够具体"
    suggested_fix: "改为 'stub 代码残留率从 X% 降到 Y%'"
```

---

### `context-engineer`

**定位**：优化上下文加载策略，减少 token 浪费。

**触发方式**：
- 大项目操作时建议调用
- 上下文利用率 ≥70% 时自动建议

**分析维度**：
1. **冗余检测**：重复加载的代码文件、过时的上下文信息
2. **加载策略**：当前任务是否只需要接口而非实现
3. **分 Session 建议**：工作是否应拆分为多个会话

**输出示例**：
```markdown
## CONTEXT ANALYSIS COMPLETE

当前利用率: 78% (critical)

冗余发现:
- `src/utils/helpers.ts` 已加载但当前任务不涉及
- 第 3-10 轮的讨论已过时

优化建议:
1. `/clear` 后重新加载，只保留 plan 文件
2. 将当前任务拆分为 2 个会话
3. 使用 `Read` 的 offset/limit 只读取代码片段

预估优化后利用率: 35%
```

---

## Rules 参考

### `rules/verification.md`

**核心规则**：

```markdown
## 验证规则

### Rule 1: 存在 ≠ 实现
文件存在不代表功能完成。每次声称"完成"后，必须运行验证检查。

### Rule 2: Stub 检测清单
提交前检查代码中是否有：
- TODO / FIXME / XXX / PLACEHOLDER
- `return null` 或空实现
- 硬编码值（应动态获取的地方）
- 模板括号残留

### Rule 3: 四层验证
复杂任务必须通过四层验证：
1. 文件存在
2. 内容实质性（非 stub）
3. 与系统连接（被引用/导入）
4. 功能可用（测试通过或可运行）
```

**适用范围**：所有生成代码的场景。

---

### `rules/agent-contracts.md`

**核心规则**：

```markdown
## Agent 合约规则

### Rule 1: 完成标记
所有 spawn 的 subagent 必须在最终输出中包含完成标记：
- `## TASK COMPLETE` — 成功
- `## CHECKPOINT REACHED` — 需用户决策
- `## TASK BLOCKED` — 被阻塞
- `## ESCALATE` — 需升级

### Rule 2: Handoff 完整性
Agent 间传递信息时，必须包含：
- 前序 Agent 的完成标记
- 相关上下文摘要
- 明确的下一步指令

### Rule 3: 修订循环
当 checker 发现问题时：
- 最多尝试 3 轮修订
- 如果问题数不减少，立即升级给用户
- 不要无限循环
```

**适用范围**：所有使用 `Agent` tool spawn subagent 的场景。

---

## 快速开始

### 第一步：安装最新版本

```bash
cd /path/to/ys-powers
make install
```

### 第二步：验证安装

```bash
/health
```

预期输出：
```markdown
✓ skills/ 目录存在
✓ commands/ 目录存在
✓ rules/ 目录存在
状态: healthy
```

### 第三步：试用新能力

**场景 1：提交前验证**
```bash
/verify src/ --deep
```

**场景 2：TDD 模式开发**
```bash
/build --tdd
```

**场景 3：生成项目规范**
```bash
/spec --template
```

**场景 4：健康检查**
```bash
/health --context
```

---

## 迁移指南

### 从现有版本迁移

**无需迁移步骤。** 所有新增功能都是 additive：

- 现有命令不变
- 现有技能不变
- 新增功能默认关闭（`--flag` 启用）

**唯一变化**：安装后会新增文件到 `.claude/` 目录。

### 逐步启用建议

| 阶段 | 启用功能 | 预期收益 |
|------|----------|----------|
| 第 1 周 | `/verify` + `rules/verification.md` | 减少 stub 残留 |
| 第 2 周 | `/build --tdd` | 提升测试覆盖率 |
| 第 3 周 | `/health --context` | 缓解 context rot |
| 第 4 周 | `plan-checker` Agent | 提升 plan 质量 |

### 回滚策略

如果某个新增功能导致问题：
1. 删除对应的 `.claude/skills/` 或 `.claude/commands/` 文件
2. 重新运行 `make install` 同步

---

## Roadmap

### Phase 1（1-2 周）：准确性基础

| 任务 | 产出 |
|------|------|
| 1.1 | `skills/verification-patterns/SKILL.md` |
| 1.2 | `commands/verify.md` |
| 1.3 | `skills/agent-contracts/SKILL.md` |
| 1.4 | `rules/agent-contracts.md` |
| 1.5 | `skills/revision-loop/SKILL.md` |
| 1.6 | `skills/gate-prompts/SKILL.md` |
| 1.7 | `commands/build.md`（增加 `--tdd`） |
| 1.8 | `commands/spec.md`（增加 `--ambiguity-check` + `--template`） |

**验证**：在 2 个真实项目中试用 `/verify` 和 `/build --tdd`，收集反馈。

### Phase 2（2-4 周）：能力扩展

| 任务 | 产出 |
|------|------|
| 2.1 | `agents/plan-checker.md` |
| 2.2 | `agents/debugger.md` |
| 2.3 | `agents/spec-reviewer.md` |
| 2.4 | `commands/health.md` |
| 2.5 | `skills/context-management/SKILL.md` |
| 2.6 | `skills/context-engineering/SKILL.md`（强化） |

**验证**：在 `/ship` 中集成 plan-checker，对比评审效果。

### Phase 3（1-2 月）：质量门强化

| 任务 | 产出 |
|------|------|
| 3.1 | `commands/ys-workflow.md` |
| 3.2 | `commands/ys-code.md` |
| 3.3 | `commands/ys-info.md` |
| 3.4 | `commands/ys-git.md` |
| 3.5 | `commands/ys-manage.md` |
| 3.6 | `rules/verification.md` |
| 3.7 | `commands/ship.md`（集成 `/verify`） |

**验证**：测量命名空间命令的使用频率 vs 原子命令。

### Phase 4（可选）：效率优化

| 任务 | 产出 |
|------|------|
| 4.1 | `agents/context-engineer.md` |
| 4.2 | 上下文利用率监控（集成到 `/health`） |
| 4.3 | Model Profiles 调研 |

**验证**：测量大项目（>100 文件）中的会话轮数变化。

---

## 附录：GSD 借鉴点索引

| 本文档内容 | GSD 来源 | 适配方式 |
|------------|----------|----------|
| Verification Patterns | `references/verification-patterns.md` | 精简为 skill，去掉 .planning 依赖 |
| Agent Contracts | `references/agent-contracts.md` | 保留核心标记规范，去掉 SDK 合约 |
| Revision Loop | `references/revision-loop.md` | 保留 3 轮循环逻辑，YAML 反馈格式 |
| Gate Prompts | `references/gate-prompts.md` | 保留模式库，适配中文语境 |
| TDD Gate | `references/execute-mvp-tdd.md` | 简化为 `/build --tdd` flag |
| Health Check | `commands/gsd/health.md` | 去掉 .planning 依赖，改为通用诊断 |
| Namespace Meta-Skills | `docs/COMMANDS.md` namespace 章节 | 简化为 5 个路由命令 |
| Model Profiles | `references/model-profiles.md` | 待调研可行性后实施 |

---

*文档版本: v1.0*
*对应 Spec: `specs/2026-06-01-gsd-inspired-optimization-design.md`*
*创建日期: 2026-06-01*
