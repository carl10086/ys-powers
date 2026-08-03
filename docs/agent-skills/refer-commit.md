# refer/agent-skills 同步工作日志

记录 refer/agent-skills 子项目的版本演进，及每次更新对 ys-powers 的同步决策。

> **工作约定**：ys-powers 只关注 **Claude Code** 生态（`.claude/commands/`、`SKILL.md`、hooks）。`.gemini/`（Gemini CLI）相关变更仅做简要提及，不作为同步决策依据。

## 当前快照

- Remote:      https://github.com/addyosmani/agent-skills.git
- Branch:      main
- Commit:      98967c45a42b88d6b8fb3a88b7ff6273920763d6
- Short:       98967c4
- Author Date: 2026-07-12 10:58:04 -0700
- Subject:     Merge pull request #396 from nucliweb/docs/adoption-guide
- Worktree:    clean
- 快照时间:    2026-07-16
- ys-powers 同期 commit: 076ebc127f585773c06e62bab6c1c3d81c2cc3fa
- 新增 tag:    无

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
| code-review-and-quality | — | 同名 | 缺 analysis；待同步：依赖升级纪律子节(+5 规则、+2 反模式、+2 红旗) |
| code-simplification | — | 同名 | 缺 analysis |
| deprecation-and-migration | — | 同名 | 缺 analysis；待同步：DB schema expand/contract 章节(+5 规则、+3 反模式、+3 红旗) |
| documentation-and-adrs | — | 同名 | 缺 analysis |
| frontend-ui-engineering | — | 同名 | 缺 analysis；待同步：frontmatter 加 "accessible, responsive" + WCAG 触发词 |
| git-workflow-and-versioning | — | 同名 | 缺 analysis；待同步：Release & Versioning 章节(SemVer / tag / changelog) |
| performance-optimization | — | 同名 | 缺 analysis；待同步：frontmatter 加 "frontend, backend, queries, databases" + N+1 触发词 |
| security-and-hardening | — | 同名 | 缺 analysis；待同步：install-script gate + manager 边界识别 + 三大表 |
| shipping-and-launch | — | 同名 | 缺 analysis |
| source-driven-development | — | 同名 | 缺 analysis |
| using-agent-skills | — | 同名 | 缺 analysis |
| interview-me | 08 | 同名 | refer 新增 skill |
| doubt-driven-development | 09 | 同名 | refer 新增 skill |
| observability-and-instrumentation | — | 缺 | 新增 skill，ys-powers 未引入 |

---

## 更新历史

### 2026-07-16: aba7c4e..98967c4

**摘要**：本次为「方法论纵深」+「跨 CLI 扩展」双轨更新。方法论侧：`security-and-hardening` 重写 supply-chain 章节(manager 边界识别 + install-script gate + provenance 验证)、新增 `deprecation-and-migration` 的 Expand/Contract 数据库迁移章节、`code-review-and-quality` 新增依赖升级纪律子节、`git-workflow-and-versioning` 新增 Release & Versioning 章节、`planning-and-task-breakdown` + `spec-driven-development` 引入 `tasks/plan.md` / `tasks/todo.md` 输出约定。跨 CLI 侧：新增 Codex 插件支持(`.codex-plugin/`) + HTTPS git-config workaround；新增三层级 skill eval 框架(`evals/` + `scripts/run-evals.js`)。`.gemini/` 本次无变更。

**上下游**：
- 起点: aba7c4e (Merge pull request #323 from An-idd/feat/validate-naming-and-trigger)
- 终点: 98967c4 (Merge pull request #396 from nucliweb/docs/adoption-guide)
- 期间提交数: 49
- ys-powers 同期 commit: 076ebc1

#### 4 维度变更

**1. 方法论修订**（既有 SKILL.md 内容变化）
- `security-and-hardening/SKILL.md`（+36 行，结构调整较大）：
  - "Triaging npm audit Results" → "Triaging Dependency Audit Results"，决策树从「dev-only 路径」扩展到「runtime/build/test/deploy 全路径」可达性判断
  - Supply-Chain Hygiene 章节重写：新增「Find the installation boundary and manager」流程（workspace root 识别 + packageManager/lockfile/CI 三方核对），新增「Block dependency scripts before first execution」4 步 gate（bootstrap 关闭 → 检视 source → 最小批准 → frozen 验证）
  - 引入「Never apply forced audit remediation automatically」原则（反对 `npm audit fix --force`），引入 `npm audit signatures` / `pnpm audit signatures` provenance 验证
  - Verification Supply Chain checklist 重写（单 lockfile、scripts 默认关闭、ownership/provenance/release age/transitive graph）
  - 新增 Rationalization："The audit passed, so the dependency is safe"
- `deprecation-and-migration/SKILL.md`（+41 行）：新增 **Database Schema Migrations (Expand/Contract)** 章节——EXPAND→MIGRATE→CONTRACT 三阶段 + rename column 案例 + 5 条规则（additive first、tested down path、批式 backfill、`CREATE INDEX CONCURRENTLY`、feature flag 切换）；新增 3 条 Rationalization + 3 条 Red Flag + 数据库迁移后 Verification
- `code-review-and-quality/SKILL.md`（+15 行）：新增 **Upgrading an existing dependency** 子节——5 条升级纪律（changelog 优先 / 单包升级 / 测试定夺 / 透传图审视 / lockfile 诚实）；新增 2 条 Rationalization + 2 条 Red Flag + Verification 增加 1 条
- `git-workflow-and-versioning/SKILL.md`（+57 行）：新增 **Release & Versioning** 章节——SemVer 阐释 + `git tag -a` 发布约定 + 给人类看的 changelog（区别于 `git log`）+ 与 `shipping-and-launch` 链接；frontmatter description 增加「cutting a release, choosing a semantic version bump, tagging, or writing a changelog」触发词；新增 3 条 Rationalization + 3 条 Red Flag
- `planning-and-task-breakdown/SKILL.md`（+9 行）：强调 plan 输出到 `tasks/plan.md`，task list 输出到 `tasks/todo.md`（新增 Output Files 章节，明确 `/build` 与下游工具预期路径）
- `spec-driven-development/SKILL.md`（+2 行）：引用 `tasks/plan.md` 与 `tasks/todo.md` 输出约定，指向 `/plan` 惯例
- `frontend-ui-engineering/SKILL.md`（frontmatter 微调）：description 增加「accessible, responsive」+ WCAG 触发词
- `performance-optimization/SKILL.md`（frontmatter 微调）：description 增加「across frontend, backend, queries, and databases」+ N+1 触发词
- `references/security-checklist.md`（+60 行）：新增 manager × install × audit 命令矩阵（npm / pnpm / Yarn 1-4+），新增「Install-Script Gate」段落，含按 manager 版本号的 policy 表（npm 11.18.x / 12.x、pnpm 10.x / 11+、Yarn 2-4.14+ / 1）
- `references/testing-patterns.md`（+21/-21 行）：Playwright 示例改用 `getByRole` / `getByLabel` role-based locator（替换旧的 CSS selector 写法）
- `commands/webperf.toml`（小修订）：CrUX API key 改为 `$CRUX_API_KEY` / `$GOOGLE_API_KEY` 环境变量引用，明确「never hard-code these values」

**2. 新增**（skills / commands / agents / hooks / references 出现新文件）
- `evals/`：全新三层级 skill eval 框架——`README.md`（文档）+ `cases/*.json`（24 个 skill 各一个 routing case）+ `scripts/run-evals.js`（449 行的 executor）；含 trace grading、owners、trust levels 机制，Tier 3 强化 + 负样例成对路由测试
- `.codex-plugin/plugin.json`：Codex CLI 插件声明；配套 `docs/codex-setup.md`（Codex CLI v0.122+ 安装指引）
- `.agents/plugins/marketplace.json`：refer 自身 marketplace 配置
- `docs/adoption-guide.md`（greenfield vs brownfield rollout 决策，含 merge-blocking review label 列表）
- `docs/developer-onboarding.md`（新贡献者 onboarding）
- `scripts/validate-commands.js`：新增跨 CLI command description 一致性校验逻辑（malformed entry 检测）
- `.gitattributes`：文本行结尾归一化（Windows 兼容）

**3. 删除/合并**
- 无实质删除。

**4. 编排层变化**（commands ⇄ agents ⇄ hooks 组合关系）
- **Codex CLI 集成**：`fix: prevent Codex from loading Claude hooks`（防止 Codex 误读 Claude hooks）+ `fix: use root Codex plugin layout`（简化 plugin 路径）+ `docs(codex): update install command for Codex CLI v0.122+`（breaking 命令更新）
- **HTTPS git-config workaround**：`docs: document the HTTPS git-config workaround for the /plugin install`——新增 `git config --global url."https://github.com/".insteadOf git@github.com:` 作为 Windows/macOS 上 SSH 失败的统一解决方案
- **Eval 框架纳入 CI**：`feat(evals): add a three-tier skill eval framework` + `feat(evals): harden Tier 3 and make negatives pairwise routing tests` + `fix(evals): cover description vocabulary gaps` + `fix(evals): pipe grader prompt via stdin; grant executor tool permissions`
- **AGENTS.md / CLAUDE.md scope 声明**：新增顶部 scope 提示，明确这两个文件仅作用于 refer 仓库自身，不应被复制到其他项目或全局配置
- **`commands/webperf.toml`**：Deep mode 触发条件进一步细化（CrUX key 文档化）

#### 同步决策

- **要同步**：
  - `security-and-hardening` 的 supply-chain 重写（manager 边界识别 + install-script gate + provenance 验证 + 反对 forced fix）→ 写入 `ys-powers/skills/security-and-hardening/SKILL.md`；同步 `references/security-checklist.md` 的 manager × install × audit 矩阵与 version-pinned policy 表
  - `deprecation-and-migration` 的 Expand/Contract 数据库迁移章节 → 写入 `ys-powers/skills/deprecation-and-migration/SKILL.md`（含 5 规则 + 3 反模式 + 3 红旗 + Verification）
  - `code-review-and-quality` 的「Upgrading an existing dependency」子节 → 写入 `ys-powers/skills/code-review-and-quality/SKILL.md`（含 5 纪律 + 2 反模式 + 2 红旗 + Verification 增加 1 条）
  - `git-workflow-and-versioning` 的「Release & Versioning」章节 → 写入 `ys-powers/skills/git-workflow-and-versioning/SKILL.md`（ys-powers 当前完全缺失此能力）；同步 frontmatter description 触发词
  - `frontend-ui-engineering` / `performance-optimization` 的 frontmatter 触发词收紧 → 写入对应 SKILL.md
  - `planning-and-task-breakdown` / `spec-driven-development` 的 `tasks/plan.md` / `tasks/todo.md` 输出约定 → 写入对应 SKILL.md，并核对 ys-powers 的 `/ys-plan` 命令当前是否真的写到 `tasks/plan.md`（当前 grep 显示无此约定，需决策）

- **暂不同步**：
  - `evals/` + `scripts/run-evals.js` —— refer 24-skill 三层级 eval 框架；ys-powers 自身 skill ~30，触发词与路由语义不同，全盘移植工作量大；可参考框架思想但独立构建
  - `.codex-plugin/` + `docs/codex-setup.md` —— ys-powers 仅服务 Claude Code
  - `.agents/plugins/marketplace.json` —— refer 自身 marketplace 配置
  - `scripts/validate-commands.js` —— 多 CLI 同步校验器，ys-powers 无此需求
  - `docs/adoption-guide.md` / `docs/developer-onboarding.md` / `docs/codex-setup.md` / `docs/copilot-setup.md` / `docs/cursor-setup.md` 等多 CLI setup 文档 —— 仅服务 refer 自身多平台分发
  - `.gitattributes` —— refer CI 自身的 Windows 兼容
  - `commands/webperf.toml` —— ys-powers 无 `webperf` command
  - `references/testing-patterns.md` 的 Playwright role-based locator 示例 —— ys-powers 不直接维护 testing reference
  - `.gemini/` —— 本次无变更，标记不相关
  - `README.md` / `CONTRIBUTING.md` 的多 CLI 路由 + skills CLI 推广 —— 仅与 refer 分发相关

- **已确认同步**：
  - `AGENTS.md` / `CLAUDE.md` scope 提示 —— ys-powers 自身 CLAUDE.md 已经在第 1 段写明本仓库上下文，且 refer 已在 `docs/agent-skills/CLAUDE.md` 顶部标注「Claude 不应修改 refer/ 下任何文件」，无需重复同步

- **待定**：
  - **是否引入 evals 框架**：ys-powers skill ~30，写 30 个 routing case + 配 eval runner 是中型工程。引入会让 quality gate 更扎实；不引入则保留当前 manual review。可在 `/wskill` 或 `using-agent-skills` 升级时一并决策
  - **`tasks/plan.md` 输出约定是否在 ys-powers /ys-plan 命令中落地**：refer 已统一为 `tasks/plan.md` + `tasks/todo.md`，ys-powers 当前 `/ys-plan` 命令（`commands/ys-plan.md`）未规定此路径。需核对：是否同步约定，或保留 ys-powers 自身惯例
  - **refer `references/security-checklist.md` 与 ys-powers `references/security-checklist.md` 的同步策略**：两个项目各自维护同名 checklist，本次 refer 大幅扩充 manager 矩阵与 install-script gate。ys-powers 端应优先采用 refer 端方法论，但 checklist 形式可独立维护

#### TODO

- [ ] 同步 `security-and-hardening`：install-script gate + manager 边界识别 + provenance 验证章节（重写风格按 `writing-skills`）
- [ ] 同步 `references/security-checklist.md`：manager × install × audit 命令矩阵 + version-pinned policy 表
- [ ] 同步 `deprecation-and-migration`：Expand/Contract 数据库迁移章节（5 规则 + 3 反模式 + 3 红旗 + Verification）
- [ ] 同步 `code-review-and-quality`：Upgrading an existing dependency 子节（5 纪律 + 2 反模式 + 2 红旗 + Verification）
- [ ] 同步 `git-workflow-and-versioning`：Release & Versioning 章节（SemVer / tag / changelog）+ frontmatter 触发词
- [ ] 同步 `frontend-ui-engineering` / `performance-optimization` 的 frontmatter 触发词
- [ ] 决策：`tasks/plan.md` / `tasks/todo.md` 输出约定是否在 `/ys-plan` 命令落地；若是，修改 `commands/ys-plan.md` 与 `/build` 期望路径
- [ ] 决策：是否引入三层级 evals 框架（参考 `refer/evals/` 与 `scripts/run-evals.js`）
- [ ] 决策：`references/security-checklist.md` 是直接同步 refer 内容，还是仅对齐方法论、独立维护 checklist

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
  - `observability-and-instrumentation` skill 是否引入 ys-powers → 需用户决策。引入会扩 ys-powers skill 数至 30+；不引入则依赖 `using-agent-skills` 决策树指向 refer 即可（与 `sop-search` / `writing-skills` 现状一致）
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
