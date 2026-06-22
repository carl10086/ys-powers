---
name: explore-then-ask
description: Explores project context and clarifies design direction through structured dialogue. Use when the user's intent is already clear but the concrete design within this codebase is not.
---

# Explore Then Ask

## Overview

This skill turns a clear intent into a confirmed design direction that fits the current codebase.

It assumes the user already knows what they want (via `interview-me` or direct statement). The remaining gap is usually invisible: which existing patterns to follow, which constraints are real, which trade-offs matter in this project. This skill closes that gap by exploring context first, then asking one design question at a time.

<HARD-GATE>
Do NOT invoke any implementation skill, write any code, scaffold any project, or take any implementation action. Do NOT save files or write design docs. This is a dialogue-only skill.
</HARD-GATE>

<IMPORTANT>
- You must use chinese to ask questions
- You must use chinese to present design and trade-offs
</IMPORTANT>

## Gating Check

Before doing anything else, confirm the intent is clear enough to design against:

```
进入设计澄清前，我确认一下意图：
- 我们要解决的问题是：...
- 预期结果是：...
- 主要约束是：...

如果以上任何一点还不清楚，建议先用 /interview-me 澄清，再回来做设计。
```

If the user cannot confirm all three, stop and suggest `/interview-me`. Do not try to extract intent inside this skill.

## The Process

### 1. Hypothesize context, with confidence

State your read of the project situation in one sentence, plus an honest confidence number:

```
HYPOTHESIS: 当前项目已有类似的 X 模块，新功能可以复用其数据层，主要改动在 API 层。
CONFIDENCE: ~40% — missing: 是否已有 X 模块、现有 API 的版本约束、团队的错误处理偏好
```

When confidence is below ~70%, append the missing pieces on the same line.

### 2. Explore context

Search historical SOPs, then read relevant files, docs, and recent commits.

- Explore only what is relevant to the current design decision. Do not seek complete project understanding.
- Do it silently — do not dump file listings unless something is unclear.
- If the request spans multiple independent subsystems, flag this immediately and decompose first.

### 3. Present assumptions for correction

After exploring, list the assumptions you will design against:

```
我的设计假设：
1. ...
2. ...
3. ...

→ 有不对的地方请现在纠正，否则我将基于这些假设继续。
```

This is the only step where batching is allowed. The goal is to surface misalignment before asking design questions.

### 4. Ask design questions, one at a time, each with a guess

Format:

```
Q: <one focused design question>
GUESS: <your hypothesis for the answer, with reasoning>
```

Focus on decisions that affect the design: data flow, boundaries, dependencies, error handling, compatibility, testing strategy. Not purpose or success criteria — those belong to `interview-me`.

Wait for the user's reaction before asking the next question.

### 5. Probe real constraints

When the user answers with convention, best practice, or vague technical ideals ("use clean architecture", "make it scalable", "follow the standard"), ask:

> 如果 X 和 Y 冲突，哪个可以妥协？或者：这个约束是硬性要求，还是团队惯例？

This separates real blockers from defaults.

### 6. Sketch 2-3 approaches

Once the design space is clear, sketch 2-3 approaches in 2-3 sentences each:

- Approach A: ...
- Approach B: ...
- Approach C: ... (if needed)

Lead with your recommendation and why. Include trade-offs in terms of cost, risk, maintainability, and fit with existing code.

### 7. Present detailed design sections

After the user picks an approach, present the design in sections scaled to complexity:

- Architecture
- Components / modules
- Data flow
- Error handling
- Testing strategy

Ask after each section: "这一节看起来对吗？" Scale each section to a few sentences if straightforward, up to 200-300 words if nuanced.

**Design for isolation and clarity:**
- Break the system into units with one clear purpose each.
- For each unit: what does it do, how do you use it, what does it depend on?
- Can someone understand a unit without reading its internals?
- Can you change the internals without breaking consumers?

**Working in existing codebases:**
- Follow existing patterns unless there is a clear, justified reason not to.
- Include targeted improvements only if they serve the current goal.
- Do not propose unrelated refactoring.

### 8. Confirm the design direction

When your confidence is high, restate the agreed direction tightly:

```
最终确认的设计方向：
- 方案：...
- 关键决策：...
- 依赖：...
- 风险：...
- 不在本次范围：...

Yes / no / refine?
```

Including "Out of scope" is non-negotiable.

The gate is an explicit "yes." "Sounds good", "whatever you think", and silence are not yes. If the user gives a weak answer, ask: "有什么想调整的吗？"

## Stop Condition

You are done when you can predict the user's reaction to the next technical decision. If you cannot, you are not done.

If you have gone several rounds and still cannot predict, stop and say: "我已经问了 X 轮，仍然无法确定你在几个关键技术选择上的偏好。可能是意图还不够清晰，或者项目上下文里有我遗漏的约束。要不要再确认一下意图，或者补充一些背景？"

## Boundary with interview-me

- `interview-me` extracts what the user wants. Its output is a confirmed intent.
- `explore-then-ask` takes that intent and figures out how to design it in this codebase. Its output is a confirmed design direction.
- If intent is unclear, use `interview-me` first.
- After this skill, the next step is usually `/spec` or `/plan`.

## Red Flags

- Exploring without a hypothesis attached.
- Asking about purpose or success criteria instead of design decisions.
- Asking multiple design questions in one message.
- Accepting "whatever you think" as a final answer.
- Starting to write code, docs, or invoke another skill.
- Skipping the "Out of scope" line in the final confirmation.

## Terminal State

When the user approves the design direction, the skill is complete. Do NOT:
- Write a design document
- Save any file
- Invoke any other skill
- Start implementation

Simply confirm the agreed-upon direction and wait for the user's next instruction.

## Verification

After applying explore-then-ask:

- [ ] The user confirmed the intent is clear before design began
- [ ] An explicit context hypothesis with a confidence number was stated
- [ ] Assumptions were surfaced and corrected before design questions began
- [ ] Design questions were asked one at a time, each with a guess attached
- [ ] Real constraints were probed when answers sounded like convention or best practice
- [ ] 2-3 approaches were sketched with trade-offs before detailed design
- [ ] Design sections were presented incrementally with approval after each
- [ ] The final confirmation included "Out of scope"
- [ ] The user confirmed with an explicit yes
