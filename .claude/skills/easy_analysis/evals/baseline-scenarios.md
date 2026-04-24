# Easy-Analysis Baseline Pressure Scenarios

## Purpose

Run these WITHOUT the easy-analysis skill loaded to document baseline failures.
These scenarios test whether agents naturally skip macro overview, skip translations, or violate the paragraph-by-paragraph requirement.

## Scenario 1: Time Pressure (Short Document)

**Prompt:**
"快速分析一下这个短文档：/Users/carlyu/soft/projects/ys-powers/.claude/skills/condition-based-waiting/SKILL.md。不用太详细，告诉我关键点就行。"

**Expected Failure:**
- Agent skips macro overview entirely ("short document, no need")
- Jumps straight to summary or key points
- Does NOT translate paragraph by paragraph

**What to Document:**
- Exact rationalization used
- Whether Step 0 (macro) was produced
- Whether paragraphs were translated individually

## Scenario 2: Scope Ambiguity (No Explicit "Paragraph-by-Paragraph")

**Prompt:**
"帮我理解一下这个文档在说什么：/Users/carlyu/soft/projects/ys-powers/.claude/skills/brainstorming/SKILL.md"

**Expected Failure:**
- Agent provides a high-level summary only
- Does NOT break down by paragraph
- Does NOT provide translations
- Treats it as a "explain this" request, not "analyze deeply"

**What to Document:**
- Output structure (summary vs paragraph blocks)
- Presence/absence of translations
- Whether structure matches "Original → Translation → Key Points"

## Scenario 3: Replication Pressure (Skip to Details)

**Prompt:**
"我要复刻这个 skill 的功能。详细分析一下 /Users/carlyu/soft/projects/ys-powers/.claude/skills/systematic-debugging/SKILL.md，我要知道每个部分怎么实现的。"

**Expected Failure:**
- Agent focuses on implementation details immediately
- Skips macro overview ("I need details for replication")
- May mix paragraphs together to "save time"
- Might skip "Key Points" section, jumping straight to code analysis

**What to Document:**
- Whether macro overview came FIRST
- Whether each paragraph was processed individually
- Whether format was strictly followed under "replication" pressure

## Scenario 4: Combined Pressure (Exhaustion + Sunk Cost)

**Prompt:**
"Analyze this document for me: /Users/carlyu/soft/projects/ys-powers/.claude/skills/test-driven-development/SKILL.md. I've read it once but didn't really get it. Just give me the important parts."

**Expected Failure:**
- Agent interprets "important parts" as excuse to skip translation
- Might produce a condensed summary
- Skips Step 0 because user "already read it once"
- Rationalization: "User wants highlights, not full analysis"

**What to Document:**
- Whether agent produced macro overview despite user saying they "already read it"
- Whether translation was skipped for "already understood" sections
