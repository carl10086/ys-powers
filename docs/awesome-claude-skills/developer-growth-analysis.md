# developer-growth-analysis

## 定位

通过分析用户近期的 Claude Code 聊天历史，识别编码模式、技术短板和成长方向，并自动从 HackerNews 筛选相关学习资源，生成个性化成长报告。

## 触发时机

- 希望了解自己近期的开发习惯和模式时
- 想识别具体的技术短板或反复遇到的挑战时
- 需要针对性的学习资源推荐（基于实际工作而非泛泛而谈）时
- 希望跟踪自己在多个项目中的进步情况时
- **不适用**：首次使用 Claude Code、无足够聊天记录（< 24 小时）时

## 核心能力

1. **聊天记录读取**：访问 `~/.claude/history.jsonl`，提取过去 24-48 小时的对话记录
2. **开发模式识别**：分析项目类型、技术栈、问题类别、解决思路
3. **改进点检测**：基于实际对话内容识别 3-5 个具体改进方向
4. **个性化报告**：生成包含工作摘要、改进领域、行动建议的结构化报告
5. **资源策展**：从 HackerNews 搜索与改进领域相关的高质量文章和讨论
6. **Slack 推送**：自动将完整报告发送到用户的 Slack 私信

## 指令流程概览

1. **读取历史**：解析 `~/.claude/history.jsonl`，按时间戳过滤最近 1-2 天的记录
2. **模式分析**：
   - 项目与领域（后端、前端、DevOps、数据等）
   - 使用的技术栈（语言、框架、工具）
   - 问题类型（性能优化、调试、功能实现、重构等）
   - 遇到的挑战（重复提问、多轮尝试才解决的知识盲区）
3. **改进点识别**：基于证据提出 3-5 个具体、可执行的改进方向
4. **生成报告**：包含工作概述、改进领域、具体建议、学习资源、行动项
5. **推送报告**：通过 Slack API 发送到用户私信

## 报告示例结构

```markdown
# Developer Growth Report

## Overview
- Projects worked on: [list]
- Technologies used: [list]
- Primary focus areas: [list]

## Improvement Areas
1. Advanced TypeScript patterns — struggled with type safety in [project]
2. Error handling and validation — patched several null-check bugs
3. Async/await patterns — race conditions and timing issues observed

## Learning Resources
- [HackerNews article 1] — directly addresses TypeScript generics
- [HackerNews article 2] — defensive programming patterns

## Action Items
- [ ] Review TypeScript utility types documentation
- [ ] Add input validation to [specific module]
```

## 与 ys-powers 的关联

- **与 ys-powers 现有能力的关系**：ys-powers 中无类似的「个人成长分析」skill。`developer-growth-analysis` 创新性地将聊天记录转化为自我提升的反馈源
- **借鉴价值**：其「本地数据读取 → 模式识别 → 外部资源策展 → 报告推送」的闭环流程可复用到任何需要「基于历史行为提供洞察」的场景
- **搬运建议**：高价值。对开发者个人成长和团队 1:1 反馈都非常有用。注意需要 Slack 集成权限

## 元信息

- 来源：`refer/awesome-claude-skills/developer-growth-analysis/SKILL.md`
- 维护者：Composio / 社区
- 许可证：Apache 2.0
