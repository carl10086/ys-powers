# refer/agent-skills 同步工作日志

记录 refer/agent-skills 子项目的版本演进，及每次更新对 ys-powers 的同步决策。

> **工作约定**：ys-powers 只关注 **Claude Code** 生态（`.claude/commands/`、`SKILL.md`、hooks）。`.gemini/`（Gemini CLI）相关变更仅做简要提及，不作为同步决策依据。

## 当前快照

- Remote:      https://github.com/addyosmani/agent-skills.git
- Branch:      main
- Commit:      2e0dfbfb436ef3307bbe8ba172f14996de980784
- Short:       2e0dfbf
- Author Date: 2026-06-05 18:00:13 -0700
- Subject:     Merge pull request #215 from addyosmani/addyosmani/fix-marketplace-schema
- Worktree:    clean
- 快照时间:    2026-06-07
- ys-powers 同期 commit: d71481c01b7b81f57aaedf5c212730ad1afbd90e

## 当前 skills 清单（23 个）

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

---

## 更新历史

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
