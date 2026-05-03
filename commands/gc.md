---
description: 智能 Git 工作流：分支创建、提交、推送、PR 一步完成
---

## 安全红线

- 永远不 force push 到 main/master
- 永远不提交包含密钥/token/credentials 的变更
- 不要跳过 Git 冲突解决直接提交
- 不要在未确定分支前缀正确前执行 push
- 不要 hardcode 路径
- 不要自动合并冲突（除非用户明确授权）

## Commit 格式

`type(scope): 描述`（≤50 字，动词开头）

**示例：**
```
feat(auth): 添加 JWT 登录
fix(order): 修复订单页面白屏问题
```

**type 选项：** feat | fix | refactor | docs | style | test | chore

## Workflow

复制此清单并逐项勾选：

```
- [ ] 1. 预检工作区 → verify: git status 干净或已处理
- [ ] 2. 分析变更，确定分支前缀 → verify: 前缀匹配变更类型
- [ ] 3. 创建并切换分支 → verify: 分支名符合 {前缀}{描述-月日}
- [ ] 4. 暂存并提交 → verify: commit message 格式正确
- [ ] 5. 推送并打开 PR → verify: push 成功，PR 页面已打开
```

### 1. 预检工作区

```bash
git status --short
```

**输出非空？** → 存在未提交变更，展示摘要并询问：

```
检测到未提交变更：
 M src/config.ts
?? docs/todo.md

处理方式：
1. 一并提交（默认）
2. 取消 gc，让我手动处理

选择 [1]:
```

- 「一并提交」→ 所有变更纳入本次 commit，继续流程
- 「取消」→ 终止流程

### 2. 确定分支前缀

| 变更类型 | 分支前缀 | 示例 |
|---------|---------|------|
| 新功能 | feature/ | feature/user-auth-0414 |
| Bug 修复 | fix/ | fix/login-crash-0414 |
| 重构 | refactor/ | refactor/api-cleanup-0414 |
| 文档 | docs/ | docs/readme-0414 |
| 格式调整 | style/ | style/formatting-0414 |
| 测试 | test/ | test/add-tests-0414 |
| 构建/工具 | chore/ | chore/deps-upgrade-0414 |

### 3. 创建并切换分支

```bash
git checkout -b {前缀}{简短描述-月日}
```

### 4. 暂存并提交

```bash
git add .
git commit -m "type(scope): 简短描述"
```

### 5. 推送并打开 PR

```bash
git push -u origin HEAD
```

推送成功后打开 PR 页面：

```javascript
mcp__chrome-devtools__new_page("https://github.com/carl10086/{repo}/pull/new/{branch}")
```

## 执行后自检

- [ ] 分支名符合 {前缀}{描述-月日} 规范
- [ ] commit message 格式正确
- [ ] 没有 secrets/keys/tokens 泄露
- [ ] push 到远程成功
- [ ] 未提交变更已妥善处理（如适用）

## 异常情况处理

| 情况 | 处理 |
|------|------|
| 分支已存在 | `git checkout {分支名}` 切换 |
| 推送失败 | 重试一次，仍失败提示用户 |
| 无变更 | 提示"无变更可提交" |
| 冲突 | 提示用户解决后继续 |
