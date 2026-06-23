# executing-plans

**定位**：在独立会话中执行已有实现计划，带审查检查点。

**触发条件**：有书面 implementation plan，且需要在另一个会话（或没有 subagent 支持的平台）中执行。

---

## 核心流程

1. **加载并审查计划**
   - 读取 plan 文件。
   - 批判性地审查：识别问题、疑虑、缺失。
   - 如有疑虑，先向用户提出，再开始执行。

2. **执行任务**
   - 每个任务标记 `in_progress` → 按步骤执行 → 跑验证 → 标记 `completed`。
   - 严格按 plan 的 bite-sized 步骤执行，不跳过验证。

3. **完成开发**
   - 所有任务完成并验证后，调用 `superpowers:finishing-a-development-branch`。

## 何时停下来求助

- 遇到阻塞（缺失依赖、测试失败、指令不清）。
- 计划有关键缺口无法开始。
- 不理解某条指令。
- 验证反复失败。

## 与 subagent-driven-development 的关系

- 如果有 subagent 支持，优先用 `subagent-driven-development`；质量更高。
- 没有 subagent 支持时，用本 skill 在当前会话内顺序执行。

## 集成依赖

- `using-git-worktrees`：确保有隔离工作区。
- `writing-plans`：生成本 skill 执行的计划。
- `finishing-a-development-branch`：最后收尾。
