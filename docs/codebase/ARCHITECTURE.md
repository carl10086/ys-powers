# ys-powers Architecture

> Prescriptive architecture guide for future developers working on the ys-powers project.
> Last updated: 2026-04-23

---

## Pattern Overview

Use a **Layered Capability Model** with progressive specificity:

- **Rules layer** (`rules/`) — Universal behavioral constraints applied to all coding activities
- **Skills layer** (`skills/`) — Reusable workflow patterns for specific problem domains
- **Commands layer** (`commands/`) — Executable playbooks for concrete tasks

This three-tier model ensures constraints apply broadly, workflows are discoverable, and actions are prescriptive. Each layer builds on the one below without circular dependencies.

---

## Layers

### Layer 1: Rules (`rules/`)

**Responsibility:** Define universal coding behavior that applies regardless of context.

**Key files:**
- `rules/code.md` — Core behavioral guidelines: Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution, Code Smells catalog

**Constraints:**
- Keep rules technology-agnostic
- Use five-tier constraint system: `<CRITICAL>`, `<NEVER>`, `<IMPORTANT>`, `<Do NOT>`, `Avoid`
- Rules must be enforceable through observation (not subjective judgment)

**Where to add new rules:**
- Add to `rules/code.md` if it applies to all coding activities
- Create new file in `rules/` only for domain-specific constraints (e.g., `rules/security.md`)

### Layer 2: Skills (`skills/`)

**Responsibility:** Provide structured, tested workflow patterns for recurring problem types.

**Directory structure per skill:**
```
skills/<skill-name>/
  SKILL.md              # Required — main reference with YAML frontmatter
  supporting-file.*     # Optional — scripts, references, templates
```

**Key files:**
- `skills/explore-then-ask/SKILL.md` — Context-first requirement clarification and design confirmation
- `skills/spec-driven-development/SKILL.md` — Structured spec workflow before implementation
- `skills/test-driven-development/SKILL.md` — RED-GREEN-REFACTOR cycle with Iron Law
- `skills/systematic-debugging/SKILL.md` — Four-phase debugging process (Root Cause → Pattern Analysis → Hypothesis → Implementation)
- `skills/subagent-driven-development/SKILL.md` — Fresh-subagent-per-task execution with two-stage review
- `skills/writing-great-skills/SKILL.md` — Predictable skills/commands via invocation, hierarchy, and pruning
- `skills/writing-plans/SKILL.md` — Bite-sized implementation plans with exact file paths and commands
- `skills/using-git-worktrees/SKILL.md` — Isolated workspace creation with safety verification
- `skills/verification-before-completion/SKILL.md` — Evidence-before-claims verification gate
- `skills/executing-plans/SKILL.md` — Plan execution in separate sessions with review checkpoints
- `skills/requesting-code-review/SKILL.md` — Dispatch reviewer subagent with git SHAs
- `skills/receiving-code-review/SKILL.md` — Technical evaluation of feedback without performative agreement
- `skills/find-bugs/SKILL.md` — TypeScript + Bun debugging workflow with pseudo-code communication
- `skills/easy_analysis/SKILL.md` — Paragraph-by-paragraph document analysis for non-native English speakers
- `skills/map-codebase/SKILL.md` — Codebase structure analysis with prescriptive ARCHITECTURE.md generation

**SKILL.md requirements:**
- YAML frontmatter with `name` (kebab-case, max 64 chars) and `description` (max 1024 chars, third-person, trigger-focused)
- Description MUST start with "Use when..." and describe triggering conditions only (never summarize workflow)
- Body under 500 lines; split heavy reference into separate files
- Include: Overview, When to Use, Core Pattern, Common Mistakes, Red Flags
- Use cross-references instead of duplicating content from other skills

**Where to add new skills:**
- Create directory `skills/<kebab-case-name>/`
- Use `skills/writing-great-skills/SKILL.md` for authoring: predictable trigger, information hierarchy, progressive disclosure, and pruning
- Add supporting references only when they are heavy or branch-specific
- For discipline-enforcing skills, verify pressure scenarios before rollout

### Layer 3: Commands (`commands/`)

**Responsibility:** Provide executable playbooks for specific operational tasks.

**Key files:**
- `commands/gc.md` — Git workflow: branch naming, commitizen format, PR creation
- `commands/refactor.md` — Refactoring playbook: gated design phase, TDD execution, code smell identification
- `commands/sop-add.md` — SOP generation from session history with YAML metadata
- `commands/teach-code.md` — Code teaching: macro-to-micro explanation with interactive checkpoints

**Command structure:**
- YAML frontmatter with `name` and `description`
- HARD-GATE blocks for preconditions
- Step-by-step workflow with exact commands
- Self-checklist for verification

**Where to add new commands:**
- Create file `commands/<kebab-case-name>.md`
- Include YAML frontmatter and structured workflow
- Commands should reference skills, not duplicate their content

### Layer 4: Installation (`install/`)

**Responsibility:** Deploy source layers to target projects.

**Key files:**
- `install/local-install.py` — Python deployment script with two copy strategies

**Copy strategies:**
- `folder` — Folder-level full replacement (for `skills/`): remove target item, copy source item
- `file` — File-level incremental overlay (for `rules/`, `commands/`): `shutil.copytree(dirs_exist_ok=True)`

**Where to modify:**
- Update `DIRECTORIES` dict in `install/local-install.py` to add new source directories
- Ensure strategy choice matches intended override behavior

### Layer 5: Documentation (`docs/`)

**Responsibility:** Capture design decisions, implementation plans, and architecture.

**Key directories:**
- `docs/codebase/` — Architecture documentation (this file)
- `docs/superpowers/specs/` — Design specifications, named `YYYY-MM-DD-<topic>-design.md`
- `docs/superpowers/plans/` — Implementation plans, named `YYYY-MM-DD-<feature-name>.md`

**Where to add new documentation:**
- Design specs go to `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`
- Implementation plans go to `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`
- Architecture updates modify `docs/codebase/ARCHITECTURE.md`

### Layer 6: SOP (`sop/`)

**Responsibility:** Store runtime-generated standard operating procedures from session history.

**Key files:**
- `sop/sop-YYYYMMDD-NNN-<keyword>.md` — Generated SOP documents with YAML metadata

**Where to add new SOPs:**
- Generated automatically via `commands/sop-add.md` workflow
- Manual creation follows same naming convention: `sop-YYYYMMDD-NNN-<keyword>.md`

---

## Data Flow

### Installation Flow

```
User executes: python install/local-install.py
    |
    v
get_project_root() resolves via __file__ → script parent parent
    |
    v
Iterate DIRECTORIES configuration:
    skills/  → .claude/skills/   (folder strategy: full replacement)
    rules/   → .claude/rules/    (file strategy: incremental overlay)
    commands/→ .claude/commands/ (file strategy: incremental overlay)
    |
    v
Output success/failure per directory with statistics
```

Use `folder` strategy when source owns the entire namespace (skills are self-contained). Use `file` strategy when target may contain user-added files that must be preserved.

### Skill Discovery Flow

```
Claude encounters problem
    |
    v
Read all SKILL.md YAML frontmatter (name + description)
    |
    v
Match description to current task triggers
    |
    v
Load matching SKILL.md body
    |
    v
Follow workflow steps, load supporting files on demand
```

**Critical for skill authors:** Description determines discovery. Write descriptions that answer "Should I read this skill right now?" not "What does this skill do?"

### Development Workflow Flow

```
New feature or change
    |
    v
Run /spec
    ├── Invoke skills/explore-then-ask/SKILL.md for context-first clarification
    ├── Optionally invoke skills/domain-modeling/SKILL.md for domain terms / ADRs
    └── Invoke skills/spec-driven-development/SKILL.md to write a structured spec
    |
    v
Run /ys-plan
    ├── Read spec
    ├── Map file structure
    ├── Decompose into dependency-ordered tasks with acceptance criteria
    └── Write plan to docs/ys-powers/plans/YYYY-MM-DD-<feature-name>.md
    |
    v
Use skills/subagent-driven-development/SKILL.md OR skills/executing-plans/SKILL.md
    ├── Set up git worktree (skills/using-git-worktrees/SKILL.md)
    ├── Per task: dispatch implementer subagent
    ├── Two-stage review: spec compliance → code quality
    └── Mark complete, proceed to next task
    |
    v
Use skills/verification-before-completion/SKILL.md
    ├── Run verification commands
    ├── Read output, confirm claims
    └── Only then claim completion
```

### Debugging Flow

```
Bug or unexpected behavior
    |
    v
Use skills/systematic-debugging/SKILL.md
    ├── Phase 1: Root Cause Investigation
    │   ├── Read error messages completely
    │   ├── Reproduce consistently
    │   ├── Check recent changes (git diff)
    │   └── Gather evidence at component boundaries
    ├── Phase 2: Pattern Analysis
    │   ├── Find working examples
    │   ├── Read reference implementations fully
    │   └── Identify differences
    ├── Phase 3: Hypothesis and Testing
    │   ├── Form single hypothesis
    │   ├── Test minimally (one variable)
    │   └── Verify before continuing
    └── Phase 4: Implementation
        ├── Create failing test (skills/test-driven-development/SKILL.md)
        ├── Implement single fix
        └── Verify fix
```

---

## Key Abstractions

### Five-Tier Constraint System

Use in rules and skills to express obligation strength:

| Tier | Usage | Example |
|------|-------|---------|
| `<CRITICAL>` | Security, data loss prevention | Never force push to main |
| `<NEVER>` | Absolute prohibitions | Never skip conflict resolution |
| `<IMPORTANT>` | Strong recommendations with consequences | Use Chinese for skill content |
| `<Do NOT>` | Specific actions to avoid | Do not hardcode paths |
| `Avoid` | Discouraged patterns | Avoid Windows-style paths |

### HARD-GATE

A block in documentation that unconditionally stops execution until a condition is met. Use for preconditions that must be satisfied before any implementation work.

Example from `commands/refactor.md`:
```markdown
<HARD-GATE>
Do not edit files until a concrete refactoring plan has been presented and approved.
</HARD-GATE>
```

### RED-GREEN-REFACTOR

The universal improvement cycle applied to both code and documentation:

- **RED**: Establish baseline by observing failure (write failing test / watch agent violate rule)
- **GREEN**: Make minimal change to pass (implement code / write skill addressing specific failure)
- **REFACTOR**: Improve while maintaining correctness (clean code / close loopholes)

Use this cycle for: code changes (`skills/test-driven-development`), discipline-enforcing skill pressure tests (`skills/writing-skills/testing-skills-with-subagents.md`), debugging fixes (`skills/systematic-debugging`).

### Claude Search Optimization (CSO)

Techniques to ensure skills are discoverable by future Claude instances:

1. **Rich description field**: Trigger conditions only, no workflow summaries
2. **Keyword coverage**: Error messages, symptoms, tools, synonyms
3. **Descriptive naming**: Active voice, verb-first, gerund form (`creating-skills` not `skill-creation`)
4. **Token efficiency**: Getting-started workflows <150 words, frequently-loaded skills <200 words, others <500 words

### Subagent Dispatch Pattern

For complex tasks, delegate to fresh subagents with isolated context:

- **Implementer subagent**: Executes one task, asks questions, self-reviews
- **Spec reviewer subagent**: Verifies implementation matches specification
- **Code quality reviewer subagent**: Evaluates code quality, identifies issues
- **Controller (you)**: Orchestrates flow, answers questions, handles blockers

Use `skills/subagent-driven-development/SKILL.md` for same-session execution. Use prompt templates in `skills/subagent-driven-development/implementer-prompt.md`, `spec-reviewer-prompt.md`, and `code-quality-reviewer-prompt.md`.

### Progressive Disclosure

Structure skills so Claude loads only what it needs:

- SKILL.md = overview + navigation (loaded when skill triggers)
- Supporting files = detailed reference (loaded on demand)
- Scripts = executable tools (executed, not loaded into context)

Keep all references one level deep from SKILL.md. Never nest references: `SKILL.md → advanced.md → details.md` is forbidden.

---

## Entry Points

### For End Users

| Entry Point | File | Purpose |
|-------------|------|---------|
| Installation | `install/local-install.py` | Deploy ys-powers to target project's `.claude/` directory |
| Project README | `README.md` | Installation instructions and usage overview |

### For Skill Authors

| Entry Point | File | Purpose |
|-------------|------|---------|
| Skill/command authoring guide | `skills/writing-great-skills/SKILL.md` | How to design predictable skills and commands |
| Authoring glossary | `skills/writing-great-skills/GLOSSARY.md` | Shared vocabulary for invocation, hierarchy, and pruning |
| Legacy skill testing guide | `skills/writing-skills/testing-skills-with-subagents.md` | Heavy RED-GREEN-REFACTOR pressure testing for discipline skills |
| Legacy Anthropic best practices | `skills/writing-skills/anthropic-best-practices.md` | Upstream reference, loaded only when needed |

### For Developers Using Skills

| Entry Point | File | Purpose |
|-------------|------|---------|
| Spec phase | `commands/spec.md` | Clarify requirements and write the structured spec |
| Planning phase | `commands/ys-plan.md` | After spec, before code |
| Execution phase | `skills/subagent-driven-development/SKILL.md` | Same-session task execution |
| Alternative execution | `skills/executing-plans/SKILL.md` | Separate-session execution |
| Debugging | `skills/systematic-debugging/SKILL.md` | Any bug or unexpected behavior |
| TDD | `skills/test-driven-development/SKILL.md` | Any feature or bugfix |

### For System Maintenance

| Entry Point | File | Purpose |
|-------------|------|---------|
| Architecture docs | `docs/codebase/ARCHITECTURE.md` | This file — project structure and conventions |
| Design specs | `docs/superpowers/specs/*.md` | Historical design decisions |
| Implementation plans | `docs/superpowers/plans/*.md` | Historical execution plans |
| SOP records | `sop/*.md` | Session-derived operational knowledge |

---

## Error Handling

### In Skills

Use structured error prevention rather than exception handling:

1. **Red Flags sections**: List specific thoughts or actions that indicate process violation. Example from `skills/test-driven-development/SKILL.md`:
   ```markdown
   ## Red Flags - STOP and Start Over
   - Code before test
   - Test passes immediately
   - "I'll write tests after"
   ```

2. **Rationalization tables**: Capture common excuses and their counter-arguments. Example from `skills/systematic-debugging/SKILL.md`:
   ```markdown
   | Excuse | Reality |
   |--------|---------|
   | "Issue is simple, don't need process" | Simple issues have root causes too |
   ```

3. **HARD-GATE blocks**: Unconditional stops for preconditions.

### In Installation Script

`install/local-install.py` handles errors per directory:

- **PermissionError**: Print to stderr, return False, continue to next directory
- **Source directory missing**: Print warning, return False, continue
- **Unknown strategy**: Print error to stderr, return False
- **Total failure**: Exit with code 1 if all directories fail

Use try/except per directory so one failure doesn't block others.

### In Documentation

Never write "TBD", "TODO", "implement later", or "add appropriate error handling". Every step must contain actual content. Placeholders are documentation failures.

---

## Cross-Cutting Concerns

### Language Policy

**All new skills SHOULD be written in Chinese (简体中文).** This convention is enforced by `/wskill` and reviewed against `skills/writing-great-skills/SKILL.md`.

What MUST be Chinese:
- Overview, usage conditions, core patterns, all explanations
- Code comments and example descriptions
- Flowchart labels and diagram text
- Error examples and correct examples

What MAY remain in English:
- Technical terms (API names, library names, CLI commands)
- File paths and directory names
- Code identifiers (variable names, function names)

Existing skills in English (e.g., `find-bugs`) are grandfathered but new skills must follow this policy.

### Authoring Discipline

For skills and commands, optimize for predictability first:
- trigger-focused description
- one source of truth per idea
- information hierarchy before adding reference files
- no-op pruning before shipping

Use heavy RED-GREEN-REFACTOR pressure testing only for discipline-enforcing skills where agents have an incentive to bypass the rule.

### Verification Culture

Before claiming completion:
1. Identify the verification command
2. Run it fresh (not from memory)
3. Read full output
4. Confirm claim matches evidence
5. Only then make the claim

Use `skills/verification-before-completion/SKILL.md` for all completion claims.

### Git Hygiene

Use `commands/gc.md` for all git operations:
- Branch naming: `{prefix}{description-MMdd}` (e.g., `feature/auth-0414`)
- Commit format: `type(scope): description` (≤50 chars, verb-first)
- Types: feat, fix, refactor, docs, style, test, chore
- Never force push to main/master
- Never commit secrets

### Security

- `.env` files: Record existence only, never read contents
- `credentials.*`, `secrets.*`, `*.pem`, `*.key`: Record existence only
- `.npmrc`, `.pypirc`: Record existence only (may contain auth tokens)
- Never commit secrets, tokens, or credentials

---

## Where to Add New Code

### New Skill

1. Create directory: `skills/<kebab-case-name>/`
2. Write `skills/<kebab-case-name>/SKILL.md` with YAML frontmatter
3. Add supporting files in same directory if needed
4. Review against `skills/writing-great-skills/SKILL.md`; add pressure scenarios only for discipline-enforcing skills
5. Run `python install/local-install.py` to deploy
6. Update this ARCHITECTURE.md to include the new skill

### New Command

1. Create file: `commands/<kebab-case-name>.md`
2. Include YAML frontmatter with `name` and `description`
3. Structure: HARD-GATE (if needed) → Workflow → Examples → Checklist
4. Run `python install/local-install.py` to deploy (uses file strategy)

### New Rule

1. Create or modify file in `rules/`
2. Use five-tier constraint system
3. Run `python install/local-install.py` to deploy (uses file strategy)

### New Design Spec

1. Write to `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`
2. Include: Overview, Requirements, Technical Design, Error Handling, Usage Examples
3. Commit to git

### New Implementation Plan

1. Write to `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`
2. Must start with plan header (see `skills/writing-plans/SKILL.md`)
3. Include exact file paths, complete code, exact commands with expected output
4. No placeholders allowed

### New SOP

1. Use `commands/sop-add.md` workflow, or
2. Manual creation: `sop/sop-YYYYMMDD-NNN-<keyword>.md`
3. Include YAML frontmatter: title, created, tags, project, summary
4. Structure: Background → Solution (pseudo-code steps, key files, key commands, key decisions)

### Installation Script Changes

1. Modify `install/local-install.py`
2. Update `DIRECTORIES` dict for new source directories
3. Choose strategy: `folder` for namespace ownership, `file` for incremental overlay
4. Test by running against a clean target directory

---

## File Reference Quick List

| File | Purpose |
|------|---------|
| `install/local-install.py` | Deployment script with two copy strategies |
| `rules/code.md` | Universal coding behavior constraints |
| `commands/gc.md` | Git workflow command |
| `commands/refactor.md` | Refactoring command |
| `commands/sop-add.md` | SOP generation command |
| `commands/teach-code.md` | Code teaching command |
| `skills/explore-then-ask/SKILL.md` | Context-first requirement clarification |
| `skills/spec-driven-development/SKILL.md` | Structured spec authoring |
| `skills/planning-and-task-breakdown/SKILL.md` | Implementation plan authoring |
| `skills/subagent-driven-development/SKILL.md` | Task execution with subagents |
| `skills/test-driven-development/SKILL.md` | TDD for code |
| `skills/systematic-debugging/SKILL.md` | Four-phase debugging |
| `skills/writing-great-skills/SKILL.md` | Skill/command authoring via predictability and pruning |
| `skills/verification-before-completion/SKILL.md` | Evidence-before-claims verification |
| `skills/using-git-worktrees/SKILL.md` | Isolated workspace setup |
| `skills/executing-plans/SKILL.md` | Plan execution in separate sessions |
| `skills/requesting-code-review/SKILL.md` | Code review dispatch |
| `skills/receiving-code-review/SKILL.md` | Feedback evaluation |
| `skills/find-bugs/SKILL.md` | TypeScript + Bun debugging |
| `skills/easy_analysis/SKILL.md` | Document analysis for non-native speakers |
| `skills/map-codebase/SKILL.md` | Architecture documentation generation |
| `docs/codebase/ARCHITECTURE.md` | This file |
