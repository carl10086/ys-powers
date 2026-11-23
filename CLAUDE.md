# CLAUDE.md

`ys-powers` 是一套以 Matt Pocock skills 为基础的本地 coding workflow。

## 目录

- `skills/` — 当前使用的 Matt skill 分包与本地 `eli`
- `install/` — 本地与全局安装器
- `docs/` — 当前配置、使用说明和历史记录
- `refer/` — 只读的上游参考仓库

当前使用的 skill 目录只有：

```text
skills/engineering/
skills/productivity/
skills/eli/
```

`deprecated/`、`in-progress/`、`misc/` 不属于当前使用范围。不要为了保持旧目录形状重新加入它们。

## 保持 Matt 的边界

保持 Matt 原始 skill 的目录结构、frontmatter、Prompt、调用策略和每个 skill 的 `agents/openai.yaml`。不要平铺、重命名或重新实现 Matt 的 skill。

本地允许的差异仅包括：

- 安装器和本地 manifest；
- 上游同步记录；
- 中文解释文档；
- `skills/eli/`；
- 面向本地运行时的必要适配。

不要修改 `refer/` 下的上游参考内容，也不要为 OMP 和 Claude 维护两套 Prompt 流程。

## 安装

```bash
make local-install
make local-install project-dir=/path/to/project
make global-install
```

`project-dir` 是 Make 变量，不是 `make` 选项。安装器只安装当前三个 skill 分包，不自动安装或创建 `AGENTS.md`、`CLAUDE.md`、`docs/agents/` 或 `rules/`。这些项目级文件由 `setup-matt-pocock-skills` 在目标项目内按选择生成。

`make global-install` 会更新 `~/.claude/`，并清理安装器登记的旧版 `commands/`、`agents/`、`references/`、`hooks/`、`rules/` 目标。涉及用户全局环境时，先确认目标范围。

## 核心 workflow

```text
grill-with-docs → to-spec → to-tickets → implement → code-review
```

复杂并行实现可以把 `implement` 换成 `implement-spec`。这只是推荐链路，不是自动流水线；每一步结束后由用户或 agent 根据产物决定是否继续调用下一个 skill。`grill-with-docs` 不会自动调用 `to-spec`。

## 项目级配置

第一次在项目中使用 Matt engineering skills 时调用 `setup-matt-pocock-skills`。它按顺序处理：

1. 可选的中文技术文档写作规则；
2. issue tracker；
3. 安装了 `triage` 时的 triage labels；
4. domain docs 布局。

当前项目级配置在 `docs/agents/`。如果启用文档语言规则，新写或新修改的项目技术文档以中文为主；technical terms、domain 定义、code identifiers、file paths、commands 和配置值保留 English。历史文档不翻译、不重写。

## 历史版本

- `1.0.0`：旧版 ys-powers。
- `matt-powers-baseline`：Matt workflow 切换基线。
- `2.0.0`：Matt-first workflow 的正式 release，待当前实现和文档验证完成后创建。
