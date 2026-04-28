# Easy Analysis: incremental-implementation/SKILL.md

## 分析概要

### 文档定位
这是一个 Claude Code **技能定义文件**，规定了"增量实现"（incremental-implementation）这一工程流程的完整工作流。它是 `planning-and-task-breakdown` 的下游技能 —— 承接已拆解的任务，通过小步快跑的方式逐个实现、测试、验证和提交。

### 核心主张
**"用薄的垂直切片构建 —— 实现一块，测试一块，验证一块，然后扩展。"** 该 skill 的核心是一种执行纪律：避免一次性实现整个功能，而是让每个增量都使系统保持在可工作、可测试的状态。这是让大型功能变得可管理的实现方法论。

### 结构骨架

| 章节 | 内容 |
|------|------|
| 概述 + 使用时机 | 增量实现的目的和触发条件 |
| 增量周期（5 步） | 实现 → 测试 → 验证 → 提交 → 下一个切片 |
| 切片策略（3 种） | 垂直切片（首选）、契约优先切片、风险优先切片 |
| 实现规则（6 条） | 简洁优先、范围纪律、一次只做一件事、保持可编译、功能标志、安全默认、可回滚 |
| 与智能体协作 | 如何指导智能体进行增量实现 |
| 增量检查清单 | 每个增量后的验证项 |
| 常见借口 | 反驳"最后一起测试""一起做更快"等借口 |
| 危险信号 | 超过 100 行未测试、范围蔓延等 |
| 验证清单 | 完成所有增量后的确认项 |

### 关键洞察

1. **增量实现不是一种选择，而是一种纪律** — 文档反复强调"避免"、"不要"、"禁止"，这表明它不是温和的建议，而是强制性的执行框架。
2. **Rule 0 是"简洁优先"，Rule 0.5 是"范围纪律"** — 这种编号方式暗示了这两条规则比 Rule 1-5 更基础、更重要。它们位于所有具体技术规则之下。
3. **"小提交是免费的"** — 文档将"commit"作为增量周期的核心环节，这与许多开发者"攒大招"的习惯直接对立。

---

## Step 1: 逐段精读

### 段落 1: Frontmatter（元数据声明）

**原文:**
```yaml
---
name: incremental-implementation
description: Delivers changes incrementally. Use when implementing any feature or change that touches more than one file. Use when you're about to write a large amount of code at once, or when a task feels too big to land in one step.
---
```

**翻译:**
```yaml
---
name: incremental-implementation
description: 以增量方式交付变更。在实现任何触及多个文件的功能或变更时使用。当你即将一次性编写大量代码，或任务感觉太大无法一步落地时使用。
---
```

**要点:**
- **为什么重要**: Frontmatter 中的触发条件非常明确："touches more than one file"（触及多个文件）。这意味着即使是两个文件的变更，也应该使用增量实现。单文件变更才是例外。
- **隐含意义**: "when a task feels too big to land in one step" 再次捕捉到了开发者的心理状态 —— "落地焦虑"。增量实现不仅是一种技术方法，也是缓解这种焦虑的工具。
- **可执行建议**: 当你准备开始编码时，先问：这件事涉及几个文件？如果答案大于 1，启用 `/build`（或对应的增量实现流程）。

---

### 段落 2: 标题与概述

**原文:**
```markdown
# Incremental Implementation

## Overview

Build in thin vertical slices — implement one piece, test it, verify it, then expand. Avoid implementing an entire feature in one pass. Each increment should leave the system in a working, testable state. This is the execution discipline that makes large features manageable.
```

**翻译:**
```markdown
# 增量实现

## 概述

用薄的垂直切片构建 —— 实现一块，测试它，验证它，然后扩展。避免一次性实现整个功能。每个增量都应该让系统保持在可工作、可测试的状态。这是让大型功能变得可管理的执行纪律。
```

**要点:**
- **为什么重要**: 开篇即定义了增量实现的本质 —— 它不是"分阶段开发"，而是"每一步都交付可工作的软件"。关键词是 "working, testable state"（可工作、可测试的状态）。
- **隐含意义**: "execution discipline"（执行纪律）这个短语非常重要。它暗示了增量实现不是自然的、直觉的做事方式 —— 人类本能倾向于一次性做完。需要纪律来约束这种本能。
- **可执行建议**: 把"每个增量后系统必须可工作"作为不可违反的规则。如果某个增量使系统暂时 broken，说明切片不够薄。

---

### 段落 3: 使用时机

**原文:**
```markdown
## When to Use

- Implementing any multi-file change
- Building a new feature from a task breakdown
- Refactoring existing code
- Any time you're tempted to write more than ~100 lines before testing

**When NOT to use:** Single-file, single-function changes where the scope is already minimal.
```

**翻译:**
```markdown
## 使用时机

- 实现任何多文件变更
- 根据任务拆解构建新功能
- 重构现有代码
- 每当你 tempted 在测试前写超过约 100 行代码时

**不要使用：**范围已经最小的单文件、单函数变更。
```

**要点:**
- **为什么重要**: "Any time you're tempted to write more than ~100 lines before testing" 是一个量化触发器。100 行不是硬性限制，而是一个"警报阈值" —— 当你接近这个数字时，应该停下来测试。
- **隐含意义**:  refactoring（重构）被明确列入使用时机。这很重要，因为很多人以为增量实现只适用于新功能开发。实际上，重构更需要增量，因为它是在不改变外部行为的前提下修改代码，每一步都必须验证行为未被破坏。
- **可执行建议**: 在编辑器中设置一个视觉提醒（比如行号计数器），当未测试的代码接近 100 行时，强制自己停下来运行测试套件。

---

### 段落 4: The Increment Cycle（增量周期）

**原文:**
```markdown
## The Increment Cycle

```
┌──────────────────────────────────────┐
│                                      │
│   Implement ──→ Test ──→ Verify ──┐  │
│       ▲                           │  │
│       └───── Commit ◄─────────────┘  │
│              │                       │
│              ▼                       │
│          Next slice                  │
│                                      │
└──────────────────────────────────────┘
```

For each slice:

1. **Implement** the smallest complete piece of functionality
2. **Test** — run the test套件 (or write a test if none exists)
3. **Verify** — confirm the slice works as expected (tests pass, build succeeds, manual check)
4. **Commit** -- save your progress with a descriptive message (see `git-workflow-and-versioning` for atomic commit guidance)
5. **Move to the next slice** — carry forward, don't restart
```

**翻译:**
```markdown
## 增量周期

```
┌──────────────────────────────────────┐
│                                      │
│   实现 ──→ 测试 ──→ 验证 ──┐          │
│       ▲                    │          │
│       └──── 提交 ◄─────────┘          │
│              │                       │
│              ▼                       │
│          下一个切片                   │
│                                      │
└──────────────────────────────────────┘
```

对于每个切片：

1. **实现** 最小的完整功能块
2. **测试** —— 运行测试套件（如果没有则写一个测试）
3. **验证** —— 确认切片按预期工作（测试通过、构建成功、手动检查）
4. **提交** —— 用描述性消息保存进度（参见 `git-workflow-and-versioning` 获取原子提交指导）
5. **移动到下一个切片** —— 继续前进，不要重新开始
```

**要点:**
- **为什么重要**: ASCII 图展示了增量周期的闭环结构。注意箭头方向：实现 → 测试 → 验证 → 提交 → （循环回到）实现。提交不是终点，而是下一个周期的起点。
- **隐含意义**: "carry forward, don't restart"（继续前进，不要重新开始）是对"完美主义陷阱"的警告。有些开发者在完成一个增量后，会忍不住回头"优化"它。skill 要求你向前推进，而不是在原地打转。
- **可执行建议**: 严格按照 5 步顺序执行。不要跳过测试或验证直接提交，也不要实现了 3 个切片后才一起提交。

---

### 段落 5: Slicing Strategies — Vertical Slices (Preferred)

**原文:**
```markdown
## Slicing Strategies

### Vertical Slices (Preferred)

Build one complete path through the stack:

```
Slice 1: Create a task (DB + API + basic UI)
    → Tests pass, user can create a task via the UI

Slice 2: List tasks (query + API + UI)
    → Tests pass, user can see their tasks

Slice 3: Edit a task (update + API + UI)
    → Tests pass, user can modify tasks

Slice 4: Delete a task (delete + API + UI + confirmation)
    → Tests pass, full CRUD complete
```

Each slice delivers working end-to-end functionality.
```

**翻译:**
```markdown
## 切片策略

### 垂直切片（首选）

构建一条贯穿全栈的完整路径：

```
切片 1: 创建任务（数据库 + API + 基础 UI）
    → 测试通过，用户可以通过 UI 创建任务

切片 2: 列出任务（查询 + API + UI）
    → 测试通过，用户可以看到他们的任务

切片 3: 编辑任务（更新 + API + UI）
    → 测试通过，用户可以修改任务

切片 4: 删除任务（删除 + API + UI + 确认）
    → 测试通过，完整 CRUD 完成
```

每个切片都交付可工作的端到端功能。
```

**要点:**
- **为什么重要**: 垂直切片是增量实现的首选策略，与 `planning-and-task-breakdown` 中的垂直切片原则一致。它确保每个增量都是一个可演示、可验证的功能单元。
- **隐含意义**: 示例展示了一个 CRUD 功能的典型切片方式。注意 Slice 4 比前三个多了一个 "+ confirmation" —— 删除操作需要确认对话框，这是一个独立的 UI 关注点，被放在最后一个切片中。这表明切片不仅按操作类型分，还按复杂度分。
- **可执行建议**: 在规划切片时，问自己："这个切片完成后，用户能做什么他们之前做不到的事？"如果答案不明显，说明切片不够垂直。

---

### 段落 6: Contract-First Slicing

**原文:**
```markdown
### Contract-First Slicing

When backend and frontend need to develop in parallel:

```
Slice 0: Define the API contract (types, interfaces, OpenAPI spec)
Slice 1a: Implement backend against the contract + API tests
Slice 1b: Implement frontend against mock data matching the contract
Slice 2: Integrate and test end-to-end
```
```

**翻译:**
```markdown
### 契约优先切片

当后端和前端需要并行开发时：

```
切片 0: 定义 API 契约（类型、接口、OpenAPI 规范）
切片 1a: 基于契约实现后端 + API 测试
切片 1b: 基于匹配契约的模拟数据实现前端
切片 2: 集成并端到端测试
```
```

**要点:**
- **为什么重要**: 这是垂直切片的变体，专门针对前后端并行开发的场景。核心洞察是：并行开发需要一个"契约"作为同步点，否则两边会在集成时发生冲突。
- **隐含意义**: Slice 0 是特殊的 —— 它不交付用户可见的功能，但它是所有后续切片的前提。这说明了"基础设施先行"在某些场景下的必要性，即使它违背了纯垂直切片的原则。
- **可执行建议**: 在前后端并行时，永远不要跳过 Slice 0。即使只是定义一个 TypeScript 接口，也要把它写下来并让双方确认。

---

### 段落 7: Risk-First Slicing

**原文:**
```markdown
### Risk-First Slicing

Tackle the riskiest or most uncertain piece first:

```
Slice 1: Prove the WebSocket connection works (highest risk)
Slice 2: Build real-time task updates on the proven connection
Slice 3: Add offline support and reconnection
```

If Slice 1 fails, you discover it before investing in Slices 2 and 3.
```

**翻译:**
```markdown
### 风险优先切片

先处理风险最高或最不确定的部分：

```
切片 1: 证明 WebSocket 连接可用（最高风险）
切片 2: 在已验证的连接上构建实时任务更新
切片 3: 添加离线支持和重连
```

如果切片 1 失败，你在投入切片 2 和 3 之前就发现了。
```

**要点:**
- **为什么重要**: 这是增量实现与风险管理结合的切片策略。它呼应了 `planning-and-task-breakdown` 中的"fail fast"（快速失败）原则。风险优先切片确保你在投入大量工作之前，先验证最不确定的假设。
- **隐含意义**: WebSocket 示例非常典型 —— 网络连接的稳定性、实时通信的可靠性，这些都是高风险的领域。如果 WebSocket 连接在目标环境中根本无法工作，那么基于它的所有功能都是浪费时间。
- **可执行建议**: 在规划切片时，为每个切片标注风险等级。把"如果这部分失败，整个项目是否会受威胁？"的切片排在第一位。

---

### 段落 8: Rule 0: Simplicity First

**原文:**
```markdown
## Implementation Rules

### Rule 0: Simplicity First

Before writing any code, ask: "What is the simplest thing that could work?"

After writing code, review it against these checks:
- Can this be done in fewer lines?
- Are these abstractions earning their complexity?
- Would a staff engineer look at this and say "why didn't you just..."?
- Am I building for hypothetical future requirements, or the current task?

```
SIMPLICITY CHECK:
✗ Generic EventBus with middleware pipeline for one notification
✓ Simple function call

✗ Abstract factory pattern for two similar components
✓ Two straightforward components with shared utilities

✗ Config-driven form builder for three forms
✓ Three form components
```

Three similar lines of code is better than a premature abstraction. Implement the naive, obviously-correct version first. Optimize only after correctness is proven with tests.
```

**翻译:**
```markdown
## 实现规则

### 规则 0: 简洁优先

在写任何代码之前，问："能工作的最简单的东西是什么？"

写完代码后，对照以下检查点审查：
- 这能用更少的行数完成吗？
- 这些抽象配得上它们的复杂度吗？
- 一个资深工程师看了会说"你为什么不直接..."吗？
- 我是在为假设的未来需求构建，还是为当前任务构建？

```
简洁性检查:
✗ 为一个通知构建通用 EventBus 加中间件管道
✓ 简单函数调用

✗ 为两个相似组件使用抽象工厂模式
✓ 两个直白的组件加共享工具函数

✗ 为三个表单构建配置驱动的表单生成器
✓ 三个表单组件
```

三行相似的代码胜过早熟抽象。先实现朴素的、明显正确的版本。仅在正确性被测试证明后才优化。
```

**要点:**
- **为什么重要**: Rule 0 被编号为 0 而不是 1，表明它是最基础的规则，甚至优先于所有其他规则。简洁优先是增量实现的精神内核 —— 增量实现的目的就是防止过度复杂的代码一次性涌入代码库。
- **隐含意义**: "SIMPLICITY CHECK" 中的三个例子构成了一个递进模式：
  1. EventBus vs function call：不要为了"可能的扩展"而引入事件系统
  2. Abstract factory vs two components：不要为了"两个相似的东西"而引入设计模式
  3. Config-driven builder vs three components：不要为了"减少重复"而引入配置系统
  核心信息是：重复比错误的抽象更便宜。
- **可执行建议**: 在写任何代码前，强制自己回答那四个检查问题。特别是最后一个："Am I building for hypothetical future requirements?"（我是在为假设的未来需求构建吗？）如果答案是"是"，停下来，删掉那部分代码。

---

### 段落 9: Rule 0.5: Scope Discipline

**原文:**
```markdown
### Rule 0.5: Scope Discipline

Touch only what the task requires.

Do NOT:
- "Clean up" code adjacent to your change
- Refactor imports in files you're not modifying
- Remove comments you don't fully understand
- Add features not in the spec because they "seem useful"
- Modernize syntax in files you're only reading

If you notice something worth improving outside your task scope, note it — don't fix it:

```
NOTICED BUT NOT TOUCHING:
- src/utils/format.ts has an unused import (unrelated to this task)
- The auth middleware could use better error messages (separate task)
→ Want me to create tasks for these?
```
```

**翻译:**
```markdown
### 规则 0.5: 范围纪律

只触及任务要求的东西。

不要做：
- "清理"变更旁边的代码
- 重构你没有修改的文件中的导入语句
- 删除你不完全理解的注释
- 因为"看起来有用"而添加规格中没有的功能
- 在你只读取的文件中现代化语法

如果你注意到任务范围之外值得改进的地方，记下来 —— 不要修复它：

```
注意到但未触及:
- src/utils/format.ts 有一个未使用的导入（与此任务无关）
- 认证中间件可以使用更好的错误消息（单独任务）
→ 需要我为这些创建任务吗？
```
```

**要点:**
- **为什么重要**: Rule 0.5 紧接 Rule 0，说明范围纪律与简洁性同等基础。增量实现要求每个增量都是精确、可预测的 —— 范围蔓延会破坏这一点。
- **隐含意义**: "Remove comments you don't fully understand" 是一个常见陷阱。开发者（和 AI）看到"看起来过时"的注释就想删掉，但注释可能包含你不知道的上下文。这条规则要求谦逊：如果你不理解，就不要动。
- **可执行建议**: 采用 "NOTICED BUT NOT TOUCHING" 模式。当你想改某个与当前任务无关的东西时，把它写下来，然后继续当前任务。如果真的很重要，可以在任务完成后创建一个新任务。

---

### 段落 10: Rule 1: One Thing at a Time

**原文:**
```markdown
### Rule 1: One Thing at a Time

Each increment changes one logical thing. Don't mix concerns:

**Bad:** One commit that adds a new component, refactors an existing one, and updates the build config.

**Good:** Three separate commits — one for each change.
```

**翻译:**
```markdown
### 规则 1: 一次只做一件事

每个增量只改变一个逻辑事项。不要混合关注点：

**不好：**一个提交同时添加新组件、重构现有组件、更新构建配置。

**好：**三个独立的提交 —— 每个变更一个。
```

**要点:**
- **为什么重要**: 这是增量实现的"原子性"原则。每个增量应该是不可再分的最小逻辑单元。混合关注点使得代码审查、调试和回滚都变得困难。
- **隐含意义**: 示例中的三个变更（新组件、重构、构建配置）在开发者看来可能都是"为同一个功能服务"，但它们属于不同的关注点。构建配置的变更可能影响所有开发者，不应该与功能代码混在一起。
- **可执行建议**: 写完代码后，在提交前审查变更列表（`git diff --stat`）。如果看到多个文件的变更属于不同的逻辑主题，把它们拆分成多个提交。

---

### 段落 11: Rule 2: Keep It Compilable

**原文:**
```markdown
### Rule 2: Keep It Compilable

After each increment, the project must build and existing tests must pass. Don't leave the codebase in a broken state between slices.
```

**翻译:**
```markdown
### 规则 2: 保持可编译

每个增量之后，项目必须能构建，且现有测试必须通过。不要在切片之间让代码库处于损坏状态。
```

**要点:**
- **为什么重要**: 这是增量实现的"安全网"原则。如果每个增量后代码都是可编译的、测试通过的，那么当后续出现问题时，你可以确信问题出在最新的增量中，而不是累积的债务。
- **隐含意义**: "existing tests must pass" 是一个强约束。它不仅要求新代码正确，还要求新代码没有破坏旧代码。这是增量实现比"大爆炸式实现"更安全的原因。
- **可执行建议**: 将构建和测试命令设置为提交前的预提交钩子（pre-commit hook），或者至少养成"提交前必运行测试"的习惯。

---

### 段落 12: Rule 3: Feature Flags for Incomplete Features

**原文:**
```markdown
### Rule 3: Feature Flags for Incomplete Features

If a feature isn't ready for users but you need to merge increments:

```typescript
// Feature flag for work-in-progress
const ENABLE_TASK_SHARING = process.env.FEATURE_TASK_SHARING === 'true';

if (ENABLE_TASK_SHARING) {
  // New sharing UI
}
```

This lets you merge small increments to the main branch without exposing incomplete work.
```

**翻译:**
```markdown
### 规则 3: 未完成功能的特性标志

如果某个功能尚未准备好给用户使用，但你需要合并增量：

```typescript
// 进行中的工作特性标志
const ENABLE_TASK_SHARING = process.env.FEATURE_TASK_SHARING === 'true';

if (ENABLE_TASK_SHARING) {
  // 新分享 UI
}
```

这让你可以将小的增量合并到主分支，而不暴露未完成的工作。
```

**要点:**
- **为什么重要**: 特性标志（feature flag）是增量实现与持续集成（CI）的桥梁。它允许你频繁地将代码合并到主分支，同时控制功能的可见性。没有特性标志，增量实现会被"不能合并未完成代码"的约束所阻碍。
- **隐含意义**: 示例使用了环境变量作为最简单的特性标志机制。这不是唯一的方式（也可以用配置系统、用户权限等），但它是最轻量、最容易移除的。
- **可执行建议**: 在 Slice 1 中就引入特性标志，而不是等到"功能差不多完成了"再加。特性标志应该伴随功能的第一个增量一起出现。

---

### 段落 13: Rule 4: Safe Defaults

**原文:**
```markdown
### Rule 4: Safe Defaults

New code should default to safe, conservative behavior:

```typescript
// Safe: disabled by default, opt-in
export function createTask(data: TaskInput, options?: { notify?: boolean }) {
  const shouldNotify = options?.notify ?? false;
  // ...
}
```
```

**翻译:**
```markdown
### 规则 4: 安全默认

新代码应该默认使用安全、保守的行为：

```typescript
// 安全：默认禁用，选择性启用
export function createTask(data: TaskInput, options?: { notify?: boolean }) {
  const shouldNotify = options?.notify ?? false;
  // ...
}
```
```

**要点:**
- **为什么重要**: 安全默认是增量实现的"防御性编程"原则。当新功能被意外启用时（比如特性标志配置错误），默认行为不应该造成损害。
- **隐含意义**: 示例中的 `?? false`（空值合并为 false）是一个微小的但重要的选择。如果默认是 `true`，那么未传递 `notify` 选项的调用者会意外触发通知。默认 false 是安全的，因为"不通知"比"意外通知"更容易被容忍。
- **可执行建议**: 在设计新 API 或功能时，问自己："如果用户不知道这个功能存在，默认行为会伤害他们吗？"如果答案是"是"，让默认行为是无害的。

---

### 段落 14: Rule 5: Rollback-Friendly

**原文:**
```markdown
### Rule 5: Rollback-Friendly

Each increment should be independently revertable:

- Additive changes (new files, new functions) are easy to revert
- Modifications to existing code should be minimal and focused
- Database migrations should have corresponding rollback migrations
- Avoid deleting something in one commit and replacing it in the same commit — separate them
```

**翻译:**
```markdown
### 规则 5: 可回滚

每个增量都应该可以独立回滚：

- 增量式变更（新文件、新函数）容易回滚
- 对现有代码的修改应该最小且聚焦
- 数据库迁移应该有对应的回滚迁移
- 避免在一个提交中删除某物并在同一提交中替换它 —— 把它们分开
```

**要点:**
- **为什么重要**: 可回滚性是增量实现的"保险"。如果某个增量引入了问题，你应该能只回滚那个增量，而不影响前后增量。这使得修复问题的成本极低。
- **隐含意义**: "Avoid deleting something in one commit and replacing it in the same commit" 是一个容易被忽视的规则。如果一个提交同时删除了旧实现和添加了新实现，回滚这个提交会导致功能完全消失。分开后，你可以先回滚新实现，恢复旧实现，然后排查问题。
- **可执行建议**: 在提交前问自己："如果明天这个提交导致了生产事故，我能否只 revert 这一个提交就恢复？"如果答案是否，拆分它。

---

### 段落 15: Working with Agents

**原文:**
```markdown
## Working with Agents

When directing an agent to implement incrementally:

```
"Let's implement Task 3 from the plan.

Start with just the database schema change and the API endpoint.
Don't touch the UI yet — we'll do that in the next increment.

After implementing, run `npm test` and `npm run build` to verify
nothing is broken."
```

Be explicit about what's in scope and what's NOT in scope for each increment.
```

**翻译:**
```markdown
## 与智能体协作

当指导智能体进行增量实现时：

```
"让我们实现计划中的任务 3。

先从数据库架构变更和 API 端点开始。
先不要碰 UI —— 我们在下一个增量中再做。

实现后，运行 `npm test` 和 `npm run build` 验证
没有破坏任何东西。"
```

对每个增量的范围内和范围外内容要明确。
```

**要点:**
- **为什么重要**: 这一段提供了与 AI 协作的**具体话术模板**。它不是抽象的建议，而是可以复制粘贴的指令格式。这对使用 Claude Code 的人类非常有价值。
- **隐含意义**: 指令中的关键元素：
  1. 引用计划中的具体任务（"Task 3"）
  2. 明确限定范围（"just the database schema change and the API endpoint"）
  3. 明确排除范围（"Don't touch the UI yet"）
  4. 指定验证命令（"run `npm test` and `npm run build`"）
  这种结构化的指令比"实现任务 3"有效得多。
- **可执行建议**: 与 Claude 协作时，使用这个模板格式。永远不要只说"实现 X"，而要明确"先做什么"、"不做什么"、"完成后运行什么测试"。

---

### 段落 16: Increment Checklist

**原文:**
```markdown
## Increment Checklist

After each increment, verify:

- [ ] The change does one thing and does it completely
- [ ] All existing tests still pass (`npm test`)
- [ ] The build succeeds (`npm run build`)
- [ ] Type checking passes (`npx tsc --noEmit`)
- [ ] Linting passes (`npm run lint`)
- [ ] The new functionality works as expected
- [ ] The change is committed with a descriptive message
```

**翻译:**
```markdown
## 增量检查清单

每个增量之后，验证：

- [ ] 变更只做一件事，并且做完整了
- [ ] 所有现有测试仍然通过（`npm test`）
- [ ] 构建成功（`npm run build`）
- [ ] 类型检查通过（`npx tsc --noEmit`）
- [ ] 代码检查通过（`npm run lint`）
- [ ] 新功能按预期工作
- [ ] 变更已提交，附带描述性消息
```

**要点:**
- **为什么重要**: 这是增量实现的**操作检查清单**。它将前面的规则转化为可执行的、可勾选的步骤。每个增量后必须完成这 7 项。
- **隐含意义**: 检查清单中包含类型检查（`npx tsc --noEmit`）和代码检查（`npm run lint`），说明增量实现不仅关注功能正确性，还关注代码质量。编译错误和代码风格问题应该在增量内解决，而不是累积到最后。
- **可执行建议**: 将这个检查清单复制到你的项目 README 中，或者作为提交前的个人检查习惯。不要跳过任何一项 —— 特别是类型检查和代码检查。

---

### 段落 17: Common Rationalizations

**原文:**
```markdown
## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll test it all at the end" | Bugs compound. A bug in Slice 1 makes Slices 2-5 wrong. Test each slice. |
| "It's faster to do it all at once" | It *feels* faster until something breaks and you can't find which of 500 changed lines caused it. |
| "These changes are too small to commit separately" | Small commits are free. Large commits hide bugs and make rollbacks painful. |
| "I'll add the feature flag later" | If the feature isn't complete, it shouldn't be user-visible. Add the flag now. |
| "This refactor is small enough to include" | Refactors mixed with features make both harder to review and debug. Separate them. |
```

**翻译:**
```markdown
## 常见借口

| 借口 | 现实 |
|---|---|
| "我最后会一起测试" | Bug 会累积。切片 1 的 bug 会让切片 2-5 都出错。每个切片都要测试。 |
| "一起做更快" | 它*感觉*更快，直到某处坏了，你找不到 500 行变更中哪一行导致的。 |
| "这些变更太小了，不值得分开提交" | 小提交是免费的。大提交隐藏 bug 并让回滚痛苦。 |
| "我稍后加特性标志" | 如果功能不完整，它就不应该对用户可见。现在就加标志。 |
| "这个重构足够小，可以包含进来" | 重构与功能混合会让两者都更难审查和调试。分开它们。 |
```

**要点:**
- **为什么重要**: 这一段直接针对增量实现最常遇到的阻力。"一起做更快"是最危险的幻觉 —— 文档用"500 行变更中找 bug"的场景来戳破它。
- **隐含意义**: "Small commits are free"（小提交是免费的）是一个有力的修辞。它纠正了"提交有成本"的潜意识。在 Git 中，创建一个提交的成本接近于零，但它的价值（可追溯性、可回滚性）是巨大的。
- **可执行建议**: 当团队有人说"这次就一起提交吧"时，引用第三点："小提交是免费的，大提交是昂贵的。"

---

### 段落 18: Red Flags

**原文:**
```markdown
## Red Flags

- More than 100 lines of code written without running tests
- Multiple unrelated changes in a single increment
- "Let me just quickly add this too" scope expansion
- Skipping the test/verify step to move faster
- Build or tests broken between increments
- Large uncommitted changes accumulating
- Building abstractions before the third use case demands it
- Touching files outside the task scope "while I'm here"
- Creating new utility files for one-time operations
```

**翻译:**
```markdown
## 危险信号

- 写了超过 100 行代码还没运行测试
- 一个增量中包含多个无关变更
- "让我快速把这个也加上"的范围蔓延
- 为了快而跳过测试/验证步骤
- 增量之间构建或测试损坏
- 大量未提交的变更累积
- 在第三个用例需要之前就构建抽象
- "既然我在这里"就触及任务范围外的文件
- 为一次性操作创建新的工具文件
```

**要点:**
- **为什么重要**: 危险信号列表比 `spec-driven-development` 和 `planning-and-task-breakdown` 更长，说明增量实现是最容易出问题的环节 —— 因为它涉及实际的编码，而编码时人的冲动最强。
- **隐含意义**: "Building abstractions before the third use case demands it" 是对 YAGNI（You Aren't Gonna Need It）原则的重述。它用"第三个用例"作为量化的阈值 —— 两个用例的重复不值得抽象，三个或更多才值得考虑。
- **可执行建议**: 把这段危险信号列表贴在显示器旁边（或保存在笔记中）。当你发现自己正在做其中任何一件事时，停下来，回退，重新开始。

---

### 段落 19: Verification

**原文:**
```markdown
## Verification

After completing all increments for a task:

- [ ] Each increment was individually tested and committed
- [ ] The full test suite passes
- [ ] The build is clean
- [ ] The feature works end-to-end as specified
- [ ] No uncommitted changes remain
```

**翻译:**
```markdown
## 验证

完成任务的所有增量后：

- [ ] 每个增量都经过了单独测试和提交
- [ ] 完整测试套件通过
- [ ] 构建干净
- [ ] 功能按规格端到端工作
- [ ] 没有未提交的变更遗留
```

**要点:**
- **为什么重要**: 这是任务级别的验证清单，区别于增量级别的检查清单。它在所有增量完成后执行，确保"树木"（增量）组合成了正确的"森林"（功能）。
- **隐含意义**: "Each increment was individually tested and committed" 强调了"单独"二字。不是"所有增量一起测试了一次"，而是每个增量都有自己的测试和提交记录。这是可追溯性的基础。
- **可执行建议**: 在宣布一个任务"完成"之前，物理地勾选这个清单。特别是最后一项 "No uncommitted changes remain" —— 未提交的变更意味着工作没有真正落地。

---

## Step 3: 整体总结

### 核心概念

| 概念 | 定义 |
|------|------|
| **Increment**（增量） | 最小的完整功能块，实现后系统仍处于可工作、可测试状态。 |
| **Vertical Slice**（垂直切片） | 按用户场景而非技术层拆解实现，每个切片都交付端到端可工作功能。 |
| **Feature Flag**（特性标志） | 控制未完成功能可见性的开关，允许代码合并但不暴露给用户。 |
| **Safe Default**（安全默认） | 新功能的默认行为应该是无害的、保守的，需要显式启用才会产生副作用。 |
| **Rollback-Friendly**（可回滚） | 每个增量应该可以独立 revert，不依赖其他增量。 |
| **Scope Discipline**（范围纪律） | 只触及任务要求的内容，对范围外的改进只做记录不动手。 |

### 工作流程

```
开始实现任务
  │
  ▼
选择切片策略
  │
  ├── 垂直切片（默认）→ 按用户场景（注册 → 登录 → 创建）
  ├── 契约优先 → 前后端并行时，先定义 API 契约
  └── 风险优先 → 最不确定的部分放在第一个切片
  │
  ▼
进入增量周期（对每个切片循环）
  │
  ┌──────────────────────────────────────────┐
  │  1. Implement（实现最小完整功能）          │
  │  2. Test（运行测试，或写测试）             │
  │  3. Verify（确认测试通过、构建成功）       │
  │  4. Commit（用描述性消息提交）             │
  │  5. Next slice（继续下一个切片）           │
  └──────────────────────────────────────────┘
  │
  ▼
任务完成验证
  - 每个增量都单独测试和提交
  - 完整测试套件通过
  - 端到端功能按规格工作
  - 没有未提交变更
```

### 实现规则层级

```
Foundation（基础层）
├── Rule 0: Simplicity First（简洁优先）
│   └── "能工作的最简单的东西是什么？"
└── Rule 0.5: Scope Discipline（范围纪律）
    └── "只触及任务要求的东西"

Execution（执行层）
├── Rule 1: One Thing at a Time（一次一件事）
├── Rule 2: Keep It Compilable（保持可编译）
├── Rule 3: Feature Flags（特性标志）
├── Rule 4: Safe Defaults（安全默认）
└── Rule 5: Rollback-Friendly（可回滚）
```

### 关键文件

| 文件 | 作用 |
|------|------|
| `skills/incremental-implementation/SKILL.md` | 本 skill 的定义文件，包含增量周期、切片策略和 6 条实现规则 |
| `docs/agent-skills/03-incremental-implementation-analysis.md` | 本分析文件，提供对 SKILL.md 的逐段精读和总结 |

### 与其他 Skill 的关系

- **前置**: `planning-and-task-breakdown`（必须先有计划，才能增量实现）
- **并行/协同**: `test-driven-development`（每个增量都应该伴随测试）
- **后置**: `git-workflow-and-versioning`（增量周期中的 commit 步骤需要遵循原子提交规范）

### 使用建议

1. **100 行是警报线** — 当你写了 100 行还没测试时，停下来。这不是建议，是纪律。
2. **Rule 0 和 0.5 是最容易被违反的** — 它们编号为 0 和 0.5 是有原因的。在考虑任何具体规则之前，先确保代码是简单的、范围是受控的。
3. **特性标志必须在第一个增量就引入** — 不要"等差不多完成了再加"。没有特性标志，你就不能安全地合并未完成代码。
4. **"NOTICED BUT NOT TOUCHING" 是防止范围蔓延的利器** — 养成记录但不修复的习惯，让当前任务保持纯粹。
5. **小提交是免费的，大提交是昂贵的** — 每次增量后都提交。Git 的存储效率极高，提交的成本接近于零，但回滚的价值巨大。
