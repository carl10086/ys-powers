---
description: Cleanup: prune docs/ys-powers/ files older than N days by filename date
disable-model-invocation: true
---

Prune files in `./docs/ys-powers/` whose filename date prefix is older than N days. Default is 7 days.

Pass the number of days as the argument, e.g. `/ys-cleanup 14`. If no argument is given, use 7.

## Steps

1. Verify `./docs/ys-powers/` exists. If missing, report and stop.
2. Resolve the cleanup script path:
   - If `.claude/commands/scripts/ys-cleanup.sh` exists, use it (local install).
   - Otherwise use `~/.claude/commands/scripts/ys-cleanup.sh` (global install).
3. Run the script with the requested number of days: `bash <script-path> ./docs/ys-powers ${ARGUMENTS:-7}`.
4. If the script reports "Nothing to clean", stop.
5. If the script lists stale files, it will prompt for confirmation before deleting. Wait for the user to confirm or cancel.
6. Report the script's final result (deleted count or cancelled).

## Safety

- Only files matching `YYYY-MM-DD*` filename pattern are candidates.
- Only files with date prefix strictly before the cutoff are deleted.
- The script asks for explicit confirmation before deleting anything.
- Empty directories are left untouched.
