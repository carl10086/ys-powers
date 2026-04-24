# Writing Plans Skill 分析

## 分析概要

### 文档定位
这是一个 **skill 工作流文档** — 定义了如何编写实现计划（implementation plans）的标准和流程。

### 核心主张
编写实现计划时，应该假设执行者对代码库一无所知、对最佳实践也不太熟悉，将任务分解为极细粒度的步骤（每步 2-5 分钟），包含完整的测试、代码和提交指令。

### 结构骨架

| 章节 | 内容 |
|------|------|
| Overview | 文档目的和假设 |
| Scope Check | 检查规格是否需要拆分 |
| File Structure | 文件结构设计原则 |
| Bite-Sized Task Granularity | 任务粒度标准（2-5 分钟/步） |
| Plan Document Header | 计划文档的固定头部格式 |
| Task Structure | 每个任务的模板格式 |
| No Placeholders | 禁止占位符规则 |
| Remember | 附加规则（使用中文、写计划前读规则） |
| Self-Review | 自我审查清单 |
| Execution Handoff | 执行交接和选项 |

### 关键洞察

1. **TDD 驱动** — 每个任务必须先写测试，再实现，确保测试覆盖
2. **极细粒度** — 每步 2-5 分钟，包含"写测试→运行失败→实现→运行通过→提交"的完整闭环
3. **零占位符** — 不允许"TODO"、"TBD"、或"类似 Task N"这类模糊引用

---

## 逐段精读

### 段落 1: 元数据

**原文:**
```
---
name: writing-plans
description: Use when you have a spec or requirements for a multi-step task, before touching code
---
```

**翻译:**
```
---
name: writing-plans
description: 当你有一个多步任务的需求文档或规格说明时，在动手写代码之前使用此 skill
---
```

**要点:**
- Skill 的元数据定义，声明了触发条件：**有规格文档的多步任务**
- 强调"before touching code" — 这是一个**计划阶段**的 skill，不是执行阶段

---

### 段落 2: 概述

**原文:**
```
# Writing Plans

## Overview

Write comprehensive implementation plans assuming the engineer has zero context for our codebase and questionable taste. Document everything they need to know: which files to touch for each task, code, testing, docs they might need to check, how to test it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

Assume they are a skilled developer, but know almost nothing about our toolset or problem domain. Assume they don't know good test design very well.
```

**翻译:**
```
# Writing Plans

## 概述

编写全面的实现计划，假设工程师对我们的代码库零认知、品味也一般。记录他们需要知道的一切：每个任务涉及哪些文件、代码、测试、需要查阅的文档、如何测试。将完整计划分解为小到一口的任务。DRY。YAGNI。TDD。频繁提交。

假设他们是有经验的开发者，但对我们的工具集和问题领域几乎一无所知。假设他们不太懂好的测试设计。
```

**要点:**
- **假设工程师"有能力但无知"** — 这是关键假设，不是贬低。计划需要覆盖所有上下文转移
- **DRY/YAGNI/TDD/Frequent commits** — 四大原则，必须体现在计划中
- **"questionable taste"** — 意味着计划要包含代码规范、最佳实践，而不只是功能实现

---

### 段落 3: 开头声明和上下文

**原文:**
```
**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Context:** This should be run in a dedicated worktree (created by brainstorming skill).

**Save plans to:** `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`
- (User preferences for plan location override this default)
```

**翻译:**
```
**开头声明:** "I'm using the writing-plans skill to create the implementation plan."

**上下文:** 这应该在专用 worktree 中运行（由 brainstorming skill 创建）。

**保存计划到:** `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`
- (用户偏好会覆盖此默认位置)
```

**要点:**
- **必须声明** — 开场就要宣告正在使用此 skill
- **worktree 隔离** — 这是一个安全机制，避免污染主分支
- **文件名格式** — YYYY-MM-DD 日期前缀，便于排序和检索

---

### 段落 4: 范围检查

**原文:**
```
## Scope Check

If the spec covers multiple independent subsystems, it should have been broken into sub-project specs during brainstorming. If it wasn't, suggest breaking this into separate plans — one per subsystem. Each plan should produce working, testable software on its own.
```

**翻译:**
```
## 范围检查

如果规格文档覆盖多个独立子系统，应该在 brainstorming 阶段就拆分为子项目规格。如果没有，建议拆分为独立计划 — 每个子系统一个计划。每个计划应该能独立产出可测试的可用软件。
```

**要点:**
- **强制拆分规则** — 多子系统必须分离，不允许一个计划涵盖一切
- **独立性要求** — 每个计划必须能独立完成并测试通过
- 这是一个**过滤器**，不是可选项

---

### 段落 5: 文件结构

**原文:**
```
## File Structure

Before defining tasks, map out which files will be created or modified and what each one is responsible for. This is where decomposition decisions get locked in.

- Design units with clear boundaries and well-defined interfaces. Each file should have one clear responsibility.
- You reason best about code you can hold in context at once, and your edits are more reliable when files are focused. Prefer smaller, focused files over large ones that do too much.
- Files that change together should live together. Split by responsibility, not by technical layer.
- In existing codebases, follow established patterns. If the codebase uses large files, don't unilaterally restructure - but if a file you're modifying has grown unwieldy, including a split in the plan is reasonable.
```

**翻译:**
```
## 文件结构

在定义任务之前，先映射出哪些文件会被创建或修改，以及每个文件的职责。这是锁定分解决策的地方。

- 设计边界清晰、接口定义明确的单元。每个文件只负责一件事。
- 你最好一次性能 hold 住的代码量是有限的，当文件专注时你的编辑更可靠。偏好小而专注的文件，而不是大而全的文件。
- 一起变更的文件应该放一起。按职责拆分，而非按技术层拆分。
- 在现有代码库中，遵循既定模式。如果代码库使用大文件，不要单方面重构 — 但如果你修改的文件已经变得臃肿，在计划中包含拆分是合理的。
```

**要点:**
- **先结构，后任务** — 文件布局必须在任务分解前确定
- **SRP（单一职责原则）** — 每个文件只做一件事
- **按职责而非技术层拆分** — 常见错误是按 dao/service/controller 分层；正确做法是按业务能力拆分
- **尊重现有模式** — 不要为了"更好"而强制重构

---

### 段落 6: 任务分解指导

**原文:**
```
This structure informs the task decomposition. Each task should produce self-contained changes that make sense independently.
```

**翻译:**
```
这个结构决定了任务分解方式。每个任务应该产出独立的、自包含的变更，可以独立理解。
```

**要点:**
- 任务分解的指导原则：**自包含、可独立理解**
- 每个任务的变更不应该依赖其他任务的完成才能被理解

---

### 段落 7: 任务粒度

**原文:**
```
## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**
- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Commit" - step
```

**翻译:**
```
## 小到一口的任务粒度

**每步是一个动作（2-5 分钟）：**
- "写一个失败的测试" - 一步
- "运行它确保它失败" - 一步
- "写最少的代码让测试通过" - 一步
- "运行测试确保通过" - 一步
- "提交" - 一步
```

**要点:**
- **极细粒度** — 5 个步骤完成一个任务的 TDD 循环
- **时间盒** — 每步 2-5 分钟，强迫你写最少的代码
- 这不是建议，是规则。超过 5 分钟就应该继续拆分

---

### 段落 8: 计划文档头部

**原文:**
```
## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---
```
```

**翻译:**
```
## 计划文档头部

**每个计划必须以此头部开头：**

```markdown
# [功能名称] Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** [一句话描述这个构建的内容]

**Architecture:** [2-3 句话描述方法]

**Tech Stack:** [关键技术和库]

---
```
```

**要点:**
- **强制头部格式** — 必须包含 Goal/Architecture/Tech Stack
- **agentic workers 声明** — 明确说明此计划是给 AI agent 用的
- **checkbox 语法** — 用于任务进度跟踪

---

### 段落 9: 任务结构

**原文:**
```
## Task Structure

````markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

- [ ] **Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

- [ ] **Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````
```

**翻译:**
```
## 任务结构

````markdown
### Task N: [组件名称]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

- [ ] **Step 1: 写一个失败的测试**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] **Step 2: 运行测试确认它失败**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

- [ ] **Step 3: 写最少的实现代码**

```python
def function(input):
    return expected
```

- [ ] **Step 4: 运行测试确认它通过**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

- [ ] **Step 5: 提交**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````
```

**要点:**
- **5 步固定结构** — 写失败测试 → 验证失败 → 实现 → 验证通过 → 提交
- **精确路径** — 文件路径必须精确到文件名和行号
- **Expected 输出** — 每步都要写清楚期望的输出是什么
- **Include 代码** — 不仅是描述，必须有实际可运行的代码

---

### 段落 10: 禁止占位符

**原文:**
```
## No Placeholders

Every step must contain the actual content an engineer needs. These are **plan failures** — never write them:
- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "add validation" / "handle edge cases"
- "Write tests for the above" (without actual test code)
- "Similar to Task N" (repeat the code — the engineer may be reading tasks out of order)
- Steps that describe what to do without showing how (code blocks required for code steps)
- References to types, functions, or methods not defined in any task
```

**翻译:**
```
## 禁止占位符

每一步必须包含工程师需要的实际内容。这些是 **计划失败** — 永远不要写：
- "TBD"、"TODO"、"later implement"、"fill in details"
- "Add appropriate error handling" / "add validation" / "handle edge cases"
- "Write tests for the above"（没有实际测试代码）
- "Similar to Task N"（重复代码 — 工程师可能按任意顺序阅读任务）
- 只描述做什么却不展示怎么做的步骤（代码步骤必须有代码块）
- 引用在任何任务中都没有定义的类型、函数或方法
```

**要点:**
- **零容忍占位符** — 这些不是"未完成的计划"，是"计划失败"
- **独立可读** — 工程师可能从任意任务开始读，必须每处都有完整上下文
- **禁止模糊引用** — "Similar to Task N" 是危险信号，必须重复必要的代码

---

### 段落 11: 记住规则

**原文:**
```
## Remember
- Exact file paths always
- Complete code in every step — if a step changes code, show the code
- Exact commands with expected output
- DRY, YAGNI, TDD, frequent commits
- You must use chinese to write the plan
- Before write plan, You must read ./claude/rules/*.md to remind the engineer to follow the rules
```

**翻译:**
```
## 记住
- 始终使用精确的文件路径
- 每步都有完整代码 — 如果步骤会修改代码，展示代码
- 精确的命令和期望输出
- DRY, YAGNI, TDD, frequent commits
- 你必须使用中文写计划
- 写计划之前，你必须读取 ./claude/rules/*.md 来提醒工程师遵守规则
```

**要点:**
- **中文要求** — 计划必须用中文写
- **读规则文件** — 这是容易被忽略的一步，在开始写计划前必须执行

---

### 段落 12: 自我审查

**原文:**
```
## Self-Review

After writing the complete plan, look at the spec with fresh eyes and check the plan against it. This is a checklist you run yourself — not a subagent dispatch.

**1. Spec coverage:** Skim each section/requirement in the spec. Can you point to a task that implements it? List any gaps.

**2. Placeholder scan:** Search your plan for red flags — any of the patterns from the "No Placeholders" section above. Fix them.

**3. Type consistency:** Do the types, method signatures, and property names you used in later tasks match what you defined in earlier tasks? A function called `clearLayers()` in Task 3 but `clearFullLayers()` in Task 7 is a bug.
```

**翻译:**
```
## 自我审查

写完完整计划后，用全新的眼光看规格文档，对照检查计划。这是你自己运行的检查清单 — 不是委托给 subagent。

**1. 规格覆盖：** 浏览规格的每个章节/需求。你能指出哪个任务实现了它吗？列出任何遗漏。

**2. 占位符扫描：** 在计划中搜索危险信号 — 任何上面"禁止占位符"部分提到的模式。修复它们。

**3. 类型一致性：** 你在后面任务中使用的类型、方法签名和属性名与前面定义的一致吗？Task 3 中叫 `clearLayers()` 但 Task 7 中叫 `clearFullLayers()` 是个 bug。
```

**要点:**
- **自己审查** — 不是委托给 AI，是人类自己的检查步骤
- **三个检查点** — 覆盖度、占位符、类型一致性
- **命名一致性** — 这是一个常见 bug，必须专项检查

---

### 段落 13: 即时修复

**原文:**
```
If you find issues, fix them inline. No need to re-review — just fix and move on. If you find a spec requirement with no task, add the task.
```

**翻译:**
```
如果发现问题，当场修复。不需要重新审查 — 修完继续。如果发现规格需求没有对应任务，添加任务。
```

**要点:**
- **即时修复** — 发现问题立即修复，不要"稍后"
- **补充任务** — 规格有要求就必须有对应任务，缺一不可

---

### 段落 14: 执行交接

**原文:**
```
## Execution Handoff

After saving the plan, offer execution choice:

**"Plan complete and saved to `docs/superpowers/plans/<filename>.md`. Two execution options:**

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?"**
```

**翻译:**
```
## 执行交接

保存计划后，提供执行选项：

**"计划完成并保存到 `docs/superpowers/plans/<filename>.md`。两种执行选项：**

**1. Subagent 驱动（推荐）** - 我为每个任务分配一个新的 subagent，任务间审查，快速迭代

**2. 内联执行** - 在此 session 中使用 executing-plans 执行，带检查点的批量执行

**选择哪种方式？"**
```

**要点:**
- **两种执行模式** — subagent 驱动（推荐）或内联执行
- **用户选择** — 不是强制的，给出选项让用户决定

---

### 段落 15: 执行模式选择

**原文:**
```
**If Subagent-Driven chosen:**
- **REQUIRED SUB-SKILL:** Use superpowers:subagent-driven-development
- Fresh subagent per task + two-stage review

**If Inline Execution chosen:**
- **REQUIRED SUB-SKILL:** Use superpowers:executing-plans
- Batch execution with checkpoints for review
```

**翻译:**
```
**如果选择 Subagent 驱动：**
- **必需 SUB-SKILL:** 使用 superpowers:subagent-driven-development
- 每个任务一个新 subagent + 两阶段审查

**如果选择内联执行：**
- **必需 SUB-SKILL:** 使用 superpowers:executing-plans
- 带审查检查点的批量执行
```

**要点:**
- **必须使用对应 skill** — 不能跳过，必须使用指定的 skill 来执行
- **两阶段审查** — subagent 驱动模式有额外审查机制

---

## 整体总结

### 核心概念

| 概念 | 定义 |
|------|------|
| **Bite-sized tasks** | 每步 2-5 分钟的极细粒度任务分解 |
| **TDD 循环** | 写失败测试 → 验证失败 → 实现 → 验证通过 → 提交 |
| **Zero placeholders** | 不允许 TBD/TODO/类似 Task N 等模糊引用 |
| **Self-contained tasks** | 每个任务可独立理解和执行 |
| **DRY/YAGNI/TDD** | 四大原则必须体现在计划中 |

### 工作流程

```
1. 宏观概览 → 理解规格文档
2. 范围检查 → 确认是否需要拆分子系统
3. 文件结构设计 → 先映射文件再分解任务
4. 逐任务编写 → 5 步 TDD 循环
5. 自我审查 → 覆盖度/占位符/类型一致性
6. 执行交接 → 用户选择执行模式
```

### 关键文件

| 文件 | 作用 |
|------|------|
| `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md` | 计划输出路径 |
| `./claude/rules/*.md` | 执行前必须读取的规则文件 |
