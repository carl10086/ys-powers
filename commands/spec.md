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

After `explore-then-ask` completes and the user approves the design direction, run this checkpoint before preparing the workspace.

<HARD-RULE name="spec-domain-modeling-checkpoint">

- Read existing domain assets before deciding whether to invoke `domain-modeling`
- Invoke `domain-modeling` if ANY of the following is true:
  1. New domain terms were resolved during Phase 1
  2. Existing `CONTEXT.md` terms conflict with Phase 1 discussion
  3. A design decision meets all three ADR criteria (hard to reverse, surprising without context, result of a real trade-off)
- Skip this phase only if none of the above apply
- Do NOT skip just because `CONTEXT.md` does not exist yet

</HARD-RULE>

### Step 1: Read existing domain assets

Read the following silently (if they do not exist, note their absence and continue):

- `CONTEXT.md` at the project root
- `CONTEXT-MAP.md` at the project root — if it exists, read the relevant per-context `CONTEXT.md` files
- `docs/adr/` files relevant to the feature area

### Step 2: Detect domain modeling needs

Compare the output of Phase 1 against the existing assets:

- [ ] Did Phase 1 introduce a new domain term that should be in the glossary?
- [ ] Did Phase 1 sharpen or redefine an existing term?
- [ ] Does Phase 1 language conflict with an existing `CONTEXT.md` definition?
- [ ] Did Phase 1 produce a decision that meets all three ADR criteria?

### Step 3: Invoke `domain-modeling`

If any checkbox above is true, **invoke the `domain-modeling` skill now**. Continue the current session with this focus:

- Review the terms and decisions from Phase 1
- Update `CONTEXT.md` inline for any resolved or sharpened terms
- Offer ADRs only for decisions that meet the ADR criteria
- Surface any conflicts between Phase 1 language and existing `CONTEXT.md`

The `domain-modeling` skill decides how to update `CONTEXT.md` and whether to propose an ADR.

### Step 4: Report checkpoint result

After the checkpoint, briefly report:

```text
领域资产检查：CONTEXT.md [未更新/更新 X 项/新建并写入 X 项]，ADR [未创建/提议创建 NNNN-xxx（等待确认）/已创建 NNNN-xxx]。
```

Then proceed to Phase 2.

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
