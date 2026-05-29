---
description: Write a new skill — run explore-then-ask to clarify requirements, then invoke writing-skills to create the skill
---

## Phase 1: Explore and Clarify

Invoke the **explore-then-ask** skill to clarify the skill requirements one question at a time (in Chinese):

1. **Skill type**: Technique, pattern, reference, or discipline-enforcing?
2. **Triggering conditions**: What symptoms or situations should load this skill?
3. **Scope**: What problem does it solve? What is it NOT for?
4. **Existing skills**: Overlap with existing skills? Extend or replace?

Follow explore-then-ask's full flow: surface assumptions, propose 2-3 approaches with trade-offs, present design sections, and get user approval.

## Phase 2: Write Skill

**Before writing, read `skills/writing-skills/anthropic-best-practices.md` for mandatory authoring constraints.**

Invoke the **writing-skills** skill to run the RED-GREEN-REFACTOR cycle:

1. **RED** — Create pressure scenarios, run WITHOUT the skill, document baseline behavior
2. **GREEN** — Write minimal `SKILL.md` addressing the baseline failures, run WITH the skill
3. **REFACTOR** — Close loopholes, add red flags, re-test until bulletproof

## Phase 3: Verify Checklist

Before finishing, confirm every item below:

- [ ] **Read `skills/writing-skills/anthropic-best-practices.md`** — All constraints reviewed (naming, description format, gerund naming, progressive disclosure, token limits, CSO rules)
- [ ] **Content language** — Skill body is in Chinese; technical terms, code identifiers, file paths, and command names remain in English
- [ ] **YAML frontmatter** — `name` (kebab-case, ≤64 chars) and `description` (starts with "Use when...", third person, ≤1024 chars) are correct
- [ ] **SKILL.md body ≤ 500 lines** — If exceeded, split into separate files using progressive disclosure
- [ ] **RED phase completed** — Baseline behavior documented with specific rationalizations/failures
- [ ] **GREEN phase completed** — Skill addresses baseline failures; agent complies with skill present
- [ ] **REFACTOR phase completed** — Loopholes closed, rationalization table built, re-tested
- [ ] **Saved to correct path** — `.claude/skills/<skill-name>/SKILL.md` (kebab-case)

<IMPORTANT>
- Write all skill content in Chinese. Keep technical terms, code identifiers, file paths, and command names in English.
- Save the skill to `.claude/skills/<skill-name>/SKILL.md` where `<skill-name>` is kebab-case.
- If supporting files needed, place them in `.claude/skills/<skill-name>/`.
- Confirm the file path with the user before saving.
</IMPORTANT>
