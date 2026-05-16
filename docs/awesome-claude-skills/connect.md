# connect

## 定位

通过 Composio 将 Claude 连接到 1000+ 外部应用（Gmail、Slack、GitHub、Notion 等），让 Claude 从「生成文字建议」升级为「执行真实操作」。

## 触发时机

- 需要 Claude 实际发送邮件、创建 Issue、发布消息时
- 需要更新数据库、添加日历事件、管理 CRM 记录时
- 需要跨多个应用串联操作（如「从 GitHub 提取 bug 列表，总结后发 Slack」）时
- **不适用**：仅需文字建议、无需实际执行的场景

## 核心能力

1. **1000+ 应用集成**：覆盖邮件（Gmail、Outlook）、聊天（Slack、Discord、Teams）、开发（GitHub、GitLab、Jira）、文档（Notion、Google Docs）、数据（Sheets、Airtable、PostgreSQL）、CRM（HubSpot、Salesforce）等
2. **自然语言驱动**：用日常语言描述需求，Claude 自动路由到正确工具
3. **自动 OAuth 处理**：首次使用某应用时自动引导授权，无需手动配置
4. **链式操作**：支持跨应用工作流，一步完成多系统协作

## 指令流程概览

1. 用户用自然语言描述要执行的操作（如 "Send email to sarah@acme.com about the launch"）
2. Composio Tool Router 从 1000+ 工具中匹配最合适的工具
3. 如首次使用，自动触发 OAuth 授权流程
4. 执行操作并返回结果给用户

## 安装配置

```bash
# 获取免费 API Key: platform.composio.dev
export COMPOSIO_API_KEY="your-key"

# Python
pip install composio

# TypeScript
npm install @composio/core
```

## 与 ys-powers 的关联

- **与 composio-skills 的关系**：`connect` 是 Composio 的「通用连接层」，而 `composio-skills` 是「按应用细分的自动化 skill」。两者互补：connect 提供「一句话执行任意操作」的通用能力，composio-skills 提供「按应用最佳实践编排」的结构化能力
- **借鉴价值**：其「自然语言 → 工具路由 → 自动执行」的交互模式是 Agent 与外部系统集成的标杆设计
- **搬运建议**：高价值。若 ys-powers 的使用者需要频繁与外部 SaaS 交互，可搬运或参考实现类似的「通用连接层」skill

## 元信息

- 来源：`refer/awesome-claude-skills/connect/SKILL.md`
- 维护者：Composio
- 许可证：Apache 2.0
