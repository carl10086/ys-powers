---
description: 智能 Git 工作流：分支创建、提交、推送、PR 一步完成
---

## 流程

```
分析变更 → 确定分支 → 执行推送 → 打开 PR
```

### 1. 分析 → 确定分支前缀

根据变更类型选择前缀：

| 变更类型 | 分支前缀 | 示例 |
|---------|---------|------|
| 新功能 | feature/ | feature/user-auth-0414 |
| Bug 修复 | fix/ | fix/login-crash-0414 |
| 重构 | refactor/ | refactor/api-cleanup-0414 |
| 文档 | docs/ | docs/readme-0414 |
| 格式调整 | style/ | style/formatting-0414 |
| 测试 | test/ | test/add-tests-0414 |
| 构建/工具 | chore/ | chore/deps-upgrade-0414 |

### 2. 执行 Git 操作

```bash
# 创建并切换分支
git checkout -b {前缀}{简短描述-月日}

# 暂存所有变更
git add .

# 提交（commitizen 格式）
git commit -m "type(scope): 简短描述"
```

**Commit 格式：**
- `type`: feat | fix | refactor | docs | style | test | chore
- `scope`: 模块/功能名（可选）
- `描述`: ≤50字，动词开头

**示例：**
```
feat(auth): 添加 JWT 登录
fix(order): 修复订单页面白屏问题
```

### 3. 推送 → 打开 PR

```bash
# 推送分支
git push -u origin HEAD
```

**自动打开 PR：**
推送成功后，使用 chrome devtools 打开 PR 页面：

```javascript
mcp__chrome-devtools__new_page("https://github.com/carl10086/{repo}/pull/new/{branch}")
```

## 特殊情况

| 情况 | 处理 |
|------|------|
| 分支已存在 | `git checkout {分支名}` 切换 |
| 推送失败 | 重试一次，仍失败提示用户 |
| 无变更 | 提示"无变更可提交" |
| 冲突 | 提示用户解决后继续 |
