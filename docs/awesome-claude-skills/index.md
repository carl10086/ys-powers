# awesome-claude-skills 本地 Skill 总览

本索引覆盖 `refer/awesome-claude-skills/` 下所有本地存在的 skill 目录（约 30 个）。每个 skill 提供一句话定位、触发时机和对应深入分析文件的链接。

---

## Document Processing（文档处理）

| Skill | 定位 | 触发时机 | 深入分析 |
|-------|------|----------|----------|
| [document-skills](document-skills.html) | 处理 Word、PDF、PPT、Excel 等办公文档 | 需要创建、编辑或分析结构化文档时 | [查看](document-skills.html) |

## Development & Code Tools（开发与代码工具）

| Skill | 定位 | 触发时机 | 深入分析 |
|-------|------|----------|----------|
| [artifacts-builder](artifacts-builder.html) | 使用 React + Tailwind + shadcn/ui 构建复杂的 Claude.ai HTML Artifacts | 需要多组件、状态管理或路由的交互式 artifact | [查看](artifacts-builder.html) |
| [changelog-generator](changelog-generator.html) | 将 Git 提交历史转换为用户友好的发布日志 | 准备发版、写 release notes、产品更新摘要时 | [查看](changelog-generator.html) |
| [connect](connect.html) | 将 Claude 连接到任意 App，执行真实操作（邮件、Issue、Slack 等） | 需要 Claude 与 Gmail、GitHub、Notion 等 1000+ 服务交互时 | [查看](connect.html) |
| [connect-apps](connect-apps.html) | Connect 的 Apps 端扩展 | 需要管理或配置已连接的 App 列表时 | [查看](connect-apps.html) |
| [connect-apps-plugin](connect-apps-plugin.html) | Claude Code 插件形式的 Connect Apps | 在 Claude Code CLI 中使用 Connect 能力时 | [查看](connect-apps-plugin.html) |
| [developer-growth-analysis](developer-growth-analysis.html) | 分析开发者成长指标与趋势 | 评估团队开发者效率、技能成长或招聘质量时 | [查看](developer-growth-analysis.html) |
| [langsmith-fetch](langsmith-fetch.html) | 从 LangSmith 获取并分析 Agent 执行轨迹 | 调试 LangChain / LangGraph Agent 的行为时 | [查看](langsmith-fetch.html) |
| [mcp-builder](mcp-builder.html) | 指导创建高质量的 MCP Server | 需要将外部 API 封装为 MCP Server 供 LLM 调用时 | [查看](mcp-builder.html) |
| [skill-creator](skill-creator.html) | 指导创建有效的 Claude Skill | 需要为特定工作流编写自定义 skill 时 | [查看](skill-creator.html) |
| [skill-share](skill-share.html) | Skill 的分享与分发机制 | 需要将自定义 skill 发布或共享给他人时 | [查看](skill-share.html) |
| [template-skill](template-skill.html) | Skill 开发的标准模板 | 从零开始创建新 skill 需要参考结构时 | [查看](template-skill.html) |
| [webapp-testing](webapp-testing.html) | 使用 Playwright 测试本地 Web 应用 | 需要验证前端功能、调试 UI 或截图对比时 | [查看](webapp-testing.html) |

## Data & Analysis（数据分析）

> 本地暂无纯数据分析类 skill。相关能力分散在 `developer-growth-analysis` 和 `langsmith-fetch` 中。

## Business & Marketing（商业与营销）

| Skill | 定位 | 触发时机 | 深入分析 |
|-------|------|----------|----------|
| [brand-guidelines](brand-guidelines.html) | 将 Anthropic 品牌色与字体应用到 Artifacts | 需要保持品牌一致性、使用官方视觉标准时 | [查看](brand-guidelines.html) |
| [competitive-ads-extractor](competitive-ads-extractor.html) | 从广告库提取并分析竞品广告 | 研究竞品广告策略、寻找创意灵感时 | [查看](competitive-ads-extractor.html) |
| [domain-name-brainstormer](domain-name-brainstormer.html) | 生成创意域名并检查多 TLD 可用性 | 为新产品或项目寻找可用域名时 | [查看](domain-name-brainstormer.html) |
| [lead-research-assistant](lead-research-assistant.html) | 识别并筛选高质量销售线索 | 需要为产品寻找目标客户并制定外联策略时 | [查看](lead-research-assistant.html) |

## Communication & Writing（沟通与写作）

| Skill | 定位 | 触发时机 | 深入分析 |
|-------|------|----------|----------|
| [content-research-writer](content-research-writer.html) | 协助撰写高质量内容，自动调研并添加引用 | 需要写长文、博客或报告，且要求有据可查时 | [查看](content-research-writer.html) |
| [internal-comms](internal-comms.html) | 撰写公司内部沟通文档（更新、FAQ、报告） | 需要写 3P 更新、公司简报或项目状态时 | [查看](internal-comms.html) |
| [meeting-insights-analyzer](meeting-insights-analyzer.html) | 分析会议转录，提取行为模式与洞察 | 需要评估会议效率、团队沟通风格时 | [查看](meeting-insights-analyzer.html) |

## Creative & Media（创意与媒体）

| Skill | 定位 | 触发时机 | 深入分析 |
|-------|------|----------|----------|
| [canvas-design](canvas-design.html) | 使用设计哲学创建视觉艺术作品（PNG / PDF） | 需要生成海报、视觉设计或其他静态艺术品时 | [查看](canvas-design.html) |
| [image-enhancer](image-enhancer.html) | 提升图像分辨率、清晰度与专业感 | 需要优化截图或图片用于演示和文档时 | [查看](image-enhancer.html) |
| [slack-gif-creator](slack-gif-creator.html) | 创建符合 Slack 尺寸限制的动画 GIF | 需要为 Slack 制作表情包或演示动画时 | [查看](slack-gif-creator.html) |
| [theme-factory](theme-factory.html) | 为文档、幻灯片和网页应用专业字体与配色主题 | 需要统一多份文档的视觉风格时 | [查看](theme-factory.html) |
| [twitter-algorithm-optimizer](twitter-algorithm-optimizer.html) | 基于 Twitter 开源算法优化推文曝光 | 需要提升推文传播力和互动率时 | [查看](twitter-algorithm-optimizer.html) |
| [video-downloader](video-downloader.html) | 从 YouTube 等平台下载视频用于离线查看 | 需要离线观看、编辑或存档视频时 | [查看](video-downloader.html) |

## Productivity & Organization（生产力与组织）

| Skill | 定位 | 触发时机 | 深入分析 |
|-------|------|----------|----------|
| [file-organizer](file-organizer.html) | 智能整理文件与文件夹，查找重复项 | 桌面或项目目录混乱需要重组时 | [查看](file-organizer.html) |
| [invoice-organizer](invoice-organizer.html) | 自动提取发票信息并按规则重命名归档 | 准备税务申报或整理财务凭证时 | [查看](invoice-organizer.html) |
| [raffle-winner-picker](raffle-winner-picker.html) | 从列表中随机抽取获奖者 | 举办抽奖、赠品分配或随机抽选时 | [查看](raffle-winner-picker.html) |
| [tailored-resume-generator](tailored-resume-generator.html) | 针对职位描述生成定制简历 | 投递简历前需要针对性优化时 | [查看](tailored-resume-generator.html) |

## Collaboration & Project Management（协作与项目管理）

> 本地暂无纯项目管理类 skill。`internal-comms` 和 `meeting-insights-analyzer` 部分覆盖协作场景。

## Security & Systems（安全与系统）

> 本地暂无纯安全类 skill。

## App Automation via Composio（Composio 应用自动化）

| Skill | 定位 | 触发时机 | 深入分析 |
|-------|------|----------|----------|
| [composio-skills](composio-skills.html) | 通过 Rube MCP 自动化 800+ SaaS App（Salesforce、Slack、Jira 等） | 需要将 Claude 与外部业务系统（CRM、项目管理、邮件等）集成时 | [查看](composio-skills.html) |

---

## 统计

| 指标 | 数值 |
|------|------|
| 本地 skill 目录总数 | ~30 个 |
| 独立分析文件 | 30 个（每个 skill 一个） |
| composio-skills 子 skill 数 | 800+（聚合为一个文件） |
| 覆盖分类 | 10 个大类 |

## 使用建议

1. **不知道用哪个** → 先按分类浏览本页，定位到相关领域后再点击深入分析
2. **想搬运到 ys-powers** → 查看每个 skill 分析文件中的「与 ys-powers 的关联」章节
3. **发现缺失** → 本索引仅覆盖本地目录，完整 1000+ skills 列表见 `refer/awesome-claude-skills/README.md`
