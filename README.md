# ys-powers

`ys-powers` 是一套以 Matt Pocock skills 为基础的本地 coding workflow。

当前主线按 `2.0.0` 设计：保留 Matt 的 skill 内容、frontmatter、调用策略和 `agents/openai.yaml`，只保留必要的本地定制与安装能力。

## 当前目录

```text
skills/
├── engineering/   代码工程主流程与按需工程能力
├── productivity/  上下文、沟通与文档能力
└── eli/           ys-powers 本地 HTML 解释能力

install/           本地与全局安装器
docs/              当前说明、安装配置与历史记录
refer/             只读的上游参考仓库
```

`deprecated/`、`in-progress/`、`misc/` 不属于当前使用范围，也不再放在 `skills/` 中。

## 安装

### 当前项目

```bash
make local-install
make local-install project-dir=/path/to/project
```

不要写成 `make local-install --project-dir=...`；`project-dir` 是 Make 变量，不是 `make` 选项。

安装目标是：

```text
<project>/.claude/skills/
```

`engineering/` 与 `productivity/` 会按 Matt 的运行时发现方式安装到同一个 `skills/` 目录；`eli` 保持独立目录。安装器不会自动创建项目的 `AGENTS.md`、`CLAUDE.md` 或 `docs/agents/`，这些由 `setup-matt-pocock-skills` 在项目内按选择生成。

### 全局环境

```bash
make global-install
make update-global
make uninstall-global
```

全局安装会更新 `~/.claude/`，并按安装器登记的 legacy targets 清理旧版 `commands/`、`agents/`、`references/`、`hooks/`、`rules/` 等内容。执行前确认这是期望的全局迁移。

## 核心 workflow

常规代码任务：

```text
grill-with-docs
  → to-spec
  → to-tickets
  → implement
  → code-review
```

多个 ticket 的复杂实现：

```text
grill-with-docs
  → to-spec
  → to-tickets
  → implement-spec
  → code-review
```

这不是自动流水线。每个 skill 完成后，用户或 agent 根据当前产物决定是否继续调用下一个 skill；`grill-with-docs` 不会自动调用 `to-spec`，`implement` 与 `implement-spec` 也可以手动选择。

按需分支：

- `wayfinder`：目标很大、路线不清，先建立 decision-ticket map。
- `research`：需要外部 primary sources 时保存 cited Markdown。
- `prototype`：用 throwaway code 验证 state model、logic 或 UI。
- `codebase-design`：设计 deep module、interface、seam 和 adapter。
- `diagnosing-bugs`：复现、定位、修复并验证 bug。
- `browser-testing-with-devtools`：有前端项目时，代码完成后手动做真实浏览器端到端验证。
- `pr`：整理 PR body、证据和 merge risk。
- `retro`：复盘本次 coding session。

## 项目初始化

第一次在项目中使用 Matt engineering skills 时，调用：

```text
setup-matt-pocock-skills
```

它会按顺序处理：

1. 可选的中文技术文档写作规则；
2. issue tracker；
3. triage labels（仅安装了 `triage` 时）；
4. domain docs 布局。

无远端或明确选择本地时，issue tracker 使用 `.scratch/`；存在 GitHub remote 时 setup 会推荐 GitHub，也可以手动选择 GitHub、GitLab 或其他工作流。初始化只执行一次；后续只有切换配置或从头重建时才需要重新执行。

## 文档规则

新写或新修改的项目技术文档以中文为主；`domain` 定义、technical terms、code identifiers、file paths、commands 和配置值保留 English。历史文档不因启用该规则而翻译或重写。

当前项目的 active configuration 位于：

```text
docs/agents/
```

`docs/share/`、`docs/gstack/`、`docs/workflow/specs/`、`docs/ys-powers/intent/` 和旧的同步记录属于历史材料，不作为当前安装或 workflow 的事实入口。

## 版本与上游

- `1.0.0`：旧版 ys-powers。
- `matt-powers-baseline`：切换到 Matt workflow 前的迁移基线，不是正式 release。
- `2.0.0`：Matt-first workflow 的正式 release，待当前安装器、文档和验证完成后创建。

不要修改 `refer/` 下的上游参考内容。需要更新时，先同步上游，再审查本地允许的差异。
