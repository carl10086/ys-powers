# refer/agent-skills 同步工作日志

记录 refer/agent-skills 子项目的版本演进，及每次更新对 ys-powers 的同步决策。

> **工作约定**：ys-powers 只关注 **Claude Code** 生态（`.claude/commands/`、`SKILL.md`、hooks）。`.gemini/`（Gemini CLI）相关变更仅做简要提及，不作为同步决策依据。

## 当前快照

- Remote:      https://github.com/addyosmani/agent-skills.git
- Branch:      main
- Commit:      f504276d8e074912f4763e6163b436a4ffc74d0d
- Short:       f504276
- Author Date: 2026-05-02 19:23:40 -0700
- Subject:     Merge pull request #108 from devmarkpro/main
- Worktree:    clean
- 快照时间:    2026-05-03
- ys-powers 同期 commit: 42eb12e5ebb0e8377c2b4de2367d4c7f85d621a5

## 当前 skills 清单（21 个）

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

---

## 更新历史

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
