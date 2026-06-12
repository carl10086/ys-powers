---
description: Write a new command — run explore-then-ask to clarify requirements, then invoke RED-GREEN-REFACTOR to create the command
---

<IMPORTANT>
- Write all command content in Chinese; keep technical terms, code identifiers, file paths, and command names in English
- Save the command to `commands/<command-name>.md` where `<command-name>` is kebab-case
- Use TodoWrite to create todos for EACH checklist item below
- Before drafting, read `references/anthropic-best-practices.md` for prompt authoring constraints
</IMPORTANT>

## Phase 1: Explore and Clarify

Invoke the **explore-then-ask** skill to clarify the command requirements one question at a time (in Chinese):

1. **Triggering conditions**: What user situation or request should load this command?
2. **Scope**: What problem does it solve? What is it NOT for?
3. **Existing commands**: Overlap with existing commands in `commands/`? Extend or replace?
4. **Invoked skills**: Which skills does this command call?

Follow explore-then-ask's full flow: search historical SOPs, explore project context, surface assumptions, ask clarifying questions one at a time, propose 2-3 approaches with trade-offs, present design sections, and get user approval.

## Phase 2: Write Command

**Before writing, you MUST read `references/anthropic-best-practices.md` for prompt authoring constraints.**

Also read `CLAUDE.md` for project-level command conventions and skim existing `commands/*.md` for style patterns.

Identify the command type to focus your RED/GREEN verification:
- **Workflow command** (e.g., `gc`, `ship`): orchestrates a sequence of steps. Verify step completeness and order.
- **Discipline command** (e.g., `wcommand` itself): enforces a rule or process. Verify the agent cannot bypass it.
- **Utility command** (e.g., `html`): invokes a tool or script. Verify input/output and error handling.

Run the RED-GREEN-REFACTOR cycle for command creation:

### Command frontmatter

Claude Code commands support the following YAML fields:

- `description` (required): Trigger scenario. Borrow the skill CSO guideline: describe when to invoke, not what steps the command performs.
- `argument-hint` (optional): Hint shown to the user for command arguments, e.g., `[file]`.
- `allowed-tools` (optional): Restrict which tools the command may use, e.g., `Bash(node:*), Read`.
- `disable-model-invocation` (optional, default `false`): Set to `true` if the command should only be invoked manually, not programmatically by the model.

Example:
```yaml
---
description: Use when committing code and pushing to remote with a generated message and user confirmation
argument-hint: [optional-commit-message]
---
```

### RED — Baseline: Run Without Command

**Iron Law for command creation: NO COMMAND WITHOUT A FAILING BASELINE FIRST.**

Run at least **2 scenarios** before writing the command:
- **Primary scenario**: the most common happy path
- **Boundary scenario**: missing input, ambiguous request, user interrupts, extra arguments provided, user asks to skip a step, or the task is partially complete

For each scenario:

1. Agree on the scenario with the user
2. **Do not explicitly invoke** the target command (or any overlapping existing command) during the baseline run
3. Let the agent execute the task directly
4. **Record the agent's actual execution sequence step by step**
5. Document friction points and trace each one to the specific baseline step that caused it:

Use the first table to capture the full execution sequence; use the second table to analyze only the steps marked with friction.

| Step # | Agent action | Result | Friction? |
|--------|--------------|--------|-----------|
| 1 | ... | ... | ... |
| 2 | ... | ... | ... |

| Friction type | Description | Caused by step # |
|---------------|-------------|------------------|
| Missing step | ... | Step 3 |
| Wrong order | ... | Step 2 |
| Redundant work | ... | Step 1 |
| Inconsistent with team workflow | ... | Step 4 |
| Scope creep | ... | Step 5 |

### GREEN — Write Minimal Command and Trial Run

1. Write the minimal command addressing the **specific baseline failures** documented in RED. Do not add extra content for hypothetical cases.
2. **Trial run**: Load the command and run **the same scenarios** against it (primary + boundary)
3. Verify:
   - [ ] Flow reaches the end without getting stuck
   - [ ] No missing steps
   - [ ] Referenced skills / tools exist and paths are correct
   - [ ] The user's original request is fully resolved

### REFACTOR — Close Execution Gaps

If the trial run reveals new friction, fix and re-run. Do not stop at the first passing run.

**Command red flags — stop and fix if you see any:**

- Agent skips a step even when the command lists it
- Agent asks the user a question that the command should have answered
- Agent invokes a different command or skill than the one specified
- Agent performs extra work outside the command scope
- Trial run results differ between scenarios
- Same scenario produces different results on re-run

| Issue | Fix |
|-------|-----|
| Missing step | Insert at correct position |
| Wrong order | Reorder steps |
| Ambiguity | Add explicit connectives ("must X before Y", "if A then B, otherwise C") |
| Overlap with existing command | Narrow scope or merge |
| Stuck execution | Check referenced skill / file paths |

Build and update a rationalization table from all test iterations:

| Rationalization observed | Why it fails | Counter added to command |
|--------------------------|--------------|--------------------------|
| "This is too simple to need a trial run" | Untested commands break in production | Added Iron Law + trial run requirement |
| "I'll add this just in case" | Scope creep, bloat | "Do not add extra content for hypothetical cases" |
| "The user can figure out this step" | Missing step, friction | Added explicit step |

Loop: Fix → re-run → until the command produces consistent results across all documented scenarios.

### Anti-Patterns

Avoid these common mistakes when drafting the command:

#### One command does everything
A command should solve one workflow. If it needs more than one high-level goal, split it.

#### Copy an existing command without changing the description
Every command must have a unique trigger. If you copy structure from an existing command, rewrite the `description` to match the new scope.

#### Steps that cannot be executed
Do not reference skills, tools, or files that do not exist. Verify every reference during the GREEN trial run.

#### No trial run
A command without a trial run is a draft, not a finished command.

## STOP: Before Finishing

**After writing ANY command, you MUST STOP and complete the verification process.**

**Do NOT:**
- Create multiple commands in batch without verifying each
- Move to the next command before the current one passes all trial runs
- Skip trial runs because "batching is more efficient"

Deploying untested commands = deploying untested prompts. It is a violation of quality standards.

## Phase 3: Verify Checklist

Before finishing, confirm every item below.

### RED Phase
- [ ] Baseline run completed without the target command
- [ ] Agent's actual execution sequence documented
- [ ] Friction points categorized and traced to specific baseline steps

### GREEN Phase
- [ ] Minimal command addresses the specific baseline failures documented in RED
- [ ] Trial run reaches end without getting stuck
- [ ] Trial run covers every RED scenario
- [ ] User's original request is fully resolved
- [ ] Referenced skills / tools / file paths exist and are correct

### REFACTOR Phase
- [ ] New friction points found during trial run are fixed
- [ ] Re-run passes after each fix
- [ ] Command produces consistent results across scenarios
- [ ] Rationalization table updated with newly observed excuses and counters

### Quality Checks
- [ ] `references/anthropic-best-practices.md` has been read; key constraints applied (concise, CSO description, consistent terminology, appropriate degree of freedom)
- [ ] YAML frontmatter present; `description` describes trigger scenario (not step summary)
- [ ] Content language: Chinese body, English technical terms / identifiers / paths / command names
- [ ] Focused scope: one command does one thing
- [ ] No overlap or functional duplication with existing `commands/*.md`
- [ ] Saved to correct path: `commands/<command-name>.md` (kebab-case)

### Deployment
- [ ] Command committed to git
- [ ] If this command replaces or extends an existing command, update `install/renames.json` accordingly
- [ ] Command path under `commands/` matches the install layout expected by `local-install.py`

## Example: Creating a `quick-commit` Command

以下示例展示如何用本流程创建一个简化版的提交命令。

### RED — Baseline

**Scenario A (Primary)**: 用户说 "commit my code"。

| Step # | Agent action | Result | Friction? |
|--------|--------------|--------|-----------|
| 1 | `git status` | 看到修改文件 | - |
| 2 | `git add .` | 全部暂存 | Scope creep |
| 3 | `git commit -m "update"` | 提交成功 | Wrong quality |
| 4 | stops | 没有 push | Missing step |

| Friction type | Description | Caused by step # |
|---------------|-------------|------------------|
| Scope creep | 未询问用户就暂存所有文件 | Step 2 |
| Wrong quality | Commit message 没有描述性 | Step 3 |
| Missing step | 没有 push 到远程 | Step 4 |

**Scenario B (Boundary)**: 用户说 "commit my code --yes"。

| Step # | Agent action | Result | Friction? |
|--------|--------------|--------|-----------|
| 1 | `git status` | 看到修改文件 | - |
| 2 | `git add .` | 全部暂存 | Scope creep |
| 3 | `git commit -m "update"` | 提交成功 | Wrong quality |
| 4 | stops | 没有 push | Missing step |
| 5 | ignores `--yes` | 用户期望被跳过 | Ambiguity |

### GREEN — Draft Command

```markdown
---
description: Use when committing code and pushing to remote with a generated message and user confirmation
argument-hint: [optional-commit-message]
---

1. Run `git status` and show the result
2. Ask the user which files to stage
3. Stage the selected files
4. Generate a descriptive commit message from the diff
5. Confirm the message with the user
6. Commit and push
```

**Trial run**: 用户说 "commit my code" → command 执行全部步骤 → 代码提交并 push。

### REFACTOR

**New friction**: 用户有时不想确认 commit message；`--yes` 参数被忽略。

**Fix**: 添加 `--yes` 参数支持；默认仍需要确认。

```markdown
---
description: Use when committing code and pushing to remote with optional confirmation skip
argument-hint: [optional-commit-message] [--yes]
disable-model-invocation: false
---

1. Run `git status` and show the result
2. Ask the user which files to stage
3. Stage the selected files
4. Generate a descriptive commit message from the diff
5. If the user provided `--yes`, commit and push immediately; otherwise confirm the message first
6. Commit and push
```

Re-run primary and boundary scenarios until results are consistent.
