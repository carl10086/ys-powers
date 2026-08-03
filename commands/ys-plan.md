---
description: Break work into small verifiable tasks with acceptance criteria and dependency ordering
disable-model-invocation: true
---

Invoke the planning-and-task-breakdown skill.

Read the spec for this feature. If a spec was generated earlier in this session, use that file path. Otherwise, check `docs/ys-powers/specs/` for the most recent spec file, or ask the user for the spec path if ambiguous. Then read the relevant codebase sections. Then:

<HARD-RULE name="plan-no-code-changes">

- Read only — no code changes。仅本命令产物 `docs/ys-powers/plans/YYYY-MM-DD-<feature-name>.md` 可写。

</HARD-RULE>

1. Identify the dependency graph between components
3. Slice work vertically (one complete path per task, not horizontal layers)
4. Write tasks with acceptance criteria and verification steps
5. Add checkpoints between phases
6. Present the plan for human review

<IMPORTANT>
- Write the plan content in Chinese. Keep technical terms, code identifiers, file paths, and command names in English.
- Save the plan to `docs/ys-powers/plans/YYYY-MM-DD-<feature-name>.md` where `<feature-name>` is a kebab-case short name derived from the plan title.
- If the directory does not exist, create it first.
- Auto-save without asking for path confirmation. Print the final saved path on completion.
</IMPORTANT>
