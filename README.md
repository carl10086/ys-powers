# ys-powers

`ys-powers` 是以 Matt Pocock skills 为基础的本地工程能力集，只保留必要的 ys-powers 定制：`eli` 与项目级 `rules`。

## 能力结构

```text
skills/
├── engineering/    写代码的工程能力
├── productivity/   通用工作流能力
├── misc/           低频工具
├── in-progress/    beta 能力
├── deprecated/     上游保留的废弃能力
└── eli/            ys-powers 的解释能力
```

Matt 的原始目录结构、frontmatter、调用策略和 `agents/openai.yaml` 保持不变。

- `User-invoked`：用户显式调用
- `Model-invoked`：模型按场景自动触发
- `misc`：稳定但低频，保留在源目录但不默认安装
- `in-progress`：公开 beta，保留在源目录但不默认安装
- `deprecated`：上游保留，但不默认安装

默认本地能力只安装：

```text
engineering
productivity
eli
rules
```

Matt 的其他分包仍保留在源目录和 `refer/` 中，后续可通过安装配置显式启用。
源目录保留 Matt 的分包结构；安装到项目 `.claude/skills/` 时，安装器会把选中的 skill 扁平化到一级目录，确保 Claude 能发现每个 `SKILL.md`。这只改变安装布局，不改变 skill 内容。

默认工程链由 Matt skills 自己的调用约束决定，不在本项目中重新实现：

```text
grill-with-docs
→ grilling / domain-modeling
→ to-spec
→ to-tickets
→ implement / implement-spec
→ tdd
→ code-review
→ retro
```

## ys-powers 定制

```text
skills/eli/
rules/code.md
```

其他旧版 `commands/`、`agents/`、`references/`、`hooks/` 已移除，不再与 Matt 流程并存。

## 安装

### 本地安装

```bash
make local-install
make local-install project-dir=/path/to/project
```

安装到 `<project>/.claude/`，适合当前实验和项目级验证。

### 全局安装

```bash
make global-install
```

安装到 `~/.claude/`。当前实验阶段不要执行此命令；全局环境清理另行处理。

### 更新与卸载

```bash
make update-local
make update-global
make uninstall-local
make uninstall-global
```

安装器只管理 `skills/` 和 `rules/`，不再注入旧 hooks，也不再安装 commands、agents 或 references。

## 上游来源

`refer/mattpocock-skills/` 是只读的 Matt 上游参考。不要直接修改其中内容。

同步上游后，更新当前分支的 `skills/`，保留必要的本地差异，并在实验记录中说明差异。

## 实验记录

当前方案：`docs/ys-powers/intent/matt-first-experiment.md`

目标：使用真实中等规模代码任务验证 Matt 完整能力，而不是提前判断 Matt 必然优于旧 ys-powers。
