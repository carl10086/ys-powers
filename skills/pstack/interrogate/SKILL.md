---
name: interrogate
description: "Run an adversarial review that keeps only behavioral failures proven by rerunnable commands."
disable-model-invocation: true
---

# Interrogate

Adversaries try to break a change or a design. A finding survives only when a run proves it. Report the findings. Do not apply fixes.

## Frame

The scope is what the user names. Otherwise it is the branch diff from its merge base with the base branch, through the working tree.

Restate the intent in your own words from the user's message, the commits, and the PR description. Ask the user when the intent is unclear. The intent is the standard every finding must break.

## Fan out

Spawn two or three `generalPurpose` adversaries in one batch. Prefer different model families when the runtime supports them; otherwise use the available models. Each adversary gets an isolated git worktree containing the same committed and uncommitted scope. If worktrees are unavailable, use separate temporary copies. Stop and report the isolation failure when fewer than two adversaries can run without sharing writable state.

Give every adversary the same scope, intent, and brief:

> Break this change. Prove each finding with a run against the real code, such as a failing test, a repro script, or command output that shows the wrong behavior. For a design or plan, run a prototype or probe the current tree. Keep repros in your isolated workspace. Report each finding with a title, the exact command, the output it printed, and the output the intent requires. Leave out anything you did not run. That excludes style, naming, structure, and risks that need a future change to matter. No findings is a valid result.

If an adversary produces no output, continue with the others and record the dropout.

## Verify

Rerun every reported command against the same scope. Keep a finding only when the rerun shows the failure and the failure breaks the intent. Drop the rest. Merge findings that share a root cause. Never accept an adversary's self-report as proof.

## Output

- **Intent**: the restatement.
- **Findings**: for each verified finding, the command, its output, how it breaks the intent, and the adversaries that found it. Say "no verified findings" when none survive.
- **Dropped**: for each adversary, the count of dropped findings and why, plus any dropout or runtime degradation.
