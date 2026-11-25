# gstack skills 调研：inventory、router、候选方法与 `how` / `why` 溯源

> 调研日期：2026-11-25  
> 主要样本：本地完整 checkout `refer/gstack/`，HEAD [`47b464a`](https://github.com/garrytan/gstack/commit/47b464a0d4a9f361b7e74f050fd569a49b20078a)。  
> 边界：本文只研究，不复制、不安装、不修改 gstack、Matt skills 或本仓库安装逻辑。下文明确区分“源码事实”和“分析建议”。

## 结论先行

### 源码事实

1. **gstack 没有名为 `how` 或 `why` 的 skill。** 当前官方自动生成的 capability index 声明它会索引 “every capability”，并列出 `/gstack` 与全部 skill；其中没有 `/how`、`/why`（[官方 `gstack/llms.txt`](https://github.com/garrytan/gstack/blob/main/gstack/llms.txt#L1-L11)、[完整 skills 列表](https://github.com/garrytan/gstack/blob/main/gstack/llms.txt#L11-L75)）。本地对应 commit 的顶层 immediate skill 结构是 62 个 `<name>/SKILL.md` 加根 router `SKILL.md`，没有 `how/` 或 `why/`。
2. **`how` / `why` 更可能来自 Cursor 官方 pstack。** Cursor 的 `cursor/plugins` 仓库明确包含短版 [`pstack/skills/how/SKILL.md`](https://github.com/cursor/plugins/blob/main/pstack/skills/how/SKILL.md) 与 [`pstack/skills/why/SKILL.md`](https://github.com/cursor/plugins/blob/main/pstack/skills/why/SKILL.md)，pstack README 也把两者列为直接调用的 skills（[官方 inventory](https://github.com/cursor/plugins/blob/main/pstack/README.md#skills)）。
3. **Go7hic/ystack 也包含 `how` / `why`，但它是 portable adaptation，不是 gstack 的组成部分。** ystack README 明说项目起源于 Cursor pstack，并保留 `how`、`why` 等工程系统（[Go7hic/ystack README](https://github.com/Go7hic/ystack/blob/main/README.md)）。它的 [`how`](https://github.com/Go7hic/ystack/blob/main/skills/how/SKILL.md) 和 [`why`](https://github.com/Go7hic/ystack/blob/main/skills/why/SKILL.md) 已明显扩展，不应与 Cursor 原版的短 prompt 混为一谈。
4. **gstack 是一套有自己 router、hooks、state、artifact handoff 和 runtime 的完整 process，而非可以无摩擦摘取的 prompt 集合。** 官方 workflow 是 **Think → Plan → Build → Review → Test → Ship → Reflect**，上一步 artifact 会被下游读取（[README: The sprint](https://github.com/garrytan/gstack/blob/main/README.md#the-sprint)）。根 [`SKILL.md`](https://github.com/garrytan/gstack/blob/main/SKILL.md#L159-L230) 又承担请求路由；安装还引入 Bun、Git、host hooks、可选 Aside / bundled browser 等运行时要求（[README: requirements](https://github.com/garrytan/gstack/blob/main/README.md#L32-L40)）。

### 分析建议

- **不要把 gstack 整套直接并入 ys-powers 当前 skills。** 当前 Matt-first 主链已经是 `grill-with-docs → to-spec → to-tickets → implement → code-review`（[本仓库约定](https://github.com/carl10086/ys-powers/blob/main/CLAUDE.md)、[Matt 官方 engineering inventory](https://github.com/mattpocock/skills/blob/main/skills/engineering/README.md#L5-L17)）。gstack 的 `/office-hours`、`/spec`、`/autoplan`、`/review` 会形成第二套前置访谈、spec、review 与 router 语义。
- 最值得继续研究的不是整条 gstack pipeline，而是四类**可独立验证的方法**：skill 体积/漂移治理（`/write-skill`）、证据化 test retirement（`/test-audit`）、report-only QA（`/qa-only`）、以及 destructive guard / completion contract 的机制设计。
- `/cso` 与 `/office-hours` 有方法论价值，但前者 runtime 耦合重，后者与 `/grill-with-docs` 重叠高；适合读方法、做对照，不适合原样引入。

## 1. Skill inventory

### 源码事实

官方 [`gstack/llms.txt`](https://github.com/garrytan/gstack/blob/main/gstack/llms.txt#L1-L11) 是自动生成的 capability index；当前样本共 **63 个 skill entry**：根 `/gstack` router，加 62 个顶层 skill 目录（[skills 明细](https://github.com/garrytan/gstack/blob/main/gstack/llms.txt#L11-L75)）。为便于理解，下面只做功能分组，不改变官方名称：

| 分组 | Skills |
|---|---|
| Router | `/gstack` |
| Discovery / planning | `/office-hours`, `/spec`, `/autoplan`, `/plan-ceo-review`, `/plan-design-review`, `/plan-devex-review`, `/plan-eng-review`, `/plan-tune`, `/eval-plan` |
| Engineering / review | `/build-check`, `/review`, `/test-audit`, `/deslop-shared-libs`, `/health`, `/modernize`, `/codex`, `/write-skill` |
| QA / browser / performance | `/browse`, `/qa`, `/qa-only`, `/open-gstack-browser`, `/pair-agent`, `/scrape`, `/skillify`, `/setup-browser-cookies`, `/benchmark`, `/benchmark-models`, `/canary` |
| Design / DX / docs / media | `/design-consultation`, `/design-html`, `/design-motion`, `/design-review`, `/design-shotgun`, `/devex-review`, `/diagram`, `/make-pdf`, `/document-generate`, `/document-release` |
| Safety / security / scope | `/careful`, `/guard`, `/freeze`, `/unfreeze`, `/cso` |
| Release / deploy / compute | `/gstack-ship`, `/land-and-deploy`, `/landing-report`, `/setup-deploy`, `/ubicloud` |
| Context / coordination / operations | `/captain`, `/context-save`, `/context-restore`, `/learn`, `/retro`, `/runaway-stopper`, `/setup-gbrain`, `/sync-gbrain`, `/gstack-upgrade` |
| iOS | `/ios-clean`, `/ios-design-review`, `/ios-fix`, `/ios-qa`, `/ios-sync` |

这个 inventory 也说明 gstack 不只是 planning/review：它同时携带 browser、release、deployment、security、state/memory、multi-agent coordination 与 host setup。官方 README 对主干 skills 的角色和 handoff 有进一步说明（[sprint 表格](https://github.com/garrytan/gstack/blob/main/README.md#L142-L190)）。

## 2. Router、workflow 与 skill contracts

### 2.1 两层路由

**源码事实：**

1. 根 `/gstack` 是 conversational router。它先把 testing / bug finding 导向 `/qa` 或 `/qa-only`，再把 browser interaction 导向 `/browse`，最后按 request pattern 分派其他 skills；不匹配则直接回答（[`SKILL.md` route first](https://github.com/garrytan/gstack/blob/main/SKILL.md#L159-L175)）。
2. `PROACTIVE` 控制主动调用范围：`off` 不主动建议；默认 `core` 只自动调用 `/office-hours`、`/review`、`/qa`、`/gstack-ship`；`all` 才按全部规则主动调用（[`SKILL.md`](https://github.com/garrytan/gstack/blob/main/SKILL.md#L185-L203)）。
3. 安装后的 deterministic routing hook 是另一层机制：它读取 `triggers:`，不调用模型；当前 gstack 自己只有 `/review`、`/qa`、`/build-check` 参与该 hook 路由，以降低误触发（[skill routing contracts 文档](https://github.com/garrytan/gstack/blob/main/docs/skill-routing-and-contracts.md#L38-L60)）。因此“根 router 能识别很多 skill”和“hook 只自动提示少数 skill”并不矛盾。

**分析建议：** ys-powers 已有 Matt 的 router / workflow 语义；若整套安装 gstack，会出现两个入口同时判断何时 grill、spec、review、QA。即使名称不冲突，调用时机与 artifact ownership 也会冲突。方法级研究应绕开第二个 top-level router。

### 2.2 Artifact handoff

**源码事实：** gstack 把 sprint 设计成串行 handoff：`/office-hours` 的 design doc 供 plan reviews 读取，`/plan-eng-review` 的 test plan 供 `/qa` 读取，`/review` findings 又被 `/gstack-ship` 检查（[README](https://github.com/garrytan/gstack/blob/main/README.md#L142-L148)）。这不是松散组合，而是共享 `$GSTACK_STATE_ROOT`、branch-aware artifacts 与 downstream gates 的系统。

**分析建议：** 这与 Matt-first 中 spec → tickets → implementation → two-axis review 的 artifact graph 重叠。未来若借鉴某一方法，应让它读取现有 spec / ticket / ADR 路径，而不是再建立 gstack state tree。

### 2.3 Contracts 与 hooks

**源码事实：** gstack 默认注册三类 hook：prompt routing、Stop-time skill contracts、PreToolUse destructive-command check（[官方说明](https://github.com/garrytan/gstack/blob/main/docs/skill-routing-and-contracts.md#L1-L16)）。其中 contract 允许 skill 声明“完成前必须存在的 outputs”；缺失时 Stop hook 阻断一次并点名缺口（[同文档](https://github.com/garrytan/gstack/blob/main/docs/skill-routing-and-contracts.md#L5-L7)）。但这些 hook 只有 Claude Code 和 Codex 有完整/部分支持；Cursor、OpenCode 与其他 hosts 不注册（[host support](https://github.com/garrytan/gstack/blob/main/docs/skill-routing-and-contracts.md#L30-L36)）。

**分析建议：** “把 completion criteria 变成可机器检查的 contract”值得研究；“复制 gstack hooks”不值得。OMP 的 tool/runtime contract 不同，应先定义 host-neutral completion evidence，再决定是否需要 OMP 原生机制。

## 3. `how` / `why` 名称核实与来源差异

### 3.1 gstack：明确不包含

**源码事实：** gstack 的 authoritative capability index 没有 `/how` 或 `/why`（[完整列表](https://github.com/garrytan/gstack/blob/main/gstack/llms.txt#L11-L75)），根 router 的 routing rules 也没有这两个目标（[`SKILL.md`](https://github.com/garrytan/gstack/blob/main/SKILL.md#L202-L250)）。文档中的普通英文 “how” / “why” 不能据此当成 skill 名。

### 3.2 Cursor pstack：原版很短

**源码事实：**

- Cursor 官方 `/how` 只有两步：spawn 一个 read-only general-purpose subagent 做 architectural explanation，然后基本原样呈现结果（[`cursor/plugins` source](https://github.com/cursor/plugins/blob/main/pstack/skills/how/SKILL.md)）。
- Cursor 官方 `/why` 更短：从 commits、PR discussions 与其他 records 回答，引用作者原话，把 inference 标成 inference，并说明记录未回答什么（[`cursor/plugins` source](https://github.com/cursor/plugins/blob/main/pstack/skills/why/SKILL.md)）。
- pstack README 把 `/how` 定义为 subsystem walkthrough，把 `/why` 定义为从历史记录解释为何这样构建（[官方 skill table](https://github.com/cursor/plugins/blob/main/pstack/README.md#skills)）。

### 3.3 Go7hic/ystack：portable expansion

**源码事实：**

- ystack README 明确把自己定位为 Cursor pstack 的 portable adaptation，并警告 Cursor 用户不要同时启用 ystack 与官方 pstack 两个 competing routers（[README](https://github.com/Go7hic/ystack/blob/main/README.md)）。
- ystack `/how` 增加 simple/complex 分类、2–4 个独立 exploration angles、read-only parallel explorers、lead synthesis、可选 architecture critique 与 runtime verification（[`how/SKILL.md`](https://github.com/Go7hic/ystack/blob/main/skills/how/SKILL.md)）。
- ystack `/why` 增加七类 evidence coverage map（source control、tickets、long-form docs、chat、observability、error tracking、analytics）、并要求区分 direct evidence、reasonable inference、competing hypotheses、unknown，采用 calibrated confidence（[`why/SKILL.md`](https://github.com/Go7hic/ystack/blob/main/skills/why/SKILL.md)）。

**判断：** 若用户记得的是 skill 名本身，源头更可能是 **Cursor pstack**；若记得的是“多角度探索”“evidence coverage map”“calibrated confidence”，则更可能是 **Go7hic/ystack 的扩展版**。两者都不是 gstack。

## 4. 最值得深入分析的 9 个候选

评分不是“是否安装”，而是“是否值得继续研究”。三个维度分别是：方法论价值、对当前 Matt-first workflow 的互补性、引入冲突/运行时依赖。

| 优先级 | 候选 | 源码中的核心方法 | 与 Matt-first 的关系 | 冲突 / 依赖 | 分析建议 |
|---|---|---|---|---|---|
| A | `/write-skill` | 先跑 `gstack-skill-bill`；把事实放在能生效的最低层；按“先修 tool → 不写模型默认会做的事 → 改原句而非追加 → 放最低层 → 写 rule 不写 story”的 edit ladder；前后记录 size，检查 command drift，完整 diet 用 before/after/no-skill eval（[`SKILL.md`](https://github.com/garrytan/gstack/blob/main/write-skill/SKILL.md#L108-L158)）。 | 与 Matt `writing-for-agents` 的 progressive disclosure、information hierarchy 和 no-op pruning 方向一致，但 size bill、drift check、三臂 eval 是有价值的补充（[Matt source](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-for-agents/SKILL.md)）。 | 原 skill 依赖 gstack helper、模板生成与 Bun tests；直接复制会引入第二套 skill-authoring convention。 | **优先研究方法，不引入 skill。** 先比较两套 pruning / eval vocabulary，寻找能落入现有 `writing-for-agents` 的最小增量。 |
| A | `/test-audit` | Discovery/report 默认只读；每个 retirement candidate 必须有 evidence card，证明 test 检测什么、production callers、stronger proof、history、unlock 与 validation；按 batch 请求批准，不能以删除量为目标（[`SKILL.md`](https://github.com/garrytan/gstack/blob/main/test-audit/SKILL.md#L107-L160)、[report/apply gates](https://github.com/garrytan/gstack/blob/main/test-audit/SKILL.md#L205-L263)）。 | Matt 有 TDD 与 behavior-focused testing，但当前主链没有专门清理 low-value/duplicate tests 的 read-only audit。 | 完整实现写 gstack state report，并假设其 AskUserQuestion / helper conventions；运行真实 retirement 还需 scratch worktree 与项目 test runner。 | **最强互补候选。** 值得单独验证 evidence card 是否能减少“凭感觉删测试”。 |
| A | `/careful` + contracts | `/careful` 对命令链逐段检查，危险操作 ask，少数 catastrophic shapes hard deny；项目规则只能 additive，不能削弱 baseline（[`careful/SKILL.md`](https://github.com/garrytan/gstack/blob/main/careful/SKILL.md#L28-L110)）。skill contracts 则在 Stop 时检查声明的 outputs（[contracts](https://github.com/garrytan/gstack/blob/main/docs/skill-routing-and-contracts.md#L1-L16)）。 | 补的是 workflow 基础设施，而不是另一段 planning/review prompt：一个防 irreversible action，一个防“没交付就结束”。 | 强 host coupling：Claude Code/Codex hooks 行为不同，其他 hosts 不注册；PowerShell 还要求 Git Bash，string matching 也不是 security boundary（[host support](https://github.com/garrytan/gstack/blob/main/docs/skill-routing-and-contracts.md#L30-L36)、[`careful`](https://github.com/garrytan/gstack/blob/main/careful/SKILL.md#L57-L95)）。 | **研究 contract shape 与 threat model，不复制 hooks。** 优先列 OMP 已有保障和缺口，避免重复拦截。 |
| A | `/qa-only` | 明确 “NEVER fix anything or change product tests”；先选 browser/API/CLI/job/worker/webhook surface 与 isolation，再写 charters、执行 probes、保存不可覆盖的 evidence；proposed test 还需 value card（[`SKILL.md`](https://github.com/garrytan/gstack/blob/main/qa-only/SKILL.md#L135-L174)、[artifact/report rules](https://github.com/garrytan/gstack/blob/main/qa-only/SKILL.md#L214-L304)）。 | 当前 Matt 链强在 spec/implement/review；report-only QA 能在不混入修复 diff 的情况下生成复现证据，尤其适合交给后续 `/diagnosing-bugs` 或 tickets。 | Browser surface 依赖 gstack `/qa` sections 与 Aside/bundled browser；report 路径、baseline、template 都耦合 gstack。Functional-only 方法较容易独立。 | **优先研究 report-only permission boundary。** 不要直接采用 browser runtime；先评估 charters + replayable evidence + test value card。 |
| B | `/cso` | 以 “evidence before assurance” 建 application model、attack-surface census；finding 必须说明 attacker、boundary、impact、counterevidence；报告 completeness 与 finding count 分离，并区分 static supported、candidate、runtime-tested、repair candidate（[`SKILL.md`](https://github.com/garrytan/gstack/blob/main/cso/SKILL.md#L16-L39)、[evidence/report rubric](https://github.com/garrytan/gstack/blob/main/cso/SKILL.md#L115-L171)）。 | 当前 Matt-first 主链没有同等深度的 security audit stage；证据标签和 coverage accounting 很互补。 | 这是最重候选：trusted `gstack-cso` helper、schema/contracts、private state、qualified runtime catalog、Docker/native toolchain、budgets 与 witness semantics 都不可随 prompt 搬运；静态模式才是低依赖部分。 | **只研究 evidence taxonomy 与 completeness language。** 不在缺少 helper/witness 时复刻 runtime assurance claim。 |
| B | `/office-hours` | Hard gate：只产 design doc / decision memo，不写代码；先读 repo 与 prior designs，再按 startup/builder/pivot 等 mode 追问，后续可做 landscape、second opinion 与 design handoff（[`SKILL.md`](https://github.com/garrytan/gstack/blob/main/office-hours/SKILL.md#L218-L267)、[phase map](https://github.com/garrytan/gstack/blob/main/office-hours/SKILL.md#L325-L390)）。 | premise challenge、alternatives 与“先理解问题”有价值；但核心职责与 `/grill-with-docs` 高度重叠，后者还维护 glossary/ADR（[Matt README](https://github.com/mattpocock/skills/blob/main/README.md#L109-L158)）。 | 依赖 gstack brain cache、learnings、state-root design docs、Aside research 与 downstream gstack reviews。双访谈会增加成本并制造两个 design artifact。 | **作为对照样本。** 只比较它比 `/grill-with-docs` 多出的 forcing questions / mode calibration，不另加入口。 |
| C | `/spec` | 五阶段锁定 why、scope、technical evidence、draft review、quality gate/file；默认 issue dedupe，technical phase 必须先读代码；之后可做 redaction、Codex score、GitHub filing、local archive、`claude -p` worktree execution（[`SKILL.md`](https://github.com/garrytan/gstack/blob/main/spec/SKILL.md#L174-L217)、[strict phases](https://github.com/garrytan/gstack/blob/main/spec/SKILL.md#L232-L346)）。 | 对“spec 必须 grounded in code”和 dedupe 的要求值得参考；但与 `/to-spec` + `/to-tickets` 正面重叠。 | 假设 `gh`、GitHub issues、Codex outside gate、gstack archive/state，且可直接 spawn implementation；会绕过当前 tracker abstraction 和 ticket graph。 | **比较，不引入。** 仅评估 code-first interrogation 与 dedupe 能否成为现有 `/to-spec` 的验证点。 |
| C | `/review` | 先做 scope drift，再完整读 diff；不在 review pass 中编辑；扫描 test/CI/snapshot suppression 等 gate edits；dispatch specialists 与 adversarial pass，并以 contract 确保 outputs 存在（[`SKILL.md`](https://github.com/garrytan/gstack/blob/main/review/SKILL.md#L34-L42)、[review flow](https://github.com/garrytan/gstack/blob/main/review/SKILL.md#L197-L290)、[gate scan](https://github.com/garrytan/gstack/blob/main/review/SKILL.md#L326-L360)）。 | scope drift、gate integrity、adversarial/chaos pass 是增量；但 Matt `/code-review` 已并行执行 Standards 与 Spec 两轴（[Matt source](https://github.com/mattpocock/skills/blob/main/skills/engineering/code-review/SKILL.md)）。 | 大量依赖 gstack helpers、review ledger、specialists、bot triage、ship/version queue；且 gstack 会 auto-fix 某些 findings，权限模型不同。 | **抽取检查维度，不替换 reviewer。** 最值得对照的是 gate integrity 是否能成为 Matt Standards 轴的一条规则。 |
| C | `/autoplan` | 严格串行 CEO → Design（UI 时）→ DX（developer-facing 时）→ Eng，Eng 最后复核所有前序 amendment；mechanical 自动决定、taste 最终汇总、user challenge 不自动决定（[`SKILL.md`](https://github.com/garrytan/gstack/blob/main/autoplan/SKILL.md#L258-L322)）。缺 design doc 时还会内联 `/office-hours`（[prerequisite handoff](https://github.com/garrytan/gstack/blob/main/autoplan/SKILL.md#L189-L256)）。 | 多视角 plan review 有启发，但整体上重复 Matt 的 grill/spec/tickets 流程，并会再引入一条 planning pipeline。 | 依赖多个 gstack skill sections、phase publication hook、AskUserQuestion、outside reviewers 与 gstack artifacts；上下文和运行成本最高。 | **不引入。** 仅把“Eng review last”与“mechanical/taste/user challenge 分级”作为流程设计参考。 |

## 5. 为什么不整套并入

### 源码事实

- gstack 官方自己称其为 process，并依靠跨 skill artifact handoff（[README](https://github.com/garrytan/gstack/blob/main/README.md#L142-L148)）。
- 完整安装要求 Git、Bun，Claude Code 是 full tier；其他多个 hosts 在当前 README 中仍标为 experimental 或 instruction-only（[requirements](https://github.com/garrytan/gstack/blob/main/README.md#L32-L40)、[host matrix](https://github.com/garrytan/gstack/blob/main/README.md#L58-L97)）。
- hooks、browser、state root、telemetry、outside review、deployment 与 security helpers 不只是 prompt 文本；其行为散布在 setup、binaries、sections 与 host adapters 中（[skill contracts](https://github.com/garrytan/gstack/blob/main/docs/skill-routing-and-contracts.md)、[capability index](https://github.com/garrytan/gstack/blob/main/gstack/llms.txt)）。

### 分析建议

直接整套并入会产生五类成本：

1. **双 router：** Matt 的 `ask-matt` / skill selection 与 `/gstack`、routing hook 同时存在。
2. **双主链：** `grill-with-docs → to-spec → to-tickets → implement → code-review` 与 `office-hours → plan reviews → review → qa → ship` 都试图拥有 lifecycle。
3. **双 artifact system：** 现有 issue tracker、spec/tickets、ADR/GLOSSARY 与 `$GSTACK_STATE_ROOT` design docs/reports/learnings 并存。
4. **host/runtime 偏差：** ys-powers 面向本地 OMP/Claude 适配；gstack hooks 对 Claude Code/Codex 才有明确支持，browser/security/deploy 还需额外 binaries 或 services。
5. **升级与语义漂移：** gstack 当前 inventory 与 contracts 已是快速演进的完整系统；复制部分文件会丢失生成、helper、schema 和 runtime invariants，整套 vendoring 又违反本仓库保持 Matt 边界的目标。

因此，正确粒度是**研究一个方法 → 在现有 workflow 中找到唯一 owner → 做独立 eval → 再决定是否原生重写**，而不是复制目录或并排安装。

## 6. 建议的下一步

以下均是后续研究建议，不代表本文已复制、安装或实现：

1. **先做四个无安装的小型 eval。** 各挑 3–5 个真实历史案例：
   - `/write-skill`：比较现有 `writing-for-agents`、加 edit-ladder/size/drift 检查、以及 no-skill baseline。
   - `/test-audit`：盲评普通建议与 evidence card，观察 false-positive retirement 数。
   - `/qa-only`：比较“边测边修”与 report-only charter，观察复现证据完整性和后续修复可接手性。
   - contracts：对已有 skills 的 completion criteria 做 transcript-only 检查，先不装 hook。
2. **为每个方法指定现有 owner，禁止新增顶层 router。** 初步映射：skill hygiene → `writing-for-agents`；test retirement → 新的独立 audit 候选或既有 testing guidance；QA evidence → `diagnosing-bugs` 前置报告模式；gate integrity → `code-review` Standards 轴。
3. **把 `/cso` 拆成两项研究。** 先研究 static evidence taxonomy；只有在已有可信 executor、isolation、schema validation 与 witness 后，才讨论 runtime-tested 语义。不要让 prompt 自证 security assurance。
4. **对重叠项只做差异清单。** `/office-hours` vs `/grill-with-docs`、`/spec` vs `/to-spec` + `/to-tickets`、`/review` vs `/code-review`、`/autoplan` vs Matt 主链。若没有经 eval 证明的独特增益，不增加入口。
5. **保持 `how` / `why` 调研独立。** 若后续要研究，应分别以 Cursor pstack 原版和 Go7hic/ystack 扩展版为两个样本；不要以 gstack 名义引入，也不要同时安装 ystack 与 pstack competing routers（[ystack 的官方提醒](https://github.com/Go7hic/ystack/blob/main/README.md)）。

最终建议：**保留 Matt-first workflow 作为唯一主链；从 gstack 只研究可验证、单一职责、低 runtime coupling 的机制。当前不复制、不安装、不整套并入。**
