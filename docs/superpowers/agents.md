# Superpowers 的 Agent/Subagent 设计笔记

Superpowers v6.0 把大量工作流交给专门的 subagent 执行。本文档总结其设计理念、角色分工与交接模式。

> 相关 skill 与模板：
> - `refer/superpowers/skills/subagent-driven-development/`
> - `refer/superpowers/skills/subagent-driven-development/implementer-prompt.md`
> - `refer/superpowers/skills/subagent-driven-development/task-reviewer-prompt.md`
> - `refer/superpowers/skills/requesting-code-review/code-reviewer.md`
> - `refer/superpowers/skills/writing-skills/testing-skills-with-subagents.md`

---

## 为什么用 Subagent

- **隔离上下文**：每个子 agent 只拿到完成任务所需的最小上下文，不受 controller 会话历史的污染。
- **保留 controller 上下文**：controller 专注于协调、判断、进度跟踪，把实现细节 delegate 出去。
- **专业化**：implementer、reviewer、fixer 各自有专门 prompt 和成功标准。

---

## 角色分工

| 角色 | 职责 | 常用模板 |
|---|---|---|
| **Controller** | 读计划、拆任务、选模型、派发子 agent、处理阻塞、维护 ledger | — |
| **Implementer** | 实现一个任务：写测试、实现、验证、提交、自评 | `implementer-prompt.md` |
| **Task Reviewer** | 审查单个任务：spec 合规 + 代码质量 | `task-reviewer-prompt.md` |
| **Final Reviewer** | 全分支审查，判断能否合并 | `code-reviewer.md` |
| **Fixer** | 根据 reviewer 发现修复问题，重新跑测试 | 复用 implementer 模式 |

---

## 一个任务一个 Agent

- 每个任务派发一个干净的 implementer。
- **不要并行派发多个 implementer**，避免文件冲突。
- 一个任务完成后，审查通过再进入下一任务。

## 通过文件交接，而非粘贴历史

所有输入输出尽量写成文件，避免把大段文本塞进 controller 上下文：

| 文件 | 作用 |
|---|---|
| `task-brief` | 从 plan 提取的单个任务完整需求 |
| `report` | implementer 的详细报告（实现、测试、TDD 证据、担忧） |
| `review-package` | 含 commit 列表、stat、完整 diff 的审查包 |
| `progress ledger` | `.superpowers/sdd/progress.md`，跨 compaction 的进度地图 |

## 模型选择策略

- **cheapest/fast**：1–2 文件、spec 含完整代码的机械转录。
- **standard**：多文件集成、需要判断。
- **most capable**：架构设计、最终全分支审查。

必须显式指定模型；省略则继承 controller 的昂贵默认模型。

## 状态协议

Implementer 返回四种状态之一：

- `DONE`
- `DONE_WITH_CONCERNS`
- `NEEDS_CONTEXT`
- `BLOCKED`

Controller 必须按状态处理，不能忽略升级。

## 审查循环

```
Implement → Review → Fix → Re-review → Approved
```

- Task reviewer 给出两个 verdict：spec 合规 + 代码质量。
- Critical/Important 发现必须派 fixer；Minor 可记入 ledger 等最终审查。
- 不要替 reviewer 预判问题严重性。

## 持久化进度

会话 compact 后 controller 可能丢失位置。Superpowers 用 `.superpowers/sdd/progress.md` 记录每个任务的 base..head 与审查结果。恢复时优先信任 ledger + `git log`。

## 对抗合理化的测试

`writing-skills` 把 subagent 当作测试工具：用压力场景观察 agent 如何找借口绕过规则，再把 counter 写进 skill。压力场景通常叠加 3+ 种压力（时间、沉没成本、权威、疲惫、经济、社交），并强制 A/B/C 选择。

## 对 ys-powers 的启示

- 在 `skills/` 下设计需要 agent 严格执行的流程时，可用“压力场景 + subagent”验证其有效性。
- 文件交接模式（task-brief / report / review-package）可借鉴到任何多 agent 工作流，减少 controller 上下文消耗。
- 显式模型选择与状态协议能让多 agent 执行更可控、更省成本。
