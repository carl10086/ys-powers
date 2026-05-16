# mcp-builder

## 定位

指导开发者创建高质量的 MCP（Model Context Protocol）Server，使 LLM 能够通过精心设计的工具与外部服务和 API 交互。支持 Python（FastMCP）和 Node/TypeScript（MCP SDK）两种技术栈。

## 触发时机

- 需要将外部 API 封装为 MCP Server 供 LLM 调用时
- 希望让 Claude 能够操作某个内部系统或第三方服务时
- 正在评估或改进现有 MCP Server 的设计质量时
- **不适用**：仅需简单的单次 API 调用（直接使用 HTTP 客户端即可）

## 核心能力

1. **Agent -centric 设计**：不是简单包装 API endpoint，而是构建面向工作流的高影响力工具
2. **上下文优化**：针对 LLM 有限的上下文窗口，返回高信号信息而非 exhaustive 数据转储
3. **可操作的错误消息**：错误信息应指导 Agent 走向正确使用模式，而非仅诊断问题
4. **自然任务细分**：工具命名和分组反映人类的任务思考方式
5. **评估驱动开发**：早期创建真实评估场景，基于 Agent 反馈迭代改进

## 开发四阶段

### Phase 1: 深度研究与规划

1. 理解 Agent-centric 设计原则
2. 研读 MCP 协议文档（`modelcontextprotocol.io/llms-full.txt`）
3. 研读对应语言的 SDK 文档（Python / TypeScript）
4. 彻底研究目标服务的 API 文档（端点、认证、限流、错误码）
5. 制定实现计划：工具选择、共享工具、输入/输出设计、错误处理策略

### Phase 2: 实现

- 搭建项目结构
- 实现认证和连接管理
- 开发核心工具集
- 设计响应格式和分页策略
- 实现错误处理和重试逻辑

### Phase 3: 测试与评估

- 创建真实使用场景的测试用例
- 验证 Agent 能否使用工具完成端到端任务
- 根据测试结果优化工具设计

### Phase 4: 文档与发布

- 编写工具使用说明
- 提供示例对话和预期输出
- 发布到 MCP Server 注册表或内部仓库

## 设计原则

| 原则 | 说明 |
|------|------|
| **面向工作流** | 合并相关操作（如 `schedule_event` 同时检查可用性和创建事件） |
| **上下文预算** | 提供 "concise" vs "detailed" 响应格式，默认使用人类可读标识符而非技术 ID |
| **教育性错误** | 错误消息中建议具体下一步："Try using filter='active_only' to reduce results" |
| **一致前缀** | 相关工具使用一致前缀以便 Agent 发现（如 `calendar_*`） |

## 与 ys-powers 的关联

- **与 composio-skills / connect 的关系**：`composio-skills` 和 `connect` 是「使用」MCP 的 skill，`mcp-builder` 是「构建」MCP 的 skill。两者互补：前者让消费者受益，后者让开发者受益
- **借鉴价值**：其「Agent-centric 设计」和「评估驱动开发」理念是构建高质量 AI 工具的核心方法论，可直接纳入 ys-powers 的任何工具开发流程
- **搬运建议**：高价值。MCP 是 Anthropic 力推的开放标准，ys-powers 若计划扩展与外部系统的集成能力，`mcp-builder` 是不可或缺的基础 skill

## 元信息

- 来源：`refer/awesome-claude-skills/mcp-builder/SKILL.md`
- 维护者：Composio / 社区
- 许可证：Apache 2.0（详见 `LICENSE.txt`）
