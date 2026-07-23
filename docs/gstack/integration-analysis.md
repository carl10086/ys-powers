# gstack 能力借鉴与集成分析（第二版）

> 分析日期：2026/05/25
> 分析对象：`refer/gstack/` vs `ys-powers/` 现有能力
> 核心结论：**不存在 P0 级缺失**。gstack 与 ys-powers 是**互补关系**，而非代差关系。
> 约束：refer/ 下文件**只读**；借鉴时须在 ys-powers 自有目录重写，禁止直接复制粘贴。

---

## 第一部分：公允对比 — ys-powers 的优势领域

经过对 26 个 skills、19 个 commands、rules、SOP 系统的完整审计，ys-powers 在以下领域**明显更强或至少持平**：

| 领域 | ys-powers 的能力深度 | gstack 的对应能力 | 结论 |
|------|---------------------|-------------------|------|
| **技能/命令编写方法论** | `writing-great-skills` 用 predictability、information hierarchy、progressive disclosure 和 no-op pruning 设计可预测能力 | 直接写模板，无系统剪枝机制 | **ys-powers 独有** |
| **编码规范体系** | `code.md` 行为指南 + `code-simplification` + 五轴审查 + Code Smells 目录 | 审查有子专家分工，但无系统规范约束 | **ys-powers 更系统** |
| **Git 工作流** | `git-workflow-and-versioning` + `gc` + `s2m` + `local-commit` + worktree 支持 | 基础 git 操作 + `/ship` | **ys-powers 更完整** |
| **发布流程** | `shipping-and-launch`（feature flag、staged rollout、rollback plan、监控阈值表） | `/ship` 自举测试框架，但发布策略较薄 | **ys-powers 更深** |
| **文档工程** | `documentation-and-adrs` + `build-doc`（强制 HTML 预览）+ `doc-codebase`（8 段 ARCHITECTURE.md 模板） | Diataxis 体系 + `/document-generate` | **各有特色，持平** |
| **HTML 生成** | `html-anything`（17+ 风格，30+ 数据源） | `/design-html`（Pretext UI，30KB） | **ys-powers 更丰富** |
| **经验沉淀** | `sop-search` + `sop-add`（从会话自动提取结构化 SOP） | `/learn`（结构化学习记录） | **各有特色，持平** |
| **源码驱动** | `source-driven-development`（强制引用官方文档，拒绝 Stack Overflow） | 无对应能力 | **ys-powers 独有** |
| **教学能力** | `teach-code`（"教一段问一段"交互模式） | 无 | **ys-powers 独有** |
| **调试方法论** | `debugging-and-error-recovery`（Stop-the-Line、最小失败用例、回归测试） | `/investigate`（系统化根因分析） | **持平** |

**关键洞察**：ys-powers 不是"缺东西"，而是**角度不同**。ys-powers 聚焦**工程正确性**（编码规范、Git 工作流、测试方法论、源码验证），gstack 聚焦**产品交付速度**（CEO 视角、设计探索、浏览器闭环、发布后监控）。两者的差异是**互补**，不是**代差**。

---

## 第二部分：真正的互补点 — 值得关注的能力

以下 gstack 能力可以为 ys-powers 用户带来**明确增益**，按投入产出比排序：

### A. 低投入高回报（建议近期引入）

#### 1. 安全防护硬边界：`/careful` + `/freeze` + `/guard`

| 维度 | 详情 |
|------|------|
| **gstack 做法** | `/careful` 在破坏性命令前强制警告；`/freeze` 硬阻断对指定目录外的编辑；`/guard` 同时激活两者。 |
| **ys-powers 现状** | 完全无此能力，依赖 Claude 内置安全机制和用户确认。 |
| **为什么值得关心** | 防止 AI 在自主模式（如 `/build` 或 `/refactor`）下误执行危险操作（`rm -rf`、force-push、误删迁移文件）。这是**防御性基础设施**，投入极低（CLAUDE.md 规则注入），收益明确。 |
| **集成建议** | 新增 `ys-guard` command，通过规则注入实现"冻结目录"和"危险命令警告"。不改动现有 workflow，作为可选安全网。 |

#### 2. 代码健康仪表盘：`/health`

| 维度 | 详情 |
|------|------|
| **gstack 做法** | 聚合类型检查、lint、测试、死代码检测，输出 0-10 分质量分数和趋势。 |
| **ys-powers 现状** | 有 `code-review-and-quality`、`code-simplification`、`security-and-hardening`，但无**统一量化仪表盘**。 |
| **为什么值得关心** | 质量退化是渐进的，需要**可量化的监控**才能及时发现。对技术负责人管理多项目尤其有价值。 |
| **集成建议** | 新增 `ys-health` command，聚合 `tsc`、`eslint`、`test`、`knip`（死代码）结果并输出分数。复用现有工具，不引入新依赖。 |

#### 3. 跨会话上下文快照：`/context-save` + `/context-restore`

| 维度 | 详情 |
|------|------|
| **gstack 做法** | 保存当前工作状态（git 状态、决策、剩余任务、关键文件），跨会话恢复。 |
| **ys-powers 现状** | `context-engineering` 管理上下文层次，但无**持久化快照**机制。 |
| **为什么值得关心** | Claude 的上下文压缩会导致"每次会话从零开始"，特别是对于多日的复杂任务。快照恢复可显著降低续作成本。 |
| **集成建议** | 基于 `.claude/memory/` 扩展，新增 `context-save` / `context-restore` commands。格式为结构化 Markdown + YAML frontmatter，无需外部数据库。 |

### B. 中等投入，场景特定（按需引入）

#### 4. 产品视角前置：`/office-hours`

| 维度 | 详情 |
|------|------|
| **gstack 做法** | YC 风格的 6 个强制性问题，从商业/用户价值角度重新框定需求。 |
| **ys-powers 现状** | `idea-refine`、`explore-then-ask`、`spec-driven-development` 覆盖从想法到设计，但**缺少 CEO/产品视角的强制审查**。 |
| **为什么值得关心** | 工程团队容易陷入"用优雅方案解决错误问题"。`/office-hours` 不是日常工具，而是**项目启动时的疫苗**——在投入大量工程资源前验证方向。 |
| **为什么不是 P0** | 对已有明确需求的工程任务价值有限，不是每次编码都需要。 |
| **集成建议** | 新增可选 `ys-office-hours` command，提取 6 个核心问题的精简版（~150 行 prompt）。不纳入默认 workflow，由用户按需调用。 |

#### 5. 浏览器闭环 QA：`/qa`

| 维度 | 详情 |
|------|------|
| **gstack 做法** | 打开真实浏览器 → 找 bug → 原子修复 → 回归验证 → 生成回归测试。 |
| **ys-powers 现状** | `browser-testing-with-devtools` 是**观察工具**（截图、DOM 检查、控制台分析），无自主修复和回归测试生成闭环。 |
| **为什么值得关心** | 把浏览器测试从"人看报告"升级为"AI 闭环修复"，对前端项目有明确增益。 |
| **为什么不是 P0** | 实现较重（需 Playwright 或 headless browser），且 `browser-testing-with-devtools` 已覆盖 80% 场景。 |
| **集成建议** | 中期项目。先调研 Playwright MCP 的可行性；若可行，扩展 `browser-testing-with-devtools` 的"修复 + 回归测试"分支。 |

#### 6. 工程复盘：`/retro`

| 维度 | 详情 |
|------|------|
| **gstack 做法** | 每周复盘，含个人分工、shipping streak、质量趋势。 |
| **ys-powers 现状** | `sop-add` 沉淀具体经验，但无**周期性复盘**机制。 |
| **为什么值得关心** | 帮助个人和小团队建立持续改进循环。对独立开发者尤其有价值。 |
| **为什么不是 P0** | 低紧迫度，属于"有好过没有"的工具。 |
| **集成建议** | 新增 `ys-retro` command，基于 `git log` 和本周变更自动生成结构化复盘模板。低投入。 |

### C. 观望中（待验证需求）

| 能力 | 说明 | 观望理由 |
|------|------|----------|
| `/canary` 发布后持续监控 | 部署后循环检测控制台错误、性能回退 | `shipping-and-launch` 已有 post-launch 验证，持续监控可用现有监控工具替代 |
| `/design-shotgun` 视觉探索 | AI mockup 变体生成 | 依赖 GPT Image API，投入高，场景窄（非设计师用户） |
| `/devex-review` DX 审计 | 真实走 onboarding，截图错误 | 有价值但耗时（20-45 分钟），适合季度而非日常 |

---

## 第三部分：明确不值得关心的

以下能力与 ys-powers 的定位冲突，或投入产出比过低，**明确排除**：

| 能力 | 排除理由 |
|------|----------|
| iOS 全系列（`/ios-qa`、`/ios-fix` 等） | 平台特定，仅 iOS 开发者需要，且依赖 macOS + Xcode |
| Chrome 扩展 (`extension/`) | 独立产品级别工作量，与 ys-powers CLI 工具定位冲突 |
| 多智能体适配层 (`hosts/`) | ys-powers 明确聚焦 Claude Code 生态，不追求跨 CLI 兼容 |
| OpenClaw 集成 | 除非用户明确使用 OpenClaw，否则不进入此赛道 |
| `/codex`（第二意见） | 依赖 OpenAI Codex CLI，与单模型专注冲突 |
| gbrain 跨机器同步 | 基础设施重（PGLite/Supabase），`.claude/memory/` + SOP 已覆盖 80% 场景 |
| `/make-pdf` | 独立工具，与核心工程工作流无关 |
| `/benchmark-models` | 跨模型技能基准，偏研究性质，对终端用户价值有限 |
| `/scrape` + `/skillify` | 网页数据抓取 → 固化技能，场景偏窄 |

---

## 第四部分：集成建议

### 原则

1. **不追全覆盖** — gstack 是 Garry Tan 的**个人软件工厂**，含大量特定需求（iOS、PDF、多智能体）。ys-powers 是**通用工程增强包**，只引入对大多数开发者有复用价值的能力。
2. **低投入优先** — 优先引入可通过规则注入、prompt 工程、现有工具聚合实现的能力，避免引入外部基础设施。
3. **重写而非搬运** — 所有借鉴必须在 `skills/` / `commands/` / `docs/` 下**重写**（按主题放入对应子目录），禁止直接复制 gstack 的 SKILL.md 模板。
4. **与现有体系兼容** — 新增能力必须适配 `install/local-install.py` 和目录结构。

### 建议引入清单

| 优先级 | 能力 | 形式 | 投入 | 预期收益 |
|--------|------|------|------|----------|
| 1 | `ys-guard`（安全防护边界） | command | 低（规则注入） | 防止 AI 误执行危险操作 |
| 2 | `ys-health`（代码健康仪表盘） | command | 低（工具聚合） | 量化质量监控 |
| 3 | `context-save/restore`（上下文快照） | command pair | 中（基于 memory 扩展） | 跨会话续作 |
| 4 | `ys-office-hours`（产品视角审查） | command | 低（prompt 工程） | 项目启动方向验证 |
| 5 | `ys-retro`（工程复盘） | command | 低（git log 聚合） | 持续改进循环 |
| 6 | 浏览器闭环 QA | skill 扩展 | 高（需 Playwright） | 前端 bug 自动修复 |

### 不建议做的事情

- 不引入 gstack 的 `/autoplan` 一键流水线 — ys-powers 的 `spec` → `plan` → `build` → `test` → `ship` 流程已足够系统，强制串行审查反而降低灵活性
- 不升级 `security-and-hardening` 为子专家模式 — 当前的五轴审查 + `security-and-hardening` 三层级（Always/Ask/Never）已足够系统，子专家分工增加复杂度而不增加覆盖率
- 不引入 Diataxis 文档类型标记 — `build-doc` 的强制 HTML 预览 + `doc-codebase` 的 8 段模板已足够实用，Diataxis 分类增加认知负担

---

## 附录：重点能力详细设计

以下为建议近期引入的 3 个能力的详细设计草案，供 implementation 参考。

---

### 附录 A：`ys-guard` 安全防护边界

#### 定位
防御性基础设施。通过 CLAUDE.md 规则注入，在 AI 自主执行 workflow（如 `/build`、`/refactor`）时提供硬边界，防止误删、误改、误推。

#### 触发条件
- 用户显式运行 `/ys-guard` 或 `/ys-guard on`
- 可在 `plan` 或 `spec` 阶段作为可选步骤自动建议启用
- 对涉及数据库迁移、文件删除、git 强制操作的会话自动激活

#### 工作流

```
1. 检测当前项目根目录（git top-level）
2. 写入/更新 .claude/rules/guard.md：
   - DANGEROUS_COMMANDS: rm -rf, git push --force, git reset --hard,
     DROP TABLE, DELETE FROM, ALTER TABLE ... DROP COLUMN,
     任何涉及 production secrets 的文件写入
   - FREEZE_SCOPE: 当前 git 根目录（允许子目录）
   - 规则：执行 DANGEROUS_COMMANDS 前必须 AskUserQuestion 确认
   - 规则：禁止编辑 FREEZE_SCOPE 外的任何文件
3. 向用户确认 guard 已激活，显示保护范围
4. （可选）/ys-guard off 移除规则
```

#### 输出格式
- 终端输出：
  ```
  🛡️ ys-guard 已激活
  冻结范围：/Users/carlyu/project/xyz
  危险命令拦截：rm -rf, git push --force, DROP TABLE, ...
  运行 /ys-guard off 解除
  ```

#### 与现有能力的交互
- 与 `build`、`refactor`、`ship` 等 commands **无侵入兼容** — guard 通过规则文件生效，不改动 command 逻辑
- 与 `code.md` 规则协同 — guard.md 作为 code.md 的补充层，优先级更高

#### 实现约束
- **零外部依赖** — 纯规则注入，不写代码
- **文件体积** — guard.md < 100 行
- **不阻断正常 workflow** — 只拦截明确危险的命令，常规 git 操作、文件编辑不受影响
- **可逆** — 用户可随时 `/ys-guard off` 解除

---

### 附录 B：`ys-health` 代码健康仪表盘

#### 定位
量化质量监控工具。聚合项目中已有的质量工具，输出统一分数和趋势，让质量退化**可见**。

#### 触发条件
- 用户显式运行 `/ys-health`
- 建议作为 `ship` command 的 pre-check 可选步骤
- 建议每周由用户手动运行一次（不适合每次 commit 运行，避免噪音）

#### 工作流

```
1. 探测项目类型和可用工具：
   - TypeScript: 检查 tsc、eslint、knip 是否存在
   - Python: 检查 mypy、ruff、vulture
   - Go: 检查 go vet、staticcheck
   - Rust: 检查 cargo check、clippy
2. 并行运行可用工具，捕获 exit code 和输出摘要
3. 统计维度：
   - 类型安全（tsc/mypy 错误数 → 分数）
   - 代码规范（eslint/ruff 错误数 → 分数）
   - 测试覆盖（测试通过率 + 覆盖率 → 分数）
   - 死代码（knip/vulture 未引用数 → 分数）
   - 安全漏洞（npm audit / pip-audit 高危数 → 分数）
4. 计算总分（0-10，加权平均）
5. 对比上次运行结果（若存在 .claude/memory/health-history.md），显示趋势
6. 生成分项报告，按优先级排序修复建议
```

#### 输出格式

```markdown
# 代码健康报告 — 2026/05/25

**总分：7.2 / 10** （上次：6.8 ↑）

| 维度 | 分数 | 状态 | 详情 |
|------|------|------|------|
| 类型安全 | 8.5 | 🟢 | tsc: 0 错误 |
| 代码规范 | 7.0 | 🟡 | eslint: 12 warnings（3 个可自动修复）|
| 测试覆盖 | 6.5 | 🟡 | 通过率 100%，覆盖率 62%（目标 80%）|
| 死代码 | 9.0 | 🟢 | knip: 2 个未引用导出 |
| 安全漏洞 | 5.0 | 🔴 | npm audit: 1 critical, 3 high |

## 优先修复
1. [🔴] 运行 `npm audit fix` 修复 1 critical 漏洞
2. [🟡] 运行 `eslint --fix` 自动修复 3 个 warning
3. [🟡] 为 src/utils/validator.ts 补充测试（当前 0% 覆盖）
```

#### 与现有能力的交互
- 被 `ship` command **可选调用** — 在 pre-launch checklist 中增加健康分数门槛（如 < 6 分提示风险）
- 与 `code-simplification` 协同 — health 报告中的死代码项可直接触发简化任务
- 与 `security-and-hardening` 协同 — 安全漏洞项直接引用其修复指南

#### 实现约束
- **复用现有工具** — 不引入新的 linter/类型检查器，只聚合已有工具
- **零配置优先** — 自动探测工具链，用户无需手动配置
- **历史记录轻量** — 只保留最近 10 次运行的分数和趋势，存储于 `.claude/memory/health-history.md`
- **失败优雅** — 若某工具未安装，该维度标记为 N/A，不影响总分计算

---

### 附录 C：`context-save` + `context-restore` 跨会话上下文快照

#### 定位
解决 Claude 上下文压缩导致的"每次会话从零开始"问题。保存复杂任务的中间状态，支持跨日续作。

#### 触发条件

**context-save：**
- 用户显式运行 `/context-save`
- 长任务（> 30 分钟）结束时自动建议
- 会话结束前检测到未完成任务时提示

**context-restore：**
- 用户显式运行 `/context-restore`
- 进入项目时检测到存在未恢复的上下文快照时提示

#### 工作流

**context-save：**
```
1. 收集当前会话状态：
   - git 状态（分支、未提交变更、最近 commit）
   - 当前活跃任务（从 plan 或 task list 读取）
   - 已做出的关键决策（从 conversation 提取）
   - 剩余工作清单（从 plan 的未完成 task 读取）
   - 关键文件路径（最近编辑的 5-10 个文件）
   - 已知阻塞点（从 conversation 提取"TODO:"、"FIXME:"、"blocked by"）
2. 生成结构化快照文件：.claude/memory/context-snapshots/YYYY-MM-DD-HH-{keyword}.md
3. 向用户确认快照已保存，显示摘要
```

**context-restore：**
```
1. 扫描 .claude/memory/context-snapshots/ 目录，列出最近快照
2. 用户选择要恢复的快照（或自动选最新）
3. 读取快照文件，向用户展示摘要：
   - 上次工作到哪个 task
   - 哪些决策已做出
   - 当前阻塞点是什么
4. 用户确认后，加载相关文件上下文，继续执行
```

#### 输出格式（快照文件）

```markdown
---
type: context-snapshot
created: 2026-05-25T14:30:00
project: ys-powers
branch: feat/health-command
keyword: health-command-halfway
---

# 上下文快照：health-command-halfway

## 当前任务
实现 `ys-health` command（源自 gstack 借鉴分析）
- [x] 阅读 gstack /health 实现参考
- [x] 设计 ys-health 工作流和输出格式
- [ ] 编写 command 文件
- [ ] 测试在 TypeScript 项目上的行为
- [ ] 更新 integration-analysis.md 文档

## 已做出的关键决策
1. **工具探测策略**：自动检测 tsc/eslint/knip，不强制要求全部存在
2. **分数算法**：加权平均，类型安全 30%、代码规范 20%、测试覆盖 25%、死代码 15%、安全漏洞 10%
3. **历史记录**：只保留 10 次，存于 `.claude/memory/health-history.md`

## 已知阻塞点
- 不确定 Python 项目的工具链探测是否准确（需要测试）
- 与 `ship` command 的集成方式待确认

## 相关文件
- `docs/gstack/integration-analysis.md`（附录 B）
- （待创建）`commands/ys-health.md`

## Git 状态
- 分支：feat/health-command
- 未提交：docs/gstack/integration-analysis.md（修改）
- 上次 commit："docs(gstack): update integration analysis v2"
```

#### 与现有能力的交互
- 与 `plan` / `build` / `test` commands 协同 — 快照中的任务列表直接对接 plan 的任务系统
- 与 `sop-add` 区分 — context-save 保存**当前进行中的状态**，sop 保存**已完成的经验**。两者互补，不重复
- 与 `.claude/memory/` 协同 — 快照存于 `context-snapshots/` 子目录，不污染 memory 根目录

#### 实现约束
- **无外部数据库** — 纯 Markdown 文件，基于 `.claude/memory/` 扩展
- **自动清理** — 只保留最近 20 个快照，超出的自动归档到 `context-snapshots/archive/`
- **轻量提取** — 不尝试用 NLP 分析整个 conversation，只提取结构化的 plan/task/decision/blocker 信息
- **人工确认** — restore 时必须经过用户确认，避免自动加载过时上下文导致误判

---

## 相关文档

- [overview.md](overview.md) — gstack 总体介绍与架构概览
- [skills-inventory.md](skills-inventory.md) — gstack 完整技能清单
- 原始项目：`refer/gstack/`（**只读**）
