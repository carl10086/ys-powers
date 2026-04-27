# CLAUDE.md

`ys-powers` 是一套用于增强 Claude Code 工作流的本地能力集，封装了 skills、rules、commands 三类配置以及一键安装到任意项目 `.claude/` 的脚本。

## 顶层目录速览

- `skills/` — Claude Code 技能定义
- `rules/` — 项目级或通用编码规范
- `commands/` — 工作流命令手册
- `sop/` — 标准操作流程
- `install/local-install.py` — 把上面三类能力安装到目标项目 `.claude/` 的脚本（详细策略见 `README.md`）
- `docs/` — 项目内部文档（详见下节）
- `refer/` — **只读** 第三方参考项目（详见下节）

## docs/ 项目内部文档

按主题划分子目录，每个子目录聚焦一个话题：

- `docs/codebase/` — 本仓库自身的架构文档（`ARCHITECTURE.md`）
- `docs/agent-skills/` — `refer/agent-skills` 项目的中文索引/笔记（`overview.md`）
- `docs/superpowers/` — `refer/superpowers` 项目的 skill 分析与实施 specs（specs 子目录）
- `docs/systematic-debugging/` — systematic-debugging 主题专栏
- `docs/ys-powers/` — ys-powers 自身 skill / command 的分析笔记
- 顶层散文件（如 `claude-prompt-design-paradigms.md`）— 跨主题的零散研究

约定：与 `refer/<X>/` 同名的 `docs/<X>/` 是该参考项目的对照笔记；spec 类设计文档放在 `docs/superpowers/specs/`。

## refer/ 第三方参考项目

`refer/` 存放第三方开源工程项目，用于借鉴方法论和对比设计。**Claude 不应修改其中任何文件**，只能读取用于学习/对比/取灵感。如果发现某个 skill/command 值得搬运，应在主项目 `skills/` 或 `commands/` 下重写，而不是直接复制粘贴。

### agent-skills/

工程级 AI 编码技能集，围绕 `/spec /plan /build /test /review /ship` 六命令的开发生命周期组织，关键词是阶段化与 quality gate。

**适用查阅**：设计 spec→plan→build 流水线、需要看工程化质量门 skills 时。

### superpowers/

Jesse Vincent 的完整软件开发方法论，强调真正的 red/green TDD、subagent-driven-development、YAGNI 与 DRY。

**适用查阅**：找 TDD、子智能体协作、计划执行类 skills 的标杆实现时。

### get-shit-done/

轻量元提示与 spec 驱动开发系统，目标是缓解 context rot，跨多家 CLI 兼容（Claude Code / Codex / Cursor / Windsurf 等）。

**适用查阅**：想看更轻量的、跨平台的 spec-driven 设计时。

## 给 Claude 的工作约定

- `refer/` 下文件**只读**：不要 edit、不要删除、不要重排。
- 借鉴 `refer/` 内容时，应在 ys-powers 自有目录中重写，而非搬运。
- `install/local-install.py` 的覆盖策略详见 `README.md`，本文件不重复说明。
