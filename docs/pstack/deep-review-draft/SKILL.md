---
name: deep-review
description: "Run a high-rigor review of a committed branch: first Standards and Spec, then verified behavioral failures and diff-external hidden coupling when the baseline has no merge blocker."
disable-model-invocation: true
---

# Deep review

Use this only for a high-risk committed change before merge.
Do not use it as the default review for ordinary changes.

## Load the owned contracts

Call the Skill tool with "code-review" for the Standards and Spec baseline.
Read and follow the installed `interrogate` and `blast-radius` skill instructions for the additional passes.
Stop if either additional contract is unavailable.
Do not copy or rewrite any owned review contract here.

## Freeze one scope

Require an explicit fixed point from the user.
Resolve the fixed point, merge base, and `HEAD` to commit SHAs.
Require `git status --porcelain` to be empty.
Require `git diff <fixed-point>...HEAD` to be non-empty.
Capture the exact diff command and `git log <fixed-point>..HEAD --oneline` once.
Identify the originating spec and the change intent before starting reviewers.
Give every reviewer the same scope manifest: fixed point, merge base, `HEAD`, diff command, commit list, spec source, and intent.
Stop rather than silently reviewing a different scope.

## Run the baseline gate

Execute the loaded `code-review` contract with the frozen fixed point and spec source.
Keep its Standards and Spec reviewers in separate fresh contexts.
Preserve its two reports without merging or reranking them.
Treat a documented-standard breach as a baseline blocker.
Treat a missing, partial, extra, or wrongly implemented spec requirement as a baseline blocker when it makes the change unmergeable.
Do not treat a Fowler smell heuristic by itself as a blocker.
If a baseline blocker exists, report Standards and Spec, explain that the expensive passes were skipped, and stop.

## Preflight isolated proof work

Before running executable probes, declare the checkout, dependency tree, process, port, database, account, fixture, credential, and cleanup boundaries.
Use independent disposable workspaces and dependency trees.
Never symlink a live checkout's dependency tree into a review workspace.
Never use production data, production accounts, or production credentials.
Assign unique ports and data namespaces when a probe starts a service.
Keep repro scripts and outputs in disposable scratch locations.
Stop if the required isolation cannot be established.

## Run the additional passes

Run the loaded `interrogate` and `blast-radius` contracts against the same frozen scope and intent.
Give them independent workspaces so one pass cannot influence the other's evidence.
Keep `interrogate` findings only when its coordinator reruns the exact command and confirms that the output violates the intent.
Disable the optional `arena` escalation inside `blast-radius` for this version of `deep-review`.
Require `blast-radius` to separate confirmed, cleared, and unproven risks.
Do not let either pass modify product code or apply fixes.

## Clean up before reporting

Run cleanup even when a probe or reviewer fails.
Remove disposable workspaces, scratch files, temporary data, and test accounts created by the review.
Stop services and release ports started by the review.
Verify that tracked files, dependency trees, processes, ports, and review data returned to their pre-review state.
Report cleanup as failed when any residue remains.

## Report

Return these sections in this order: `Standards`, `Spec`, `Verified behavioral failures`, `Hidden coupling`, `Unproven risks`, and `Cleanup`.
Keep each section's original evidence policy and confidence language.
Cross-reference duplicate findings, but do not delete them or collapse the sections.
Do not create one severity ranking across sections.
State which passes ran, which were skipped, and why.
Do not apply fixes or create commits.
