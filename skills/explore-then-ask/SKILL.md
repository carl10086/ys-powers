---
name: explore-then-ask
description: Explore project context and turn confirmed requirements into an approved design through structured dialogue — propose approaches with trade-offs, present design sections. No requirement re-clarification; no implementation handoff. May write to a user-specified document path.
---

# Explore Then Ask

## Overview

Turn confirmed requirements into an approved design through natural collaborative dialogue.

Start from a confirmed intent (typically produced by `/clarify-intent`). Understand the current project context, propose 2-3 approaches with trade-offs, then present the design in sections and get user approval.

需求还没确认（要什么、为什么、验收标准不清楚）→ 停止并告知用户：需求未确认，请先运行 `/clarify-intent`。

This skill is primarily dialogue-based. It does NOT invoke other skills or hand off to implementation. It ends when the user approves the design direction. Writing to a user-specified document path is the only allowed file-writing case.

<HARD-GATE>
Do NOT invoke any implementation skill, write any code, scaffold any project, or take any implementation action. This is a primarily dialogue-based skill.

**Exception — user-specified document path**: if the user explicitly tells you where to write (a concrete file path), you MAY write the agreed-upon design there. Do not invent paths on your own; if unclear, confirm before writing.
</HARD-GATE>

<IMPORTANT>
- You must use chinese to ask question
- You must use chinese to present design and trade-offs
</IMPORTANT>

## Anti-Pattern: "This Is Too Simple To Need A Design"

Every project goes through this process. A todo list, a single-function utility, a config change — all of them. "Simple" projects are where unexamined assumptions cause the most wasted work. The design can be short (a few sentences for truly simple projects), but you MUST present it and get approval.

## Checklist

Complete these in order:

1. **Search Historical SOPs** — use sop-search to check for relevant historical experience
   - Match found → read relevant SOPs and incorporate into context
   - No match → continue
2. **Explore project context** — check files, docs, recent commits
   - If `CONTEXT.md` exists at the project root, read it for established domain terminology
   - If `docs/adr/` exists, scan recent ADRs to respect prior architectural decisions
3. **Propose 2-3 approaches** — with trade-offs and your recommendation
4. **Present design** — in sections scaled to their complexity, get user approval after each section

## Process Flow

```
Search Historical SOPs
        |
        v
Explore project context
        |
        v
Propose 2-3 approaches (with trade-offs)
        |
        v
Present design sections (get approval per section)
        |
        v
User approves design? ---no--> revise
        | yes
        v
   DONE (no handoff, no skill invocation)
   [user-specified doc path? -> write there, else just confirm]
```

## The Process

### 1. Search Historical SOPs

Before exploring project context, always search for relevant historical SOPs first.

- Use `sop-search` to find past experiences related to the current task
- If matching SOPs exist, read them and incorporate key decisions and pseudo-code steps into your context
- If no matching SOPs exist, proceed normally — this establishes the habit of checking history first

This step is unconditional. Even if the project has few SOPs, executing this query builds muscle memory for knowledge reuse.

### 2. Explore Project Context

Check out the current project state (files, docs, recent commits), incorporating any SOP insights discovered in Step 1.

- Do this silently — don't dump file listings unless something is unclear
- Before proposing approaches, assess scope: if the request describes multiple independent subsystems, flag this immediately and help decompose
- If the project is too large, help the user decompose into sub-projects, then explore-and-design the first one

**Surface assumptions immediately** after exploring:

```
我的假设：
1. ...
2. ...
→ 有不对的地方请现在纠正，否则我将基于这些假设继续。
```

### 3. Propose 2-3 Approaches

Based on the confirmed requirements, propose different approaches with trade-offs.

- Present options conversationally with your recommendation and reasoning
- Lead with your recommended option and explain why
- Be ready to go back and clarify if something doesn't make sense

### 4. Present Design

Present the design in sections scaled to complexity.

- Ask after each section whether it looks right so far
- Cover: architecture, components, data flow, error handling, testing
- Scale each section: a few sentences if straightforward, up to 200-300 words if nuanced
- Be ready to go back and clarify

**Design for isolation and clarity:**
- Break the system into smaller units that each have one clear purpose
- For each unit: what does it do, how do you use it, what does it depend on?
- Can someone understand what a unit does without reading its internals?
- Can you change the internals without breaking consumers?

**Working in existing codebases:**
- Explore the current structure before proposing changes. Follow existing patterns.
- Include targeted improvements only if they serve the current goal
- Don't propose unrelated refactoring

## Terminal State

When the user approves the design, the skill is complete.

- **Default**: simply confirm the agreed-upon direction and wait for the user's next instruction.
- **User-specified path**: if the user has explicitly named a target document path during the dialogue, write the agreed design to that path before concluding. Do not pick paths yourself.

In all cases, do NOT:
- Invoke any other skill
- Start implementation

## Key Principles

- **Context first** — Always read before asking
- **One question at a time** — Don't overwhelm
- **Multiple choice preferred** — Easier to answer than open-ended
- **YAGNI ruthlessly** — Remove unnecessary features from all designs
- **Explore alternatives** — Always propose 2-3 approaches before settling
- **Incremental validation** — Present design, get approval before moving on
- **Be flexible** — Go back and clarify when something doesn't make sense

