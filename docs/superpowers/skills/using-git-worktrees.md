# using-git-worktrees

**定位**：在开始需要隔离的功能工作、或执行 implementation plan 前，确保存在隔离工作区。

**触发条件**：需要隔离当前工作区，或在执行 plan 前准备干净工作区。

---

## 核心原则

- 先检测是否已有隔离。
- 优先用平台原生 worktree 工具。
- 没有原生工具才用 `git worktree add`。
- 永远别和 harness 对着干。

## Step 0: 检测现有隔离

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
BRANCH=$(git branch --show-current)
```

- 如果 `GIT_DIR != GIT_COMMON` 且不是 submodule：已在 linked worktree，跳到 Step 2。
- 如果是 submodule：当作普通仓库处理。
- 普通仓库：询问用户是否需要创建 worktree（若指令未声明偏好）。

## Step 1: 创建隔离工作区

### 1a. 原生工具（优先）

如果平台有 `EnterWorktree`、`WorktreeCreate`、`/worktree` 命令或 `--worktree` 标志，使用它。不要再用 `git worktree add`，否则会产生 harness 看不到的 phantom state。

### 1b. Git worktree 回退

- 目录优先级：用户显式偏好 > 项目已存在的 `.worktrees/` > `worktrees/` > 默认 `.worktrees/`。
- 创建前必须用 `git check-ignore` 确认目录已被忽略；否则先加 `.gitignore` 并提交。
- `git worktree add "$path" -b "$BRANCH_NAME"`。
- 若 sandbox 拒绝，向用户说明并在当前目录工作。

## Step 2: 项目初始化

根据项目类型自动安装依赖：

- `package.json` → `npm install`
- `Cargo.toml` → `cargo build`
- `requirements.txt` / `pyproject.toml` → pip/poetry
- `go.mod` → `go mod download`

## Step 3: 验证干净基线

跑测试确认起点干净：

```bash
npm test / cargo test / pytest / go test ./...
```

- 测试失败：报告并询问是否继续。
- 测试通过：报告准备就绪。

## 常见错误

- 已有隔离还创建 worktree。
- 放着原生工具不用，直接用 `git worktree add`。
- 没确认 `.worktrees/` 已 ignore。
- 未验证干净基线就开工。
