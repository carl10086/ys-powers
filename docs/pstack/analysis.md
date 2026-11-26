# Cursor 官方 pstack 当前版本分析

> **Decision update（2026-11-26）**：本文是筛选阶段的研究结论，不是当前 active manifest。后续逐项实验已 Promotion `why`、`how` 与 `bro`，并 Experimental Promotion `teach` 与 `unslop`；`teach` 的跨 runtime 风险见 [`invocation-semantics.md`](./invocation-semantics.md) 和 [wayfinder map](https://github.com/carl10086/ys-powers/issues/106)。

## 结论先行

pstack 的价值不在于 59 个 skill 的数量，而在于一套可组合的控制结构：`poteto-mode` 只负责匹配 playbook；playbook 给任务提供顺序和完成条件；principle 在触发点改变具体决策；model role 决定由谁执行；verification 决定什么才算完成；隔离、聚合和复验让 parallelism 不至于放大错误。官方把它概括为“go deep first”与“fearless parallelism”，并明确反对以 LOC 或纯 throughput 为目标。[README](https://github.com/cursor/plugins/blob/main/pstack/README.md)

对 ys-powers 的判断是：**不要整体引入 pstack，也不要增加第二个 router。** 当前 `grill-with-docs → to-spec → to-tickets → implement → code-review` 仍应是唯一 Matt-first 主链。pstack 最值得研究的是几条很小、可独立验证的内核：history-first 的 `why`、以“一个安全事实”为中心的 `blast-radius`、只保留可复现 finding 的 `interrogate`、benchmark validity checklist，以及把重复纠正下沉为结构约束的 `correct`。正式 verification skill 与 formal verification 只适合在有明确目标项目时做有界 eval。

另一个重要判断来自官方自身的演进，而不是我的偏好。2026-11-14 的 [commit `bf0c7cd`](https://github.com/cursor/plugins/commit/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7) / [PR #1236](https://github.com/cursor/plugins/pull/1236) 把 `why` 的 investigators、synthesizer、model routing、输出模板与 12 个 reference files 删除，把 `how` 的 complexity gate、2–4 个 explorers、synthesizer 与两个 prompt templates 删除。当前 `why` 只有一个 48-word body，`how` 只有“一个 read-only subagent + present”。`poteto-mode` 也不再自动 route 到 `how`，由各 playbook 直接 trace code。**当前官方设计判断是保留强契约、删除重型编排。** 分析或借鉴时不应把旧版复杂流程当成当前最佳实践。

## 范围、版本与可复核基线

本文只分析 `cursor/plugins` 官方仓库中的 `pstack/`，不使用任何 fork 作为事实来源。

| 项目 | 当前样本 |
|---|---|
| 官方仓库 | [`cursor/plugins`](https://github.com/cursor/plugins) |
| 本地仓库快照 `HEAD` | [`41e400932eca14f289e7db717a70455256b6d388`](https://github.com/cursor/plugins/commit/41e400932eca14f289e7db717a70455256b6d388) |
| 最近一次改动 `pstack/` 的 commit | [`9e278fe4d4ecd8bfe98b1b79bf4be662efb338cc`](https://github.com/cursor/plugins/commit/9e278fe4d4ecd8bfe98b1b79bf4be662efb338cc)，2026-11-23，`feat(pstack): have /reframe list the problems a vague description could be (#1326)` |
| plugin version | `0.15.48`，author `Lauren Tan`，[manifest](https://github.com/cursor/plugins/blob/main/pstack/.cursor-plugin/plugin.json) |
| license | MIT，Copyright © 2026 Lauren Tan，[LICENSE](https://github.com/cursor/plugins/blob/main/pstack/LICENSE) |

这里同时记录 repository `HEAD` 与 `pstack/` 的 last-touch commit，避免把“仓库当前 commit”和“pstack 最近改动”混成一个值。

### 目录与数量

官方 Cursor manifest 把 `./skills/` 与 `./agents/` 注册为 plugin 内容；兼容 manifest 另以 Agent Plugins schema 描述同一 package。[Cursor manifest](https://github.com/cursor/plugins/blob/main/pstack/.cursor-plugin/plugin.json) · [compatibility manifest](https://github.com/cursor/plugins/blob/main/pstack/plugin.json)

当前源码的主要构成如下：

- `skills/`：59 个顶层 skill directory，59 个 `SKILL.md`。其中 24 个为 `principle-*`。
- `skills/poteto-mode/playbooks/`：22 个 playbook。官方 README 逐项列出这 22 个入口。[README: playbooks](https://github.com/cursor/plugins/blob/main/pstack/README.md#just-use-poteto-mode)
- `agents/`：2 个 agent，`poteto-agent` 与 read-only 的 `comment-sicko`。[poteto-agent](https://github.com/cursor/plugins/blob/main/pstack/agents/poteto-agent.md)
- `docs/guide/`：guide index 加 10 个章节；`docs/harness/` 提供 Claude Code adapter。
- `automations/benny/`：3 个 automation-local skills 与 templates。它默认 dormant，不注册为 slash skills，而且依赖 Cursor Automations，所以是 Cursor-only。[README: automations](https://github.com/cursor/plugins/blob/main/pstack/README.md#automations)
- `assets/` 与两个 plugin manifests；整个 `pstack/` 快照共 554 个 files，其中大量文件属于 `statechart` 的 scripts 与 test corpus。文件数不是 59 个 skill 的复杂度代理。

### Cursor 与 Claude Code runtime 边界

**源码事实：Cursor 是原生 runtime。** `poteto-mode` 可以作为 Cursor Custom Mode 跨 turn 保持；playbooks 使用 Cursor todo、`Task`、cloud subagent、Bugbot、`/loop`、built-in PR 能力与 Automations。Cursor model role 写入 `~/.cursor/rules/pstack-models.mdc`。[poteto-mode](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md) · [setup-pstack](https://github.com/cursor/plugins/blob/main/pstack/skills/setup-pstack/SKILL.md) · [setup guide](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/01-setup.md)

**源码事实：Claude Code 是 adapter runtime，而不是另一套 prompt。** 官方 adapter 把 `Task` 映射到 `Agent`、Cursor model slug 映射到 Claude model/effort、`.cursor/skills/` 映射到 `.claude/skills/`，并把 model rule 写到 `~/.claude/rules/pstack-models.md`。Claude Code 没有 Cursor Automations、Bugbot 启动能力、Cursor cloud-agent dashboard 或 built-in PR tool；遇到这些步骤时必须明确 `Skipped in Claude Code` 后继续。官方还说明 Claude Code 安装的是从 repository-root `harness/pstack/` 生成的 copy，CI 检查 generated tree 是否同步。[Claude Code adapter](https://github.com/cursor/plugins/blob/main/pstack/docs/harness/claude-code.md) · [README: Claude Code](https://github.com/cursor/plugins/blob/main/pstack/README.md#install)

**分析建议：** prompt-only contract 通常可跨 runtime；涉及 model slug、Cursor rules、cloud worktree、Bugbot、Automations、transcript path、`.cursor/skills/` 输出位置或 `statechart` toolchain 的流程不可直接复制。ys-powers 若做 eval，应只测内核行为，不应先移植 adapter 或 model router。

## 设计哲学：六层怎样组合

### 1. `poteto-mode` 是薄 router，不是包办所有工作的超级 skill

收到任务后，`poteto-mode` 先读取内嵌 principle index，再匹配一个 playbook，并把 playbook steps 原样放入 todo；真正的 trace、设计、实现和验证由 playbook 与被调用 skill 完成。[poteto-mode](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md) · [guide: routing](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/02-poteto-mode.md)

它的 110 行主要是全局 invariants，而不是任务细节：首条消息重述目标；fork 能通过运行 settle 就 prototype；跨函数边界触发 `architect`；fan-out 用 `swarm`；bakeoff 用 `arena`；测量数字必须过 `benchmark-checklist`；完成前验证真实 artifact。也就是说，mode 负责“何时切换协议”，不负责把每个协议展开在同一 prompt 中。[poteto-mode](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md)

这正是它与 Matt-first 的根本冲突点。ys-powers 当前主链要求每一步由用户或 agent 根据产物显式选择，不自动串成流水线。引入 `poteto-mode` 会形成第二套入口、第二套路由语义与第二套完成定义，而不是补一个缺失能力。

### 2. playbook 是可审计的 task protocol

22 个 playbook 不是简单 inventory。它们把不同任务的 epistemic order 固定下来：

- Investigation 只读，先 trace code，动机问题才加 `why`，最后给 cited explanation 或 tradeoff recommendation。[Investigation](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/investigation.md)
- Bug fix 先在真实 surface 复现，再 binary-search hypotheses，用 runtime evidence 确认 mechanism，跨 boundary 才 `architect`，最后在同一 surface 验证；无法证明的 belt-and-suspenders change 不得 ship。[Bug fix](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/bug-fix.md)
- Eval 把 candidate prompt、路径、文件名与 judge label 都 blind 化；同一 organic prompt 并行运行；judge 不知道 model；最后从 transcript 与 artifact 判断，而不是听 agent 自报。[Eval](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/eval.md)

因此 playbook 的作用是防止顺序错误。例如先抽象设计再复现，会把 bug hypothesis 变成设计前提；先看 rubric 再答题，会让 skill eval 只测 compliance；先开并行 worker 再定义 isolation，会让 throughput 变成共享状态冲突。

### 3. principles 是触发式 decision vocabulary

24 个 principle 分为 Core、Architecture、Verification、Delegation、Meta。`poteto-mode` 只内嵌 index；真正应用某条 principle 时必须读取 leaf skill，并在回复中说明“哪条 principle 改变了哪个具体 decision”。仅报名字不算应用。[poteto-mode: Principles](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md#principles) · [principles guide](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/08-principles.md)

这种设计有两个作用：

1. 短名字让 operator 可以低成本纠偏，例如 `prove it works` 指向真实 artifact，而不是“再多跑几个 test”。
2. leaf-on-trigger 避免把 24 份全文永久塞进 context。index 用来识别触发点，leaf 提供完整约束。

风险也很清楚：名称可能成为没有行为变化的 ritual。官方用“必须指出改变的 decision”抑制这个问题，但无法完全消除 self-report 偏差。

### 4. model roles 把 policy 与 task protocol 分开

`setup-pstack` 当前配置 9 条 role：`feature, refactoring`、`bug-fix`、`perf-issue`、`hillclimb`、`judgment and prose`、`arena runners`、`arena cross-judge pool`、`swarm workers`、`interrogate reviewers`。默认 code/prose/judgment 是 Opus 5.5 xhigh，panel 与 swarm 通常是 high；panel 默认跨 Fable、Opus、Gemini。`inherit-parent` / `auto` 表示省略 model field，而不是 model slug。[setup-pstack](https://github.com/cursor/plugins/blob/main/pstack/skills/setup-pstack/SKILL.md)

其合理之处是：skill contract 描述要做什么，role config 描述由哪个 model、多少 reasoning 执行。多模型被限制在 design/review panel 等需要 diversity 的位置，而不是每一步都 fan out。官方同时明确这是 token 成本，并建议缩短 panel、降低 budget、只在需要 rigor 时使用 mode。[setup guide](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/01-setup.md#keep-the-cost-in-check)

对 ys-powers 而言，这层不应借鉴。OMP 已有自己的 agent 类型、model policy 与 delegation contract；再写一份 pstack role file 只会产生互相漂移的 runtime policy。

### 5. verification 不是末尾测试，而是可执行的完成定义

pstack 的 verification 有四个层次：

1. `prove-it-works`：检查真实 command、flow、stored value、profile，而不是“it compiles”。
2. playbook 内的 same-surface repro、failing-then-passing evidence 与 benchmark validity。
3. `create-verification-skill`：从 repo 推导 Launch / Doctor / Drive / Evidence / Cleanup，加 feature map，并在交付前完整运行一次。[create-verification-skill](https://github.com/cursor/plugins/blob/main/pstack/skills/create-verification-skill/SKILL.md)
4. formal verification：在 tests 难以覆盖且失败代价高的地方选一个 property，按问题选 model checker、code verifier 或 proof，并记录 bounds、assumptions、covered code 与 sync commit。[create-formal-verification-skill](https://github.com/cursor/plugins/blob/main/pstack/skills/create-formal-verification-skill/SKILL.md)

这使 verification 同时成为 parallelism 的前置条件与收敛条件。没有可信 verifier，更多 agents 只产生更多 unchecked work。官方 guide 也直接这样表述。[verification guide](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/06-verify-and-ship.md)

### 6. parallelism 的单位是隔离后的责任，不是 agent 数量

pstack 区分三种 fan-out：

- `swarm`：不同 slice 或预先声明 selection rule 的 race；每个 worker 有独立 scope、SHA、method 与 `PASS / ISSUES / BLOCKED` 结果，parent 聚合而不粘贴 raw dumps。[swarm](https://github.com/cursor/plugins/blob/main/pstack/skills/swarm/SKILL.md)
- `arena`：相同 brief 的多个 candidate；独立 worktree/output；cross-vendor judge；按 rubric 选一个 base，再手工 graft 少量优点，最终复验。[arena](https://github.com/cursor/plugins/blob/main/pstack/skills/arena/SKILL.md)
- `interrogate`：相同 intent 的多个 adversary；不选 winner，只合并每个可被 coordinator 重跑证明的 failure。[interrogate](https://github.com/cursor/plugins/blob/main/pstack/skills/interrogate/SKILL.md)

共同内核是：先定义 contract，再隔离写入，再并行，最后由 parent 验收和聚合。`separate-before-serializing-shared-state` 明确要求优先消除共享状态，而不是先加锁。[principles guide](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/08-principles.md)

这解释了“fearless parallelism”的真实含义：信心来自独立 ownership、可重跑 proof 与 parent accountability，不来自多模型投票。

## `how` 与 `why`：当前源码的刻意极简

### `how`

**核心机制。** 当前 skill 只做两步：若 scope 含糊就声明解释后继续；启动一个 `generalPurpose`、`readonly: true` 的 subagent，以“让陌生 senior engineer 得到可工作的 architecture mental model”为 brief；parent 只做轻量编辑后呈现。[how](https://github.com/cursor/plugins/blob/main/pstack/skills/how/SKILL.md)

**为何有效。** 单独 read-only context 避免实现任务的上下文与预设污染解释；“能 confidently start working”把输出目标从 symbol inventory 提升到 architecture/runtime mental model。更关键的是官方主动删掉 complexity gate、2–4 explorers、synthesizer 与 output schema，说明对通用 code walkthrough，强而短的 audience contract 比固定多 agent ceremony 更重要。[commit `bf0c7cd`](https://github.com/cursor/plugins/commit/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7)

**与 Matt-first overlap。** `research` 已要求 primary sources，`codebase-design` 提供 module/interface/seam vocabulary，agent runtime 也已有代码探索能力。`how` 不提供新的工程流程。

**独特增量。** 一个很小的 read-only explanation contract，以及把“解释给谁、读完能做什么”写清楚。

**Runtime coupling。** 低到中。Prompt 本身通用；`Task`、`readonly` field 需要 adapter。

**最小可借鉴内核。** “一个 fresh read-only explorer；以 senior onboarding mental model 为 acceptance；parent 只校正上下文，不重写结论。”

**风险。** 当前文件不要求 citation、call-path proof 或 parent spot-check；单一 explorer 的误读可能被原样放大。它也已从 `poteto-mode` 自动路由中移除，只保留 direct use、`teach` 与 help catalog。这不是应该放回每个 implementation 前的 mandatory gate。

**判断。** 只读参考，不新增 skill。

### `why`

**核心机制。** 一句 contract 完成全部工作：从引入目标及其后续变更的 commits 与 PR discussions 回答；trail 薄时才找其他来源；引用作者原话；把 agent inference 标为 inference；明确 record 没回答什么。[why](https://github.com/cursor/plugins/blob/main/pstack/skills/why/SKILL.md)

**为何有效。** Code 只能证明现在“是什么”，不能证明过去“为什么”。按 introduction → later changes 的历史顺序能区分原始 rationale、后续修补与今天仍成立的约束；显式 unknown 阻止 agent 用 plausible story 填空。

**与 Matt-first overlap。** `research` 已要求高可信 primary sources，`diagnosing-bugs` 会看 ADR 与 history。两者都没有把“record, not code”“作者原话 / inference / unanswered”压缩成如此清晰的 default contract。

**独特增量。** history-first evidence discipline，尤其适合 threshold、feature flag、regression 与 architecture rationale。

**Runtime coupling。** 很低。只要求能读 git/PR history。

**最小可借鉴内核。** 在既有 `research` 或 investigation 中增加一种问题类型，不新增 router：`why` 问题先找 introducing commit/PR 与 later changes；事实、作者理由、inference、unknown 分栏。

**风险。** Repository history 可能经过 squash，PR discussion 可能不可达；“其他来源”没有固定可信度顺序。必须把缺失写成 unknown，而不是降级为 code-based motive。

**判断。** 第一优先级 eval。当前 9 行版本比旧 900 行左右的 references/orchestration 更值得评估。

## 高价值能力逐项评估

### `blast-radius`

**机制与 why。** 它拒绝把 caller list 当成结果，要求找到 change 安全所依赖的“一到两个事实”，沿五级 confidence ladder 从 assertion、source line、unreachable failure walk-through，一直推进到 real-code script 与 running app。搜索重点是 grep 看不到的边界：pinned dependency、local patch、wire format、DB column、另一种语言的 reader、feature flag 与 timing。最终把 confirmed risks 与 cleared risks 分开。[blast-radius](https://github.com/cursor/plugins/blob/main/pstack/skills/blast-radius/SKILL.md)

这有效是因为长风险清单容易显得全面，却没有可证伪中心。大多数小 change 的安全性确实依赖少数 invariant；直接执行那个 invariant 可以一次清掉多条 speculative risk。

- **Overlap：** `code-review` 检查 Standards/Spec，`diagnosing-bugs` 建立 red-capable loop，`codebase-design` 关注 seam；都有交集。
- **独特增量：** diff 外的 hidden coupling，加“one safety fact + proof level + cleared list”。
- **Runtime coupling：** 低；大 change 可选 `arena` 是附加项，不是内核。
- **最小内核：** code review 增加一问：“这次 change 安全依赖哪个事实？能否用最小 real-code probe 证明？”
- **风险：** 过早认定“一个事实”会漏掉多个独立 hazard；为了证明而写的 script 若不走 production path，会制造假安全。必须允许“unproven”。
- **判断：** 第一优先级 eval。

### `architect`

**机制与 why。** 当前只有 11 行。先 trace 触及的所有 system，再画两个不同 shape，比较 types、signatures、module boundaries；选择 state 单一 owner、task 单一路径、caller knowledge 最少的方案；workaround 重复时 redesign；大型或 contested design 才升级到 `arena`。[architect](https://github.com/cursor/plugins/blob/main/pstack/skills/architect/SKILL.md)

- **Overlap：** 与 Matt `codebase-design` 的 deep module、small interface、seam、design-it-twice 高度重叠。
- **独特增量：** “每份 state 一个 owner、每个 task 一条路径”是很实用的 selection rubric；`trace every system touched` 防止局部接口优化。
- **Runtime coupling：** 核心很低；升级到 `arena` 后为中高。
- **最小内核：** 把两个 selection criteria 合并进既有 `codebase-design` 的评估，不引入 `/architect`。
- **风险：** “跨 function boundary 就触发”过宽，会给普通改动增加 ceremony；两个 paper shape 也不如可运行 prototype。
- **判断：** 只读参考。不要复制 skill。

### `interrogate`

**机制与 why。** 先从 user message、commits、PR description 重述 intent；多个 adversary 在隔离 worktree 中尝试 break change；每条 finding 必须给 exact command、actual output 与 intended output；coordinator 重跑，只有确实 failure 且违反 intent 的 finding 才保留；style、naming、未来风险等未运行结论直接丢弃。它只报告，不自动修复。[interrogate](https://github.com/cursor/plugins/blob/main/pstack/skills/interrogate/SKILL.md)

- **Overlap：** Matt `code-review` 已并行运行 Standards/Spec 两轴，且要求固定 merge-base。
- **独特增量：** review comment 的 admission gate 从“论证合理”提升为“可重跑 failure”；多 adversary 追求 failure diversity，不是多数票。
- **Runtime coupling：** 中高。完整实现依赖 `arena` fan-out、per-model role、worktree copy 与 Task semantics；proof gate 本身很低。
- **最小内核：** 在 code-review 后增加可选 adversarial verification pass：只有能复现、违反 spec intent 的 behavior finding 进入 confirmed；其余保持 candidate，不混入 hard findings。
- **风险：** 无法廉价运行的 security、data-loss、race risk 可能被错误清零；plan/design 在没有 prototype 时几乎无法通过 admission gate。官方也明确建议先 prototype，再 interrogate。[design guide](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/04-design.md)
- **判断：** 第一优先级 eval，但只测 proof gate，不先复制 multi-model orchestration。

### `correct`

**机制与 why。** 从 commits、reverts、review comments、agent instructions 与 workaround comments 中找发生至少两次的 mistake class；按 architecture → type → lint/CI → behavior test → docs 的顺序选择最高有效层；每个新 check 必须在真实历史错误上失败；机械规则的 error 要直接指出正确 file/type/function；最后维护 rule-to-enforcement table。[correct](https://github.com/cursor/plugins/blob/main/pstack/skills/correct/SKILL.md)

- **Overlap：** Matt `retro` 已优先 deterministic guardrail 而非 instruction，`improve-codebase-architecture` 找结构摩擦。
- **独特增量：** “class 至少重复两次”、enforcement hierarchy、用真实 past mistake 做 mutation-like proof、规则与 enforcement 映射。
- **Runtime coupling：** 中。源码读取通用，但“读 agent history / review comments”取决于 tracker 与 transcript 可达性。
- **最小内核：** 作为 `retro` 的判定框架：重复证据 ≥2；优先消除错误路径；对新增 guardrail 回放一个历史 bad patch。
- **风险：** 为低频错误增加 lint/type machinery 会让 repo 过度约束；“one commit each”与本地 commit policy 不一定兼容；维护 rule table 可能退化成另一份漂移文档。
- **判断：** 第二优先级 eval，优先在已有重复 agent mistake 的真实 repo 上评估。

### `sharpen`

**机制与 why。** 重写 prompt 前只问四件事：顶尖专业人员还会做什么、最 raw 的 material 是什么、会使用哪些具体 methods/tools、什么外部证据能证明结果；然后把 prompt 变深而非变大，并要求对 experiment 可 settle 的选择先 prototype，product/preference choice 留给 operator。[sharpen](https://github.com/cursor/plugins/blob/main/pstack/skills/sharpen/SKILL.md)

- **Overlap：** `grill-with-docs`、`grilling`、`to-spec` 已负责澄清、tradeoff 与约束。
- **独特增量：** rawest-material 与 independent-proof 两问非常紧凑；明确分离 empirical choice 与 preference choice。
- **Runtime coupling：** 无。
- **最小内核：** 作为 prompt review checklist，而不是入口 skill。
- **风险：** “top professional”容易诱发 prestige theater 与无关 scope；methods/tools 列表可能把 outcome prompt 重新变成 ceremony prompt。
- **判断：** 只读参考，不进入主链。

### `reframe`

**机制与 why。** 从用户自己的 code/files/description 出发；若描述可对应多个问题，先列 2–3 个候选及 discriminating sign；再给 8–12 个按 design impact 排序的 expert terms，每个必须绑定原描述、真实 project/paper/system 与已打开验证的链接；借 2–3 个邻域类比并明确 analogy break；最后重写描述。[reframe](https://github.com/cursor/plugins/blob/main/pstack/skills/reframe/SKILL.md) · [commit `9e278fe`](https://github.com/cursor/plugins/commit/9e278fe4d4ecd8bfe98b1b79bf4be662efb338cc)

- **Overlap：** `grill-with-docs` 与 `domain-modeling` 都处理术语、领域边界与 glossary。
- **独特增量：** 先 differential diagnosis 再命名；按“会改变什么设计”排序；neighboring-field analogy 必须说明失效边界。
- **Runtime coupling：** 低，但依赖 web access 与逐链接验证。
- **最小内核：** 当用户无法命名问题时，先列候选问题 + 一条区分信号；术语只保留真正改变 design decision 的项。
- **风险：** 固定 8–12 terms 容易 padding；外部名词可能压过 repo 自己的 ubiquitous language；类比会制造错误 authority。
- **判断：** 第二优先级 eval，限于 `grill-with-docs` 前的 terminology case，不新增长期 router。

### `benchmark-checklist`

**机制与 why。** 在运行前先写出将要发布的 claim、读 measurement script、检查 machine load；然后回答七问：limiter、production tuning、physical limits、errors/correctness、alternating repeats、end-to-end relevance、work 是否真的发生。默认至少 A/B 交替 5 次，报告 median/range；无法命名 limiter、某侧未调优，或无法确认 error/work 时必须判 `inconclusive`。[benchmark-checklist](https://github.com/cursor/plugins/blob/main/pstack/skills/benchmark-checklist/SKILL.md)

- **Overlap：** `diagnosing-bugs` 的 perf branch 已要求 baseline 与 profiler。
- **独特增量：** measurement validity 的系统化 checklist，尤其是“why not double”、Amdahl-style bound、load generator saturation、lazy/no-op work 与 correctness count。
- **Runtime coupling：** 低；具体命令需按 OS/toolchain 替换。
- **最小内核：** 先固定 claim；A/B interleave；count work/errors；给 median/range/limiter；不能满足则 inconclusive。
- **风险：** 小型 ballpark 若机械执行全套会浪费成本；不同 workload 不能统一用 5 次 median；统计检验必须服从 harness 特性。
- **判断：** 第一优先级 eval，且最容易独立验证价值。

### formal verification family

该 family 包括 `create-formal-verification-skill`、`maintain-formal-verification-skill` 与 TLA+ 可视化的 `statechart`。

**机制与 why。** generator 从“失败伤害高、tests 最难覆盖”的 promise 选一个 target；按 question 选 model checker、code-level verifier、SMT/proof 或 generated inputs；每个 model element 要指回 code；property 必须在 broken variant 上失败；pass 要写清 bounds/assumptions；产物记录 covered files/functions 与 sync commit。[create formal](https://github.com/cursor/plugins/blob/main/pstack/skills/create-formal-verification-skill/SKILL.md)

maintainer 先运行旧 check，再从 sync commit 逐 commit 阅读 covered code，区分 no effect、model drift、intentional promise change、possible bug；先按 code 更新 model，再运行，防止为了 pass 反向塑形；failure 要 replay 到真实 code，pass 要再次用 broken variant 证明 check 仍有 sensitivity。[maintain formal](https://github.com/cursor/plugins/blob/main/pstack/skills/maintain-formal-verification-skill/SKILL.md)

`statechart` 以 TLA+ + TLC 为底层，把 invariant violation 变成 reader language 的 shortest path 与 Mermaid chart；但它需要 TypeScript runtime，首次运行通过 mise 安装 TLC 与 Java，并包含大量 compiler/rendering scripts。[statechart](https://github.com/cursor/plugins/blob/main/pstack/skills/statechart/SKILL.md)

- **Overlap：** Matt 的 TDD、prototype、diagnosing-bugs 都强调可执行反馈，但不做 bounded exhaustive state exploration。
- **独特增量：** code↔model traceability、sensitivity test、sync commit 与 drift classification。这四点比“使用 TLA+”本身更有价值。
- **Runtime coupling：** generator contract 中等；TLA+ / `statechart` 实现很高，且 generated path 固定为 project-local skill convention。
- **最小内核：** 只在 concurrency/retry/state-machine/parser/unsafe code 上选一个 property；记录 scope/assumptions/covered code/sync commit；用一个 broken variant 证明 check 会失败。
- **风险：** model pass 可能只是 stale description；atomic step 与 code 不一致会给假 proof；bounds 容易被误报成 universal guarantee；当不支持 code verifier 而退回 generated-input testing 时，结果已不是 formal proof；toolchain 与维护成本高。
- **判断：** `create/maintain` 作为条件式 eval；`statechart` 实现明确跳过。只有真实高风险 property 与 owner 愿意维护 sync record 时才试。

### `teach`

**机制与 why。** `teach` 在 code context 中并行组合 `how` 与 `why`，先按用户为何询问选择少数 learning outcomes，再从 plain definition 开始，把机制、原因和 edge case 编成一个解释；三件以上 moving parts 时用多张递进 diagram，每张只增加一个部分，而不是一次给完整 reference diagram；保留 `why` 的 confidence language。[teach](https://github.com/cursor/plugins/blob/main/pstack/skills/teach/SKILL.md)

- **Overlap：** ys-powers 已有 Matt productivity `teach`，它是持久 teaching workspace、lessons、retrieval practice 与 learning record；`eli` 也承担本地解释。名称完全冲突，但目标不同。
- **独特增量：** 一次性的 code/change explanation；how/why 合流；逐图构建 mental model；不把 uncertainty “润色掉”。
- **Runtime coupling：** 低到中，因为它依赖 `how`/`why` invocation 与 `unslop`。
- **最小内核：** 给现有解释能力借用 progressive diagrams 与 confidence-preserving synthesis。
- **风险：** 同名 `teach` 会直接造成 skill resolution 与用户心智冲突；“并行 how/why”对小问题成本过高。
- **判断：** 明确不引入；仅只读借鉴表达方法。

## 基于证据调整候选集

### 应新增关注：`create-verification-skill`

它比“再加一个 review prompt”更可能给长期收益。该 skill 先 interview repo 而不是 user，确定真实 surface、launch、drive、evidence 与 isolation；生成 Launch / Doctor / Drive / Evidence / Cleanup contract 和 feature map；交付前必须完整走一遍并确认 cleanup 没删 evidence。[create-verification-skill](https://github.com/cursor/plugins/blob/main/pstack/skills/create-verification-skill/SKILL.md)

与 `browser-testing-with-devtools`、`diagnosing-bugs` 的 overlap 很高，但独特增量是把一次性控制方法固化为可复用、agent-readable 的 repo capability。最小 eval 不应生成 `.cursor/skills/`，而应测试“能否从现有项目资料生成并实际跑通一份 runtime-neutral verification runbook”。风险是 feature map drift，因此必须连同 source-wave + one live pass 的 maintenance idea 一起评价。[maintain-verification-skill](https://github.com/cursor/plugins/blob/main/pstack/skills/maintain-verification-skill/SKILL.md)

### 应降级：`how`、`architect`、`teach`

这三项不是低质量，而是当前 Matt-first 已有更合适的 ownership：code exploration、`codebase-design`、现有 `teach`/`eli`。官方最新演进也主动把 `how` 从 mode 自动路由移除。它们适合作为 prompt-diet 与表达方法的只读样本，不值得成为新增 skill。

### 应把 orchestration 与内核拆开：`interrogate`、formal verification

`interrogate` 的价值来自“只保留可重跑 failure”，不来自固定三模型 panel。formal verification 的价值来自 traceability、scope honesty、sensitivity 与 drift control，不来自复制 `statechart` compiler。eval 应分别测内核，避免把 runtime coupling 误判成能力本身。

## 分级建议

### A. 优先 eval

1. **`why` 的 history-first contract。** 低成本，独特性高，几乎无 runtime coupling。
2. **`blast-radius` 的 one-safety-fact proof。** 直接补足现有 review 对 diff 外 hidden coupling 的覆盖。
3. **`interrogate` 的 rerunnable-finding admission gate。** 先单模型或现有 reviewer 上测，不上 model router。
4. **`benchmark-checklist`。** 可在已有 benchmark 上客观比较它是否阻止错误结论。
5. **`correct` 的 repeated-class + highest-enforcement-level。** 需要真实历史 mistake 才有意义。
6. **`reframe` 的 differential terminology。** 只在需求确实缺少 expert vocabulary 时 eval。
7. **runtime-neutral verification runbook。** 有真实 app/CLI/service 项目时才评估。
8. **formal verification kernel。** 有高代价 concurrency/retry/state-machine property 时才评估。

### B. 只读参考

- `how`：one read-only explorer 与 audience-based acceptance。
- `architect`：two shapes、single state owner、single task path、least caller knowledge。
- `sharpen`：raw material、specific method、independent proof、experiment vs preference。
- `teach`：how/why synthesis、progressive diagrams、保留 uncertainty。
- 24 principles：作为 review vocabulary 查阅，尤其 `prove-it-works`、`explain-the-number`、`separate-before-serializing-shared-state`；不要整体注入常驻 prompt。
- `arena` / `swarm`：只借鉴先 frame、写入隔离、parent aggregation、dropout/gap 显式化。

### C. 明确跳过

- 整套 `poteto-mode` 与 22-playbook router。它会与 Matt-first 主链形成第二入口。
- `setup-pstack` model router 与 Cursor/Claude role files。OMP runtime 已拥有自己的 model/delegation policy。
- `poteto-agent` wrapper。它为 pstack mode 的 context propagation 服务，不是独立工程能力。
- `automations/benny`、Bugbot/PR babysit/shipping/autopilot。Cursor-only 且超出本地 workflow 目标。
- `statechart` compiler/scripts/test corpus。toolchain 与维护面过大；只有 formal eval 证明真实需求后才重新考虑外部工具，不复制实现。
- pstack 的同名 `teach`、`tdd`、`bro` 等 skill。当前已有 Matt ownership，重复注册只会制造冲突。
- 整体复制 24 principles 或 59 skills。原则名与 inventory 不是可验证增量。

## 可执行 eval 顺序

以下顺序只产生评估证据，不实施任何 skill，也不改变主链。

### Eval 0：冻结 baseline

- 选 3 个已知答案的 history/rationale 问题、2 个小 diff、1 个容易被误读的 benchmark、1 个已有重复 agent mistake 的 repo history。
- 记录现有 Matt-first 流程的时间、tool calls、引用准确率、confirmed finding 数、false positive、是否给出真实 proof。
- candidate prompt 使用 pstack 的内核，但不出现 pstack skill 名称；judge 盲看输出。此做法直接沿用官方 Eval playbook 的 organic prompt、sanitized labels 与 blind judge 原则。[Eval playbook](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/eval.md)

### Eval 1：`why`

- 对每个历史问题运行 baseline 与 history-first variant。
- Rubric：是否找到 introducing commit/PR；是否覆盖 later changes；作者原话是否可追溯；inference 是否标记；unknown 是否诚实；是否把 code shape 冒充 rationale。
- Promotion gate：引用准确率提高，且没有明显增加 unsupported narrative 或运行成本。

### Eval 2：`blast-radius`

- 对两个已知 hidden coupling 的小 diff，比较普通 review 与 one-safety-fact variant。
- Rubric：是否识别 diff 外 boundary；是否给出一个可证伪 safety fact；proof 是否走真实 shipped path；confirmed 与 cleared 是否分开；允许 unproven。
- Promotion gate：至少多抓到一个已知 coupling，且 speculative risk 数下降。

### Eval 3：`interrogate` proof gate

- 使用相同 reviewer 与相同 diff，先不引入 multi-model variable。
- Variant 要求每个 behavior finding 附 exact command/output，coordinator 独立重跑；无法运行但高影响的风险进入 `Unverified risks`，不可静默删除。
- Promotion gate：confirmed findings 的 precision 提升；security/race 等难运行风险没有被错误归零。

### Eval 4：`benchmark-checklist`

- 选择一个已知有 warmup、error count、lazy work 或 end-to-end mismatch 的 benchmark。
- 比较 baseline verdict 与 checklist verdict；确认 A/B interleave、median/range、limiter、work count、error count。
- Promotion gate：能把错误的“faster/slower”降级为 `inconclusive`，并指出可执行的补测。

### Eval 5：`correct`

- 从真实 history 选择一个至少发生两次的 mistake class。
- Baseline 只写 rule；variant 按 architecture → types → lint/CI → behavior test → docs 选择，并回放真实 bad patch。
- Promotion gate：guardrail 对 bad patch 可靠失败、对当前 tree 通过，且没有引入不成比例的机制或 false positives。

### Eval 6：`reframe` 与 verification runbook

- `reframe` 只测一个术语含混、确实可能对应 2–3 个问题的需求。检查 discriminating sign 是否真的改变后续 design，删除 padding term。
- Verification runbook 选择一个已有可启动 surface 的项目。要求 Launch / Doctor / Drive / Evidence / Cleanup 全程可运行，proof 在 cleanup 后仍存在；不生成 `.cursor/skills/`。
- Promotion gate：后续 agent 在 fresh context 中能无人工补充地完成一次真实验证。

### Eval 7：formal verification，仅条件触发

- 前提：存在一个具体、高伤害、tests 难覆盖的 property，并有 owner 接受持续维护。
- 只验证一个 property；明确 bounds/assumptions；每个 model step 指回 code；用 broken variant 证明 sensitivity；记录 sync commit；把 counterexample replay 到 real code。
- Promotion gate：check 能抓到 intentional break，pass 没有越过 scope 宣称，维护者能在 covered code change 后更新它。

## 最终建议

pstack 当前版本最值得学习的不是“更多 skill”，而是三种约束：

1. **evidence contract 足够短。** `why` 的事实、inference、unknown；`how` 的 read-only mental model；`architect` 的两个 shape。
2. **只有可重跑证据才能升级为结论。** `blast-radius` 证明 safety fact，`interrogate` 重跑 finding，benchmark 无 limiter/正确性/work count 就判 inconclusive，formal check 必须在 broken variant 上失败。
3. **parallelism 必须建立在 isolation、明确责任与 parent verification 上。** model diversity 是补充，不是可信度来源。

因此，保持 Matt-first 唯一主链；把 pstack 当作第一方 prompt 与 verification 研究样本；按上面的 eval 顺序验证小内核；只有实验证明独特增量后，才考虑在现有 Matt skill 的 ownership 内吸收一条规则。不要安装整套 pstack，不要新增第二 router，也不要先实现任何 skill。
