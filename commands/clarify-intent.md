---
description: 先读项目上下文，再调用 interview-me 澄清真实意图，允许访谈中动态查询项目，输出确认的 intent
argument-hint: [topic]
disable-model-invocation: true
---

## 本命令在整体工作流中的位置

`/clarify-intent` 是 ys-powers 开发流程的起点，只负责**确认真实意图**，不写代码、不做设计。

```
CLARIFY ──→ SPECIFY ──→ [REVIEW] ──→ [PLAN] ──→ BUILD ──→ [TEST] ──→ REVIEW ──→ SHIP
   │           │            │            │          │          │          │         │
   ▼           ▼            ▼            ▼          ▼          ▼          ▼         ▼
 Human      Human        Human        Human      Human      Human      Human     Human
 confirms   writes       reviews      reviews    implements explicit   reviews    decides
 intent     spec         spec         plan       + tests    TDD /      code       ship
                                                  per task   bug
                                                             repro

fast path（用户明确选择跳过 SPECIFY / PLAN 时）：
CLARIFY ──→ 直接实现 ──→ REVIEW ──→ SHIP
```

- **CLARIFY**（本命令）：产出确认的 intent 陈述。
- **SPECIFY**：`/spec`，写结构化设计文档。
- **[REVIEW]**：可选 `/review-spec`，对 spec 做六维度质量审查。
- **[PLAN]**：可选 `/plan`，把 spec 拆成可执行任务。小改动可在 spec 中直接带过。
- **BUILD**：`/build`，按任务逐个实现；每个任务内部已经走「写测试 → 实现 → 跑全量测试」的循环。
- **[TEST]**：可选 `/test`，仅在以下情况单独调用：修 bug 时先写失败测试（Prove-It 模式）、需要专门补全边界/异常/并发测试、用户明确要求显式 TDD。
- **REVIEW**：`/ys-review`，五维度代码审查。
- **SHIP**：`/ship`，交付前检查与 go/no-go 决策。

**本命令出口标准**：用户明确确认 intent 陈述（明确的 "yes"，不是 "sounds good"）。

<HARD-RULE name="clarify-intent-no-implementation">

- 本命令只读 + 只产出确认的意图陈述
- 不写代码、不创建 scaffold、不生成 task list、不做具体设计
- 保存意图文档是唯一的写操作，且必须用户确认

</HARD-RULE>

## Phase 1: 读取项目上下文（只读 3 项，避免深 explore）

先快速扫描项目，建立足够提问的背景知识。不要读太深——目标是「避免愚蠢问题」，不是「提前做设计」。

如果用户传了 `[topic]` 参数，优先读取与该 topic 相关的目录和文件。

读取范围（控制在 3 项直读，避免深 explore）：

1. 项目根目录的 `README.md`、`CLAUDE.md`、`CONTEXT.md`（直接读，不作深 explore）
2. 最近的 5-10 条 git commit message（不看 diff）
3. 目录结构（只扫与 `[topic]` 直接相关的子目录树，不读文件）

**Phase 1 不读 `docs/adr/` 与 `docs/ys-powers/intent/`，这是故意的。**

读得太早会拿既有词汇束缚用户真实意图。三步时序分清：

- Phase 1（这里）：冷启动，只防蠢问题
- interview-me Step 1.5：访谈中遇到「该不该问」的项目事实再查
- Phase 3：意图确认后，用 ADR / CONTEXT.md 做一次 consistency check

读取后，用 3-5 句话向用户总结你读到的关键上下文：

```text
我从项目上下文中看到：
1. ...
2. ...
→ 如果以上有理解错误，请直接纠正。
```

## Phase 2: 上下文化访谈（产出 confirmed intent）

调用 **interview-me** skill，并叠加以下额外约束：

- 问题和猜测必须基于 Phase 1 加载的项目上下文
- 如果某个问题或猜测依赖尚未确认的项目事实（例如某个表/服务/页面是否存在、现有实现细节），**暂停提问，先查询项目**，然后把查到的事实带回访谈
- **只查询对下一个问题/猜测有决定性影响的事实**；不要为了"更了解项目"而查询
- 查询前简短告知用户：

```text
你提到的「X」让我想确认一下项目里的现状，我先快速查一下。
```

- 查到的项目事实只用于优化问题，**不用于替用户做设计决定**

继续通过 interview-me 的完整流程：提出假设、一次一问、附带猜测、95% 置信度停止、重述意图并确认。

## Phase 3: 上下文交叉检查（验证 confirmed intent）

基于已确认的意图，快速检查以下项目事实：

- [ ] 与 outcome 直接相关的 1-2 个核心文件/表/服务是否存在
- [ ] 约束条件提到的技术栈/工具在项目中是否已配置
- [ ] 明确不做的 out-of-scope 项是否已被部分实现（如果是，说明 scope 理解可能有偏差）

如果发现冲突，把冲突点作为补充问题抛回给用户，重新确认后再进入下一步。

## Phase 4: 出口路由

路由完全由用户决定，不评估、不推荐：

1. 用户已明确要求直接实现（"直接开干"、"不用写 spec"、"快速实现" 等）→ 免问，走 fast path
2. 否则，问一句：「接下来走 fast path 还是 `/spec`？」等用户回答后再继续

fast path → 本命令结束，本会话直接实现（不调 `/build`，照常写测试并跑全量测试）；`/spec` → 继续 Phase 5。

## Phase 5: 保存意图文档（可选）

如果用户希望持久化或交接，询问是否保存到：

```text
docs/ys-powers/intent/<topic>.md
```

其中 `<topic>` 优先使用用户传入的 `[topic]` 参数；若未传，则从确认意图中提炼 kebab-case 短名。仅当用户明确确认后才保存。

## Phase 6: 沉淀到领域语言（可选追加）

intent 文档保存之后，若意图满足以下任一条件，询问用户是否叠加 `/domain-modeling`：

- 新引入概念 / 词汇
- 跨模块语义变化
- 架构选型决策

`/domain-modeling` 产出的三选一：

- 更新 `CONTEXT.md` 的 ubiquitous language
- 新增 ADR 到 `docs/adr/`
- 写 glossary entry

仅当用户明确要求时执行。

**澄清意图本身不写 `CONTEXT.md` / ADR**——那些 artefact 应该是意图**确认后**才留痕。`/domain-modeling` 是把意图**翻译**到领域语言，不是给 intent 加设计。

## Failure Modes

- **interview-me 无法收敛** — 如果多轮访谈后置信度仍低于 70%，停止并告诉用户：
  > "目前信息不足以确认意图。建议先补充 [具体缺失项]，再重新启动 /clarify-intent。"
- **项目事实与意图冲突** — 在 Phase 3 发现现有代码/文档明确否定用户想要的 outcome 时，不要直接放弃，把冲突点作为补充问题抛回用户确认。
- **用户拒绝回答关键问题** — 记录缺失项，基于已有信息给出最可能的 confirmed intent，并明确标注未确认部分。
- **项目过大无法快速读完** — 只读与 `[topic]` 最相关的 2-3 个目录，并在总结中告诉用户"我只读了 X、Y，可能遗漏其他相关上下文"。
- **用户中途改变话题** — 如果用户明显偏离最初问题，暂停并确认："你刚才的回答转向了 Z，我们是继续聊 Z，还是回到原来的 X？"
- **项目上下文与 `CLAUDE.md` / `CONTEXT.md` 矛盾** — 以代码/文件事实为准，同时向用户指出矛盾点。

## 示例

用户输入：`/clarify-intent dashboard`

**Phase 1 总结：**

```text
我从项目上下文中看到：
1. 项目用 Next.js
2. 已有 `/app/metrics` 页面和 `Metric` 表
→ 如果以上有理解错误，请直接纠正。
```

**Phase 2 提问：**

```text
Q: 你说的 dashboard 是要扩展现有 `/app/metrics`，还是做新的视图？
GUESS: 做新视图，因为你提到的是"加"而不是"改"。
```
