---
name: explore-then-ask
description: Explore project context and clarify requirements through structured dialogue. A self-contained behavioral skill for context-first design clarification — no docs, no browser, no handoff.
---

# Explore Then Ask

## Overview

Turn vague ideas into clarified designs through natural collaborative dialogue.

Start by understanding the current project context, then ask questions one at a time to refine the idea. Once you understand what you're building, present 2-3 approaches with trade-offs, then present the design in sections and get user approval.

This skill does NOT write documents, invoke other skills, or hand off to implementation. It ends when the user approves the design direction.

<HARD-GATE>
Do NOT invoke any implementation skill, write any code, scaffold any project, or take any implementation action. Do NOT save files or write design docs. This is a dialogue-only skill.
</HARD-GATE>

<IMPORTANT>
- You must use chinese to ask question
- You must use chinese to present design and trade-offs
</IMPORTANT>

## Anti-Pattern: "This Is Too Simple To Need A Design"

Every project goes through this process. A todo list, a single-function utility, a config change — all of them. "Simple" projects are where unexamined assumptions cause the most wasted work. The design can be short (a few sentences for truly simple projects), but you MUST present it and get approval.

## Checklist

Complete these in order:

1. **Explore project context** — check files, docs, recent commits
2. **Ask clarifying questions** — one at a time, understand purpose/constraints/success criteria
3. **Propose 2-3 approaches** — with trade-offs and your recommendation
4. **Present design** — in sections scaled to their complexity, get user approval after each section

## Process Flow

```
Explore project context
        |
        v
Ask clarifying questions (one at a time)
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
   DONE (no handoff, no doc, no skill invocation)
```

## The Process

### 1. Explore Project Context

Check out the current project state first (files, docs, recent commits).

- Do this silently — don't dump file listings unless something is unclear
- Before asking detailed questions, assess scope: if the request describes multiple independent subsystems, flag this immediately and help decompose
- If the project is too large, help the user decompose into sub-projects, then explore-and-clarify the first one

**Surface assumptions immediately** after exploring:

```
我的假设：
1. ...
2. ...
→ 有不对的地方请现在纠正，否则我将基于这些假设继续。
```

### 2. Ask Clarifying Questions

Ask questions **one at a time** to refine the idea.

- Prefer multiple choice questions when possible
- Only one question per message — if a topic needs more exploration, break it into multiple questions
- Focus on understanding: purpose, constraints, success criteria
- Continue until requirements are concrete

### 3. Propose 2-3 Approaches

Once you understand what you're building, propose different approaches with trade-offs.

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

When the user approves the design, the skill is complete. Do NOT:
- Write a design document
- Save any file
- Invoke any other skill
- Start implementation

Simply confirm the agreed-upon direction and wait for the user's next instruction.

## Key Principles

- **Context first** — Always read before asking
- **One question at a time** — Don't overwhelm
- **Multiple choice preferred** — Easier to answer than open-ended
- **YAGNI ruthlessly** — Remove unnecessary features from all designs
- **Explore alternatives** — Always propose 2-3 approaches before settling
- **Incremental validation** — Present design, get approval before moving on
- **Be flexible** — Go back and clarify when something doesn't make sense

