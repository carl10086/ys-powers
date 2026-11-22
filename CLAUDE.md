# CLAUDE.md

`ys-powers` 是以 Matt Pocock skills 为基础的本地工程能力集。

## 目录

- `skills/` — Matt 的完整 skill 分包，以及 ys-powers 的 `eli`
- `rules/` — 保留的项目级编码规则
- `install/` — 本地与全局安装器
- `docs/` — 实验意图、迁移说明和解释文档
- `refer/mattpocock-skills/` — 只读的 Matt 上游参考

## Skills 分包

```text
skills/engineering/
skills/productivity/
skills/misc/
skills/in-progress/
skills/deprecated/
skills/eli/
```

保持 Matt 原始目录结构、frontmatter、调用策略和每个 skill 的 `agents/openai.yaml`。不要把 skill 平铺、重命名或重新实现。
源目录保持分包；安装器针对本地 `.claude/skills/` 做一级扁平化，因为本地 Claude skill 发现只读取直接子目录。扁平化不修改 skill 内容。

Matt 的分包含义：

- `engineering`：日常代码工程能力
- `productivity`：通用工作流能力
- `misc`：稳定但低频的工具
- `in-progress`：公开 beta 能力
- `deprecated`：上游保留的废弃能力
- `eli`：ys-powers 的本地能力

## 本地化边界

允许的本地差异：

- `.scratch/` → `.ys-powers/`
- 安装器和本地 manifest
- 上游同步记录
- 中文解释文档
- `skills/eli/`
- `rules/code.md`

不要针对 OMP 或 Claude 另做两套 prompt 流程。不要修改 `refer/mattpocock-skills/`。

## 安装

```bash
make local-install
make local-install project-dir=/path/to/project
```

实验阶段只使用 local install。不要操作全局 `~/.claude/`，除非用户明确要求进行全局迁移。

安装器只安装 `skills/engineering`、`skills/productivity`、`skills/eli` 和 `rules/`；`misc`、`in-progress`、`deprecated` 保留在源目录但不默认安装。

## 实验方案

完整意图记录在 `docs/ys-powers/intent/matt-first-experiment.md`。先用真实代码任务验证 Matt 完整能力，再决定后续定制。
