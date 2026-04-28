# Easy Analysis: spec-driven-development/SKILL.md

## 分析概要

### 文档定位
这是一个 Claude Code **技能定义文件（skill definition）**，规定了"spec-driven development"（规格驱动开发）这一工程流程的完整工作流。

### 核心主张
**"不写规格，不写代码"** — 在编码之前先写结构化的规格说明，将规格作为人机之间的共享真相源（shared source of truth），通过四阶段门控流程（Specify → Plan → Tasks → Implement）确保需求在编码前就被澄清和验证。

### 结构骨架

| 章节 | 内容 |
|------|------|
| 概述 + 使用时机 | 什么是规格驱动开发，何时使用、何时不使用 |
| 门控工作流 | 四阶段流程：Specify → Plan → Tasks → Implement，每阶段需人工审核 |
| Phase 1: Specify | 核心阶段：假设暴露、六大核心区域、规格模板、重述成功标准 |
| Phase 2: Plan | 技术实现计划：组件、依赖、顺序、风险、验证点 |
| Phase 3: Tasks | 将计划拆解为可执行、可验证的任务 |
| Phase 4: Implement | 使用其他 skill 执行任务 |
| Keeping the Spec Alive | 规格是活的文档，需持续更新 |
| Common Rationalizations | 反驳常见的"不写规格"借口 |
| Red Flags | 危险信号：无规格编码、猜测式实现 |
| Verification | 进入实现前的确认清单 |

### 关键洞察

1. **这不是瀑布模型，而是快速对齐** — 规格不需要写得很长，15 分钟的规格能避免数小时的返工。
2. **核心防御机制是"假设暴露"** — 大部分编码错误源于隐含的、未经检验的假设，规格的首要价值是把这些假设摆到台面上。
3. **规格必须进入版本控制** — 它不只是对话中的一段文字，而是与代码同等的工程产物。

---

## Step 1: 逐段精读

### 段落 1: Frontmatter（元数据声明）

**原文:**
```yaml
---
name: spec-driven-development
description: Creates specs before coding. Use when starting a new project, feature, or significant change and no specification exists yet. Use when requirements are unclear, ambiguous, or only exist as a vague idea.
---
```

**翻译:**
```yaml
---
name: spec-driven-development
description: 在编码前创建规格。在启动新项目、新功能或重大变更且尚无规格时使用。在需求不清晰、模糊或仅存在于模糊想法时使用。
---
```

**要点:**
- **为什么重要**: 这段 frontmatter 定义了 skill 的触发条件（trigger conditions）。它不是"总是使用"，而是有明确的使用场景边界。
- **隐含意义**: 该 skill 被设计为对话入口 —— 当 Claude 检测到用户处于"没有规格就开始编码"的状态时，应该主动建议启用此 skill。
- **可执行建议**: 作为使用者，应在每次新任务开始时自问："我有清晰的规格吗？"如果没有，就调用 `/spec` 命令。

---

### 段落 2: 标题与概述

**原文:**
```markdown
# Spec-Driven Development

## Overview

Write a structured specification before writing any code. The spec is the shared source of truth between you and the human engineer — it defines what we're building, why, and how we'll know it's done. Code without a spec is guessing.
```

**翻译:**
```markdown
# 规格驱动开发

## 概述

在写任何代码之前，先写一份结构化的规格说明。规格是你与人工工程师之间的共享真相源 —— 它定义了我们要构建什么、为什么构建，以及我们如何知道它已经完成了。没有规格的代码就是猜测。
```

**要点:**
- **为什么重要**: 明确定义了"规格"的本质 —— 不是技术文档，而是**人机之间的共享真相源（shared source of truth）**。这意味着规格必须被双方认可，而不是 Claude 单方面输出。
- **隐含意义**: 最后一句"Code without a spec is guessing"（没有规格的代码就是猜测）是一种强有力的价值主张，把整个 skill 的存在理由浓缩成一句话。它暗示了：如果你跳过规格，你不是在节省时间在赌博。
- **可执行建议**: 规格必须回答三个问题：What（构建什么）、Why（为什么）、How we'll know it's done（如何知道完成）。缺少任何一个维度，规格就不完整。

---

### 段落 3: 使用时机

**原文:**
```markdown
## When to Use

- Starting a new project or feature
- Requirements are ambiguous or incomplete
- The change touches multiple files or modules
- You're about to make an architectural decision
- The task would take more than 30 minutes to implement

**When NOT to use:** Single-line fixes, typo corrections, or changes where requirements are unambiguous and self-contained.
```

**翻译:**
```markdown
## 使用时机

- 启动新项目或新功能
- 需求模糊或不完整
- 变更涉及多个文件或模块
- 你即将做出架构决策
- 任务预计需要超过 30 分钟来实现

**不要使用：**单行修复、拼写更正，或需求明确且自包含的变更。
```

**要点:**
- **为什么重要**: 明确了 skill 的适用范围。特别注意"30 分钟"这个量化阈值 —— 它提供了一个实用的决策边界，避免在 trivial 的事情上过度流程化。
- **隐含意义**: "多个文件或模块"的提及暗示了规格的耦合分析价值。规格的存在强迫你在编码前思考变更范围，避免代码完成后才发现影响面超出预期。
- **可执行建议**: 面对一个新任务时，用 30 分钟规则快速判断是否需要正式规格。不需要为改一个变量名写规格，但为一个新 API 端点写规格是值得的。

---

### 段落 4: 门控工作流

**原文:**
```markdown
## The Gated Workflow

Spec-driven development has four phases. Do not advance to the next phase until the current one is validated.

```
SPECIFY ──→ PLAN ──→ TASKS ──→ IMPLEMENT
   │          │        │          │
   ▼          ▼        ▼          ▼
 Human      Human    Human      Human
 reviews    reviews  reviews    reviews
```
```

**翻译:**
```markdown
## 门控工作流

规格驱动开发有四个阶段。在当前阶段被验证之前，不要进入下一阶段。

```
规格化 ──→ 计划 ──→ 任务 ──→ 实现
   │          │        │          │
   ▼          ▼        ▼          ▼
 人工审核   人工审核  人工审核   人工审核
```
```

**要点:**
- **为什么重要**: "Gated Workflow"（门控工作流）是这个 skill 的核心机制。每个阶段都有"门"，必须通过人工审核才能解锁下一阶段。这不是自动化流水线，而是人机协作的节奏控制。
- **隐含意义**: ASCII 流程图明确显示了**四个阶段下方都有"Human reviews"（人工审核）**。这意味着 Claude 不能自己决定进入下一阶段 —— 它必须停下来等待人类确认。这个设计防止了 AI 自作主张地快速推进而人类还没跟上。
- **可执行建议**: 在实际使用 `/spec` 命令时，要有意识地等待每个阶段的"门"被打开。不要在人类还没确认规格时就跳入计划阶段，即使 Claude 已经"知道"下一步该怎么做。

---

### 段落 5: Phase 1: Specify — 开头段

**原文:**
```markdown
### Phase 1: Specify

Start with a high-level vision. Ask the human clarifying questions until requirements are concrete.
```

**翻译:**
```markdown
### 阶段 1：规格化

从高层愿景开始。向人类提出澄清问题，直到需求变得具体。
```

**要点:**
- **为什么重要**: 这个阶段的核心动作不是"写"，而是"问"。规格化的起点是**对话和澄清**，而不是 Claude 单方面输出一份文档。
- **隐含意义**: "Ask the human clarifying questions" 强调了 AI 的主动性 —— 好的 AI 助手不是被动等待指令，而是在检测到模糊性时主动提问。
- **可执行建议**: 在使用此 skill 时，Claude 应该在写规格前先列出 3-5 个澄清问题，确保人类和 AI 对需求的理解一致。

---

### 段落 6: Surface assumptions immediately

**原文:**
```markdown
**Surface assumptions immediately.** Before writing any spec content, list what you're assuming:

```
ASSUMPTIONS I'M MAKING:
1. This is a web application (not native mobile)
2. Authentication uses session-based cookies (not JWT)
3. The database is PostgreSQL (based on existing Prisma schema)
4. We're targeting modern browsers only (no IE11)
→ Correct me now or I'll proceed with these.
```

Don't silently fill in ambiguous requirements. The spec's entire purpose is to surface misunderstandings *before* code gets written — assumptions are the most dangerous form of misunderstanding.
```

**翻译:**
```markdown
**立即暴露假设。** 在写任何规格内容之前，列出你的假设：

```
我正在做的假设：
1. 这是一个 Web 应用（不是原生移动应用）
2. 认证使用基于会话的 Cookie（不是 JWT）
3. 数据库是 PostgreSQL（基于现有的 Prisma 架构）
4. 我们只针对现代浏览器（不支持 IE11）
→ 现在就纠正我，否则我将按这些假设继续。
```

不要默默地填补模糊的需求。规格的全部目的就是在代码被写出来之前暴露误解 —— 假设是最危险的误解形式。
```

**要点:**
- **为什么重要**: 这是整个 skill 中最关键的实践之一。假设往往是隐性的，而且恰恰是这些隐性假设导致了最多的返工。文档明确要求在写规格**之前**先列出假设。
- **隐含意义**: 示例中的假设列表展示了一个技巧 —— 每个假设都带有一个简短的依据说明（"based on existing Prisma schema"），这让人类更容易判断假设是否合理。
- **可执行建议**: 模板末尾的 "Correct me now or I'll proceed with these" 是一个强有力的行动号召（call to action）。它设定了明确的截止时间，迫使人类立即响应，而不是拖延。

---

### 段落 7: Write a spec document — 六大核心区域

**原文:**
```markdown
**Write a spec document covering these six core areas:**

1. **Objective** — What are we building and why? Who is the user? What does success look like?

2. **Commands** — Full executable commands with flags, not just tool names.
   ```
   Build: npm run build
   Test: npm test -- --coverage
   Lint: npm run lint --fix
   Dev: npm run dev
   ```

3. **Project Structure** — Where source code lives, where tests go, where docs belong.
   ```
   src/           → Application source code
   src/components → React components
   src/lib        → Shared utilities
   tests/         → Unit and integration tests
   e2e/           → End-to-end tests
   docs/          → Documentation
   ```

4. **Code Style** — One real code snippet showing your style beats three paragraphs describing it. Include naming conventions, formatting rules, and examples of good output.

5. **Testing Strategy** — What framework, where tests live, coverage expectations, which test levels for which concerns.

6. **Boundaries** — Three-tier system:
   - **Always do:** Run tests before commits, follow naming conventions, validate inputs
   - **Ask first:** Database schema changes, adding dependencies, changing CI config
   - **Never do:** Commit secrets, edit vendor directories, remove failing tests without approval
```

**翻译:**
```markdown
**编写一份涵盖这六个核心区域的规格文档：**

1. **目标** — 我们要构建什么，为什么？用户是谁？成功是什么样子？

2. **命令** — 完整的可执行命令及其标志，不只是工具名称。
   ```
   构建: npm run build
   测试: npm test -- --coverage
   检查: npm run lint --fix
   开发: npm run dev
   ```

3. **项目结构** — 源代码放在哪里，测试放在哪里，文档属于哪里。
   ```
   src/           → 应用源代码
   src/components → React 组件
   src/lib        → 共享工具函数
   tests/         → 单元测试和集成测试
   e2e/           → 端到端测试
   docs/          → 文档
   ```

4. **代码风格** — 一个真实的代码片段展示你的风格，胜过三段描述它的文字。包含命名约定、格式化规则和好输出的示例。

5. **测试策略** — 使用什么框架，测试放在哪里，覆盖率期望，哪些关注点用哪些测试级别。

6. **边界** — 三层系统：
   - **总是做：** 提交前运行测试，遵循命名约定，验证输入
   - **先询问：** 数据库架构变更、添加依赖、修改 CI 配置
   - **绝不做：** 提交密钥、编辑 vendor 目录、未经批准删除失败的测试
```

**要点:**
- **为什么重要**: 这是规格的**内容标准**。六个区域覆盖了从"为什么"（Objective）到"怎么做"（Commands, Project Structure）到"什么不能做"（Boundaries）的完整光谱。
- **隐含意义**: 
  - **Commands** 区域强调"完整可执行命令"，这避免了"用 jest 测试"这种模糊指令，转而要求 "`npm test -- --coverage`"这种可以直接复制粘贴的命令。
  - **Boundaries** 的三层系统（Always/Ask First/Never）是一个精妙的权力分配机制。它明确了 AI 的自主权范围（Always）、需要协商的范围（Ask First）、以及绝对禁区（Never）。
- **可执行建议**: 在实际写规格时，不要跳过任何一个区域。即使某个区域的内容很短（比如"Code Style: 遵循现有项目的 ESLint 配置"），也应该明确写出来，而不是省略。

---

### 段落 8: Spec template（规格模板）

**原文:**
```markdown
**Spec template:**

```markdown
# Spec: [Project/Feature Name]

## Objective
[What we're building and why. User stories or acceptance criteria.]

## Tech Stack
[Framework, language, key dependencies with versions]

## Commands
[Build, test, lint, dev — full commands]

## Project Structure
[Directory layout with descriptions]

## Code Style
[Example snippet + key conventions]

## Testing Strategy
[Framework, test locations, coverage requirements, test levels]

## Boundaries
- Always: [...]
- Ask first: [...]
- Never: [...]

## Success Criteria
[How we'll know this is done — specific, testable conditions]

## Open Questions
[Anything unresolved that needs human input]
```
```

**翻译:**
```markdown
**规格模板：**

```markdown
# 规格：[项目/功能名称]

## 目标
[我们要构建什么以及为什么。用户故事或验收标准。]

## 技术栈
[框架、语言、关键依赖及其版本]

## 命令
[构建、测试、检查、开发 —— 完整命令]

## 项目结构
[目录布局及说明]

## 代码风格
[示例片段 + 关键约定]

## 测试策略
[框架、测试位置、覆盖率要求、测试级别]

## 边界
- 总是做：[...]
- 先询问：[...]
- 绝不做：[...]

## 成功标准
[我们如何知道这件事完成了 —— 具体的、可测试的条件]

## 开放问题
[任何尚未解决、需要人工输入的事项]
```
```

**要点:**
- **为什么重要**: 这是一个可直接使用的 Markdown 模板。它的存在降低了"写规格"的认知负担 —— 用户不需要从零开始构思格式，只需要填空。
- **隐含意义**: 模板末尾的 **"Open Questions"（开放问题）** 是一个容易被忽视但极其重要的部分。它承认规格不是一次性完美的，而是有明确的知识缺口需要后续填补。这创造了一种健康的对话文化。
- **可执行建议**: 保存这个模板到项目目录中（例如 `docs/templates/spec-template.md`），并在每次启动新功能时复制它。不要试图凭记忆重写规格结构。

---

### 段落 9: Reframe instructions as success criteria

**原文:**
```markdown
**Reframe instructions as success criteria.** When receiving vague requirements, translate them into concrete conditions:

```
REQUIREMENT: "Make the dashboard faster"

REFRAMED SUCCESS CRITERIA:
- Dashboard LCP < 2.5s on 4G connection
- Initial data load completes in < 500ms
- No layout shift during load (CLS < 0.1)
→ Are these the right targets?
```

This lets you loop, retry, and problem-solve toward a clear goal rather than guessing what "faster" means.
```

**翻译:**
```markdown
**将指令重述为成功标准。** 当收到模糊的需求时，将它们转化为具体的条件：

```
需求："让仪表盘更快"

重述后的成功标准：
- 仪表盘在 4G 连接下 LCP < 2.5s
- 初始数据加载在 500ms 内完成
- 加载期间无布局偏移（CLS < 0.1）
→ 这些是正确的目标吗？
```

这让你能够围绕一个清晰的目标进行循环、重试和问题解决，而不是猜测"更快"意味着什么。
```

**要点:**
- **为什么重要**: 这是将**定性需求转化为定量指标**的技术。模糊需求（如"更快"、"更好"、"更稳定"）是项目延期的主要来源，因为它们无法在代码层面被验证。
- **隐含意义**: 示例中使用了 Web Vitals 指标（LCP、CLS），暗示了该 skill 的目标受众是前端/全栈开发者。但这种方法论是通用的 —— 任何领域都可以找到可量化的验收标准。
- **可执行建议**: 面对任何形容词驱动的需求（faster, better, cleaner, more robust）时，自动触发这个重构流程。不要接受没有数字的验收标准。

---

### 段落 10: Phase 2: Plan

**原文:**
```markdown
### Phase 2: Plan

With the validated spec, generate a technical implementation plan:

1. Identify the major components and their dependencies
2. Determine the implementation order (what must be built first)
3. Note risks and mitigation strategies
4. Identify what can be built in parallel vs. what must be sequential
5. Define verification checkpoints between phases

The plan should be reviewable: the human should be able to read it and say "yes, that's the right approach" or "no, change X."
```

**翻译:**
```markdown
### 阶段 2：计划

使用经过验证的规格，生成技术实现计划：

1. 识别主要组件及其依赖关系
2. 确定实现顺序（什么必须先构建）
3. 记录风险和缓解策略
4. 识别哪些可以并行构建，哪些必须串行构建
5. 定义阶段之间的验证检查点

该计划应该是可审核的：人类应该能够阅读它并说"是的，这是正确的方法"或"不，改变 X"。
```

**要点:**
- **为什么重要**: 计划阶段填补了"规格（做什么）"和"任务（怎么做）"之间的鸿沟。它的产出是技术层面的实现策略，而不是具体代码。
- **隐含意义**: 第 4 点（并行 vs 串行）暗示了这个 skill 是为非平凡项目设计的。对于简单任务，所有工作都是串行的；但当涉及多个组件时，并行化规划能显著提高效率。
- **可执行建议**: 计划阶段的一个关键验收标准是**可审核性（reviewable）**。如果人类看完计划后无法给出"是"或"否"的判断，说明计划还不够清晰。好的计划应该让人类能在 2 分钟内做出判断。

---

### 段落 11: Phase 3: Tasks

**原文:**
```markdown
### Phase 3: Tasks

Break the plan into discrete, implementable tasks:

- Each task should be completable in a single focused session
- Each task has explicit acceptance criteria
- Each task includes a verification step (test, build, manual check)
- Tasks are ordered by dependency, not by perceived importance
- No task should require changing more than ~5 files

**Task template:**
```markdown
- [ ] Task: [Description]
  - Acceptance: [What must be true when done]
  - Verify: [How to confirm — test command, build, manual check]
  - Files: [Which files will be touched]
```
```

**翻译:**
```markdown
### 阶段 3：任务

将计划拆解为离散的、可执行的任务：

- 每个任务应该能在一次专注的会话中完成
- 每个任务都有明确的验收标准
- 每个任务都包含一个验证步骤（测试、构建、手动检查）
- 任务按依赖关系排序，而不是按感知的重要性排序
- 任何任务都不应需要修改超过约 5 个文件

**任务模板：**
```markdown
- [ ] 任务：[描述]
  - 验收标准：[完成时必须为真的事项]
  - 验证：[如何确认 —— 测试命令、构建、手动检查]
  - 文件：[将触及哪些文件]
```
```

**要点:**
- **为什么重要**: 这是从"规划"到"执行"的转换点。任务的粒度控制是这个 skill 的精髓 —— "单次专注会话"、"最多 5 个文件" 这些约束防止了任务过大导致的认知过载。
- **隐含意义**: "按依赖关系排序，而不是按感知的重要性排序"是一个反直觉但极其重要的规则。人类倾向于先做"重要的"或"有趣的"部分，但如果 B 依赖 A，先做 B 会导致阻塞和返工。
- **可执行建议**: "最多 5 个文件"是一个经验法则。它的目的不是严格限制文件数量，而是作为一个** smells detector** —— 如果一个任务需要修改 15 个文件，说明它应该被进一步拆分。

---

### 段落 12: Phase 4: Implement

**原文:**
```markdown
### Phase 4: Implement

Execute tasks one at a time following `incremental-implementation` and `test-driven-development` skills. Use `context-engineering` to load the right spec sections and source files at each step rather than flooding the agent with the entire spec.
```

**翻译:**
```markdown
### 阶段 4：实现

一次执行一个任务，遵循 `incremental-implementation` 和 `test-driven-development` 技能。使用 `context-engineering` 在每个步骤加载正确的规格章节和源文件，而不是用整个规格淹没智能体。
```

**要点:**
- **为什么重要**: 这个阶段把控制权交给其他 skill。它明确声明了 spec-driven development 不是孤立的，而是与其他技能（增量实现、测试驱动开发、上下文工程）协同工作的流程的一部分。
- **隐含意义**: "而不是用整个规格淹没智能体" 是对 LLM 上下文管理的深刻洞察。Claude 的上下文窗口有限，一次性塞入整个规格会导致注意力分散。应该在每个步骤只加载相关的规格部分。
- **可执行建议**: 在实际使用中，这意味着每个任务开始时，应该显式引用规格中的相关部分（例如"根据规格 §4.2 代码风格，我们将..."），而不是假设 Claude 记得所有内容。

---

### 段落 13: Keeping the Spec Alive

**原文:**
```markdown
## Keeping the Spec Alive

The spec is a living document, not a one-time artifact:

- **Update when decisions change** — If you discover the data model needs to change, update the spec first, then implement.
- **Update when scope changes** — Features added or cut should be reflected in the spec.
- **Commit the spec** — The spec belongs in version control alongside the code.
- **Reference the spec in PRs** — Link back to the spec section that each PR implements.
```

**翻译:**
```markdown
## 保持规格的生命力

规格是一份活的文档，不是一次性的产物：

- **决策变更时更新** —— 如果你发现数据模型需要改变，先更新规格，再实现。
- **范围变更时更新** —— 增加或减少的功能应该在规格中得到反映。
- **将规格提交到版本控制** —— 规格属于版本控制，与代码并存。
- **在 PR 中引用规格** —— 链接回每个 PR 实现的规格章节。
```

**要点:**
- **为什么重要**: 这一段对抗了"规格写完后就被遗忘"的常见反模式。它明确声明规格有生命周期，必须与代码同步演化。
- **隐含意义**: "先更新规格，再实现"（update the spec first, then implement）是一个纪律要求。它防止了"代码已经改了，规格还是旧的"这种状态，这种状态会摧毁规格作为"共享真相源"的可信度。
- **可执行建议**: 在项目根目录创建一个 `specs/` 目录，将每个规格作为独立文件纳入版本控制。在 PR 模板中增加一个字段："相关规格："，强制要求开发者建立 PR 与规格之间的追溯关系。

---

### 段落 14: Common Rationalizations

**原文:**
```markdown
## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "This is simple, I don't need a spec" | Simple tasks don't need *long* specs, but they still need acceptance criteria. A two-line spec is fine. |
| "I'll write the spec after I code it" | That's documentation, not specification. The spec's value is in forcing clarity *before* code. |
| "The spec will slow us down" | A 15-minute spec prevents hours of rework. Waterfall in 15 minutes beats debugging in 15 hours. |
| "Requirements will change anyway" | That's why the spec is a living document. An outdated spec is still better than no spec. |
| "The user knows what they want" | Even clear requests have implicit assumptions. The spec surfaces those assumptions. |
```

**翻译:**
```markdown
## 常见借口

| 借口 | 现实 |
|---|---|
| "这很简单，我不需要规格" | 简单任务不需要*长篇*规格，但它们仍然需要验收标准。两行字的规格也可以。 |
| "我先写代码，之后再写规格" | 那是文档，不是规格。规格的价值在于在代码之前强制清晰。 |
| "规格会拖慢我们的速度" | 15 分钟的规格能避免数小时的返工。15 分钟的瀑布胜过 15 小时的调试。 |
| "需求反正会变" | 这就是为什么规格是活的文档。过时的规格仍然比没有规格好。 |
| "用户知道他们想要什么" | 即使清晰的请求也有隐含的假设。规格能暴露这些假设。 |
```

**要点:**
- **为什么重要**: 这是一个"心理防御"章节。它预见到人类开发者会找各种理由跳过规格，并提前准备好了反驳。这种设计非常聪明 —— 它不仅告诉你要写规格，还帮助你在面对抵触时坚持这个实践。
- **隐含意义**: "15 分钟的瀑布胜过 15 小时的调试"是一个强有力的修辞。它将"瀑布模型"这个通常带有负面含义的词汇重新定义为"快速对齐的工具"，而不是"沉重的流程"。
- **可执行建议**: 当团队有人（包括你自己）说"这次不需要规格"时，对照这个表格。即使规格只有两行验收标准，也比没有好。

---

### 段落 15: Red Flags

**原文:**
```markdown
## Red Flags

- Starting to write code without any written requirements
- Asking "should I just start building?" before clarifying what "done" means
- Implementing features not mentioned in any spec or task list
- Making architectural decisions without documenting them
- Skipping the spec because "it's obvious what to build"
```

**翻译:**
```markdown
## 危险信号

- 在没有任何书面需求的情况下开始写代码
- 在澄清"完成"意味着什么之前就询问"我应该直接开始构建吗？"
- 实现规格或任务列表中未提及的功能
- 在没有文档记录的情况下做出架构决策
- 因为"要构建什么很明显"而跳过规格
```

**要点:**
- **为什么重要**: 这些是**行为层面的预警信号**。如果你或你的团队出现这些行为，说明 spec-driven development 正在被破坏。它们比代码 smells 更严重，因为它们位于流程层面。
- **隐含意义**: "实现规格或任务列表中未提及的功能"（scope creep）被明确列为危险信号。这反映了 skill 对"范围纪律"（scope discipline）的重视 —— 不要因为你"觉得有用"就加功能。
- **可执行建议**: 将这段作为团队代码审查（code review）的检查清单。在审查 PR 时，不仅要审查代码质量，还要审查"这个 PR 实现了规格中的哪个部分？"

---

### 段落 16: Verification

**原文:**
```markdown
## Verification

Before proceeding to implementation, confirm:

- [ ] The spec covers all six core areas
- [ ] The human has reviewed and approved the spec
- [ ] Success criteria are specific and testable
- [ ] Boundaries (Always/Ask First/Never) are defined
- [ ] The spec is saved to a file in the repository
```

**翻译:**
```markdown
## 验证

在继续实现之前，确认：

- [ ] 规格涵盖全部六个核心区域
- [ ] 人工已审核并批准规格
- [ ] 成功标准是具体的且可测试的
- [ ] 边界（总是做/先询问/绝不做）已定义
- [ ] 规格已保存到仓库中的文件
```

**要点:**
- **为什么重要**: 这是门控工作流的最后一个检查点。它是一个强制性的 checklist，确保所有前置条件都已满足。这个 checklist 的存在使得"跳过规格"变得困难 —— 你必须主动勾选所有框。
- **隐含意义**: 最后一项 "The spec is saved to a file in the repository" 再次强调了规格的持久性。口头达成的共识不可靠，只有写下来的、纳入版本控制的规格才是可信赖的。
- **可执行建议**: 将此清单复制到项目的 PR 模板中，或作为每次任务启动前的标准步骤。不要仅仅在脑子里"确认"这些事项 —— 物理地勾选它们。

---

## Step 3: 整体总结

### 核心概念

| 概念 | 定义 |
|------|------|
| **Shared Source of Truth**（共享真相源） | 规格作为人类工程师和 AI 之间的共同参考点，消除双方对需求的理解偏差。 |
| **Gated Workflow**（门控工作流） | 四阶段流程（Specify → Plan → Tasks → Implement），每阶段必须经过人工审核才能进入下一阶段。 |
| **Assumption Surfacing**（假设暴露） | 在写规格之前先显式列出所有假设，因为假设是最危险的误解形式。 |
| **Success Criteria Reframing**（成功标准重述） | 将模糊的定性需求（如"更快"）转化为可量化的、可测试的具体指标。 |
| **Living Document**（活的文档） | 规格不是一次性的，而是与代码同步演化，决策变更时先更新规格再实现。 |
| **Boundaries**（边界） | 三层权限系统：Always（AI 自主决定）、Ask First（需协商）、Never（禁区）。 |

### 工作流程

```
开始
  │
  ▼
判断是否需要规格？（新功能？多文件？>30分钟？）
  │
  ├── 否 → 直接编码（单行修复、拼写更正等）
  │
  └── 是 → 进入门控工作流
            │
            ▼
      ┌─────────────┐
      │ 1. Specify  │ ← 暴露假设、写规格（6大区域）、获取人工批准
      └──────┬──────┘
             │
             ▼
      ┌─────────────┐
      │  2. Plan    │ ← 技术实现计划、组件依赖、风险识别
      └──────┬──────┘
             │
             ▼
      ┌─────────────┐
      │  3. Tasks   │ ← 拆分为小任务（单次会话、<5文件、有验收标准）
      └──────┬──────┘
             │
             ▼
      ┌─────────────┐
      │ 4. Implement│ ← 使用增量实现 + TDD + 上下文工程技能执行
      └─────────────┘
```

### 关键文件

| 文件 | 作用 |
|------|------|
| `skills/spec-driven-development/SKILL.md` | 本 skill 的定义文件，包含完整的四阶段工作流 |
| `docs/agent-skills/01-spec-driven-development-analysis.md` | 本分析文件，提供对 SKILL.md 的逐段精读和总结 |

### 与其他 Skill 的关系

- **前置/并发**: `idea-refine`（需求不明确时先精炼想法）
- **后置**: `planning-and-task-breakdown`（将规格转化为具体任务）
- **实现阶段协同**: `incremental-implementation`、`test-driven-development`、`context-engineering`

### 使用建议

1. **不要跳过 Step 0（假设暴露）** — 这是防止后续返工的最强防线。
2. **规格再短也比没有好** — 即使是两行字的验收标准也构成一份有效规格。
3. **把规格当作代码一样对待** — 纳入版本控制、在 PR 中引用、随代码同步更新。
4. **警惕"这很明显"陷阱** — 如果某事"很明显"，那么花 2 分钟把它写下来应该毫不费力；如果写下来很困难，说明它并不那么明显。
