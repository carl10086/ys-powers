# composio-skills

## 定位

通过 Rube MCP（Composio 的 MCP 实现）将 Claude 连接到 800+ SaaS 应用，实现跨 CRM、项目管理、邮件、代码托管、社交媒体等业务系统的自动化操作。

## 触发时机

- 需要将 Claude 与外部业务系统（Salesforce、Slack、GitHub、Gmail 等）集成时
- 需要自动化执行「创建 Issue、发送邮件、更新客户记录」等具体操作时
- 已有 Composio / Rube MCP 连接，需要按最佳实践编排工具调用时
- **不适用**：无 Composio 账号、或目标应用不在 Composio 支持列表中

## 核心能力

每个子 skill 的能力本质相同，只是目标应用不同：

1. **工具发现**：通过 `RUBE_SEARCH_TOOLS` 动态查询目标应用的可用工具、输入 schema 和执行建议
2. **连接管理**：通过 `RUBE_MANAGE_CONNECTIONS` 建立和管理与目标应用的 OAuth 连接
3. **工具执行**：通过 `RUBE_MULTI_EXECUTE_TOOL` 调用具体工具完成业务操作
4. **会话复用**：在同一个工作流中复用 session ID，减少重复认证

## 通用工作流模式

所有 composio-skills 遵循同一套三段式工作流：

### Step 1: 发现工具

```
RUBE_SEARCH_TOOLS
queries: [{use_case: "your specific task", known_fields: ""}]
session: {generate_id: true}
```

返回可用工具 slug、输入 schema、推荐执行计划和已知陷阱。

### Step 2: 检查连接

```
RUBE_MANAGE_CONNECTIONS
toolkits: ["target-app-name"]
session_id: "your_session_id"
```

确认连接状态为 ACTIVE，如未激活则按返回的授权链接完成设置。

### Step 3: 执行操作

```
RUBE_MULTI_EXECUTE_TOOL
tools: [{
  tool_slug: "TOOL_SLUG_FROM_SEARCH",
  arguments: {/* schema-compliant args */}
}]
memory: {}
session_id: "your_session_id"
```

## 已知陷阱（通用）

| 陷阱 | 说明 |
|------|------|
| **必须先搜索** | 工具 schema 会变，永远不要硬编码 tool slug 或参数 |
| **检查连接状态** | 执行前确认 `RUBE_MANAGE_CONNECTIONS` 返回 ACTIVE |
| **Schema 合规** | 使用搜索返回的精确字段名和类型 |
| **Memory 参数** | `RUBE_MULTI_EXECUTE_TOOL` 必须包含 `memory`，即使为空 `{}` |
| **Session 复用** | 同一工作流复用 session ID，新工作流再生成新 ID |
| **分页处理** | 检查响应中的分页 token，继续获取直到完整 |

## 应用分类与代表性示例

832 个子 skill 按业务领域分布如下：

### CRM & 销售

| 应用 | 能力 |
|------|------|
| salesforce-* | 对象管理、记录操作、SOQL 查询、批量处理 |
| zoho-* | Leads、Contacts、Deals、Accounts、模块管理 |

### 项目管理

| 应用 | 能力 |
|------|------|
| atlassian-automation | Jira / Confluence 集成 |
| asana-automation | Tasks、Projects、Sections、Workspaces |
| notion-automation | Pages、Databases、Blocks、Comments |

### 沟通协作

| 应用 | 能力 |
|------|------|
| slackbot-automation | Messages、Channels、Search、Reactions、Threads |
| discordbot-automation | Messages、Channels、Servers、Roles |
| webex-automation | Meetings、Messages |

### 邮件营销

| 应用 | 能力 |
|------|------|
| gmail-automation | Send / Reply、Search、Labels、Drafts、Attachments |
| mailchimp-automation | Audiences、Campaigns、Templates、Segments |
| sendgrid-automation | Emails、Templates、Contacts、Lists |

### 代码 & DevOps

| 应用 | 能力 |
|------|------|
| github-automation | Issues、PRs、Repos、Branches、Actions |
| gitlab-automation | Issues、MRs、Projects、Pipelines |
| vercel-automation | Deployments、Projects、Domains、Environment Variables |
| digital-ocean-automation | Droplets、Databases、Spaces |

### 存储 & 文件

| 应用 | 能力 |
|------|------|
| googledrive-automation | Upload、Download、Search、Share、Organize |
| dropbox-sign-automation | Sign requests、Templates |

### 电子表格 & 数据库

| 应用 | 能力 |
|------|------|
| baserow-automation | Tables、Rows、Fields |
| influxdb-cloud-automation | Metrics、Queries |

### 日历 & 日程

| 应用 | 能力 |
|------|------|
| googlecalendar-automation | Events、Attendees、Recurring Schedules |
| calendarhero-automation | Event Types、Bookings、Availability |

### 社交媒体

| 应用 | 能力 |
|------|------|
| twitter-automation | Tweets、Search、Users、Lists |
| youtube-automation | Videos、Channels、Playlists、Comments |
| twitch-automation | Streams、Users、Clips |

### 电商 & 支付

| 应用 | 能力 |
|------|------|
| amazon-automation | Products、Orders、Inventory |
| stripe-automation | Charges、Customers、Products、Subscriptions |
| lemon-squeezy-automation | Products、Orders、Customers |

### 设计 & 文档

| 应用 | 能力 |
|------|------|
| documenso-automation | Documents、Signatures |
| zeplin-automation | Designs、Screens、Components |
| visme-automation | Presentations、Infographics |

### AI & 内容

| 应用 | 能力 |
|------|------|
| elevenlabs-automation | Voice synthesis、Voice cloning |
| deepgram-automation | Speech-to-text、Audio intelligence |
| apify-automation | Web scraping、Data extraction |
| anthropic-* | Anthropic API 管理 |

## 与 ys-powers 的关联

- **与 ys-powers 现有能力的关系**：ys-powers 目前无任何外部 SaaS 集成 skill。`composio-skills` 提供了现成的「连接层」能力，可直接补全这一空白
- **借鉴价值**：其「搜索 → 连接 → 执行」的三段式 MCP 调用模式是通用的工具使用最佳实践，可复用到任何 MCP Server 的调用场景中
- **搬运建议**：搬运价值有限——子 skill 数量过多（800+）且高度同质化，更合理的做法是：在 ys-powers 中创建一个通用的「Composio MCP 使用指南」skill，而非搬运每个子 skill

## 元信息

- 来源：`refer/awesome-claude-skills/composio-skills/`（800+ 子目录）
- 维护者：Composio
- 许可证：各子 skill 可能不同，以目录内文件为准
- 连接要求：需配置 Rube MCP（`https://rube.app/mcp`）
