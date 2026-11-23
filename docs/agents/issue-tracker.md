# Issue tracker：GitHub

本仓库的 issues 和 specs 位于 GitHub Issues。所有操作使用 `gh` CLI。

## Conventions

- **Create an issue**：`gh issue create --title "..." --body "..."`；多行 body 使用 heredoc。
- **Read an issue**：`gh issue view <number> --json number,title,body,labels,comments`。
- **List issues**：使用 `gh issue list --state open --json number,title,body,labels,comments`，并按需使用 `--label` 与 `--state` 过滤。
- **Comment on an issue**：`gh issue comment <number> --body "..."`。
- **Apply / remove labels**：`gh issue edit <number> --add-label "..."` / `--remove-label "..."`。
- **Close**：先发表评论，再执行 `gh issue close <number>`。

从 `git remote -v` 推断仓库；在本 clone 内运行 `gh` 时会自动使用该仓库。仅向用户自己的仓库创建 issues，不要向 `mattpocock/skills` 创建。

## Pull requests as a triage surface

**PRs as a request surface: no.**

## When a skill says “publish to the issue tracker”

创建 GitHub issue。

## When a skill says “fetch the relevant ticket”

按上面的 Read an issue 方式读取。
