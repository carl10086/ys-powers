# Awesome Claude Skills 文档化设计 Spec

## 1. Objective

为 `refer/awesome-claude-skills/` 建立一套完整的分析文档系统，实现两个目标：

1. **总览索引**：创建一个 `overview.md`，按分类列出所有本地 skill 的名称、定位、触发时机，让人一眼看清awesome-claude-skills 的全貌。
2. **逐个深入**：为每个本地 skill 创建独立的分析文件，结构化摘要其 SKILL.md 的核心内容，提炼与 ys-powers 的关联或借鉴点。

最终产出保留为 Markdown，并通过 `/html` skill 生成 HTML 预览版，方便在浏览器中阅读。

---

## 2. Commands

本工作流不涉及代码编译或测试运行，主要命令/操作如下：

| 命令/操作 | 用途 |
|-----------|------|
| `find refer/awesome-claude-skills -maxdepth 2 -name "SKILL.md"` | 定位所有本地 skill 目录 |
| `cat refer/awesome-claude-skills/<skill>/SKILL.md` | 读取单个 skill 的指令内容 |
| `/html <file-path>` | 生成 HTML 预览（通过 `html-anything` skill） |
| `git add docs/awesome-claude-skills/` | 暂存新文档 |
| `git commit` | 分批提交（每批一个 commit） |

---

## 3. Project Structure

文档目录统一放在 `docs/awesome-claude-skills/`，与 `refer/awesome-claude-skills/` 形成对照关系（遵循 CLAUDE.md 中 "与 `refer/<X>/` 同名的 `docs/<X>/` 是该参考项目的对照笔记" 的约定）。

```
docs/awesome-claude-skills/
├── README.md              # 目录说明：awesome-claude-skills 是什么、文档约定、使用方式
├── overview.md            # 总览索引：按分类列出所有 ~28 个 skill 的摘要
├── index.html             # overview.md 的 HTML 预览版
├── composio-skills.md     # 分类聚合分析（因 composio-skills 子目录极多，需特殊处理）
├── composio-skills.html
├── artifacts-builder.md   # 单个 skill 深入分析
├── artifacts-builder.html
├── brand-guidelines.md
├── brand-guidelines.html
├── ...（其余每个 skill 一一对应）
└── batch-log.md           # 批次执行日志，记录每批完成的 skill 列表和进度
```

### 3.1 composio-skills 的特殊处理

`composio-skills` 子目录下包含 78+ 个 SaaS App 的自动化 skill（如 salesforce-automation、slack-automation 等），数量庞大且结构雷同。不为其每个子 skill 创建独立文件，而是统一在 `composio-skills.md` 中按类别（CRM、项目管理、沟通、代码/DevOps 等）做聚合分析，每个类别提取通用模式和代表性示例。

### 3.2 分类体系

`overview.md` 中的分类沿用 awesome-claude-skills README 中的分类：

- Document Processing
- Development & Code Tools
- Data & Analysis
- Business & Marketing
- Communication & Writing
- Creative & Media
- Productivity & Organization
- Collaboration & Project Management
- Security & Systems
- App Automation via Composio

---

## 4. Code Style（文档风格）

### 4.1 单个 Skill 分析文件模板

每个独立分析文件遵循以下结构：

```markdown
# <Skill 名称>

## 定位
一句话描述这个 skill 解决什么问题。

## 触发时机
- 何时应该使用这个 skill（从 SKILL.md 的 When to Use 提取）
- 何时不应该使用（如有明确的 NOT to use 提示）

## 核心能力
- 能力 1：简述
- 能力 2：简述
- ...

## 指令流程概览
将 SKILL.md 中的指令流程提炼为 3-5 个关键步骤，用结构化列表呈现。不复制全文，只提取骨架。

## 与 ys-powers 的关联
- 是否已有类似 skill？（如 agent-skills、superpowers 中的对应能力）
- 是否值得借鉴搬运到 ys-powers 的 `skills/` 目录？
- 是否有互补价值？

## 元信息
- 来源：`refer/awesome-claude-skills/<skill-name>/SKILL.md`
- 作者/维护者：（从 SKILL.md frontmatter 或 README 链接提取）
- 许可证：（如有标注）
```

### 4.2 写作规范

- 用中文撰写，skill 名称、文件路径、命令名保持英文原文
- 不复制 SKILL.md 全文，只做结构化摘要
- 每个 skill 分析文件控制在 200-500 字（composio-skills 聚合文件可更长）
- 避免主观评价，保持客观描述

---

## 5. Testing Strategy

文档工作的"验证"不同于代码测试，验证标准如下：

| 验证项 | 方法 |
|--------|------|
| 文件完整性 | `ls docs/awesome-claude-skills/*.md | wc -l` 应等于计划文件数 |
| 内容准确性 | 抽查 3-5 个分析文件，对照原始 SKILL.md 确认摘要无偏差 |
| 链接可达性 | `overview.md` 中的内部链接全部可点击跳转 |
| HTML 生成 | 每个 `.md` 都有对应的 `.html`，浏览器打开无报错 |
| 分类一致性 | 所有 skill 在 `overview.md` 中都有归属分类，无遗漏 |

---

## 6. Boundaries

### 6.1 Always Do
- 每个本地 skill 目录至少有一个对应的分析条目（overview 中）或独立文件
- 保留原始 Markdown，HTML 仅作为预览副本
- 每完成一批后 `git commit`，commit message 注明批次号

### 6.2 Ask First
- 如果发现某个 skill 的 SKILL.md 内容极少（< 50 字），是否仍按完整模板写，还是降级为 overview 中的简条目
- 是否需要在 `docs/awesome-claude-skills/` 下创建子目录按分类组织，还是全部平铺

### 6.3 Never Do
- 不修改 `refer/awesome-claude-skills/` 下的任何文件（只读）
- 不为 composio-skills 下的 78+ 个子 skill 创建独立文件（统一聚合）
- 不搬运 awesome-claude-skills 的代码到 ys-powers（仅做分析笔记）
- 不在分析文件中泄露 SKILL.md 中的 API key、token 等敏感信息

---

## 7. Batch Plan（分批执行计划）

共 ~28 个 skill 目录（含 composio-skills），分 4 批：

| 批次 | Skill 列表 | 预计文件数 |
|------|-----------|-----------|
| Batch 1 | overview.md + README.md + artifacts-builder, brand-guidelines, canvas-design, changelog-generator, competitive-ads-extractor, composio-skills | 1 总览 + 1 说明 + 5 单文件 + 1 聚合 = 8 |
| Batch 2 | connect, connect-apps, connect-apps-plugin, content-research-writer, developer-growth-analysis, document-skills, domain-name-brainstormer | 7 单文件 |
| Batch 3 | file-organizer, image-enhancer, internal-comms, invoice-organizer, langsmith-fetch, lead-research-assistant, mcp-builder | 7 单文件 |
| Batch 4 | meeting-insights-analyzer, raffle-winner-picker, skill-creator, skill-share, slack-gif-creator, tailored-resume-generator, template-skill, theme-factory, twitter-algorithm-optimizer, video-downloader, webapp-testing | 11 单文件 + batch-log.md |

每批流程：读取 SKILL.md → 撰写/更新 Markdown → 生成 HTML → `git commit` → 进入下一批。
