# langsmith-fetch

## 定位

通过从 LangSmith Studio 获取 LangChain / LangGraph Agent 的执行轨迹（trace），帮助开发者调试 Agent 行为、分析工具调用、检查记忆操作和审查性能指标。

## 触发时机

- Agent 行为异常，需要查看最近执行记录时
- 调查工具调用失败或返回错误时
- 分析 Agent 的记忆（LTM）操作是否正常时
- 检查 Token 使用情况和执行性能时
- 需要向 LangSmith 获取特定 Trace ID 的详细信息时
- **不适用**：未使用 LangChain / LangGraph 构建 Agent，或未配置 LangSmith 监控时

## 核心能力

1. **快速调试**：获取最近 N 分钟内的 traces，快速定位失败点
2. **深度分析**：针对特定 trace ID 获取完整执行流程和 JSON 详情
3. **错误定位**：识别工具调用失败、连接超时、节点执行异常等问题
4. **性能监控**：查看执行时长、Token 消耗等关键指标
5. **工具调用审计**：追踪 Agent 调用了哪些工具、调用顺序和返回结果

## 指令流程概览

### 快速调试（最近活动）

```bash
langsmith-fetch traces --last-n-minutes 5 --limit 5 --format pretty
```

分析并报告：
- 发现 traces 数量
- 错误/失败项
- 调用的工具列表
- 执行时长
- Token 使用量

### 深度调查（特定 Trace）

```bash
langsmith-fetch trace <trace-id> --format json
```

分析 JSON 并输出：
- Agent 目标
- 工具调用顺序和结果
- 失败点和错误信息
- 根因分析
- 修复建议

## 安装要求

```bash
pip install langsmith-fetch
export LANGSMITH_API_KEY="your_key"
export LANGSMITH_PROJECT="your_project"
```

## 与 ys-powers 的关联

- **与 developer-growth-analysis 的关系**：两者都分析「历史行为」，但 `langsmith-fetch` 聚焦 Agent 执行层，`developer-growth-analysis` 聚焦开发者个人成长
- **借鉴价值**：其「最近活动快速扫描 → 特定 Trace 深度钻取」的两级调试模式是通用的可观测性（observability）最佳实践，可复用到任何需要排查复杂执行流程的场景
- **搬运建议**：高价值。若 ys-powers 的使用者使用 LangChain / LangGraph 构建 Agent，这是必备的调试工具。可作为「Agent 可观测性」skill 的一部分搬运

## 元信息

- 来源：`refer/awesome-claude-skills/langsmith-fetch/SKILL.md`
- 维护者：Composio / 社区（@OthmanAdi）
- 许可证：Apache 2.0
