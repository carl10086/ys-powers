---
description: Review and improve spec documents across six dimensions with 0-10 scoring, quality gate, and up to 3 review rounds
disable-model-invocation: true
---

## Phase 1: Load Context

1. Locate the spec file:
   - If user provided a path, use it
   - Otherwise, find the most recent `.md` in `docs/ys-powers/specs/`
   - If none found, ask user for the spec path

2. Read the spec file + project context:
   - `CLAUDE.md` (if exists) — for project conventions
   - `package.json` / `Cargo.toml` / `go.mod` (if exists) — for tech stack validation
   - Existing directory structure — for structure consistency

## Phase 2: Six-Dimension Review

Evaluate the spec against these dimensions. For each finding, classify as:
- **AUTO-FIX** — mechanical issue (format, missing element, vague wording). Fix directly.
- **ASK** — judgment call (scope, architecture, trade-off). Surface to user with recommendation.
- **PASS** — no issue.

Each dimension scored **0-10**. Quality Gate: avg ≥ 7.0 and no dimension < 5.

### Dimension 1: Completeness (0-10)
Check if all required sections exist and are substantive:
- [ ] Objective — has "what", "why", and "who"
- [ ] Tech Stack — specific versions/frameworks listed
- [ ] Commands — full executable commands (not just tool names)
- [ ] Project Structure — directory layout with descriptions
- [ ] Code Style — at least one real code snippet + naming conventions
- [ ] Testing Strategy — framework, coverage, test levels
- [ ] Boundaries — Always / Ask First / Never defined
- [ ] Success Criteria — specific, testable conditions (not vibes)
- [ ] Open Questions — unresolved items explicitly listed (can be "none")

### Dimension 2: Clarity (0-10)
Check for ambiguity and consistency:
- [ ] Terminology is consistent throughout (same concept = same word)
- [ ] Commands are copy-paste runnable in the target environment
- [ ] Directory paths match actual project structure
- [ ] Success Criteria have unambiguous pass/fail definitions
- [ ] Boundaries are explicit (no implicit assumptions)

### Dimension 3: Feasibility (0-10)
Check if the design can be implemented:
- [ ] Tech Stack versions are compatible with existing dependencies
- [ ] Commands reference tools available in the environment
- [ ] Project Structure can be merged into existing codebase
- [ ] Testing Strategy is executable (framework configured or easy to add)
- [ ] No over-engineering for current phase

### Dimension 4: Consistency (0-10)
Check alignment with existing project:
- [ ] Code Style matches existing conventions (check 2-3 source files)
- [ ] Naming conventions align with existing code
- [ ] Architecture patterns follow existing project structure
- [ ] Boundaries don't contradict CLAUDE.md rules

### Dimension 5: Testability (0-10)
Check if "done" is verifiable:
- [ ] Each Success Criteria has a corresponding test method
- [ ] Edge cases are covered (not just happy path)
- [ ] Manual verification items are minimized
- [ ] Criteria are independently testable

### Dimension 6: Simplicity (0-10)
Check for unnecessary complexity:
- [ ] MVP is identifiable from the spec
- [ ] No premature abstractions (plugin system, microservices, event bus in Phase 1)
- [ ] File/directory count is proportional to feature complexity
- [ ] Can the same value be delivered with fewer components?

## Phase 3: Apply Fixes, Score, and Re-Review Loop

### Scoring Rules
- **10**: Excellent — no issues, exemplary spec
- **8-9**: Good — minor gaps, easily fixed
- **6-7**: Acceptable — noticeable issues, needs some fixes
- **4-5**: Weak — significant gaps, must improve before build
- **0-3**: Poor — fundamentally incomplete or misaligned

### Round 1: Initial Review
1. Evaluate all 6 dimensions, score each, collect findings
2. Apply all AUTO-FIX items directly to the spec file
3. Present score table + ASK items to user
4. Ask: "Continue to Round 2/3 to re-review after fixes? [yes / no]"

### Round 2+: Re-Review (if user says yes and round ≤ 3)
1. Re-read the modified spec file
2. Re-evaluate all 6 dimensions
3. Output **score delta table** showing changes from previous round

```
| Dimension    | R{N-1} | R{N} | Δ     |
|-------------|--------|------|-------|
| Completeness| 7      | 9    | ↑+2   |
```

4. Apply any new AUTO-FIX items
5. If score converged (no change from previous round) → "Scores converged. Finalizing."
6. Otherwise, if round < 3 → ask to continue; if round == 3 → finalize

### Convergence Conditions
- **Early exit**: Two consecutive rounds with identical scores → stop, report convergence
- **Max rounds**: 3 rounds total
- **Forced finalize**: After Round 3, output final report regardless of score

## Phase 4: Final Report

```
SPEC REVIEW REPORT — Round {N}/3
══════════════════════════════════════════════════
Spec:     {file-path}
Score:    {total}/60 (avg {avg:.1f})  Gate: {PASS / NEEDS_IMPROVEMENT}
Rounds:   {N} (converged: {yes/no})

Dimension      Score  Findings        Action
─────────────  ─────  ──────────────  ──────────
Completeness   {s}/10 {n} findings     {pass/ask/fix}
Clarity        {s}/10 {n} findings     {pass/ask/fix}
Feasibility    {s}/10 {n} findings     {pass/ask/fix}
Consistency    {s}/10 {n} findings     {pass/ask/fix}
Testability    {s}/10 {n} findings     {pass/ask/fix}
Simplicity     {s}/10 {n} findings     {pass/ask/fix}

Auto-fixed:  {N} items
Ask items:   {N} items

[If converged after re-review]
✓ Quality converged at Round {N}. No further improvements detected.

[If not converged and N == 3]
⚠ Max rounds reached. Remaining issues require manual decisions.

[If gate FAILED]
⚠ Quality Gate failed (avg < 7.0 or dimension < 5). Recommend addressing
  blocking items before proceeding to /build.

[If ASK items exist]
待确认项：
1. [Dimension] Issue → Recommended: ...
2. ...

══════════════════════════════════════════════════
VERDICT: {Ready for build / Needs improvement / Blocked}
```

## Hard Rules

- **Read before judging** — always read at least one source file to verify Code Style consistency
- **Project stack over personal preference** — if spec contradicts existing conventions, flag it
- **Quantify the vague** — every "better/faster/easier" must have a number or test
- **YAGNI by default** — challenge abstractions unless spec justifies them with concrete use cases
- **Preserve user intent** — auto-fix mechanical issues, never auto-cut scope without asking
- **Score honestly** — a 10 means you'd show this spec to a new engineer with zero context
