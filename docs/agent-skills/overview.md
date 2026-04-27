# agent-skills 速览

本文档是 `refer/agent-skills/` 下 21 个 skill 的中文索引。用于快速定位想借鉴的 skill；详细内容请回到 `refer/agent-skills/skills/<name>/SKILL.md`。

> 注意：`refer/` 下文件**只读**。要借鉴某个 skill，请在主项目 `skills/` 下重写，而不是直接搬运。

阶段分组沿用 agent-skills 自带 CLAUDE.md 的 "Skills by Phase"，将 `using-agent-skills` 单列为 Meta。

---

## Define（定义阶段）

- **spec-driven-development** — 在动代码前写好结构化规范，作为人机共识的"事实之源"。**适用查阅**：项目刚启动、需求模糊、改动跨多文件，或要做架构决策时。
- **idea-refine** — 通过发散与收敛的思考循环打磨创意。**适用查阅**:想法还很粗糙、要从一个模糊点子精炼成可执行方向时。

## Plan（规划阶段）

- **planning-and-task-breakdown** — 把整块工作拆成有序、可实施的小任务。**适用查阅**：已有 spec 或清晰需求但任务太大不知从哪起手、需要估算范围或拆出可并行项时。

## Build（构建阶段）

- **incremental-implementation** — 让改动分小步落地，避免一次写大量代码。**适用查阅**：改动跨多个文件、或感觉一次落地太大的时候。
- **test-driven-development** — 先写失败测试再写实现；修 bug 也先写复现测试。**适用查阅**：实现任何逻辑、修任何 bug、或要改动既有行为时。
- **context-engineering** — 给智能体调好上下文与规则文件。**适用查阅**：开新会话、智能体输出质量下滑、切换任务或要为项目配置 rules 时。
- **source-driven-development** — 每个实现决策都引用官方文档为依据。**适用查阅**：希望代码权威、可溯源、远离过期写法；用任何框架/库时正确性很重要的场景。
- **frontend-ui-engineering** — 构建生产质量的 UI（避免 "AI 味"样板）。**适用查阅**：写或改用户界面、做组件/布局/状态管理时。
- **api-and-interface-design** — 设计稳定的 API 与模块接口。**适用查阅**：设计 REST/GraphQL 端点、定义模块间类型契约、划前后端边界时。

## Verify（验证阶段）

- **browser-testing-with-devtools** — 通过 Chrome DevTools MCP 在真实浏览器里调试和验证。**适用查阅**：构建或调试浏览器内的东西，需要查 DOM、抓控制台错误、分析网络请求或做性能分析时。
- **debugging-and-error-recovery** — 系统性追根因、避免靠猜。**适用查阅**:测试失败、构建挂了、行为与预期不符、或遇到任何意外错误时。

## Review（审查阶段）

- **code-review-and-quality** — 多维度审查代码质量。**适用查阅**:合并任何改动前；review 自己、其他智能体或同事写的代码时。
- **code-simplification** — 不改变行为的前提下简化代码。**适用查阅**:代码能跑但难读难维护；review 时发现累积了不必要的复杂度。
- **security-and-hardening** — 对用户输入、认证、存储、第三方集成做加固。**适用查阅**:处理不可信输入、管理会话、或对接外部服务时。
- **performance-optimization** — 解决性能瓶颈。**适用查阅**:有明确性能需求、怀疑出现回归、Core Web Vitals 或加载时间需要改善时。

## Ship（交付阶段）

- **git-workflow-and-versioning** — 规范 git 工作流（提交、分支、冲突解决、多分支并行）。**适用查阅**:做任何代码改动；尤其是要组织多条并行工作流时。
- **ci-cd-and-automation** — 自动化构建/部署流水线，自动化 quality gate。**适用查阅**:搭建或修改 CI/CD、配置 CI 测试运行器、确立部署策略时。
- **deprecation-and-migration** — 移除老系统、迁移用户。**适用查阅**:决定是维护还是下线既有代码；做 API 或功能迁移时。
- **documentation-and-adrs** — 用 ADR 等形式记录架构决策与文档。**适用查阅**:做架构决策、改公开 API、发布功能、或需要给未来的人留上下文时。
- **shipping-and-launch** — 上线前的清单、监控、灰度与回滚策略。**适用查阅**:部署到生产前、要准备灰度发布或回滚预案时。

## Meta（元工作流）

- **using-agent-skills** — 元 skill：管理其他 skill 的发现与调用。**适用查阅**:开新会话、不确定当前任务该用哪个 skill 时。

---

**总计 21 个**：Define 2 / Plan 1 / Build 6 / Verify 2 / Review 4 / Ship 5 / Meta 1。

---

## Command → Skill 触发逻辑

agent-skills 在 `.claude/commands/` 下放了 7 个 slash command（`/spec /plan /build /test /review /code-simplify /ship`）。每个 command 是一个 markdown 文件，结构为：

```yaml
---
description: <一行说明>
---

Invoke the agent-skills:<skill-name> skill.

<给主 agent 的步骤说明：1. 2. 3. ...>
```

**触发语法**：用自然语言句式 `Invoke the agent-skills:<skill-name> skill` 调用 skill；命名空间 `agent-skills:` 用来避免与其他来源的同名 skill 冲突。

### 7 个 command 与所触发的 skill

| Command | 主 skill | 还会拉起 | 触发模式 |
|---|---|---|---|
| `/spec` | spec-driven-development | — | 单一 |
| `/plan` | planning-and-task-breakdown | — | 单一 |
| `/build` | incremental-implementation **+** test-driven-development | debugging-and-error-recovery（失败分支） | 多 skill 并挂 + 条件 |
| `/test` | test-driven-development | browser-testing-with-devtools（仅浏览器场景） | 主 + 可选辅 |
| `/review` | code-review-and-quality | security-and-hardening、performance-optimization（特定审查维度） | 主 + 子 skill 嵌套 |
| `/code-simplify` | code-simplification | code-review-and-quality（事后回审） | 串联 |
| `/ship` | shipping-and-launch | **3 个 subagent**：code-reviewer / security-auditor / test-engineer | **fan-out 编排** |

### 五种触发模式

1. **单一触发**（`/spec`、`/plan`）：command = 一个 skill 的入口包装。
2. **多 skill 并挂**（`/build`）：一句话同时拉起两个 skill，让方法论互补（增量交付 × TDD）。
3. **条件触发**（`/build` 末尾）：`If any step fails, follow the agent-skills:debugging-and-error-recovery skill.` 把失败分支 skill 挂上。
4. **嵌套子 skill**（`/review`）：主 skill 是 code-review-and-quality，特定维度（安全、性能）调用专门的子 skill。
5. **fan-out 到 subagent**（`/ship`）：跳出 command → skill 模式，改为 command → 3 个 persona subagent 并行 → 主上下文 merge。这里调度的是 `agents/` 下的 persona（`code-reviewer.md` / `security-auditor.md` / `test-engineer.md`），不是 skill。

### 一个关键观察：不是所有 skill 都靠 command 触发

7 个 command 显式 `Invoke ... skill` 拉起的 skill 共 11 处（去重 9 个）：
spec-driven-development、planning-and-task-breakdown、incremental-implementation、test-driven-development、browser-testing-with-devtools、debugging-and-error-recovery、code-review-and-quality、security-and-hardening、performance-optimization、code-simplification、shipping-and-launch。

**剩余约一半的 skill** 没有专属 command（context-engineering、git-workflow-and-versioning、frontend-ui-engineering、source-driven-development、api-and-interface-design、deprecation-and-migration、documentation-and-adrs、ci-cd-and-automation、idea-refine、using-agent-skills 等）。这些靠 SKILL.md frontmatter 中 description 的 "Use when..." 触发条件，由 Claude 在合适场景**自动激活**——这正是元 skill `using-agent-skills` 所规定的"skill 自动发现/调用"机制。

### Command 与 Skill 的职责切分

- **Command** = 流程步骤（"先做 X，再做 Y，失败走 Z"）+ skill 入口
- **Skill** = 方法论本身（Overview / When to Use / Process / Red Flags / Verification）
- Command 不重复 skill 的方法论，只调用并按场景给步骤
