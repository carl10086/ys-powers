# docs/agent-skills 概览 + CLAUDE.md docs 章节 设计

- 日期：2026-04-26
- 类型：文档新增 + CLAUDE.md 增补
- 目标产出：
  - `docs/agent-skills/overview.md`（新建）
  - `CLAUDE.md` 增加"docs/ 项目内部文档"专节

## 背景

`refer/agent-skills/` 是新近加入的第三方参考项目，下含 21 个 skill。仓库 `docs/` 已经为其他参考项目（superpowers、ys-powers、systematic-debugging）准备了对照笔记目录；这次需要为 agent-skills 也建立同样的对照笔记目录，并在 `CLAUDE.md` 中点明 `docs/` 整体的组织约定。

## 目标

1. 在 `docs/agent-skills/overview.md` 给出 21 个 skill 的中文索引（"定位 + 适用场景"格式），按 agent-skills 项目自身的 6 阶段方法论分组。
2. 更新 `CLAUDE.md`，新增"docs/ 项目内部文档"章节，让 Claude 看到整个 docs/ 的子目录划分及约定。

## 非目标

- 不直接搬运 SKILL.md 英文 description，要重写为中文。
- 不分析 agent-skills 内每个 skill 的实现细节（这是后续 deep-dive 的事）。
- 不修改 `refer/agent-skills/` 任何文件。
- 不为 docs 下其他子目录（codebase、superpowers 等）生成新内容。

## 设计

### 1. `docs/agent-skills/overview.md`

#### 文件结构

```
1. 标题与引言（2-3 句）
   - 这是 refer/agent-skills 21 个 skill 的中文索引
   - 用途：快速定位想借鉴的 skill；详细内容回 SKILL.md
   - 边界：refer/ 只读

2. 按阶段分组的 skill 列表（6 个 + 1 个 Meta）
```

#### 阶段分组（共 21 个）

| 阶段 | 数量 | Skills |
|------|------|--------|
| Define | 2 | spec-driven-development, idea-refine |
| Plan | 1 | planning-and-task-breakdown |
| Build | 6 | incremental-implementation, test-driven-development, context-engineering, source-driven-development, frontend-ui-engineering, api-and-interface-design |
| Verify | 2 | browser-testing-with-devtools, debugging-and-error-recovery |
| Review | 4 | code-review-and-quality, code-simplification, security-and-hardening, performance-optimization |
| Ship | 5 | git-workflow-and-versioning, ci-cd-and-automation, deprecation-and-migration, documentation-and-adrs, shipping-and-launch |
| Meta | 1 | using-agent-skills |

阶段命名：Define / Plan / Build / Verify / Review / Ship 与 agent-skills 项目自身 CLAUDE.md 一致；Meta 单列。

#### 每个 skill 的格式

```markdown
- **<skill-name>** — <一句话定位，中文重写自 frontmatter description 第一部分>。**适用查阅**：<一句话 trigger 场景，重写自 description 第二部分>。
```

示例：

> - **spec-driven-development** — 在动代码前写好结构化规范，作为人机共识的"事实之源"。**适用查阅**：项目刚启动、需求模糊、改动跨多文件，或要做架构决策时。

#### 引言段落的关键内容

- 文档定位：refer/agent-skills 21 个 skill 的中文索引
- 不复制粘贴：要借鉴的 skill 应在 `skills/` 目录下重写
- 详细内容：参见 `refer/agent-skills/skills/<name>/SKILL.md`
- 阶段映射来源：与 agent-skills 自带 CLAUDE.md 的 "Skills by Phase" 一致

### 2. `CLAUDE.md` 增补

#### 插入位置

在现有"顶层目录速览"小节之后、"refer/ 第三方参考项目"小节之前，插入新的 `## docs/ 项目内部文档` 章节。

#### 章节内容（约 8-12 行）

```markdown
## docs/ 项目内部文档

按主题划分子目录，每个子目录聚焦一个话题：

- `docs/codebase/` — 本仓库自身的架构文档（ARCHITECTURE.md）
- `docs/agent-skills/` — refer/agent-skills 项目的中文索引/笔记
- `docs/superpowers/` — refer/superpowers 项目的 skill 分析及实施 specs（specs/ 子目录）
- `docs/systematic-debugging/` — systematic-debugging 主题专栏
- `docs/ys-powers/` — ys-powers 自身 skill / command 的分析笔记
- 顶层散文件（如 `claude-prompt-design-paradigms.md`）— 跨主题的零散研究

约定：与 `refer/<X>/` 同名的 `docs/<X>/` 是该参考项目的对照笔记；spec 类设计文档放在 `docs/superpowers/specs/`。
```

## 实施步骤

1. 创建 `docs/agent-skills/` 目录。
2. 通读 21 个 SKILL.md 的 frontmatter，提炼 description，逐个写中文"定位 + 适用场景"两句。
3. 写入 `docs/agent-skills/overview.md`。
4. 在 `CLAUDE.md` 现有"顶层目录速览"和"refer/ 第三方参考项目"之间插入 `## docs/ 项目内部文档` 章节。
5. 通读检查：阶段分组数量加和等于 21，CLAUDE.md 顺序合理。

## 验收标准

- `docs/agent-skills/overview.md` 存在，按 6 阶段 + Meta 分组列出 21 个 skill，每个均有"定位 + 适用查阅"两句中文。
- `CLAUDE.md` 增加 `## docs/ 项目内部文档` 章节，列出现有 5 个子目录并写明对照约定。
- 阶段分组数量加和 = 21；与 agent-skills 自带 CLAUDE.md 的 Skills by Phase 一致（Meta 单列）。
- 没有直接复制英文 description 原文。

## 不在本次范围

- 改动 `README.md`。
- 修改 `refer/` 下任何文件。
- 为 docs 下其他子目录（superpowers / ys-powers / codebase）补充内容。
- 为 agent-skills 各 skill 写更深的 deep-dive 分析。
