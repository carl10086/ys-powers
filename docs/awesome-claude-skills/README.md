# awesome-claude-skills 分析笔记

本目录是 `refer/awesome-claude-skills/` 的对照笔记，按 [ys-powers 文档化设计 Spec](../ys-powers/specs/2026-05-16-awesome-claude-skills-docs-design.md) 的规范建立。

## 这是什么

[awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) 是由 Composio 维护的社区 Claude Skills 合集，收录了 1000+ 生产级、跨平台兼容的 Skills。本地 `refer/` 目录中保留了其中约 30 个可直接分析的 skill 目录（含 `SKILL.md`），外加 `composio-skills/` 下 800+ 个 SaaS App 自动化 skill。

## 文档约定

- **总览索引**：`overview.md` 按分类列出所有本地 skill 的一览信息
- **逐个深入**：每个 skill 对应一个独立的 `.md` 分析文件，结构化摘要其 `SKILL.md`
- **HTML 预览**：每个 `.md` 都有对应的 `.html`，通过 `/html` skill 生成
- **只读原则**：不修改 `refer/awesome-claude-skills/` 下的任何源文件

## 文件结构

```
docs/awesome-claude-skills/
├── README.md                          # 本文件
├── overview.md                        # 总览索引
├── batch-log.md                       # 批次执行进度
├── composio-skills.md                 # composio-skills 聚合分析
├── artifacts-builder.md               # 单个 skill 深入分析
├── brand-guidelines.md
├── canvas-design.md
├── changelog-generator.md
├── competitive-ads-extractor.md
├── connect.md
├── connect-apps.md
├── connect-apps-plugin.md
├── content-research-writer.md
├── developer-growth-analysis.md
├── document-skills.md
├── domain-name-brainstormer.md
├── file-organizer.md
├── image-enhancer.md
├── internal-comms.md
├── invoice-organizer.md
├── langsmith-fetch.md
├── lead-research-assistant.md
├── mcp-builder.md
├── meeting-insights-analyzer.md
├── raffle-winner-picker.md
├── skill-creator.md
├── skill-share.md
├── slack-gif-creator.md
├── tailored-resume-generator.md
├── template-skill.md
├── theme-factory.md
├── twitter-algorithm-optimizer.md
├── video-downloader.md
└── webapp-testing.md
```

## 如何使用

- 快速了解全貌 → 阅读 `overview.md`
- 深入了解某个 skill → 打开对应名称的 `.md` 文件
- 浏览器阅读 → 打开对应名称的 `.html` 文件

## 分类体系

沿用 awesome-claude-skills 官方 README 中的分类：

- Document Processing（文档处理）
- Development & Code Tools（开发与代码工具）
- Data & Analysis（数据分析）
- Business & Marketing（商业与营销）
- Communication & Writing（沟通与写作）
- Creative & Media（创意与媒体）
- Productivity & Organization（生产力与组织）
- Collaboration & Project Management（协作与项目管理）
- Security & Systems（安全与系统）
- App Automation via Composio（Composio 应用自动化）
