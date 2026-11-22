# Matt-based ys-powers 重写方案

## Outcome

在 `experiment/matt-powers` 分支中，把当前 ys-powers 重写为以 Matt Pocock skills 为基础的完整能力包，使用更小、更清晰的默认工程内核。

## User

项目维护者本人，使用真实代码任务长期验证和定制这套能力。

## Why now

当前 ys-powers 的 commands、agents、skills 和 references 与 Matt 的工作流存在重复。目标不是比较两套长期并存，而是以 Matt 的原始分包和调用逻辑为基础，删除旧实现，减少内核。

## Baseline

完整保留 Matt 原始分包：

```text
skills/engineering
skills/productivity
skills/misc
skills/in-progress
```

保留 Matt 的目录结构、frontmatter、调用策略和 `agents/openai.yaml`。`engineering/` 与 `productivity/` 是默认稳定能力；`misc/` 是低频工具；`in-progress/` 是 beta 能力。

保留 ys-powers 自有的：

```text
skills/eli
rules/code.md
```

## Success

使用真实的中等规模代码任务验证完整链路：

- 业务和技术讨论；
- domain model；
- spec；
- 2–4 个 ticket；
- implement 或 implement-spec；
- tdd；
- code review；
- retro。

观察：

- 是否更快进入有效实现；
- 是否减少返工和重复解释；
- ticket 和 blocking 是否让下一步更清晰；
- session 中断后是否容易恢复；
- 测试和 review 是否真正改善交付；
- 使用者是否愿意继续使用这套流程。

## Constraints

- 实验分支长期独立，不进入 `master`。
- Matt 的 Prompt 和 Skill 逻辑尽量保持原样。
- 不针对 OMP 或 Claude 做额外流程分叉。
- 只做必要的本地化：`.scratch/` → `.ys-powers/`、安装 manifest、同步记录和中文解释文档。
- `.ys-powers/` 作为 Git 中持久化的 local tracker 状态。
- `refer/mattpocock-skills/` 作为只读上游参考，不直接修改。
- 定期同步 Matt 上游，并记录本地必要差异。

## Migration boundary

删除旧 ys-powers runtime 能力：

```text
commands/
agents/
旧 skills/（skills/eli 除外）
references/
旧 hooks/
```

保留并重写：

```text
install/
Makefile
README.md
```

`rules/` 不删除，作为项目级编码规则 overlay。

## Out of scope

- 修改 `refer/mattpocock-skills/`；
- 把 Matt skills 平铺或重新命名；
- 自行重新实现 Matt 的核心工作流；
- 现在清理全局 `~/.claude/`；
- 在没有本地真实任务验证前宣称 Matt 一定更优。

## Next validation

先完成源目录和安装边界，再通过 local install 生成当前项目的 `.claude/`，验证完整 Matt 分包及 `eli` 的实际可用性。
