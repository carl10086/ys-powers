# pstack 对五阶段主流程的优化研究

## 结论

当前五阶段全部由 Matt active source 拥有。pstack 与 local skills 没有任何一个阶段的 ownership。pstack 中只有两个候选值得进入下一波有界实验：

1. **`blast-radius`**：最高优先级。它补充 `code-review` 没有覆盖的 diff 外 hidden coupling，并要求把 change 安全所依赖的事实运行到可证明或明确标成 `unproven`。
2. **`principle-prove-it-works`**：第二优先级。它补充 `implement` 只要求 typecheck/tests、没有要求实际运行 user-facing artifact 的缺口。

这两个结论仍是 **prototype/eval 建议，不是 promotion 决策**。其余直接相关候选要么重复 active `grilling`、`prototype`、`domain-modeling`、`codebase-design`、`tdd`、`diagnosing-bugs` 和 `code-review`，要么依赖 Cursor model router、worktree fan-out、TLA+/Java 或 `.cursor/skills/` 生成约定。它们不进入下一波。

更重要的是，当前主流程最严重的三个问题不是 pstack 能补的能力缺口，而是 `implement → code-review` 自身的 contract mismatch：

- `implement` 要求先 review、后 commit；`code-review` 只审 `<fixed-point>...HEAD`，因此看不到尚未 commit 的实现。
- `implement` 调用 review 时没有提供后者必需的 fixed point。
- 单-ticket `implement` 没有修复 review findings 或复审的闭环。

这些问题应单独修正，不能用新增 pstack skill 掩盖。

## 范围、版本与判断标签

本文只使用 owner 的 source、official docs 和 first-party repository。调查基线如下：

| Source | 调查时 pinned commit | 本地边界 |
|---|---|---|
| Matt Pocock skills | [`abeeaf95660ba9e8b7c753eb38f441ca707a8823`](https://github.com/mattpocock/skills/commit/abeeaf95660ba9e8b7c753eb38f441ca707a8823) | active `skills/matt/`；pin 与 `/teach` cutover 见 [`skills/matt/README.md`](../../skills/matt/README.md#L3-L11) |
| Cursor pstack | [`41e400932eca14f289e7db717a70455256b6d388`](https://github.com/cursor/plugins/commit/41e400932eca14f289e7db717a70455256b6d388) | read-only `refer/cursor-plugins/pstack/`；plugin `0.15.48`，author Lauren Tan，MIT；active 子集与 pin 见 [`skills/pstack/README.md`](../../skills/pstack/README.md#L3-L20)，版本与作者见 [`plugin.json`](../../refer/cursor-plugins/pstack/plugin.json#L3-L11) |
| pstack last-touch | [`9e278fe4d4ecd8bfe98b1b79bf4be662efb338cc`](https://github.com/cursor/plugins/commit/9e278fe4d4ecd8bfe98b1b79bf4be662efb338cc) | 上述 repository HEAD 中最后修改 `pstack/` 的 commit |
| local skills | 不对应 upstream pin | active `skills/local/`，边界见 [`skills/local/README.md`](../../skills/local/README.md#L1-L11) |

本文使用三个标签：

- **事实**：prompt、frontmatter、source 或 official docs 直接陈述的行为。
- **推断**：由两个以上事实得出的 workflow 影响。
- **建议**：需要 eval 才能升级为 promotion 决策的选择。

## 当前五阶段：输入、输出与 ownership

### 1. `grill-with-docs`

- **Active owner：** Matt engineering。wrapper 只要求调用 `grilling` 与 `domain-modeling` 两个 skills。[`grill-with-docs` lines 1–7](../../skills/matt/engineering/grill-with-docs/SKILL.md#L1-L7)
- **输入：** 当前 idea、plan 或 design，repo 中的 code/domain docs，以及用户逐轮回答。
- **处理：** `grilling` 把问题组织成 design tree，按已满足 prerequisites 的 frontier 分轮提问，每题给推荐答案；环境事实由 agent 查，真正的 product/design decisions 留给用户。[`grilling` lines 6–30](../../skills/matt/productivity/grilling/SKILL.md#L6-L30)
- **输出：** 用户确认过的 shared understanding；`domain-modeling` 同时校准术语、用具体 scenario 压测边界、与代码交叉检查，并即时更新 glossary。[`domain-modeling` lines 42–64](../../skills/matt/engineering/domain-modeling/SKILL.md#L42-L64)
- **Side effects：** 只有在有内容时才创建或更新 `GLOSSARY.md`；ADR 仅在 hard to reverse、surprising、真实 trade-off 三项同时成立时生成。[`domain-modeling` lines 40, 66–74](../../skills/matt/engineering/domain-modeling/SKILL.md#L40-L74)
- **Runtime assumptions：** `grill-with-docs` 是 manual-only，并假设 runtime 能从一个 skill 调用另外两个 skills。它还假设当前存在 workspace；无 workspace 时 canonical router 改用 `grill-me`。

### 2. `to-spec`

- **Active owner：** Matt engineering。
- **输入：** 当前 conversation 和已有 codebase understanding；它明确禁止重新做一次 interview。[`to-spec` lines 7–13](../../skills/matt/engineering/to-spec/SKILL.md#L7-L13)
- **处理：** 找到尽可能高、尽可能少的 test seams，优先复用已有 seam，并让用户确认；使用 glossary vocabulary、遵守相关 ADR。[`to-spec` lines 13–19](../../skills/matt/engineering/to-spec/SKILL.md#L13-L19)
- **输出：** issue tracker 中带 `ready-for-agent` label 的 spec，包括 Problem Statement、Solution、User Stories、Implementation Decisions、Testing Decisions、Out of Scope 和 Further Notes。[`to-spec` lines 19–73](../../skills/matt/engineering/to-spec/SKILL.md#L19-L73)
- **Side effects / dependencies：** 发布 tracker issue；依赖 `setup-matt-pocock-skills` 已配置 tracker 与 labels。通常不写 code/path；prototype 产出的 decision-rich state machine、schema 或 type shape 是明示例外。[`to-spec` lines 9, 55–57](../../skills/matt/engineering/to-spec/SKILL.md#L9-L57)

### 3. `to-tickets`

- **Active owner：** Matt engineering。
- **输入：** conversation、plan、spec，或 spec path / issue URL；若给 reference，读取完整 body 和 comments。[`to-tickets` lines 15–21](../../skills/matt/engineering/to-tickets/SKILL.md#L15-L21)
- **处理：** 切成 tracer-bullet vertical slices。每片贯穿相关层、独立 demo/verify、适合一个 fresh context，并显式声明 blockers；wide mechanical refactor 使用 expand–migrate–contract，而不是强行 vertical slice。[`to-tickets` lines 25–40](../../skills/matt/engineering/to-tickets/SKILL.md#L25-L40)
- **输出：** 用户确认后的 task graph。Local tracker 写 `.scratch/<feature>/issues/` 中一 ticket 一文件；real tracker 创建 issues/sub-issues 和 blocking edges，通常加 `ready-for-agent`。[`to-tickets` lines 42–67](../../skills/matt/engineering/to-tickets/SKILL.md#L42-L67)
- **Side effects / dependencies：** 写 `.scratch/` 或 tracker，但明确不关闭或修改 parent issue；同样依赖 setup 提供 tracker contract。

### 4. `implement`

- **Active owner：** Matt engineering。
- **输入：** 用户给出的 spec 或 ticket；tracker reference 必须先 fetch 并报告 title。[`implement` lines 7–9](../../skills/matt/engineering/implement/SKILL.md#L7-L9)
- **处理：** 在预先约定的 seams 上尽可能调用 active Matt `tdd`；定期 typecheck 和运行单 test，最后跑 full suite；再调用 `code-review`。[`implement` lines 11–15](../../skills/matt/engineering/implement/SKILL.md#L11-L15)
- **输出：** production/test changes、review report 和 current branch 上的 commit。[`implement` lines 15–17](../../skills/matt/engineering/implement/SKILL.md#L15-L17)
- **Side effects / runtime assumptions：** 修改代码、运行 repo commands、调用 sub-skill、commit。它没有定义真实 app/CLI/service 的 user-path verification，也没有定义 review finding 的 fix/re-review loop。

### 5. `code-review`

- **Active owner：** Matt engineering。
- **输入：** 用户指定的 fixed point、originating spec/issue 和 repo standards。没有 fixed point 必须询问。[`code-review` lines 17–32](../../skills/matt/engineering/code-review/SKILL.md#L17-L32)
- **处理：** 固定运行 `git diff <fixed-point>...HEAD` 与对应 `git log`；在 fresh contexts 并行运行 Standards 和 Spec 两轴。[`code-review` lines 19–23, 58–74](../../skills/matt/engineering/code-review/SKILL.md#L19-L74)
- **输出：** 分开的 `## Standards` 与 `## Spec` 报告，不 merge 或跨轴 rerank；最后给每轴 finding count 和该轴最严重问题。[`code-review` lines 76–89](../../skills/matt/engineering/code-review/SKILL.md#L76-L89)
- **Side effects / runtime assumptions：** 只读 Git/repo/tracker 并启动 reviewers；prompt 没有修改代码、运行真实 user flow、修复 findings 或 commit 的步骤。

### Ownership 结论

五个阶段均由 Matt 拥有。第一阶段组合了 Matt productivity `grilling` 与 Matt engineering `domain-modeling`；第四阶段组合 Matt `tdd` 和第五阶段。Active pstack 的 `bro`、`why`、`how`、`teach`、`unslop`、`in-your-own-words`，以及 local 的 browser/解释 skills 都是相邻能力，不拥有主流程阶段。[Matt catalog](../../skills/matt/engineering/README.md#L5-L32) · [pstack active list](../../skills/pstack/README.md#L11-L20) · [local list](../../skills/local/README.md#L5-L11)

## 不要把已有能力误报为缺口

### Grilling 与 prototype 已有完整路由

Canonical `ask-matt` 已明确规定：若 grilling 的问题不能在 conversation 中解决，需要 runnable answer，就通过 `handoff → prototype → handoff` detour，随后把 observation 带回原 idea thread。[`ask-matt` lines 15–30](../../skills/matt/engineering/ask-matt/SKILL.md#L15-L30)

Active Matt `prototype` 也已区分 logic/state 与 UI 两类 artifact；产物必须 throwaway、易运行、默认无 persistence、不做 production polish，并把验证后的 decision 回写 issue。[`prototype` lines 8–26](../../skills/matt/engineering/prototype/SKILL.md#L8-L26)

因此：

- pstack `sharpen` 的“可由 experiment 解决的 choice 先 prototype”不是新 capability。
- `principle-exhaust-the-design-space` 的 2–3 个 competing prototypes 与 active UI prototype 的多 variants、`codebase-design` 的 design-it-twice 已重叠。
- `reframe` 的 fuzzy terminology 与 active `domain-modeling` 已有直接 overlap。

### Test、debug、architecture 与 retro 也已有 owner

- `tdd` 已要求 public behavior、pre-agreed seams、vertical red/green slices。[`tdd` lines 12–38](../../skills/matt/engineering/tdd/SKILL.md#L12-L38)
- `diagnosing-bugs` 已要求先构造 red-capable executable loop，再 hypothesis、instrument、fix 和 regression test。[`diagnosing-bugs` lines 18–66](../../skills/matt/engineering/diagnosing-bugs/SKILL.md#L18-L66)
- `codebase-design` 已提供 deep module、small interface、seam、adapter 与 design-it-twice vocabulary。[`codebase-design` lines 6–28, 111–114](../../skills/matt/engineering/codebase-design/SKILL.md#L6-L114)
- `retro` 已把重复问题路由到 automated checks、coding standards 或更好的 information access，且机械规则优先 deterministic enforcement。[`retro` lines 13–25](../../skills/matt/engineering/retro/SKILL.md#L13-L25)
- Browser-facing work 由 OMP browser 与 Chrome DevTools MCP 提供 runtime verification。交付规则要求按 spec 驱动真实 user flow，并报告 observed evidence。[OMP browser runtime](../omp/devtools-mcp-integration.md)

## 上游 59 个 skills 的筛选

Pinned pstack snapshot 有 59 个顶层 `SKILL.md`。以下分组完整枚举 inventory；只对直接影响五阶段的 12 项做深入分析。

上游没有可直接替换 `to-spec` 或 `to-tickets` 的 planning skill。官方明确说明 pstack 不提供 planning skills；需要 plan 时交给 `poteto-mode`，且不是 default。[pstack README lines 269–271](https://github.com/cursor/plugins/blob/41e400932eca14f289e7db717a70455256b6d388/pstack/README.md#L269-L271) 因而本文不会把 router/playbook 当作 spec 或 ticket ownership 的候选。

### 已 active，不再作为 promotion candidate（6）

`bro`、`how`、`in-your-own-words`、`teach`、`unslop`、`why`。

### 与五阶段直接相关，深入分析（12）

`architect`、`benchmark-checklist`、`blast-radius`、`create-verification-skill`、`interrogate`、`principle-exhaust-the-design-space`、`principle-prove-it-works`、`reframe`、`sharpen`、`show-me-your-work`、`statechart`、`tdd`。

### 条件式 verification family，不是通用主链步骤（3）

`create-formal-verification-skill`、`maintain-formal-verification-skill`、`maintain-verification-skill`。它们只在项目已经选定高代价 property 或已有 generated verification skill 时成立，不应因 skill 存在而推断所有项目都有此缺口。

### Router、orchestration 与个人工作方式（9）

`arena`、`automate-me`、`figure-it-out`、`poteto-help`、`poteto-mode`、`recall`、`reflect`、`setup-pstack`、`swarm`。

### 与本主流程不直接相关或已决策（7）

`correct`、`ketchup`、`ketchup-video`、`make-bot-ui`、`no-comments`、`technical-writing`、`typescript-best-practices`。

`correct` 按既有决定继续 Reference only；本文不重新讨论。

### 其余 principle leaves（22）

`principle-attack-the-premise`、`principle-boundary-discipline`、`principle-build-the-lever`、`principle-encode-lessons-in-structure`、`principle-experience-first`、`principle-explain-the-number`、`principle-fix-root-causes`、`principle-foundational-thinking`、`principle-guard-the-context-window`、`principle-laziness-protocol`、`principle-make-operations-idempotent`、`principle-migrate-callers-then-delete-legacy-apis`、`principle-minimize-reader-load`、`principle-model-the-domain`、`principle-never-block-on-the-human`、`principle-outcome-oriented-execution`、`principle-redesign-from-first-principles`、`principle-separate-before-serializing-shared-state`、`principle-sequence-verifiable-units`、`principle-subtract-before-you-add`、`principle-test-behavior-not-implementation`、`principle-type-system-discipline`。

这些 leaves 可作 vocabulary/reference，但整体导入会形成第二套常驻 policy。pstack 官方也把 `poteto-mode` 定义为读取 task、匹配 playbook、再 route leaves 的主入口，而不是独立小补丁。[pstack README lines 34–53, 97–111](https://github.com/cursor/plugins/blob/41e400932eca14f289e7db717a70455256b6d388/pstack/README.md#L34-L111)

## 12 个直接候选的 prompt、依赖与风险

所有 12 项的 upstream frontmatter 都是 `disable-model-invocation: true`。它们在 Cursor 中是 explicit-only；跨 runtime 的 named composition 不能假定原样可用。pstack 的 Claude adapter 明确把 `Task` 映射为 `Agent`、把 nested skill invocation 改成直接读取目标 `SKILL.md`，并为 readonly/worktree/model slug 提供额外映射。[Claude adapter lines 1–38](https://github.com/cursor/plugins/blob/41e400932eca14f289e7db717a70455256b6d388/pstack/docs/harness/claude-code.md#L1-L38)

| Candidate | 完整 prompt 的核心动作 | Dependencies / side effects / runtime assumptions | 与 active overlap | 结论 |
|---|---|---|---|---|
| `architect` | trace 所有 touched systems；画两个 type/signature/module shapes；以 single state owner、single task path、least caller knowledge 选型；大型争议设计升级 `arena`。 | 核心只读；升级路径依赖 `arena`、model roles、隔离输出。 | `codebase-design` 已有 seam/depth/design-it-twice；`to-spec` 已定 test seams。 | Reference only。selection rubric 可借鉴，不新增入口。[source](https://github.com/cursor/plugins/blob/41e400932eca14f289e7db717a70455256b6d388/pstack/skills/architect/SKILL.md#L7-L11) |
| `benchmark-checklist` | 先固定 claim、读 harness、查 machine load；检查 limiter、tuning、physical bound、errors、repeatability、end-to-end relevance 和 work 是否实际发生。 | 运行 benchmark/profiler；假设 `uptime`、`nproc`，部分建议是 Linux-only；可能修改 harness 增加 counters。 | `diagnosing-bugs` perf branch 已要求 baseline/profiler，但没有同样完整的 measurement-validity checklist。 | 条件式 Reference。仅 perf ticket 有直接价值，不进入通用下一波。[source](https://github.com/cursor/plugins/blob/41e400932eca14f289e7db717a70455256b6d388/pstack/skills/benchmark-checklist/SKILL.md#L7-L39) |
| `blast-radius` | 不停在 callers；找 1–2 个 safety facts，沿 source line → impossible path → real-code run → running app 提升 confidence；分开 confirmed risks 与 cleared risks。 | 依赖 `how`、`why`；输出经 `unslop`；wide change 可选 `arena`。会 pull/read PR、读 pinned dependency/local patch、写并运行 script/test，可能启动 app。Prompt 没有 isolation/cleanup contract。 | `code-review` 只查 Standards/Spec，没有 diff 外 hidden coupling 或 runtime proof。 | **下一波 #1**。[source](https://github.com/cursor/plugins/blob/41e400932eca14f289e7db717a70455256b6d388/pstack/skills/blast-radius/SKILL.md#L7-L50) |
| `create-verification-skill` | 从 repo 推导 Surface/Run/Drive/Observe/Isolate，生成 Launch/Doctor/Drive/Evidence/Cleanup 与 feature map，并完整跑一次。 | 写 `.cursor/skills/verify-*`；可能先修 build/start、增加 scaffolding、运行 app 和清理；后续依赖 `maintain-verification-skill`。Cursor path 与 skill generation 是强 runtime assumption。 | Browser 项目已有 local DevTools skill；debug 已会建 executable loop。独特性在跨项目持久 verification runbook。 | 条件式 Reference。只有真实项目反复缺 verifier 才单独 eval。[source](https://github.com/cursor/plugins/blob/41e400932eca14f289e7db717a70455256b6d388/pstack/skills/create-verification-skill/SKILL.md#L7-L44) |
| `interrogate` | adversaries 尝试 break change/design；每条 finding 必须附 exact command/output；coordinator 重跑，只有违反 intent 的真实 failure 保留；不修复。 | 强依赖 `in-your-own-words`、`arena` Phase A/B/F、`interrogate reviewers` model role、多个 worktrees 和 uncommitted-change copy。 | `code-review` 已有 parallel two-axis review；独特增量是 rerunnable-failure admission gate。 | Reference only。完整 orchestration runtime 风险过高；先不与 `blast-radius` 同波引入。[source](https://github.com/cursor/plugins/blob/41e400932eca14f289e7db717a70455256b6d388/pstack/skills/interrogate/SKILL.md#L7-L31) |
| `principle-exhaust-the-design-space` | novel UI/architecture 无 precedent 时做 2–3 个 competing prototypes 并 side-by-side 比较；也覆盖依赖 feel 的 product design。 | 会生成多个 throwaway artifacts；prompt 没有 selection rubric、cleanup 或 evidence format。 | `ask-matt` 已有 prototype detour；active UI prototype 已要求 multiple variants；`codebase-design` 已有 design-it-twice。 | Reference only，属于重复 trigger。[source](https://github.com/cursor/plugins/blob/41e400932eca14f289e7db717a70455256b6d388/pstack/skills/principle-exhaust-the-design-space/SKILL.md#L1-L9) |
| `principle-prove-it-works` | 完成后检查 real artifact：运行 feature、读 actual value、inspect diff；拒绝 mtime/self-report/cache/compile 等 proxy；尽量 script。 | 会运行真实 feature、读 state、写 script/output；prompt 没有 auth、data isolation、teardown 或 privacy guard。 | Browser skill 覆盖 web，但 generic `implement` 没有 CLI/service/desktop/library 的 real-artifact gate。 | **下一波 #2**。[source](https://github.com/cursor/plugins/blob/41e400932eca14f289e7db717a70455256b6d388/pstack/skills/principle-prove-it-works/SKILL.md#L7-L11) |
| `reframe` | ambiguity 时先列 2–3 个可能问题和 discriminating sign；再给 8–12 个按 design impact 排序的 expert terms、neighboring-field analogies 及 break points，最后重写描述。 | 需要 web access，必须逐个打开并验证链接；会把外部 vocabulary 带入 domain docs。 | `domain-modeling` 已处理 overloaded terms、scenario、code cross-check 与 glossary。 | Reference only。固定 8–12 terms 有 padding 和污染 ubiquitous language 的风险。[source](https://github.com/cursor/plugins/blob/41e400932eca14f289e7db717a70455256b6d388/pstack/skills/reframe/SKILL.md#L7-L16) |
| `sharpen` | 以 top professional、raw material、methods/tools、external proof 四问重写 prompt；empirical choice 先 prototype，preference 留给 operator。 | Prompt-only，无直接 file side effect；会扩大 task framing，且只重写、不执行。 | `grilling` 已分事实与用户决策；`ask-matt` 已 route runnable question 到 prototype。 | Reference only。其 prototype-routing kernel 已存在。[source](https://github.com/cursor/plugins/blob/41e400932eca14f289e7db717a70455256b6d388/pstack/skills/sharpen/SKILL.md#L7-L16) |
| `show-me-your-work` | 维护 append-only TSV decision log，逐 row 指向 evidence；结束时审 transcript，再做 cross-vendor review。 | 写 `decisions.tsv`/`.audit/`；依赖 bundled script、Cursor transcript path、另一个 vendor model、`unslop` 与 `poteto-mode`；可能 commit log。 | Specs、tickets、commits 已承担主流程 decision/evidence trail。 | Reference only。只适合长时间无人值守 run，不是单-ticket 主链默认。[source](https://github.com/cursor/plugins/blob/41e400932eca14f289e7db717a70455256b6d388/pstack/skills/show-me-your-work/SKILL.md#L7-L82) |
| `statechart` | 在 repo 外写 TLA+ spec/config，运行 TLC，生成 Mermaid 与 shortest counterexample path，并回放到真实代码。 | TypeScript runtime；首次运行通过 mise 安装 TLC/Java并联网；依赖 bundled compiler/scripts 和 Pele；有 state bounds/model drift 风险。 | Active logic prototype 已能让用户驱动 state model；formal exhaustive exploration 是窄域增量。 | 当前主流程明确不适合。只有具体高风险 concurrency/state property 才另立 formal eval。[source](https://github.com/cursor/plugins/blob/41e400932eca14f289e7db717a70455256b6d388/pstack/skills/statechart/SKILL.md#L7-L82) |
| `tdd` | bug 有 cheap local path 时先写 focused regression test、看 red、最小修复、看 green；没有 practical path 就用最近的 executable check。 | 运行 tests/scripts/browser；本身低 runtime coupling。 | 与 active Matt `tdd` 同名冲突；Matt 版本覆盖 feature 与 bug、seam agreement 和 vertical slices，范围更完整。 | 明确不适合，不能 duplicate register。[source](https://github.com/cursor/plugins/blob/41e400932eca14f289e7db717a70455256b6d388/pstack/skills/tdd/SKILL.md#L7-L42) |

## 当前流程的真实缺口

### G1. 未 commit 的实现可能不在 review diff 中

**事实：** `implement` 的顺序是 full suite → `code-review` → commit；`code-review` 固定审 `git diff <fixed-point>...HEAD`，且要求非空。[`implement` lines 13–17](../../skills/matt/engineering/implement/SKILL.md#L13-L17) · [`code-review` lines 17–23](../../skills/matt/engineering/code-review/SKILL.md#L17-L23)

**推断：** 严格按 prompt 执行时，当前 uncommitted changes 不进入 `<fixed-point>...HEAD`。Review 可能只看到旧 commits，或因 empty diff 失败。

**建议：** 这是 native contract bug。先在 Matt workflow ownership 内解决；`blast-radius` 也不能自动修复错误 diff scope。

### G2. `implement` 没有提供 review 所需 fixed point

**事实：** `code-review` 没有 fixed point 就必须询问；`implement` 只说调用 skill，没有捕获起始 SHA 或传 branch/base。[`code-review` lines 17–23](../../skills/matt/engineering/code-review/SKILL.md#L17-L23) · [`implement` lines 15–17](../../skills/matt/engineering/implement/SKILL.md#L15-L17)

**推断：** 自动 handoff 不完整，review 会中断要求额外输入。

### G3. 单-ticket 路径没有 finding closure

**事实：** `code-review` 只报告；`implement` review 后直接 commit。相比之下，active `implement-spec` 明确要求用 fresh implementer 修复所有 review issues。[`code-review` lines 76–89](../../skills/matt/engineering/code-review/SKILL.md#L76-L89) · [`implement-spec` lines 34–40](../../skills/matt/engineering/implement-spec/SKILL.md#L34-L40)

**推断：** 单-ticket flow 可能在已知 finding 未修复时 commit。

### G4. Tests/typecheck 不能替代 real-artifact proof

**事实：** `implement` 只要求 typecheck、test files 和 full suite。Browser skill 是独立 adjacent capability，不是 generic implementation completion gate。

**推断：** CLI、service、desktop 与非浏览器 integration 可以 tests green 但真实入口失败。`principle-prove-it-works` 对应的是一个真实缺口，但必须增加 isolation/cleanup guard，不能照抄即用。

### G5. Review 没有 diff 外 hidden-coupling 轴

**事实：** `code-review` 两轴分别是 repo standards 与 originating spec；没有 dependency implementation、wire format、other-language reader、timing、feature flag 或 running-app proof 轴。[`code-review` lines 6–11, 62–72](../../skills/matt/engineering/code-review/SKILL.md#L6-L72)

**推断：** 一个符合 standards 且实现 spec 的 diff，仍可能破坏 diff 外 consumer。`blast-radius` 的 safety-fact proof 是直接增量。

## 分层结论

### A. 优先 grilling/prototype：只研究 2 项

这里的 “prototype” 指 blind、bounded eval，不是直接复制 skill。

#### 1. `blast-radius`

- **确切插入位置：** `code-review` 的 Standards/Spec 报告之后，merge/ship 之前。它不替代任何 axis，只增加一个按风险触发的 hidden-coupling proof pass。
- **Ownership：** 不改变五阶段 ownership。若 eval 通过，可作为独立 pstack leaf；不能修改 Matt source 或增加第二 router。
- **适用 trigger：** small-looking change 涉及 dependency behavior、wire/data format、lifecycle/timing、feature flag、cross-language consumer，或 reviewer 对 safety fact 不确定。
- **验收场景：** 选择至少 2 个历史小 diff，其中 1 个有已知 diff 外 breakage。Baseline 是现有 `code-review`，variant 再运行 candidate。Variant 必须找到真实 boundary、陈述可证伪 safety fact、运行 production-equivalent probe，并把 confirmed / cleared / unproven 分开。
- **Promotion gate：** 至少多抓到一个 baseline 漏掉的已知 coupling；没有增加 fabricated callers；probe 走实际 shipped library/function/path；speculative findings 减少或明确降为 `unproven`。
- **失败判据：** 只列 callers；用 mock/重实现代替 production path；为了“证明”而修改 product code；把 search miss 当安全保证；没有 isolation/cleanup；wide change 自动升级 `arena`；成本高于 finding value。
- **Runtime guard：** 下一波禁用 optional `arena`，只用当前 runtime 的单 coordinator；任何 script 放 scratch、默认不 commit；运行 app 前声明数据/端口/账号隔离与 cleanup；私密输出不得进入公开 writeup。

#### 2. `principle-prove-it-works`

- **确切插入位置：** `implement` 的 full suite 之后、`code-review` 之前。它补充 completion gate，不替代 TDD/tests/review。
- **Ownership：** 仍由 Matt `implement` 拥有 implementation；下一波只评估 5 行 evidence contract。由于 active Matt source 要保持 upstream prompt，实验不能先改 `implement`；使用显式、有界 run。
- **适用 trigger：** ticket 有明确 user-facing artifact，且能在 isolated local/test environment 中运行。
- **验收场景：** 选择 2 个 tests/typecheck 均通过的历史 change，其中至少 1 个真实 CLI/API/UI flow 曾失败。Baseline 按现有 `implement` checks；variant 再运行真实入口并读取实际 side effect/value。
- **Promotion gate：** variant 能抓到 proxy-pass/real-fail；命令可重复；evidence 直接对应 acceptance criterion；执行后没有残留 process/data；browser case 不重复 local browser skill 已提供的同一证据。
- **失败判据：** 只是重跑 unit tests 或 compile；只看 screenshot 最终态而不驱动 action；依赖人工不可重复操作；污染真实账号/数据；无 teardown；所有样本都被现有 browser/TDD flow 等价覆盖。
- **Runtime guard：** 每次先定义 artifact、isolated state、exact command、expected observation 与 cleanup；不能从该 5 行 prompt 推断这些 guard 已存在。

### B. 继续 Reference only

- `architect`：selection rubric 有用，但能力被 `codebase-design`/`to-spec` 覆盖。
- `benchmark-checklist`：仅 perf task 条件触发；若未来单独研究 performance workflow，再独立 eval。
- `create-verification-skill` / `maintain-verification-skill`：只有真实项目反复缺少 executable verifier 时才评估 runtime-neutral runbook，不生成 `.cursor/skills/`。
- `interrogate`：proof admission gate 有价值，但完整 orchestration 依赖 `arena`、model roles、worktrees；先让低风险 `blast-radius` 证明需求。
- `principle-exhaust-the-design-space`、`sharpen`：canonical Matt router 已有 grilling ↔ prototype detour。
- `reframe`：domain-modeling 已拥有 terminology；仅借鉴 differential diagnosis 与 analogy-break 写法。
- `show-me-your-work`：长时间无人值守 work 可参考；不把 TSV/transcript/cross-vendor ceremony 加到普通 ticket。
- formal verification family：仅在明确 property、高 failure cost、tests 难覆盖且有人维护 model 时单独立项。
- `correct`：沿用既定 Reference only 决策。
- 其余 principles：按问题查 leaf，不整体安装。

### C. 明确不适合当前主流程

- `poteto-mode`、`poteto-help`、`figure-it-out`：形成第二 router/playbook system。pstack official README 明说 mode 会选 22 个 playbooks 并 route 其他 skills，与 Matt-first 单一主链冲突。[README lines 45–103](https://github.com/cursor/plugins/blob/41e400932eca14f289e7db717a70455256b6d388/pstack/README.md#L45-L103)
- `setup-pstack`：写 `~/.cursor/rules/pstack-models.mdc` 并配置 model roles；当前 runtime 已有自己的 model/delegation policy。[source lines 6–76](https://github.com/cursor/plugins/blob/41e400932eca14f289e7db717a70455256b6d388/pstack/skills/setup-pstack/SKILL.md#L6-L76)
- 完整 `arena` / `swarm`：多模型、隔离 worktree/output、cross-judge 与 parent aggregation 是另一套 orchestration，不是缺失 stage。
- `statechart` compiler/scripts：toolchain、network install、model drift 与维护面不符合通用主链。
- pstack `tdd`：与 active Matt `tdd` 同名且范围更窄。
- 整体导入 24 principles 或 59 skills：inventory 本身不是可验证收益。

## 下一波为何只有两个 candidates

不建议凑第三项：

- Grilling/prototype trigger 已存在于 `ask-matt`，所以 `sharpen` 和 `principle-exhaust-the-design-space` 不能作为“缺口”进入同波。
- `reframe` 与 domain-modeling 重叠，且会引入 web vocabulary 与 8–12 terms 的 padding risk。
- `interrogate` 同时改变 reviewer count、model diversity、worktree isolation 与 finding gate，无法在一轮 eval 中归因。
- `create-verification-skill` 是 repo capability generation，不是每次 feature flow 的 step。
- `benchmark-checklist` 和 formal verification 都需要特定 workload/property；没有目标项目时，实验只会测 prompt compliance。
- `architect`、pstack `tdd`、`statechart` 分别被 active design/TDD/prototype 覆盖或 runtime 成本过高。

下一波顺序是：先修复或隔离验证 G1–G3，冻结 current `code-review` baseline，再分别测试 `blast-radius` 和 `principle-prove-it-works`。两项分开跑，避免把“发现 hidden coupling”和“实际 artifact 可运行”混成一个无法归因的综合分数。

## Primary sources

- Matt active ownership 与 pins：[`skills/matt/README.md`](../../skills/matt/README.md)、[`skills/matt/engineering/README.md`](../../skills/matt/engineering/README.md)。
- 当前主流程：[`ask-matt`](../../skills/matt/engineering/ask-matt/SKILL.md)、[`grill-with-docs`](../../skills/matt/engineering/grill-with-docs/SKILL.md)、[`to-spec`](../../skills/matt/engineering/to-spec/SKILL.md)、[`to-tickets`](../../skills/matt/engineering/to-tickets/SKILL.md)、[`implement`](../../skills/matt/engineering/implement/SKILL.md)、[`code-review`](../../skills/matt/engineering/code-review/SKILL.md)。
- Active adjacent skills：[`prototype`](../../skills/matt/engineering/prototype/SKILL.md)、[`tdd`](../../skills/matt/engineering/tdd/SKILL.md)、[`domain-modeling`](../../skills/matt/engineering/domain-modeling/SKILL.md)、[`codebase-design`](../../skills/matt/engineering/codebase-design/SKILL.md)、[`diagnosing-bugs`](../../skills/matt/engineering/diagnosing-bugs/SKILL.md)、[`retro`](../../skills/matt/engineering/retro/SKILL.md)。Browser verification 由 [OMP browser runtime](../omp/devtools-mcp-integration.md) 提供，不属于 active skill source。
- Cursor pstack pinned source：[`pstack/README.md`](https://github.com/cursor/plugins/blob/41e400932eca14f289e7db717a70455256b6d388/pstack/README.md)、[`pstack/skills/`](https://github.com/cursor/plugins/tree/41e400932eca14f289e7db717a70455256b6d388/pstack/skills)、[Claude Code adapter](https://github.com/cursor/plugins/blob/41e400932eca14f289e7db717a70455256b6d388/pstack/docs/harness/claude-code.md)。
