# Matt `code-review` 与 pstack review leaves 的组合研究

> 研究日期：2026-11-26  
> 结论适用版本：Matt [`abeeaf95660ba9e8b7c753eb38f441ca707a8823`](https://github.com/mattpocock/skills/commit/abeeaf95660ba9e8b7c753eb38f441ca707a8823)，pstack [`41e400932eca14f289e7db717a70455256b6d388`](https://github.com/cursor/plugins/commit/41e400932eca14f289e7db717a70455256b6d388)。本仓库的两个 pin 分别记录在 [`skills/matt/README.md` lines 3–8](../../skills/matt/README.md#L3-L8) 与 [`skills/pstack/README.md` lines 3–9](../../skills/pstack/README.md#L3-L9)。

## 直接答案

1. **Standards 与 Spec axes 属于 Matt，不属于 pstack。** 它们在 Matt pinned upstream 的 `code-review` 中被定义为两条并行、互不 rerank 的 review axes；active copy 保持同一 contract。pstack 的完整 skill catalog 没有一个独立的 `/code-review`，只有职责不同的 `/interrogate` 与 `/blast-radius`。[Matt upstream `code-review` lines 1–11, 76–89](../../refer/mattpocock-skills/skills/engineering/code-review/SKILL.md#L1-L11) · [pstack catalog lines 109–160](../../refer/cursor-plugins/pstack/README.md#L109-L160) · [pstack router lines 64–118](../../refer/cursor-plugins/pstack/skills/poteto-help/SKILL.md#L64-L118)
2. **pstack leaves 在 Matt-first flow 下技术上可以作为独立补充 pass，但不能替代 Matt 两轴。** `/interrogate` 只保留真实运行能复现且违反 intent 的 failure，并明确丢弃 style、naming、structure 与只在未来变化下才成立的风险；`/blast-radius` 找 diff 外 hidden coupling，并证明一两个 safety facts。它们都没有 Standards 的 repo-rule/Fowler contract，也没有 Spec 的 missing/partial、scope creep、wrong implementation 三项完整审查。[`interrogate` lines 9–31](../../refer/cursor-plugins/pstack/skills/interrogate/SKILL.md#L9-L31) · [`blast-radius` lines 13–48](../../refer/cursor-plugins/pstack/skills/blast-radius/SKILL.md#L13-L48) · [Matt axes prompts lines 62–74](../../skills/matt/engineering/code-review/SKILL.md#L62-L74)
3. **没有证据证明三者组合比单独 Matt `code-review` 更好。** issue [#111](https://github.com/carl10086/ys-powers/issues/111) 的首轮实验只测了 `blast-radius`，没有测 `interrogate` 或三者组合。该样本中两种 treatment 都抓到 oracle；candidate 改善 uncertainty discipline，却没有增加 confirmed bug，并发生 dependency-tree isolation incident。因此当前最多能说“语义上有潜在增量”，不能说“实验上更好”。[#111 eval run 1](https://github.com/carl10086/ys-powers/issues/111#issuecomment-7192902417)
4. **最少改变 ownership 的组合是：Matt baseline 保持唯一 review owner，按风险触发独立 pstack passes。** 不创建总 wrapper，不重写四轴，不把 pstack pair 当第二套 review lifecycle。每个 pass 使用同一个已冻结 scope 和 intent，分别报告，不跨轴 merge/rerank。[Matt aggregation contract lines 76–89](../../skills/matt/engineering/code-review/SKILL.md#L76-L89) · [active source ownership](../../skills/pstack/README.md#L3-L20)
5. **当前下一步是完成隔离后的 `blast-radius` eval，再单独 eval `interrogate`；当前不应创建 wrapper，也不应 promotion。** 只有两个 leaves 分别显示稳定、可归因的增量后，才值得做 factorial composition eval。

## 证据分类与版本边界

本文使用以下标签：

- **事实**：由 pinned source、active source、first-party adapter、official runtime docs 或 issue #111 的记录直接支持。
- **实验结论**：只适用于已记录 fixture 与 treatment，不外推到其他仓库或 review 类型。
- **推断**：从 contract coverage 或 runtime mismatch 推导，尚未由对照实验确认。
- **建议**：对本仓库 Matt-first ownership 的选择。

本仓库 installer 只从 `skills/matt/engineering`、`skills/matt/productivity`、`skills/pstack` 与 `skills/local` 安装；`refer/` 不会进入 runtime。[`install/lib/config.py` lines 3–9](../../install/lib/config.py#L3-L9) 当前 active pstack manifest 只列出 `bro`、`why`、`how`、`teach`、`unslop`、`in-your-own-words`，没有 `interrogate` 或 `blast-radius`。[`skills/pstack/README.md` lines 11–18](../../skills/pstack/README.md#L11-L18) 因此本文说“技术上可用”是指：**若以后把经过 eval 的 leaf 作为 active pstack skill 安装，或在 eval 中明确读取 pinned reference contract**；不是说当前 runtime 已能用 `/interrogate` 或 `/blast-radius` 命名调用。

## 1. 来源与 ownership

### 1.1 Matt 的 Standards/Spec

**事实。** Matt pinned source 的 `code-review` frontmatter 和正文直接命名两轴：

- Standards：diff 是否符合 repo documented coding standards；
- Spec：diff 是否忠实实现 originating issue/spec；
- 两轴用 fresh-context subagents 并行运行，避免互相污染；
- 输出保持分离，不 merge、不跨轴 rerank。[Matt `code-review` lines 1–13, 76–89](../../refer/mattpocock-skills/skills/engineering/code-review/SKILL.md#L1-L13)

Matt upstream engineering catalog 也把 `code-review` 列为 model-invoked skill，并用同样的 Standards/Spec 描述；`implement` 与 `implement-spec` 都以它结束 review。[Matt engineering catalog lines 14–17, 21–33](../../refer/mattpocock-skills/skills/engineering/README.md#L14-L33) Active source 的 contract 与 pinned upstream 相同，并带独立 OpenAI adapter metadata `Review a diff on standards and spec`。[active `code-review`](../../skills/matt/engineering/code-review/SKILL.md#L1-L89) · [`agents/openai.yaml`](../../skills/matt/engineering/code-review/agents/openai.yaml#L1-L3)

这不是 pstack terminology 的本地别名，也不是从 pstack leaves 抽出的共同 contract。

### 1.2 pstack 是否有独立 `code-review`

**事实。** Pinned pstack README 自称列出 “all skills”，其中 review-related entries 是 `/blast-radius` 与 `/interrogate`，没有 `/code-review`。[pstack README lines 109–160](../../refer/cursor-plugins/pstack/README.md#L109-L160) `poteto-help` 的完整 routing table 同样没有 `/code-review`，并明确区分：`interrogate` review diff；`blast-radius` 看 diff 外 breakage 并证明 safety fact。[`poteto-help` lines 64–110](../../refer/cursor-plugins/pstack/skills/poteto-help/SKILL.md#L64-L110)

Host 自身可能另有同名能力，但不属于 pstack。例如 Cursor 当前 official skill catalog 有 built-in `/review`，Claude Code 有 bundled `/code-review`；这不能反推 pstack 提供了它们。[Cursor Agent Skills: built-in skills](https://cursor.com/docs/skills#built-in-cursor-skills) · [Claude Code skills: bundled skills](https://code.claude.com/docs/en/skills#bundled-skills)

## 2. 四个 review contracts

### 2.1 Matt Standards axis

| 项目 | Contract |
|---|---|
| 输入 | 用户给出的 fixed point；一次性固定的 `git diff <fixed-point>...HEAD` 与 `git log <fixed-point>..HEAD --oneline`；仓库内所有 coding-standard sources，至少包含存在的 `CODING_STANDARDS.md`、`CONTRIBUTING.md`；完整 Fowler smell baseline。[lines 17–23, 34–66](../../skills/matt/engineering/code-review/SKILL.md#L17-L66) |
| 判断 | 报告每个 documented-standard breach，并引用 rule；报告 baseline smells 并引用 hunk。Repo rule 覆盖 smell baseline；documented breach 可以是 hard finding，smell 永远是 judgement call；tooling 已 enforce 的内容跳过。[lines 38–66](../../skills/matt/engineering/code-review/SKILL.md#L38-L66) |
| 输出 | 一个不超过 400 words 的 Standards report；最终保留独立 `## Standards` heading，并给该轴 finding count 与轴内最严重 finding；不与 Spec rerank。[lines 62–66, 76–89](../../skills/matt/engineering/code-review/SKILL.md#L62-L89) |
| Side effects | Contract 只要求 resolve ref、读 diff/log、搜索 standards 和报告；不要求写代码、运行 repro 或应用 fixes。[lines 17–23, 58–80](../../skills/matt/engineering/code-review/SKILL.md#L17-L80) |

完整 smell baseline 是 Mysterious Name、Duplicated Code、Feature Envy、Data Clumps、Primitive Obsession、Repeated Switches、Shotgun Surgery、Divergent Change、Speculative Generality、Message Chains、Middle Man 与 Refused Bequest。[lines 43–56](../../skills/matt/engineering/code-review/SKILL.md#L43-L56)

### 2.2 Matt Spec axis

| 项目 | Contract |
|---|---|
| 输入 | 与 Standards 相同的 fixed-point diff/log；spec source 按 commit-message issue reference、用户路径、匹配 branch/feature 的 `docs/`、`specs/`、`.scratch/` 顺序解析。仍没有 spec 时询问；确认不存在时 skip 并报告 `no spec available`。[lines 17–32, 68–74](../../skills/matt/engineering/code-review/SKILL.md#L17-L32) |
| 判断 | 查 missing/partial requirements、unasked behavior/scope creep、看似实现但实现错误的 requirements；每条引用 spec line。[lines 68–72](../../skills/matt/engineering/code-review/SKILL.md#L68-L72) |
| 输出 | 一个不超过 400 words 的 Spec report；最终保留独立 `## Spec` heading，并给该轴 finding count 与轴内最严重 finding；不与 Standards rerank。[lines 68–80](../../skills/matt/engineering/code-review/SKILL.md#L68-L80) |
| Side effects | 可能通过 tracker workflow 读取 issue；contract 不要求运行真实代码、写 repro 或应用 fixes。[lines 25–32, 68–80](../../skills/matt/engineering/code-review/SKILL.md#L25-L32) |

**重要 contract inconsistency。** Frontmatter 声称支持 work-in-progress changes，但实际命令是 `<fixed-point>...HEAD`，且要求该 committed diff 非空，所以 unstaged/staged-but-uncommitted changes 不在 review scope。[lines 3, 19–23](../../skills/matt/engineering/code-review/SKILL.md#L3-L23) 这是 Matt baseline 自身要修正或在 eval harness 中冻结处理的 scope 问题，不是 pstack leaf 能自动修复的问题。

### 2.3 pstack `interrogate`

| 项目 | Contract |
|---|---|
| 输入 | 用户命名的 scope；否则是 base branch merge-base 到 branch diff，再延伸到 working tree。Intent 由用户消息、commits、PR description 经 `in-your-own-words` 重述；不清楚时询问。[`interrogate` lines 11–14](../../refer/cursor-plugins/pstack/skills/interrogate/SKILL.md#L11-L14) |
| 依赖 | 强依赖 `arena` Phase A steps 3/4、Phase B、Phase F；读取 `interrogate reviewers` model-role list；每个 adversary 为 `generalPurpose`；每个 adversary 有独立 worktree，并复制 scope 的 uncommitted changes。[lines 15–25](../../refer/cursor-plugins/pstack/skills/interrogate/SKILL.md#L15-L25) `arena` 自身要求选择 runner models、给每个 candidate 独立 worktree/output location、并行 fan-out 和最终 verify。[`arena` lines 11–24, 42–48](../../refer/cursor-plugins/pstack/skills/arena/SKILL.md#L11-L24) |
| 判断 | 每个 adversary 必须用 real code 的 failing test、repro script 或 command output 证明 finding；没有运行的 finding 不得提交。Coordinator 重跑 exact command；只有输出显示 failure 且 failure 违反 intent 才保留；同 root cause 合并。[`interrogate` lines 17–25](../../refer/cursor-plugins/pstack/skills/interrogate/SKILL.md#L17-L25) |
| 明确排除 | Style、naming、structure 与“需要未来变化才会发生”的风险会被 adversary brief 排除；no findings 是合法结果。[lines 17–20](../../refer/cursor-plugins/pstack/skills/interrogate/SKILL.md#L17-L20) |
| 输出 | `Intent`；每个 verified finding 的 command、output、违反 intent 的解释、发现它的 adversaries；按 adversary 统计 `Dropped` 数量和原因。No finding 时写 `no verified findings`。[lines 27–31](../../refer/cursor-plugins/pstack/skills/interrogate/SKILL.md#L27-L31) |
| Side effects | 创建 worktrees、复制 uncommitted changes、写 repro 到各自 worktree、运行真实代码/测试/命令；最终不应用 fixes。[lines 9, 17–23](../../refer/cursor-plugins/pstack/skills/interrogate/SKILL.md#L9-L23) Worktree 只隔离 checkout edits，不天然隔离 process、port、database、account 或其他 external state。[OMP subagents: Shared checkout or isolated workspace](https://omp.sh/docs/subagents#shared-checkout-or-isolated-workspace) |

### 2.4 pstack `blast-radius`

| 项目 | Contract |
|---|---|
| 输入 | Change 的 diff、added/changed/deleted symbols、行为变化、PR 与 commits；library source、pinned version、local patch；grep 看不到的 wire format、DB column、cross-language reader、feature flag、timing 和 downstream boundaries。[`blast-radius` lines 31–38](../../refer/cursor-plugins/pstack/skills/blast-radius/SKILL.md#L31-L38) |
| 依赖 | `how` 与 `why` 被称为 companions，但 prompt 没有强制调用它们；输出明确要求通过 `unslop`；big/wide change 可选升级为 `arena`。[lines 9–12, 38, 48](../../refer/cursor-plugins/pstack/skills/blast-radius/SKILL.md#L9-L12) |
| 判断 | 不把 caller list 当结果。找一两个 change safety 所依赖的事实；按 assertion、source line、failure-path walk-through、real-code script/test、running app 五级提升 confidence；分别列 confirmed risks、cleared risks，对无法证明的 safety fact 写 `unproven`。[lines 13–29, 33–45](../../refer/cursor-plugins/pstack/skills/blast-radius/SKILL.md#L13-L45) |
| 输出 | `What it does`、`The one fact it's safe because of`、`Risks`、`Cleared`、`Before you merge`；给 proof、`file:line`、likelihood/cost、cheapest test/repro。[lines 40–50](../../refer/cursor-plugins/pstack/skills/blast-radius/SKILL.md#L40-L50) |
| Side effects | Pull/read PR，写 script 或 test，运行 shipped library/function，可能运行 app；wide change 还可能启动 arena fan-out。[lines 29, 31–38](../../refer/cursor-plugins/pstack/skills/blast-radius/SKILL.md#L29-L38) Upstream contract 没有规定 scratch location、process/data/port isolation 或 cleanup，也没有规定 product tree 必须保持不变。[完整 pinned contract](../../refer/cursor-plugins/pstack/skills/blast-radius/SKILL.md#L1-L50) |

Issue #111 的 “scripts in scratch、product code unchanged、启动 app/service 前声明 isolation 与 cleanup” 是**本仓库 eval harness 增加的安全条件**，不是 upstream `blast-radius` 已有保证。[#111 body: Candidate run and promotion gate](https://github.com/carl10086/ys-powers/issues/111)

### 2.5 两个 pstack leaves 的关系

**事实。** 它们不是前后依赖，也不互相调用。`interrogate` 的 orchestration 建立在 `arena` 上，目标是让多个 configured models break scoped change，并用 rerun admission gate 过滤 findings；`blast-radius` 的核心是 diff 外 boundary 与 one-safety-fact proof，只有 wide change 才可选用 `arena`。[`interrogate` lines 15–25](../../refer/cursor-plugins/pstack/skills/interrogate/SKILL.md#L15-L25) · [`blast-radius` lines 31–38](../../refer/cursor-plugins/pstack/skills/blast-radius/SKILL.md#L31-L38)

pstack 自己给出的 close-call rule 是：`interrogate` reviews the diff，`blast-radius` looks for breakage outside the diff。[`poteto-help` lines 106–111](../../refer/cursor-plugins/pstack/skills/poteto-help/SKILL.md#L106-L111) 两者会在“运行真实代码”和“行为 failure”上有部分重叠，但 selection question、evidence unit 与 output schema 不同。

## 3. 语义兼容：补充、重复与缺口

| Review concern | Matt Standards/Spec | `interrogate` | `blast-radius` | 组合判断 |
|---|---|---|---|---|
| Repo documented standards | Standards 明确覆盖并引用 rule | 明确排除 style/naming/structure | 无此 contract | pstack pair 不能替代 Standards |
| Fowler smell baseline | Standards 固定 12 项 heuristic | 明确排除大部分结构类 finding | 无此 contract | 只有 Matt 覆盖 |
| Missing/partial spec requirement | Spec 明确覆盖 | 只有能运行并证明违反 intent 时可能覆盖行为子集 | 无此 contract | `interrogate` 不能替代完整 Spec |
| Scope creep | Spec 明确覆盖 | 若产生可运行的 wrong behavior，可能重复 | 通常不覆盖 | 有少量重叠 |
| Implementation looks wrong | Spec 可凭 diff 判断 | 必须以 run 证明，证据门更强 | 只在影响 safety fact/boundary 时覆盖 | `interrogate` 可验证或淘汰 Matt speculation |
| Diff 内 behavioral regression | 可能由 Spec 捕捉，但不要求 repro | 核心职责 | 不是核心 | `interrogate` 是潜在增量 |
| Diff 外 hidden coupling | 只有 spec/standard 恰好写明时才会命中 | Scope 可扩展但默认 brief 聚焦 break change | 核心职责 | `blast-radius` 是潜在增量 |
| Runtime evidence admission | 不要求 command/output | Coordinator rerun 每条 finding | 证明一两个 safety facts | 两个 leaves 都比 Matt 更强调 runtime proof |
| Unproven risk | Matt 允许 judgement call 与“looks wrong” | 直接 drop | 标记 `unproven` 并给 check path | 三者 uncertainty policy 不同，不应强行合并成一个 severity list |
| Apply fixes | 只报告 | 明确不 apply fixes | review contract 未要求修复 | 可保持 report-only，但 blast run 的 artifacts 需另加 cleanup policy |

上述 coverage 来自各自原始 prompts，而不是名称类比。[Matt axes prompts](../../skills/matt/engineering/code-review/SKILL.md#L62-L74) · [`interrogate` adversary brief](../../refer/cursor-plugins/pstack/skills/interrogate/SKILL.md#L17-L25) · [`blast-radius` steps](../../refer/cursor-plugins/pstack/skills/blast-radius/SKILL.md#L31-L48)

**推断。** 在 Matt-first flow 中，两个 pstack leaves 只能是补充 passes：

- `interrogate` 补的是“让不同 adversaries 尝试破坏 change，并只接纳 coordinator 可重跑的 behavioral failure”；
- `blast-radius` 补的是“追出 diff 外 boundary，并把 safety 归结为可证伪 fact”；
- 它们不能取代 repo standards ownership 或 originating spec completeness；
- Matt 的两轴报告必须继续分开。额外 passes 也应分别命名，避免把不同 evidence policy rerank 成一个总榜单。[Matt why-two-axes lines 82–89](../../skills/matt/engineering/code-review/SKILL.md#L82-L89)

## 4. Runtime compatibility

### 4.1 Named skill invocation

两个 pstack leaves 都有 `disable-model-invocation: true`。[`interrogate` lines 1–5](../../refer/cursor-plugins/pstack/skills/interrogate/SKILL.md#L1-L5) · [`blast-radius` lines 1–5](../../refer/cursor-plugins/pstack/skills/blast-radius/SKILL.md#L1-L5) Agent Skills open specification本身不定义该字段，它是 host extension。[Agent Skills specification: Frontmatter](https://agentskills.io/specification#frontmatter)

- Cursor：该 flag 关闭 automatic invocation，保留用户显式 `/skill-name`。[Cursor docs: Disabling automatic invocation](https://cursor.com/docs/skills#disabling-automatic-invocation)
- Claude Code：用户仍可 invoke，Claude 不能自行 invoke；pstack first-party Claude adapter 因而把 “run another pstack skill” 映射成直接读取 `<pstack>/skills/<name>/SKILL.md`，而不是依赖 Skill tool。[Claude Code: Control who invokes a skill](https://code.claude.com/docs/en/skills#control-who-invokes-a-skill) · [pstack Claude adapter lines 1–13](../../refer/cursor-plugins/pstack/docs/harness/claude-code.md#L1-L13)
- OMP：hidden skill 不参与 automatic matching，但在启用 skill commands 时仍可由用户 `/skill:<name>` 显式调用；`disable-model-invocation` 与 `hide` 同义。[OMP Skills: explicit invocation and frontmatter](https://omp.sh/docs/skills#find-and-use-an-installed-skill)

**结论。** 一个 local wrapper 只写“run `interrogate` then `blast-radius`”并不构成跨 runtime 保证。它至少要有 host-specific explicit load adapter。更直接的问题是，这两个 leaves 当前不在 active source，根本不会被 installer 安装；在 promotion 前，eval 必须明确读取 pinned reference file，而不是假装 named invocation 已存在。[installer source map](../../install/lib/config.py#L3-L9)

### 4.2 Fresh context

Matt 明确要求每个 axis 使用 fresh-context parallel subagent。[Matt `code-review` lines 6–13, 58–60](../../skills/matt/engineering/code-review/SKILL.md#L6-L13) `interrogate` 要求并行 adversaries，但它通过 `arena` 描述 task/output isolation，没有单独写出 “fresh context” 字样。[`interrogate` lines 15–20](../../refer/cursor-plugins/pstack/skills/interrogate/SKILL.md#L15-L20)

OMP 的 child session 不继承 main conversation，只接收 assignment 与显式 shared context，因此可以满足 fresh-context 目标。[OMP Subagents: child context](https://omp.sh/docs/subagents#when-delegation-helps) pstack Claude adapter 也把 Cursor `Task` 映射为 Claude `Agent`。[adapter lines 5–29](../../refer/cursor-plugins/pstack/docs/harness/claude-code.md#L5-L29) 组合时必须给每个 reviewer 同一份 frozen scope、intent 与 source pointers，不能依赖 parent 隐含对话。

### 4.3 Worktrees 与 uncommitted diff

`interrogate` 默认 scope 包含 working tree，并要求把 uncommitted changes 复制到每个 worktree。[`interrogate` lines 11–18](../../refer/cursor-plugins/pstack/skills/interrogate/SKILL.md#L11-L18) 这比 Matt 的 `<fixed-point>...HEAD` 更能表达 WIP，但 prompt 没有规定 staged、unstaged、untracked、ignored files、submodules 或 symlinked dependencies 的复制算法。

Runtime support 不等于默认启用。OMP subagents 默认共享 checkout，isolation mode 默认 `none`；开启 isolated workspace 后，仍只隔离 checkout edits，不是 security sandbox 或 external-state sandbox。[OMP Subagents: isolation defaults and limits](https://omp.sh/docs/subagents#shared-checkout-or-isolated-workspace) Claude Code 可给 subagent `isolation: worktree`，但 worktree 是 fresh checkout，需要单独处理 dependencies 与 gitignored files。[Claude Code Worktrees: setup and subagent isolation](https://code.claude.com/docs/en/worktrees#isolate-subagents-with-worktrees)

**建议的 scope normalization：** coordinator 先冻结一个 manifest，至少记录 fixed point、merge-base、HEAD、committed diff、staged diff、unstaged diff、需要纳入的 untracked paths 与 intent source。Matt baseline、`interrogate`、`blast-radius` 都消费同一 manifest。否则三份报告可能审的是三份不同 change。

### 4.4 Fixed point

Matt 没有 fixed point 必须询问，并在 fan-out 前验证 ref 可解析且 committed diff 非空。[Matt lines 17–23](../../skills/matt/engineering/code-review/SKILL.md#L17-L23) `interrogate` 默认从 base-branch merge-base 到 working tree，也允许 user-named scope；`blast-radius` 只说 read the change/PR/commits，没有定义统一 fixed-point algorithm。[`interrogate` lines 11–14](../../refer/cursor-plugins/pstack/skills/interrogate/SKILL.md#L11-L14) · [`blast-radius` lines 31–35](../../refer/cursor-plugins/pstack/skills/blast-radius/SKILL.md#L31-L35)

因此 wrapper 若不先解析并传同一 fixed point，会出现 scope drift。独立风险触发 pass 反而更容易显式写清 “review exactly `<fixed-point>` through `<head/worktree snapshot>`”。

### 4.5 Model roles

`interrogate` 的 multi-model claim 依赖 `interrogate reviewers` role list；pinned default 是 Fable、Opus、Gemini 三席。[`setup-pstack` lines 46–68](../../refer/cursor-plugins/pstack/skills/setup-pstack/SKILL.md#L46-L68) `arena` 要求 seat 被 runtime 拒绝时替换或 drop，但至少保留两个 runners。[`arena` lines 15–24](../../refer/cursor-plugins/pstack/skills/arena/SKILL.md#L15-L24)

Claude adapter 会把 Claude slug 映射为 Claude model/effort，而 Gemini 或其他 non-Claude slug 映射为省略 `model`、继承 session model；所以在 Claude runtime 中，configured seats 不一定保持 vendor diversity。[adapter lines 31–39](../../refer/cursor-plugins/pstack/docs/harness/claude-code.md#L31-L39) OMP 有 model roles 与 per-agent routing，但 pstack role file 不会自动变成 OMP roles，需要 adapter 或显式 agent definitions。[OMP Agents & model roles](https://omp.sh/docs/agents-and-roles)

**结论。** `interrogate` 可以在支持多个 child sessions 的 runtime 运行，但“different models”只有在 coordinator 记录每席 effective model、保持至少两个真实独立 seats，并报告 collapsed/dropped seats 时才成立。否则它是 multi-agent review，不是已证明的 multi-model review。

### 4.6 Probe isolation

Worktree 解决的是并发文件写入，不解决 package manager shared tree、shared package store mutation、process、port、database、account、network 或 credential side effects。[OMP Subagents: isolation is not a sandbox](https://omp.sh/docs/subagents#shared-checkout-or-isolated-workspace) `blast-radius` upstream 又要求真实 script/test/app proof，却没有 preflight 与 cleanup contract。[`blast-radius` lines 19–38](../../refer/cursor-plugins/pstack/skills/blast-radius/SKILL.md#L19-L38)

因此每个 runtime probe 在执行前必须声明：

1. checkout/worktree 与 dependency tree 是否独立；
2. package store/cache 是否只读或可安全共享；
3. process、port、database/schema、account、fixtures 与 credentials 的 namespace；
4. teardown command 与 crash recovery；
5. cleanup 后如何检查没有残留；
6. product code 与 tracked files 必须保持不变，临时 repro 只放 disposable scratch/worktree。

这些是本仓库 promotion gate，不应误写成 upstream 已提供。[#111 body](https://github.com/carl10086/ys-powers/issues/111)

## 5. Issue #111 已知实验事实

### 5.1 Run 1 说明了什么

**实验结论，只适用于 Drizzle `.env.local` fixture。**

- Fixture 的 hidden-breakage oracle 是 Drizzle Kit 没有加载 `.env.local`，导致 `pnpm db:migrate` 得到 `url: ''`；两个 treatments 都被禁止读取 later history。
- Matt baseline 的 Standards pass；Spec axis 从 plan/config mismatch 抓到该 failure，同时把 module-level postgres client 报成 definite hot-reload problem。
- `blast-radius` 也抓到 `.env.local` boundary；它运行 pinned postgres-js code，清除了“constructor 立即连接”的 claim，并把 hot-reload concern 降为 `unproven`。
- Blind score 的 oracle coverage 与 evidence quality 相同；candidate 的 uncertainty discipline 从 0 提升到 3，但 operational safety 从 2 降到 0；candidate 没有发现 baseline 漏掉的新 oracle-confirmed breakage。[#111 run 1 comment](https://github.com/carl10086/ys-powers/issues/111#issuecomment-7192902417)

### 5.2 Isolation incident

Candidate 在 detached fixture 内运行 `pnpm exec`，但 fixture 的 `node_modules` symlink 指向 live checkout；pnpm 按 historical lockfile relink 了共享 dependency tree。没有 tracked-file change，parent 仍需用 `pnpm install --frozen-lockfile` 恢复当前 dependencies，再删除 worktree。[#111 operational incident](https://github.com/carl10086/ys-powers/issues/111#issuecomment-7192902417)

**实验结论。** 这同时是 harness isolation error 与 candidate preflight failure。它证明“有 worktree”不等于“probe isolated”。它不证明所有 `blast-radius` runs 都不安全，也不证明 Matt baseline 更准确。

### 5.3 不能从 run 1 推出的结论

- 不能说 `blast-radius` 普遍没有增量；样本只有一个，且 baseline 在该样本已经从 Spec 捕捉 oracle。
- 不能说 candidate 普遍优于 baseline；它没有增加 confirmed finding，并发生 side effect。
- 不能评价 `interrogate`；它没有参加实验。
- 不能评价 `interrogate + blast-radius` 的 synergy 或 duplication；没有 composition treatment。
- 不能 promotion；issue 自身的 promotion gate 要求至少抓到一个 baseline 漏掉的 known hidden coupling，并且 isolation/cleanup 通过。[#111 promotion gate](https://github.com/carl10086/ys-powers/issues/111)

## 6. 五种架构评价

| 架构 | 能否工作 | 优点 | 主要缺口/风险 | Ownership 影响 | 当前判断 |
|---|---|---|---|---|---|
| **A. 只用 Matt `code-review`** | 是，前提是 fixed point 与 committed diff 正确 | 已 active；Standards/Spec coverage 完整；fresh-context 双轴；read-oriented，成本与 side effects 较低 | 不要求 runtime proof，不系统追 diff 外 hidden coupling；WIP 与 `<fixed>...HEAD` contract 不一致 | 最小 | **当前 baseline**。先修/隔离 scope mismatch |
| **B. 只用 pstack `interrogate + blast-radius`** | Runtime 适配后可运行，但语义上不是 Matt review 的替代品 | verified behavioral failures；hidden-coupling safety proof；uncertainty discipline 强 | 丢失 repo standards、Fowler baseline、完整 Spec completeness/scope contract；成本和 probe side effects 高；当前两个 leaves 未 active，`interrogate` 未 eval | 建立第二 review owner | **拒绝作为替代** |
| **C. 一个 wrapper 依次调用三者** | 条件式可行 | 理论 coverage 最宽；可统一 scope manifest | 必须解决 disabled leaf loading、fresh contexts、worktree/WIP copy、model roles、scope normalization、probe isolation；三轮输出 evidence policy 不同；成本高；目前没有 composition evidence | 新增 lifecycle owner，容易变第二 router | **现在不创建** |
| **D. 一个 local replacement 重写四 axes** | 可以实现代码/Prompt，但维护风险最高 | 可一次定义 scope、isolation、output schema | 复制 Matt/pstack upstream contracts，容易 drift；模糊 attribution 与 ownership；必须同步四套 prompt semantics；会违反“保持 Matt 分包/调用策略”的本仓库边界。[`skills/matt/README.md` lines 3–13](../../skills/matt/README.md#L3-L13) | 最大 | **拒绝** |
| **E. Matt baseline + 风险触发的独立 pstack passes** | 是，满足 adapter/isolation 条件即可 | Matt 继续拥有 Standards/Spec；只在有价值时支付 pstack 成本；reports 可分开；每个 leaf 可独立 eval/promotion/rollback | 仍需统一 scope manifest；未 promotion 的 leaf 只能按 reference eval；风险触发规则要明确 | 最小增量 | **推荐目标架构，但当前仍处 eval 阶段** |

### A. 只用 Matt `code-review`

这是唯一已经 active 且 ownership 清晰的 baseline。Issue #111 run 1 说明 Spec axis 有能力从 plan/config mismatch 抓到一个看似 diff 外的 tool boundary，但同一 run 也显示它会把未经 runtime proof 的 concern 报成 definite。[#111 run 1](https://github.com/carl10086/ys-powers/issues/111#issuecomment-7192902417) 单样本不能保证它总能捕捉 hidden coupling。

### B. 只用 pstack pair

语义上不可接受。`interrogate` 主动排除 style、naming、structure；`blast-radius` 关注 safety facts，不查 originating spec completeness。两者相加仍缺 Matt 两轴的核心 ownership。[`interrogate` lines 17–20](../../refer/cursor-plugins/pstack/skills/interrogate/SKILL.md#L17-L20) · [`blast-radius` lines 31–46](../../refer/cursor-plugins/pstack/skills/blast-radius/SKILL.md#L31-L46)

### C. 三者 wrapper

**推断。** 在一个 coordinator 先冻结 scope、然后运行 Matt 双轴、再运行 `interrogate`、最后运行 `blast-radius`，技术上可以 work。但顺序本身没有 proven benefit：`interrogate` 与 `blast-radius` 都会运行真实代码，可能重复 repro；若前者先运行，后者可能复用 evidence，也可能被前一轮 side effect 污染。若后者先运行，它的 safety fact 可能 bias adversaries。Fresh workspaces 可以减轻污染，却增加成本。

Wrapper 还会把 three-source orchestration 变成本地长期 owner。没有 individual signal 与 composition eval 时，这是先建 abstraction 再找需求。

### D. local four-axis replacement

这里的“四轴”只能解释为 Standards、Spec、adversarial verified failures、blast-radius safety proof。它们并非四个同构 axes：Matt 两轴允许 standards judgement 与 diff/spec reasoning；`interrogate` 只接纳 rerunnable failures；`blast-radius` 可以把关键事实留为 `unproven`。统一重写会丢失这些 admission-policy 差异，或被迫复制 upstream prompts。两种结果都比直接保留 source ownership 更差。

### E. Matt baseline + risk-triggered passes

这是最少改变 ownership 的方式：

1. 始终运行 Matt Standards/Spec baseline；
2. 只有小但跨 dependency/wire/storage/lifecycle/timing/feature-flag/language boundary 的 change 才触发 `blast-radius`；
3. 只有 high-risk behavior、contested implementation、难以由单 reviewer 信任，且存在可运行 repro path 时才触发 `interrogate`；
4. 每个 pass 使用同一 frozen scope/intent，但独立 fresh contexts/workspaces；
5. 输出保持 `Standards`、`Spec`、`Interrogate verified findings`、`Blast radius` 四个 sections，不合并 severity、不选单一 winner。

这保留了 Matt “axes 不互相遮蔽”的理由，也让 pstack leaves 可以逐个 promotion 或撤回。[Matt lines 76–89](../../skills/matt/engineering/code-review/SKILL.md#L76-L89)

## 7. 什么时候组合可能比 Matt-only 更好

**推断，尚未证明。** 至少满足以下全部条件时，组合才可能更好：

- Change 有 Matt axes 未显式覆盖的 boundary，例如 pinned dependency behavior、wire format、cross-language reader、DB schema consumer、lifecycle timing 或 feature flag。[`blast-radius` line 35](../../refer/cursor-plugins/pstack/skills/blast-radius/SKILL.md#L35-L35)
- 存在 production-equivalent、可重复、失败会明确违反 intent 的 probe；否则 `interrogate` 会 drop finding，`blast-radius` 只能写 `unproven`。[`interrogate` lines 19–25](../../refer/cursor-plugins/pstack/skills/interrogate/SKILL.md#L19-L25) · [`blast-radius` lines 21–29, 42–46](../../refer/cursor-plugins/pstack/skills/blast-radius/SKILL.md#L21-L29)
- Runtime 能提供真正独立的 checkout、dependency tree 与 external-state namespace，并在 cleanup 后验证无残留；worktree 本身不够。[OMP isolation limits](https://omp.sh/docs/subagents#shared-checkout-or-isolated-workspace)
- `interrogate` 的 effective model seats 被记录，至少两个 seats 可运行；若要声称 multi-model benefit，还要确保不全都 collapse 到 parent model。[pstack model roles](../../refer/cursor-plugins/pstack/skills/setup-pstack/SKILL.md#L59-L68)
- 额外 confirmed finding 或减少的 false certainty 的价值高于 model fan-out、runtime 与 operational risk。

即使这些条件成立，正确结论也是“在这类 risk profile 上增量有效”，不是“所有 change 都固定运行三者”。

## 8. 必须先完成的 eval

### 8.1 完成 `blast-radius` issue #111

1. 按 issue 计划运行第二个“无 known hidden breakage” fixture，使用完全独立 dependency tree；禁止 symlink live `node_modules`，package store 只读或单独 namespace。
2. 记录 confirmed、cleared、unproven、false positives、exact commands/outputs、runtime、tool calls 与 cleanup proof。
3. 另增至少一个 blinded historical hidden-coupling fixture。Promotion gate 仍要求 candidate 抓到 baseline 漏掉的 known coupling；run 1 没做到。
4. Candidate 只运行 pinned prompt 加预先声明的 harness safety constraints；不要在看到结果后修改 prompt。
5. 在 cleanup 后检查 process、port、dependency tree、data/account 与 scratch artifacts，而不只检查 `git status`。[#111 promotion/failure conditions](https://github.com/carl10086/ys-powers/issues/111)

### 8.2 单独 eval `interrogate`

在任何组合前，用固定 fixture set 对比：

- baseline：Matt `code-review`；
- variant：同一 baseline 后独立运行 pinned `interrogate`；
- 固定 scope manifest、intent、effective model seats、worktree-copy algorithm 与 probe isolation；
- blind judge 只看 oracle，不看 treatment name；
- 指标至少包括 unique confirmed bugs、rerun survival rate、dropped/fabricated findings、baseline speculation 被证实或清除的数量、runtime/cost、worktree/probe incidents；
- 至少包含一项有 reproducible behavioral regression、一项只有 standards/spec defect、一项没有 bug 的 fixture。

这样才能验证 `interrogate` 的 rerun gate 是否提供净增量，同时确认它不会因排除 style/structure 而被误当成 replacement。

### 8.3 最后才做 composition eval

只有两个 leaves 分别通过 gate 后，做四 treatment 的 factorial comparison：

1. Matt baseline；
2. Matt + `blast-radius`；
3. Matt + `interrogate`；
4. Matt + 两者。

所有 treatment 共享 fixture、scope manifest、oracle、isolation policy 与 blind scoring。比较 unique confirmed findings、重叠 findings、false certainty、side effects、runtime 与 cost。只有 treatment 4 显示超出 2/3 的增量，才有证据讨论 wrapper；否则保留独立 risk-triggered passes。

## 9. 最终建议

### 现在做什么

- 保持 `grill-with-docs → to-spec → to-tickets → implement → code-review` 为唯一 Matt-first lifecycle owner。
- 保持 `blast-radius` 为 candidate；先完成 issue #111 的隔离后续实验。
- 把 `interrogate` 作为独立 candidate 设计 eval，不与 `blast-radius` 同波引入。
- 在所有 eval 中先冻结 scope manifest，显式覆盖 committed 与 uncommitted state。
- 把 probe isolation/cleanup 作为 harness hard gate，而不是 report wording。
- 若将来 promotion，优先把每个 leaf 独立放入 `skills/pstack/`，保留 attribution 与 manual invocation；由使用场景按风险显式触发。

### 现在不做什么

- 不宣称 Standards/Spec 来自 pstack。
- 不用 `interrogate + blast-radius` 替换 Matt `code-review`。
- 不从 issue #111 的单样本宣称组合更好。
- 不 promotion `blast-radius`，不引入尚未 eval 的 `interrogate`。
- 不创建顺序调用三者的新 wrapper。
- 不本地重写“四轴 replacement”。
- 不把 worktree 当成 dependency、process、port、database 或 account isolation。
- 不把 collapsed model seats 宣称为 multi-model review。

**最终判断：能 work，但当前没有证据证明更好。** 最小 ownership change 是 Matt baseline 加风险触发、独立、可撤回的 pstack passes。当前应先完成 leaf-level eval 与 runtime isolation，不应先建 wrapper。

## Approved non-active draft

The line-reviewed draft lives at [`docs/pstack/deep-review-draft/SKILL.md`](./deep-review-draft/SKILL.md). It is documentation, not an installed skill. Promotion remains blocked until `blast-radius` completes issue #111 and `interrogate` passes an independent eval.
