# interview-me Skill 逐段精读分析

## 分析概要

### 文档定位
这是一份 **agent skill 文档**，定义了 `interview-me`（意图挖掘）的方法论，属于 `agent-skills` 框架中 Define 阶段的**前置步骤**——在 `idea-refine`、`spec-driven-development` 甚至 `doubt-driven-development` 之前执行。

### 核心主张
**"人们要求的和他们真正想要的不是一回事"** — 通过一次一个问题的结构化访谈，把用户真实意图从" convention 驱动的表层需求"中挖出来，在写任何 spec 之前就消除歧义。

### 结构骨架

| 章节 | 内容 |
|------|------|
| Overview + When to Use | Skill 定位、使用时机、显式排除场景 |
| Loading Constraints | 仅适用于交互式会话，禁止在 CI/loop 中使用 |
| The Process (5 Steps) | 假设→提问→倾听→重述→确认 |
| The 95% Confidence Stop | 可检查的停止条件，不是 vibe |
| Output | 产物定义：confirmed statement of intent |
| Example | 对比：有/无 interview-me 的前后差异 |
| Interaction with Other Skills | 与 idea-refine / spec / plan / doubt-driven 的衔接关系 |
| Common Rationalizations | 反驳"问题已经足够清晰"的借口 |
| Red Flags | 危险信号：batch 提问、无假设、接受"whatever you think" |
| Verification | 执行后的验收清单 |

### 关键洞察

1. ** cheapest moment to find the gap is before any plan, spec, or code exists** — 一旦开始编码，切换成本是 10 倍
2. **"Out of scope" line is non-negotiable** — 一半的错位来自对"不做什么"的沉默分歧
3. **Confidence number forces honesty** — 数字比 vibe 更难伪装，低于 70% 必须附原因
4. **Guess attached to question is a feature, not a bug** — 用户对一个错误猜测的反应速度远快于从零生成答案

---

## 逐段精读

### 段落 1: Frontmatter

**原文:**
```yaml
---
name: interview-me
description: Extracts what the user actually wants instead of what they think they should want. Achieves this through one-question-at-a-time interview until ~95% confidence about the underlying intent. Use when an ask is underspecified ("build me X" without "for whom" or "why now"), when the user explicitly invokes ("interview me", "grill me", "are we sure?", "stress-test my thinking"), or when you catch yourself silently filling in ambiguous requirements before any plan, spec, or code exists.
---
```

**翻译:**
```yaml
---
name: interview-me
description: 挖掘用户真正想要的，而非他们认为应该想要的。通过一次一个问题的访谈达到 ~95% 的意图置信度。在请求欠指定时（"给我做个 X"但没有说明"给谁做"或"为什么现在做"）、用户显式调用时（"interview me"、"grill me"、"are we sure?"、"stress-test my thinking"），或当你发现自己正在沉默地填充模糊需求时使用。
---
```

**要点:**
- **触发条件三重门**：(1) 请求欠指定 (2) 用户显式调用 (3) 模型自己发现正在做假设填充
- **触发词非常丰富**：不只是 "interview me"，还有 "grill me"、"stress-test my thinking" 等口语化表达
- **95% 是量化指标**：不是"感觉差不多了"，而是可检查的测试标准

---

### 段落 2: Overview

**原文核心:**
> What people ask for and what they actually want are different things. They ask for "a dashboard" because that's what one asks for, not because a dashboard solves their problem.

> The cheapest moment to find this gap is before any plan, spec, or code exists. Once you've started building, switching costs are real, and the user will rationalize the wrong thing into a "good enough" thing.

**要点:**
- **"Dashboard" 是典型的 convention-driven 请求** — 用户说"dashboard"是因为这是 convention，不是因为 dashboard 解决了他们的问题
- **Switching costs are real** — 编码开始后的切换成本是真实的，而且用户会把错误的东西 rationalize 成"good enough"
- **与下游 skill 的关系明确**：idea-refine 生成变体、spec-driven 写需求、doubt-driven 审查计划，interview-me 在它们全部之前

---

### 段落 3: The Process — Step 1 (Hypothesize)

**原文核心:**
```
HYPOTHESIS: You want a way to answer "how are we doing?" in standup, and "dashboard" was the convention that came to mind.
CONFIDENCE: ~30% — missing: who it's for, what "metrics" means in context, and what success looks like
```

**要点:**
- **必须先写假设再提问** — 不能跳过这一步直接问"你想要什么"
- **Confidence number 是硬性要求** — 0-100%，如果写高了但无法预测用户下三个反应，数字就是错的
- **低于 70% 必须附原因** — 告诉用户"还缺什么"，让访谈有明确方向

---

### 段落 4: The Process — Step 2 (One question at a time)

**原文核心:**
```
Q: <one focused question>
GUESS: <your hypothesis for the answer, with the reasoning that produced it>
```

**要点:**
- **为什么一次只问一个**：(1) 用户无法对 buried hypotheses 反应 (2) batch 鼓励 skim-reading (3) 第三个问题通常依赖第一个答案 (4) 用户精力有限
- **为什么 attach guess**：(1) 用户对错误猜测反应更快 (2) 迫使自己诚实 (3) 暴露自己的假设
- **风险：sycophancy（谄媚）** — 礼貌用户可能同意你的猜测来讨好你；mitigation 是 visibly willing to be wrong

---

### 段落 5: The Process — Step 3 (Listen for "want vs. should want")

**原文核心:**
> Watch for: answers that pattern-match best-practice talk ("I want it to be scalable", "clean architecture") without specifics... Phrases like "I should probably…", "I think I'm supposed to…"

> When you hear these, the question to ask is: "If you didn't have to justify this to anyone, what would you actually want?"

**要点:**
- **最危险的答案**：听起来像" thoughtful answer "但实际上不是用户真正想要的
- **关键探针**："If you didn't have to justify this to anyone..." — 这句话 often does more work than the previous five
- **Buzzwords as goals**：当"modern"、"scalable"、"robust"是答案而不是具体 outcome 时

---

### 段落 6: The Process — Step 4 (Restate)

**原文核心:**
```
Here's what I now think you want:

- Outcome:      <one line>
- User:         <one line — who benefits>
- Why now:      <one line — what changed>
- Success:      <one line — how we know it worked>
- Constraint:   <one line — the binding limit>
- Out of scope: <one line — what we're explicitly not doing>

Yes / no / refine?
```

**要点:**
- **模板六要素**：Outcome / User / Why now / Success / Constraint / Out of scope
- **Out of scope 是非谈判条款** — "Half of misalignment is silent disagreement about what is not being built"
- **Yes / no / refine?** — 给用户明确的回应选项

---

### 段落 7: The Process — Step 5 (Confirm)

**原文核心:**
> The gate is an explicit "yes." The following are NOT yes:
> - "Whatever you think is best." → delegation, not decision
> - "Sounds good." → ambiguous
> - "Sure, let's go." → polite exit
> - Silence followed by "okay let's start." → user has given up

**要点:**
- **"Whatever you think is best" 是 delegation** — 用户没有 95% 信心，应该 re-ask with two concrete options
- **如果用户纠正你**：fold the correction in and restate，loop until explicit yes
- **Hollow yes**：如果 yes 跟随 vague restate 或 open-ended "sounds good"，yes 是空的

---

### 段落 8: The 95% Confidence Stop

**原文核心:**
> You're done when you can answer yes to this: Can I predict the user's reaction to the next three questions I would ask?

> This is a checkable test, not a vibe.

**要点:**
- **可检查的停止条件**：能预测用户对下三个问题的反应 = 共享理解达成
- **Floor**：如果多轮后仍无法预测，说明"something foundational is missing"，应该 stop and escalate
- **不是 vibe**：明确区别于"感觉聊得差不多了"

---

### 段落 9: Interaction with Other Skills

**原文核心:**
| Skill | 关系 |
|-------|------|
| idea-refine | downstream — 确认意图后如果 scope 仍模糊，交给 idea-refine 生成变体 |
| spec-driven-development | downstream — 意图 concrete 后交给 spec |
| planning-and-task-breakdown | two hops downstream (after spec) |
| doubt-driven-development | opposite end — interview-me 是 pre-decision，ddt 是 post-decision |
| source-driven-development | orthogonal — interview-me 澄清 wants，SDD 验证 framework facts |

**要点:**
- **明确的 handoff 关系**：不是替代下游 skill，而是为它们提供 confirmed intent
- **与 doubt-driven 的 timeline 对比**：两者都 catch divergence，但在不同时间点

---

## 与 ys-powers 现有 workflow 的对比

### 当前 ys-powers 链路
```
/spec (explore-then-ask → spec-driven-development) → /plan → /build
```

`/spec` 的 Phase 1 已经包含 explore-then-ask，会 ask clarifying questions about objective/target users/core features/constraints。

### interview-me 的差异

| 维度 | /spec 中的 explore-then-ask | interview-me |
|------|---------------------------|--------------|
| **时机** | 在 /spec 命令内部，用户已表达要做某事 | 在一切之前，甚至可能在用户没想清楚时 |
| **目标** | 澄清需求以写 spec | 挖掘真实意图，可能发现"要做的不是 dashboard 而是 list" |
| **格式** | 多问题 batch（explore-then-ask 的 Phase 3 可以一次问多个）| **严格一次一个**，每个带 guess |
| **停止条件** | 用户批准设计 | **95% confidence + explicit yes** |
| **产物** | spec 文档 | confirmed statement of intent（6 要素模板）|
| **深度** | 问"做什么" | 问"为什么做、给谁做、成功什么样" |

### 关键差异

**interview-me 比 explore-then-ask 更前置、更深度**：
- explore-then-ask 假设用户"大致知道想要什么，需要澄清细节"
- interview-me 假设用户"可能不知道真正想要什么，需要挖掘"

**两者的冲突点**：
- 如果 /spec 命令执行时，模型已经加载了 interview-me skill，可能在 Phase 1 试图插入 interview-me 流程
- 但由于 /spec 有 HARD-RULE 显式要求 explore-then-ask，优先级上命令应胜出

---

## 同步决策

### 已同步内容
- `skills/interview-me/SKILL.md` — 完整搬运，已加入 ys-powers skill 集
- `skills/using-agent-skills/SKILL.md` — 决策树已新增 interview-me 入口
- 路径本地化：`docs/intent/` → `docs/ys-powers/intent/`

### 与现有 workflow 的衔接建议

**选项 A：替换 explore-then-ask（不推荐）**
- 在 /spec 命令中把 explore-then-ask 替换为 interview-me
- 风险：interview-me 更深度，可能让简单任务变重

**选项 B：前置 interview-me（推荐）**
- 在 /spec 之前增加一个可选的 interview-me 阶段
- 触发条件：当用户请求欠指定时（如"build me a dashboard"）
- 完成后 hand off 到 /spec

**选项 C：保持并行（当前状态）**
- interview-me 作为独立 skill 存在，用户显式调用
- /spec 继续使用 explore-then-ask
- 风险：两个 skill 可能有重叠，但用户选择权更大

### 建议
采用 **选项 C（当前状态）**，但考虑在 `using-agent-skills` 的决策树中明确标注：
- "Don't know what you want yet? → interview-me" — 用于意图完全模糊时
- "Have a rough concept, need variants? → idea-refine" — 用于有概念但需要扩展
- "New project/feature/change? → spec-driven-development" — 用于意图已清晰

这样三条路径互不重叠，用户根据"清晰度"选择入口。

---

## Red Flags（执行 interview-me 时的危险信号）

| 危险信号 | 含义 |
|---------|------|
| 一次消息中三个以上问题 | Batching，不是 interviewing |
| 问题没有附带假设 | Surveying，不是 committing |
| 接受 "whatever you think is best" | 用户 delegate，不是 decide |
| 在确认 restate 前就产 spec/plan/task | 跳过了 gate |
| 用户给 sophistication-signaling 答案（"scalable"、"clean"）且未 probe | 接受了表层答案 |
| 三轮后 confidence 未上升 | 问错了问题，需要 reframe |
| Confidence < 70% 但没有附原因 | 用户无法帮助 close gap |
| 跳过 "Out of scope" | 一半的错位来自非目标沉默分歧 |

---

## Verification（执行后的验收清单）

- [ ] 首 turn 有显式假设 + confidence number
- [ ] < 70% 的 confidence 有一行原因
- [ ] 问题一次一个，每个带 guess
- [ ] 至少有一次 "what would you actually want?" probe
- [ ]  Concrete restate（6 要素）写回用户
- [ ] 用户用 explicit yes 确认（不是 "whatever" / "sounds good" / silence）
- [ ] 停止时 agent 能预测下三个问题的反应
- [ ] Handoff 到下游 skill 时用 confirmed intent 而非原始欠指定请求
