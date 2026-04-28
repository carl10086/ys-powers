# idea-refine Skill 逐段精读分析

## 分析概要

### 文档定位
这是一份 **agent skill 文档**，定义了 `idea-refine`（创意精炼）的方法论，属于 `agent-skills` 框架中 Define 阶段的一个 skill。

### 核心主张
通过**结构化发散与收敛思考**，将粗糙的原始想法打磨成"值得构建的、清晰可执行的"概念。不是头脑风暴——而是有纪律的创意锻造。

### 结构骨架

| 章节 | 内容 |
|------|------|
| How It Works + Usage + Output | Skill 定位、触发方式、产出物定义 |
| Philosophy | 6 条创意哲学（极简、UX 优先、说不、挑战假设等） |
| Process (3 Phases) | Phase 1 发散 → Phase 2 收敛 → Phase 3 输出 |
| Anti-patterns + Tone | 7 个反模式 + 沟通语气规范 |
| Red Flags + Verification | 危险信号与验收清单 |

### 关键洞察

1. **"Not Doing" 列表是最有价值的部分**——文档反复强调，专注的本质是对好想法说不
2. **不是 yes-machine**——好的创意伙伴要诚实推回，弱想法要直接指出
3. **Phase 1 的 6 个透镜**（Inversion、Constraint removal、Audience shift 等）是可复用的思维框架
4. **引用的 3 个外部文件**（frameworks.md、refinement-criteria.md、examples.md）构成了完整的工具箱

---

## 逐段精读

### 段落 1: Frontmatter

**原文:**
```yaml
---
name: idea-refine
description: Refines ideas iteratively. Refine ideas through structured divergent and convergent thinking. Use "idea-refine" or "ideate" to trigger.
---
```

**翻译:**
```yaml
---
name: idea-refine
description: 迭代精炼创意。通过结构化发散与收敛思考打磨创意。使用 "idea-refine" 或 "ideate" 触发。
---
```

**要点:**
- **触发词双轨制**: 既可用 `idea-refine`（正式 skill 名），也可用 `ideate`（口语化）触发，降低了用户记忆成本
- **强调"迭代"**: 不是一次性的头脑风暴，而是反复打磨
- **"发散与收敛"是核心方法论**: 这是设计思维的经典框架，文档将其结构化应用于 AI 交互

---

### 段落 2: 主标题段

**原文:**
> Refines raw ideas into sharp, actionable concepts worth building through structured divergent and convergent thinking.

**翻译:**
> 通过结构化发散与收敛思考，将粗糙的想法打磨成锐利、可执行、值得构建的概念。

**要点:**
- **三个递进形容词**: raw（原始）→ sharp（锐利）→ actionable（可执行）→ worth building（值得构建）
- **"worth building"是最终门槛**: 不是"有趣的点子"，而是"值得投入工程资源的创意"
- **主语缺失（隐含 agent）**: 文档用无主语句，暗示这是 agent 的核心职责

---

### 段落 3: How It Works

**原文:**
> 1. **Understand & Expand (Divergent):** Restate the idea, ask sharpening questions, and generate variations.
> 2. **Evaluate & Converge:** Cluster ideas, stress-test them, and surface hidden assumptions.
> 3. **Sharpen & Ship:** Produce a concrete markdown one-pager moving work forward.

**翻译:**
> 1. **理解与扩展（发散）**: 重述想法，提出 sharpening 问题，生成变体
> 2. **评估与收敛**: 聚类想法，压力测试，暴露隐藏假设
> 3. **精炼与交付**: 产出一份推动工作前进的 concrete markdown one-pager

**要点:**
- **三阶段命名精确**: Divergent（发散）→ Converge（收敛）→ Ship（交付），符合设计思维的双钻模型
- **"sharpening questions"是关键词**: 不是任意提问，而是让想法更锐利的问题
- **产出物明确**: concrete markdown one-pager，不是开放式讨论，而是结构化文档

---

### 段落 4: Usage

**原文:**
> This skill is primarily an interactive dialogue. Invoke it with an idea, and the agent will guide you through the process.
> 
> ```bash
> # Optional: Initialize the ideas directory
> bash /mnt/skills/user/idea-refine/scripts/idea-refine.sh
> ```
> 
> **Trigger Phrases:**
> - "Help me refine this idea"
> - "Ideate on [concept]"
> - "Stress-test my plan"

**翻译:**
> 此 skill 主要是一种交互式对话。用一个想法触发它，agent 会引导你完成整个过程。
> 
> ```bash
> # 可选：初始化 ideas 目录
> bash /mnt/skills/user/idea-refine/scripts/idea-refine.sh
> ```
> 
> **触发短语:**
> - "帮我精炼这个想法"
> - "就 [概念] 进行头脑风暴"
> - "压力测试我的计划"

**要点:**
- **交互式对话定位**: 不是一次性输出，而是多轮对话
- **可选初始化脚本**: `/mnt/skills/user/idea-refine/scripts/idea-refine.sh` 是一个具体的路径引用，但文档中没有展开此脚本的内容
- **触发短语覆盖三种场景**: 精炼（refine）、头脑风暴（ideate）、压力测试（stress-test）

---

### 段落 5: Output

**原文:**
> The final output is a markdown one-pager saved to `docs/ideas/[idea-name].md` (after user confirmation), containing:
> - Problem Statement
> - Recommended Direction
> - Key Assumptions
> - MVP Scope
> - Not Doing list

**翻译:**
> 最终产出是一份保存到 `docs/ideas/[idea-name].md` 的 markdown one-pager（需用户确认后保存），包含：
> - 问题陈述
> - 推荐方向
> - 关键假设
> - MVP 范围
> - 不做清单

**要点:**
- **产出物结构化**: 5 个固定字段，不是自由文本
- **需要用户确认**: 不是自动保存，体现用户控制权
- **`docs/ideas/` 是约定目录**: 与 `docs/ys-powers/plans/` 等项目结构呼应
- **"Not Doing list"作为一等公民**: 与问题陈述、MVP 并列，说明"说不"和"说做"同等重要

---

### 段落 6: Philosophy

**原文:**
> - Simplicity is the ultimate sophistication. Push toward the simplest version that still solves the real problem.
> - Start with the user experience, work backwards to technology.
> - Say no to 1,000 things. Focus beats breadth.
> - Challenge every assumption. "How it's usually done" is not a reason.
> - Show people the future — don't just give them better horses.
> - The parts you can't see should be as beautiful as the parts you can.

**翻译:**
> - 极简是终极的复杂。推向能解决真正问题的最简单版本。
> - 从用户体验出发，反向推导技术方案。
> - 对 1000 个东西说不。专注胜过广度。
> - 挑战每一个假设。"历来如此"不是理由。
> - 向人们展示未来——不要只给他们更好的马。
> - 你看不见的部分应该和看得见的一样美。

**要点:**
- **六条哲学高度浓缩**: 涵盖极简主义（1,3）、UX 优先（2）、批判思维（4）、愿景驱动（5）、工程美学（6）
- **"更好的马"典故**: 引用亨利·福特的名言，暗示不要只做渐进式改进，要做范式跃迁
- **与 `using-agent-skills` 的 "Enforce Simplicity" 核心规则完全一致**
- **"Say no to 1,000 things"**: 直接引用史蒂夫·乔布斯，强调专注

---

### 段落 7: Process 总起

**原文:**
> When the user invokes this skill with an idea (`$ARGUMENTS`), guide them through three phases. Adapt your approach based on what they say — this is a conversation, not a template.

**翻译:**
> 当用户用一个想法（`$ARGUMENTS`）触发此 skill 时，引导他们通过三个阶段。根据他们说的话调整你的方法——这是对话，不是模板。

**要点:**
- **`$ARGUMENTS` 是参数占位符**: 说明此 skill 接受用户输入的想法作为参数
- **"对话，不是模板"**: 强调灵活性，三个阶段是节奏而非死板的检查单
- **适应性要求**: agent 需要根据用户反应动态调整，不是机械执行

---

### 段落 8: Phase 1 — Restate the idea

**原文:**
> **Goal:** Take the raw idea and open it up.
> 
> 1. **Restate the idea** as a crisp "How Might We" problem statement. This forces clarity on what's actually being solved.

**翻译:**
> **目标:** 拿住粗糙的想法并打开它。
> 
> 1. **将想法重述**为一个清晰的"我们如何能"（HMW）问题陈述。这迫使澄清真正要解决的是什么。

**要点:**
- **Phase 1 的目标是"打开"**: 发散不是目的，目的是扩展可能性空间
- **HMW 格式强制澄清**: 不是"我要做个 XXX"，而是"我们如何能帮 [用户] 解决 [问题]"
- **"forces clarity"**: 重述不是装饰，而是诊断工具——如果无法清晰重述，说明想法本身模糊

---

### 段落 9: Phase 1 — Ask sharpening questions

**原文:**
> 2. **Ask 3-5 sharpening questions** — no more. Focus on:
>    - Who is this for, specifically?
>    - What does success look like?
>    - What are the real constraints (time, tech, resources)?
>    - What's been tried before?
>    - Why now?
> 
>    Use the `AskUserQuestion` tool to gather this input. Do NOT proceed until you understand who this is for and what success looks like.

**翻译:**
> 2. **提出 3-5 个 sharpening 问题**——不要更多。聚焦于：
>    - 这具体是为谁做的？
>    - 成功是什么样？
>    - 真正的约束是什么（时间、技术、资源）？
>    - 之前尝试过什么？
>    - 为什么是现在？
> 
>    使用 `AskUserQuestion` 工具收集这些输入。**在理解为谁做、成功什么样之前，不要继续。**

**要点:**
- **3-5 个问题，不多不少**: 太少诊断不足，太多让用户疲惫
- **五个问题覆盖经典框架**: 用户（Who）、目标（What）、约束（Constraints）、历史（What's been tried）、时机（Why now）
- **`AskUserQuestion` 是强制工具**: 不是聊天式追问，而是用工具结构化收集
- **硬停止条件**: "Do NOT proceed until..."——这是 skill 中的硬性质量门

---

### 段落 10: Phase 1 — Generate variations

**原文:**
> 3. **Generate 5-8 idea variations** using these lenses:
>    - **Inversion:** "What if we did the opposite?"
>    - **Constraint removal:** "What if budget/time/tech weren't factors?"
>    - **Audience shift:** "What if this were for [different user]?"
>    - **Combination:** "What if we merged this with [adjacent idea]?"
>    - **Simplification:** "What's the version that's 10x simpler?"
>    - **10x version:** "What would this look like at massive scale?"
>    - **Expert lens:** "What would [domain] experts find obvious that outsiders wouldn't?"
> 
>    Push beyond what the user initially asked for. Create products people don't know they need yet.

**翻译:**
> 3. **使用以下透镜生成 5-8 个想法变体**：
>    - **反转:**"如果我们做相反的事会怎样？"
>    - **移除约束:**"如果预算/时间/技术不是问题会怎样？"
>    - **受众转移:**"如果这是为 [不同用户] 做的呢？"
>    - **组合:**"如果我们把它和 [相邻想法] 合并呢？"
>    - **简化:**"10 倍简化的版本是什么？"
>    - **10 倍版本:**"大规模下这会是什么样？"
>    - **专家视角:**"[领域] 专家会觉得什么是外人看不出来的？"
> 
>    超越用户最初的要求。创造人们不知道自己需要的产品。

**要点:**
- **7 个透镜是可复用的思维工具**: 每个透镜都是一种系统性打破思维定式的方法
- **5-8 个变体**: 与反模式中的"不要生成 20+ 个浅层想法"呼应
- **"Create products people don't know they need yet"**: 直接引用乔布斯/福特的创新哲学
- **与 frameworks.md 的关系**: 这里的 7 个透镜是 frameworks.md 中框架的子集/变体

---

### 段落 11: Phase 1 — Codebase context

**原文:**
> **If running inside a codebase:** Use `Glob`, `Grep`, and `Read` to scan for relevant context — existing architecture, patterns, constraints, prior art. Ground your variations in what actually exists. Reference specific files and patterns when relevant.

**翻译:**
> **如果在代码库中运行:** 使用 `Glob`、`Grep` 和 `Read` 扫描相关上下文——现有架构、模式、约束、先例。让你的变体立足于实际存在的东西。在相关时引用具体文件和模式。

**要点:**
- **代码库感知是差异化设计**: 不是所有 ideation 都抽象进行，在项目中时要结合现实约束
- **三个工具（Glob/Grep/Read）是具体指令**: 不是"看看代码"，而是明确使用这些工具
- **"Ground your variations in what actually exists"**: 防止 agent 提出与现有架构完全不兼容的幻想方案

---

### 段落 12: Phase 1 — Read frameworks.md

**原文:**
> Read `frameworks.md` in this skill directory for additional ideation frameworks you can draw from. Use them selectively — pick the lens that fits the idea, don't run every framework mechanically.

**翻译:**
> 读取此 skill 目录中的 `frameworks.md`，获取可借鉴的额外创意框架。有选择地使用它们——挑选适合想法的透镜，不要机械地运行每个框架。

**要点:**
- **选择性使用是强制要求**: "don't run every framework mechanically"——防止 agent 变成检查单机器
- **`frameworks.md` 是扩展工具箱**: 主文档提供 7 个透镜，frameworks.md 提供 6 个更系统的框架（SCAMPER、HMW、First Principles、JTBD、Constraint-Based、Pre-mortem、Analogous Inspiration）
- **"pick the lens that fits the idea"**: 强调适配性而非全面性

---

### 段落 13: Phase 2 — Cluster

**原文:**
> After the user reacts to Phase 1 (indicates which ideas resonate, pushes back, adds context), shift to convergent mode:
> 
> 1. **Cluster** the ideas that resonated into 2-3 distinct directions. Each direction should feel meaningfully different, not just variations on a theme.

**翻译:**
> 在用户回应 Phase 1 后（指出哪些想法共鸣、推回、补充上下文），切换到收敛模式：
> 
> 1. **聚类**共鸣的想法为 2-3 个不同方向。每个方向应该感觉有实质不同，而不只是主题上的变体。

**要点:**
- **Phase 2 的启动条件是用户反应**: 不是自动继续，需要用户输入
- **2-3 个方向，不是更多**: 太少缺乏选择，太多无法深入
- **"meaningfully different"是质量标准**: 不是表面差异，而是核心假设不同的方向

---

### 段落 14: Phase 2 — Stress-test

**原文:**
> 2. **Stress-test** each direction against three criteria:
>    - **User value:** Who benefits and how much? Is this a painkiller or a vitamin?
>    - **Feasibility:** What's the technical and resource cost? What's the hardest part?
>    - **Differentiation:** What makes this genuinely different? Would someone switch from their current solution?
> 
>    Read `refinement-criteria.md` in this skill directory for the full evaluation rubric.

**翻译:**
> 2. 用三个标准对每个方向进行**压力测试**：
>    - **用户价值:** 谁受益、受益多少？这是止痛药还是维生素？
>    - **可行性:** 技术和资源成本是什么？最难的部分是什么？
>    - **差异化:** 什么让这真正不同？有人愿意从现有方案切换过来吗？
> 
>    读取此 skill 目录中的 `refinement-criteria.md` 获取完整评估标准。

**要点:**
- **三个标准（User Value / Feasibility / Differentiation）是黄金三角**: 价值不够则无需考虑，不可行则无法落地，无差异则无法竞争
- **"Painkiller vs Vitamin"是经典产品框架**: 止痛药（用户主动寻找）vs 维生素（可有可无）
- **`refinement-criteria.md` 包含详细评估表**: 包括 Painkiller/Vitamin 的具体症状、可行性红线、差异化的 6 个层级（New capability → Cheaper）

---

### 段落 15: Phase 2 — Surface hidden assumptions

**原文:**
> 3. **Surface hidden assumptions.** For each direction, explicitly name:
>    - What you're betting is true (but haven't validated)
>    - What could kill this idea
>    - What you're choosing to ignore (and why that's okay for now)
> 
>    This is where most ideation fails. Don't skip it.

**翻译:**
> 3. **暴露隐藏假设。** 对每个方向，明确命名：
>    - 你在赌什么为真（但尚未验证）
>    - 什么可能杀死这个想法
>    - 你选择忽略什么（以及为什么现在可以忽略）
> 
>    这是大多数创意失败的地方。不要跳过。

**要点:**
- **"This is where most ideation fails"**: 作者明确指出这是最关键也最常被跳过的步骤
- **三个层次**: 未验证的赌注（正向假设）、致命风险（负向假设）、有意忽略的（范围决策）
- **与 `refinement-criteria.md` 的 Assumption Audit 呼应**: 将假设分为 Must Be True / Should Be True / Might Be True 三级

---

### 段落 16: Phase 2 — Be honest

**原文:**
> **Be honest, not supportive.** If an idea is weak, say so with kindness. A good ideation partner is not a yes-machine. Push back on complexity, question real value, and point out when the emperor has no clothes.

**翻译:**
> **诚实，而非支持。** 如果一个想法很弱，善意地指出来。一个好的创意伙伴不是 yes-machine。对复杂性推回，质疑真实价值，在皇帝没穿衣服时指出来。

**要点:**
- **"Be honest, not supportive"**: 直接引用，语气强烈
- **"with kindness"**: 诚实不等于刻薄，推回需要建设性
- **与 `using-agent-skills` 的 "Push Back When Warranted" 核心规则完全一致**
- **"emperor has no clothes"**: 经典隐喻，指明显的问题不能被权威/惯性掩盖

---

### 段落 17: Phase 3 — Sharpen & Ship

**原文:**
> Produce a concrete artifact — a markdown one-pager that moves work forward:
> 
> ```markdown
> # [Idea Name]
> 
> ## Problem Statement
> [One-sentence "How Might We" framing]
> 
> ## Recommended Direction
> [The chosen direction and why — 2-3 paragraphs max]
> 
> ## Key Assumptions to Validate
> - [ ] [Assumption 1 — how to test it]
> - [ ] [Assumption 2 — how to test it]
> - [ ] [Assumption 3 — how to test it]
> 
> ## MVP Scope
> [The minimum version that tests the core assumption. What's in, what's out.]
> 
> ## Not Doing (and Why)
> - [Thing 1] — [reason]
> - [Thing 2] — [reason]
> - [Thing 3] — [reason]
> 
> ## Open Questions
> - [Question that needs answering before building]
> ```
> 
> **The "Not Doing" list is arguably the most valuable part.** Focus is about saying no to good ideas. Make the trade-offs explicit.
> 
> Ask the user if they'd like to save this to `docs/ideas/[idea-name].md` (or a location of their choosing). Only save if they confirm.

**翻译:**
> 产出一份具体的产物——一份推动工作前进的 markdown one-pager：
> [one-pager 模板，包含问题陈述/推荐方向/待验证关键假设/MVP范围/不做/开放问题]
> 
> **"不做"清单可以说是最有价值的部分。** 专注是对好想法说不。让权衡显式化。
> 
> 询问用户是否想保存到 `docs/ideas/[idea-name].md`（或他们选择的其他位置）。只有在用户确认后才保存。

**要点:**
- **Phase 3 是产出，不是讨论**: 前面两阶段是对话，第三阶段是产物
- **one-pager 模板结构化**: 6 个固定字段，其中 Key Assumptions 带有复选框和验证方法
- **"Not Doing" 被明确标注为最有价值**: 作者三次强调这一点（Philosophy 中一次，这里两次）
- **用户确认是硬性要求**: "Only save if they confirm"——尊重用户控制权

---

### 段落 18: Anti-patterns to Avoid

**原文:**
> - **Don't generate 20+ ideas.** Quality over quantity. 5-8 well-considered variations beat 20 shallow ones.
> - **Don't be a yes-machine.** Push back on weak ideas with specificity and kindness.
> - **Don't skip "who is this for."** Every good idea starts with a person and their problem.
> - **Don't produce a plan without surfacing assumptions.** Untested assumptions are the #1 killer of good ideas.
> - **Don't over-engineer the process.** Three phases, each doing one thing well. Resist adding steps.
> - **Don't just list ideas — tell a story.** Each variation should have a reason it exists, not just be a bullet point.
> - **Don't ignore the codebase.** If you're in a project, the existing architecture is a constraint and an opportunity. Use it.

**翻译:**
> - **不要生成 20+ 个想法。** 质量胜过数量。5-8 个深思熟虑的变体胜过 20 个浅层的。
> - **不要做 yes-machine。** 用具体性和善意对弱想法推回。
> - **不要跳过"这是为谁做的"。** 每个好想法都始于一个人和他们的难题。
> - **不要在未暴露假设的情况下产出计划。** 未测试的假设是好想法的头号杀手。
> - **不要过度工程化流程。** 三个阶段，每个做好一件事。抵制添加步骤。
> - **不要只是列想法——讲个故事。** 每个变体应该有它存在的理由，不只是个 bullet point。
> - **不要忽视代码库。** 如果你在项目中，现有架构既是约束也是机会。利用它。

**要点:**
- **7 个反模式覆盖常见 LLM 错误**: 生成太多（1）、迎合用户（2）、忽略用户（3）、忽略假设（4）、流程臃肿（5）、罗列无故事（6）、脱离上下文（7）
- **"#1 killer of good ideas"**: 未测试的假设——与 Phase 2 的 "Surface hidden assumptions" 呼应
- **"tell a story"**: 每个变体需要叙事逻辑（用了什么透镜、为什么存在），不是随机生成

---

### 段落 19: Tone

**原文:**
> Direct, thoughtful, slightly provocative. You're a sharp thinking partner, not a facilitator reading from a script. Channel the energy of "that's interesting, but what if..." -- always pushing one step further without being exhausting.
> 
> Read `examples.md` in this skill directory for examples of what great ideation sessions look like.

**翻译:**
> 直接、深思熟虑、略带挑衅。你是一个锐利的思考伙伴，不是照着脚本读的引导者。传递"这很有趣，但如果..."的能量——总是再推进一步，但不让人疲惫。
> 
> 读取此 skill 目录中的 `examples.md`，获取优秀创意会话的示例。

**要点:**
- **语气定位精确**: Direct（不绕弯子）、thoughtful（有深度）、slightly provocative（适度挑战）
- **"sharp thinking partner" vs "facilitator"**: 区分在于前者有观点、会推回，后者只是引导流程
- **"without being exhausting"**: 推进需要节奏感，不能让用户感到被攻击或疲劳
- **Read `examples.md`**: 用 3 个完整示例展示这种语气的具体表现

---

### 段落 20: Red Flags

**原文:**
> - Generating 20+ shallow variations instead of 5-8 considered ones
> - Skipping the "who is this for" question
> - No assumptions surfaced before committing to a direction
> - Yes-machining weak ideas instead of pushing back with specificity
> - Producing a plan without a "Not Doing" list
> - Ignoring existing codebase constraints when ideating inside a project
> - Jumping straight to Phase 3 output without running Phases 1 and 2

**翻译:**
> - 生成 20+ 浅层变体而非 5-8 个深思熟虑的
> - 跳过"这是为谁做的"问题
> - 在承诺方向前未暴露假设
> - 对弱想法 yes-machine 而非用具体性推回
> - 产出计划但没有"不做"清单
> - 在项目中创意时忽视现有代码库约束
> - 跳过 Phase 1 和 2 直接跳到 Phase 3 输出

**要点:**
- **Red Flags 与 Anti-patterns 高度对应**: 只是从"不要做"转换为"危险信号"
- **新增第 7 条**: "Jumping straight to Phase 3"——这是最严重的流程违规，直接跳过诊断和收敛
- **代码库约束被反复强调**: 在 Usage、Process、Anti-patterns、Red Flags 四处出现，说明这是常见失败模式

---

### 段落 21: Verification

**原文:**
> After completing an ideation session:
> 
> - [ ] A clear "How Might We" problem statement exists
> - [ ] The target user and success criteria are defined
> - [ ] Multiple directions were explored, not just the first idea
> - [ ] Hidden assumptions are explicitly listed with validation strategies
> - [ ] A "Not Doing" list makes trade-offs explicit
> - [ ] The output is a concrete artifact (markdown one-pager), not just conversation
> - [ ] The user confirmed the final direction before any implementation work

**翻译:**
> 完成创意会话后：
> 
> - [ ] 存在清晰的"我们如何能"问题陈述
> - [ ] 目标用户和成功标准已定义
> - [ ] 探索了多个方向，不只是第一个想法
> - [ ] 隐藏假设被明确列出并附验证策略
> - [ ] "不做"清单让权衡显式化
> - [ ] 产出是具体产物（markdown one-pager），不只是对话
> - [ ] 用户在开始任何实施工作前确认了最终方向

**要点:**
- **7 项验收清单覆盖完整流程**: 从问题定义（1-2）→ 发散（3）→ 收敛（4-5）→ 产出（6）→ 用户确认（7）
- **最后一项是用户确认**: "user confirmed... before any implementation"——明确禁止未经确认的自动执行
- **与 `spec-driven-development` 的验收清单风格一致**: 复选框 + 可验证的标准

---

## 引用文件分析

### 引用文件 1: frameworks.md

**结构概述:**
包含 6 个（实际是 7 个，HMW 和 First Principles 分开计）创意框架，每个框架包含：
- 名称和一句话描述
- 具体操作步骤或问题清单
- **Best for:** 适用场景标注

**核心概念:**

| 框架 | 核心机制 | 适用场景 |
|------|---------|---------|
| **SCAMPER** | 7 种操作（Substitute/Combine/Adapt/Modify/Put to other uses/Eliminate/Reverse） | 改进或重新想象现有产品 |
| **How Might We (HMW)** | 将痛点重构为"我们如何能..."格式 | 被困在解决方案思维中时 |
| **First Principles Thinking** | 拆解到基本真理，再重建 | 打破渐进式思维 |
| **Jobs to Be Done (JTBD)** | 关注用户要完成的工作（功能/情感/社会） | 不确定是否解决了正确的问题 |
| **Constraint-Based Ideation** | 主动施加约束（时间/功能/技术/成本） | 想法太大或太模糊时 |
| **Pre-mortem** | 假设已失败，倒推原因 | Phase 2 压力测试 |
| **Analogous Inspiration** | 跨领域寻找结构相似性 | Phase 1 生成真正不同的变体 |

**关键洞察:**
- **"Use selectively" 贯穿始终**: 每个框架都有 "Best for" 标注，防止机械套用
- **"structural vs surface-level" 区分**: Analogous Inspiration 中明确批评 "Uber for X" 是表面类比，"解决陌生人信任问题的双边市场"才是结构类比
- **Pre-mortem 专门用于 Phase 2**: 说明 frameworks.md 中的框架不是只用于 Phase 1

---

### 引用文件 2: refinement-criteria.md

**结构概述:**
Phase 2 评估的完整评分标准，包含：
- 三个核心评估维度（User Value / Feasibility / Differentiation）
- Assumption Audit（假设审计，三级分类）
- Decision Framework（2x2 矩阵）
- MVP Scoping Principles（5 条原则）

**核心概念:**

**1. User Value — Painkiller vs Vitamin:**
- **Painkiller**: 解决急性、频繁的问题，用户会主动寻找，有情感色彩描述，有 workaround
- **Vitamin**: 锦上添花，用户礼貌点头但不会改变行为
- **Red flags**: "Everyone could use this"（无法命名具体用户）、"It's like X but better"（边际改进）、"real but rare"（高频 > 强度）

**2. Feasibility — 技术 + 资源 + Time-to-value:**
- 核心技术是否可靠存在？
- 最难的技术问题是已知难题还是新难题？
- MVP 能否在几天/几周内交付价值？
- **Red flags**: "We just need to solve [very hard research problem] first"、多依赖同时生效、MVP 仍需数月

**3. Differentiation — 六级梯度（强到弱）:**
1. New capability（以前不可能）→ 最强
2. 10x improvement（关键维度改变行为）
3. New audience（带给被排除的人）
4. New context（现有方案失效的场景）
5. Better UX（同样能力，更简单体验）
6. Cheaper（同样东西，更低成本）→ 最弱，易被复制

**4. Assumption Audit — 三级分类:**
- **Must Be True（Dealbreakers）**: 错了就杀死想法，需要在构建前验证
- **Should Be True（Important）**: 显著影响成功但不致命，错了可调整
- **Might Be True（Nice to Have）**: 关于次要功能，核心验证后再管

**5. Decision Framework — 2x2 矩阵:**
```
            High Feasibility    Low Feasibility
High Value    Do this first       Worth the risk
Low Value     Only if trivial     Don't do this
```
然后用 Differentiation 作为同象限的决胜因素。

**6. MVP Scoping Principles:**
1. One job, done well（MVP 只 nail 一个用户工作）
2. Riskiest assumption first（MVP 的首要目的是测试最可能错的假设）
3. Time-box, not feature-list（"在时间框内能做什么"优于"需要哪些功能"）
4. 'Not Doing' list is mandatory（明确命名切割什么及原因）
5. If it's not embarrassing, you waited too long（第一版应该让构建者感到不完整）

**关键洞察:**
- **"The real competitor is always the current workaround"**: 用户价值评估的核心洞见
- **Differentiation 六级梯度极具实操性**: 从"新能力"到"更便宜"的排序直接指导产品定位
- **"If it's not embarrassing, you waited too long"**: 与 MVP 的"最小"定义完全一致

---

### 引用文件 3: examples.md

**结构概述:**
3 个完整示例，展示不同类型的 ideation 会话：
1. **Example 1: 创业概念**（完整 3 阶段）— 帮助本地餐馆与外卖平台竞争
2. **Example 2: 产品功能**（Phase 1 + 概述 2-3）— 给文档编辑器加实时协作
3. **Example 3: 流程改进**（Phase 1 + 概述 2-3）— 改进团队回顾会议

**核心概念:**

**Example 1（餐馆 vs 外卖平台）:**
- **重述转变**: "帮助餐馆竞争" → "客户依赖问题"（平台拥有客户关系）
- **6 个变体**: Direct Channel Toolkit / Inversion（向顾客收费）/ Constraint Removal（只做自提）/ Combination（餐馆合作社）/ Audience Shift（只为老顾客）/ Expert Lens（零餐馆端操作）
- **Phase 2 诚实推回**: "你说 variation 1 '必要但无聊'，这种想包含'必要'东西的本能就是产品失去焦点的方式"
- **最终方向**: "Regulars Engine"—只服务老顾客的留存引擎，SMS 优先，零管理
- **Not Doing 列表 5 项**: 配送物流、客户获取、品牌应用、菜单管理/POS 集成、分析仪表盘

**Example 2（文档编辑器实时协作）:**
- **代码库感知**: 扫描到使用 block-based editor + REST API，无 WebSocket 基础设施
- **竞争压力 framing**: 这可能是 checkbox feature（必须有才能进入候选集）而非 differentiator
- **5 个变体**: Block-Level Locking / Async-First / Presence Without Co-Editing / Collaboration + Version Branches / AI-Mediated
- **推荐**: variation 1 或 3，因为需要快速交付关闭交易

**Example 3（回顾会议 stale）:**
- **诊断转变**: "会议 format 陈旧" → "输出层损坏"（action items 堆起来没变化）
- **6 个变体**: Fix Output / Kill Meeting / For Quiet Ones / One Question / Retro + Experimentation / Safety First
- **零成本实验**: "第一个 fix 应该花 0 分钟准备、0 美元"

**What to Notice（设计意图总结）:**
1. **重述改变框架**
2. **问题在处方前诊断**
3. **变体有理由**（标注用了什么 lens）
4. **skill 有观点**（"我会推你 toward 1 或 3"）
5. **Phase 2 诚实**（想法被指出低差异化或高复杂度）
6. **产出可执行**
7. **"Not Doing" 做实际工作**
8. **skill 适应上下文**（代码库感知 vs 零成本实验）

**关键洞察:**
- **三个示例覆盖三种典型场景**: 创业（从 0 到 1）、产品功能（从 1 到 N）、流程改进（非产品）——说明 skill 的通用性
- **示例 1 的 Phase 3 最完整**: 其他两个示例只概述 Phase 2-3，说明示例 1 是"黄金标准"
- **"What to Notice" 是元教学**: 不仅展示内容，还教用户如何观察方法论的运用

---

## 整体总结

### 核心概念

| 概念 | 定义 |
|------|------|
| **Divergent-Convergent Thinking** | 双钻模型：先扩展可能性（Phase 1），再聚焦决策（Phase 2），最后交付（Phase 3） |
| **HMW (How Might We)** | 将想法重述为"我们如何能..."格式的问题陈述，强制澄清真正要解决的问题 |
| **Sharpening Questions** | 3-5 个诊断性问题（Who/What/Constraints/History/Why now），Phase 1 的硬性质量门 |
| **Ideation Lenses** | 7 个思维透镜（Inversion/Constraint removal/Audience shift/Combination/Simplification/10x/Expert） |
| **Painkiller vs Vitamin** | 用户价值的根本区分：止痛药（用户主动寻找）vs 维生素（可有可无） |
| **Assumption Audit** | 三级假设分类（Must/Should/Might Be True），未测试假设是想法的头号杀手 |
| **Not Doing List** | 明确命名不做的事及原因，专注的本质是对好想法说不 |

### 工作流程

```
用户触发 skill（带着一个想法）
    │
    ├─ Phase 1: Understand & Expand（发散）
    │   1. 重述为 HMW 问题陈述
    │   2. AskUserQuestion 提出 3-5 sharpening questions
    │      └─ 硬停止：直到理解 Who 和 What success looks like
    │   3. 生成 5-8 个变体（使用 7 个透镜）
    │   4. 如果在代码库中：Glob/Grep/Read 扫描上下文
    │   5. 可选：从 frameworks.md 引入额外框架
    │
    ├─ 等待用户反应（指出共鸣/推回/补充）
    │
    ├─ Phase 2: Evaluate & Converge（收敛）
    │   1. 聚类为 2-3 个不同方向
    │   2. 压力测试（User Value / Feasibility / Differentiation）
    │      └─ 参考 refinement-criteria.md
    │   3. 暴露隐藏假设（赌什么/什么会杀死它/忽略什么）
    │   4. 诚实推回（不是 yes-machine）
    │
    ├─ Phase 3: Sharpen & Ship（交付）
    │   产出 markdown one-pager：
    │   - Problem Statement
    │   - Recommended Direction
    │   - Key Assumptions to Validate（带验证方法）
    │   - MVP Scope
    │   - Not Doing（附原因）
    │   - Open Questions
    │   └─ 用户确认后保存到 docs/ideas/[idea-name].md
    │
    └─ Verification（7 项验收清单）
```

### 关键文件

| 文件 | 作用 |
|------|------|
| `SKILL.md` | 主 skill 文档，定义三阶段流程、哲学、反模式 |
| `frameworks.md` | 扩展框架库（SCAMPER/HMW/First Principles/JTBD/Constraint/Pre-mortem/Analogous）|
| `refinement-criteria.md` | Phase 2 完整评估标准（Painkiller vs Vitamin / 六级 Differentiation / 2x2 决策矩阵 / MVP 原则）|
| `examples.md` | 3 个完整示例（创业概念/产品功能/流程改进）+ 8 个观察要点 |

### 设计亮点

1. **双轨触发**: `idea-refine`（正式）和 `ideate`（口语），降低使用门槛
2. **硬质量门**: "Do NOT proceed until you understand who this is for"——在流程中嵌入停止点
3. **7 个透镜 + 6 个框架**: 主文档提供轻量工具，扩展文件提供重型工具，按需取用
4. **三级假设审计**: Must/Should/Might Be True 的分级让"验证"有了优先级
5. **六级差异化梯度**: 从 New capability（最强）到 Cheaper（最弱），直接指导产品定位
6. **"Not Doing" 的三次强调**: Philosophy 一次、Phase 3 两次，说明作者认为这是最常见的失败模式
7. **诚实推回的语气规范**: "Be honest, not supportive"、"slightly provocative"、"point out when the emperor has no clothes"
8. **代码库感知**: 四处强调在项目中时要扫描现有架构，防止提出空中楼阁的方案
9. **示例的元教学**: examples.md 最后的 "What to Notice" 不仅展示内容，还教用户如何观察方法论
