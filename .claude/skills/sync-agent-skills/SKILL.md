---
name: Syncing Agent Skills
description: Detects refer/agent-skills upstream updates, extracts Claude Code-relevant changes, generates structured refer-commit.md entries, and recommends ys-powers sync actions. Focuses on Claude Code ecosystem; ignores .gemini/. Use when refer is behind origin/main, user asks to sync agent-skills, or refer-commit.md needs maintenance.
---

# Syncing Agent Skills

## Overview

`refer/agent-skills/` 是 ys-powers 的方法论上游。本 skill 封装了从"检测更新"到"生成同步决策"的完整工作流，确保 refer 的每次更新都被系统化地记录和分析。

## When to Use

- refer/agent-skills 的 origin/main 比本地领先（`git status` 提示 "Your branch is behind"）
- 用户说"更新 refer"、"同步 agent-skills"、"看看 refer 有什么新变化"
- 需要维护 `docs/agent-skills/refer-commit.md` 工作日志

## When NOT to Use

- 实际执行代码修改（用 `incremental-implementation` 或 `build`）
- 只查历史经验不更新（用 `sop-search`）
- 一般性的 git 操作（用 `git-workflow-and-versioning`）

## Process

```
Progress:
- [ ] Step 1: 记录起点 commit
- [ ] Step 2: 安全 pull 更新
- [ ] Step 3: 提取变更清单
- [ ] Step 4: 4 维度变更分析
- [ ] Step 5: 同步决策
- [ ] Step 6: 写入 refer-commit.md
- [ ] Step 7: 推荐下一步
- [ ] Verification: 6 项 checklist 通过
```

### Step 1: 获取更新前快照

```bash
cd refer/agent-skills
git log -1 --format="%H %h %ai %s"
```

记录当前 HEAD commit hash 作为本次分析的**起点**，记为 `<prev>`。同时记录 ys-powers 自身同期 commit。

> **终止条件**：若 refer 已是 `origin/main` 最新状态（`git status` 显示 "Your branch is up to date"），停止并告知用户无需更新。

### Step 2: Pull 更新

```bash
git status
```

- 若工作树不是 clean，停止并提示用户处理未提交变更
- 若存在冲突风险，停止并交由用户处理
- 确认安全后执行：

```bash
git pull
```

如果 pull 过程中产生冲突，停止并交由用户处理。

### Step 3: 提取变更清单

```bash
git log --oneline <prev>..HEAD          # commit 列表（<prev> 为 Step 1 记录的起点 commit hash）
git diff --name-status <prev> HEAD       # 文件级变更
git diff --stat <prev> HEAD              # 变更统计
```

### Step 4: 4 维度变更分析

对每一项变更，分类到以下 4 个维度：

| 维度 | 说明 | 示例 |
|---|---|---|
| **1. 方法论修订** | 既有 `skills/<name>/SKILL.md` 的内容变化 | 某 skill 的流程步骤修改、threshold 调整 |
| **2. 新增** | skills / commands / agents / hooks / references 中出现新文件 | 新增 skill、新增 command、新增 hook |
| **3. 删除/合并** | 目录或文件被移除/合并 | skill 下线、command 合并 |
| **4. 编排层变化** | commands ⇄ agents ⇄ hooks 的组合关系变化 | /ship 改为 fan-out、hook 触发条件变化 |

**专注规则**：
- 仅分析与 **Claude Code** 生态相关的内容（`.claude/`、`SKILL.md`、hooks）
- `.gemini/`（Gemini CLI）相关变更仅做**简要提及**，标记为"不相关"
- 不展开 `.gemini/commands/*.toml` 的详细内容

### Step 5: 同步决策

对每个相关变更，判断：

- **要同步**：refer 的修复/改进在 ys-powers 中有对应文件，且需要更新
- **暂不同步**：仅与 refer 自身分发相关（如 README marketplace 指引），或 ys-powers 不支持的生态
- **已确认同步**：refer 的改进已在 ys-powers 中存在，无需补充
- **待定**：需要用户决策或进一步调研

### Step 6: 写入 refer-commit.md

在 `docs/agent-skills/refer-commit.md` 中执行：

1. **覆盖 §1 当前快照**：更新为最新 commit 元数据
2. **覆盖 §2 已吸收度索引**：如有新增/删除 skill，更新表格
3. **在 §3 顶部追加 Update Entry**：按固定模板填写
4. **保持 §4 Update Entry 模板不变**

**Entry 模板**：参见 [`entry-template.md`](entry-template.md)。

### Step 7: 推荐下一步

向用户呈现：

1. **本次更新的核心变化**（3 句话以内）
2. **对 ys-powers 的影响评估**（高/中/低）
3. **TODO 清单**：需要用户决策或执行的动作
4. **是否需要立即同步**：如果涉及 hooks 安全修复等紧急事项，明确提示

## Red Flags

| 错误 | 后果 | 如何避免 |
|---|---|---|
| 详细分析 `.gemini/` 内容 | 浪费时间，产出不相关 | 始终标记为"不相关，不展开" |
| 忽略 hooks 安全修复 | 本地项目存在同类漏洞 | 每次更新优先检查 `hooks/` 变更 |
| 遗漏"已确认同步"项 | 用户重复调研已知事实 | 主动对比 refer 与 ys-powers 的同名文件 |
| 假设所有新增 skill 都需要同步 | 过度同步，增加维护负担 | 仅当 skill 与当前工作流相关时才推荐 |
| 不写 refer-commit.md | 后续更新无法追溯基线 | 每次 pull 后必须生成 entry |

## Verification

- [ ] refer 的起点 commit hash 已记录
- [ ] refer-commit.md 的 §1 快照已更新为最新 commit
- [ ] §3 顶部新增了本次 update entry
- [ ] entry 中包含完整的 4 维度变更分析
- [ ] 所有 `.gemini/` 变更已被标记为"不相关"
- [ ] 至少包含 1 项"同步决策"（要同步 / 暂不同步 / 已确认同步 / 待定）
- [ ] TODO 清单中的动作可执行、路径明确
