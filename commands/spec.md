---
description: Start spec-driven development — load confirmed intent, discuss implementation design, prepare workspace, then write spec
---

## Phase 1: Load Intent and Design Dialogue

<HARD-RULE name="spec-no-code-changes">

- Read only — no code changes。
- 可写产物：
  - `docs/ys-powers/specs/YYYY-MM-DD-<feature-name>-design.md`（Phase 3 结构化 spec）
  - `CONTEXT.md` / `CONTEXT-MAP.md` 及相关 per-context `CONTEXT.md`（Phase 1.5 由 `domain-modeling` 更新）
  - `docs/adr/NNNN-*.md`（Phase 1.5 由 `domain-modeling` 提议并创建）

</HARD-RULE>

载入 confirmed intent（需求澄清只发生在 `/clarify-intent`，本命令不重复）：

1. 本会话刚运行过 `/clarify-intent` → 直接使用会话内 confirmed intent
2. 否则从 `docs/ys-powers/intent/` 读取：用户指定了 topic 读对应文件；未指定取最近修改的一份；topic 与当前需求明显不符的按没有处理；无法确定则询问用户
3. 目录不存在或没有匹配文档 → 停止，提示用户先运行 `/clarify-intent`

以 confirmed intent 为输入，调用 **explore-then-ask** skill 做实现层设计对话：

1. Tech stack preferences and constraints
2. Known boundaries (what to always do, ask first about, and never do)

Continue through explore-then-ask's dialogue flow: surface assumptions, propose 2-3 approaches with trade-offs, present design sections, and get user approval.

## Phase 1.5: Domain Modeling Checkpoint

Before preparing the workspace, check whether Phase 1 produced domain assets that need recording.

If `CONTEXT.md` exists, read it first (and `CONTEXT-MAP.md` if present, plus any relevant per-context `CONTEXT.md` files). Scan `docs/adr/` for decisions related to this feature.

Check whether any of the following is true:

- [ ] New or sharpened domain terms should go into `CONTEXT.md`
- [ ] Phase 1 language conflicts with an existing `CONTEXT.md` definition
- [ ] A design decision meets all three ADR criteria (hard to reverse, surprising without context, result of a real trade-off)

If any checkbox is true, **invoke the `domain-modeling` skill now** to update `CONTEXT.md` inline and offer ADRs. Otherwise skip this step.

After the checkpoint, briefly report what changed, then proceed to Phase 2.

## Phase 2: Prepare Workspace

Ask the user to choose a workspace strategy:

> 这个需求需要隔离开发环境吗？
> 1. 创建 git worktree（适合较大改动，完全隔离目录）
> 2. 创建 feature branch（适合常规改动，轻量分支）
> 3. 直接基于当前分支（适合极小改动，如配置调整、单函数修改）

根据选择执行：

- **worktree**: derive kebab-case `topic`, then `git worktree add .claude/worktrees/${topic}`
- **feature branch**: derive kebab-case `topic`, then `git checkout -b feat/${topic}`
- **current branch**: no action

## Phase 3: Structured Spec

Invoke the **spec-driven-development** skill to generate a structured spec covering all six core areas: objective, commands, project structure, code style, testing strategy, and boundaries.

以 confirmed intent 与已确认的设计方案为输入直接撰写，不重新访谈需求（该 skill 中 "ask clarifying questions" 的指引在此不适用）；仍不确定的点写入 spec 的 Open Questions 段。

<IMPORTANT>
- Write the spec content in Chinese. Keep technical terms, code identifiers, file paths, and command names in English.
- Save the spec to `docs/ys-powers/specs/YYYY-MM-DD-<feature-name>-design.md` where `<feature-name>` is a kebab-case short name derived from the spec title.
- If the directory does not exist, create it first.
- Save directly without asking the user for confirmation.
</IMPORTANT>
