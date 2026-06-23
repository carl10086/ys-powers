# writing-plans

**定位**：在有 spec 或明确需求后、动手写代码前，制定一份“零基础工程师也能执行”的实现计划。

**触发条件**：多步任务已有 spec 或需求文档，准备进入实现阶段。

---

## 核心主张

- 假设执行者对代码库、工具链、问题域都零认知，且品味一般。
- 计划本身是“任务 + 精确文件路径 + 可运行代码 + 测试命令 + 提交指令”的完整交付物。
- 每个步骤控制在 2–5 分钟，遵循 DRY、YAGNI、TDD、频繁提交。

## 计划文档固定头部

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development ...

**Goal:** ...
**Architecture:** ...
**Tech Stack:** ...

## Global Constraints
...
```

Global Constraints 必须逐字复制 spec 里的绑定要求（版本、命名、格式、组件关系）。

## 任务结构

每个任务包含：

- **Files**：创建/修改/测试的精确路径。
- **Interfaces**：消费什么、产出什么（函数签名、类型）。
- **Steps**：按 `写失败测试 → 运行确认失败 → 最小实现 → 运行确认通过 → 提交` 组织。
- 每个步骤必须给出可运行的代码或命令，以及期望输出。

## 禁止占位符

计划中不能出现：

- `TBD`、`TODO`、`implement later`
- “添加适当错误处理 / 验证 / 边缘情况处理”
- “类似 Task N”（重复写全）
- 只描述不展示代码

## 自检清单

1. **Spec coverage**：spec 里的每条要求都能指向一个任务。
2. **Placeholder scan**：检查上述禁用模式。
3. **Type consistency**：跨任务签名、命名一致。

## 执行交接

计划保存后提供两种执行方式：

1. **Subagent-Driven（推荐）**：每个任务派一个子 agent，任务间审查。
2. **Inline Execution**：当前会话批量执行，带检查点。

分别要求使用 `superpowers:subagent-driven-development` 或 `superpowers:executing-plans`。
