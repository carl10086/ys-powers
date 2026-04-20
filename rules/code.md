Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

---

## Code Smells

Know these to avoid writing them, and recognize them during review.

### 5.1 Bloaters

| Smell | Recognition | Threshold | How to Avoid |
|-------|-------------|----------|--------------|
| Long Method | Function does too many things | > 20 lines | Single responsibility; extract early |
| Large Class | Class has too many responsibilities | > 200 lines | Single responsibility; extract subclasses |
| Long Parameter List | Too many arguments passed together | > 3 params | Introduce parameter object |
| Primitive Obsession | Same field groups repeated as primitives | Multiple occurrences | Extract dedicated type |
| Data Clumps | Same fields appear together everywhere | Repeated field groups | Extract shared object |

### 5.2 Dispensables

| Smell | Recognition | Threshold | How to Avoid |
|-------|-------------|----------|--------------|
| Dead Code | Unused variables, functions, or imports | Any unused code | Remove when discovered; don't accumulate |
| Duplicate Code | Same logic repeated in multiple places | Any repetition | Extract shared function |
| Speculative Generality | Unused abstractions "for future" | Unused interfaces/classes | Don't build what isn't needed yet |
| Comments | Code needs a comment to explain why it exists | Any "explains the why" comment | Fix the code, don't explain it |

### 5.3 Couplers

| Smell | Recognition | Threshold | How to Avoid |
|-------|-------------|----------|--------------|
| Feature Envy | Method heavily uses another class's data | Multiple methods accessing same external class | Move method to the data's class |
| Message Chains | `a.b().c().d()` chains | Chain > 2 | Introduce intermediate variable or restructure |
| Middle Man | Class delegates everything to another class | Delegation > 80% | Remove middleman; call directly |
| Inappropriate Intimacy | Classes know each other's internals | Cross-class internal access | Enforce encapsulation |

**When you spot a smell:** Flag it in review rather than silently working around it. "This function is 80 lines — consider splitting" is more helpful than working around the length.
