# Superpowers v6.0 概览

本文档是 `refer/superpowers/`（v6.0）的中文总览。Superpowers 是一套完整的软件开发方法论，通过一组可组合的 skill 在正确时机自动触发，引导 agent 完成从“澄清意图”到“分支收尾”的全流程。

> `refer/` 下文件**只读**。要借鉴某个 skill，请在主项目 `skills/` 或 `commands/` 下重写，而不是直接搬运。

---

## 核心主张

- **先设计，后代码**：任何创造性工作（新功能、组件、行为变更）都必须先出设计/spec，并经用户批准。
- **真正的红/绿 TDD**：每个实现任务先写失败测试，再写最小实现，最后重构。
- **YAGNI / DRY**：设计、计划、实现中持续剔除不需要的东西，避免重复。
- **Subagent-Driven Development**：把计划拆成独立任务，每个任务派一个干净的子 agent 实现 + 审查，控制器保留协调上下文。
- **验证先于断言**：在声称“完成/通过/修复”之前，必须出示刚跑过的命令输出。

---

## 标准工作流

| 阶段 | 触发 Skill | 产出 | 下一步 |
|---|---|---|---|
| 启动/自检 | `using-superpowers` | 识别并激活适用的 skill | 视任务而定 |
| 工作区隔离 | `using-git-worktrees` | 干净的独立工作区 | `brainstorming` / `writing-plans` / `executing-plans` |
| 意图澄清 | `brainstorming` | 经批准的 design spec | `writing-plans` |
| 计划制定 | `writing-plans` | 可执行的 implementation plan | `subagent-driven-development` 或 `executing-plans` |
| 任务实现 | `subagent-driven-development` / `executing-plans` | 逐个完成并验证的任务 | `requesting-code-review`（最终审查） |
| 分支收尾 | `finishing-a-development-branch` | 合并/PR/清理 | — |

贯穿始终的横向 skill：

- `using-superpowers`：任何行动前先调用相关 skill。
- `test-driven-development`：写代码前先写失败测试。
- `systematic-debugging`：修 bug 前先找根因。
- `verification-before-completion`：任何“完成”声明前必须验证。
- `requesting-code-review` / `receiving-code-review`：主动请求审查、理性接受反馈。
- `writing-skills`：当需要创建或修改 skill 本身时，用 TDD 方式写 skill。

---

## Skill 清单（13 个）

| Skill | 一句话定位 | 典型触发 |
|---|---|---|
| `using-superpowers` | 会话启动器：行动前必须先调用相关 skill | 任何对话/任务开始时 |
| `using-git-worktrees` | 确保功能工作发生在隔离工作区 | 开始新功能、执行 plan 前 |
| `brainstorming` | 把模糊想法聊成经批准的设计/spec | 任何创造性工作之前 |
| `writing-plans` | 把 spec 拆成极细粒度、可执行的计划 | 有 spec 的多步任务，动手前 |
| `executing-plans` | 在独立会话中按检查点执行计划 | 有 plan，无 subagent 或需另开会话 |
| `subagent-driven-development` | 同会话内用子 agent 逐任务实现计划 | 任务相对独立、在当前会话执行 |
| `finishing-a-development-branch` | 实现完成后提供结构化合并/PR/清理选项 | 测试通过、需要集成 |
| `requesting-code-review` | 派 reviewer subagent 在问题扩散前发现它 | 完成任务、重大特性、合并前 |
| `receiving-code-review` | 技术化、可验证地处理代码审查反馈 | 收到 review 反馈后 |
| `test-driven-development` | 先写失败测试，再最小实现，再重构 | 写任何功能/修复/行为变更前 |
| `systematic-debugging` | 找到根因再修复，而不是随机 patch | 任何 bug、测试失败、意外行为 |
| `writing-skills` | 用 TDD 方法创作和验证 agent skill | 新建/修改 skill，部署前 |
| `verification-before-completion` | claims 之前必须有新鲜验证证据 | 任何完成/通过/修复声明前 |

---

## 与 ys-powers 的关系

`refer/superpowers/` 是 ys-powers 的参考来源之一，重点借鉴：

- `using-superpowers` 的“启动即强制调用 skill”的 bootstrap 思想。
- 严格的“设计 → 计划 → 子 agent 实现 → 审查 → 收尾”流水线。
- 用 subagent 隔离任务上下文、通过文件交接（task-brief / report / review-package）降低上下文消耗。
- 把 TDD 思想扩展到 skill 创作（`writing-skills`）。
- “验证先于断言”的文化（`verification-before-completion`）。
- “先找根因再修复”的调试纪律（`systematic-debugging`）。

`skills/` 下已有的 `interview-me`、`spec`、`plan`、`build`、`review`、`ship` 等已覆盖部分类似能力；是否需要进一步对齐 superpowers 的细粒度流程，可逐 skill 评估。

---

## 本文档结构

```
docs/superpowers/
├── overview.md          # 本文件：总览与流程地图
├── agents.md            # agent/subagent 设计笔记
└── skills/
    ├── using-superpowers.md
    ├── using-git-worktrees.md
    ├── brainstorming.md
    ├── writing-plans.md
    ├── executing-plans.md
    ├── subagent-driven-development.md
    ├── finishing-a-development-branch.md
    ├── requesting-code-review.md
    ├── receiving-code-review.md
    ├── test-driven-development.md
    ├── systematic-debugging.md
    ├── writing-skills.md
    └── verification-before-completion.md
```

详细内容请回到 `refer/superpowers/skills/<name>/SKILL.md`。
