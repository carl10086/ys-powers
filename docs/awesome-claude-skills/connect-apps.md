# connect-apps

## 定位

通过 Claude Code 插件形式将 Claude 连接到 1000+ 应用，实现邮件发送、Issue 创建、消息发布等真实操作。与 `connect` 功能相同，但安装方式为插件化。

## 触发时机

- 在 Claude Code CLI 环境中需要与外部应用交互时
- 已通过 `/plugin install composio-toolrouter` 安装插件后
- 需要执行「发送邮件、创建 GitHub Issue、发 Slack 消息」等具体操作时
- **不适用**：Claude.ai Web 界面或未安装插件的 Claude Code 环境

## 核心能力

1. **插件化安装**：通过 `/plugin install composio-toolrouter` 一键安装，约 60 秒完成配置
2. **1000+ 应用覆盖**：与 `connect` 相同的应用生态（邮件、聊天、开发、文档、数据、CRM 等）
3. **自然语言操作**：用日常语言描述需求即可执行，无需记忆具体命令
4. **首次 OAuth 授权**：首次使用某应用时通过链接授权，一次授权长期有效

## 指令流程概览

1. **安装插件**：`claude --plugin-dir ./connect-apps-plugin`（或通过 `/plugin install`）
2. **运行配置**：`/composio-toolrouter:setup`，输入从 platform.composio.dev 获取的免费 API Key
3. **重启 Claude Code**：使插件生效
4. **执行操作**：用自然语言描述要执行的任务

## 使用示例

```
Send email to sarah@acme.com about the launch
Create GitHub issue: fix login bug
Post to Slack #general: deploy complete
```

## 故障排查

| 问题 | 解决方式 |
|------|----------|
| Plugin not found | 确认已运行 `/plugin install composio-toolrouter` |
| Need to authorize | 点击 Claude 提供的 OAuth 链接，完成后回复 "done" |
| Action failed | 检查在目标应用中是否有足够权限 |

## 与 ys-powers 的关联

- **与 connect 的关系**：`connect-apps` 和 `connect` 是同一能力的两种安装形态。`connect` 面向代码集成（Python/TypeScript SDK），`connect-apps` 面向 Claude Code 插件化使用
- **与 connect-apps-plugin 的关系**：`connect-apps-plugin` 是 `connect-apps` 的物理插件目录，包含实际的插件代码
- **借鉴价值**：其「插件安装 → 配置向导 → 自然语言操作」的三步用户体验设计值得借鉴
- **搬运建议**：价值中等。若 ys-powers 需要与 Composio 生态集成，直接使用 `connect` 或 `connect-apps` 即可，无需重复搬运

## 元信息

- 来源：`refer/awesome-claude-skills/connect-apps/SKILL.md`
- 维护者：Composio
- 许可证：Apache 2.0
