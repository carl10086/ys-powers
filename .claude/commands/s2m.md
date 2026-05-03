---
name: switch-to-main
description: Use when working in a git worktree and need to return to main branch, update it, and clean up the worktree environment
---

# Switch to Main

## Overview

一个用于在 git worktree 环境中安全返回 main 分支的标准化流程。处理分支检查、main 更新、冲突解决和 worktree 清理。

## When to Use

- 在 git worktree 中完成特性开发或修复后
- 需要同步最新 main 分支代码时
- 准备删除临时 worktree 环境时

## When NOT to Use

- 当前分支有未提交的更改（应先提交或 stash）
- 当前不在 worktree 环境中（直接使用 `git checkout main`）

## Core Pattern

```
检查当前分支状态
  ↓
确认处于 worktree 环境
  ↓
切换到 main 分支
  ↓
拉取最新 main（自动处理冲突）
  ↓
删除 worktree
```

## Quick Reference

| 步骤 | 命令 | 说明 |
|------|------|------|
| 检查分支 | `git branch --show-current` | 确认当前所在分支 |
| 检查 worktree | `git worktree list` | 查看所有 worktree |
| 切换 main | `git checkout main` | 切换到主分支 |
| 更新 main | `git pull origin main` | 拉取最新代码 |
| 解决冲突 | `git merge --abort` 或手动解决 | 如有冲突 |
| 删除 worktree | `git worktree remove <path>` | 清理 worktree |

## Implementation

### 完整流程

```bash
# 1. 检查当前分支
git branch --show-current

# 2. 检查是否在 worktree 中
git worktree list

# 3. 切换到 main 分支
git checkout main

# 4. 更新 main
git pull origin main

# 5. 如果有冲突，自动处理
# 使用合并策略或手动解决

# 6. 删除 worktree
git worktree remove <worktree-path>
```

### 冲突处理

```bash
# 放弃当前合并（如需重新开始）
git merge --abort

# 或：接受远程版本
git checkout --theirs .

# 或：接受本地版本
git checkout --ours .
```

## Common Mistakes

| 错误 | 后果 | 修复 |
|------|------|------|
| 未提交更改直接切换 | 丢失工作 | 先 `git stash` 或提交 |
| 在 main 上直接开发 | 污染主分支 | 创建新分支或使用 worktree |
| 强制删除 worktree | 丢失未保存文件 | 使用 `git worktree remove` |

## Red Flags

- 当前有未跟踪文件（应清理或提交）
- main 分支有本地未推送提交（应先处理）
- worktree 中包含子模块（需额外处理）
