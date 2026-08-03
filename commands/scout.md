---
description: 多渠道并行信息探索。输入查询后，自动拆解角度、分配精准渠道（Context7、OpenCLI browser、Chrome DevTools、GitHub）、并行派遣 sub-agent、汇总结果。不使用 WebSearch。
disable-model-invocation: true
---

# Scout

接收用户查询，执行多渠道并行信息探索。

## 工作流程

```
Date ──→ Decompose ──→ Assign ──→ Dispatch ──→ Synthesize
```

### 1. 获取当前日期

```bash
date "+%Y-%m-%d"
```

将年份融入搜索角度（如 "React 19 2025-2026"）。

### 2. 拆解角度

将查询拆为 2-3 个角度：

| 角度 | 渠道 |
|------|------|
| 官方文档/API | Context7 (`ctx7` CLI / `find-docs` skill) |
| 浏览器搜索/页面检查 | OpenCLI browser / Chrome DevTools MCP |
| 代码仓库/issue | GitHub (`gh` CLI) |

### 3. 派遣

并行生成最多 2 个 sub-agent，每个负责一个角度。

Sub-agent 硬性限制：
- 最多 3 次 tool 调用
- 90 秒内返回

### 4. 汇总

合并结果、交叉验证、标记缺口、注明来源。

## 渠道工具速查

```bash
# Context7
ctx7 library <name> "<query>"
ctx7 docs <libraryId> "<query>"

# OpenCLI Browser
opencli browser default open "<url>"
opencli browser default state
opencli browser default fill "<selector>" "<text>"
opencli browser default keys Enter

# Chrome DevTools MCP
mcp__chrome-devtools__navigate_page
mcp__chrome-devtools__take_snapshot
mcp__chrome-devtools__evaluate_script

# GitHub
gh search repos/issues "<query>" --sort stars
```

## 约束

- **不使用 WebSearch**
- 最多 2 个并行 agent
- 每个 agent 最多 3 次 tool 调用
- Context7 优先用于技术文档查询
