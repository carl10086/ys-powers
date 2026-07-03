# refer/agent-skills 同步工作日志

记录 refer/agent-skills 子项目的版本演进，及每次更新对 ys-powers 的同步决策。

> **工作约定**：ys-powers 只关注 **Claude Code** 生态（`.claude/commands/`、`SKILL.md`、hooks）。`.gemini/`（Gemini CLI）相关变更仅做简要提及，不作为同步决策依据。

## 当前快照

- Remote:      https://github.com/addyosmani/agent-skills.git
- Branch:      main
- Commit:      aba7c4e9695c363e65cb59effe926c7f1d1abe3d
- Short:       aba7c4e
- Author Date: 2026-06-28 11:11:20 -0700
- Subject:     Merge pull request #323 from An-idd/feat/validate-naming-and-trigger
- Worktree:    clean
- 快照时间:    2026-07-03
- ys-powers 同期 commit: 533b0fd96b8a7d3fa3cc3ad95f197562aa6b9dc2
- 新增 tag:    0.6.2

## 当前 skills 清单（24 个）

- api-and-interface-design
- browser-testing-with-devtools
- ci-cd-and-automation
- code-review-and-quality
- code-simplification
- context-engineering
- debugging-and-error-recovery
- deprecation-and-migration
- documentation-and-adrs
- frontend-ui-engineering
- git-workflow-and-versioning
- idea-refine
- incremental-implementation
- observability-and-instrumentation
- performance-optimization
- planning-and-task-breakdown
- security-and-hardening
- shipping-and-launch
- source-driven-development
- spec-driven-development
- test-driven-development
- using-agent-skills

## 已吸收度索引

| refer skill | docs analysis | ys-powers/skills | 备注 |
|---|---|---|---|
| spec-driven-development | 01 | 同名 | |
| planning-and-task-breakdown | 02 | 同名 | |
| incremental-implementation | 03 | 同名 | |
| test-driven-development | 04 | 同名 | |
| context-engineering | 05 | 同名 | |
| idea-refine | 06 | 同名 | |
| debugging-and-error-recovery | 07 | 同名 | |
| api-and-interface-design | — | 同名 | 缺 analysis |
| browser-testing-with-devtools | — | 同名 | 缺 analysis |
| ci-cd-and-automation | — | 同名 | 缺 analysis |
| code-review-and-quality | — | 同名 | 缺 analysis |
| code-simplification | — | 同名 | 缺 analysis |
| deprecation-and-migration | — | 同名 | 缺 analysis |
| documentation-and-adrs | — | 同名 | 缺 analysis |
| frontend-ui-engineering | — | 同名 | 缺 analysis |
| git-workflow-and-versioning | — | 同名 | 缺 analysis |
| performance-optimization | — | 同名 | 缺 analysis |
| security-and-hardening | — | 同名 | 缺 analysis |
| shipping-and-launch | — | 同名 | 缺 analysis |
| source-driven-development | — | 同名 | 缺 analysis |
| using-agent-skills | — | 同名 | 缺 analysis |
| interview-me | 08 | 同名 | refer 新增 skill |
| doubt-driven-development | 09 | 同名 | refer 新增 skill |
| observability-and-instrumentation | — | 缺 | 新增 skill，ys-powers 未引入 |

---

## 更新历史

### 2026-07-03: 2e0dfbf..aba7c4e

**摘要**：本次为能力大幅扩展+编排重构。新增 `observability-and-instrumentation`（贯穿 Build/Review/Ship 阶段的可观测方法论）+ `web-performance-auditor` agent 与 `/webperf` command（Deep/Quick 双模式审计）；`security-and-hardening` 引入 STRIDE 威胁建模 + SSRF + supply-chain + OWASP LLM Top 10；`using-agent-skills` 决策树新增 observability 入口，生命周期从 15 步扩到 16 步；新增 `definition-of-done.md` 项目级交付清单。编排层：`.claude-plugin/plugin.json` 简化为 `plugin.json`，agents 注册机制稳定。

**上下游**：
- 起点: 2e0dfbf (Merge pull request #215 from addyosmani/addyosmani/fix-marketplace-schema)
- 终点: aba7c4e (Merge pull request #323 from An-idd/feat/validate-naming-and-trigger)
- 期间提交数: 60+
- 新增 tag: 0.6.2
- ys-powers 同期 commit: 533b0fd

#### 4 维度变更

**1. 方法论修订**（既有 SKILL.md 内容变化）
- `security-and-hardening/SKILL.md`（+126 行）：新增"Threat Model First"前置流程（信任边界 → 资产 → STRIDE → 滥用用例）；新增 SSRF 章节（含 TOCTOU 警告）；新增 supply-chain hygiene 章节（`npm ci`、postinstall、typosquat）；OWASP LLM Top 10 映射（LLM03 Supply Chain）
- `code-review-and-quality/SKILL.md`（+38 行）：新增 structural-depth lenses（结构性深度视角），统一"presumptive blockers"立场，与五维评审互补
- `using-agent-skills/SKILL.md`（+21 行）：决策树新增 `observability-and-instrumentation` 入口；生命周期从 15 步扩到 16 步（observability 与 7-9 并行）；新增 DoD（Definition of Done）项目级交付清单交叉引用
- `browser-testing-with-devtools/SKILL.md`（+23 行）：默认 isolated profile 配置，demote autoConnect（避免隐式行为）
- `incremental-implementation/SKILL.md`（+4 行）：小修订
- `planning-and-task-breakdown/SKILL.md`（+4 行）：spec 阶段显式指明该 skill 的优先级
- `spec-driven-development/SKILL.md`（+4 行）：Plan/Tasks 阶段指向 `planning-and-task-breakdown`
- `debugging-and-error-recovery/SKILL.md`：step range 修正（4-10 → 4-6）
- `idea-refine/SKILL.md`（+2 行）：脚本可执行位修复
- `shipping-and-launch/SKILL.md`（+1 行）：小修订

**2. 新增**（skills / commands / agents / hooks / references 出现新文件）
- `skills/observability-and-instrumentation/SKILL.md`：全新 skill。覆盖结构化日志、RED/USE 指标、分布式追踪、症状驱动告警；强调"先写 on-call 问题再写 instrumentation"
- `agents/web-performance-auditor.md`：全新 agent（184 行），提供 Lighthouse / CrUX / DevTools trace 三类深度审计能力
- `.claude/commands/webperf.md`：新增 Claude command（32 行），Deep/Quick 双模式路由
- `references/definition-of-done.md`：新增 DoD 清单（67 行），区分"acceptance criteria"vs"DoD"，5 大类（Correctness / Quality / Integration / Documentation / Ship-readiness）checklist
- `references/observability-checklist.md`：新增配套 checklist（91 行）
- `references/security-checklist.md`：新增配套 checklist（45 行）
- `.claude/rules/skills-contributing.md`：新增贡献规则（15 行）
- `docs/comparison.md`：新增与同类工具对比文档（82 行），警告"避免堆叠多个 router"
- `docs/antigravity-setup.md`：新增 Antigravity CLI 配置指南（123 行）
- `commands/*.toml`（8 个）+ `.gemini/commands/build.toml` 等：新增 Antigravity CLI 与 Gemini CLI 的命令适配文件
- `scripts/validate-commands.js`：新增 commands 描述跨 CLI 同步校验器（172 行）

**3. 删除/合并**
- `agents/README.md` → 重命名为 `docs/agents.md`（消除 harness 警告）
- `.claude-plugin/plugin.json` → 简化为 `plugin.json`（移到根目录）

**4. 编排层变化**（commands ⇄ agents ⇄ hooks 组合关系）
- `plugin.json`：新增 `web-performance-auditor` agent 注册
- `hooks/hooks.json`：增加手动安装场景的 path fallback
- `/build auto`：新增"单次 plan + implement"快捷模式（`feat(build): add /build auto for one-pass plan + implement`）
- `using-agent-skills` → `web-performance-auditor` 路由：原决策树末尾新增分支
- `AGENTS.md` 大幅精简（-107 行），skill 创作规范迁移到 `docs/skill-anatomy.md`

#### 同步决策

- **要同步**：
  - `security-and-hardening` 的 STRIDE 威胁建模 + SSRF + supply-chain + OWASP LLM Top 10 → `ys-powers/skills/security-and-hardening/SKILL.md`（349 行）目前只有 OWASP Top 10 与 boundary 系统，缺这些高价值章节，应在 `writing-skills` 重写流程下扩充
  - `using-agent-skills` 的 16 步生命周期 + observability 入口 + DoD 交叉引用 → `ys-powers/skills/using-agent-skills/SKILL.md`（186 行）需对齐
  - `observability-and-instrumentation` 新 skill → 评估是否纳入 `ys-powers/skills/`（ys-powers 的 `references/` 已有 `testing-patterns.md` / `performance-checklist.md` 风格，可类比新增 `observability-checklist.md`）
  - `definition-of-done.md` → 评估是否纳入 `ys-powers/references/`（与现有 `orchestration-patterns.md` 同性质）
  - `webperf` command + `web-performance-auditor` agent → 评估是否纳入 `ys-powers/commands/` 与 `ys-powers/skills/`（ys-powers 无 `agents/` 子目录惯例，需评估是否新增）

- **暂不同步**：
  - `commands/*.toml` Antigravity CLI 命令 + `.gemini/commands/*.toml` → 第三/多方 CLI 适配，ys-powers 仅聚焦 Claude Code
  - `docs/antigravity-setup.md` → Antigravity 平台特定，ys-powers 不支持
  - `plugin.json` 重命名（`.claude-plugin/` → 根目录）→ 仅与 agent-skills 自身 marketplace 分发相关
  - `scripts/validate-commands.js` → CI 工具，ys-powers 无 multi-CLI 适配场景
  - `references/security-checklist.md` → 与 ys-powers 现有 `references/security-checklist.md` 已存在同名重复，ys-powers 优先自维护
  - `AGENTS.md` 精简 → 与 ys-powers 无关

- **已确认同步**：
  - `incremental-implementation` / `test-driven-development` 的"避免重复验证"反模式 → 上次（2026-06-07）entry 已确认同步并勾选完成
  - `idea-refine.sh` 可执行位 → 已在 refer commit `079913a` 中修复，ys-powers 同步对应文件即可（一次性 chmod）

- **待定**：
  - `observability-and-instrumentation` skill 是否引入 ys-powers → 需用户决策。引入会扩 ys-powers skill 数至 30+；不引入则依赖 `using-agent-skills` 决策树指向 refer 即可（与 `brainstorming` / `sop-search` / `writing-skills` 现状一致）
  - `webperf` command + `web-performance-auditor` agent 是否引入 → 需用户决策。ys-powers 当前没有 agent 子目录惯例，需先决定是否建立 `agents/` 模式
  - `definition-of-done.md` 引入位置 → `references/` 还是 `skills/`？前者更轻量、后者更易被 skill 触发发现

#### TODO

- [ ] 决策：是否在 `ys-powers/skills/` 下新建 `observability-and-instrumentation/` （参照 refer 结构，约 200 行 + 配套 checklist）
- [ ] 决策：是否在 `ys-powers/commands/` 下新建 `webperf.md` + 在 `ys-powers/skills/` 或新建 `ys-powers/agents/web-performance-auditor.md`
- [ ] 决策：是否在 `ys-powers/references/` 下新建 `definition-of-done.md`（中文版）
- [ ] 同步 `security-and-hardening` 的 STRIDE / SSRF / supply-chain / OWASP LLM Top 10 章节（重写风格按 `writing-skills` 流程）
- [ ] 同步 `using-agent-skills` 的 16 步生命周期 + observability 入口 + DoD 引用
- [ ] `idea-refine.sh` 可执行位核对与 chmod（如 ys-powers 有对应文件）

### 2026-06-07: f504276..2e0dfbf

**摘要**：本次为大规模方法论扩展。新增 `interview-me`（Define 阶段前置）和 `doubt-driven-development`（Build 阶段对抗性审查）两个核心 skill；`using-agent-skills` 决策树从 11 步扩展为 15 步生命周期；多个既有 skill 新增"避免无意义重复验证"反模式；编排层 `plugin.json` 引入 skills/agents 数组声明。

**上下游**：
- 起点: f504276 (Merge pull request #108 from devmarkpro/main)
- 终点: 2e0dfbf (Merge pull request #215 from addyosmani/addyosmani/fix-marketplace-schema)
- 期间提交数: 41
- ys-powers 同期 commit: d71481c

#### 4 维度变更

**1. 方法论修订**（既有 SKILL.md 内容变化）
- `using-agent-skills/SKILL.md`：重大更新——决策树新增 `interview-me`（Define 阶段入口）、`doubt-driven-development`（Build 阶段审查）、`code-simplification`（Review 阶段）、`deprecation-and-migration`（Ship 阶段）；生命周期序列从 11 步扩展为 15 步；Quick Reference 表格同步扩展
- `incremental-implementation/SKILL.md`：新增"避免无意义重复验证"条款——成功运行后不要在未改代码的情况下重复执行 build/test 命令
- `test-driven-development/SKILL.md`：同上，新增"避免重复运行测试"的反模式说明与 verification note
- `browser-testing-with-devtools/SKILL.md`：frontmatter 微调——description 增加 "Requires the chrome-devtools MCP server"
- `idea-refine/SKILL.md`：frontmatter 微调——description 更具体化触发词（"ideate", "refine this idea", "stress-test my plan"）
- `spec-driven-development/SKILL.md`：内联引用路径从裸 skill 名改为 `skills/<name>/SKILL.md` 格式

**2. 新增**（skills / commands / agents / hooks / references 出现新文件）
- `skills/doubt-driven-development/SKILL.md`：全新 skill，用于"在飞行中"对非平凡决策进行对抗性审查（区别于 `/review` 的事后 verdict）。使用场景：分支逻辑、跨模块边界、类型系统无法验证的断言（线程安全、幂等性）、不可逆操作前。
- `skills/interview-me/SKILL.md`：全新 skill，Define 阶段前置步骤。通过逐题提问（附最佳猜测）挖掘用户真实意图，直到 ~95% 置信度。用于请求欠指定时（"build me X" 但没有 who/why/success/constraint）。
- `scripts/validate-skills.js`：CI 验证器，检查 SKILL.md frontmatter 合规性（长度、必填字段、YAML 语法）。
- `hooks/session-start-test.sh`：session-start hook 的回归测试脚本，覆盖 JSON 转义场景。

**3. 删除/合并**
- 无。

**4. 编排层变化**（commands ⇄ agents ⇄ hooks 组合关系）
- `.claude-plugin/plugin.json`：移除 `version` 字段；新增 `skills`（目录形式，支持 auto-discover）和 `agents`（文件数组）声明。format 从对象改为数组再改为目录形式，最终稳定为 `"skills": "./skills"`。
- `.claude-plugin/marketplace.json`：适配显式 GitHub source 格式、relative path source，修复 install bug。
- `README.md`：skill 数量从 21 更新为 23+；新增 `interview-me` 和 `doubt-driven-development` 的引用；`using-agent-skills` 作为元 skill 被显式列出。
- `AGENTS.md`：agents 文件命名规范改为 `*.agent.md` 扩展名。
- `docs/skill-anatomy.md`：新增 frontmatter 规范条款（description 长度限制、触发词写法）。
- `docs/cursor-setup.md`：移除已废弃的 Option 3 (Notepads)。
- `.github/workflows/test-plugin-install.yml`：新增 marketplace install 测试。

#### 同步决策

- **要同步**：
  - `using-agent-skills` 决策树和生命周期序列的扩展 → `ys-powers/skills/using-agent-skills/SKILL.md` 需要更新以反映 15 步生命周期和 4 个新增 skill 入口
  - `incremental-implementation` 和 `test-driven-development` 的"避免重复验证"反模式 → 对应 skill 文件可能需要补充
  - `interview-me` 和 `doubt-driven-development` → 评估是否需要在 `ys-powers/skills/` 下新建同名 skill

- **暂不同步**：
  - `.claude-plugin/marketplace.json` / `plugin.json` —— 仅与 agent-skills 的 marketplace 插件分发相关，ys-powers 不走此分发渠道
  - `scripts/validate-skills.js` —— CI 工具，ys-powers 的 skill 数量/结构不同，但可参考其 frontmatter 校验逻辑用于自身质量门
  - `docs/copilot-setup.md` / `docs/cursor-setup.md` —— 第三方 IDE 配置文档，不相关
  - `AGENTS.md` 的 `*.agent.md` 扩展名 —— ys-powers 没有 agents 目录
  - `.gemini/commands/*.toml` 变更 —— Gemini CLI 生态，不相关，不展开

- **已确认同步**：
  - `spec-driven-development` 的内联路径写法（`skills/<name>/SKILL.md`）—— ys-powers 的同名 skill 需核对是否已采用
  - `browser-testing-with-devtools` / `idea-refine` 的 frontmatter 收紧 —— 若 ys-powers 已同步同一条 description 调整，则无需再动
  - `hooks/session-start.sh` 的 jq-based JSON 转义模式 —— 已在 2026-05-03 update entry 中标记为"要同步"，如已处理则此处为已确认

- **待定**：
  - `interview-me` 和 `doubt-driven-development` 是否纳入 ys-powers skill 集——需用户决策。两者均为高质量方法论 skill，但需评估是否与当前 workflow 重叠。

#### TODO（已完成）

- [x] 更新 `ys-powers/skills/using-agent-skills/SKILL.md` 的决策树和生命周期序列（15 步）
- [x] 检查并同步 `incremental-implementation` 和 `test-driven-development` 的"避免重复验证"反模式
- [x] 将 `interview-me` 和 `doubt-driven-development` 纳入 `ys-powers/skills/`
- [x] 核对并同步 `spec-driven-development` / `browser-testing-with-devtools` / `idea-refine` 的 frontmatter 调整

---

### 2026-05-03: 44b9e37..f504276

**摘要**：本次为纯“多 CLI 适配”更新，未触及任何 SKILL.md 方法论本身。对 ys-powers 仅有 2 处相关：`hooks/session-start.sh` 的 JSON 转义修复（issue #89）、`README.md` 的 HTTPS 安装指引微调。其余为 `.gemini/` 新增（Gemini CLI），不相关。

**上下游**：
- 起点: 44b9e37 (Merge pull request #66 from datfinesoul/opencode-skills)
- 终点: f504276 (Merge pull request #108 from devmarkpro/main)
- 期间提交数: 11
- 新增 tag: 0.6.0
- ys-powers 同期 commit: 42eb12e

#### 4 维度变更

**1. 方法论修订**（既有 SKILL.md 内容变化）
- 无。本次更新未触及任何 `skills/<name>/SKILL.md`。

**2. 新增**（skills / commands / agents / hooks / references 出现新文件）
- `.gemini/commands/*.toml`（7 个）+ `docs/gemini-cli-setup.md` 新增 Slash Commands 章节：Gemini CLI 适配。**与 ys-powers 无关，不展开。**

**3. 删除/合并**
- 无。

**4. 编排层变化**（commands ⇄ agents ⇄ hooks 组合关系）
- `hooks/session-start.sh`：关键修复——将 JSON 构造从手写 heredoc 改为 `jq` 命令，修复 issue #89（JSON 转义问题）；新增 `jq` 缺失时的优雅回退（`exit 0` + INFO 提示）
- `README.md`：将 SSH 替代方案改为 HTTPS URL 推荐（`/plugin marketplace add https://github.com/addyosmani/agent-skills.git`）；目录树中标注 `.gemini/commands/` 为 Gemini CLI 专用

#### 同步决策

- **要同步**：
  - `hooks/session-start.sh` 的 jq-based JSON 转义模式 → 检查 ys-powers 自身的 hooks 是否有类似 issue #89 的风险。当前项目级 `.claude/hooks/` 下是否有 session-start 类钩子？如有，应同步此修复。

- **暂不同步**：
  - `.gemini/commands/*.toml` — Gemini CLI 特定格式，不相关。
  - README 的 HTTPS 安装指引 — 仅与 agent-skills 插件 marketplace 分发相关，ys-powers 不通过 marketplace 分发。

- **已确认同步**：
  - `shipping-and-launch` 的 fan-out 跳过条件（2 文件以下 / 50 行以下 / 不涉及 auth/payments/data）→ 已在 `ys-powers/commands/ship.md` 中存在，无需补充。

- **待定**：
  - 无。本次更新无待定项。

#### TODO

- [ ] 检查 `ys-powers/.claude/hooks/` 下是否有 session-start 类钩子，评估是否需同步 jq 转义修复

### 2026-05-03: 初始快照（baseline）

本文件首次创建。锚点 commit = 44b9e37。
本条目无变更分析；下一次 git pull 后将基于此 commit 生成首份“4 维度变更”。

## Update Entry 模板

每次 `git pull` 后，在「更新历史」顶部追加一条，按以下模板填写。

```markdown
### YYYY-MM-DD: <prev-short>..<new-short>

**摘要**：一行总结本次更新的性质。

**上下游**：
- 起点: <prev-short> (<prev-subject>)
- 终点: <new-short> (<new-subject>)
- 期间提交数: N
- ys-powers 同期 commit: <short>

#### 4 维度变更

**1. 方法论修订**（既有 SKILL.md 内容变化）
- `<skill-name>`: 一行说明改了什么

**2. 新增**（skills / commands / agents / hooks / references 出现新文件）
- `<path>`: 一行说明

**3. 删除/合并**
- `<path>`: 一行说明

**4. 编排层变化**（commands ⇄ agents ⇄ hooks 组合关系）
- 一行说明

#### 同步决策

- **要同步**:
  - <动作> → 影响 ys-powers 路径 `<path>`
- **暂不同步**:
  - <理由>
- **待定**:
  - <未决问题>

#### TODO

- [ ] <动作 1>
- [ ] <动作 2>
```
