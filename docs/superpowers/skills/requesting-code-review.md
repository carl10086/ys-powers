# requesting-code-review

**定位**：在问题扩散前，派一个专门的 reviewer subagent 检查实现是否符合要求。

**触发条件**：完成任务、实现重大特性、合并到 main 之前。

---

## 为什么需要

- 发现问题的最佳时机是在它进入下游工作之前。
- Reviewer 只看工作产物，不看 controller 的会话历史，保持专注。
- Controller 保留上下文继续工作。

## 何时必须 review

- Subagent-Driven Development 的每个任务之后。
- 完成重大特性后。
- 合并到 main 之前。

## 如何请求

1. 获取 git 范围：`BASE_SHA` 与 `HEAD_SHA`。
2. 使用 `code-reviewer.md` 模板派发 `general-purpose` subagent。
3. 填入描述、计划/需求、git 范围。
4. 根据反馈行动。

## 反馈处理

- **Critical**：立即修复。
- **Important**：继续前先修复。
- **Minor**：记下来，后续处理。
- 如果 reviewer 错了，用技术理由 push back。

## 集成场景

- **SDD**：每任务后 review。
- **Executing Plans**：每任务或自然检查点 review。
- **Ad-Hoc**：合并前 review，卡住时 review。

详见模板：`refer/superpowers/skills/requesting-code-review/code-reviewer.md`。
