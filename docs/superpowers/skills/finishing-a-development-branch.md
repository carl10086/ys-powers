# finishing-a-development-branch

**定位**：实现完成、测试通过后，提供结构化的分支收尾选项（合并 / PR / 保留 / 丢弃）。

**触发条件**：所有实现任务完成、测试通过，需要决定如何集成工作。

---

## 核心流程

```
Verify Tests → Detect Environment → Determine Base → Present Options → Execute Choice → Cleanup
```

## Step 1：验证测试

在展示任何选项之前先跑测试。测试失败就停下，不修好不继续。

## Step 2：检测环境

通过比较 `GIT_DIR` 与 `GIT_COMMON_DIR` 判断当前工作区状态：

| 状态 | 菜单 | 清理 |
|---|---|---|
| 普通仓库 | 4 个选项 | 无 worktree |
| worktree + 命名分支 | 4 个选项 | 清理 superpowers 创建的 worktree |
| detached HEAD | 3 个选项（无本地合并） | 不清理，外部管理 |

## Step 3：确定 base branch

通常 `main`；向用户确认。

## Step 4：呈现选项

**普通仓库 / 命名分支 worktree：**

1. Merge back to `<base-branch>` locally
2. Push and create a Pull Request
3. Keep the branch as-is
4. Discard this work

**Detached HEAD：**

1. Push as new branch and create a Pull Request
2. Keep as-is
3. Discard this work

选项必须原样呈现，不加解释。

## Step 5：执行选择

- **Merge locally**：先合并并验证测试，成功后再清理 worktree、删除分支。
- **Create PR**：推送分支，**不清理 worktree**（用户还要迭代）。
- **Keep as-is**：保留 worktree。
- **Discard**：要求用户输入 `discard` 确认，再清理 worktree 并强制删除分支。

## Step 6：清理 worktree

仅对选项 1 和 4 执行，且只清理 superpowers 自己创建的 worktree（路径在 `.worktrees/` 或 `worktrees/` 下）。执行前必须先 `cd` 到主仓库根目录，再 `git worktree remove`。

## 常见错误

- 测试没通过就提供选项。
- 创建 PR 后误删 worktree。
- 在 worktree 内部执行 `git worktree remove`。
- 未确认就丢弃工作。
