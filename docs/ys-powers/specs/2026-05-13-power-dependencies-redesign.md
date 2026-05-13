# Spec: power-dependencies 文档重构

## Objective

重构 `docs/power-dependencies.md`，让它从 `commands` 和 `skills` 作者视角解释 ys-powers 的能力关系。

新版文档的核心读者是混合读者，但以继续编写和维护 `commands/`、`skills/` 的作者为主。文档需要帮助读者同时理解两条主线：

1. `Command -> Skill`：用户入口如何委托或组合能力模块。
2. `Skill -> Skill`：能力模块之间如何引用、建议配合或作为异常处理路径协作。

`agents/` 不作为主线，只在 `/ship` 明确编排时作为附录说明。

成功状态：

- 文档先用详细文本说明依赖关系，再用一张 Mermaid “一图流”做总览。
- `Command -> Skill` 和 `Skill -> Skill` 都是主线。
- `Skill -> Skill` 只记录源文件中明确出现的关系，并解释其关系类型，不做推断链。
- `agents`、`hooks`、`install` 等支撑内容不抢主线。
- 不再使用“审计”这类过重语气，改用“阅读口径”“关系类型”“维护规则”等文档化表达。

## Tech Stack

本次改动是 Markdown 文档重构，不涉及运行时代码。

- Language: Markdown
- Diagram: Mermaid
- Source directories: `commands/`, `skills/`, `agents/`
- Primary target file: `docs/power-dependencies.md`
- Design spec: `docs/ys-powers/specs/2026-05-13-power-dependencies-redesign.md`

## Commands

用于核对和验证的命令：

```bash
ls commands/*.md
ls skills/*/SKILL.md
ls agents/*.md
rg "Invoke|skill|Skill|agent|Agent|subagent|调用|使用" commands skills agents
git diff --check
```

如果需要检查 Markdown 结构：

```bash
rg '```' docs/power-dependencies.md
```

## Project Structure

与本次改动相关的目录：

```text
commands/                         -> slash command 源文件，是用户入口和工作流编排层
skills/<name>/SKILL.md            -> skill 源文件，是可复用能力模块层
agents/*.md                       -> specialist persona，仅在被 command 明确编排时说明
docs/power-dependencies.md        -> 本次要重构的依赖关系说明文档
docs/ys-powers/specs/             -> 本次设计 spec 保存位置
```

不作为本文依据的目录：

```text
.claude/                          -> 安装产物，不作为源依赖关系依据
refer/                            -> 第三方参考项目，只读，不作为 ys-powers 源依赖依据
```

## Code Style

文档使用中文说明，保留英文技术标识符、文件路径、command 名称和 skill 名称。

推荐段落格式：

```markdown
### `/spec`

类型：多 skill 串联型 command

直接关系：

- invokes `explore-then-ask`
- invokes `spec-driven-development`

说明：

`/spec` 先通过 `explore-then-ask` 澄清需求，再通过 `spec-driven-development` 生成结构化 spec。这里是强关系，因为 command 源文件明确要求 invoke 这两个 skills。
```

Skill 关系说明格式：

```markdown
### `spec-driven-development`

关系：

- references `incremental-implementation`
  - 类型：后续实现阶段建议
  - 理由：源文件将实现阶段描述为在 spec validated 后进入，而不是当前 skill 直接调用。
- references `test-driven-development`
  - 类型：实现阶段协作建议
  - 理由：用于说明实现时应遵循的工程方法，不等同于运行时调用。
```

Mermaid 风格：

- 一张主图优先，不拆成多张阶段图。
- 实线表示明确 `Command -> Skill`。
- 虚线表示 `Skill -> Skill` 的 `references`、`recommends`、`fallback` 等弱关系。
- `/ship -> agents` 使用虚线，并放在附属区域。

## Testing Strategy

本次是文档变更，验证重点是准确性和可读性：

- 源目录一致性：`commands/`、`skills/`、`agents/` 的数量和名称必须与文档一致。
- 关系准确性：每条 `Command -> Skill` 和 `Skill -> Skill` 必须能在源文件中找到文本依据。
- Mermaid 可读性：主图是一图流，避免 phase 分组和深度分组。
- Markdown 健康度：code fence 成对，`git diff --check` 通过。

不要求新增自动化测试。

## Boundaries

- Always:
  - 只修改 `docs/power-dependencies.md` 和本 spec 文件。
  - 以 `commands/` 和 `skills/` 为双主线。
  - 对 `Skill -> Skill` 关系给出类型和理由。
  - 保持 `.claude/` 作为安装产物，不作为依赖依据。
- Ask first:
  - 如果要修改任何 `commands/`、`skills/`、`agents/` 源文件。
  - 如果要把 hooks、install、references 提升为主线章节。
  - 如果要拆成多张 Mermaid 图。
- Never:
  - 不修改 `refer/` 下的任何文件。
  - 不把 `using-agent-skills` 画成依赖所有 skills 的普通强依赖。
  - 不把未明确出现的 skill 协作关系写成事实依赖。
  - 不再把不存在于 `commands/` 源目录的 command 写入主清单。

## Success Criteria

- 新版文档开头说明“阅读口径”，不使用“审计”作为章节主语。
- 文档包含一张 Mermaid 一图流总览，同时表达 `Command -> Skill` 与 `Skill -> Skill` 两条主线。
- 文档包含详细文本版 `Command -> Skill` 清单。
- 文档包含详细文本版 `Skill -> Skill` 清单，并解释每条关系的类型和理由。
- 自包含 commands 被单独说明，不伪装成 skill 依赖。
- `agents` 仅作为 `/ship` 附录说明。
- `git diff --check` 通过。

## Open Questions

当前已确认：

- 文本可以详细一点。
- 图片优先一图流。
- `Command -> Skill` 与 `Skill -> Skill` 都是主线。
- `Skill -> Skill` 只写明确出现的关系，并解释关系类型。

待实现时确认：

- 是否保留 hooks / install 的极简说明。如果保留，应放在维护规则或附录，不进入主图。
