# CLAUDE.md 设计：项目说明 + refer/ 结构

- 日期：2026-04-26
- 类型：文档新增
- 目标文件：`/Users/carlyu/soft/projects/ys-powers/CLAUDE.md`

## 背景

`ys-powers` 仓库目前只有 `README.md`，没有面向 Claude Code 的项目级说明文件 (`CLAUDE.md`)。最近在 `refer/` 下新增了开源参考项目 `agent-skills`，加上原有的 `superpowers` 与 `get-shit-done`，共三个第三方项目。当前缺乏一份让 Claude 快速理解项目结构、并清楚 `refer/` 是只读资料的文档。

## 目标

新增一份**轻量全项目说明**风格的 `CLAUDE.md`：

1. 让 Claude 在新会话进入项目时即能理解顶层目录的用途。
2. 重点说明 `refer/` 是**只读参考资料**，并对其下三个子项目做中等深度介绍（定位 + 适用查阅场景）。
3. 避免与 `README.md` 重复（如 install 脚本细节、覆盖策略）。

## 非目标

- 不写完整项目文档（不覆盖每个 skill / rule / command 的细节）。
- 不修改 `README.md`。
- 不在 `refer/` 下做任何修改。

## 文件结构

```
1. 项目一句话定位
2. 顶层目录速览 (skills / rules / commands / sop / install / docs / refer)
3. refer/ 详细说明（重点章节）
4. 给 Claude 的工作约定
```

### 第 1 节：项目定位（1-2 句）

> ys-powers 是一套用于增强 Claude Code 工作流的本地能力集，封装了 skills、rules、commands 三类配置以及一键安装到任意项目 `.claude/` 的脚本。

### 第 2 节：顶层目录速览

紧凑列表，一行一个：

- `skills/` — Claude Code 技能定义
- `rules/` — 项目级或通用编码规范
- `commands/` — 工作流命令手册
- `sop/` — 标准操作流程
- `install/local-install.py` — 把上面三类能力安装到目标项目 `.claude/` 的脚本（详细策略见 `README.md`）
- `docs/` — 项目内部文档（包括 specs / codebase 架构）
- `refer/` — **只读** 第三方参考项目（详见下节）

### 第 3 节：refer/ 章节（重点）

引导段：

> `refer/` 存放第三方开源工程项目，用于借鉴方法论和对比设计。**Claude 不应修改其中任何文件**，只能读取用于学习/对比/取灵感。如果发现某个 skill/command 值得搬运，应在主项目 `skills/` 或 `commands/` 下重写，而不是直接复制粘贴。

三个子项目（中等深度，每个 2-3 句：定位 + 适用查阅场景）：

- **agent-skills/** — 工程级 AI 编码技能集，围绕 `/spec /plan /build /test /review /ship` 六命令的开发生命周期，关键词是 quality gate 与阶段化。**适用查阅**：设计 spec→plan→build 流水线、需要工程化质量门 skills 时。
- **superpowers/** — Jesse Vincent 的完整软件开发方法论，强调真正的 red/green TDD、subagent-driven-development、YAGNI / DRY。**适用查阅**：找 TDD、子智能体协作、计划执行类 skills 的标杆实现。
- **get-shit-done/** — 轻量元提示与 spec 驱动开发系统，目标是缓解 context rot，跨多家 CLI 兼容。**适用查阅**：想看更轻量的、跨平台（Codex / Cursor / Windsurf 等）的 spec-driven 设计时。

> 注：`get-shit-done/` 的 README 含较多营销内容（代币、徽章等），CLAUDE.md 中只聚焦其工程价值。

### 第 4 节：给 Claude 的工作约定（3-5 行）

- `refer/` 下文件**只读**：不要 edit、不要删除、不要重排。
- 借鉴 `refer/` 内容时，应在 ys-powers 自有目录中重写，而非搬运。
- `install/local-install.py` 的覆盖策略详见 `README.md`，不在 CLAUDE.md 中重复。

## 实施步骤

1. 在仓库根目录创建 `CLAUDE.md`，按上述四节结构填写。
2. 验证：通读一遍，确保没有自相矛盾、没有占位符、与 `README.md` 不重复。
3. 提交：`docs(claude-md): 新增 CLAUDE.md 说明项目结构与 refer/ 角色`。

## 验收标准

- `CLAUDE.md` 存在于仓库根目录。
- 文件包含上述四节，且 refer/ 下三个子项目均有"定位 + 适用查阅场景"形式的描述。
- 明确告知 Claude `refer/` 是只读边界。
- 与 `README.md` 无冗余重复（不重写安装命令、不再列覆盖策略细节）。

## 不在本次范围

- 修改 `README.md`。
- 改动 `refer/` 下任何文件。
- 给 `skills/` `rules/` `commands/` 写更细的文档。
