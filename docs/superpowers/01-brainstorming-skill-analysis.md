---
name: Brainstorming Skill 深度分析
description: 对 skills/brainstorming/ 目录下所有文件的逐段精读、翻译与总结
type: analysis
---

# Brainstorming Skill 深度分析

## 文件清单

| 文件 | 类型 | 作用 |
|------|------|------|
| `SKILL.md` | 主定义文件 | Skill 的核心流程、检查清单、关键原则 |
| `visual-companion.md` | 子文档 | 浏览器可视化辅助工具的详细使用指南 |
| `spec-document-reviewer-prompt.md` | 模板文件 | 派发 spec 审查子 agent 的 prompt 模板 |
| `scripts/start-server.sh` | 启动脚本 | 启动 brainstorm 服务器 |
| `scripts/server.cjs` | 服务端 | HTTP + WebSocket 服务器实现 |
| `scripts/helper.js` | 客户端脚本 | 浏览器端的交互与事件上报 |
| `scripts/stop-server.sh` | 停止脚本 | 停止 brainstorm 服务器 |
| `scripts/frame-template.html` | 模板文件 | HTML 页面框架模板 |

---

## SKILL.md 逐段分析

### 段落 1: Frontmatter

**原文:**
```yaml
---
name: brainstorming
description: "You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation."
---
```

**翻译:**
```yaml
---
name: brainstorming
描述: "在进行任何创造性工作之前必须使用——包括创建功能、构建组件、添加功能或修改行为。在实施之前探索用户意图、需求和设计。"
---
```

**要点:**
- 这是 skill 的元数据，声明了 skill 的名称和触发条件
- 强调"任何创造性工作之前必须使用"，是一个强制性的前置步骤
- 目的：在实施前充分理解用户意图和需求

---

### 段落 2: 标题与核心目的

**原文:**
```markdown
# Brainstorming Ideas Into Designs

Help turn ideas into fully formed designs and specs through natural collaborative dialogue.
```

**翻译:**
```markdown
# 将想法 brainstorm 成设计

通过自然的协作对话，帮助将想法转化为完整的设计和规格说明。
```

**要点:**
- Skill 的核心目标：将模糊的想法转化为完整的设计和规格
- 方式：通过自然的协作对话（一问一答）

---

### 段落 3: 项目上下文理解与提问策略

**原文:**
```markdown
Start by understanding the current project context, then ask questions one at a time to refine the idea. Once you understand what you're building, present the design and get user approval.
```

**翻译:**
```markdown
首先理解当前项目的上下文，然后逐个问题地提炼想法。一旦理解了要构建的内容，就呈现设计并获取用户批准。
```

**要点:**
- 第一步：理解项目上下文（文件、文档、最近提交）
- 策略：一次只问一个问题（One question at a time）
- 终点：呈现设计并获取用户批准

---

### 段落 4: HARD-GATE（硬性门槛）

**原文:**
```markdown
<HARD-GATE>
Do NOT invoke any implementation skill, write any code, scaffold any project, or take any implementation action until you have presented a design and the user has approved it. This applies to EVERY project regardless of perceived simplicity.
</HARD-GATE>
```

**翻译:**
```markdown
<硬性门槛>
在呈现设计并获得用户批准之前，不得调用任何实现 skill、编写任何代码、搭建任何项目或采取任何实施行动。这适用于所有项目，无论其看起来多么简单。
</硬性门槛>
```

**要点:**
- 这是绝对红线：未经设计批准，禁止任何实现动作
- 适用于所有项目，没有例外（即使是"简单"的项目）
- 目的是防止未经验证的假设导致返工

---

### 段落 5: 语言要求

**原文:**
```markdown
<IMPORTANT>
    - You must use chinese to ask question
    - You must use chinese to write spec plan file
</IMPORTANT>
```

**翻译:**
```markdown
<重要>
    - 必须使用中文提问
    - 必须使用中文编写规格计划文件
</重要>
```

**要点:**
- 硬性语言约束：所有问题和 spec 文件必须使用中文
- 这是针对中文用户的定制化要求

---

### 段落 6: 反模式——"这太简单了不需要设计"

**原文:**
```markdown
## Anti-Pattern: "This Is Too Simple To Need A Design"

Every project goes through this process. A todo list, a single-function utility, a config change — all of them. "Simple" projects are where unexamined assumptions cause the most wasted work. The design can be short (a few sentences for truly simple projects), but you MUST present it and get approval.
```

**翻译:**
```markdown
## 反模式："这太简单了不需要设计"

每个项目都要经过这个流程。待办清单、单功能工具、配置变更——所有这些都是。"简单"的项目正是未经验证的假设造成最多无效工作的地方。设计可以很短（真正简单的项目只需几句话），但你必须呈现它并获得批准。
```

**要点:**
- 明确反对"太简单不需要设计"的心态
- 简单项目反而更容易因为假设错误而浪费工作
- 设计可以简短，但流程不能跳过

---

### 段落 7: 检查清单（Checklist）

**原文:**
```markdown
## Checklist

You MUST create a task for each of these items and complete them in order:

1. **Explore project context** — check files, docs, recent commits
2. **Offer visual companion** (if topic will involve visual questions) — this is its own message, not combined with a clarifying question. See the Visual Companion section below.
3. **Ask clarifying questions** — one at a time, understand purpose/constraints/success criteria
4. **Propose 2-3 approaches** — with trade-offs and your recommendation
5. **Present design** — in sections scaled to their complexity, get user approval after each section
6. **Write design doc** — save to `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` and commit
7. **Spec self-review** — quick inline check for placeholders, contradictions, ambiguity, scope (see below)
8. **User reviews written spec** — ask user to review the spec file before proceeding
9. **Transition to implementation** — invoke writing-plans skill to create implementation plan
```

**翻译:**
```markdown
## 检查清单

你必须为以下每个项目创建任务并按顺序完成：

1. **探索项目上下文** — 检查文件、文档、最近提交
2. **提供可视化辅助**（如果主题涉及视觉问题）— 这是独立的消息，不与澄清问题合并。详见下方的 Visual Companion 部分。
3. **提出澄清问题** — 一次一个，理解目的/约束/成功标准
4. **提出 2-3 种方案** — 附带权衡和你的推荐
5. **呈现设计** — 按复杂度分节呈现，每节后获取用户批准
6. **编写设计文档** — 保存到 `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` 并提交
7. **Spec 自检** — 快速内联检查占位符、矛盾、歧义、范围（见下文）
8. **用户审查书面 spec** — 要求用户在继续前审查 spec 文件
9. **过渡到实现** — 调用 writing-plans skill 创建实现计划
```

**要点:**
- 9 步流程，必须严格按顺序执行
- 第 2 步（visual companion）是可选的，取决于是否涉及视觉问题
- 第 6 步指定了固定的文件命名格式：`YYYY-MM-DD-<topic>-design.md`
- 第 9 步明确：brainstorming 的唯一出口是调用 `writing-plans` skill

---

### 段落 8: 流程图

**原文:**
DOT 流程图（略，详见原文件）

**翻译:**
流程图展示了从"探索项目上下文"到"调用 writing-plans skill"的完整流程，包含决策节点（如"用户批准设计？"）和循环（不批准则修订）。

**要点:**
- 流程图用 DOT 语言编写，可在支持 Graphviz 的工具中渲染
- 关键循环：设计不批准 → 修订 → 重新呈现
- 终端状态（双圆圈）：调用 writing-plans skill

---

### 段落 9: 终端状态声明

**原文:**
```markdown
**The terminal state is invoking writing-plans.** Do NOT invoke frontend-design, mcp-builder, or any other implementation skill. The ONLY skill you invoke after brainstorming is writing-plans.
```

**翻译:**
```markdown
**终端状态是调用 writing-plans。** 不要调用 frontend-design、mcp-builder 或任何其他实现 skill。brainstorming 之后唯一能调用的 skill 是 writing-plans。
```

**要点:**
- 再次强调：brainstorming → writing-plans 是唯一的合法路径
- 禁止直接跳到任何实现 skill

---

### 段落 10: 理解想法（Understanding the idea）

**原文:**
```markdown
## The Process

**Understanding the idea:**

- Check out the current project state first (files, docs, recent commits)
- Before asking detailed questions, assess scope: if the request describes multiple independent subsystems (e.g., "build a platform with chat, file storage, billing, and analytics"), flag this immediately. Don't spend questions refining details of a project that needs to be decomposed first.
- If the project is too large for a single spec, help the user decompose into sub-projects: what are the independent pieces, how do they relate, what order should they be built? Then brainstorm the first sub-project through the normal design flow. Each sub-project gets its own spec → plan → implementation cycle.
- For appropriately-scoped projects, ask questions one at a time to refine the idea
- Prefer multiple choice questions when possible, but open-ended is fine too
- Only one question per message - if a topic needs more exploration, break it into multiple questions
- Focus on understanding: purpose, constraints, success criteria
```

**翻译:**
```markdown
## 流程

**理解想法：**

- 首先检查当前项目状态（文件、文档、最近提交）
- 在问详细问题之前，评估范围：如果请求描述了多个独立的子系统（例如，"构建一个包含聊天、文件存储、计费和分析的平台"），立即标记出来。不要花时间提炼需要先分解的项目的细节。
- 如果项目太大无法放入单个 spec，帮助用户分解为子项目：有哪些独立的部分、它们如何关联、应该按什么顺序构建？然后通过正常的设计流程 brainstorm 第一个子项目。每个子项目都有自己的 spec → plan → implementation 周期。
- 对于范围合适的项目，一次一个问题地提炼想法
- 尽可能使用选择题，但开放式问题也可以
- 每条消息只问一个问题——如果某个话题需要更多探索，将其拆分为多个问题
- 聚焦于理解：目的、约束、成功标准
```

**要点:**
- 先评估项目范围，过大项目要先分解
- 分解后，每个子项目独立走完整流程（spec → plan → implementation）
- 提问策略：一次一个问题，优先选择题
- 核心关注点：purpose（目的）、constraints（约束）、success criteria（成功标准）

---

### 段落 11: 探索方案（Exploring approaches）

**原文:**
```markdown
**Exploring approaches:**

- Propose 2-3 different approaches with trade-offs
- Present options conversationally with your recommendation and reasoning
- Lead with your recommended option and explain why
```

**翻译:**
```markdown
**探索方案：**

- 提出 2-3 种不同方案，附带权衡分析
- 以对话方式呈现选项，包含你的推荐和理由
- 以你的推荐选项开头，并解释原因
```

**要点:**
- 必须提供多个方案（2-3 个），不能只有一个
- 每个方案都要有 trade-offs（权衡分析）
- 要明确表达自己的推荐和理由

---

### 段落 12: 呈现设计（Presenting the design）

**原文:**
```markdown
**Presenting the design:**

- Once you believe you understand what you're building, present the design
- Scale each section to its complexity: a few sentences if straightforward, up to 200-300 words if nuanced
- Ask after each section whether it looks right so far
- Cover: architecture, components, data flow, error handling, testing
- Be ready to go back and clarify if something doesn't make sense
```

**翻译:**
```markdown
**呈现设计：**

- 一旦确信理解了要构建的内容，就呈现设计
- 每个部分的详略程度与其复杂度匹配：简单的几句话，复杂的 200-300 词
- 每呈现一部分后询问用户是否看起来正确
- 覆盖：架构、组件、数据流、错误处理、测试
- 如果某些内容不合理，准备好回溯和澄清
```

**要点:**
- 分节呈现，每节后验证
- 设计内容五要素：架构、组件、数据流、错误处理、测试
- 灵活的详略策略：根据复杂度调整

---

### 段落 13: 设计的隔离性与清晰性

**原文:**
```markdown
**Design for isolation and clarity:**

- Break the system into smaller units that each have one clear purpose, communicate through well-defined interfaces, and can be understood and tested independently
- For each unit, you should be able to answer: what does it do, how do you use it, and what does it depend on?
- Can someone understand what a unit does without reading its internals? Can you change the internals without breaking consumers? If not, the boundaries need work.
- Smaller, well-bounded units are also easier for you to work with - you reason better about code you can hold in context at once, and your edits are more reliable when files are focused. When a file grows large, that's often a signal that it's doing too much.
```

**翻译:**
```markdown
**为隔离性和清晰性而设计：**

- 将系统分解为更小的单元，每个单元有一个明确的目的，通过定义良好的接口通信，并能独立理解和测试
- 对于每个单元，你应该能回答：它做什么、如何使用它、它依赖什么？
- 有人能在不阅读内部实现的情况下理解一个单元的功能吗？你能在不破坏消费者的情况下改变内部实现吗？如果不能，边界需要调整。
- 更小、边界清晰的单元也更容易让你处理——你能更好地推理一次能放入上下文的代码，当文件聚焦时你的编辑更可靠。当文件变大时，这通常是它做得太多的信号。
```

**要点:**
- 核心设计原则：高内聚、低耦合
- 每个模块必须能回答三个问题：做什么、怎么用、依赖什么
- 信息隐藏：消费者不应需要了解内部实现
- 文件大小是信号：过大的文件意味着职责过重

---

### 段落 14: 在现有代码库中工作

**原文:**
```markdown
**Working in existing codebases:**

- Explore the current structure before proposing changes. Follow existing patterns.
- Where existing code has problems that affect the work (e.g., a file that's grown too large, unclear boundaries, tangled responsibilities), include targeted improvements as part of the design - the way a good developer improves code they're working in.
- Don't propose unrelated refactoring. Stay focused on what serves the current goal.
```

**翻译:**
```markdown
**在现有代码库中工作：**

- 在提出变更前先探索现有结构。遵循现有模式。
- 如果现有代码存在影响工作的问题（例如文件过大、边界不清、职责纠缠），将针对性改进作为设计的一部分——就像优秀开发者在工作中改进代码一样。
- 不要提议无关的重构。专注于服务当前目标的事情。
```

**要点:**
- 先理解现有结构和模式
- 可以包含针对性改进，但仅限于与当前工作相关的部分
- 禁止无关的重构（避免范围蔓延）

---

### 段落 15: 设计之后的文档

**原文:**
```markdown
## After the Design

**Documentation:**

- Write the validated design (spec) to `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`
  - (User preferences for spec location override this default)
- Use elements-of-style:writing-clearly-and-concisely skill if available
- Commit the design document to git
```

**翻译:**
```markdown
## 设计之后

**文档：**

- 将验证过的设计（spec）写入 `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`
  - （用户对 spec 位置的偏好覆盖此默认值）
- 如果可用，使用 elements-of-style:writing-clearly-and-concisely skill
- 将设计文档提交到 git
```

**要点:**
- Spec 文件固定命名格式：`YYYY-MM-DD-<topic>-design.md`
- 默认路径：`docs/superpowers/specs/`
- 必须提交到 git（不是只写在本地）

---

### 段落 16: Spec 自检（Spec Self-Review）

**原文:**
```markdown
**Spec Self-Review:**
After writing the spec document, look at it with fresh eyes:

1. **Placeholder scan:** Any "TBD", "TODO", incomplete sections, or vague requirements? Fix them.
2. **Internal consistency:** Do any sections contradict each other? Does the architecture match the feature descriptions?
3. **Scope check:** Is this focused enough for a single implementation plan, or does it need decomposition?
4. **Ambiguity check:** Could any requirement be interpreted two different ways? If so, pick one and make it explicit.

Fix any issues inline. No need to re-review — just fix and move on.
```

**翻译:**
```markdown
**Spec 自检：**
编写 spec 文档后，用新鲜的眼光审视它：

1. **占位符扫描：** 有任何"TBD"、"TODO"、不完整的部分或模糊的需求吗？修复它们。
2. **内部一致性：** 各部分之间是否存在矛盾？架构是否与功能描述匹配？
3. **范围检查：** 这是否足够聚焦以放入单个实现计划，还是需要分解？
4. **歧义检查：** 任何需求是否可能被两种不同方式解读？如果是，选择一种并明确说明。

内联修复任何问题。无需重新审查——修复并继续即可。
```

**要点:**
- 自检四步：占位符扫描、一致性检查、范围检查、歧义检查
- 发现问题直接修复，不需要再次完整审查
- 目的是确保 spec 足够清晰，可以作为实现计划的输入

---

### 段落 17: 用户审查门槛（User Review Gate）

**原文:**
```markdown
**User Review Gate:**
After the spec review loop passes, ask the user to review the written spec before proceeding:

> "Spec written and committed to `<path>`. Please review it and let me know if you want to make any changes before we start writing out the implementation plan."

Wait for the user's response. If they request changes, make them and re-run the spec review loop. Only proceed once the user approves.
```

**翻译:**
```markdown
**用户审查门槛：**
spec 审查循环通过后，要求用户在继续前审查书面 spec：

> "Spec 已编写并提交到 `<path>`。请审查它，并告诉我是否需要在开始编写实现计划之前进行任何更改。"

等待用户回复。如果他们请求更改，进行更改并重新运行 spec 审查循环。仅在用户批准后继续。
```

**要点:**
- 明确的用户审查门槛，不能跳过
- 用户批准前不得进入实现阶段
- 如果需要修改，修改后重新自检，再次提交用户审查

---

### 段落 18: 实现过渡

**原文:**
```markdown
**Implementation:**

- Invoke the writing-plans skill to create a detailed implementation plan
- Do NOT invoke any other skill. writing-plans is the next step.
```

**翻译:**
```markdown
**实现：**

- 调用 writing-plans skill 创建详细的实现计划
- 不要调用任何其他 skill。writing-plans 是下一步。
```

**要点:**
- 再次强调：writing-plans 是唯一的下一步
- 实现计划的创建被委托给专门的 skill

---

### 段落 19: 关键原则

**原文:**
```markdown
## Key Principles

- **One question at a time** - Don't overwhelm with multiple questions
- **Multiple choice preferred** - Easier to answer than open-ended when possible
- **YAGNI ruthlessly** - Remove unnecessary features from all designs
- **Explore alternatives** - Always propose 2-3 approaches before settling
- **Incremental validation** - Present design, get approval before moving on
- **Be flexible** - Go back and clarify when something doesn't make sense
```

**翻译:**
```markdown
## 关键原则

- **一次一个问题** - 不要用多个问题压垮用户
- **优先选择题** - 可能时，选择题比开放式问题更容易回答
- **无情地 YAGNI** - 从所有设计中移除不必要的功能
- **探索替代方案** - 在确定前总是提出 2-3 种方案
- **增量验证** - 呈现设计，在继续前获取批准
- **保持灵活** - 当某些内容不合理时，回溯并澄清
```

**要点:**
- YAGNI（You Aren't Gonna Need It）：核心原则，防止过度设计
- 增量验证：每步都需用户确认，避免方向性错误
- 灵活性：设计是迭代过程，允许回溯

---

### 段落 20: Visual Companion 概述

**原文:**
```markdown
## Visual Companion

A browser-based companion for showing mockups, diagrams, and visual options during brainstorming. Available as a tool — not a mode. Accepting the companion means it's available for questions that benefit from visual treatment; it does NOT mean every question goes through the browser.
```

**翻译:**
```markdown
## 可视化辅助工具

一个基于浏览器的辅助工具，用于在 brainstorm 期间展示原型、图表和视觉选项。作为工具提供——而非模式。接受该辅助工具意味着它可用于受益于视觉处理的问题；并不意味着每个问题都通过浏览器进行。
```

**要点:**
- Visual Companion 是一个可选工具，不是必需模式
- 只在需要视觉辅助的问题中使用
- 接受不代表所有问题都用浏览器

---

### 段落 21: 提供 Visual Companion

**原文:**
```markdown
**Offering the companion:** When you anticipate that upcoming questions will involve visual content (mockups, layouts, diagrams), offer it once for consent:
> "Some of what we're working on might be easier to explain if I can show it to you in a web browser. I can put together mockups, diagrams, comparisons, and other visuals as we go. This feature is still new and can be token-intensive. Want to try it? (Requires opening a local URL)"

**This offer MUST be its own message.** Do not combine it with clarifying questions, context summaries, or any other content. The message should contain ONLY the offer above and nothing else. Wait for the user's response before continuing. If they decline, proceed with text-only brainstorming.
```

**翻译:**
```markdown
**提供辅助工具：** 当你预期接下来的问题将涉及视觉内容（原型、布局、图表）时，一次性征求用户同意：
> "如果我们正在做的某些内容我可以在网页浏览器中展示给你，可能会更容易解释。我可以随时整理原型、图表、对比和其他视觉内容。这个功能还比较新，可能会消耗较多 token。想试试吗？（需要打开本地 URL）"

**这个提议必须是独立的消息。** 不要将它与澄清问题、上下文总结或任何其他内容合并。消息应该只包含上面的提议，其他什么都没有。等待用户回复后再继续。如果他们拒绝，继续仅使用文本的 brainstorm。
```

**要点:**
- 提供辅助工具的提议必须是独立消息
- 用户同意后，逐问题决定是否使用浏览器
- 用户拒绝后，完全使用文本 brainstorm

---

### 段落 22: 逐问题决策

**原文:**
```markdown
**Per-question decision:** Even after the user accepts, decide FOR EACH QUESTION whether to use the browser or the terminal. The test: **would the user understand this better by seeing it than reading it?**

- **Use the browser** for content that IS visual — mockups, wireframes, layout comparisons, architecture diagrams, side-by-side visual designs
- **Use the terminal** for content that is text — requirements questions, conceptual choices, tradeoff lists, A/B/C/D text options, scope decisions

A question about a UI topic is not automatically a visual question. "What does personality mean in this context?" is a conceptual question — use the terminal. "Which wizard layout works better?" is a visual question — use the browser.

If they agree to the companion, read the detailed guide before proceeding:
`skills/brainstorming/visual-companion.md`
```

**翻译:**
```markdown
**逐问题决策：** 即使用户接受了，对每个问题都要决定使用浏览器还是终端。测试标准是：**用户通过看到它是否比阅读它更容易理解？**

- **使用浏览器** 处理视觉内容——原型、线框图、布局对比、架构图、并排视觉设计
- **使用终端** 处理文本内容——需求问题、概念选择、权衡列表、A/B/C/D 文本选项、范围决策

关于 UI 话题的问题不一定是视觉问题。"在这个上下文中 personality 是什么意思？"是概念问题——使用终端。"哪种向导布局更好？"是视觉问题——使用浏览器。

如果他们同意使用辅助工具，在继续前阅读详细指南：
`skills/brainstorming/visual-companion.md`
```

**要点:**
- 核心决策标准：视觉内容用浏览器，文本内容用终端
- 关键区分：关于 UI 的话题 ≠ 视觉问题
- 同意后需要阅读 `visual-companion.md` 获取详细指南

---

## visual-companion.md 逐段分析

### 段落 1: 标题与概述

**原文:**
```markdown
# Visual Companion Guide

Browser-based visual brainstorming companion for showing mockups, diagrams, and options.
```

**翻译:**
```markdown
# 可视化辅助工具指南

基于浏览器的可视化 brainstorm 辅助工具，用于展示原型、图表和选项。
```

**要点:**
- 这是 Visual Companion 的详细使用手册
- 用途：展示原型、图表、选项

---

### 段落 2: 何时使用

**原文:**
```markdown
## When to Use

Decide per-question, not per-session. The test: **would the user understand this better by seeing it than reading it?**

**Use the browser** when the content itself is visual:

- **UI mockups** — wireframes, layouts, navigation structures, component designs
- **Architecture diagrams** — system components, data flow, relationship maps
- **Side-by-side visual comparisons** — comparing two layouts, two color schemes, two design directions
- **Design polish** — when the question is about look and feel, spacing, visual hierarchy
- **Spatial relationships** — state machines, flowcharts, entity relationships rendered as diagrams

**Use the terminal** when the content is text or tabular:

- **Requirements and scope questions** — "what does X mean?", "which features are in scope?"
- **Conceptual A/B/C choices** — picking between approaches described in words
- **Tradeoff lists** — pros/cons, comparison tables
- **Technical decisions** — API design, data modeling, architectural approach selection
- **Clarifying questions** — anything where the answer is words, not a visual preference

A question *about* a UI topic is not automatically a visual question. "What kind of wizard do you want?" is conceptual — use the terminal. "Which of these wizard layouts feels right?" is visual — use the browser.
```

**翻译:**
```markdown
## 何时使用

按问题决定，不是按会话决定。测试标准：**用户通过看到它是否比阅读它更容易理解？**

**使用浏览器** 当内容本身是视觉性的：

- **UI 原型** — 线框图、布局、导航结构、组件设计
- **架构图** — 系统组件、数据流、关系图
- **并排视觉对比** — 对比两种布局、两种配色方案、两种设计方向
- **设计打磨** — 当问题是关于外观和感觉、间距、视觉层次时
- **空间关系** — 状态机、流程图、实体关系图

**使用终端** 当内容是文本或表格时：

- **需求和范围问题** — "X 是什么意思？"、"哪些功能在范围内？"
- **概念性 A/B/C 选择** — 在文字描述的方案之间选择
- **权衡列表** — 优缺点、对比表
- **技术决策** — API 设计、数据建模、架构方法选择
- **澄清问题** — 任何答案是文字而非视觉偏好的问题

关于 UI 话题的问题不一定是视觉问题。"你想要什么样的向导？"是概念性的——使用终端。"哪种向导布局感觉更好？"是视觉性的——使用浏览器。
```

**要点:**
- 按问题粒度决策，不是一揽子决定
- 5 类视觉内容用浏览器，5 类文本内容用终端
- 关键区分线：概念性 vs 视觉性

---

### 段落 3: 工作原理

**原文:**
```markdown
## How It Works

The server watches a directory for HTML files and serves the newest one to the browser. You write HTML content to `screen_dir`, the user sees it in their browser and can click to select options. Selections are recorded to `state_dir/events` that you read on your next turn.

**Content fragments vs full documents:** If your HTML file starts with `<!DOCTYPE` or `<html`, the server serves it as-is (just injects the helper script). Otherwise, the server automatically wraps your content in the frame template — adding the header, CSS theme, selection indicator, and all interactive infrastructure. **Write content fragments by default.** Only write full documents when you need complete control over the page.
```

**翻译:**
```markdown
## 工作原理

服务器监视一个目录中的 HTML 文件，将最新的一个提供给浏览器。你将 HTML 内容写入 `screen_dir`，用户在浏览器中看到它并可以点击选择选项。选择被记录到 `state_dir/events` 中，你在下一轮读取。

**内容片段 vs 完整文档：** 如果你的 HTML 文件以 `<!DOCTYPE` 或 `<html` 开头，服务器按原样提供（只注入 helper 脚本）。否则，服务器自动将你的内容包装在框架模板中——添加标题、CSS 主题、选择指示器和所有交互基础设施。**默认写内容片段。** 只有在你需要完全控制页面时才写完整文档。
```

**要点:**
- 核心机制：监控目录 → 服务最新 HTML → 用户点击 → 事件记录到文件
- 默认写内容片段（fragment），服务器自动包装
- 只有需要完全控制时才写完整 HTML 文档

---

### 段落 4: 启动会话

**原文:**
```markdown
## Starting a Session

```bash
# Start server with persistence (mockups saved to project)
scripts/start-server.sh --project-dir /path/to/project

# Returns: {"type":"server-started","port":52341,"url":"http://localhost:52341",
#           "screen_dir":"/path/to/project/.superpowers/brainstorm/12345-1706000000/content",
#           "state_dir":"/path/to/project/.superpowers/brainstorm/12345-1706000000/state"}
```

Save `screen_dir` and `state_dir` from the response. Tell user to open the URL.

**Finding connection info:** The server writes its startup JSON to `$STATE_DIR/server-info`. If you launched the server in the background and didn't capture stdout, read that file to get the URL and port. When using `--project-dir`, check `<project>/.superpowers/brainstorm/` for the session directory.

**Note:** Pass the project根目录 as `--project-dir` so mockups persist in `.superpowers/brainstorm/` and survive server restarts. Without it, files go to `/tmp` and get cleaned up. Remind the user to add `.superpowers/` to `.gitignore` if it's not already there.
```

**翻译:**
```markdown
## 启动会话

```bash
# 启动服务器并持久化（原型保存到项目）
scripts/start-server.sh --project-dir /path/to/project

# 返回：{"type":"server-started","port":52341,"url":"http://localhost:52341",
#           "screen_dir":"/path/to/project/.superpowers/brainstorm/12345-1706000000/content",
#           "state_dir":"/path/to/project/.superpowers/brainstorm/12345-1706000000/state"}
```

从响应中保存 `screen_dir` 和 `state_dir`。告诉用户打开 URL。

**查找连接信息：** 服务器将启动 JSON 写入 `$STATE_DIR/server-info`。如果你在后台启动了服务器且没有捕获 stdout，读取该文件获取 URL 和端口。使用 `--project-dir` 时，在 `<project>/.superpowers/brainstorm/` 中检查会话目录。

**注意：** 将项目根目录作为 `--project-dir` 传入，这样原型会持久化在 `.superpowers/brainstorm/` 中并在服务器重启后保留。不传入的话，文件会放到 `/tmp` 并被清理。提醒用户将 `.superpowers/` 添加到 `.gitignore`（如果还没有的话）。
```

**要点:**
- 启动命令：`start-server.sh --project-dir <path>`
- 必须保存返回的 `screen_dir`（写 HTML）和 `state_dir`（读事件）
- 使用 `--project-dir` 让文件持久化，否则放在 `/tmp` 会被清理
- 需要提醒用户将 `.superpowers/` 加入 `.gitignore`

---

### 段落 5: 多平台启动方式

**原文:**
```markdown
**Launching the server by platform:**

**Claude Code (macOS / Linux):**
```bash
# Default mode works — the script backgrounds the server itself
scripts/start-server.sh --project-dir /path/to/project
```

**Claude Code (Windows):**
```bash
# Windows auto-detects and uses foreground mode, which blocks the tool call.
# Use run_in_background: true on the Bash tool call so the server survives
# across conversation turns.
scripts/start-server.sh --project-dir /path/to/project
```
When calling this via the Bash tool, set `run_in_background: true`. Then read `$STATE_DIR/server-info` on the next turn to get the URL and port.

**Codex:**
```bash
# Codex reaps background processes. The script auto-detects CODEX_CI and
# switches to foreground mode. Run it normally — no extra flags needed.
scripts/start-server.sh --project-dir /path/to/project
```

**Gemini CLI:**
```bash
# Use --foreground and set is_background: true on your shell tool call
# so the process survives across turns
scripts/start-server.sh --project-dir /path/to/project --foreground
```

**Other environments:** The server must keep running in the background across conversation turns. If your environment reaps detached processes, use `--foreground` and launch the command with your platform's background execution mechanism.

If the URL is unreachable from your browser (common in remote/containerized setups), bind a non-loopback host:

```bash
scripts/start-server.sh \
  --project-dir /path/to/project \
  --host 0.0.0.0 \
  --url-host localhost
```

Use `--url-host` to control what hostname is printed in the returned URL JSON.
```

**翻译:**
```markdown
**按平台启动服务器：**

**Claude Code (macOS / Linux):**
```bash
# 默认模式工作——脚本自动将服务器放到后台
scripts/start-server.sh --project-dir /path/to/project
```

**Claude Code (Windows):**
```bash
# Windows 自动检测并使用前台模式，这会阻塞工具调用。
# 在 Bash 工具调用上设置 run_in_background: true，这样服务器能跨会话轮次存活
scripts/start-server.sh --project-dir /path/to/project
```
通过 Bash 工具调用时，设置 `run_in_background: true`。然后在下一轮读取 `$STATE_DIR/server-info` 获取 URL 和端口。

**Codex:**
```bash
# Codex 会收割后台进程。脚本自动检测 CODEX_CI 并切换到前台模式。
# 正常运行即可——不需要额外标志
scripts/start-server.sh --project-dir /path/to/project
```

**Gemini CLI:**
```bash
# 使用 --foreground 并在 shell 工具调用上设置 is_background: true
# 这样进程能跨轮次存活
scripts/start-server.sh --project-dir /path/to/project --foreground
```

**其他环境：** 服务器必须在后台跨会话轮次持续运行。如果你的环境会收割分离的进程，使用 `--foreground` 并通过你平台的后台执行机制启动命令。

如果 URL 无法从浏览器访问（在远程/容器化环境中常见），绑定非回环主机：

```bash
scripts/start-server.sh \
  --project-dir /path/to/project \
  --host 0.0.0.0 \
  --url-host localhost
```

使用 `--url-host` 控制返回的 URL JSON 中打印的主机名。
```

**要点:**
- 不同平台/环境需要不同的启动方式
- 核心挑战：后台进程被"收割"（reap）的问题
- macOS/Linux：默认后台；Windows/Codex：自动前台；Gemini：显式前台 + 背景标志
- 远程环境需要 `--host 0.0.0.0` + `--url-host localhost`

---

### 段落 6: 工作流程循环（The Loop）

**原文:**
```markdown
## The Loop

1. **Check server is alive**, then **write HTML** to a new file in `screen_dir`:
   - Before each write, check that `$STATE_DIR/server-info` exists. If it doesn't (or `$STATE_DIR/server-stopped` exists), the server has shut down — restart it with `start-server.sh` before continuing. The server auto-exits after 30 minutes of inactivity.
   - Use semantic filenames: `platform.html`, `visual-style.html`, `layout.html`
   - **Never reuse filenames** — each screen gets a fresh file
   - Use Write tool — **never use cat/heredoc** (dumps noise into terminal)
   - Server automatically serves the newest file

2. **Tell user what to expect and end your turn:**
   - Remind them of the URL (every step, not just first)
   - Give a brief text summary of what's on screen (e.g., "Showing 3 layout options for the homepage")
   - Ask them to respond in the terminal: "Take a look and let me know what you think. Click to select an option if you'd like."

3. **On your next turn** — after the user responds in the terminal:
   - Read `$STATE_DIR/events` if it exists — this contains the user's browser interactions (clicks, selections) as JSON lines
   - Merge with the user's terminal text to get the full picture
   - The terminal message is the primary feedback; `state_dir/events` provides structured interaction data

4. **Iterate or advance** — if feedback changes current screen, write a new file (e.g., `layout-v2.html`). Only move to the next question when the current step is validated.

5. **Unload when returning to terminal** — when the next step doesn't need the browser（例如，a clarifying question, a tradeoff discussion），push a waiting screen to clear the stale content:

   ```html
   <!-- filename: waiting.html (or waiting-2.html, etc.) -->
   <div style="display:flex;align-items:center;justify-content:center;min-height:60vh">
     <p class="subtitle">Continuing in terminal...</p>
   </div>
   ```

   This prevents the user from staring at a resolved choice while the conversation has moved on. When the next visual question comes up, push a new content file as usual.

6. Repeat until done.
```

**翻译:**
```markdown
## 工作流程循环

1. **检查服务器是否存活**，然后向 `screen_dir` 中的新文件**写入 HTML**：
   - 每次写入前，检查 `$STATE_DIR/server-info` 是否存在。如果不存在（或 `$STATE_DIR/server-stopped` 存在），服务器已关闭——用 `start-server.sh` 重启后再继续。服务器在 30 分钟不活动后自动退出。
   - 使用语义化文件名：`platform.html`、`visual-style.html`、`layout.html`
   - **永远不要复用文件名**——每个屏幕都使用新文件
   - 使用 Write 工具——**不要用 cat/heredoc**（会在终端产生噪音）
   - 服务器自动提供最新的文件

2. **告诉用户期待什么并结束你的回合：**
   - 提醒他们 URL（每一步，不只是第一步）
   - 简要文本总结屏幕上显示的内容（例如，"展示首页的 3 种布局选项"）
   - 要求他们在终端回复："看一看，告诉我你的想法。如果想的话可以点击选择一个选项。"

3. **在你的下一轮**——用户在终端回复后：
   - 如果存在，读取 `$STATE_DIR/events`——这包含用户的浏览器交互（点击、选择），以 JSON 行格式
   - 与用户的终端文本合并以获得完整图景
   - 终端消息是主要反馈；`state_dir/events` 提供结构化的交互数据

4. **迭代或推进**——如果反馈改变了当前屏幕，写一个新文件（例如 `layout-v2.html`）。仅在当前步骤验证后才进入下一个问题。

5. **返回终端时卸载**——当下一步不需要浏览器时（例如，澄清问题、权衡讨论），推送等待屏幕以清除过时内容：

   ```html
   <!-- 文件名：waiting.html（或 waiting-2.html 等） -->
   <div style="display:flex;align-items:center;justify-content:center;min-height:60vh">
     <p class="subtitle">Continuing in terminal...</p>
   </div>
   ```

   这防止用户在对话已经推进时还盯着一个已解决的选择。当下一个视觉问题出现时，像往常一样推送新内容文件。

6. 重复直到完成。
```

**要点:**
- 6 步循环：检查 → 写 HTML → 告知用户 → 读取事件 → 迭代/推进 → 返回终端时卸载
- 关键规则：永不复用文件名、使用 Write 工具、每次提醒 URL
- 30 分钟空闲自动关闭，需要检查存活状态
- 终端消息是主要反馈，events 文件是辅助数据

---

### 段落 7: 编写内容片段

**原文:**
```markdown
## Writing Content Fragments

Write just the content that goes inside the page. The server wraps it in the frame template automatically (header, theme CSS, selection indicator, and all interactive infrastructure).

**Minimal example:**

```html
<h2>Which layout works better?</h2>
<p class="subtitle">Consider readability and visual hierarchy</p>

<div class="options">
  <div class="option" data-choice="a" onclick="toggleSelect(this)">
    <div class="letter">A</div>
    <div class="content">
      <h3>Single Column</h3>
      <p>Clean, focused reading experience</p>
    </div>
  </div>
  <div class="option" data-choice="b" onclick="toggleSelect(this)">
    <div class="letter">B</div>
    <div class="content">
      <h3>Two Column</h3>
      <p>Sidebar navigation with main content</p>
    </div>
  </div>
</div>
```

That's it. No `<html>`, no CSS, no `<script>` tags needed. The server provides all of that.
```

**翻译:**
```markdown
## 编写内容片段

只写页面内部的内容。服务器自动将其包装在框架模板中（标题、主题 CSS、选择指示器和所有交互基础设施）。

**最小示例：**

```html
<h2>哪种布局更好？</h2>
<p class="subtitle">考虑可读性和视觉层次</p>

<div class="options">
  <div class="option" data-choice="a" onclick="toggleSelect(this)">
    <div class="letter">A</div>
    <div class="content">
      <h3>单列</h3>
      <p>干净、专注的阅读体验</p>
    </div>
  </div>
  <div class="option" data-choice="b" onclick="toggleSelect(this)">
    <div class="letter">B</div>
    <div class="content">
      <h3>双列</h3>
      <p>侧边导航与主内容</p>
    </div>
  </div>
</div>
```

就这些。不需要 `<html>`、CSS、`<script>` 标签。服务器提供所有这些东西。
```

**要点:**
- 默认写内容片段，不需要完整 HTML 结构
- 使用预定义的 CSS 类和 JavaScript 函数（如 `toggleSelect`）
- 服务器负责注入框架模板和 helper 脚本

---

### 段落 8: 可用的 CSS 类

**原文:**
```markdown
## CSS Classes Available

The frame template provides these CSS classes for your content:

### Options (A/B/C choices)

```html
<div class="options">
  <div class="option" data-choice="a" onclick="toggleSelect(this)">
    <div class="letter">A</div>
    <div class="content">
      <h3>Title</h3>
      <p>Description</p>
    </div>
  </div>
</div>
```

**Multi-select:** Add `data-multiselect` to the container to let users select multiple options. Each click toggles the item. The indicator bar shows the count.

```html
<div class="options" data-multiselect>
  <!-- same option markup — users can select/deselect multiple -->
</div>
```

### Cards (visual designs)

```html
<div class="cards">
  <div class="card" data-choice="design1" onclick="toggleSelect(this)">
    <div class="card-image"><!-- mockup content --></div>
    <div class="card-body">
      <h3>Name</h3>
      <p>Description</p>
    </div>
  </div>
</div>
```

### Mockup container

```html
<div class="mockup">
  <div class="mockup-header">Preview: Dashboard Layout</div>
  <div class="mockup-body"><!-- your mockup HTML --></div>
</div>
```

### Split view (side-by-side)

```html
<div class="split">
  <div class="mockup"><!-- left --></div>
  <div class="mockup"><!-- right --></div>
</div>
```

### Pros/Cons

```html
<div class="pros-cons">
  <div class="pros"><h4>Pros</h4><ul><li>Benefit</li></ul></div>
  <div class="cons"><h4>Cons</h4><ul><li>Drawback</li></ul></div>
</div>
```

### Mock elements (wireframe building blocks)

```html
<div class="mock-nav">Logo | Home | About | Contact</div>
<div style="display: flex;">
  <div class="mock-sidebar">Navigation</div>
  <div class="mock-content">Main content area</div>
</div>
<button class="mock-button">Action Button</button>
<input class="mock-input" placeholder="Input field">
<div class="placeholder">Placeholder area</div>
```

### Typography and sections

- `h2` — page title
- `h3` — section heading
- `.subtitle` — secondary text below title
- `.section` — content block with bottom margin
- `.label` — small uppercase label text
```

**翻译:**
```markdown
## 可用的 CSS 类

框架模板为你的内容提供以下 CSS 类：

### 选项（A/B/C 选择）

```html
<div class="options">
  <div class="option" data-choice="a" onclick="toggleSelect(this)">
    <div class="letter">A</div>
    <div class="content">
      <h3>标题</h3>
      <p>描述</p>
    </div>
  </div>
</div>
```

**多选：** 向容器添加 `data-multiselect` 让用户选择多个选项。每次点击切换项目。指示器栏显示数量。

```html
<div class="options" data-multiselect>
  <!-- 相同的选项标记——用户可以选择/取消多个 -->
</div>
```

### 卡片（视觉设计）

```html
<div class="cards">
  <div class="card" data-choice="design1" onclick="toggleSelect(this)">
    <div class="card-image"><!-- 原型内容 --></div>
    <div class="card-body">
      <h3>名称</h3>
      <p>描述</p>
    </div>
  </div>
</div>
```

### 原型容器

```html
<div class="mockup">
  <div class="mockup-header">预览：仪表板布局</div>
  <div class="mockup-body"><!-- 你的原型 HTML --></div>
</div>
```

### 分栏视图（并排）

```html
<div class="split">
  <div class="mockup"><!-- 左侧 --></div>
  <div class="mockup"><!-- 右侧 --></div>
</div>
```

### 优缺点

```html
<div class="pros-cons">
  <div class="pros"><h4>优点</h4><ul><li>好处</li></ul></div>
  <div class="cons"><h4>缺点</h4><ul><li>坏处</li></ul></div>
</div>
```

### 模拟元素（线框构建块）

```html
<div class="mock-nav">Logo | Home | About | Contact</div>
<div style="display: flex;">
  <div class="mock-sidebar">导航</div>
  <div class="mock-content">主内容区域</div>
</div>
<button class="mock-button">操作按钮</button>
<input class="mock-input" placeholder="输入字段">
<div class="placeholder">占位区域</div>
```

### 排版和分区

- `h2` — 页面标题
- `h3` — 分区标题
- `.subtitle` — 标题下方的次要文本
- `.section` — 带底部边距的内容块
- `.label` — 小型大写标签文本
```

**要点:**
- 提供 6 类 UI 组件：options、cards、mockup、split、pros-cons、mock-elements
- 支持单选和多选（`data-multiselect`）
- 线框元素（mock-nav、mock-sidebar 等）适合快速原型
- 排版类（h2、h3、subtitle、section、label）定义视觉层次

---

### 段落 9: 浏览器事件格式

**原文:**
```markdown
## Browser Events Format

When the user clicks options in the browser, their interactions are recorded to `$STATE_DIR/events` (one JSON object per line). The file is cleared automatically when you push a new screen.

```jsonl
{"type":"click","choice":"a","text":"Option A - Simple Layout","timestamp":1706000101}
{"type":"click","choice":"c","text":"Option C - Complex Grid","timestamp":1706000108}
{"type":"click","choice":"b","text":"Option B - Hybrid","timestamp":1706000115}
```

The full event stream shows the user's exploration path — they may click multiple options before settling. The last `choice` event is typically the final selection, but the pattern of clicks can reveal hesitation or preferences worth asking about.

If `$STATE_DIR/events` doesn't exist, the user didn't interact with the browser — use only their terminal text.
```

**翻译:**
```markdown
## 浏览器事件格式

当用户在浏览器中点击选项时，他们的交互被记录到 `$STATE_DIR/events`（每行一个 JSON 对象）。推送新屏幕时文件自动清除。

```jsonl
{"type":"click","choice":"a","text":"Option A - Simple Layout","timestamp":1706000101}
{"type":"click","choice":"c","text":"Option C - Complex Grid","timestamp":1706000108}
{"type":"click","choice":"b","text":"Option B - Hybrid","timestamp":1706000115}
```

完整的事件流显示用户的探索路径——他们可能在确定前点击多个选项。最后一个 `choice` 事件通常是最终选择，但点击模式可以揭示犹豫或值得询问的偏好。

如果 `$STATE_DIR/events` 不存在，用户没有与浏览器交互——仅使用他们的终端文本。
```

**要点:**
- 事件格式：JSON Lines（每行一个 JSON 对象）
- 事件包含：type、choice、text、timestamp
- 用户可能点击多个选项（探索行为），最后一个是最终选择
- 点击模式本身也是信息来源（犹豫、偏好）

---

### 段落 10: 设计技巧

**原文:**
```markdown
## Design Tips

- **Scale fidelity to the question** — wireframes for layout, polish for polish questions
- **Explain the question on each page** — "Which layout feels more professional?" not just "Pick one"
- **Iterate before advancing** — if feedback changes current screen, write a new version
- **2-4 options max** per screen
- **Use real content when it matters** — for a photography portfolio, use actual images (Unsplash). Placeholder content obscures design issues.
- **Keep mockups simple** — focus on layout and structure, not pixel-perfect design
```

**翻译:**
```markdown
## 设计技巧

- **保真度与问题匹配** — 布局用线框图，打磨问题用精细设计
- **在每一页上解释问题** — "哪种布局感觉更专业？"而不是"选一个"
- **在推进前迭代** — 如果反馈改变了当前屏幕，写一个新版本
- **每屏最多 2-4 个选项**
- **重要时使用真实内容** — 对于摄影作品集，使用实际图片（Unsplash）。占位内容会掩盖设计问题。
- **保持原型简单** — 关注布局和结构，而非像素级完美设计
```

**要点:**
- 保真度匹配问题复杂度（不要过度设计线框图）
- 每屏选项上限：4 个
- 真实内容比占位符更能暴露设计问题
- 迭代文化：反馈改变屏幕 → 写新版本

---

### 段落 11: 文件命名

**原文:**
```markdown
## File Naming

- Use semantic names: `platform.html`, `visual-style.html`, `layout.html`
- Never reuse filenames — each screen must be a new file
- For iterations: append version suffix like `layout-v2.html`, `layout-v3.html`
- Server serves newest file by modification time
```

**翻译:**
```markdown
## 文件命名

- 使用语义化名称：`platform.html`、`visual-style.html`、`layout.html`
- 永远不要复用文件名——每个屏幕必须是一个新文件
- 迭代时：追加版本后缀如 `layout-v2.html`、`layout-v3.html`
- 服务器按修改时间提供最新的文件
```

**要点:**
- 语义化命名，便于理解
- 严格禁止复用文件名（防止缓存/混淆）
- 迭代版本：`layout-v2.html`、`layout-v3.html`

---

### 段落 12: 清理

**原文:**
```markdown
## Cleaning Up

```bash
scripts/stop-server.sh $SESSION_DIR
```

If the session used `--project-dir`, mockup files persist in `.superpowers/brainstorm/` for later reference. Only `/tmp` sessions get deleted on stop.
```

**翻译:**
```markdown
## 清理

```bash
scripts/stop-server.sh $SESSION_DIR
```

如果会话使用了 `--project-dir`，原型文件会持久化在 `.superpowers/brainstorm/` 中供以后参考。只有 `/tmp` 会话在停止时被删除。
```

**要点:**
- 停止命令：`stop-server.sh $SESSION_DIR`
- 持久化会话的文件保留，临时会话（`/tmp`）删除

---

### 段落 13: 参考

**原文:**
```markdown
## Reference

- Frame template (CSS reference): `scripts/frame-template.html`
- Helper script (client-side): `scripts/helper.js`
```

**翻译:**
```markdown
## 参考

- 框架模板（CSS 参考）：`scripts/frame-template.html`
- 辅助脚本（客户端）：`scripts/helper.js`
```

**要点:**
- 两个参考文件：框架模板和客户端 helper 脚本

---

## spec-document-reviewer-prompt.md 逐段分析

### 段落 1: 标题与用途

**原文:**
```markdown
# Spec Document Reviewer Prompt Template

Use this template when dispatching a spec document reviewer subagent.

**Purpose:** Verify the spec is complete, consistent, and ready for implementation planning.

**Dispatch after:** Spec document is written to docs/superpowers/specs/
```

**翻译:**
```markdown
# Spec 文档审查者 Prompt 模板

在派发 spec 文档审查子 agent 时使用此模板。

**目的：** 验证 spec 是否完整、一致，并准备好进行实现规划。

**派发时机：** Spec 文档已写入 docs/superpowers/specs/ 后
```

**要点:**
- 这是一个 prompt 模板，用于创建审查子 agent
- 审查时机：spec 编写完成后、实现规划前
- 审查目的：确保 spec 质量，避免有缺陷的规划

---

### 段落 2: 审查内容

**原文:**
```markdown
**Task tool (general-purpose):**
  description: "Review spec document"
  prompt: |
    You are a spec document reviewer. Verify this spec is complete and ready for planning.

    **Spec to review:** [SPEC_FILE_PATH]

    ## What to Check

    | Category | What to Look For |
    |----------|------------------|
    | Completeness | TODOs, placeholders, "TBD", incomplete sections |
    | Consistency | Internal contradictions, conflicting requirements |
    | Clarity | Requirements ambiguous enough to cause someone to build the wrong thing |
    | Scope | Focused enough for a single plan — not covering multiple independent subsystems |
    | YAGNI | Unrequested features, over-engineering |

    ## Calibration

    **Only flag issues that would cause real problems during implementation planning.**
    A missing section, a contradiction, or a requirement so ambiguous it could be
    interpreted two different ways — those are issues. Minor wording improvements,
    stylistic preferences, and "sections less detailed than others" are not.

    Approve unless there are serious gaps that would lead to a flawed plan.

    ## Output Format

    ## Spec Review

    **Status:** Approved | Issues Found

    **Issues (if any):**
    - [Section X]: [specific issue] - [why it matters for planning]

    **Recommendations (advisory, do not block approval):**
    - [suggestions for improvement]
```

**翻译:**
```markdown
**Task 工具（通用目的）：**
  描述："审查 spec 文档"
  prompt: |
    你是一个 spec 文档审查者。验证此 spec 是否完整并准备好进行规划。

    **要审查的 spec：** [SPEC_FILE_PATH]

    ## 检查内容

    | 类别 | 查找内容 |
    |------|----------|
    | 完整性 | TODO、占位符、"TBD"、不完整的部分 |
    | 一致性 | 内部矛盾、冲突的需求 |
    | 清晰性 | 模糊到可能导致某人构建错误东西的需求 |
    | 范围 | 是否足够聚焦以放入单个计划——不覆盖多个独立的子系统 |
    | YAGNI | 未请求的功能、过度工程 |

    ## 校准标准

    **只标记会在实现规划期间造成真正问题的问题。**
    缺失的部分、矛盾、或模糊到可以被两种不同方式解读的需求——这些才是问题。
    细微的措辞改进、风格偏好、和"某些部分不如其他部分详细"不是。

    除非存在会导致缺陷计划的严重漏洞，否则批准。

    ## 输出格式

    ## Spec 审查

    **状态：** 已批准 | 发现问题

    **问题（如有）：**
    - [第 X 部分]：[具体问题] - [为什么它对规划重要]

    **建议（参考性，不阻塞批准）：**
    - [改进建议]
```

**要点:**
- 审查五维度：完整性、一致性、清晰性、范围、YAGNI
- 校准原则：只标记真正影响规划的问题，不纠结于措辞和风格
- 输出格式：状态（Approved/Issues Found）、问题列表、建议列表
- 建议不阻塞批准，只有严重问题才阻塞

---

### 段落 3: 审查者返回

**原文:**
```markdown
**Reviewer returns:** Status, Issues (if any), Recommendations
```

**翻译:**
```markdown
**审查者返回：** 状态、问题（如有）、建议
```

**要点:**
- 审查者输出三部分：状态、问题、建议

---

## 脚本文件详细分析

### start-server.sh

**代码结构:**
- 参数解析：支持 `--project-dir`、`--host`、`--url-host`、`--foreground`、`--background`
- 环境检测：自动检测 Codex（`CODEX_CI`）和 Windows（`OSTYPE`/`MSYSTEM`），切换到前台模式
- 会话目录生成：使用 `$$-$(date +%s)` 创建唯一会话 ID
- 目录结构：`$SESSION_DIR/content`（HTML 文件）和 `$SESSION_DIR/state`（状态文件）
- 旧进程清理：如果存在 `server.pid`，杀死旧进程
- PID 解析：尝试解析 harness PID（脚本的父进程的父进程）
- 启动模式：
  - 前台模式：直接运行 node server.cjs
  - 后台模式：使用 `nohup` + `disown`，并将输出重定向到日志文件
- 健康检查：轮询日志文件最多 5 秒，等待 `server-started` 消息
- 存活验证：确认服务器进程在启动后仍然存活

**关键逻辑:**
- 跨平台兼容是核心挑战（不同环境对后台进程的处理不同）
- 使用 `nohup` 和 `disown` 确保后台进程 survive shell exit
- 通过 `OWNER_PID` 监控实现"主人进程退出则服务器关闭"

**数据流:**
- 输入：命令行参数
- 输出：JSON（成功时返回 server-started 信息，失败时返回错误）
- 状态：写入 `$STATE_DIR/server.pid` 和 `$STATE_DIR/server.log`

---

### server.cjs

**代码结构:**
1. **WebSocket 协议实现**（RFC 6455）：
   - `computeAcceptKey`：计算 WebSocket 握手 accept key
   - `encodeFrame`/`decodeFrame`：编解码 WebSocket 数据帧
   - 支持 TEXT、CLOSE、PING、PONG 操作码

2. **配置解析**：
   - 从环境变量读取 PORT、HOST、URL_HOST、SESSION_DIR、OWNER_PID
   - 默认端口：49152-65535 范围内的随机端口

3. **模板加载**：
   - 读取 `frame-template.html` 和 `helper.js`
   - 构建 `helperInjection`（注入到每个页面的脚本）

4. **HTTP 请求处理**：
   - `GET /`：返回最新屏幕（自动包装在框架模板中）
   - `GET /files/<name>`：提供 content 目录中的静态文件
   - 自动将 helper 脚本注入到 HTML 中

5. **WebSocket 连接处理**：
   - 握手升级处理
   - 消息解析和事件记录
   - 广播 reload 消息给所有客户端

6. **文件监视**：
   - 使用 `fs.watch` 监视 `content` 目录
   - 新文件：清除 events 文件，广播 reload
   - 更新文件：广播 reload
   - 100ms 防抖

7. **生命周期管理**：
   - 每 60 秒检查：owner 进程是否存活、是否空闲超过 30 分钟
   - 任一条件满足则优雅关闭

**关键逻辑:**
- 文件监视 + WebSocket 广播实现"保存即刷新"
- 新屏幕自动清除旧 events，确保每个屏幕有独立的选择记录
- 空闲超时 30 分钟，防止服务器无限运行

**数据流:**
- 输入：HTML 文件写入 `content/` 目录、用户浏览器点击
- 输出：HTTP 响应、WebSocket 消息、events 文件
- 状态：`server-info`、`server.pid`、`events`、`server-stopped`

---

### helper.js

**代码结构:**
1. **WebSocket 连接**：
   - 连接到 `ws://window.location.host`
   - 自动重连（断开后 1 秒重试）
   - 消息队列：连接前发送的事件缓存，连接后批量发送

2. **事件捕获**：
   - 监听 `click` 事件，捕获 `[data-choice]` 元素的点击
   - 发送事件：type、text、choice、id

3. **UI 反馈**：
   - `toggleSelect`：切换选中状态，支持单选和多选
   - 更新指示器栏：显示当前选中项或选中数量

4. **API 暴露**：
   - `window.brainstorm.send`：发送自定义事件
   - `window.brainstorm.choice`：发送选择事件

**关键逻辑:**
- 事件委托模式：在 document 上监听 click，通过 `closest('[data-choice]')` 找到目标
- 单选/多选区分：检查容器是否有 `data-multiselect` 属性
- 选择状态持久化在 DOM class 中，不依赖服务器

**数据流:**
- 输入：用户点击、页面 reload WebSocket 消息
- 输出：WebSocket 事件消息
- 状态：DOM class（selected）、indicator-text 内容

---

### stop-server.sh

**代码结构:**
- 参数检查：必须提供 `SESSION_DIR`
- 读取 PID 文件
- 优雅停止：先发送 SIGTERM，等待最多 2 秒
- 强制停止：如果仍在运行，发送 SIGKILL
- 清理：删除 PID 文件和日志文件
- 目录处理：仅删除 `/tmp/*` 下的临时目录

**关键逻辑:**
- 分层停止策略：SIGTERM → 等待 → SIGKILL
- 区分临时和持久化会话：不删除 `.superpowers/` 目录

---

## 整体总结

### 核心概念

| 概念 | 定义 |
|------|------|
| **Brainstorming** | 在实施前通过对话将想法转化为完整设计的流程 |
| **HARD-GATE** | 硬性门槛：未经设计批准禁止任何实现动作 |
| **Visual Companion** | 可选的浏览器辅助工具，用于展示视觉原型和选项 |
| **Spec** | 设计文档，记录验证过的设计决策 |
| **YAGNI** | "You Aren't Gonna Need It"——避免过度设计的核心原则 |
| **Content Fragment** | 不完整的 HTML 片段，由服务器自动包装成完整页面 |
| **Screen** | 一次视觉呈现，对应一个 HTML 文件 |

### 工作流程

```
用户提出想法
    ↓
探索项目上下文（文件、文档、提交）
    ↓
[可选] 提供 Visual Companion（浏览器辅助）
    ↓
逐个问题澄清（目的、约束、成功标准）
    ↓
提出 2-3 种方案（含权衡分析和推荐）
    ↓
分节呈现设计（架构、组件、数据流、错误处理、测试）
    ↓
用户批准设计？
    ├── 否 → 修订 → 重新呈现
    └── 是 → 编写 spec 文档
              ↓
         Spec 自检（占位符、一致性、范围、歧义）
              ↓
         用户审查 spec
              ↓
         用户批准？
              ├── 否 → 修改 → 重新自检
              └── 是 → 调用 writing-plans skill
```

### 关键文件及其作用

| 文件 | 作用 |
|------|------|
| `SKILL.md` | Brainstorming skill 的主定义，包含完整流程和规则 |
| `visual-companion.md` | 浏览器辅助工具的详细使用指南 |
| `spec-document-reviewer-prompt.md` | 创建 spec 审查子 agent 的 prompt 模板 |
| `scripts/start-server.sh` | 启动服务器，处理跨平台兼容性 |
| `scripts/server.cjs` | HTTP + WebSocket 服务器，实现文件监视和实时刷新 |
| `scripts/helper.js` | 浏览器端脚本，处理点击事件和选择状态 |
| `scripts/stop-server.sh` | 停止服务器，区分临时/持久化会话 |
| `scripts/frame-template.html` | HTML 页面框架模板，提供 CSS 和交互基础设施 |

### 如何复刻/应用

1. **直接应用此 skill**：
   - 在 Claude Code 中将此 skill 放入 `.claude/skills/brainstorming/`
   - 确保 `docs/superpowers/specs/` 目录存在
   - 遵循 9 步检查清单执行 brainstorm

2. **复刻 Visual Companion**：
   - 核心机制：文件监视 + WebSocket 广播
   - 需要：HTTP 服务器、WebSocket 服务器、文件系统监视器
   - 客户端：点击事件捕获、选择状态管理、自动重连
   - 关键设计：内容片段自动包装、新文件清除旧事件、空闲超时

3. **复刻 Spec 审查流程**：
   - 创建子 agent，使用提供的 prompt 模板
   - 审查五维度：完整性、一致性、清晰性、范围、YAGNI
   - 校准原则：只标记真正影响规划的问题
