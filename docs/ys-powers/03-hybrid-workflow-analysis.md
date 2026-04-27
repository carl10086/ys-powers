# 混合工作流分析（Hybrid Workflow Analysis）

> **目标**：分析 `refer/superpowers/` 与 `refer/agent-skills/` 两个参考项目的**原本实现**，作为后续构建 ys-powers 自有工作流（融合双方优点）的事实基础。
>
> **节奏**：本文按 Define / Plan / Build / Verify / Review / Ship 六阶段拆分。当前**只产出 Define 章节**，后续阶段单独追加。
>
> **视角声明**：Define 阶段保持事实中立——不预设"以 superpowers 为基"或"以 agent-skills 为基"，只把两者各自的实现摊开看。"以谁为基 + 怎么调整"是 Plan 阶段才决策。

---

## Define：两者原本实现的 6 阶段对照

### 1. 6 阶段映射总表

下表把两个项目在每个阶段对应的 skill / command / agent 都列出来。空缺意味着该项目在该阶段没有显式机制（不等于功能空白，下文会展开）。

| 阶段 | superpowers 的实现 | agent-skills 的实现 |
|------|-------------------|---------------------|
| Define  | `brainstorming` skill + `/brainstorm` command | `/spec` command → `spec-driven-development` skill |
| Plan    | `writing-plans` skill + `/write-plan` command | `/plan` command → `planning-and-task-breakdown` skill |
| Build   | `executing-plans` skill + `/execute-plan` command + `subagent-driven-development` skill | `/build` command → `incremental-implementation` skill **+** `test-driven-development` skill |
| Verify  | `verification-before-completion` skill + `test-driven-development` skill + `systematic-debugging` skill | `/test` command → `test-driven-development` skill（+ 浏览器场景拉起 `browser-testing-with-devtools`）|
| Review  | `requesting-code-review` skill + `receiving-code-review` skill + `code-reviewer` agent | `/review` command → `code-review-and-quality` skill（嵌套 `security-and-hardening` / `performance-optimization` 子 skill）|
| Ship    | `finishing-a-development-branch` skill + `using-git-worktrees` skill | `/ship` command → `shipping-and-launch` skill **+ 3 persona subagent fan-out**（`code-reviewer` / `security-auditor` / `test-engineer`）|

**第一眼能看到的事实**：

- **两者在 6 个阶段都有覆盖**——superpowers 没有"空缺阶段"，只是没用 6 阶段命名而已。
- **agent-skills 的 slash command 入口更全**：7 个 command（多一个 `/code-simplify`），覆盖到 Verify / Review / Ship 三个阶段；superpowers 只有 3 个 command（`/brainstorm` `/write-plan` `/execute-plan`），后三阶段靠 skill 自动激活和文档显式 "REQUIRED SUB-SKILL" 串联。
- **agent-skills 在 Ship 阶段独有 fan-out 编排**：`/ship` 并发拉起 3 个 persona subagent，主 agent 在 Phase B 合并结果。superpowers 在 Review 阶段也用 subagent（`code-reviewer`），但只有 1 个 persona、不并发。

---

### 2. 每个阶段展开

每个小节按"superpowers 怎么做 / agent-skills 怎么做 / 两者关键差异"三段展开。

---

#### 2.1 Define 阶段

##### superpowers：`brainstorming` skill

- **入口**：`/brainstorm` command 或自动触发（"creating features, building components, adding functionality, or modifying behavior" 都必须先走）。
- **核心机制**：
  - **`<HARD-GATE>` 标记**：在用户批准设计前**禁止**调用任何实现 skill、写代码、scaffold 项目。这是在 SKILL.md 里硬编码的一行 XML 标签，不靠"建议"，靠"门禁"。
  - **Socratic 一次一个问题**：通过 `AskUserQuestion` 工具弹框，每条消息只问一个问题，优先选项式。
  - **2-3 approach 提案**：在动手前必须给出 2-3 个不同方案 + trade-off + 推荐。
  - **Visual Companion**（浏览器伴侣）：可选，用于在浏览器里展示 mockup / 架构图 / 视觉对比。
  - **产出物固定**：`docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`，必须 commit 到 git。
- **流程图**（SKILL.md 用 Graphviz dot 描述）：探索项目上下文 → 视觉伴侣询问 → Socratic 澄清 → 提议 2-3 方案 → 分节呈现 design → 用户批准 → 写 spec → spec self-review → 用户审 spec → **进入 `writing-plans` skill**。
- **终态**：调用 `writing-plans` skill。**不允许**进入 `frontend-design` / `mcp-builder` 等任何其他实现 skill。
- **SKILL.md 章节结构**：Anti-Pattern / Checklist / Process Flow / The Process / After the Design / Key Principles / Visual Companion。

##### agent-skills：`/spec` → `spec-driven-development` skill

- **入口**：`/spec` command（一行 `Invoke the agent-skills:spec-driven-development skill`），也可在合适场景由 SKILL 的 description 自动激活。
- **核心机制**：
  - **4-Phase Gated Workflow**：SPECIFY → PLAN → TASKS → IMPLEMENT，每阶段过完都要人工 review，不准跨阶段跳。
  - **6 个固定 spec 区域**：objective / commands / project structure / code style / testing strategy / boundaries（在 SKILL.md 的 spec 模板里硬编码）。
  - **Surface assumptions immediately**：要求在写 spec 内容前先列出所有隐含假设，给人审。
  - **Common Rationalizations / Red Flags / Verification**：SKILL.md 末尾三段固定模板字段，分别对应"LLM 偷懒时的常见借口"、"失控的危险信号"、"怎么验证 skill 真的执行了"。
- **产出物**：`SPEC.md` 放在项目根（不是按日期归档到 specs/）。
- **触发其他 skill**：`/spec` command 是单一触发，只调起 `spec-driven-development` 一个 skill；不像 `/build` 一次拉两个。
- **SKILL.md 章节结构**：Overview / When to Use / The Gated Workflow / [spec 模板] / Common Rationalizations / Red Flags / Verification。

##### 关键差异

| 维度 | superpowers | agent-skills |
|------|-------------|--------------|
| 强制力机制 | `<HARD-GATE>` XML 标签 | 4-phase gated workflow（流程门禁） |
| 提问形式 | Socratic 一次一问 + AskUserQuestion 弹框 | "Surface assumptions immediately" 列表式 |
| 产出物归档 | `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` | 项目根的 `SPEC.md` |
| 视觉辅助 | Visual Companion 浏览器伴侣 | 无 |
| LLM 防御段 | 无 | Common Rationalizations + Red Flags + Verification |
| 中文化 | brainstorming 已在 ys-powers 本地版加 `<IMPORTANT>` 强制中文 | 无中文支持（英文 spec） |

---

#### 2.2 Plan 阶段

##### superpowers：`writing-plans` skill

- **入口**：`/write-plan` command 或由 brainstorming 终态自动调用。
- **核心机制**：
  - **bite-sized task granularity**：每步 2-5 分钟（如 "Write the failing test" / "Run it to make sure it fails" / "Implement the minimal code" / "Run the tests" / "Commit" 都是独立 step）。
  - **DRY / YAGNI / TDD**：作为基础原则写在 Overview 里。
  - **File Structure 决策提前**：动手前先 map 要新建/修改哪些文件、每个文件的责任，"decomposition decisions get locked in"。
  - **plan 头部强制模板**：每份 plan 必须以 `# [Feature Name] Implementation Plan` 开头，含 `> For agentic workers: REQUIRED SUB-SKILL: ...` 一行，明确指引执行者用 `subagent-driven-development` 或 `executing-plans`。
- **产出物**：`docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`。
- **scope check**：如果 spec 跨多个独立子系统，要拆成多份 plan（每份独立可交付）。

##### agent-skills：`/plan` → `planning-and-task-breakdown` skill

- **入口**：`/plan` command。
- **核心机制**：
  - **Plan Mode（read-only）**：写代码前进入只读模式——读 spec、读相关代码、识别已有模式、map 依赖、记风险/未知。"Do NOT write code during planning."
  - **Dependency Graph 显式化**：要求把任务依赖画成树状图（schema → API → endpoint → frontend → UI components）。
  - **小且可验证**：每个任务"small enough to implement, test, and verify in a single focused session"。
  - **NOT use 场景**：单文件 + 范围明确时不用调用此 skill（明确边界自己的不适用范围）。
- **SKILL.md 章节结构**：Overview / When to Use / The Planning Process / [...] / Common Rationalizations / Red Flags / Verification。

##### 关键差异

| 维度 | superpowers | agent-skills |
|------|-------------|--------------|
| 任务粒度规范 | "2-5 分钟一步"，明确具体 | "small enough to implement+test+verify in one session"，定性 |
| 依赖管理 | File Structure 决策（隐式表达依赖）| Dependency Graph 显式画图 |
| plan 头部模板 | 强制头部含 SUB-SKILL 指引 | 无强制头部 |
| 产出物归档 | `docs/superpowers/plans/YYYY-MM-DD-...md` | 在 SKILL.md 里没强制路径 |
| 与下一阶段衔接 | 头部直接点名 `executing-plans` 或 `subagent-driven-development` | 靠 `/build` command 自动衔接 |

---

#### 2.3 Build 阶段

##### superpowers：`executing-plans` skill（+ 可选的 `subagent-driven-development`）

- **入口**：`/execute-plan` command。
- **核心机制**：
  - **三步走**：Step 1 Load and Review Plan（先批判性读，有疑问就停下来问人）→ Step 2 Execute Tasks（每个 task：mark in_progress → 严格按 step 走 → 跑 verification → mark completed）→ Step 3 完成后调用 `finishing-a-development-branch`。
  - **明确 stop 信号**：阻塞、计划有 critical gap、不理解指令、verification 反复失败 → 立即停下来问人，不要猜。
  - **subagent 优先**：SKILL.md 明确推荐"在支持 subagent 的平台（Claude Code / Codex），改用 `subagent-driven-development`"——把每个 task 派给独立 subagent 执行，主 session 只做编排和验证。
- **产出物**：每个 task 一个 commit；最终交给 `finishing-a-development-branch`。

##### agent-skills：`/build` → `incremental-implementation` + `test-driven-development`（双 skill 并挂）

- **入口**：`/build` command 一次拉起两个 skill（增量交付 × TDD），让方法论互补。失败分支挂 `debugging-and-error-recovery`（条件触发）。
- **核心机制**：
  - **Increment Cycle**：Implement → Test → Verify → Commit → Next slice，每 slice 都要让系统处于 "working, testable state"。
  - **Vertical Slices preferred**：优先做穿透整个 stack 的薄垂直切片，而不是横切（先全部 schema 再全部 API 再全部 UI）。
  - **100 行触发线**：超过 100 行不测试就警告。
  - **TDD 内嵌**：测试先行不是可选，是 `/build` 默认拉起的第二个 skill。

##### 关键差异

| 维度 | superpowers | agent-skills |
|------|-------------|--------------|
| 触发模式 | 单 skill 触发（`executing-plans`）| 多 skill 并挂（`incremental-implementation` + `test-driven-development`）+ 条件触发（失败 → `debugging-and-error-recovery`）|
| 增量节奏定义 | task-by-task（按 plan 任务粒度）| slice-by-slice（按"垂直切片"概念）+ 100 行警戒线 |
| TDD 强制度 | 在 plan 头部建议 TDD，但不强制 | `/build` 默认并挂 TDD skill |
| Subagent 用法 | 主推 `subagent-driven-development`：每个 task 派独立 subagent | `/build` 阶段不用 subagent；subagent 集中在 `/ship` |
| 失败处理 | "STOP and ask"——人工介入 | 条件触发 `debugging-and-error-recovery` skill |

---

#### 2.4 Verify 阶段

##### superpowers：`verification-before-completion` + `test-driven-development` + `systematic-debugging`

- **入口**：没有显式 `/verify` command，靠 SKILL 触发条件自动激活，或在 `executing-plans` 流程中自然进入。
- **核心机制（`verification-before-completion`，最硬核的一个）**：
  - **The Iron Law**：`NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE`。
  - **The Gate Function 5 步**：IDENTIFY 哪个命令能证明 → RUN 完整跑一遍 → READ 完整 output / exit code / failure 数 → VERIFY 是否真的支持 claim → ONLY THEN 才能下结论。跳任何一步 = "lying, not verifying"。
  - **Common Failures 表**：列出"测试通过 / linter 干净 / build 成功 / bug 已修 / regression test 工作 / agent 完成 / requirement 达标"7 类 claim 的"什么算证据 vs 什么不算"。
- **`systematic-debugging`**：调试方法论，避免靠猜。
- **`test-driven-development`**：与 agent-skills 同名（red-green-refactor）。

##### agent-skills：`/test` → `test-driven-development` skill

- **入口**：`/test` command。浏览器场景下可选辅助 `browser-testing-with-devtools`（通过 Chrome DevTools MCP）。
- **核心机制**：
  - red-green-refactor 标准 TDD 循环。
  - SKILL.md 含 Common Rationalizations（"测试只是辅助" / "等代码稳定再写测试" 等借口的拆解）+ Red Flags + Verification。
- **特点**：agent-skills 没有跟 `verification-before-completion` 等价的"不准白嫖"硬约束 skill；它的"verification" 主要在每个 SKILL.md 的尾部 `Verification` 段（"怎么证明本 skill 被正确执行"）。

##### 关键差异

| 维度 | superpowers | agent-skills |
|------|-------------|--------------|
| "不准白嫖完成"约束 | `verification-before-completion`（独立 skill，硬规则）| 散布在每个 SKILL 的 Verification 段 |
| 调试方法论 | `systematic-debugging`（独立 skill）| `debugging-and-error-recovery`（独立 skill）|
| 浏览器测试 | 无（不绑定具体浏览器工具）| `browser-testing-with-devtools` 通过 Chrome DevTools MCP |
| 触发模式 | 自动激活（无 command）| `/test` command 显式入口 |

---

#### 2.5 Review 阶段

##### superpowers：`requesting-code-review` + `receiving-code-review` + `code-reviewer` agent

- **入口**：在 `subagent-driven-development` 中，每个 task 完成后**强制**调用；major feature 完成后；merge 前。
- **核心机制（`requesting-code-review`）**：
  - 显式拿到 BASE_SHA / HEAD_SHA。
  - 用 Task tool 派 `superpowers:code-reviewer` subagent 类型，填模板（`{WHAT_WAS_IMPLEMENTED}` / `{PLAN_OR_REQUIREMENTS}` / `{BASE_SHA}` / `{HEAD_SHA}` / `{DESCRIPTION}`）。
  - **关键设计**：reviewer 不继承主 session 的对话历史——只看精心构造的上下文，专注 work product 而不是思考过程，同时保护主 session 的 context window。
  - 反馈处理：Critical 立即修；Important 进度前修；Minor 记录后修；reviewer 错了可以反驳（带理由）。
- **`receiving-code-review`**：被 review 一方的对应 skill。
- **`code-reviewer.md`**：persona agent 定义文件（在 `agents/` 目录）。

##### agent-skills：`/review` → `code-review-and-quality` skill

- **入口**：`/review` command。
- **核心机制**：
  - **The approval standard**：通过标准是"明确改善 overall code health"，不是 perfect。"Don't block a change because it isn't exactly how you would have written it."
  - **Five-Axis Review**：Correctness / Readability & Simplicity / Architecture / Security / Performance。每轴有具体 checklist。
  - **嵌套子 skill**：特定维度调用专门的子 skill——安全维度拉起 `security-and-hardening`，性能维度拉起 `performance-optimization`。
  - **Code Smells 章节**：内置 Bloaters / Dispensables / Couplers 三大类 smell 表（识别阈值 + 怎么避免）。
- **subagent**：`code-reviewer` agent 在 `/ship` 阶段被 fan-out 拉起；`/review` 本身不显式 fan-out，而是在主 session 内做 5 轴审查。

##### 关键差异

| 维度 | superpowers | agent-skills |
|------|-------------|--------------|
| 触发频率 | 每个 task 后强制（subagent-driven 模式下）| 主要是 PR / merge 前 |
| 执行模式 | 派 subagent（context 隔离）| 主 session 内做 5 轴审查；subagent fan-out 在 `/ship` |
| 审查维度 | 通用（reviewer agent 的 prompt 决定）| 显式 5 轴 + 5 轴各有 checklist |
| 子 skill 嵌套 | 无 | 安全/性能维度调用专门子 skill |
| Code Smell 表 | 无（在外部规则文件里）| 在 SKILL 内置 3 类 smell 表 |
| 反馈处理协议 | Critical/Important/Minor 三级 + 可反驳 | approval standard "improvement, not perfection" |

---

#### 2.6 Ship 阶段

##### superpowers：`finishing-a-development-branch` + `using-git-worktrees`

- **入口**：`executing-plans` 完成后**强制**调用 `finishing-a-development-branch`（SKILL.md 标 REQUIRED SUB-SKILL）。
- **核心机制（`finishing-a-development-branch`）**：
  - **Step 1 Verify Tests**：先跑项目测试套件，**failures > 0 直接停**，不准进 Step 2。
  - **Step 2 Determine Base Branch**：识别从哪个分支分出来的（main/master），不确定就问。
  - **Step 3 Present Options**：把可选项（merge / 开 PR / 清理）摆给用户，让用户挑。
  - **Step 4 Execute Choice**：执行用户选的路径。
- **`using-git-worktrees`**：处理多分支并行（与 brainstorming 的 "dedicated worktree" 配合）。
- **特点**：superpowers 的 Ship 阶段是**用户决策驱动**——把选项摆出来让用户挑，不主动 fan-out 验证。

##### agent-skills：`/ship` → `shipping-and-launch` + 3 persona subagent fan-out

- **入口**：`/ship` command。
- **核心机制（最复杂、agent-skills 最独特的一个 command）**：
  - **Phase A 并行 fan-out**：单条 assistant turn 内同时发 3 个 Agent tool 调用——`code-reviewer` / `security-auditor` / `test-engineer`。"Issue all three Agent tool calls in a single assistant turn so they execute in parallel — sequential calls defeat the purpose."
  - **Persona 隔离**：每个 subagent 独立 context window，不共享状态、不互相调用、不跟 main agent 之外的对象通信。
  - **Phase B 主 agent merge**：6 个维度合并——Code Quality / Security / Performance / Accessibility / Infrastructure / Documentation。前三个从 persona 报告聚合，后三个主 agent 直接核查。
  - **Phase C Decision**：固定输出格式——GO / NO-GO + Blockers + Recommended fixes + Acknowledged risks + **Rollback plan**（mandatory）+ Specialist reports 全文。
  - **Skip 条件极严**：只有当 ≤2 文件 / <50 行 / 不涉及 auth/payments/data/config 时才可以跳过 fan-out。否则即便 diff 看起来小也默认 fan-out。
  - **Persona resolution**：用户在 `.claude/agents/` 自定义的同名 persona 优先于 plugin 自带的——这是 Claude Code subagent 优先级机制的"故意行为"。

##### 关键差异

| 维度 | superpowers | agent-skills |
|------|-------------|--------------|
| 决策驱动 | 用户决策（present options 让人挑）| 自动化决策（GO / NO-GO + Blocker 列表）|
| 并行 fan-out | 无（Review 阶段也只 1 个 reviewer subagent）| Phase A 三 persona 并行（核心特色）|
| 验证维度 | 跑测试 + 让用户挑路径 | 6 维度（含 a11y / infra / docs）+ rollback plan |
| Rollback plan | 不强制 | mandatory，是 GO 决策的前置 |
| 跳过条件 | 无（流程必走）| 有但极严（≤2 文件 / <50 行 / 不碰敏感面）|
| Subagent 优先级 | superpowers 自带的 reviewer | 用户 `.claude/agents/` 自定义优先于 plugin |

---

### 3. 事实层结论

Define 阶段不做决策，只把"事实清单"钉死给 Plan 阶段用。

#### 3.1 两者各自的"完整覆盖区"

- **superpowers**：14 个 skill，覆盖 6 阶段全程，但**只有 3 个 slash command**（`/brainstorm` `/write-plan` `/execute-plan`），后三阶段靠 SKILL 自动激活 + 文档显式 `REQUIRED SUB-SKILL` 串联。
- **agent-skills**：21 个 skill，覆盖 6 阶段 + Meta，**7 个 slash command**（多一个 `/code-simplify`），有 11 个 skill 由 command 显式触发，剩下约一半靠 SKILL description 的 "Use when..." 自动激活——这正是元 skill `using-agent-skills` 规定的发现机制。

#### 3.2 实现差异的 4 个分类

**(A) SKILL.md 模板差异**（最重要的结构差异）

| 字段 | superpowers brainstorming | agent-skills spec-driven-development |
|------|---------------------------|--------------------------------------|
| Overview | 有（开头） | 有 |
| When to Use | 隐含在 description | 独立章节 |
| Process / Process Flow | 有（含 dot 流程图）| 有（叫 The Gated Workflow） |
| Checklist | 有 | 无 |
| Anti-Pattern | 有 | 无（散在 Common Rationalizations）|
| Common Rationalizations | **无** | **有**（防 LLM 偷懒）|
| Red Flags | **无** | **有**（失控信号）|
| Verification | **无** | **有**（怎么证明 skill 真被执行）|
| HARD-GATE | **有**（XML 标签）| **无** |
| Visual Companion | **有**（独立子文件）| **无** |

**结论**：两套 SKILL 模板的设计取向不同——superpowers 偏"正向流程 + 强门禁"，agent-skills 偏"反向防御 + 自我验证"。**两套字段几乎不重叠**，融合时不是"二选一"而是"两边都加"。

**(B) 触发机制差异**

- superpowers：command 数量少（3 个），主链是 brainstorming → writing-plans → executing-plans，靠"REQUIRED SUB-SKILL" 文档约定串联；其他 skill 靠自动激活。
- agent-skills：command 数量多（7 个），覆盖 6 阶段，命名空间 `agent-skills:<skill-name>` 显式调用；剩余 skill 也靠自动激活。

**(C) 编排范式差异**

- superpowers：subagent 用在 Review（每 task 一次）+ subagent-driven-development（每 task 派独立 subagent 执行整段实现）。**单 persona、串行**。
- agent-skills：subagent 集中在 `/ship`，**3 persona、并行 fan-out**，主 agent 在 Phase B 同步合并。

**(D) "硬约束"分布差异**

| 硬约束 | superpowers 所在位置 | agent-skills 所在位置 |
|--------|---------------------|----------------------|
| 设计未批准不写代码 | brainstorming `<HARD-GATE>` | spec-driven-development 4-phase gated workflow |
| 测试不通过不能合并 | finishing-a-development-branch Step 1 | shipping-and-launch Phase A 的 test-engineer + Phase C blocker |
| 不准声称"完成"无证据 | verification-before-completion The Iron Law | 散布在每 SKILL 的 Verification 段 |
| 关键 review 必须独立 context | requesting-code-review 派 subagent | /ship Phase A 三 persona 隔离 |
| Rollback plan 必备 | 无 | shipping-and-launch Phase C mandatory |

#### 3.3 一方独有 / 另一方没有的特性清单

**只在 superpowers 有**：
- `<HARD-GATE>` XML 硬门禁标签
- Visual Companion（浏览器视觉伴侣）
- `verification-before-completion` 独立硬约束 skill
- `subagent-driven-development`（每 task 独立 subagent 执行）
- 显式的 plan 头部模板（强制 `REQUIRED SUB-SKILL` 行）
- Socratic 一次一问 + AskUserQuestion 弹框形式

**只在 agent-skills 有**：
- Common Rationalizations 段（针对 LLM 自我借口的反向防御）
- Red Flags 段（失控信号清单）
- Verification 段（怎么证明 skill 真被执行）
- 6 阶段显式命名（Define/Plan/Build/Verify/Review/Ship）
- 7 个 slash command 入口
- `/ship` 三 persona fan-out 编排
- Five-Axis Review 显式审查框架（5 轴 + 各轴 checklist）
- 内置 Code Smell 表（Bloaters/Dispensables/Couplers）
- 嵌套子 skill 触发（review → security/performance）
- Rollback plan mandatory
- 用户级 persona 优先于 plugin persona 的解析机制

#### 3.4 待 Plan 阶段决策的几个关键问题

**这些问题 Define 阶段不回答，只列出供 Plan 阶段处理**：

1. **SKILL 模板取舍**：是融合两套字段（既要 HARD-GATE 又要 Common Rationalizations），还是分两类 skill（流程类用 superpowers 模板、防御类用 agent-skills 模板）？
2. **slash command 数量**：要不要把 superpowers 的 3 个扩展到 7 个？还是保留 3 个主链 command + 用户能自己加？
3. **subagent 编排**：fan-out 默认开还是默认关？哪些场景强制开？
4. **6 阶段命名**：在 ys-powers 里是用英文（Define/Plan/Build/...）还是中文（设计/规划/构建/...）？
5. **HARD-GATE 怎么扩散**：只在 brainstorming 有，要不要扩到 plan / ship？
6. **verification-before-completion 的硬约束**怎么和 agent-skills 的"散布在 Verification 段"模式合并？

#### 3.5 Define 章节自检（Spec Self-Review）

- **Placeholder 扫描**：无 TBD / TODO（已检查）
- **内部一致性**：6 阶段表格与每节展开内容一致；3.3 独有特性清单与 2.x 各节叙述一致
- **范围检查**：Define 章节集中于"原本实现"事实陈述，未越界进入 Plan/Build 决策（3.4 列出的问题明确标注"留给 Plan 阶段"）
- **歧义检查**：所有 skill 名 / command 名都用 backtick 加粗格式；阶段名首字母大写统一
- **未尽事项**：Plan / Build / Verify / Review / Ship 五章后续追加；本文只交付 Define
