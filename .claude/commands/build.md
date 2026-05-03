---
description: Implement the next task incrementally — build, test, verify, commit
---

Invoke the incremental-implementation skill alongside test-driven-development.

Read the plan for this feature. If a plan was generated earlier in this session, use that file path. Otherwise, check `docs/ys-powers/plans/` for the most recent plan file, or ask the user for the plan path if ambiguous. Then pick the next pending task. For each task:

1. Read the task's acceptance criteria
2. Load relevant context (existing code, patterns, types)
3. Write a failing test for the expected behavior (RED)
4. Implement the minimum code to pass the test (GREEN)
5. Run the full test suite to check for regressions
6. Run the build to verify compilation
7. Commit with a descriptive message
8. Mark the task complete and move to the next one

If any step fails, follow the debugging-and-error-recovery skill.
