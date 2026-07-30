# spec 系列去重 + explore-then-ask 流程优化 — 改动思路

日期：2026-07-27
状态：待批准（未动任何源文件）

## 1. 问题

**症状**：同一个需求被问两遍。`/clarify-intent` 访谈确认 intent 后，`/spec` Phase 1 又调 explore-then-ask 把目标、用户、验收标准、边界重问一遍。

**根因**：职责未分层。上游 `refer/agent-skills/commands/spec.toml` 里没有 clarify 阶段，需求澄清本来就住在 `/spec` 内部（命令直接写死 4 个澄清问题）。ys-powers 后来前置了 `/clarify-intent` 作为流程起点，却没有回收 `/spec` 的提问职责。

**重复 prompt 的三处定位**（缺一堵不死）：

| # | 位置 | 内容 |
|---|------|------|
| ① | `commands/spec.md:19-26` | 命令指示调 explore-then-ask 问 4 条问题（2 条需求层 + 2 条实现层） |
| ② | `skills/explore-then-ask/SKILL.md` step 3 | 访谈机器本体：Checklist 项、Process Flow 节点、`### 3` 整节 |
| ③ | `skills/spec-driven-development/SKILL.md:36` | "Ask the human clarifying questions until requirements are concrete"（`/spec` Phase 3 调它时会再次触发） |

**关键约束**：`/spec` 的设计对话不能跟着需求澄清一起砍掉。clarify-intent 的 HARD-RULE 明确「不做具体设计」，技术方案的沟通问问题（选型、约束、trade-off、boundaries、设计分节确认）必须有个家——这个家就是 `/spec`。

## 2. 设计原则

| 层 | 归属 | 问什么 |
|----|------|--------|
| 需求层（what/why） | `/clarify-intent` | 目标、用户、验收标准、约束 —— 全流程只问这一次 |
| 实现层（how） | `/spec` | 技术方案：选型、约束、trade-off、boundaries、设计分节确认 |

explore-then-ask 内容分层（砍之前的判定依据）：

| 内容 | 层级 | 处置 |
|------|------|------|
| spec.md 问题清单 1-2（objective/users、features/验收） | 需求层 | 删 |
| spec.md 问题清单 3-4（tech constraints、boundaries） | 实现层 | 留 |
| skill step 3（Ask clarifying questions until concrete） | 需求层 | 删 |
| skill step 4-5（方案对比、设计分节确认） | 实现层 | 留 |
| skill step 2 的 surface assumptions | 缓冲层 | 留（书面假设清单，残余歧义的安全网） |

## 3. 改动方案

### 3.1 `commands/spec.md`（3 处）

**① Phase 1 重写**

原文（`:5`、`:17-26`）：

```markdown
## Phase 1: Explore and Clarify

Begin by understanding what the user wants to build.

Invoke the **explore-then-ask** skill to ask clarifying questions one at a time (in Chinese) about:

1. The objective and target users
2. Core features and acceptance criteria
3. Tech stack preferences and constraints
4. Known boundaries (what to always do, ask first about, and never do)

Continue through explore-then-ask's full dialogue flow: ...
```

问题："Begin by understanding what the user wants to build" 默认 `/spec` 是理解需求的起点，intent 来源没有交代；第 1-2 条是纯需求层重问；"full dialogue flow" 在 skill 的 step 3 删除后措辞失真。

改为：

```markdown
## Phase 1: Load Intent and Design Dialogue

载入 confirmed intent（需求澄清只发生在 `/clarify-intent`，本命令不重复）：

1. 本会话刚运行过 `/clarify-intent` → 直接使用会话内 confirmed intent
2. 否则从 `docs/ys-powers/intent/` 读取：用户指定了 topic 读对应文件；未指定取最近修改的一份；无法确定则询问用户
3. 目录不存在或没有匹配文档 → 停止，提示用户先运行 `/clarify-intent`

以 confirmed intent 为输入，调用 **explore-then-ask** skill 做实现层设计对话（in Chinese）：

1. Tech stack preferences and constraints
2. Known boundaries (what to always do, ask first about, and never do)

Continue through explore-then-ask's dialogue flow: surface assumptions, propose 2-3 approaches with trade-offs, present design sections, and get user approval.
```

**② Phase 3 加覆盖句**

原文（`:61`）：

```markdown
Invoke the **spec-driven-development** skill to generate a structured spec covering all six core areas: ...
```

问题：该 skill 的 `:36` 自带 "Ask the human clarifying questions until requirements are concrete"，只改 Phase 1 堵不住 Phase 3 的重问。

改为（`:61` 后追加一句）：

```markdown
以 confirmed intent 与已确认的设计方案为输入直接撰写，不重新访谈需求（该 skill 中 "ask clarifying questions" 的指引在此不适用）；仍不确定的点写入 spec 的 Open Questions 段。
```

skill 本体不动：它可独立用于无 clarify 前置的场景，泛化指令保留，命令层覆盖（与上游 spec.toml 用 4 个问题限定 skill 泛化指令是同一 overlay 模式）。Open Questions 段真实存在于该 skill（`:113`），残余歧义有正式出口。

**③ frontmatter description**

原文：`Start spec-driven development — explore context, clarify requirements, prepare workspace, then write spec`

问题："clarify requirements" 宣称了本命令不再承担的职责。

改为：`Start spec-driven development — load confirmed intent, discuss implementation design, prepare workspace, then write spec`

### 3.2 `skills/explore-then-ask/SKILL.md`（4 处）

**④ 删 step 3 三处一体 + 重编号**

原文三处互为呼应，必须同删（只删一处，另外两处仍在指示提问）：

- Checklist（`:41-42`）：`3. **Ask clarifying questions** — one at a time, understand purpose/constraints/success criteria` 及其子项
- Process Flow（`:55-57`）：`Ask clarifying questions (one at a time)` 节点
- 正文（`:100-107`）：`### 3. Ask Clarifying Questions` 整节（含 "Continue until requirements are concrete"）

问题：这是重问需求的引擎本体，"until requirements are concrete" 与 `/clarify-intent` 的 95% 置信度收敛同义。

改为：三处全删；Checklist 4→3、5→4 重编号；正文 `### 4`→`### 3`（开头改为 "Based on the confirmed requirements, propose different approaches with trade-offs."）、`### 5`→`### 4`。

提问的**行为**不消失，只换对象：分布在 `### 3`（conversationally 给选项）和 `### 4`（逐节问 looks right），问的从需求变成方案。

**⑤ Overview / description 重锚定**

原文：

```
description: Explore project context and clarify requirements through structured dialogue. A self-contained behavioral skill for context-first design clarification — primarily dialogue; no browser, no implementation handoff. May write to a user-specified document path.
```

```markdown
Turn vague ideas into clarified designs through natural collaborative dialogue.

Start by understanding the current project context, then ask questions one at a time to refine the idea. Once you understand what you're building, present 2-3 approaches with trade-offs, then present the design in sections and get user approval.
```

问题：skill 是 model-invoked，会脱离 `/spec` 被自动触发单飞；契约层仍写 "clarify requirements"、"vague ideas"，光删 step 3，单飞时重问从契约里复活。这是不能只改 spec.md 的原因。

改为：

```
description: Explore project context and turn confirmed requirements into an approved design through structured dialogue — propose approaches with trade-offs, present design sections. No requirement re-clarification; no implementation handoff. May write to a user-specified document path.
```

```markdown
Turn confirmed requirements into an approved design through natural collaborative dialogue.

Start from a confirmed intent (typically produced by `/clarify-intent`). Understand the current project context, propose 2-3 approaches with trade-offs, then present the design in sections and get user approval.

需求还没确认（要什么、为什么、验收标准不清楚）→ 先去 `/clarify-intent`，本 skill 不做需求澄清。
```

**⑥ 残留词修正**

原文（`:88-89`）："Before asking detailed questions, assess scope"；"then explore-and-clarify the first one"。

问题：step 3 死后 "detailed questions" 失去指代；"explore-and-clarify" 是旧词汇残留。

改为："Before proposing approaches, assess scope"；"then explore-and-design the first one"。

**⑦ 不加新句**

决定：Overview 不追加「提问围绕技术方案」类总纲句。

逻辑：description 已有 "No requirement re-clarification"，Overview 已有重定向句，提问行为已在 `### 3/4` 兑现——再加一句不改变任何行为，通不过 no-op 测试。

## 4. 不动的部分及理由

| 内容 | 理由 |
|------|------|
| `skills/spec-driven-development/SKILL.md` 本体 | 可独立用于无 clarify 前置的场景；命令层覆盖即可 |
| skill 的 ASSUMPTIONS 机制（surface assumptions） | 书面假设清单，不是访谈，是残余歧义的安全网 |
| "go back and clarify" ×3（`### 3/4`、Key Principles） | 设计层往返，非需求层系统访谈 |
| Key Principles「一次一问 / 多选题」 | 设计对话仍在用；`wskill.md:15` 借用此原则，删了指针死 |
| Anti-Pattern 节（"too simple to need a design"） | 流程层规则：进入本 skill 后不许拿"简单"当借口跳过设计呈现 |
| `docs/codebase/power-dependencies.md` | `spec --> explore` 边仍成立（调用保留，只是重新限定任务） |

## 5. 已否备选

- **方案 A：`/spec` 整个不再调 explore-then-ask** —— 误删技术方案对话，spec 变成 agent 闷头写、用户只能事后 review 文档，丢了事前对齐关口。
- **方案 B：只改 spec.md、skill 本体不动** —— skill 单飞时契约仍写 "clarify requirements"，重问行为在别处复活。

## 6. 已知代价

- 被删的 "Challenge fuzzy language" 子项（挑战模糊措辞）在 skill 内无承接——接受：术语打磨由 `/spec` Phase 1.5 的 domain-modeling checkpoint 显式承担，需求措辞挑战由 interview-me 在澄清阶段承担。
- 新会话直接 `/spec`（无 intent）会被重定向——接受：这是「需求只问一次」的强制保证。

## 7. 验证

`make global-install` + 新会话：

1. `/clarify-intent` 确认一个需求 → `/spec`：不重问需求，只聊技术方案
2. 新会话直接 `/spec` 且无 intent 文档：正确重定向到 `/clarify-intent`
3. 新会话 `/spec <topic>` 且有对应 intent 文档：从文档载入开工

## 8. 明确不做（另一条线）

invocation 治理（disable-model-invocation）、commands 物理迁移、README 同步。
