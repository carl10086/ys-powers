# Spec: 基于 GSD 思路优化 ys-powers

## Objective

基于对 `refer/get-shit-done` 的深度分析，提取其工程化思想中最适合 ys-powers「纯配置、无运行时、中文优先」定位的借鉴点，通过新增 skills、commands、agents 和 rules，系统性地提升 ys-powers 的**执行准确性、能力覆盖度、质量保障力和上下文效率**。

**核心原则：** 吸收思想，不复制复杂度。保持 ys-powers 的轻量本质，不做任何运行时改造，不引入状态系统。

**成功定义：** 三个月后，使用 ys-powers 的项目在「模型执行走偏率」「stub 代码残留率」「plan 可执行率」三个指标上明显改善，且用户无明显感知到系统变重。

---

## Tech Stack

- **配置格式：** Markdown + YAML frontmatter（保持现有）
- **脚本语言：** Python 3.12+（`install/local-install.py`）
- **构建工具：** `uv` + `Makefile`（现有）
- **版本控制：** Git
- **目标运行时：** Claude Code（ primary），其他运行时暂不考虑

---

## Commands

### P0 准确性 — 新增/强化命令

#### `/verify`（新增）

**定位：** 通用验证命令，对标 GSD 的 Verification Patterns。

**描述：** 对指定文件或目录执行四层验证（存在→实质→连接→功能），检测 stub/placeholder/TODO 等幻觉痕迹。

**用法：**
```bash
/verify <path> [--deep] [--strict]
```

**Flags：**
- `--deep`：启用第四层「功能验证」（尝试运行/调用）
- `--strict`：将 WARNING 升级为 BLOCKER

**执行流程：**
1. 扫描目标路径的所有代码文件
2. 应用 stub 检测规则集（grep 模式）
3. 检查文件是否被引用/导入（连接层）
4. （`--deep` 时）尝试运行相关测试或构建
5. 输出验证报告，按 BLOCKER / WARNING / INFO 分级

**示例输出：**
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

**实现方式：** 新增 `commands/verify.md`，调用 `skills/verification-patterns/SKILL.md`。

---

#### `/build --tdd`（扩展现有 `/build`）

**定位：** TDD 强制模式，对标 GSD 的 MVP+TDD Gate。

**描述：** 在标准 `/build` 流程基础上，强制执行「先写 failing test，再实现，再重构」的红绿循环。

**用法：**
```bash
/build [--tdd] [--task <n>]
```

**`--tdd` 执行流程：**
1. 读取当前任务的 acceptance criteria
2. **RED：** 先写 failing test（禁止写任何实现代码）
3. 确认 test 失败（截图/输出验证）
4. **GREEN：** 写最小实现使 test 通过
5. **REFACTOR：** 清理代码，保持测试通过
6. 提交：`test(task-N): add failing test for <criteria>`
7. 提交：`feat(task-N): implement <criteria>`
8. 继续下一任务

**中断条件：**
- 如果跳过 RED 步骤直接写实现，立即中断并提示用户
- 如果 failing test 无法写出（如纯 UI 调整），需用户确认豁免

**实现方式：** 修改 `commands/build.md`，在 incremental-implementation skill 调用前插入 TDD 分支逻辑。

---

### P1 能力覆盖 — 新增命令

#### `/health`（新增）

**定位：** 项目健康检查 + 上下文利用率监控，对标 GSD 的 `/gsd-health`。

**描述：** 诊断当前项目的 ys-powers 配置健康度和会话上下文利用率。

**用法：**
```bash
/health [--context]
```

**检查项：**

| 维度 | 检查内容 | 健康标准 |
|------|----------|----------|
| 配置完整 | `.claude/skills/`、`commands/`、`rules/` 是否存在 | 全部存在 |
| Skill 同步 | 本地 skills 与 ys-powers 最新版本差异 | 无重大差异 |
| 上下文利用率 | 当前会话 tokens used / context window | < 60% healthy, 60-70% warning, ≥70% critical |
| 未提交变更 | 工作区是否有未提交修改 | 无（或用户确认） |

**`--context` 输出：**
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

**实现方式：** 新增 `commands/health.md`，调用 Bash 检查目录和 git 状态。

---

#### `/spec --template`（扩展现有 `/spec`）

**定位：** 基于 spec 生成 CLAUDE.md 模板，对标 GSD 的 new-project 脚手架。

**描述：** 在 `/spec` 的 Phase 3 完成后，询问用户是否基于 spec 内容生成 `CLAUDE.md` 项目规范。

**新增流程：**
```
Phase 3 完成 → 保存 spec 文件
    │
    ▼
询问: "需要基于本 spec 生成 CLAUDE.md 项目规范吗？"
    │
    ├── 是 → 生成 CLAUDE.md → 询问保存路径 → 保存
    └── 否 → 结束
```

**CLAUDE.md 模板内容（自动生成）：**
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

**实现方式：** 修改 `commands/spec.md`，在保存 spec 后增加 CLAUDE.md 生成步骤。

---

### P2 质量门 — 新增命令

#### `/ys-workflow`（新增）

**定位：** Namespace Meta-Skill 路由，对标 GSD 的 `/gsd-workflow`。

**描述：** 将现有 20 个命令按功能域分组，降低技能列表 token 消耗。

**子命令映射：**

```
/ys-workflow
├── spec, plan, build, test, ship

/ys-code
├── ys-review, code-simplify, refactor, html

/ys-info
├── scout, doc-codebase, easy-analysis, teach-code

/ys-git
├── gc, local-commit, s2m

/ys-manage
├── alias, wskill, sop-add
```

**内容格式：**
```yaml
---
description: ys-powers workflow 命名空间路由 — spec/plan/build/test/ship
---

## /ys-workflow

快速访问 ys-powers 核心工作流命令：

| 命令 | 描述 |
|------|------|
| `/spec` | 启动 spec-driven 开发 |
| `/plan` | 基于 spec 拆解任务 |
| `/build` | 增量实现 + TDD |
| `/test` | 运行测试工作流 |
| `/ship` | 交付前 fan-out 评审 |

所有命令仍可独立调用。
```

**实现方式：** 在 `commands/` 下新增 5 个命名空间命令文件（`ys-workflow.md`、`ys-code.md`、`ys-info.md`、`ys-git.md`、`ys-manage.md`）。

**向后兼容：** 所有原子命令保持不变，命名空间命令是 additive。

---

## Skills

### P0 准确性 — 新增 Skills

#### `skills/verification-patterns/SKILL.md`

**定位：** 通用验证框架，对标 GSD 的 `references/verification-patterns.md`。

**核心原则：**
```markdown
## 存在 ≠ 实现

验证必须检查四层：
1. **Exists** — 文件存在于预期路径
2. **Substantive** — 内容是真实实现，非占位符
3. **Wired** — 与系统其余部分有连接
4. **Functional** — 实际运行时可用
```

**Stub 检测规则集：**
```markdown
## 通用 Stub 模式

**注释类 stub：**
- `TODO|FIXME|XXX|HACK|PLACEHOLDER`
- `implement|add later|coming soon|will be`
- `// ...|/* ... */|# ...`

**空实现：**
- `return null|return undefined|return {}|return []`
- `pass$|...|nothing`
- `console.(log|warn|error).*only`

**硬编码值：**
- 硬编码 ID、count、length
- 模板括号残留 `<.*>|\[.*\]|\{.*\}`

**UI 占位符：**
- `placeholder|lorem ipsum|coming soon|under construction`
```

**使用场景：**
- `/verify` 命令内部调用
- `/build` 完成后自动运行（可选）
- `/ship` 前强制运行（作为 fan-out 的一部分）

---

#### `skills/agent-contracts/SKILL.md`

**定位：** Agent 完成标记与 handoff 合约规范，对标 GSD 的 `references/agent-contracts.md`。

**核心规则：**
```markdown
## Agent 完成标记规范

所有 spawn 的 subagent 必须在最终输出中包含完成标记，格式为 H2 标题：

| 场景 | 标记 |
|------|------|
| 任务成功完成 | `## TASK COMPLETE` |
| 发现需要用户决策的问题 | `## CHECKPOINT REACHED` |
| 任务被阻塞 | `## TASK BLOCKED` |
| 发现严重问题需升级 | `## ESCALATE` |

## Handoff 合约

### Planner → Executor
| 字段 | 必填 | 说明 |
|------|------|------|
| frontmatter | 是 | task, acceptance, verify |
| <objective> | 是 | 任务目标 |
| <tasks> | 是 | 有序任务列表 |
| <verification> | 是 | 验证步骤 |

### Executor → Verifier
| 字段 | 必填 | 说明 |
|------|------|------|
| frontmatter | 是 | task, files_modified, metrics |
| <summary> | 是 | 执行摘要 |
| <deviations> | 否 | 偏离计划的部分及原因 |
```

**使用场景：**
- 所有使用 `Agent` tool spawn subagent 的命令
- `/ship` 的 fan-out 评审
- `/plan` 生成的 plan 文档结构

---

#### `skills/revision-loop/SKILL.md`

**定位：** 检查-修订-升级循环，对标 GSD 的 `references/revision-loop.md`。

**核心模式：**
```markdown
## Check-Revise-Escalate（最多 3 轮）

适用场景：checker/validator 发现问题，需要 producer 修订。

### 流程

```
prev_issue_count = Infinity
iteration = 0

LOOP:
  1. 运行 checker 评估当前输出
  2. 如果 PASSED 或只有 INFO：接受，退出
  3. 如果有 BLOCKER 或 WARNING：
     a. iteration += 1
     b. 如果 iteration > 3：升级给用户
     c. 如果 issue_count >= prev_issue_count：
        → 升级："修订循环停滞（问题数未减少）"
     d. prev_issue_count = issue_count
     e. 用 checker 反馈重新 spawn producer
     f. 回到 LOOP
```

### 反馈格式

```
<checker_issues>
{YAML 格式的问题列表：dimension, severity, finding, suggested_fix}
</checker_issues>

<revision_instructions>
- 修复所有 BLOCKER
- 尽可能修复 WARNING
- 如果某个 WARNING 不修复，解释原因
</revision_instructions>
```
```

**使用场景：**
- `/plan` 后自动运行 plan-checker（如果实现了 plan-checker Agent）
- `/build` 失败后的自动修复尝试
- `/ship` 前 code-reviewer 发现问题后的自动修订

---

#### `skills/gate-prompts/SKILL.md`

**定位：** 结构化决策 gate 模式，对标 GSD 的 `references/gate-prompts.md`。

**模式库：**
```markdown
## approve-revise-abort
用于 plan 审批、gap closure 审批。
- 问题: "批准这些 {noun}？"
- header: "批准?"
- 选项: 批准 | 请求修改 | 中止

## yes-no
用于重新规划、重建、替换、提交确认。
- 问题: "{具体动作}？"
- header: "确认"
- 选项: 是 | 否

## stale-continue
用于过时警告、时间戳新鲜度检查。
- 问题: "{产物} 可能已过时。刷新还是继续？"
- header: "过时"
- 选项: 刷新 | 继续

## multi-option-failure
用于构建失败处理。
- 问题: "Plan {id} 失败。如何处理？"
- header: "失败"
- 选项: 重试 | 跳过 | 回滚 | 中止

## multi-option-gaps
用于验证发现 gaps。
- 问题: "{count} 个验证 gaps 需要处理。"
- header: "Gaps"
- 选项: 自动修复 | 覆盖 | 手动处理 | 跳过
```

**约束：**
- header 最多 12 个字符
- 每 prompt 最多 4 个选项
- 必须处理 "Other"（用户输入自定义回复）

**使用场景：**
- 嵌入到所有需要用户决策的命令中
- `/spec` 的假设确认步骤
- `/build` 的 checkpoint 暂停
- `/ship` 的 blocker 处理

---

### P1 能力覆盖 — 新增 Skills

#### `skills/context-engineering/SKILL.md`（强化现有）

**现有状态：** ys-powers 已有 `skills/context-engineering/SKILL.md`，需要强化。

**新增内容：**
```markdown
## Context 加载策略

### 原则：Right Context at Right Time

不要一次性加载全部上下文。按阶段按需加载：

| 阶段 | 加载内容 | 避免加载 |
|------|----------|----------|
| 探索 | 项目结构、README、最近提交 | 全部源码 |
| 规划 | Spec 相关章节、依赖模块接口 | 实现细节 |
| 实现 | 当前任务涉及的文件 + 直接依赖 | 无关模块 |
| 验证 | 测试文件 + 被测代码 | 未变更文件 |

### Context 预算分配

- Orchestrator（主会话）：~15% context budget
- Subagent（每次 spawn）：100% fresh context

### 信号词检测

当用户说以下词语时，通常意味着 context 不足：
- "不对，我说的是..."
- "你理解错了..."
- "等等，让我重新说明..."

此时应主动请求用户澄清，而不是继续猜测。
```

---

#### `skills/health-check/SKILL.md`

**定位：** 项目健康诊断规范。

**内容：**
```markdown
## 健康检查维度

### 1. 配置完整性
检查 `.claude/` 目录结构：
- `skills/` 是否存在
- `commands/` 是否存在
- `rules/` 是否存在
- 文件是否为最新版本（与 ys-powers 上游对比）

### 2. 上下文利用率
询问模型当前 tokens used + context window，计算利用率：
| 利用率 | 状态 | 行动 |
|--------|------|------|
| < 60% | healthy | 无需操作 |
| 60-70% | warning | 建议 `/clear` 或开启新会话 |
| ≥ 70% | critical | 推理质量可能下降，强烈建议重置 |

### 3. 工作区状态
- 未提交变更数量和文件列表
- 当前分支名
- 与上游的差异

### 4. Skill 质量
- 是否有重复或冲突的 skills
- 是否有 deprecated 的 skills
```

---

### P3 效率 — 新增 Skills

#### `skills/context-management/SKILL.md`

**定位：** 上下文窗口管理与 context rot 缓解。

**内容：**
```markdown
## Context Rot 缓解策略

### 信号检测

以下迹象表明 context 可能已腐烂：
- 会话超过 30 轮
- 模型开始重复之前的回答
- 模型忘记了会话早期的关键决策
- 响应质量明显下降

### 应对措施

| 严重程度 | 措施 |
|----------|------|
| 轻度（20-30 轮） | 主动总结关键决策，要求用户确认 |
| 中度（30-50 轮） | 建议保存当前状态到文件，然后 `/clear` |
| 重度（>50 轮） | 强制建议开启新会话，加载 plan 文件恢复上下文 |

### 预防性措施

- 每 10 轮主动做一次「决策回顾」
- 将关键决策写入 `.claude/STATE.md`（可选，用户自行管理）
- 复杂任务拆分为多个会话，每个会话聚焦一个子任务
```

---

## Agents

### P1 能力覆盖 — 新增 Agents

#### `agents/plan-checker.md`

**定位：** 验证 plan 的可执行性，对标 GSD 的 `gsd-plan-checker`。

**触发场景：**
- `/plan` 完成后自动执行（可选，通过 flag 控制）
- 用户手动调用：`/plan --verify`

**系统提示草案：**
```markdown
---
name: plan-checker
description: 验证 plan 的可执行性和完整性
---

## 角色

你是 plan-checker。你的任务是验证一个任务计划（PLAN.md）是否可执行。

## 验证维度

| 维度 | 检查内容 | 标准 |
|------|----------|------|
| 完整性 | 每个任务是否有 acceptance criteria | 必须有 |
| 可达性 | 任务依赖是否形成循环 | 必须无循环 |
| 粒度 | 每个任务是否可在一个会话内完成 | 建议 ≤5 文件 |
| 验证 | 每个任务是否有 verify 步骤 | 必须有 |
| 一致性 | 任务是否与 spec 一致 | 必须一致 |

## 输出格式

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

  - dimension: 粒度
    severity: WARNING
    task: "Task 5"
    finding: "涉及 12 个文件，超出建议范围"
    suggested_fix: "拆分为 2-3 个子任务"
```

## 规则

- BLOCKER：必须修复，否则计划不可执行
- WARNING：建议修复，但不阻塞执行
- INFO：参考信息
```

---

#### `agents/debugger.md`

**定位：** 系统化调试流程，对标 GSD 的 `gsd-debugger`。

**触发场景：**
- `/build` 失败时自动调用
- 用户手动调用：`/debug <error-message>`

**系统提示草案：**
```markdown
---
name: debugger
description: 系统化诊断和修复代码问题
---

## 角色

你是 debugger。你的任务是通过系统化方法诊断代码问题，找到 root cause。

## 调试流程

1. **信息收集**
   - 错误消息和堆栈跟踪
   - 相关代码文件
   - 最近变更（git diff）
   - 环境信息（依赖版本、配置）

2. **假设生成**
   - 列出 3-5 个可能的 root cause
   - 按可能性排序

3. **假设验证**
   - 对每个假设，设计验证方法
   - 运行验证（测试、日志、断点）

4. **修复方案**
   - 针对确认的 root cause，提出修复方案
   - 评估修复方案的副作用

5. **输出**
   - root cause 分析
   - 修复方案
   - 预防建议

## 输出标记

- `## DEBUG COMPLETE` — 调试完成，找到 root cause
- `## ROOT CAUSE FOUND` — 找到 root cause，提供修复方案
- `## CHECKPOINT REACHED` — 需要用户决策或额外信息
```

---

#### `agents/spec-reviewer.md`

**定位：** 评审 spec 的完整性和质量，对标 GSD 的文档审查 Agent。

**触发场景：**
- `/spec` 完成后可选执行：`/spec --review`
- 用户手动调用评审现有 spec

**系统提示草案：**
```markdown
---
name: spec-reviewer
description: 评审 spec 的完整性和质量
---

## 角色

你是 spec-reviewer。你的任务是评审一份 spec 文档是否足够清晰、完整、可执行。

## 评审维度

| 维度 | 检查内容 |
|------|----------|
| 六域覆盖 | Objective、Commands、Structure、Style、Testing、Boundaries 是否齐全 |
| 可测试性 | Success Criteria 是否具体、可测量 |
| 无歧义 | 是否存在多个合理解读 |
| 边界清晰 | Always/Ask First/Never 是否明确 |
| 一致性 | 各章节之间是否矛盾 |

## 输出格式

```yaml
## SPEC REVIEW COMPLETE

score: 85/100

strengths:
  - "Objective 清晰，用户场景明确"
  - "Boundaries 定义完整"

gaps:
  - dimension: 可测试性
    severity: WARNING
    finding: "Success Criteria 中 '提升准确性' 不够具体"
    suggested_fix: "改为 'stub 代码残留率从 X% 降到 Y%'"

recommendations:
  - "补充性能指标"
  - "明确并发场景约束"
```
```

---

#### `agents/context-engineer.md`

**定位：** 优化上下文加载策略，对标 GSD 的上下文工程实践。

**触发场景：**
- 大项目操作时建议调用
- 上下文利用率 ≥70% 时自动建议

**系统提示草案：**
```markdown
---
name: context-engineer
description: 优化上下文加载策略，减少 token 浪费
---

## 角色

你是 context-engineer。你的任务是分析当前会话的上下文使用情况，提出优化建议。

## 分析维度

1. **冗余检测**
   - 是否有重复加载的代码文件
   - 是否有已过时但仍保留在上下文中的信息

2. **加载策略**
   - 当前任务是否只需要接口而非实现
   - 是否有更精简的方式表达相同信息

3. **分 Session 建议**
   - 当前工作是否应拆分为多个会话
   - 每个会话应加载哪些上下文

## 输出格式

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
```

---

## Rules

### 新增 Rules

#### `rules/verification.md`

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

#### `rules/agent-contracts.md`

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

---

## Project Structure

优化后的 ys-powers 目录结构：

```
ys-powers/
├── skills/
│   ├── api-and-interface-design/
│   ├── ...（现有 skills）
│   ├── verification-patterns/          # NEW — 四层验证框架
│   ├── agent-contracts/                # NEW — Agent 完成标记规范
│   ├── revision-loop/                  # NEW — 检查-修订-升级循环
│   ├── gate-prompts/                   # NEW — 结构化决策 gate
│   └── context-management/             # NEW — 上下文窗口管理
├── commands/
│   ├── spec.md
│   ├── plan.md
│   ├── build.md                        # MODIFIED — 增加 --tdd
│   ├── ship.md
│   ├── ...（现有 commands）
│   ├── verify.md                       # NEW — 通用验证命令
│   ├── health.md                       # NEW — 健康检查
│   ├── ys-workflow.md                  # NEW — 命名空间路由
│   ├── ys-code.md                      # NEW — 命名空间路由
│   ├── ys-info.md                      # NEW — 命名空间路由
│   ├── ys-git.md                       # NEW — 命名空间路由
│   └── ys-manage.md                    # NEW — 命名空间路由
├── rules/
│   ├── code.md
│   ├── context7.md
│   ├── verification.md                 # NEW — 验证规则
│   └── agent-contracts.md              # NEW — Agent 合约规则
├── agents/
│   ├── code-reviewer.md
│   ├── security-auditor.md
│   ├── test-engineer.md
│   ├── plan-checker.md                 # NEW — 验证 plan 可执行性
│   ├── debugger.md                     # NEW — 系统化调试
│   ├── spec-reviewer.md                # NEW — 评审 spec 质量
│   └── context-engineer.md             # NEW — 优化上下文加载
├── docs/
│   ├── ys-powers/specs/                # spec 文件存放地
│   └── get-shit-done/                  # GSD 分析笔记（已有）
├── sop/
│   └── ...（现有 SOP）
├── install/
│   └── local-install.py                # MODIFIED — 新增文件同步
└── Makefile
```

---

## Code Style

### Skill / Command / Agent 文件规范

**Frontmatter 格式：**
```yaml
---
name: skill-name
description: 一句话描述，50 字以内
# Agent 特有字段
tools: Read, Write, Bash, Glob, Grep  # 限制可用工具
---
```

**命名规范：**
- 文件名：kebab-case（`verification-patterns.md`）
- Skill name：kebab-case（`verification-patterns`）
- Agent name：kebab-case（`plan-checker`）
- Command name：kebab-case（`ys-workflow`）

**内容规范：**
- 中文为主，技术术语保留英文
- 使用 Markdown 表格展示结构化信息
- 代码块标注语言（`bash`、`yaml`、`markdown`）
- 关键约束用 **粗体** 标注

---

## Testing Strategy

### 测试方法

由于 ys-powers 是纯配置系统，无运行时代码，测试策略为：

1. **安装测试**
   - 运行 `make install` 到测试项目
   - 验证所有新增文件正确安装到 `.claude/`
   - 验证无文件遗漏或冲突

2. **功能测试（手动）**
   - 每个新增命令在真实项目中试用
   - 验证输出格式符合预期
   - 验证边界情况（空输入、错误输入）

3. **回归测试**
   - 验证现有命令未被破坏
   - 验证现有 skills 仍正常工作

4. **一致性测试**
   - 检查所有新文件的 frontmatter 格式
   - 检查命名规范一致性
   - 检查链接引用有效性

---

## Boundaries

### Always
- 新增任何 command/skill/agent 前，先在 spec 中定义
- 保持中文用户可见文本，技术术语保留英文
- 每个新增文件必须有明确的价值主张
- 向后兼容：不破坏现有命令和技能

### Ask First
- 修改现有核心命令（spec, plan, build, ship）的行为
- 引入需要外部依赖的机制（如需要安装 CLI 工具）
- 变更 install 脚本的覆盖策略
- 删除或重命名现有文件

### Never
- 引入运行时依赖（Node.js、npm 包等）
- 引入状态系统（`.planning/` 目录、STATE.md 等）
- 修改 refer/ 下的任何文件
- 复制粘贴 GSD 的原始内容（必须重写适配）
- 让系统变重：如果一个功能可以用 10 行实现，不要用 100 行

---

## Success Criteria

### 准确性指标（3 个月后）

| 指标 | 当前基线 | 目标 | 测量方法 |
|------|----------|------|----------|
| 模型执行走偏率 | 未知（需建立） | 降低 50% | 随机抽样 20 个 build 会话，统计偏离 plan 的比例 |
| stub 代码残留率 | 未知（需建立） | 降低 70% | `/verify` 扫描最近 10 个 PR 的变更文件 |
| plan 可执行率 | 未知（需建立） | ≥90% | plan-checker Agent 评审最近 10 个 plan |

### 能力覆盖指标

| 指标 | 当前 | 目标 | 测量方法 |
|------|------|------|----------|
| Agent 数量 | 3 | 7 | 统计 `.claude/agents/` 下文件数 |
| 命令数量 | 20 | 25+ | 统计 commands/ 下文件数 |
| Skill 数量 | ~25 | 30+ | 统计 skills/ 下目录数 |

### 质量门指标

| 指标 | 当前 | 目标 | 测量方法 |
|------|------|------|----------|
| TDD 使用率 | 0% | ≥30%（在启用 --tdd 的项目中） | 统计 `--tdd` flag 使用次数 |
| Spec 评审率 | 0% | ≥50% | 统计 spec-reviewer 调用次数 |

### 效率指标

| 指标 | 当前 | 目标 | 测量方法 |
|------|------|------|----------|
| 平均会话轮数 | 未知 | 降低 20% | 抽样统计用户会话长度 |
| Context 重置建议采纳率 | 0% | ≥40% | 统计 context-management skill 建议被采纳的比例 |

---

## Open Questions

1. **Agent 的 tools 限制**：Claude Code 的 subagent 是否支持 `tools:` frontmatter 限制？如果上游 bug（anthropics/claude-code#13898）导致 MCP tools 被 strip，是否有 fallback 策略？

2. **Revision Loop 的自动化程度**：check-revise-escalate 循环在实际使用中，3 轮是否足够？是否需要根据任务复杂度动态调整？

3. **Namespace Meta-Skills 的效果验证**：20 个命令的 token 消耗是否已经到了需要路由的程度？是否需要先测量基线再决定是否实施？

4. **Verification Patterns 的误报率**：stub 检测的 grep 模式可能产生误报（如合法的 `return null`）。如何平衡检测覆盖率和误报率？

5. **Model Profiles 的可行性**：Claude Code 是否支持按 subagent 配置模型？如果不可行，是否需要降级为 prompt 级别的建议？

---

## Roadmap

### Phase 1（立即，1-2 周）— 准确性基础

**目标：** 建立验证框架和 Agent 合约规范，解决最痛的「执行走偏」问题。

| 任务 | 产出 | 验收标准 |
|------|------|----------|
| 1.1 | `skills/verification-patterns/SKILL.md` | 包含四层验证定义和 stub 检测规则集 |
| 1.2 | `commands/verify.md` | 可运行，输出格式符合 spec |
| 1.3 | `skills/agent-contracts/SKILL.md` | 完成标记规范和 handoff 合约定义 |
| 1.4 | `rules/agent-contracts.md` | 主会话强制执行 Agent 合约 |
| 1.5 | `skills/revision-loop/SKILL.md` | 包含 check-revise-escalate 流程和 YAML 反馈格式 |
| 1.6 | `skills/gate-prompts/SKILL.md` | 包含 5+ 种 gate 模式 |
| 1.7 | 更新 `commands/build.md` | 增加 `--tdd` flag 支持 |
| 1.8 | 更新 `commands/spec.md` | 增加 `--ambiguity-check` 和 `--template` 支持 |

**验证：** 在 2 个真实项目中试用 `/verify` 和 `/build --tdd`，收集反馈。

---

### Phase 2（近期，2-4 周）— 能力扩展

**目标：** 新增专项 Agent，提升覆盖场景。

| 任务 | 产出 | 验收标准 |
|------|------|----------|
| 2.1 | `agents/plan-checker.md` | 可 spawn，输出 YAML 格式报告 |
| 2.2 | `agents/debugger.md` | 可 spawn，能系统化诊断问题 |
| 2.3 | `agents/spec-reviewer.md` | 可 spawn，输出评分和 gaps 列表 |
| 2.4 | `commands/health.md` | 可运行，覆盖 4 个健康维度 |
| 2.5 | `skills/context-management/SKILL.md` | 包含 context rot 信号检测和应对措施 |
| 2.6 | `skills/context-engineering/SKILL.md`（强化） | 新增 Right Context at Right Time 策略 |

**验证：** 在 `/ship` 中集成 plan-checker，对比评审效果。

---

### Phase 3（中期，1-2 个月）— 质量门强化

**目标：** 在关键节点嵌入强制验证，防止问题漏出。

| 任务 | 产出 | 验收标准 |
|------|------|----------|
| 3.1 | `commands/ys-workflow.md` | 包含 5 个子命令索引 |
| 3.2 | `commands/ys-code.md` | 包含 4 个子命令索引 |
| 3.3 | `commands/ys-info.md` | 包含 4 个子命令索引 |
| 3.4 | `commands/ys-git.md` | 包含 3 个子命令索引 |
| 3.5 | `commands/ys-manage.md` | 包含 3 个子命令索引 |
| 3.6 | `rules/verification.md` | 主会话强制执行验证规则 |
| 3.7 | 更新 `commands/ship.md` | 集成 `/verify` 作为 fan-out 的一部分 |

**验证：** 测量命名空间命令的使用频率 vs 原子命令。

---

### Phase 4（远期，可选）— 效率优化

**目标：** 上下文效率提升，缓解 context rot。

| 任务 | 产出 | 验收标准 |
|------|------|----------|
| 4.1 | `agents/context-engineer.md` | 可 spawn，能分析上下文利用率并提出优化 |
| 4.2 | 上下文利用率监控 | 在 `/health --context` 中集成 |
| 4.3 | Model Profiles 调研 | 确认 Claude Code subagent 模型配置可行性 |

**验证：** 测量大项目（>100 文件）中的会话轮数变化。

---

## 借鉴点来源索引

| 本 Spec 内容 | GSD 来源 | 适配方式 |
|--------------|----------|----------|
| Verification Patterns | `references/verification-patterns.md` | 精简为 skill，去掉 .planning 依赖 |
| Agent Contracts | `references/agent-contracts.md` | 保留核心标记规范，去掉 SDK 合约 |
| Revision Loop | `references/revision-loop.md` | 保留 3 轮循环逻辑，YAML 反馈格式 |
| Gate Prompts | `references/gate-prompts.md` | 保留模式库，适配中文语境 |
| TDD Gate | `references/execute-mvp-tdd.md` | 简化为 `/build --tdd` flag |
| Health Check | `commands/gsd/health.md` | 去掉 .planning 依赖，改为通用诊断 |
| Namespace Meta-Skills | `docs/COMMANDS.md` namespace 章节 | 简化为 5 个路由命令 |
| Model Profiles | `references/model-profiles.md` | 待调研可行性后实施 |

---

*Spec 版本: v1.0*
*创建日期: 2026-06-01*
*对应分析文档: `docs/get-shit-done/overview.md`, `comparison.md`, `takeaways.md`*
