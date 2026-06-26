---
description: Start spec-driven development — explore context, clarify requirements, prepare workspace, then write spec
---

## Phase 1: Explore and Clarify

<HARD-RULE name="spec-no-code-changes">

- Read only — no code changes。
- 可写产物：
  - `docs/ys-powers/specs/YYYY-MM-DD-<feature-name>-design.md`（Phase 3 结构化 spec）
  - `CONTEXT.md` / `CONTEXT-MAP.md` 及相关 per-context `CONTEXT.md`（Phase 1.5 由 `domain-modeling` 更新）
  - `docs/adr/NNNN-*.md`（Phase 1.5 由 `domain-modeling` 提议并创建）

</HARD-RULE>

Begin by understanding what the user wants to build.

Invoke the **explore-then-ask** skill to ask clarifying questions one at a time (in Chinese) about:

1. The objective and target users
2. Core features and acceptance criteria
3. Tech stack preferences and constraints
4. Known boundaries (what to always do, ask first about, and never do)

Continue through explore-then-ask's full dialogue flow: surface assumptions, propose 2-3 approaches with trade-offs, present design sections, and get user approval.

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

<IMPORTANT>
- Write the spec content in Chinese. Keep technical terms, code identifiers, file paths, and command names in English.
- Save the spec to `docs/ys-powers/specs/YYYY-MM-DD-<feature-name>-design.md` where `<feature-name>` is a kebab-case short name derived from the spec title.
- If the directory does not exist, create it first.
- Save directly without asking the user for confirmation.
</IMPORTANT>
