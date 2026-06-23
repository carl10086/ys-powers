# subagent-driven-development

**定位**：在同一会话内，通过“一个任务一个干净子 agent + 任务级审查 + 最终全分支审查”来执行实现计划。

**触发条件**：已有实现计划，任务相对独立，且在当前会话执行。

---

## 核心公式

```
Fresh implementer per task
+ task review (spec ✅ + code quality)
+ broad whole-branch review
= 高质量、快迭代
```

## 单次任务循环

1. **读取计划**，记录上下文与 Global Constraints，创建 todos。
2. **Pre-flight 扫描**：检查任务间冲突、计划自相矛盾点，一次性向用户确认。
3. **派发 implementer subagent**：使用 `implementer-prompt.md` 模板，附带 task-brief 与 report 文件路径。
4. **回答 implementer 问题**：先问清楚再开工。
5. **实现、测试、提交、自评**：implementer 完成任务后写 report。
6. **生成 review package**：用 `scripts/review-package BASE HEAD` 生成 diff 文件。
7. **派发 task reviewer subagent**：使用 `task-reviewer-prompt.md`，读取 brief + report + diff。
8. **处理发现**：Critical/Important 问题派 fix subagent；Minor 记入 ledger 留给最终审查。
9. **标记完成**，继续下一个任务。

## 模型选择

- **机械实现任务**（1–2 文件、规格清晰）：用最快/最便宜的模型。
- **集成与判断任务**：用标准模型。
- **架构/设计任务 + 最终全分支审查**：用最强模型。
- 必须显式指定模型，否则默认继承当前会话的昂贵模型。

> Turn count 往往比 token 单价更重要；多步任务上过便宜的模型可能反而更贵。

## Implementer 返回状态

| 状态 | 含义 | 处理 |
|---|---|---|
| `DONE` | 完成 | 生成 review package，进入审查 |
| `DONE_WITH_CONCERNS` | 完成但有疑虑 | 先读疑虑，判断是否需要处理再审查 |
| `NEEDS_CONTEXT` | 缺少信息 | 补充后重新派发 |
| `BLOCKED` | 无法完成 | 补充上下文 / 换更强模型 / 拆任务 / 升级到人 |

## 文件交接

所有子 agent 的输入输出尽量走文件，避免把大段文本贴进 controller 上下文：

- `scripts/task-brief PLAN_FILE N` → 生成任务 brief。
- implementer 把完整 report 写入约定文件。
- `scripts/review-package BASE HEAD` → 生成 reviewer 用的 diff package。

## 持久化进度

用 `.superpowers/sdd/progress.md` 记录每个任务的完成状态与 commit 范围。对话 compact 后，ledger + `git log` 是恢复进度的唯一可信来源。

## 关键红线

- 不要并行派发多个 implementer（会冲突）。
- 不要跳过 task review 或接受缺少 verdict 的报告。
- 不要帮 reviewer 预判问题严重程度（“这个算 Minor”）。
- 不要在没有 diff 文件的情况下派发 reviewer。
- 未解决的 Critical/Important 问题不能进入下一任务。
