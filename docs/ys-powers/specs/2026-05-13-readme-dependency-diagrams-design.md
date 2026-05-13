# Spec: README 依赖关系简图更新

## Objective

更新 `README.md`，让首次阅读 ys-powers 的使用者能快速理解：

1. 常见开发流程中应该调用哪些 commands。
2. 16 个 commands 大致如何连接到核心 skills。
3. 更完整的依赖关系应去阅读 `docs/power-dependencies.md`。

README 面向使用者，不承担维护者级完整依赖说明。完整的 `Command -> Skill` 和 `Skill -> Skill` 关系仍由 `docs/power-dependencies.md` 承担。

成功状态：

- README 保留两张小 Mermaid 图。
- 第一张图说明典型使用工作流。
- 第二张图说明简化后的 `Command -> Skill` 依赖关系。
- 第二张图覆盖当前 `commands/` 源目录中的 16 个 commands，但自包含 commands 可以聚合展示。
- README 中的数量与当前源目录一致：16 commands、25 skills、3 agents。
- README 中不再使用不存在于当前 `commands/` 源目录的 `/review`，改为 `/ys-review`。

## Tech Stack

本次改动是 Markdown 文档更新，不涉及运行时代码。

- Language: Markdown
- Diagram: Mermaid
- Target file: `README.md`
- Reference file: `docs/power-dependencies.md`
- Source directories: `commands/`, `skills/`, `agents/`

## Commands

用于核对和验证的命令：

```bash
ls commands/*.md
ls skills/*/SKILL.md
ls agents/*.md
rg "/review|28 个|28|/ys-review|docs/power-dependencies.md" README.md
git diff --check -- README.md
```

如果需要检查 Markdown code fence：

```bash
rg '```' README.md
```

## Project Structure

相关文件：

```text
README.md                         -> 本次更新目标，面向使用者的项目入口文档
docs/power-dependencies.md        -> 详细依赖关系说明
commands/*.md                     -> command 源目录，用于确认 16 个 commands
skills/*/SKILL.md                 -> skill 源目录，用于确认 25 个 skills
agents/*.md                       -> agent 源目录，用于确认 3 个 agents
```

不作为 README 依赖依据：

```text
.claude/                          -> 安装产物，不作为源目录统计依据
refer/                            -> 第三方参考项目，只读，不作为 README 当前能力统计依据
```

## Code Style

README 使用中文说明，保留 command、skill、路径等英文标识符。

Mermaid 风格：

- 图一保持横向主流程，节点少，便于快速理解。
- 图二覆盖 16 个 commands，但允许把 embedded-workflow commands 聚合为一组。
- 不在 README 图中展开完整 `Skill -> Skill` 关系。
- 不把 agents 放成主线，只在 `/ship` 周边作为附属说明。
- 图下方用 1-2 句解释读图方式，并链接 `docs/power-dependencies.md`。

推荐图形意图：

```markdown
## 典型工作流

一张图说明 `/spec -> /plan -> /build -> /test -> /ys-review -> /ship`。

## 简化依赖关系

一张图说明核心 commands 如何连接到直接 skills，自包含 commands 聚合为一组。
```

## Testing Strategy

本次是文档变更，验证重点：

- `README.md` 中 command / skill / agent 数量与源目录一致。
- `/review` 被替换为 `/ys-review`，除非明确作为历史说明出现。
- Mermaid code fence 成对。
- `git diff --check -- README.md` 通过。
- README 不复制 `docs/power-dependencies.md` 的长篇说明，只保留简化入口图。

不需要新增自动化测试。

## Boundaries

- Always:
  - 只修改 `README.md` 和本 spec 文件。
  - README 面向使用者，保持简洁。
  - 保留两张小 Mermaid 图。
  - 将详细依赖关系链接到 `docs/power-dependencies.md`。
- Ask first:
  - 如果要修改 `docs/power-dependencies.md`。
  - 如果要新增或修改 `commands/`、`skills/`、`agents/` 源文件。
  - 如果要把 README 改成维护者级长文档。
- Never:
  - 不修改 `refer/`。
  - 不使用 `.claude/` 作为源目录统计依据。
  - 不把 README 的简图扩展成完整依赖图。

## Success Criteria

- README 中有两张 Mermaid 图：
  - 典型工作流图。
  - 简化 `Command -> Skill` 依赖图。
- README 能覆盖当前 16 个 commands 的入口说明。
- README 中 skills 数量为 25。
- README 中 review 入口使用 `/ys-review`。
- README 明确提示完整依赖说明见 `docs/power-dependencies.md`。
- `git diff --check -- README.md` 通过。

## Open Questions

已确认：

- README 面向使用者快速上手。
- 保留两张小图。
- 简化依赖图尽量覆盖所有 16 个 commands，但保持图小。

待实现时处理：

- 自包含 commands 在图中聚合展示，正文表格中补全具体 command 名称。
